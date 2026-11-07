"""T1: synthetic positive/negative cases for every zh_lint rule."""
import unittest
from zh_lint import lint

FOOT = '\n\n---\n\n原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/x.html)（原文版本：18.6；核對日期：2026-10-01）\n'
META = dict(source_version='18.6', source_url='https://www.postgresql.org/docs/18/x.html', retrieved='2026-10-01')


def checks(text, **kw):
    kw.setdefault('meta', META)
    return {f['check'] for f in lint(text + FOOT, **kw) if f['level'] == 'error'}


def warns(text, **kw):
    return {f['check'] for f in lint(text + FOOT, meta=META, **kw) if f['level'] == 'warn'}


class Footer(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(checks('<a id="X"></a>\n\n## 標題 [#](#X)\n\n內容。'), set())

    def test_date_mismatch(self):
        self.assertIn('footer.date', checks('內容。', meta=dict(META, retrieved='2026-09-30')))

    def test_url_mismatch(self):
        self.assertIn('footer.url', checks('內容。', meta=dict(META, source_url='https://www.postgresql.org/docs/18/y.html')))

    def test_missing(self):
        self.assertIn('footer.missing', {f['check'] for f in lint('只有內容。', meta=META)})

    def test_bad_format(self):
        self.assertIn('footer.format', {f['check'] for f in lint('內容。\n\n原文：PostgreSQL 18.6（核對日期：2026-10-01）\n', meta=META)})

    def test_snapshot_warn(self):
        self.assertIn('footer.snapshot', {f['check'] for f in lint('內容。' + FOOT, meta=META, snapshot_date='2026-10-02')})


class Anchors(unittest.TestCase):
    def test_link_without_id(self):
        self.assertIn('anchor.link', checks('## 標題 [#](#SQL-X)\n\n內容。'))

    def test_same_page_filename_link(self):
        got = {f['check'] for f in lint('請見[子句](sql-insert.md#SQL-ON-CONFLICT)。' + FOOT, meta=dict(META, page='reference/sql-commands/sql-insert.md'))}
        self.assertIn('anchor.link', got)
        got = {f['check'] for f in lint('請見[子句](sql-update.md#SQL-X)。' + FOOT, meta=dict(META, page='reference/sql-commands/sql-insert.md'))}
        self.assertNotIn('anchor.link', got)

    def test_link_with_id(self):
        self.assertNotIn('anchor.link', checks('<a id="SQL-X"></a>\n\n## 標題 [#](#SQL-X)\n\n內容。'))

    def test_baseline_id_lost(self):
        self.assertIn('anchor.baseline', checks('## 標題\n\n內容。', baseline='<a id="A"></a>\n\n## Title\n\nText.'))

    def test_official_id_missing(self):
        html = '<html><body><div class="sect1" id="ROOT"><p>x</p><div class="note" id="id-1.2.3"><p>n</p></div></div></body></html>'
        got = {f['check']: f['level'] for f in lint('<a id="ROOT"></a>\n\n## 標題\n\n內容。' + FOOT, meta=META, html=html)}
        self.assertEqual(got.get('anchor.official'), 'error')
        self.assertNotIn('anchor.root', got)

    def test_official_root_is_warn(self):
        html = '<html><body><div class="sect1" id="ROOT"><p>x</p></div></body></html>'
        got = {f['check']: f['level'] for f in lint('<a id="B"></a>\n\n## 標題\n\n內容。' + FOOT, meta=META, html=html)}
        self.assertEqual(got.get('anchor.root'), 'error')

    def test_anchor_placement(self):
        bad = '<a id="A"></a>\n\n## 甲 [#](#A)\n\n內容。<a id="B"></a>\n\n文字。\n\n## 乙 [#](#B)\n\n內容。'
        good = '<a id="A"></a>\n\n## 甲 [#](#A)\n\n內容。\n\n<a id="B"></a>\n\n## 乙 [#](#B)\n\n內容。'
        self.assertIn('anchor.placement', checks(bad))
        self.assertNotIn('anchor.placement', checks(good))

    def test_heading_anchor_follows_official(self):
        # 使用者裁決 2026-10-11：官方沒有 id 的標題（提示／注意等）不要求錨點；官方有就必須有
        html = '<html><body><div class="sect1" id="ROOT"><div class="tip"><h3>Tip</h3></div><div class="note" id="id-9"><p>n</p></div></div></body></html>'
        got = {f['check'] for f in lint('<a id="ROOT"></a>\n\n### 提示\n\n內容。' + FOOT, meta=META, html=html) if f['level'] == 'error'}
        self.assertIn('anchor.official', got)
        got = {f['check'] for f in lint('<a id="ROOT"></a>\n\n### 提示\n\n<a id="id-9"></a>\n\n### 注意\n\n內容。' + FOOT, meta=META, html=html)}
        self.assertFalse(any(c.startswith('anchor') for c in got))


class Untranslated(unittest.TestCase):
    def test_heading_english(self):
        self.assertIn('untranslated.heading', checks('<a id="N"></a>\n\n### Note\n\n內容。'))
        self.assertIn('untranslated.heading', checks('<a id="N"></a>\n\n### 51.9.4. Stream Start 回呼\n\n內容。'))

    def test_heading_allowed(self):
        self.assertEqual(checks('<a id="A"></a>\n\n## PostgreSQL 與 `pg_dump` 的 SQL 命令\n\n內容。'), set())

    def test_xref(self):
        self.assertIn('untranslated.xref', checks('請參閱 [Section 17.7](install.md#X)。'))
        self.assertNotIn('untranslated.xref', checks('請參閱[第 17.7 節](install.md#X)。'))

    def test_prose_function_word(self):
        self.assertIn('untranslated.prose', checks('| `oid` | (references pg_class.oid) |'))
        self.assertIn('untranslated.prose', checks('範圍為 -32768 to +32767。'))

    def test_gloss_and_quote_ok(self):
        self.assertEqual(checks('目錄（Table of Contents）檔案會回報「does not exist」錯誤。'), set())

    def test_code_ignored(self):
        self.assertEqual(checks('執行 `SELECT * FROM t WHERE a is not null` 即可。\n\n```sql\nselect 1 to 2;\n```'), set())

    def test_function_signature_ignored(self):
        self.assertNotIn('untranslated.prose', checks('<p class="func_signature">\n<code>f</code> ( <code>name</code> or <code>oid</code> )\n</p>'))

    def test_nested_quote(self):
        self.assertEqual(checks('會引發類似「collation "de-x-icu" for encoding（編碼）」的錯誤，或「file not found（找不到檔案）」。'), set())

    def test_heading_lowercase_identifier_from_baseline(self):
        base = '<a id="A"></a>\n\n## createuser\n\nText.'
        self.assertNotIn('untranslated.heading', checks('<a id="A"></a>\n\n## createuser\n\n內容。', baseline=base))
        self.assertIn('untranslated.heading', checks('<a id="A"></a>\n\n## Note\n\n內容。', baseline='<a id="A"></a>\n\n## Note\n\nText.'))

    def test_sql_type_phrase_and_translator_note(self):
        self.assertNotIn('untranslated.prose', checks('| <code>timestamp</code> with time zone | 8 位元組 |'))
        self.assertNotIn('untranslated.prose', checks('已經加密（原文此處寫作 sent to the client，但實際上不同）。'))
        self.assertNotIn('untranslated.prose', checks('輸出「ISO 8601 格式（format\nwith designators）」的時間間隔。'))

    def test_prose_word_warn(self):
        self.assertIn('untranslated.word', warns('死亡 tuple 會被回收。'))


class Terms(unittest.TestCase):
    def test_conditional_on_english(self):
        base = '## X\n\nThe server process forks.'
        self.assertIn('term.process', checks('## X\n\n伺服器處理程序會分叉。', baseline=base))
        self.assertNotIn('term.process', checks('## X\n\n並行程度與執行程式的平行程序，以及資料庫關閉處理程序。', baseline=base))
        self.assertNotIn('term.process', checks('## X\n\n訊號處理程序會被呼叫。', baseline='## X\n\nThe signal handler is called.'))

    def test_unconditional_client(self):
        self.assertIn('term.client', checks('客戶端連線。'))
        self.assertNotIn('term.client', checks('用戶端連線。'))

    def test_replication_vs_copy(self):
        self.assertIn('term.replication', checks('## X\n\n邏輯複製插槽', baseline='## X\n\nlogical replication slot'))
        self.assertNotIn('term.replication', checks('## X\n\n複製檔案', baseline='## X\n\ncopy the file; replication is separate'))

    def test_constraint_noun_not_verb(self):
        base = '## X\n\nconstraint'
        self.assertIn('term.constraint', checks('## X\n\n唯一性條件約束', baseline=base))
        self.assertNotIn('term.constraint', checks('## X\n\n擁有者不受資料列安全政策的約束。', baseline=base))

    def test_regional(self):
        self.assertIn('term.regional', checks('數據庫伺服器'))


class Typography(unittest.TestCase):
    def test_simplified(self):
        self.assertIn('simplified', checks('保留英文表头。'))
        self.assertNotIn('simplified', checks('移動游標並在平台上的群組占用空間。'))

    def test_dup(self):
        self.assertIn('dup', checks('因此，因此不需要。'))
        self.assertIn('dup', checks('這是的的錯字。'))
        self.assertNotIn('dup', checks('每個插槽都有一個名稱，名稱可以包含小寫字母；程序、程序語言；一對一對應。'))

    def test_space_warn(self):
        self.assertIn('space', warns('無效 資料列'))
        self.assertNotIn('space', warns('使用 `x` 指令'))


if __name__ == '__main__':
    unittest.main()
