<a id="INTRO-WHATIS"></a>

## 1. 什麼是 PostgreSQL？ [#](#INTRO-WHATIS)

PostgreSQL 是一套物件關聯式資料庫管理系統（ORDBMS），以加州大學柏克萊分校資訊科學系所開發的 [POSTGRES 第 4.2 版](https://dsf.berkeley.edu/postgres.html)為基礎。POSTGRES 開創了許多概念，這些概念直到很久以後才出現在部分商業資料庫系統中。

PostgreSQL 是這份柏克萊原始程式碼的開放原始碼後裔。它支援 SQL 標準的大部分內容，並提供許多現代功能：

* [複雜查詢](../the-sql-language/README.md)
* [外鍵](../the-sql-language/ddl/ddl-constraints.md#DDL-CONSTRAINTS-FK)
* [觸發程序](../server-programming/triggers/README.md)
* [可更新的檢視表](../reference/sql-commands/sql-createview.md#SQL-CREATEVIEW-UPDATABLE-VIEWS)
* [交易完整性](../the-sql-language/mvcc/transaction-iso.md)
* [多版本並行控制](../the-sql-language/mvcc/README.md)

此外，使用者還可以透過許多方式擴充 PostgreSQL，例如新增

* [資料型別](../the-sql-language/datatype/README.md)
* [函式](../the-sql-language/functions/README.md)
* [運算子](../the-sql-language/functions/README.md)
* [彙總函式](../the-sql-language/functions/functions-aggregate.md)
* [索引方法](../the-sql-language/indexes/README.md)
* [程序語言](../server-programming/README.md)

而且由於採用寬鬆的授權條款，任何人都可以為任何目的免費使用、修改及散布 PostgreSQL，無論是私人、商業或學術用途。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intro-whatis.html)（原文版本：18.6；核對日期：2026-10-10）
