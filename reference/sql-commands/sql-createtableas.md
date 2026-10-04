<a id="SQL-CREATETABLEAS"></a><a id="id-1.9.3.86.1"></a>

## CREATE TABLE AS

CREATE TABLE AS — 以查詢的結果定義新的資料表

<a id="id-1.9.3.86.4"></a>

## 語法

```

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
    [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

<a id="id-1.9.3.86.5"></a>

## 說明

`CREATE TABLE AS` 會建立一個資料表，並以 `SELECT` 命令所計算出的資料填入。資料表的欄位具有與 `SELECT` 之輸出欄位相關聯的名稱與資料型別（不過你可以提供明確的新欄位名稱清單來覆寫欄位名稱）。

`CREATE TABLE AS` 與建立檢視表有些相似，但實際上相當不同：它會建立一個新的資料表，並且只對查詢求值一次，以初始填入新資料表。新資料表不會追蹤查詢來源資料表後續的變更。相較之下，檢視表在每次被查詢時，都會重新對其定義的 `SELECT` 陳述式求值。

`CREATE TABLE AS` 需要資料表所使用之綱要的 `CREATE` 權限。

<a id="id-1.9.3.86.6"></a>

## 參數

`GLOBAL` 或 `LOCAL`
:   為了相容性而忽略。這些關鍵字的使用已被棄用；詳細資訊請參閱 [CREATE TABLE](sql-createtable.md)。

`TEMPORARY` 或 `TEMP`
:   若有指定，資料表會建立為暫存資料表。詳細資訊請參閱 [CREATE TABLE](sql-createtable.md)。

`UNLOGGED`
:   若有指定，資料表會建立為無日誌資料表（unlogged table）。詳細資訊請參閱 [CREATE TABLE](sql-createtable.md)。

`IF NOT EXISTS`
:   若已存在同名的關聯，不擲出錯誤；只會發出 notice，並保持該資料表不變。

*`table_name`*
:   要建立的資料表名稱（可選擇以綱要限定）。

*`column_name`*
:   新資料表中欄位的名稱。若未提供欄位名稱，會取自查詢的輸出欄位名稱。

`USING method`
:   此選用子句指定用來儲存新資料表內容的資料表存取方法；該方法必須是 `TABLE` 類型的存取方法。更多資訊請參閱[第 62 章](../../internals/tableam/README.md)。若未指定此選項，新資料表會使用預設的資料表存取方法。更多資訊請參閱 [default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD)。

`WITH ( storage_parameter [= value] [, ... ] )`
:   此子句為新資料表指定選用的儲存參數；更多資訊請參閱 [CREATE TABLE](sql-createtable.md) 文件中的[儲存參數](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。為了向後相容性，資料表的 `WITH` 子句也可以包含 `OIDS=FALSE`，以指定新資料表的資料列不應包含 OID（物件識別碼）；`OIDS=TRUE` 已不再支援。

`WITHOUT OIDS`
:   這是用來宣告資料表 `WITHOUT OIDS` 的向後相容語法；建立 `WITH
    OIDS` 的資料表已不再支援。

`ON COMMIT`
:   暫存資料表在交易區塊結束時的行為可以使用 `ON COMMIT` 來控制。三個選項如下：

    `PRESERVE ROWS`
    :   在交易結束時不採取任何特殊動作。這是預設行為。

    `DELETE ROWS`
    :   暫存資料表中的所有資料列會在每個交易區塊結束時被刪除。基本上，就是在每次提交時自動執行一次 [`TRUNCATE`](sql-truncate.md)。

    `DROP`
    :   暫存資料表會在目前交易區塊結束時被移除。

`TABLESPACE tablespace_name`
:   *`tablespace_name`* 是要在其中建立新資料表的資料表空間名稱。若未指定，會參考 [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE)；若資料表是暫存的，則參考 [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES)。

*`query`*
:   一個 [`SELECT`](sql-select.md)、[`TABLE`](sql-select.md#SQL-TABLE) 或 [`VALUES`](sql-values.md) 命令，或是執行預備之 `SELECT`、`TABLE` 或 `VALUES` 查詢的 [`EXECUTE`](sql-execute.md) 命令。

`WITH [ NO ] DATA`
:   此子句指定查詢所產生的資料是否應該複製到新資料表中。若否，則只複製資料表結構。預設是複製資料。

<a id="id-1.9.3.86.7"></a>

## 注意事項

此命令在功能上類似於 [SELECT INTO](sql-selectinto.md)，但較建議使用此命令，因為它比較不容易與 `SELECT INTO` 語法的其他用法混淆。此外，`CREATE
TABLE AS` 提供的功能是 `SELECT INTO` 所提供功能的超集合。

<a id="id-1.9.3.86.8"></a>

## 範例

建立一個新資料表 `films_recent`，只包含資料表 `films` 中的近期項目：

```

CREATE TABLE films_recent AS
  SELECT * FROM films WHERE date_prod >= '2002-01-01';
```

要完整複製一個資料表，也可以使用以 `TABLE` 命令表示的簡短形式：

```

CREATE TABLE films2 AS
  TABLE films;
```

使用預備陳述式建立一個新的暫存資料表 `films_recent`，只包含資料表 `films` 中的近期項目。新資料表會在提交時被移除：

```

PREPARE recentfilms(date) AS
  SELECT * FROM films WHERE date_prod > $1;
CREATE TEMP TABLE films_recent ON COMMIT DROP AS
  EXECUTE recentfilms('2002-01-01');
```

<a id="id-1.9.3.86.9"></a>

## 相容性

`CREATE TABLE AS` 符合 SQL 標準。以下是非標準的擴充：

* 標準要求子查詢子句前後加上括號；在 PostgreSQL 中，這些括號是選用的。
* 在標準中，`WITH [ NO ] DATA` 子句是必要的；在 PostgreSQL 中則是選用的。
* PostgreSQL 處理暫存資料表的方式與標準相當不同；詳細資訊請參閱 [CREATE TABLE](sql-createtable.md)。
* `WITH` 子句是 PostgreSQL 的擴充語法；儲存參數不在標準中。
* PostgreSQL 的資料表空間概念並不是標準的一部分。因此，`TABLESPACE` 子句是擴充語法。

<a id="id-1.9.3.86.10"></a>

## 另請參閱

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [CREATE TABLE](sql-createtable.md), [EXECUTE](sql-execute.md), [SELECT](sql-select.md), [SELECT INTO](sql-selectinto.md), [VALUES](sql-values.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtableas.html)（原文版本：18.6；核對日期：2026-10-04）
