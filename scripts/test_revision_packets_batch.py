"""Reproducible ten-page local experiment; does not invoke the publisher."""
import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from pg_project import translation_path

NAMES = ('app-psql','app-pgdump','app-reindexdb','app-createuser',
         'app-pgamcheck','app-postgres','sql-createpolicy','sql-copy',
         'view-pg-locks','warm-standby')

def readjson(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--local',action='store_true')
    args=parser.parse_args()
    out=Path('outputs/local-review-feasibility/batch-10')
    out.mkdir(parents=True,exist_ok=True)
    groups=defaultdict(list)
    root=translation_path(Path.cwd(), 'agents/inbox/claude')
    for category in ('_rejected','_published'):
        for folder in (root/category).iterdir():
            if all((folder/f).exists() for f in ('page.md','result.json','meta.json')):
                groups[folder.name.split('--')[0]].append(folder)
    manifests={Path(m['page']).stem:(f,m) for f in translation_path(Path.cwd(), 'pipeline-runtime/pages').glob('*/manifest.json') for m in [readjson(f)] if Path(m['page']).stem in NAMES}
    results=[]
    for name in NAMES:
        mf,manifest=manifests[name]
        slug=manifest['page'].replace('/','__')
        candidates=sorted(groups[slug],key=lambda f:f.name.split('--')[-1])
        old,new=candidates[-2:]
        target=out/(name+'.json')
        row=dict(name=name,page=manifest['page'],old=str(old),new=str(new),manifest=str(mf),
                 source=str(mf.parent/'draft/source.html'),
                 old_source=readjson(old/'meta.json').get('source_version'),
                 new_source=readjson(new/'meta.json').get('source_version'),
                 source_metadata=manifest['source'])
        command=[sys.executable,'scripts/revision_review_packets.py','--old',str(old/'page.md'),'--new',str(new/'page.md'),'--prior',str(old/'result.json'),'--manifest',str(mf),'--source',row['source'],'--out',str(target)]
        if args.local: command.append('--local')
        started=time.monotonic()
        run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace')
        row.update(exit_code=run.returncode,elapsed_seconds=round(time.monotonic()-started,2))
        if run.returncode:
            row['error']=run.stderr[-4000:]
        else:
            packet=readjson(target)
            row.update(changes=len(packet['changes']),records=len(packet['records']),unresolved=len(packet['unresolved_changes']),
                       local_seconds=round(sum(r.get('local_seconds',0) for r in packet['records']),2),
                       metrics=packet.get('actual_model_token_counts'),
                       source_excerpt_exact=True if packet['records'] else None,
                       revision_packet_eligible=bool(packet['changes']) and not packet['unresolved_changes'],
                       full_page_approved=False)
        results.append(row)
        (out/'summary.json').write_text(json.dumps(dict(local=args.local,cases=results),ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(row,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
