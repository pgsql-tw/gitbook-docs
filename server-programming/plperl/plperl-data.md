## 43.2. PL/Perl 中的資料值 [#](#PLPERL-DATA)

提供給 PL/Perl 函式程式碼的引數值，就是轉換成文字形式的輸入引數（如同由 `SELECT` 陳述式顯示出來的形式）。反過來說，`return` 與 `return_next` 命令可接受任何符合函式所宣告回傳型別之合法輸入格式的字串。

如果這種行為在某個情況下不方便，可以使用轉換（transform）加以改善，如先前針對 `bool` 值所示範的方式。PostgreSQL 發行版包含數個轉換模組範例。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-data.html)（原文版本：18.6；核對日期：2026-09-07）
