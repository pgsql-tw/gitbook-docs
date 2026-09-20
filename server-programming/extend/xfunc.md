<a id="XFUNC"></a>
## 36.3. 使用者自訂函式 [#](#XFUNC)

<a id="id-1.8.3.6.2"></a>

PostgreSQL 提供四種函式：

* 查詢語言函式（以 SQL 撰寫的函式）（[第 36.5 節](xfunc-sql.md)）
* 程序語言函式（例如以 PL/pgSQL 或 PL/Tcl 撰寫的函式）（[第 36.8 節](xfunc-pl.md)）
* 內部函式（[第 36.9 節](xfunc-internal.md)）
* C 語言函式（[第 36.10 節](xfunc-c.md)）

每一種函式都可以接受基礎型別、複合型別，或是這些型別的組合，作為引數（參數）。此外，每一種函式也都可以回傳基礎型別或複合型別。函式也可以被定義成回傳一組基礎值或複合值。

許多種類的函式都可以接受或回傳某些虛擬型別（例如多型型別），但可用的機制因種類而異。詳情請參閱各種函式各自的說明。

定義 SQL 函式是最容易的，所以我們會先從這裡開始討論。SQL 函式所介紹的大多數概念，也都適用於其他種類的函式。

在本章中，參考 [`CREATE FUNCTION`](../../reference/sql-commands/sql-createfunction.md) 命令的參考頁面，有助於更好地理解範例。本章的部分範例可以在 PostgreSQL 原始碼發行版中 `src/tutorial` 目錄下的 `funcs.sql` 與 `funcs.c` 中找到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc.html)（原文版本：18.6；核對日期：2026-09-15）
