<a id="DDL-FOREIGN-DATA"></a>

## 5.13. 外部資料 [#](#DDL-FOREIGN-DATA)

<a id="id-1.5.4.15.2"></a><a id="id-1.5.4.15.3"></a><a id="id-1.5.4.15.4"></a>

PostgreSQL 實作了 SQL/MED 規範的一部分，讓你可以使用一般的 SQL 查詢來存取位於 PostgreSQL 之外的資料。這類資料稱為*外部資料*。（請注意，這個用法不要與外鍵混淆，外鍵是資料庫內的一種限制條件。）

外部資料是藉由*外部資料包裝器*的協助來存取的。外部資料包裝器是一個能夠與外部資料來源溝通的程式庫，它會隱藏連線到該資料來源以及從中取得資料的細節。有一些外部資料包裝器是以 `contrib` 模組的形式提供；請參閱[附錄 F](../../appendixes/contrib/README.md)。其他種類的外部資料包裝器可能可以在第三方產品中找到。如果現有的外部資料包裝器都不符合你的需求，你可以自己撰寫一個；請參閱[第 58 章](../../internals/fdwhandler/README.md)。

要存取外部資料，你需要建立一個*外部伺服器*物件，它會依照其所搭配的外部資料包裝器所使用的選項集合，定義如何連線到某個特定的外部資料來源。接著你需要建立一個或多個*外部資料表*，用來定義遠端資料的結構。外部資料表可以像一般資料表一樣用在查詢中，但外部資料表在 PostgreSQL 伺服器中並沒有儲存空間。每當它被使用時，PostgreSQL 就會要求外部資料包裝器從外部來源取得資料，或者在更新指令的情況下將資料傳送到外部來源。

存取遠端資料時，可能需要對外部資料來源進行身分驗證。這項資訊可以由*使用者對應*來提供，它能夠依據目前的 PostgreSQL 角色提供使用者名稱與密碼等額外資料。

更多資訊請參閱
[CREATE FOREIGN DATA WRAPPER](../../reference/sql-commands/sql-createforeigndatawrapper.md)、
[CREATE SERVER](../../reference/sql-commands/sql-createserver.md)、
[CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md)、
[CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md) 與
[IMPORT FOREIGN SCHEMA](../../reference/sql-commands/sql-importforeignschema.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-foreign-data.html)（原文版本：18.6；核對日期：2026-09-13）
