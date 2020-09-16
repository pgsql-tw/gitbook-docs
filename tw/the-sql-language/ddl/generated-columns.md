# 5.3. Generated Columns

Generated column \(自動欄位\)是特殊的欄位，它的內容由其他欄位的內容計算得出。相對於資料表來說，就是欄位形態的 View。Generated column 有兩種：stored 和 virtual。 Stored 的自動欄位在寫入（插入或更新）時進行計算，會像正常欄位一樣佔用儲存空間。Virtual 的自動欄位則不佔用任何儲存空間，而是在讀取時會對其進行計算。因此，虛擬的自動欄位類似於檢視表\(view\)，而儲存的自動欄位則類似於具體化檢視表\(materialized view\)（但會自動更新）。 PostgreSQL 目前僅實作了儲存的自動欄位。

To create a generated column, use the `GENERATED ALWAYS AS` clause in `CREATE TABLE`, for example:

```text
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

The keyword `STORED` must be specified to choose the stored kind of generated column. See [CREATE TABLE](https://www.postgresql.org/docs/12/sql-createtable.html) for more details.

A generated column cannot be written to directly. In `INSERT` or `UPDATE` commands, a value cannot be specified for a generated column, but the keyword `DEFAULT` may be specified.

Consider the differences between a column with a default and a generated column. The column default is evaluated once when the row is first inserted if no other value was provided; a generated column is updated whenever the row changes and cannot be overridden. A column default may not refer to other columns of the table; a generation expression would normally do so. A column default can use volatile functions, for example `random()` or functions referring to the current time; this is not allowed for generated columns.

Several restrictions apply to the definition of generated columns and tables involving generated columns:

* The generation expression can only use immutable functions and cannot use subqueries or reference anything other than the current row in any way.
* A generation expression cannot reference another generated column.
* A generation expression cannot reference a system column, except `tableoid`.
* A generated column cannot have a column default or an identity definition.
* A generated column cannot be part of a partition key.
* Foreign tables can have generated columns. See [CREATE FOREIGN TABLE](https://www.postgresql.org/docs/12/sql-createforeigntable.html) for details.

Additional considerations apply to the use of generated columns.

* Generated columns maintain access privileges separately from their underlying base columns. So, it is possible to arrange it so that a particular role can read from a generated column but not from the underlying base columns.
* Generated columns are, conceptually, updated after `BEFORE` triggers have run. Therefore, changes made to base columns in a `BEFORE` trigger will be reflected in generated columns. But conversely, it is not allowed to access generated columns in `BEFORE` triggers.

