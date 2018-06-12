---
description: 版本：10
---

# CREATE TABLE AS

CREATE TABLE AS — 從查詢結果來定義一個新資料表

### 語法

```text
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ WITH ( storage_parameter [= value] [, ... ] ) | WITH OIDS | WITHOUT OIDS ]
    [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

### 說明

CREATE TABLE AS 建立一個資料表並且以 SELECT 指令産生的資料填入。資料表欄位具有與 SELECT 的輸出列表相關聯的名稱與資料型別（除此之外，你也可以透過給予明確欄位來重寫欄位名稱）。

CREATE TABLE AS 與建立檢視表具有一些相似之處，但實際上完全不同：它建立一個新的資料表並僅對該查詢進行一次性運算以填入新資料表。新資料表將不隨查詢來源資料表的後續變更而改變。相比之下，無論何時查詢，檢視資料表都會重新運算其所定義的 SELECT 語句。

### 參數

`GLOBAL` or `LOCAL`

忽略相容性。不推薦使用這個關鍵字；有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

`TEMPORARY` or `TEMP`

如果指定，則資料表被建立為臨時資料表。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

`UNLOGGED`

如果指定，則將該資料表建立為無日誌記錄的資料表。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

`IF NOT EXISTS`

如果已存在具有相同名稱的關連，則不要拋出錯誤。 在這種情況下發布 NOTICE。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

_`table_name`_

要建立的資料表名稱（可以加上綱要名稱）。

_`column_name`_

新資料表中欄位的名稱。如果未提供欄位名稱，則從查詢的輸出欄位名稱中取得它們。

`WITH (` _`storage_parameter`_ \[= _`value`_\] \[, ... \] \)

此子句為新資料表指定可選用的儲存參數；請參閱[儲存參數](create-table.md#storage-parameters)了解更多訊息。WITH 子句還可以包含 OIDS = TRUE（或只是 OIDS）來指定新資料表的資料列應具有分配給它們的 OID（物件指標），或者 OIDS = FALSE 來指定行不應具有 OID。有關更多訊息，請參閱 [CREATE TABLE](create-table.md)。

`WITH OIDS`  
`WITHOUT OIDS`

這些過時的語法分別等同於 WITH（OIDS）和 WITH（OIDS = FALSE）。如果您希望同時提供 OIDS 設定和儲存參數，則必須使用 WITH（...）語法；請參閱上個段落。

`ON COMMIT`

使用 ON COMMIT 可以控制交易事務區塊結尾時的臨時資料表行為。有三個選項是：

`PRESERVE ROWS`

交易結束時不會採取特殊行動。這是預設行為。

`DELETE ROWS`

臨時資料表中的所有資料列將在每個交易事務區塊的末尾被刪除。本質上，每次提交都會自動完成 TRUNCATE。

`DROP`

臨時資料表將在目前交易事務區塊的結尾被刪除。

`TABLESPACE` _`tablespace_name`_

tablespace\_name 是要在其中建立新資料表的資料表空間名稱。如果未指定，則查詢 [default\_tablespace](../../server-administration/runtime-config/runtime-config-client.md#19-11-1-cha-ju-de-hang)，如果該資料表是臨時資料表，則為 [temp\_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#19-11-1-cha-ju-de-hang)。

_`query`_

[SELECT](select.md)，[TABLE](select.md#table-command) 或 [VALUES](values.md) 指令或執行預備好 SELECT，TABLE 或 VALUES 查詢的 [EXECUTE ](execute.md)指令。

`WITH [ NO ] DATA`

此子句指定是否將查詢産生的資料複製到新資料表中。如果不是，則就只複製資料表結構。預設值是複製資料。

### 注意

此指令在功能上類似於 SELECT INTO，但通常會優先使用這個，因為它不太可能與 SELECT INTO 語法的其他用法混淆。基本上，CREATE TABLE AS 的功能包含了 SELECT INTO 所提供的功能。

CREATE TABLE AS 指令允許使用者明確指定是否應包含 OID。如果未明確指定 OID 的存在，則使用 [default\_with\_oids ](../../server-administration/runtime-config/19.13.-ban-ben-yu-ping-tai-de-xiang-rong-xing.md#19-13-1-previous-postgresql-versions)的設定變數。

### 範例

建立一個新的資料表 films\_recent，其中只包含來自資料表 film 的最新項目：

```text
CREATE TABLE films_recent AS
  SELECT * FROM films WHERE date_prod >= '2002-01-01';
```

要完全複製資料表，也可以使用 TABLE 指令的簡短格式：

```text
CREATE TABLE films2 AS
  TABLE films;
```

使用預備查詢語句建立一個新的臨時資料表 films\_recent，僅包含來自資料表 film 的最近項目。新資料表具有 OID，並將在 commit 時丢棄：

```text
PREPARE recentfilms(date) AS
  SELECT * FROM films WHERE date_prod > $1;
CREATE TEMP TABLE films_recent WITH (OIDS) ON COMMIT DROP AS
  EXECUTE recentfilms('2002-01-01');
```

### 相容性

CREATE TABLE AS 符合 SQL 標準。以下是非標準的延伸功能：

* 在標準中需要括住子查詢子句的括號；在 PostgreSQL 中，這些括號是選用的。
* 在標準中，WITH \[NO\] DATA 子句是必須的；在 PostgreSQL 中是選用的。
* PostgreSQL 以一種與標準不同的方式處理臨時資料表；有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。
* WITH 子句是一個 PostgreSQL 延伸功能；標準中既沒有儲存參數也沒有 OID。
* PostgreSQL 資料表空間的概念並不是標準的一部分。因此，TABLESPACE 子句是一個延伸功能。

### See Also

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [CREATE TABLE](create-table.md), [EXECUTE](execute.md), [SELECT](select.md), [SELECT INTO](select-into.md), [VALUES](values.md)

