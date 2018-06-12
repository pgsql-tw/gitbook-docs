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

### Parameters

`GLOBAL` or `LOCAL`

Ignored for compatibility. Use of these keywords is deprecated; refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`TEMPORARY` or `TEMP`

If specified, the table is created as a temporary table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`UNLOGGED`

If specified, the table is created as an unlogged table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`IF NOT EXISTS`

Do not throw an error if a relation with the same name already exists. A notice is issued in this case. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details._`table_name`_

The name \(optionally schema-qualified\) of the table to be created.

_`column_name`_

The name of a column in the new table. If column names are not provided, they are taken from the output column names of the query.

`WITH (` _`storage_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional storage parameters for the new table; see [Storage Parameters](https://www.postgresql.org/docs/10/static/sql-createtable.html#SQL-CREATETABLE-STORAGE-PARAMETERS) for more information. The `WITH` clause can also include `OIDS=TRUE` \(or just `OIDS`\) to specify that rows of the new table should have OIDs \(object identifiers\) assigned to them, or `OIDS=FALSE` to specify that the rows should not have OIDs. See [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for more information.

`WITH OIDS`  
`WITHOUT OIDS`

These are obsolescent syntaxes equivalent to `WITH (OIDS)` and `WITH (OIDS=FALSE)`, respectively. If you wish to give both an `OIDS` setting and storage parameters, you must use the `WITH ( ... )` syntax; see above.

`ON COMMIT`

The behavior of temporary tables at the end of a transaction block can be controlled using `ON COMMIT`. The three options are:

`PRESERVE ROWS`

No special action is taken at the ends of transactions. This is the default behavior.

`DELETE ROWS`

All rows in the temporary table will be deleted at the end of each transaction block. Essentially, an automatic [TRUNCATE](https://www.postgresql.org/docs/10/static/sql-truncate.html) is done at each commit.

`DROP`

The temporary table will be dropped at the end of the current transaction block.`TABLESPACE` _`tablespace_name`_

The _`tablespace_name`_ is the name of the tablespace in which the new table is to be created. If not specified, [default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE) is consulted, or [temp\_tablespaces](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TEMP-TABLESPACES) if the table is temporary.

_`query`_

A [SELECT](https://www.postgresql.org/docs/10/static/sql-select.html), [TABLE](https://www.postgresql.org/docs/10/static/sql-select.html#SQL-TABLE), or [VALUES](https://www.postgresql.org/docs/10/static/sql-values.html) command, or an [EXECUTE](https://www.postgresql.org/docs/10/static/sql-execute.html) command that runs a prepared `SELECT`, `TABLE`, or `VALUES` query.

`WITH [ NO ] DATA`

This clause specifies whether or not the data produced by the query should be copied into the new table. If not, only the table structure is copied. The default is to copy the data.

### Notes

This command is functionally similar to [SELECT INTO](https://www.postgresql.org/docs/10/static/sql-selectinto.html), but it is preferred since it is less likely to be confused with other uses of the `SELECT INTO` syntax. Furthermore, `CREATE TABLE AS` offers a superset of the functionality offered by `SELECT INTO`.

The `CREATE TABLE AS` command allows the user to explicitly specify whether OIDs should be included. If the presence of OIDs is not explicitly specified, the [default\_with\_oids](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#GUC-DEFAULT-WITH-OIDS) configuration variable is used.

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

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [CREATE TABLE](create-table.md), EXECUTE, [SELECT](select.md), [SELECT INTO](select-into.md), [VALUES](values.md)

