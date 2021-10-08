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

必須指定關鍵字 STORED 來作為自動欄位的儲存型別。相關的詳細說明，請參閱 [CREATE TABLE](../../reference/sql-commands/create-table.md)。

A generated column cannot be written to directly. In `INSERT` or `UPDATE` commands, a value cannot be specified for a generated column, but the keyword `DEFAULT` may be specified.

Consider the differences between a column with a default and a generated column. The column default is evaluated once when the row is first inserted if no other value was provided; a generated column is updated whenever the row changes and cannot be overridden. A column default may not refer to other columns of the table; a generation expression would normally do so. A column default can use volatile functions, for example `random()` or functions referring to the current time; this is not allowed for generated columns.

Several restrictions apply to the definition of generated columns and tables involving generated columns:

* 自動欄位的表示式只能使用 immutable 函數，不能使用子查詢或以任何方式引用同筆資料以外的任何內容。
* 自動欄位的表示式不能引用另一個自動欄位。
* 自動欄位的表示式不能引用系統欄位（tableoid 除外）。
* 自動欄位不能有欄位預設值或識別定義。
* 自動欄位不能是分割區主鍵的一部分。
* 外部資料表可以具有自動欄位。有關詳細資訊，請參閱 [CREATE FOREIGN TABLE](../../reference/sql-commands/create-foreign-table.md)。
* For inheritance:
  * If a parent column is a generated column, a child column must also be a generated column using the same expression. In the definition of the child column, leave off the `GENERATED` clause, as it will be copied from the parent.
  * In case of multiple inheritance, if one parent column is a generated column, then all parent columns must be generated columns and with the same expression.
  * If a parent column is not a generated column, a child column may be defined to be a generated column or not.

其他注意事項適用於自動欄位的使用。

* 自動欄位與其一般欄位分開維護存取權限。因此，可以對其進行安排，以便設定可以從自動欄位中讀取，但不能從一般欄位中讀取的特定角色。
* 從概念上講，在執行事件觸發器之前，會先更新自動欄位。因此，在 BEFORE 觸發器中對基本欄位所做的更新將先反映在自動欄位中。但是相反地，不允許在觸發器之前讀取自動欄位。

