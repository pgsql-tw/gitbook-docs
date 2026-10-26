<a id="FDWHANDLER"></a>

## 第 58 章 撰寫外部資料包裝器

**目錄**

[58.1. 外部資料包裝器函式](fdw-functions.md)

[58.2. 外部資料包裝器回呼常式](fdw-callbacks.md)
:   [58.2.1. 掃描外部資料表的 FDW 常式](fdw-callbacks.md#fdw-callbacks-scan)

    [58.2.2. 掃描外部資料表連接的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-JOIN-SCAN)

    [58.2.3. 規劃掃描／連接後處理的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-UPPER-PLANNING)

    [58.2.4. 更新外部資料表的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-UPDATE)

    [58.2.5. `TRUNCATE` 的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-TRUNCATE)

    [58.2.6. 資料列鎖定的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-ROW-LOCKING)

    [58.2.7. `EXPLAIN` 的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-EXPLAIN)

    [58.2.8. `ANALYZE` 的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-ANALYZE)

    [58.2.9. `IMPORT FOREIGN SCHEMA` 的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-IMPORT)

    [58.2.10. 平行執行的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-PARALLEL)

    [58.2.11. 非同步執行的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-ASYNC)

    [58.2.12. 路徑重新參數化的 FDW 常式](fdw-callbacks.md#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

[58.3. 外部資料包裝器輔助函式](fdw-helpers.md)

[58.4. 外部資料包裝器查詢規劃](fdw-planning.md)

[58.5. 外部資料包裝器中的資料列鎖定](fdw-row-locking.md)

<a id="id-1.10.10.2"></a>

對外部資料表的所有操作，都是透過其外部資料包裝器處理；外部資料包裝器由一組供核心伺服器呼叫的函式組成。外部資料包裝器負責從遠端資料來源擷取資料，並將資料傳回給 PostgreSQL 執行器。如果要支援更新外部資料表，包裝器也必須處理這部分。本章概述如何撰寫新的外部資料包裝器。

嘗試撰寫自己的外部資料包裝器時，標準發行版中所附的外部資料包裝器是很好的參考。請查看原始碼樹中的 `contrib` 子目錄。[CREATE FOREIGN DATA WRAPPER](../../reference/sql-commands/sql-createforeigndatawrapper.md) 參考頁面也有一些實用的細節。

### 注意

SQL 標準規定了一套撰寫外部資料包裝器的介面。然而，PostgreSQL 並未實作該 API，因為要將它納入 PostgreSQL 的工作量會很大，而且該標準 API 本來就沒有獲得廣泛採用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdwhandler.html)（原文版本：18.6；核對日期：2026-10-17）
