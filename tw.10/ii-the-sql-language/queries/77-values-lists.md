# 7.7. 列舉資料[^1]

VALUES 提供了一種產生「靜態資料表」的方法，可以在查詢中使用，而不必實際創建和寫入磁碟上的資料表。其語法是

```
VALUES ( expression [, ...] ) [, ...]
```

每個括號內的表示式列表在資料表中生成一個資料列。列表必須具有相同數量的元素（即資料表中的欄位數），並且每個列表中的對應條目必須具有兼容的資料型別。 分配給結果中每個欄位的實際資料型別，使用與 UNION 相同的規則來給定（請參閱[第 10.5 節](/ii-the-sql-language/type-conversion/105-union-case-and-related-constructs.md)）。

如下範例所示：

```
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

將回傳一個兩個欄位三個資料列的資料表。這實際上相當於：

```
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

預設情況下，PostgreSQL 會將名稱 column1、column2 等分配給 VALUES 資料表的欄位。欄位名稱並不是由 SQL 標準規定的，不同的資料庫系統會以不同的方式賦予，所以通常以資料表別名列表覆寫預設名稱會比較好，如下所示：

```
=> SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t (num,letter);
 num | letter
-----+--------
   1 | one
   2 | two
   3 | three
(3 rows)
```

在語法上，VALUES 接在表示式列表之後被視為等同於：

```
SELECT select_list FROM table_expression
```

並可以出現在任何一個 SELECT 可以使用的地方。例如，你可以將其用作為 UNION 的一部分，或者為其增加排序規則（ORDER BY、LIMIT 和 OFFSET）。在 INSERT 命令中，VALUES 最常來作為資料源，其次最常在子查詢。

關於更多訊息，請參閱 [VALUES](/vi-reference/i-sql-commands/values.md)。

---

[^1]: [PostgreSQL: Documentation: 10: 7.7. VALUES Lists](https://www.postgresql.org/docs/10/static/queries-values.html)

