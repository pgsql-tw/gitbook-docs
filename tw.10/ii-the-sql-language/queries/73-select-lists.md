# 7.3. 取得資料列表[^1]

如前一節所述，SELECT 指令中的資料示表表示式透過各種可能地組合資料表、view、消除資料列、分組等來建構中介的虛擬資料表。這個資料表最終會被傳遞給資料列表的處理。資料列表確認中介資料表的哪些欄位是實際上要輸出的。

### 7.3.1. 資料列表項目

最簡單的選擇列表是\*，它表示資料表表示式產生的所有欄位。否則，資料列表是逗號分隔的參數表示式列表（如[第 4.2 節](/ii-the-sql-language/sql-syntax/42-value-expressions.md)中所定義的）。例如，它可能是欄位名稱的列表：

```
SELECT a, b, c FROM ...
```

欄位名稱 a、b 和 c 是 FROM 子句中資料表的欄位的實際名稱，或者是由[第 7.2.1.2 節](/ii-the-sql-language/queries/72-table-expressions.md)中所賦予它們的別名。資料列表中可用的命名空間與 WHERE 子句中的命名空間相同，除非是使用分組查詢，在這種情況下，它與 HAVING 子句中的相同。

如果多個資料表具有相同名稱的欄位，則還必須加上資料表的名稱，如下所示：

```
SELECT tbl1.a, tbl2.a, tbl1.b FROM ...
```

處理多個資料表時，查詢特定資料表的所有欄位也是可以的：

```
SELECT tbl1.*, tbl2.a FROM ...
```

有關 table\_name.\* 表示法的更多信息，請參閱第 8.16.5 節。

如果在資料列表中使用任意值表示式，則概念上是它將新的虛擬欄位加到回傳的資料表中。參數表示式對每個結果資料列計算一次，將該資料列的值替換為任何欄位引用。但是資料列表中的表示式不必引用 FROM 子句的資料表表示式中的任何欄位；例如，它們可以是常數算術表示式。

### 7.3.2. 欄位命名標籤

資料列表中的項目可以被分配用於後續處理的名稱，例如在 ORDER BY 子句中使用或由用戶端應用程序顯示。 例如：

```
SELECT a AS value, b + c AS sum FROM ...
```

如果沒有使用 AS 指定輸出欄位的名稱，系統將分配一個預設的欄位名稱。對於簡單欄位的引用，就是引用欄位的名稱。對於函數呼叫，就是函數的名稱。對於複雜的表示式，系統將會產成一個通用的名稱。

AS 關鍵字是選用的，但前提是新的欄位名稱不為任何PostgreSQL 關鍵字（請參閱附錄C）。為避免與關鍵字意外撞名，你可以對欄位名稱使用雙引號。例如，VALUE 是一個關鍵字，所以就不能這樣使用：

```
SELECT a value, b + c AS sum FROM ...
```

但這樣就可以了：

```
SELECT a "value", b + c AS sum FROM ...
```

為了防止未來可能增加的關鍵字，建議你習慣使用 AS 或總是在欄位名稱使用雙引號。

### Note

The naming of output columns here is different from that done in the`FROM`clause \(see[Section 7.2.1.2](https://www.postgresql.org/docs/10/static/queries-table-expressions.html#queries-table-aliases)\). It is possible to rename the same column twice, but the name assigned in the select list is the one that will be passed on.

### 7.3.3. `DISTINCT`

After the select list has been processed, the result table can optionally be subject to the elimination of duplicate rows. The`DISTINCT`key word is written directly after`SELECT`to specify this:

```
SELECT DISTINCT 
select_list
 ...
```

\(Instead of`DISTINCT`the key word`ALL`can be used to specify the default behavior of retaining all rows.\)

Obviously, two rows are considered distinct if they differ in at least one column value. Null values are considered equal in this comparison.

Alternatively, an arbitrary expression can determine what rows are to be considered distinct:

```
SELECT DISTINCT ON (
expression
 [
, 
expression
 ...
]) 
select_list
 ...
```

Here\_`expression`\_is an arbitrary value expression that is evaluated for all rows. A set of rows for which all the expressions are equal are considered duplicates, and only the first row of the set is kept in the output. Note that the“first row”of a set is unpredictable unless the query is sorted on enough columns to guarantee a unique ordering of the rows arriving at the`DISTINCT`filter. \(`DISTINCT ON`processing occurs after`ORDER BY`sorting.\)

The`DISTINCT ON`clause is not part of the SQL standard and is sometimes considered bad style because of the potentially indeterminate nature of its results. With judicious use of`GROUP BY`and subqueries in`FROM`, this construct can be avoided, but it is often the most convenient alternative.

---

[^1]: [PostgreSQL: Documentation: 10: 7.3. Select Lists](https://www.postgresql.org/docs/10/static/queries-select-lists.html)

