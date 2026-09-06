"""Import missing PostgreSQL 15 manual pages without replacing existing prose.

Dependencies: markdownify==1.2.2, markdown-it-py==4.0.0 (installed in TEMP/pg15-doc-tools).
Stages: plan, fetch (network), render, apply, verify. Cached upstream HTML stays in TEMP.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from collections import Counter

sys.path.insert(0, str(Path(tempfile.gettempdir()) / 'pg15-doc-tools'))
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
AUDIT = ROOT / 'outputs/pg15-audit'
CACHE = Path(tempfile.gettempdir()) / 'pg15-original-html'
STAGE = Path(tempfile.gettempdir()) / 'pg15-original-markdown'
BASE = 'https://www.postgresql.org/docs/15/'

def read_csv(name):
    return list(csv.DictReader((AUDIT / name).open(encoding='utf-8-sig')))

def norm(s):
    s = re.sub(r'^(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?\s+', '', s)
    return re.sub(r'[^a-z0-9]', '', s.lower())

def clean_title(s):
    return ' '.join(s.split())

def number(s):
    m = re.match(r'^(\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?(?:\s|$)', s)
    return m[1] if m else ''

def body(s):
    return re.sub(r'^#+ .*$', '', re.sub(r'\A---\n.*?\n---\n', '', s, flags=re.S), flags=re.M).strip()

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def plan():
    es = read_csv('inventory.csv')
    comparison = read_csv('section-comparison.csv')
    upstream = json.loads((AUDIT / 'official-toc.json').read_text(encoding='utf-8'))
    nodes = {}
    mapping = {r['url'].removeprefix(BASE): r['local'] for r in comparison if r['local']}
    mapping.update({'queries-with.html': 'the-sql-language/queries/with-queries.md',
                    'predefined-roles.html': 'server-administration/database-roles/default-roles.md',
                    'index.html':'README.md', 'preface.html':'preface/README.md',
                    'tutorial.html':'tutorial/README.md', 'sql.html':'the-sql-language/README.md',
                    'admin.html':'server-administration/README.md', 'client-interfaces.html':'client-interfaces/README.md',
                    'server-programming.html':'server-programming/README.md', 'reference.html':'reference/README.md',
                    'internals.html':'internals/README.md', 'appendixes.html':'appendixes/README.md',
                    'sql-commands.html':'reference/sql-commands/README.md',
                    'reference-client.html':'reference/client-applications/README.md',
                    'reference-server.html':'reference/server-applications/README.md', 'biblio.html':'bibliography.md',
                    'contrib-dblink-function.html':'appendixes/additional-supplied-modules/dblink/dblink.md'})
    for x in upstream['index']['toc']:
        page = x['href']
        if page=='bookindex.html':
            continue  # Generated keyword index, not a manual chapter.
        n = number(x['title'])
        if page not in mapping:
            candidates = [e for e in es if e['level']=='1' and number(e['title'])==n and
                          (e['path'].startswith('preface/') if page in ['intro-whatis.html','history.html','notation.html','resources.html','bug-reporting.html'] else not e['path'].startswith('preface/'))]
            if not n.isdigit():
                candidates = [e for e in candidates if e['part'].startswith('VIII.')]
            if len(candidates)==1:
                mapping[page] = candidates[0]['path']
        if page not in mapping:
            raise ValueError(('Unmapped root', x))
        nodes[page] = dict(page=page, title=clean_title(x['title']), parent=None)

    root_pages = set(nodes)
    for c in upstream['chapters']:
        # Parts repeat the chapter entries; individual chapters provide their full subtree.
        if c['page'] not in root_pages or any(x['href'] in root_pages for x in c['toc']):
            continue
        previous_numbered = c['page']
        for x in c['toc']:
            page = x['href']
            if '#' in page or not page.endswith('.html'):
                continue
            title = clean_title(x['title'])
            n = number(title)
            parent = c['page']
            if n:
                previous_numbered = page
                prefix = n.rsplit('.',1)[0]
                ancestor = c['page'] if prefix==number(nodes[c['page']]['title']) else next((p for p, node in nodes.items() if number(node['title'])==prefix and node['parent']==c['page'] and p!=page), None)
                if '.' in n and ancestor:
                    parent = ancestor
            elif c['page'] not in ['sql-commands.html','reference-client.html','reference-server.html']:
                parent = previous_numbered
            nodes.setdefault(page, dict(page=page,title=title,parent=parent))
            if page not in mapping:
                local_chapter = next((e['chapter'] for e in es if e['path']==mapping[c['page']]), None)
                candidates = [e for e in es if e['chapter']==local_chapter and norm(e['title'])==norm(title)]
                if len(candidates)==1:
                    mapping[page]=candidates[0]['path']

    # New paths follow stable upstream slugs under the existing chapter folder.
    for page, node in nodes.items():
        if page in mapping:
            continue
        parent = node['parent']
        if parent not in mapping:
            raise ValueError(('Unmapped parent',node))
        parent_path = Path(mapping[parent])
        folder = parent_path.parent if parent_path.name=='README.md' else parent_path.with_suffix('')
        if parent in ['contrib.html','release.html','catalogs.html','views.html','information-schema.html']:
            if parent=='views.html':
                folder=Path('internals/system-views')
        slug = page.removesuffix('.html')
        if parent=='sql-commands.html':
            slug=re.sub(r'[^a-z0-9]+','-',node['title'].lower()).strip('-')
        elif parent in ['reference-client.html','reference-server.html']:
            slug=node['title']
        elif parent in ['catalogs.html','views.html','information-schema.html'] and re.search(r'\b(?:pg_|routine_)',node['title']):
            slug=re.sub(r'^\S+\s+','',node['title'])
        elif parent=='contrib.html':
            slug=re.sub(r'^\S+\s+','',node['title'])
        elif parent=='release.html':
            slug=page.removesuffix('.html')
        target=(folder/(slug+'.md')).as_posix()
        if (ROOT/target).exists():
            raise ValueError(('Existing unclassified file',page,target))
        mapping[page]=target

    reverse=Counter(mapping[p] for p in nodes)
    assert max(reverse.values())==1, [(p,n) for p,n in reverse.items() if n>1]
    for page,node in nodes.items():
        path=mapping[page]; p=ROOT/path
        original=p.read_text(encoding='utf-8-sig') if p.exists() else None
        node.update(path=path, action='new' if original is None else 'fill-empty' if not body(original) else 'preserve',
                    original_sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None)
    unmatched=[e for e in es if e['path'] not in {x['path'] for x in nodes.values()} and e['path']!='README.md']
    save('plan.json',{'base':BASE,'version':'15.19','created':datetime.now(timezone.utc).isoformat(),
                      'summary_sha256':hashlib.sha256((ROOT/'SUMMARY.md').read_bytes()).hexdigest(),
                      'nodes':list(nodes.values()),'unmapped_local':unmatched})
    print(Counter(n['action'] for n in nodes.values()))
    print('Unmapped local:',[(e['title'],e['path']) for e in unmatched])

def fetch():
    doc=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
    CACHE.mkdir(exist_ok=True)
    pages=[n['page'] for n in doc['nodes'] if n['action']!='preserve']
    def get(page):
        p=CACHE/page
        if not p.exists():
            req=urllib.request.Request(BASE+page,headers={'User-Agent':'PostgreSQL-TW-documentation-import/1.0'})
            with urllib.request.urlopen(req,timeout=60) as r:
                raw=r.read()
            p.write_bytes(raw)
        return page
    with ThreadPoolExecutor(max_workers=6) as pool:
        for i,p in enumerate(pool.map(get,pages),1):
            if i%30==0: print('Fetched',i,'/',len(pages),flush=True)
    print('Fetched',len(pages),'pages to',CACHE)

def raw_inline(el):
    s=str(el)
    for ch in '\\*_`[]':
        s=s.replace(ch,'&#'+str(ord(ch))+';')
    return s

class Converter(MarkdownConverter):
    def convert_br(self,el,text,parent_tags):
        if 'table-break' in el.get('class',[]):
            return '\n\n'
        return '<br>'
    def convert_code(self,el,text,parent_tags):
        if el.find(True):
            return raw_inline(el)
        return super().convert_code(el,text,parent_tags)
    convert_kbd=convert_code
    convert_samp=convert_code
    convert_tt=convert_code
    def convert_em(self,el,text,parent_tags):
        # Inline emphasis can touch punctuation/word suffixes where Markdown delimiters fail.
        return raw_inline(el)
    convert_i=convert_em
    def convert_strong(self,el,text,parent_tags):
        return raw_inline(el)
    convert_b=convert_strong
    def convert_pre(self, el, text, parent_tags):
        raw=el.get_text()
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',raw)),default=0))
        return '\n\n'+fence+'\n'+raw.rstrip('\n')+'\n'+fence+'\n\n'
    def convert_table(self, el, text, parent_tags):
        # PostgreSQL tables contain paragraphs, lists, spans and merged cells.
        return '\n\n'+str(el)+'\n\n'
    def convert_dt(self,el,text,parent_tags):
        return '\n\n'+text.strip()+'\n\n'
    def convert_dd(self,el,text,parent_tags):
        return '\n\n'+text.strip()+'\n\n'
    def convert_a(self,el,text,parent_tags):
        if not el.get('href') and (el.get('id') or el.get('name')):
            return '<a id="'+(el.get('id') or el['name'])+'"></a>'+text
        return super().convert_a(el,text,parent_tags)
    def convert_sup(self,el,text,parent_tags):
        return '<sup>'+text+'</sup>'
    def convert_sub(self,el,text,parent_tags):
        return '<sub>'+text+'</sub>'

def content(page):
    soup=BeautifulSoup((CACHE/page).read_text(encoding='utf-8'),'html.parser')
    container=soup.find(id='docContent')
    assert container, page
    for n in container.select('.navheader, .navfooter'):
        n.decompose()
    # Only DocBook content: exclude the site's correction form and footer.
    main=next((n for n in container.find_all(recursive=False) if set(n.get('class',[])) &
               {'sect1','sect2','sect3','chapter','appendix','part','preface','reference','refentry','bibliography'}),None)
    assert main is not None, (page,[n.get('class') for n in container.find_all(recursive=False)])
    return soup,main

def normalize_text(s):
    return re.sub(r'\s+','',s)

def render():
    doc=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
    nodes=doc['nodes']; bypage={n['page']:n for n in nodes}
    STAGE.mkdir(exist_ok=True)
    checks=[]
    renderer=MarkdownIt('commonmark',{'html':True}).enable('table')
    for node in nodes:
        if node['action']=='preserve':
            continue
        page=node['page']; soup,main=content(page)
        # Normalizing the page heading does not translate or change the body.
        heading=main.find(re.compile('^h[1-6]$'))
        assert heading, page
        heading_level=int(heading.name[1])
        display_title=node['title']
        if node['action']=='fill-empty':
            old=(ROOT/node['path']).read_text(encoding='utf-8-sig')
            old_heading=re.search(r'^# (.*)$',old,re.M)
            if old_heading:
                display_title=old_heading[1].replace('\\_','_')
                old_num=number(display_title); new_num=number(node['title'])
                if old_num and new_num:
                    display_title=re.sub(r'^'+re.escape(old_num)+r'(?=\.|\s|$)',new_num,display_title,count=1)
        heading.clear(); heading.string=display_title
        for h in main.find_all(re.compile('^h[1-6]$')):
            level=1 if h is heading else max(2,int(h.name[1])-heading_level+1+int('refentry' in main.get('class',[])))
            h.name='h'+str(min(6,level))
        # Keep all upstream fragment identifiers, including table and footnote anchors.
        for tag in list(main.find_all(id=True)):
            if tag.name=='a' or tag.find_parent('table') or tag.name=='table':
                continue
            anchor=soup.new_tag('a',id=tag['id'])
            del tag['id']
            if tag.name=='li': tag.insert(0,anchor)
            else: tag.insert_before(anchor)
        if main.get('id'):
            anchor=soup.new_tag('a',id=main['id']); del main['id']; main.insert(0,anchor)
        for link in main.find_all('a',href=True):
            url=urllib.parse.urljoin(BASE+page,link['href'])
            u=urllib.parse.urlsplit(url)
            target=u.path.removeprefix('/docs/15/') if u.netloc=='www.postgresql.org' else ''
            if target in bypage and not u.query:
                targetnode=bypage[target]
                # Imported pages preserve exact IDs. Existing translated page anchors are unknown.
                if not u.fragment or targetnode['action']!='preserve':
                    rel=os.path.relpath(targetnode['path'],Path(node['path']).parent).replace('\\','/')
                    link['href']=('' if target==page and u.fragment else rel)+('#'+u.fragment if u.fragment else '')
                else:
                    link['href']=url
            else:
                link['href']=url
            link.attrs.pop('title',None)
        for img in main.find_all('img',src=True):
            img['src']=urllib.parse.urljoin(BASE+page,img['src'])
        expected=normalize_text(main.get_text())
        source_pres=[p.get_text().rstrip('\n') for p in main.find_all('pre')]
        source_tables=[normalize_text(t.get_text()) for t in main.find_all('table')]
        md=Converter(heading_style='ATX',bullets='*',escape_underscores=False,escape_asterisks=True,wrap=False).convert(str(main)).strip()+'\n'
        lines=[]; fence=None; html_pre=False
        for line in md.splitlines():
            m=re.match(r'^\s*(`{3,}|~{3,})',line)
            inside=fence is not None or html_pre
            if m:
                if fence is None: fence=m[1]
                elif m[1][0]==fence[0] and len(m[1])>=len(fence): fence=None
            if '<pre' in line: html_pre=True
            # markdownify escapes literal asterisks in text. Use an HTML entity
            # outside code so GitBook renders the original character, not '\\*'.
            if not inside and not html_pre:
                line=line.replace('\\*','&#42;')
            lines.append(line if inside or html_pre else line.rstrip())
            if '</pre>' in line: html_pre=False
        md='\n'.join(lines)+'\n'
        rendered=BeautifulSoup(renderer.render(md),'html.parser')
        actual=normalize_text(rendered.get_text())
        pre_ok=[p.get_text().rstrip('\n') for p in rendered.find_all('pre')]==source_pres
        table_ok=[normalize_text(t.get_text()) for t in rendered.find_all('table')]==source_tables
        all_ids={t.get('id') or t.get('name') for t in main.find_all() if t.get('id') or t.get('name')}
        output_ids={t.get('id') or t.get('name') for t in rendered.find_all() if t.get('id') or t.get('name')}
        checks.append(dict(page=page,path=node['path'],text_equal=actual==expected,code_equal=pre_ok,table_equal=table_ok,
                           anchors_preserved=all_ids<=output_ids,source_code_blocks=len(source_pres),source_tables=len(source_tables),
                           html_sha256=hashlib.sha256((CACHE/page).read_bytes()).hexdigest()))
        md+='\n---\n\n原文：[PostgreSQL 15.19 Documentation]('+BASE+page+')（英文原文，待翻譯）\n'
        target=STAGE/node['path']; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(md,encoding='utf-8')
        if actual!=expected:
            import difflib
            diff=[]
            for kind,a,b,c,d in difflib.SequenceMatcher(None,expected,actual,autojunk=False).get_opcodes():
                if kind!='equal': diff.append({'source':expected[max(0,a-50):b+50], 'rendered':actual[max(0,c-50):d+50]})
            (STAGE/(page+'.diff.json')).write_text(json.dumps(diff,ensure_ascii=False,indent=2),encoding='utf-8')
    save('conversion-checks.json',checks)
    failed=[c for c in checks if not all(c[k] for k in ['text_equal','code_equal','table_equal','anchors_preserved'])]
    print('Rendered',len(checks),'pages. Failed:',len(failed))
    print([(c['page'],[k for k in ['text_equal','code_equal','table_equal','anchors_preserved'] if not c[k]]) for c in failed][:35])
    if failed: raise SystemExit(1)

def summary_and_headings(doc):
    original=(ROOT/'SUMMARY.md').read_text(encoding='utf-8-sig')
    tree={}; roots=[]; stack=[]
    for line in original.splitlines():
        m=re.match(r'(\s*)\* \[(.*?)\]\((.*?)\)',line)
        if not m: continue
        indent,title,path=m.groups(); path=path.replace('\\_','_'); title=title.replace('\\_','_')
        level=len(indent)//2
        while len(stack)>level: stack.pop()
        parent=stack[-1] if stack else None
        tree[path]={'path':path,'title':title,'children':[],'parent':parent}
        (tree[parent]['children'] if parent else roots).append(path)
        stack.append(path)
    bypage={n['page']:n for n in doc['nodes']}
    bypath={n['path']:n for n in doc['nodes']}
    touched=set(); moved=[]
    for n in doc['nodes']:
        parent=bypage[n['parent']]['path'] if n['parent'] else None
        if n['action']=='new':
            assert parent in tree,(n,parent)
            tree[n['path']]={'path':n['path'],'title':n['title'],'children':[],'parent':parent}
            tree[parent]['children'].append(n['path']); touched.add(parent)
        elif parent and tree[n['path']]['parent']!=parent:
            old=tree[n['path']]['parent']
            assert old is not None,(n,old)
            tree[old]['children'].remove(n['path']); tree[parent]['children'].append(n['path'])
            tree[n['path']]['parent']=parent; touched.update([old,parent]); moved.append(n['path'])
        if n['action']=='fill-empty':
            touched.add(n['path'])
            if parent: touched.add(parent)
    order={n['path']:i for i,n in enumerate(doc['nodes'])}
    renumber={}
    for parent in touched:
        # Leave unmatched legacy entries at the end; do not delete existing pages.
        tree[parent]['children'].sort(key=lambda p:order.get(p,len(order)))
        for path in [parent]+tree[parent]['children']:
            if path not in bypath: continue
            n=bypath[path]; new_num=number(n['title']); old_num=number(tree[path]['title'])
            if new_num and old_num and new_num!=old_num:
                tree[path]['title']=re.sub(r'^'+re.escape(old_num)+r'\.?\s+',new_num+'. ',tree[path]['title'],count=1)
            if n['action']=='preserve' and new_num:
                s=(ROOT/path).read_text(encoding='utf-8-sig')
                first=re.search(r'^# (.*)$',s,re.M)
                old_heading_num=number(first[1]) if first else ''
                if old_heading_num and old_heading_num!=new_num:
                    new=re.sub(r'^(#+\s+)'+re.escape(old_heading_num)+r'(?=\.|\s|$)',lambda m:m[1]+new_num,s,flags=re.M)
                    renumber[path]=new
    lines=['# Table of contents','']
    def emit(path,level):
        n=tree[path]
        title=n['title'].replace('_','\\_'); url=path.replace('_','\\_')
        lines.append('  '*level+'* ['+title+']('+url+')')
        for p in n['children']: emit(p,level+1)
    for path in roots: emit(path,0)
    return '\n'.join(lines)+'\n',renumber,moved

def apply():
    doc=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
    checks=json.loads((OUT/'conversion-checks.json').read_text(encoding='utf-8'))
    assert len(checks)==sum(n['action']!='preserve' for n in doc['nodes'])
    assert all(all(c[k] for k in ['text_equal','code_equal','table_equal','anchors_preserved']) for c in checks)
    assert hashlib.sha256((ROOT/'SUMMARY.md').read_bytes()).hexdigest()==doc['summary_sha256'], 'SUMMARY changed since planning'
    # Preflight every original before any writes.
    for n in doc['nodes']:
        p=ROOT/n['path']
        assert (hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None)==n['original_sha256'],n['path']
    summary,renumber,moved=summary_and_headings(doc)
    changes=[]
    for n in doc['nodes']:
        if n['action']=='preserve' and n['path'] not in renumber: continue
        s=(STAGE/n['path']).read_text(encoding='utf-8') if n['action']!='preserve' else renumber[n['path']]
        target=ROOT/n['path']; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(s,encoding='utf-8')
        changes.append({'path':n['path'],'action':n['action'] if n['action']!='preserve' else 'heading-number-only',
                        'source':BASE+n['page'],'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (ROOT/'SUMMARY.md').write_text(summary,encoding='utf-8')
    save('changes.json',{'version':doc['version'],'date':datetime.now(timezone.utc).isoformat(),
                         'changes':changes,'relocated_summary_entries':moved,
                         'summary_sha256':hashlib.sha256((ROOT/'SUMMARY.md').read_bytes()).hexdigest()})
    print('Applied:',Counter(c['action'] for c in changes),'relocated entries',len(moved))

def verify():
    doc=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
    changes=json.loads((OUT/'changes.json').read_text(encoding='utf-8'))
    changed={c['path']:c for c in changes['changes']}
    summary=(ROOT/'SUMMARY.md').read_text(encoding='utf-8')
    paths=[]; stack=[]; parents={}; titles={}
    for line in summary.splitlines():
        m=re.match(r'(\s*)\* \[(.*?)\]\((.*?)\)',line)
        if not m: continue
        indent,title,path=m.groups(); path=path.replace('\\_','_')
        level=len(indent)//2
        assert level<=len(stack),(line,stack)
        while len(stack)>level: stack.pop()
        parents[path]=stack[-1] if stack else None; stack.append(path)
        paths.append(path); titles[path]=title.replace('\\_','_')
        assert (ROOT/path).is_file(),path
    assert len(paths)==len(set(paths)), 'Duplicate SUMMARY path'
    before={e['path'] for e in read_csv('inventory.csv')}
    assert before<=set(paths),'Existing SUMMARY entries lost'
    bypage={n['page']:n for n in doc['nodes']}
    for n in doc['nodes']:
        assert n['path'] in paths,n
        if n['parent']:
            assert parents[n['path']]==bypage[n['parent']]['path'],n
        digest=hashlib.sha256((ROOT/n['path']).read_bytes()).hexdigest()
        assert digest==(changed[n['path']]['sha256'] if n['path'] in changed else n['original_sha256']),n['path']
    renderer=MarkdownIt('commonmark',{'html':True}).enable('table')
    parsed={}; local_links=0; external_links=0
    for c in changes['changes']:
        if c['action']=='heading-number-only': continue
        md=(ROOT/c['path']).read_text(encoding='utf-8')
        parsed[c['path']]=BeautifulSoup(renderer.render(md),'html.parser')
        assert len(parsed[c['path']].find_all('h1'))==1,c['path']
        assert '英文原文，待翻譯' in md,c['path']
    for path,soup in parsed.items():
        for a in soup.find_all('a',href=True):
            u=urllib.parse.urlsplit(a['href'])
            if u.scheme or u.netloc:
                external_links+=1
                assert not a['href'].startswith(('https://www.postgresql.org/docs/current/','https://www.postgresql.org/docs/devel/')),a['href']
                continue
            target=(ROOT/path).parent/urllib.parse.unquote(u.path) if u.path else ROOT/path
            target=target.resolve()
            assert target.is_relative_to(ROOT) and target.is_file(),(path,a['href'])
            rel=target.relative_to(ROOT).as_posix()
            if u.fragment:
                assert rel in parsed,(path,a['href'],'Unverified existing anchor')
                assert parsed[rel].find(id=urllib.parse.unquote(u.fragment)) or parsed[rel].find(attrs={'name':urllib.parse.unquote(u.fragment)}),(path,a['href'])
            local_links+=1
    results={'summary_entries':len(paths),'new_pages':sum(c['action']=='new' for c in changes['changes']),
             'filled_pages':sum(c['action']=='fill-empty' for c in changes['changes']),
             'heading_only_changes':sum(c['action']=='heading-number-only' for c in changes['changes']),
             'relocated_entries':len(changes['relocated_summary_entries']),
             'imported_local_links_verified':local_links,'external_links_preserved':external_links,
             'preserved_pages_verified':sum(n['path'] not in changed for n in doc['nodes']),
             'checks':'Source text, code, table contents and anchors; SUMMARY reachability, hierarchy and uniqueness; local links and fragments; unchanged-page hashes.'}
    save('verification.json',results)
    print(json.dumps(results,ensure_ascii=False,indent=2))

def refresh():
    """Apply a verified formatting correction only to our imported pages."""
    changes=json.loads((OUT/'changes.json').read_text(encoding='utf-8'))
    checks=json.loads((OUT/'conversion-checks.json').read_text(encoding='utf-8'))
    assert all(all(c[k] for k in ['text_equal','code_equal','table_equal','anchors_preserved']) for c in checks)
    for c in changes['changes']:
        assert hashlib.sha256((ROOT/c['path']).read_bytes()).hexdigest()==c['sha256'],c['path']
    for c in changes['changes']:
        if c['action']=='heading-number-only': continue
        target=ROOT/c['path']; target.write_bytes((STAGE/c['path']).read_bytes())
        c['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
    save('changes.json',changes)
    print('Refreshed imported pages only')

if __name__=='__main__':
    {'plan':plan,'fetch':fetch,'render':render,'apply':apply,'verify':verify,'refresh':refresh}[sys.argv[1]]()
