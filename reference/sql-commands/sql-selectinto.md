<a id="id-1.9.3.173.1"></a>

## SELECT INTO

SELECT INTO — 從查詢結果定義一個新資料表

## 語法

```

[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    [ { * | expression [ [ AS ] output_name ] } [, ...] ]
    INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY expression [, ...] ]
    [ HAVING condition ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
    [ FOR { UPDATE | SHARE } [ OF table_name [, ...] ] [ NOWAIT ] [...] ]
```

<a id="id-1.9.3.173.5"></a>

## 說明

`SELECT INTO` 會建立一個新資料表，並以查詢計算出的資料填入。
資料不會像一般的 `SELECT` 那樣回傳給用戶端。新資料表的欄位
會沿用 `SELECT` 輸出欄位的名稱與資料型別。

<a id="id-1.9.3.173.6"></a>

## 參數

`TEMPORARY` 或 `TEMP`
:   若指定此項，資料表會建立為暫存資料表。詳情請參閱
    [CREATE TABLE](sql-createtable.md)。

`UNLOGGED`
:   若指定此項，資料表會建立為非日誌資料表。詳情請參閱
    [CREATE TABLE](sql-createtable.md)。

*`new_table`*
:   要建立的資料表名稱（可加上綱要限定）。

其他所有參數的詳細說明，請參閱 [SELECT](sql-select.md)。

<a id="id-1.9.3.173.7"></a>

## 注意事項

[`CREATE TABLE AS`](sql-createtableas.md) 在功能上與
`SELECT INTO` 相似。建議使用 `CREATE TABLE AS`
的語法，因為這種形式的 `SELECT
INTO` 無法在 ECPG
或 PL/pgSQL 中使用，因為它們對
`INTO` 子句的解讀方式不同。此外，
`CREATE TABLE AS` 提供的功能是
`SELECT INTO` 所提供功能的超集合。

與 `CREATE TABLE AS` 不同的是，`SELECT
INTO` 不允許指定資料表的存取方法（如
[`USING method`](sql-createtable.md#SQL-CREATETABLE-METHOD)）或資料表的
表空間（如 [`TABLESPACE tablespace_name`](sql-createtable.md#SQL-CREATETABLE-TABLESPACE)）等屬性。
如有需要，請改用 `CREATE TABLE AS`。因此，新資料表會採用
預設的資料表存取方法。詳情請參閱
[default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD)。

<a id="id-1.9.3.173.8"></a>

## 範例

建立一個新資料表 `films_recent`，只包含資料表
`films` 中較新近的項目：

```

SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
```

<a id="id-1.9.3.173.9"></a>

## 相容性

SQL 標準使用 `SELECT INTO` 表示將值選入宿主程式的
純量變數，而非建立新資料表。這確實就是 ECPG
（見[第 34 章](../../client-interfaces/ecpg/README.md)）與
PL/pgSQL（見[第 41 章](../../server-programming/plpgsql/README.md)）中所採用的用法。
PostgreSQL 用 `SELECT
INTO` 來表示建立資料表，是歷史沿革所致。其他一些 SQL
實作也以同樣方式使用 `SELECT INTO`（但大多數 SQL
實作改為支援 `CREATE TABLE AS`）。
撇開這類相容性考量不談，在新程式碼中最好還是為此目的使用
`CREATE TABLE AS`。

<a id="id-1.9.3.173.10"></a>

## 另請參閱

[CREATE TABLE AS](sql-createtableas.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-selectinto.html)（原文版本：18.6；核對日期：2026-09-28）
