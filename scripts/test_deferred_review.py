"""Regression tests in disposable repositories; no model calls."""
from unittest.mock import patch
import unittest
import agent_handoff as h
import test_agent_handoff as fixture_module
from test_agent_handoff import PAGE, TARGET
from translation_pipeline import Queue, SKILL, GlobalFailure, PageFailure
from publish_inbox_structural import main


class DeferredTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture_module.Tests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.queue = Queue(self.root)
        self.addCleanup(self.queue.db.close)
        self.queue.init()

    def legacy(self):
        self.fixture.submit(TARGET.replace('請先設定', '請勿設定'))
        h.publish(self.root, publisher='publish-inbox-structural', reviewer=lambda *args: [])

    def state(self):
        entry = self.queue.deferred_publications()[PAGE]
        (self.queue.workdir(PAGE) / 'draft' / PAGE).parent.mkdir(parents=True, exist_ok=True)
        return dict(base_hash=entry['meta']['base_sha256'],
                    policy_hash=h.digest(h.read(SKILL / 'SKILL.md') + h.read(SKILL / 'references/style.md')),
                    source={'url': entry['meta']['source_url']}, reviews=[])

    def test_preflight_never_publishes(self):
        item = self.fixture.submit()
        head = h.git(self.root, 'rev-parse', 'HEAD')
        result = main(self.root)
        self.assertEqual(result[0]['outcome'], 'structural_passed_semantic_review_required')
        self.assertTrue(item.exists())
        self.assertEqual(h.git(self.root, 'rev-parse', 'HEAD'), head)
        self.assertNotEqual(h.pending_state(self.root, PAGE), 'done')
        self.fixture.review_patch.target.semantic_review.assert_not_called()

    def test_legacy_done_is_reopened_and_survives_restart(self):
        self.legacy()
        self.queue.update(PAGE, 'done')
        self.queue.sync_collaborators()
        other = Queue(self.root)
        try:
            self.assertEqual(other.db.execute('SELECT phase FROM pages WHERE path=?', (PAGE,)).fetchone()[0],
                             'review_required')
        finally:
            other.db.close()

    def test_rejection_cannot_become_done(self):
        self.legacy()
        with patch.object(self.queue, 'prepare', return_value=self.state()), \
             patch.object(self.queue, 'review', return_value=['negation reversed']):
            self.assertTrue(self.queue.process_deferred())
        self.assertFalse(self.queue.meta('deferred:' + PAGE)['passed'])
        self.assertEqual(self.queue.counts()['review_exception'], 1)
        with patch.object(self.queue, 'review') as reviewer:
            self.assertFalse(self.queue.process_deferred())
            reviewer.assert_not_called()

    def test_rejected_page_does_not_block_next_page(self):
        self.legacy()
        entries = self.queue.deferred_publications()
        other = fixture_module.OTHER
        # A cached rejection precedes a valid page in the same scan.
        self.queue.setmeta('deferred:' + other, dict(key='rejected-key', passed=False, errors=['bad']))
        real_key = self.queue.deferred_key
        with patch.object(self.queue, 'deferred_publications', return_value={other: entries[PAGE], **entries}), \
             patch.object(self.queue, 'deferred_key', side_effect=lambda p, e: 'rejected-key' if p == other else real_key(p, e)), \
             patch.object(self.queue, 'prepare', return_value=self.state()), \
             patch.object(self.queue, 'review', return_value=[]) as reviewer:
            self.assertTrue(self.queue.process_deferred())
            self.assertEqual(reviewer.call_args.args[0], PAGE)
        self.assertEqual(self.queue.counts()['review_exception'], 1)

    def test_local_worker_failure_quarantined_but_global_failure_propagates(self):
        self.legacy()
        with patch.object(self.queue, 'prepare', return_value=self.state()), \
             patch.object(self.queue, 'review', side_effect=GlobalFailure('usage limit')):
            with self.assertRaisesRegex(GlobalFailure, 'usage limit'):
                self.queue.process_deferred()
        with patch.object(self.queue, 'prepare', return_value=self.state()), \
             patch.object(self.queue, 'review', side_effect=PageFailure('invalid coverage')):
            self.assertTrue(self.queue.process_deferred())
        self.assertEqual(self.queue.counts()['review_exception'], 1)

    def test_batch_target_does_not_hide_review_exceptions(self):
        self.queue.setmeta('active_batch', dict(start_head=h.git(self.root, 'rev-parse', 'HEAD'), target=1))
        self.legacy()
        self.queue.update(PAGE, 'review_exception', error='bad')
        self.assertTrue(self.queue.batch_complete())
        self.assertEqual(self.queue.meta('health'), 'batch_target_reached_review_incomplete')

    def test_approval_cached_but_candidate_change_invalidates(self):
        self.legacy()
        with patch.object(self.queue, 'prepare', return_value=self.state()), \
             patch.object(self.queue, 'review', return_value=[]) as reviewer:
            self.assertTrue(self.queue.process_deferred())
            self.assertFalse(self.queue.process_deferred())
            reviewer.assert_called_once()
        h.write_styled(self.root / PAGE, h.read(self.root / PAGE) + '\nchanged\n')
        with self.assertRaisesRegex(GlobalFailure, 'changed'):
            self.queue.process_deferred()
        self.assertEqual(self.queue.counts()['review_required'], 1)


if __name__ == '__main__':
    unittest.main()
