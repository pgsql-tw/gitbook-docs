"""Small, reproducible local translation-review smoke test (no publication)."""
import json
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path('outputs/local-review-feasibility')
CASES = [
    ('boundary_bad', 'Ports under 1024 require special privileges.', '1024 以下的連接埠需要特殊權限。', False),
    ('boundary_good', 'Ports under 1024 require special privileges.', '小於 1024 的連接埠需要特殊權限。', True),
    ('validation_bad', 'NOT VALID constraints check new rows. VALIDATE CONSTRAINT checks existing rows.', 'NOT VALID 限制條件會檢查新資料列。VALIDATE CONSTRAINT 讓限制條件開始生效。', False),
    ('validation_good', 'NOT VALID constraints check new rows. VALIDATE CONSTRAINT checks existing rows.', 'NOT VALID 限制條件會檢查新資料列。VALIDATE CONSTRAINT 驗證既有資料列。', True),
    ('causality_bad', 'An overflowing listen backlog can cause refused connections or hangs, resulting in spurious test failures.', '虛假的測試失敗會造成 listen 佇列溢位，導致連線遭拒或停止回應。', False),
    ('causality_good', 'An overflowing listen backlog can cause refused connections or hangs, resulting in spurious test failures.', 'listen 等待佇列溢位可能造成連線遭拒或停止回應，進而產生虛假的測試失敗。', True),
    ('permission_bad', 'The current user must have CONNECT privilege on the database.', '資料庫必須對目前使用者具有 CONNECT 權限。', False),
    ('permission_good', 'The current user must have CONNECT privilege on the database.', '目前使用者必須對該資料庫具有 CONNECT 權限。', True),
    ('approved_header', 'Table header: SELECT/ALL policy; USING expression.', '表頭保留 SELECT/ALL policy、USING expression；表前說明：policy 為政策，USING expression 為 USING 運算式。', True),
    ('approved_correction', 'The header contains 15 bytes: an 11-byte signature and two 32-bit fields.', '標頭共 19 位元組；原文寫作 15，但所列欄位合計為 11＋4＋4＝19。', True),
    ('header_bad_explanation', 'SELECT/ALL policy means a policy defined FOR SELECT or FOR ALL. ALL is a policy command-type option, not an SQL command.', 'SELECT/ALL policy 指適用於 SELECT 或 ALL SQL 命令的政策。', False),
    ('source_bad_correction', 'The header contains 15 bytes: an 11-byte signature and two 32-bit fields.', '標頭共 23 位元組；原文寫作 15，但所列欄位合計為 11＋4＋4＝23。', False),
]
SCHEMA = {'type': 'object', 'properties': {'passed': {'type': 'boolean'}, 'issues': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['passed', 'issues'], 'additionalProperties': False}
SYSTEM = '''你是 PostgreSQL 繁體中文翻譯審查員。僅依英文、譯文與以下裁決檢查技術語意；不因可選文風而退件。必須檢查數量邊界、主受詞、權限關係、驗證與生效差異及因果。使用者已接受：保留英文表头並附中文對照說明；標頭 15 bytes 的原文內部矛盾可明確勘誤為 19（11+4+4），附註原文數字。只有實際語意問題才 passed=false，issues 須指出具體差異。通過時 issues 為空。輸出指定 JSON。'''

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    focused = '--focused' in sys.argv
    cases = [c for c in CASES if c[0] in ('boundary_bad', 'boundary_good', 'approved_correction', 'source_bad_correction')] if focused else CASES
    system = SYSTEM
    if focused:
        system += '\n強制裁決：under N 僅指 < N；中文「N 以下」包含 N，不能互換。已裁決的來源勘誤若明確寫出原文 15、正確值 19 與 11+4+4 算式，該項必須通過。不要把原文錯誤算成譯文錯誤；若譯文算式或數字不正確，仍須指出。'
    rows = []
    for name, source, target, expected in cases:
        body = {'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': f'英文：{source}\n譯文：{target}'}], 'temperature': 0, 'max_tokens': 512, 'stream': False, 'chat_template_kwargs': {'enable_thinking': False}, 'response_format': {'type': 'json_schema', 'json_schema': {'name': 'review', 'schema': SCHEMA}}}
        started = time.monotonic()
        try:
            request = urllib.request.Request('http://127.0.0.1:18080/v1/chat/completions', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=180) as response:
                raw = json.load(response)
            result = json.loads(raw['choices'][0]['message']['content'])
            valid = isinstance(result.get('passed'), bool) and isinstance(result.get('issues'), list) and all(isinstance(x, str) for x in result['issues']) and result['passed'] == (not result['issues'])
            row = dict(case=name, expected=expected, result=result, valid=valid, correct=valid and result['passed'] == expected, seconds=round(time.monotonic()-started, 2), usage=raw.get('usage'), timings=raw.get('timings'))
        except Exception as exc:
            row = dict(case=name, expected=expected, correct=False, error=str(exc), seconds=round(time.monotonic()-started, 2))
        rows.append(row)
        (OUT/('results-focused.json' if focused else 'results.json')).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(row, ensure_ascii=False), flush=True)
    print(json.dumps({'correct': sum(r['correct'] for r in rows), 'total': len(rows), 'seconds': sum(r['seconds'] for r in rows)}), flush=True)

if __name__ == '__main__':
    main()
