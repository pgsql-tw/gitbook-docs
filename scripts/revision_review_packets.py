"""Experimental revision packets. No publication; unresolved changes fail closed."""
import argparse
import difflib
import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path
from html.parser import HTMLParser
from translation_packets import estimate_tokens, SourceIndex, packet, render
from translation_pipeline import parts

def read(path):
    return Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n')

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

class Terms(HTMLParser):
    """Extract complete dt+dd entries with exact character provenance."""
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.entries, self.current, self.depth = text, [], None, 0
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1]+len(line))
        self.feed(text)
    def pos(self):
        line, col = self.getpos()
        return self.offsets[line-1]+col
    def handle_starttag(self, tag, attrs):
        if tag == 'dt' and dict(attrs).get('id'):
            self.current = dict(anchor=dict(attrs)['id'], start=self.pos())
        if tag == 'dd' and self.current:
            self.depth += 1
    def handle_endtag(self, tag):
        if tag == 'dd' and self.current:
            self.depth -= 1
            if self.depth == 0:
                self.current['end'] = self.text.find('>', self.pos())+1
                self.entries.append(self.current)
                self.current = None

def spans(text, entries):
    ids = {e['anchor'] for e in entries}
    # A table/section anchor also terminates a preceding definition entry.
    # Ignoring non-dt anchors falsely attributes later table prose to that dt.
    anchors = [(m.start(), m[1]) for m in re.finditer(r'<a\s+id="([^"]+)"[^>]*>', text)]
    result=[]
    for i,(start,a) in enumerate(anchors):
        if a not in ids: continue
        end=anchors[i+1][0] if i+1<len(anchors) else len(text)
        heading=re.search(r'^#{1,6}\s',text[start:end],re.MULTILINE)
        if heading: end=start+heading.start()
        result.append(dict(anchor=a,start=start,end=end))
    return result

def covered(lo,hi,units):
    """A partial overlap must not certify the rest of a changed range."""
    if lo==hi: return True
    cursor=lo
    for s in sorted(units,key=lambda s:s['start']):
        if s['end']<=cursor: continue
        if s['start']>cursor: break
        cursor=max(cursor,s['end'])
        if cursor>=hi: return True
    return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--old', required=True); p.add_argument('--new', required=True)
    p.add_argument('--source', required=True); p.add_argument('--prior', required=True)
    p.add_argument('--out', required=True); p.add_argument('--local', action='store_true')
    p.add_argument('--manifest', required=True)
    args=p.parse_args()
    old,new,html=read(args.old),read(args.new),read(args.source)
    entries=Terms(html).entries
    lookup={e['anchor']:e for e in entries}
    oldsp,newsp=spans(old,entries),spans(new,entries)
    a,b=old.splitlines(keepends=True),new.splitlines(keepends=True)
    ao,bo=[0],[0]
    for line in a: ao.append(ao[-1]+len(line))
    for line in b: bo.append(bo[-1]+len(line))
    changed=[]; selected=set(); unresolved=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=='equal': continue
        hits={s['anchor'] for ss,lo,hi in ((oldsp,ao[i],ao[j]),(newsp,bo[k],bo[l])) for s in ss if s['start']<max(hi,lo+1) and s['end']>lo}
        changed.append(dict(kind=tag,old_lines=[i+1,j],new_lines=[k+1,l],old=''.join(a[i:j]),new=''.join(b[k:l]),anchors=sorted(hits)))
        selected.update(hits)
        if not hits or not covered(ao[i],ao[j],oldsp) or not covered(bo[k],bo[l],newsp):
            unresolved.append(dict(**changed[-1],reason='all or part of change lacks supported alignment; broader review required'))
    prior=json.loads(read(args.prior))
    records=[]
    for anchor in sorted(selected):
        os=next((s for s in oldsp if s['anchor']==anchor),None)
        ns=next((s for s in newsp if s['anchor']==anchor),None)
        if not os or not ns:
            unresolved.append(dict(anchor=anchor,reason='anchor removed or added; broader review required')); continue
        e=lookup[anchor]
        record=dict(anchor=anchor,source_range=[e['start'],e['end']],official_html=html[e['start']:e['end']],old_translation=old[os['start']:os['end']],new_translation=new[ns['start']:ns['end']],old_range=[os['start'],os['end']],new_range=[ns['start'],ns['end']])
        if args.local:
            # Model only verifies correspondence; cannot drop records or decide pass/fail.
            body={'messages':[{'role':'system','content':'唯讀檢查中英文是否描述同一個命令或選項。不要審查正確性；不要修改引句。JSON aligned=true 僅表示主題對應，不能表示譯文通過。'},{'role':'user','content':json.dumps(record,ensure_ascii=False)}], 'temperature':0,'max_tokens':200,'chat_template_kwargs':{'enable_thinking':False},'response_format':{'type':'json_schema','json_schema':{'name':'alignment','schema':{'type':'object','properties':{'aligned':{'type':'boolean'},'reason':{'type':'string'}},'required':['aligned','reason'],'additionalProperties':False}}}}
            started=time.monotonic()
            token_req=urllib.request.Request('http://127.0.0.1:18080/tokenize',data=json.dumps({'content':json.dumps(body,ensure_ascii=False),'add_special':False}).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(token_req,timeout=60) as response: input_tokens=len(json.load(response)['tokens'])
            if input_tokens>7400:
                record['local_alignment']=dict(aligned=False,reason='input exceeds conservative 8192 context budget; no truncation permitted')
                unresolved.append(dict(anchor=anchor,reason=record['local_alignment']['reason']))
                records.append(record)
                continue
            req=urllib.request.Request('http://127.0.0.1:18080/v1/chat/completions',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=180) as response: raw=json.load(response)
            record['local_alignment']=json.loads(raw['choices'][0]['message']['content'])
            record['local_seconds']=round(time.monotonic()-started,2)
            if not record['local_alignment'].get('aligned'): unresolved.append(dict(anchor=anchor,reason='model uncertain; broader review required'))
        records.append(record)
    # Compare old section-scoped official packets for every affected heading section.
    revision_parts=parts(old)
    original_baseline=json.loads(read(args.manifest))['baseline']
    originals=parts(original_baseline); translations=parts(new)
    if len(originals)!=len(translations) or len(revision_parts)!=len(originals):
        raise ValueError('heading structure changed; section comparison requires manual mapping')
    affected_set=set()
    for sections,offsets,key in ((revision_parts,ao,'old_lines'),(translations,bo,'new_lines')):
        offset=0
        for idx,section in enumerate(sections):
            if any(offset < max(offsets[c[key][1]], offsets[c[key][0]-1]+1) and offset+len(section)>offsets[c[key][0]-1] for c in changed): affected_set.add(idx)
            offset+=len(section)
    affected=sorted(affected_set)
    index=SourceIndex(html,originals)
    manifest=json.loads(read(args.manifest))
    baseline_packets=[render(packet(index,originals,translations,[i],manifest['source'],manifest.get('submission'))) for i in affected]
    baseline=sum(estimate_tokens(text) for text in baseline_packets)
    result=dict(version='revision-packets-experiment-v1',scope='revision-only, NOT full-page approval',unchanged_scope_status='not certified by this experiment; requires valid prior coverage before publication',hashes=dict(old=sha(old),new=sha(new),source=sha(html)),prior_issues=prior['errors'],changes=changed,records=records,unresolved_changes=unresolved,affected_sections=affected,old_packet_estimated_tokens=baseline)
    result['new_packet_estimated_tokens']=estimate_tokens(json.dumps(result,ensure_ascii=False))
    result['token_estimate_note']='Heuristic only; excludes shared reviewer instructions and local alignment call cost. Not cloud billing.'
    result['savings_percent']=round(100*(1-result['new_packet_estimated_tokens']/baseline),2) if baseline else None
    result['fallback_required']=bool(unresolved)
    if args.local:
        # Tokenization has no context-limit truncation or generation, unlike inference.
        def token_count(text):
            req=urllib.request.Request('http://127.0.0.1:18080/tokenize',data=json.dumps({'content':text,'add_special':False}).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=60) as response: return len(json.load(response)['tokens'])
        new_count=token_count(json.dumps(result,ensure_ascii=False))
        old_count=sum(token_count(text) for text in baseline_packets)
        result['actual_model_token_counts']=dict(old=old_count,new=new_count,savings_percent=round(100*(1-new_count/old_count),2),note='Qwen3 tokenizer; data packets only, excludes shared prompt, output and local inference. New count excludes this metrics field.')
        result['safe_review_model_tokens']=old_count if unresolved else new_count
    for record in records:
        start,end=record['source_range']
        assert html[start:end]==record['official_html']
        start,end=record['new_range']
        assert new[start:end]==record['new_translation']
        start,end=record['old_range']
        assert old[start:end]==record['old_translation']
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    if unresolved:
        out.with_suffix('.fallback.json').write_text(json.dumps(dict(scope='All affected heading sections; no delta-only review permitted',prior_issues=prior['errors'],packets=baseline_packets),ensure_ascii=False,indent=2),encoding='utf-8')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('affected_sections','old_packet_estimated_tokens','new_packet_estimated_tokens','savings_percent')},ensure_ascii=False))
    print(json.dumps(dict(changes=len(changed),records=len(records),unresolved=len(unresolved),local_seconds=sum(r.get('local_seconds',0) for r in records))))

if __name__=='__main__': main()
