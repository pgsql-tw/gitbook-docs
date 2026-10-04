<a id="SQL-CREATEMATERIALIZEDVIEW"></a><a id="id-1.9.3.71.1"></a>

## CREATE MATERIALIZED VIEW

CREATE MATERIALIZED VIEW — 定義新的具體化檢視表

<a id="id-1.9.3.71.4"></a>

## 語法

```

CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

<a id="id-1.9.3.71.5"></a>

## 說明

`CREATE MATERIALIZED VIEW` 會定義一個查詢的具體化檢視表。該查詢會在下達此命令時執行，並用來填入檢視表的內容（除非使用了 `WITH NO DATA`），之後可以使用 `REFRESH MATERIALIZED VIEW` 進行重新整理。

`CREATE MATERIALIZED VIEW` 類似於 `CREATE TABLE AS`，不同之處在於它還會記住用來初始化檢視表的查詢，以便之後可以依需要進行重新整理。具體化檢視表具有許多與資料表相同的特性，但不支援暫存具體化檢視表。

`CREATE MATERIALIZED VIEW` 需要具體化檢視表所使用之綱要的 `CREATE` 權限。

<a id="id-1.9.3.71.6"></a>

## 參數

`IF NOT EXISTS`
:   若已存在同名的具體化檢視表，不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的具體化檢視表與原本會建立的具體化檢視表有任何相似之處。

*`table_name`*
:   要建立之具體化檢視表的名稱（可選擇以綱要限定）。名稱必須與同一綱要中任何其他關聯（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱不同。

*`column_name`*
:   新具體化檢視表中某個欄位的名稱。若未提供欄位名稱，則取自查詢的輸出欄位名稱。

`USING method`
:   這個選擇性的子句指定用來儲存新具體化檢視表內容的資料表存取方法；該方法必須是 `TABLE` 類型的存取方法。詳細資訊請參閱[第 62 章](../../internals/tableam/README.md)。若未指定此選項，則會為新的具體化檢視表選用預設的資料表存取方法。詳細資訊請參閱 [default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD)。

`WITH ( storage_parameter [= value] [, ... ] )`
:   此子句為新的具體化檢視表指定選擇性的儲存參數；詳細資訊請參閱 [CREATE TABLE](sql-createtable.md) 說明文件中的[儲存參數](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。`CREATE
    TABLE` 支援的所有參數，`CREATE MATERIALIZED
    VIEW` 也都支援。詳細資訊請參閱 [CREATE TABLE](sql-createtable.md)。

`TABLESPACE tablespace_name`
:   *`tablespace_name`* 是要在其中建立新具體化檢視表的資料表空間名稱。若未指定，則會參考 [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE)。

*`query`*
:   一個 [`SELECT`](sql-select.md)、[`TABLE`](sql-select.md#SQL-TABLE) 或 [`VALUES`](sql-values.md) 命令。此查詢會在安全限制操作（security-restricted operation）中執行；特別是，呼叫本身會建立暫存資料表的函式將會失敗。此外，在查詢執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog, pg_temp`。

`WITH [ NO ] DATA`
:   此子句指定具體化檢視表是否應該在建立時填入資料。若否，該具體化檢視表會被標記為不可掃描，並且在使用 `REFRESH
    MATERIALIZED VIEW` 之前無法查詢。

<a id="id-1.9.3.71.7"></a>

## 相容性

`CREATE MATERIALIZED VIEW` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.71.8"></a>

## 另請參閱

[ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [CREATE TABLE AS](sql-createtableas.md), [CREATE VIEW](sql-createview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-creatematerializedview.html)（原文版本：18.6；核對日期：2026-10-04）
