"""Offline cross-version/path regressions in disposable repositories."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import agent_handoff as h
from pg_project import BASE, translation_root, translation_path, major_version, source_prefix
from translation_pipeline import Queue, PageFailure, write_text
import test_agent_handoff as fixture


class ProjectTests(unittest.TestCase):
    def repo(self, version='19'):
        temp = tempfile.TemporaryDirectory(prefix='pg-project-test-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        h.git(root, 'init', '-b', version)
        return root

    def test_new_checkout_uses_neutral_root(self):
        root = self.repo()
        self.assertEqual(translation_root(root), root / BASE)
        self.assertFalse(translation_root(root).exists())

    def test_existing_evidence_and_publisher_paths_stay_together(self):
        root = self.repo()
        old = root / 'outputs' / ('pg' + '17' + '-translation')
        old.mkdir(parents=True)
        marker = old / 'pending-pages.md'
        marker.write_bytes(b'unchanged historical evidence\r\n')
        q = Queue(root)
        self.addCleanup(q.db.close)
        self.assertEqual(q.rt, old / 'pipeline-runtime')
        self.assertEqual(h.claims_dir(root), old / 'agents/claims')
        self.assertEqual(h.inbox_dir(root, 'claude'), old / 'agents/inbox/claude')
        self.assertEqual(marker.read_bytes(), b'unchanged historical evidence\r\n')
        self.assertFalse((root / BASE).exists())

    def test_ambiguous_roots_fail_instead_of_splitting_state(self):
        root = self.repo()
        old = root / 'outputs' / ('pg' + '17' + '-translation')
        old.mkdir(parents=True)
        (old / 'pending-pages.md').write_text('history', encoding='utf-8')
        (root / BASE).mkdir()
        with self.assertRaisesRegex(ValueError, 'Multiple translation roots'):
            translation_root(root)

    def test_version_branch_drives_official_prefix(self):
        for major in ['18', '19']:
            root = self.repo(major)
            self.assertEqual(major_version(root), major)
            self.assertEqual(source_prefix(root), f'https://www.postgresql.org/docs/{major}/')

    def test_non_numeric_branch_needs_explicit_version(self):
        root = self.repo('main')
        with self.assertRaises(ValueError):
            major_version(root)
        (root / 'pg-project.json').write_text('{"major": 19}', encoding='utf-8')
        self.assertEqual(major_version(root), '19')

    def test_configuration_cannot_override_conflicting_version_branch(self):
        root = self.repo('18')
        (root / 'pg-project.json').write_text('{"major": 19}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs'):
            major_version(root)

    def test_pipeline_fetches_target_major_and_rejects_other_major_redirect(self):
        root = self.repo('19')
        q = Queue(root)
        self.addCleanup(q.db.close)
        response = MagicMock()
        response.url = 'https://www.postgresql.org/docs/19/test.html'
        response.read.return_value = b'<title>PostgreSQL 19.1 Documentation</title>'
        response.__enter__.return_value = response
        baseline = '[official](https://www.postgresql.org/docs/19/test.html)'
        with patch('translation_pipeline.urllib.request.urlopen', return_value=response) as fetch:
            result = q.source('test.md', baseline, root)
        self.assertEqual(result['minor'], '19.1')
        self.assertEqual(fetch.call_args.args[0].full_url, response.url)
        response.url = 'https://www.postgresql.org/docs/18/test.html'
        with patch('translation_pipeline.urllib.request.urlopen', return_value=response):
            with self.assertRaisesRegex(PageFailure, 'outside pinned major'):
                q.source('test.md', baseline, root)

    def test_pipeline_does_not_reuse_other_major_cached_source(self):
        root = self.repo('19')
        q = Queue(root)
        self.addCleanup(q.db.close)
        saved = {'source': {'url': 'https://www.postgresql.org/docs/18/test.html'}}
        write_text(q.workdir('test.md') / 'manifest.json', json.dumps(saved))
        with self.assertRaisesRegex(PageFailure, 'another PostgreSQL major'):
            q.prepare('test.md')
        self.assertEqual(json.loads((q.workdir('test.md')/'manifest.json').read_text()), saved)

    def test_version_19_submission_publishes_with_neutral_subject(self):
        f = fixture.Tests()
        f.setUp()
        self.addCleanup(f.tearDown)
        self.addCleanup(f.doCleanups)
        h.git(f.root, 'checkout', '-b', '19')
        source = fixture.SOURCE.replace('18.6', '19.1').replace('/docs/18/', '/docs/19/')
        target = fixture.TARGET.replace('18.6', '19.1').replace('/docs/18/', '/docs/19/')
        h.write_styled(f.root/fixture.PAGE, source)
        h.git(f.root, 'add', '--', fixture.PAGE)
        h.git(f.root, 'commit', '-m', 'version 19 fixture')
        f.submit(text=target, source_url='https://www.postgresql.org/docs/19/tutorial-install.html', source_version='19.1')
        result = h.publish(f.root)
        self.assertEqual(result[0]['outcome'], 'published')
        self.assertEqual(h.git(f.root, 'log', '-1', '--format=%s'), '文件(pg)：翻譯 tutorial-install')


if __name__ == '__main__':
    unittest.main()
