# SELECT INTO

SELECT INTO — 以查詢結果建立一個新資料表

### 語法

```text
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    * | expression [ [ AS ] output_name ] [, ...]
    INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY expression [, ...] ]
    [ HAVING condition [, ...] ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
    [ FOR { UPDATE | SHARE } [ OF table_name [, ...] ] [ NOWAIT ] [...] ]
```

### 說明

SELECT INTO 會建立一個新的資料表並使用查詢産生的資料填入。資料不會回傳到用戶端，即使它具有普通的 SELECT。新資料表的欄位具有與 SELECT 的輸出欄位相關聯的名稱和資料型別。

### 參數

`TEMPORARY` 或 `TEMP`

如果指定的話，則資料表被建立為臨時資料表。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

`UNLOGGED`

如果指定的話，則將此表建立為無日誌記錄的資料表。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

_`new_table`_

要建立的資料表名稱（可加上綱要名稱）。

所有其他參數在 [SELECT](select.md) 下詳細描述。

### 注意

[CREATE TABLE AS](create-table-as.md) 在功能上類似於 SELECT INTO。CREATE TABLE AS 是推薦的語法，因為這種 SELECT INTO 形式在 ECPG 或 PL/pgSQL 中不可用，它們會以不同的方式解釋 INTO 子句。此外，CREATE TABLE AS 提供了 SELECT INTO 提供的功能的更多功能。

要將 OID 加到 SELECT INTO 所建立的資料表中，請啟用 [default\_with\_oids](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/19.13.-ban-ben-yu-ping-tai-de-xiang-rong-xing.md#19-13-1-previous-postgresql-versions) 組態變數。或者，以 CREATE TABLE AS 與 WITH OIDS 子句一起使用。

### 範例

建立一個新的資料表 films\_recent，其中只包含來自資料表 film 的最新項目：

```text
SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
```

### 相容性

SQL 標準使用 SELECT INTO 將查詢結果表示為主機程序的 scalar 變量，而不是建立新資料表。這確實是 ECPG（參閱[第 35 章](../../iv.-yong-hu-duan-jie-mian/ecpg-embedded-sql-in-c/)）和 PL/pgSQL（參見[第 42 章](../../v.-zi-liao-ku-cheng-shi-she-ji/42.-pl-pgsql-sql-procedural-language.md)）中的用法。SELECT INTO 用於結果資料表建立的 PostgreSQL 用法是歷史性的。在新的程式中最好使用 CREATE TABLE AS 來達到此目的。

### 參閱

[CREATE TABLE AS](create-table-as.md)

