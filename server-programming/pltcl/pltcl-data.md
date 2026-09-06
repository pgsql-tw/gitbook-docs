## 42.3. PL/Tcl 中的資料值 [#](#PLTCL-DATA)

提供給 PL/Tcl 函式程式碼的引數值，就是轉換成文字形式的輸入引數（如同由 `SELECT` 陳述式顯示出來的形式）。反過來說，`return` 與 `return_next` 命令可接受任何字串，只要它符合函式所宣告回傳型別的合法輸入格式，或符合複合回傳型別中指定欄位的合法輸入格式即可。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-data.html)（原文版本：18.6；核對日期：2026-09-07）
