<a id="DDL-GENERATED-COLUMNS"></a>

## 5.4. 產生欄位 [#](#DDL-GENERATED-COLUMNS)

<a id="id-1.5.4.6.2"></a>

產生欄位是一種特殊的欄位，它的值一律由其他欄位計算而來。因此，產生欄位之於欄位，就像是檢視表之於資料表。產生欄位有兩種：儲存式（stored）與虛擬（virtual）。儲存式產生欄位會在寫入（新增或更新）時計算，並且像一般欄位一樣佔用儲存空間。虛擬產生欄位不佔用儲存空間，而是在讀取時才計算。因此，虛擬產生欄位類似於檢視表，而儲存式產生欄位則類似於具體化檢視表（差別在於它一定會自動更新）。

若要建立產生欄位，請在 `CREATE TABLE` 中使用 `GENERATED ALWAYS AS` 子句，例如：

```

CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54)
);
```

產生欄位預設是虛擬的。請使用關鍵字 `VIRTUAL` 或 `STORED` 來明確指定。更多細節請參閱 [CREATE TABLE](../../reference/sql-commands/sql-createtable.md)。

產生欄位不能直接寫入。在 `INSERT` 或 `UPDATE` 指令中，不能為產生欄位指定值，但可以指定關鍵字 `DEFAULT`。

請思考具有預設值的欄位與產生欄位之間的差異。欄位預設值只有在資料列第一次被新增、而且沒有提供其他值時才會被求值一次；產生欄位則是每當資料列變動時就會更新，而且無法被覆寫。欄位預設值不能參照資料表的其他欄位；產生運算式通常則會這麼做。欄位預設值可以使用揮發性（volatile）函式，例如 `random()` 或參照目前時間的函式；產生欄位則不允許這麼做。

產生欄位的定義，以及含有產生欄位的資料表，有以下幾項限制：

* 產生運算式只能使用 immutable 函式，而且不能使用子查詢，也不能以任何方式參照目前資料列以外的東西。
* 產生運算式不能參照另一個產生欄位。
* 產生運算式不能參照系統欄位，`tableoid` 除外。
* 虛擬產生欄位不能使用使用者自訂型別，而且虛擬產生欄位的產生運算式不得參照使用者自訂的函式或型別，也就是說，它只能使用內建的函式或型別。這一點同樣適用於間接的情況，例如運算子或型別轉換底層所使用的函式或型別。（儲存式產生欄位沒有這項限制。）
* 產生欄位不能有欄位預設值，也不能有識別欄位定義。
* 產生欄位不能作為分割鍵的一部分。
* 外部資料表可以有產生欄位。細節請參閱 [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md)。
* 關於繼承與分割：

  * 如果父欄位是產生欄位，其子欄位也必須是相同種類（儲存式或虛擬）的產生欄位；不過子欄位可以有不同的產生運算式。

    對儲存式產生欄位而言，在新增或更新某筆資料列時實際套用的產生運算式，是與該資料列實體所在資料表相關聯的那一個。（這與欄位預設值的行為不同：對預設值而言，套用的是與查詢中所指名資料表相關聯的預設值。）對虛擬產生欄位而言，讀取資料表時套用的是查詢中所指名資料表的產生運算式。
  * 如果父欄位不是產生欄位，其子欄位也不能是產生欄位。
  * 對於繼承的資料表，如果你在 `CREATE TABLE ... INHERITS` 中寫下子欄位的定義而沒有加上任何 `GENERATED` 子句，那麼它的 `GENERATED` 子句會自動從父資料表複製過來。`ALTER TABLE ... INHERIT` 會要求父欄位與子欄位在產生狀態上必須已經相符，但不會要求它們的產生運算式相符。
  * 分割資料表的情況也類似，如果你在 `CREATE TABLE ... PARTITION OF` 中寫下子欄位的定義而沒有加上任何 `GENERATED` 子句，那麼它的 `GENERATED` 子句會自動從父資料表複製過來。`ALTER TABLE ... ATTACH PARTITION` 會要求父欄位與子欄位在產生狀態上必須已經相符，但不會要求它們的產生運算式相符。
  * 在多重繼承的情況下，如果有一個父欄位是產生欄位，那麼所有的父欄位都必須是產生欄位。如果它們的產生運算式不完全相同，那麼子欄位所要的運算式就必須明確指定。

使用產生欄位時還有其他需要考量的地方。

* 產生欄位的存取權限與其底層的基礎欄位是分開維護的。因此，可以安排成讓某個特定角色能夠讀取產生欄位，卻不能讀取底層的基礎欄位。

  對虛擬產生欄位而言，只有當產生運算式僅使用 leakproof 函式時（請參閱 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)），這種安排才算完全安全，但系統並不會強制檢查這一點。
* 產生運算式中所使用函式的權限，是在該運算式實際執行時（分別在寫入或讀取時）才檢查，就好像產生運算式是由使用該產生欄位的查詢直接呼叫的一樣。使用產生欄位的使用者必須擁有呼叫產生運算式所使用之所有函式的權限。產生運算式中的函式會以執行查詢之使用者的權限、或是函式擁有者的權限來執行，取決於這些函式定義為 `SECURITY INVOKER` 或 `SECURITY DEFINER`。
* 就概念上而言，產生欄位是在 `BEFORE` 觸發程序執行完畢之後才更新。因此，在 `BEFORE` 觸發程序中對基礎欄位所做的變更會反映到產生欄位上。但反過來說，在 `BEFORE` 觸發程序中不允許存取產生欄位。
* 在邏輯複寫期間，產生欄位可以依據 `CREATE PUBLICATION` 的參數 [`publish_generated_columns`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) 被複寫，或是將它們納入 `CREATE PUBLICATION` 指令的欄位清單中而被複寫。目前這只支援儲存式產生欄位。細節請參閱[第 29.6 節](../../server-administration/logical-replication/logical-replication-gencols.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-generated-columns.html)（原文版本：18.6；核對日期：2026-09-12）
