"""離線預檢 inbox；不發佈、不勾選完成、不移動送件。

用法：py -3 scripts\\publish_inbox_structural.py [每次最多幾頁]
正式發佈必須使用 agent_handoff.py publish，通過獨立語意審查。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_handoff as handoff

def main(root=None, limit=None):
    results = handoff.publish(root or Path(__file__).resolve().parents[1],
                              publisher='structural-preflight', limit=limit, dry_run=True)
    for result in results:
        if result['outcome'] == 'would_publish':
            result['outcome'] = 'structural_passed_semantic_review_required'
    return results


if __name__ == '__main__':
    print(json.dumps(main(limit=int(sys.argv[1]) if len(sys.argv) > 1 else None),
                     ensure_ascii=False, indent=2))
