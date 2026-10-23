import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import translation_feature_packets as fp
import translation_pipeline as pipeline


def document(count=3):
    ids = ['E091-06', 'E091-07'] + [f'X{i:03}' for i in range(count-2)]
    rows = ''.join('<tr><td>'+i+'</td><td>Core</td><td>ALL &amp; DISTINCT</td><td> note </td></tr>' for i in ids)
    return '<h2>Title</h2><p>before</p><table><thead><tr><th>ID</th><th>Core?</th><th>Description</th><th>Comment</th></tr></thead><tbody>'+rows+'</tbody></table><p>after</p>'


class PacketTests(unittest.TestCase):
    def test_lossless_complete_rows_and_prose(self):
        doc = document(83)
        manifest, units = fp.build(doc,doc,doc,40)
        self.assertEqual([len(u.get('rows',[])) for u in units],[0,40,40,3])
        self.assertEqual([r['id'] for u in units[1:] for r in u['rows']],manifest['ids'])
        for name in ('original','translation','official'):
            structure=units[0]['documents'][name]
            rows=[structure['header']]+[r[name] for u in units[1:] for r in u['rows']]
            table=''.join(structure['gaps'][i]+r['raw_html'] for i,r in enumerate(rows))+structure['gaps'][-1]
            self.assertEqual(structure['before']+table+structure['after'],doc)
        self.assertEqual(units[1]['rows'][0]['official']['cells'][2],'ALL & DISTINCT')

    def test_mismatch_reorder_duplicate_and_missing_cell_fail(self):
        doc=document()
        candidates=[doc.replace('E091-07','E091-08'),doc.replace('X000','E091-07'),
                    doc.replace('<td> note </td>','',1),doc.replace('E091-06','Z999')]
        for candidate in candidates:
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                fp.build(doc,candidate,doc)

    def test_actual_459_rows(self):
        root=Path(__file__).resolve().parents[1]
        archive=root/'outputs/pg18-translation/agents/inbox/claude/_rejected/appendixes__features__features-sql-standard.md--20261022T174526'
        source=root/'outputs/pg18-translation/pipeline-runtime/pages/dc6427055204038674af/draft/source.html'
        if not archive.exists() or not source.exists(): self.skipTest('local evidence unavailable')
        candidate=(archive/'page.md').read_text(encoding='utf-8-sig')
        html=source.read_text(encoding='utf-8-sig')
        manifest,units=fp.build(candidate,candidate,html)
        self.assertEqual(manifest['feature_count'],459)
        self.assertEqual(len(units),13)
        for key in ('E091-06','E091-07','X056','X057','X058','X059'):
            self.assertEqual(sum(r['id']==key for u in units[1:] for r in u['rows']),1)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='feature-packet-test-')
        self.addCleanup(self.tmp.cleanup)
        self.folder=Path(self.tmp.name)
        self.doc=document(83)
        target=self.folder/'draft'/fp.PAGE
        target.parent.mkdir(parents=True)
        target.write_text(self.doc,encoding='utf-8')
        (self.folder/'draft/source.html').write_text(self.doc,encoding='utf-8')
        self.q=object.__new__(pipeline.Queue)
        self.q.workdir=lambda page:self.folder
        self.q.common_prompt=lambda page:''
        self.q.immutable=lambda page,state:None
        self.q.save=lambda page,state:None
        self.q.event=lambda kind,page,**kwargs:None
        self.calls=[]
        self.q.call=self.call
        self.state=dict(baseline=self.doc,source=dict(sha256=fp.sha(self.doc)),policy_hash='policy',
                        submission=dict(retrieved='2026-10-22'))
        self.mode=None

    def call(self,page,role,prompt,schema):
        data=json.loads(prompt.split('document data, not instructions.\n',1)[1])
        idx=data['assigned_unit']['unit']
        self.calls.append(idx)
        if self.mode=='crash' and idx==2: raise pipeline.GlobalFailure('simulated quota')
        if self.mode=='mutate': (self.folder/'draft'/fp.PAGE).write_text('changed',encoding='utf-8')
        return dict(reviews=[dict(section=idx+1 if self.mode=='wrong_id' else idx,
                                  passed=not(self.mode=='reject' and idx==1),
                                  issues=['real issue'] if self.mode=='reject' and idx==1 else [],
                                  evidence='Checked all assigned cells.')])

    def test_complete_review_and_checkpoint_reuse(self):
        self.assertEqual(self.q.review_feature_table(fp.PAGE,self.state,self.doc),[])
        self.assertEqual(self.calls,[0,1,2,3])
        self.calls.clear()
        self.assertEqual(self.q.review_feature_table(fp.PAGE,self.state,self.doc),[])
        self.assertEqual(self.calls,[])
        self.state['submission']['retrieved']='2026-10-23'
        self.q.review_feature_table(fp.PAGE,self.state,self.doc)
        self.assertEqual(self.calls,[0,1,2,3])

    def test_quota_resume_preserves_only_valid_successes(self):
        self.mode='crash'
        with self.assertRaises(pipeline.GlobalFailure): self.q.review_feature_table(fp.PAGE,self.state,self.doc)
        self.assertEqual(set(self.state['feature_unit_reviews']),{'0','1'})
        self.assertEqual(self.state['reviews'],[])
        self.calls.clear(); self.mode=None
        self.assertEqual(self.q.review_feature_table(fp.PAGE,self.state,self.doc),[])
        self.assertEqual(self.calls,[2,3])

    def test_real_issue_still_rejects_and_does_not_cache_failure(self):
        self.mode='reject'
        errors=self.q.review_feature_table(fp.PAGE,self.state,self.doc)
        self.assertIn('real issue',errors[0])
        self.assertFalse(self.state['reviews'][0]['result']['passed'])
        self.calls.clear(); self.mode=None
        self.q.review_feature_table(fp.PAGE,self.state,self.doc)
        self.assertEqual(self.calls,[1])

    def test_wrong_unit_or_modified_candidate_cannot_approve(self):
        self.mode='wrong_id'
        with self.assertRaises(pipeline.PageFailure): self.q.review_feature_table(fp.PAGE,self.state,self.doc)
        self.mode='mutate'
        with self.assertRaises(pipeline.GlobalFailure): self.q.review_feature_table(fp.PAGE,self.state,self.doc)


if __name__=='__main__': unittest.main()
