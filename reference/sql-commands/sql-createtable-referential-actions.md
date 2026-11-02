# CREATE TABLE：外鍵參照動作

[返回 CREATE TABLE 主頁](sql-createtable.md)。

<a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-NO-ACTION"></a>

## `NO ACTION` [#](#sql-createtable-parms-references-refact-no-action) <a href="#sql-createtable-parms-references-refact-no-action" id="sql-createtable-parms-references-refact-no-action"></a>

若刪除或更新會造成違反外鍵限制條件，就產生錯誤。若限制條件已延遲，而在檢查限制條件時仍存在任何參照的資料列，就會在那時產生此錯誤。這是預設動作。
<a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-RESTRICT"></a>

## `RESTRICT` [#](#sql-createtable-parms-references-refact-restrict) <a href="#sql-createtable-parms-references-refact-restrict" id="sql-createtable-parms-references-refact-restrict"></a>

若要刪除或更新的資料列與參照資料表中的某個資料列相符，就產生錯誤。即使動作之後的狀態不會違反外鍵限制條件，這也會阻止該動作。特別是，它會阻止將被參照的資料列更新為不同但比較結果相等的值。（但它不會阻止將欄位更新為相同值的「無操作」更新。）

在時態外鍵中不支援此選項。
<a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-CASCADE"></a>

## `CASCADE` [#](#sql-createtable-parms-references-refact-cascade) <a href="#sql-createtable-parms-references-refact-cascade" id="sql-createtable-parms-references-refact-cascade"></a>

分別為：刪除參照了被刪除資料列的任何資料列，或將參照欄位的值更新為被參照欄位的新值。

在時態外鍵中不支援此選項。
<a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-NULL"></a>

## `SET NULL [ ( column_name [, ... ] ) ]` [#](#sql-createtable-parms-references-refact-set-null) <a href="#sql-createtable-parms-references-refact-set-null" id="sql-createtable-parms-references-refact-set-null"></a>

將所有參照欄位，或參照欄位中指定的子集合，設為 null。只有 `ON DELETE` 動作才能指定欄位的子集合。

在時態外鍵中不支援此選項。
<a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-DEFAULT"></a>

## `SET DEFAULT [ ( column_name [, ... ] ) ]` [#](#sql-createtable-parms-references-refact-set-default) <a href="#sql-createtable-parms-references-refact-set-default" id="sql-createtable-parms-references-refact-set-default"></a>

將所有參照欄位，或參照欄位中指定的子集合，設為其預設值。只有 `ON DELETE` 動作才能指定欄位的子集合。（若預設值不是 null，被參照資料表中必須存在與預設值相符的資料列，否則操作會失敗。）

在時態外鍵中不支援此選項。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtable.html)（原文版本：18.6；核對日期：2026-10-04）
