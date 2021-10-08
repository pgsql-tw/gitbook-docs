# 5.3. Generated Columns

Generated column \(自動欄位\)是特殊的欄位，它的內容由其他欄位的內容計算得出。相對於資料表來說，就是欄位形態的 View。Generated column 有兩種：stored 和 virtual。 Stored 的自動欄位在寫入（插入或更新）時進行計算，會像正常欄位一樣佔用儲存空間。Virtual 的自動欄位則不佔用任何儲存空間，而是在讀取時會對其進行計算。因此，虛擬的自動欄位類似於檢視表\(view\)，而儲存的自動欄位則類似於具體化檢視表\(materialized view\)（但會自動更新）。 PostgreSQL 目前僅實作了儲存的自動欄位。

使用 `GENERATED ALWAYS AS` 語法來產生自動欄位，舉例來說：

```text
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

務必要加上 `STORED` 關鍵字以寫入自動欄位. 更多細節請參閱 [CREATE TABLE](https://www.postgresql.org/docs/12/sql-createtable.html)

使用 `INSERT` 或 `UPDATE` 指令時，不能直接指定內容至自動欄位，但可以使用 `DEFAULT` 關鍵字來設定預設值。

針對「包含預設值的欄位」及 「自動欄位」進行比較:

當資料列第一次被寫入時，如果該欄位沒有提供任何值，將採用預設值寫入; 而自動欄位則是在資料列被更新時，根據其他欄位來產生對應的值，該值無法被覆寫。

+ 「包含預設值的欄位」通常不會參考到表格的其他欄位; 而「自動欄位」通常都會參考到其他欄位。
+ 「含預設值的欄位」在設定預設值時可以使用易變函數 \(volatile function\)，舉例來說: `random()` 或者是取得當前時間的函式; 而「自動欄位」則不允許使用。

「自動欄位」和「包含自動欄位的表格」有一些限制：

* 自動欄位的表示式只能使用 immutable 函數，不能使用子查詢或以任何方式引用同筆資料以外的任何內容。
* 自動欄位的表示式不能引用另一個自動欄位。
* 自動欄位的表示式不能引用系統欄位（tableoid 除外）。
* 自動欄位不能有欄位預設值或識別定義。
* 自動欄位不能是分割區主鍵的一部分。
* 外部資料表可以具有自動欄位。有關詳細資訊，請參閱 [CREATE FOREIGN TABLE](../../reference/sql-commands/create-foreign-table.md)。

其他注意事項適用於自動欄位的使用。

* 自動欄位與其一般欄位分開維護存取權限。因此，可以對其進行安排，以便設定可以從自動欄位中讀取，但不能從一般欄位中讀取的特定角色。
* 從概念上講，在執行事件觸發器之前，會先更新自動欄位。因此，在 BEFORE 觸發器中對基本欄位所做的更新將先反映在自動欄位中。但是相反地，不允許在觸發器之前讀取自動欄位。

