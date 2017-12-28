# 7.8. 遞迴查詢[^1]

WITH 提供了一種撰寫用於更複雜查詢輔助語句的方法。這些通常被稱為公用資料表表示式或 CTE 的宣告可以被想成是定義僅存在於一個查詢中的臨時資料表。WITH子句中的每個輔助語句都可以是SELECT，INSERT，UPDATE或DELETE; 並且WITH子句本身附加到也可以是SELECT，INSERT，UPDATE或DELETE的主語句。

### 7.8.1. `SELECT`in`WITH`

SELECT 中 WITH 的基本價值是將複雜的查詢分解為較為簡單的部分。一個例子是：

```
WITH regional_sales AS (
        SELECT region, SUM(amount) AS total_sales
        FROM orders
        GROUP BY region
     ), top_regions AS (
        SELECT region
        FROM regional_sales
        WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
     )
SELECT region,
       product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;
```

其中僅顯示最上層銷售區域中的每個產品的銷售總計。WITH子句定義了兩個名為 regional\_sales 和 top\_regions 的輔助語句，其中  top\_size 使用 region\_sales 的輸出，top\_regions 的輸出在主 SELECT 語句中使用。這個例子本來可以不用 WITH 編寫，但是我們需要兩層的SELECT 子查詢。按照這種方式更容易一些。

選擇性的 RECURSIVE 修飾字將 WITH 從單純的語法便利性增加了標準SQL所無法實現的功能。使用 RECURSIVE，WITH 查詢可以引用它自己的輸出。一個非常簡單的例子是這個查詢來從1到100的整數求和：

```
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

遞迴 WITH 查詢的一般形式始終是非遞迴子句，然後是 UNION（或 UNION ALL），然後是遞迴子句，其中只有遞迴子句可以包含對查詢自己的輸出引用。這樣的查詢執行如下：

執行**遞迴查詢**

1. 執行非遞迴子句。 對於 UNION（但不是 UNION ALL），丟棄重複的資料列。在遞迴查詢的結果中包含所有剩餘的資料列，並將它們放在臨時的工作資料表中。

2. 只要工作資料表不是空的，就重複這些步驟：

   1. 執行遞迴子句，將工作資料表的當下的內容替換為遞迴自我引用。對於 UNION（但不是 UNION ALL），將重複的資料列及和之前結果重覆的資料列都丟棄。在遞迴查詢的結果中包含所有剩餘的資料列，並將其放置在臨時中介資料表中。

   2. 將工作資料表的內容替換為中介資料表的內容，然後清空中介資料表。

> ### 注意
>
> 嚴格地說，這個過程仍然是疊代的而不是遞迴的，但是 RECURSIVE 是 SQL 標準委員會所選擇的用字。

在上面的例子中，工作資料表在每一步驟中只有一個資料列，並且在連續的步驟中從 1 取值到 100。在第 100 步時，由於 WHERE 子句而沒有輸出，因此結束查詢。

遞迴查詢通常用於處理分層或樹狀結構的資料。一個實用的例子是，這個查詢用來找到產品的所有直接和間接子部分，只產出一個顯示即時包含這些資訊的資料表：

```
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
  )
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part
```

使用遞迴查詢時，務必確保查詢的遞迴部分最終不回傳資料列，否則查詢將會無限循環。有時，使用 UNION 而不是 UNION ALL 可以透過丟棄與先前輸出行重覆的資料列來達成此目的。但是，循環查詢通常不涉及完全重複的輸出資料列：可能需要檢查一個或幾個欄位，以查看是否在之前就已經達到相同的點。處理這種情況的標準方法是從已經訪問過的陣列中，計算其值。例如，以下查詢是，使用連接欄位搜尋資料表網路圖：

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
        SELECT g.id, g.link, g.data, 1
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1
        FROM graph g, search_graph sg
        WHERE g.id = sg.link
)
SELECT * FROM search_graph;
```

如果連接關係包含循環，則此查詢將持續循環。因為我們需要一個「depth」輸出，只要將 UNION ALL 更改為 UNION 就不會停止循環。相反地，我們需要瞭解到，在遵循特定的連接路徑的情況下，我們是否再一次到達同樣的資料列。我們增加兩個欄位 path 和 cycle 到有循環傾向的查詢之中：

```
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
        SELECT g.id, g.link, g.data, 1,
          ARRAY[g.id],
          false
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1,
          path || g.id,
          g.id = ANY(path)
        FROM graph g, search_graph sg
        WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;
```

除了防止循環之外，陣列內容本身通常也是有用的，表示為達到任何特定資料列所採取的「path」。

在一般情況下，需要檢查多個欄位來識別是一個循環，請使用資料列陣列來處理。例如，如果我們需要比較欄位 f1 和 f2：

```
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
        SELECT g.id, g.link, g.data, 1,
          ARRAY[ROW(g.f1, g.f2)],
          false
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1,
          path || ROW(g.f1, g.f2),
          ROW(g.f1, g.f2) = ANY(path)
        FROM graph g, search_graph sg
        WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;
```

> ### 小技巧
>
> 在通常情況下，只需要檢查一個欄位來識別週期，就會省略 ROW\(\) 語法。這可以使用簡單的陣列而不用複合型別的陣列，從而獲得效率。

### Tip

The recursive query evaluation algorithm produces its output in breadth-first search order. You can display the results in depth-first search order by making the outer query`ORDER BY`a“path”column constructed in this way.

A helpful trick for testing queries when you are not certain if they might loop is to place a`LIMIT`in the parent query. For example, this query would loop forever without the`LIMIT`:

```
WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

This works becausePostgreSQL's implementation evaluates only as many rows of a`WITH`query as are actually fetched by the parent query. Using this trick in production is not recommended, because other systems might work differently. Also, it usually won't work if you make the outer query sort the recursive query's results or join them to some other table, because in such cases the outer query will usually try to fetch all of the`WITH`query's output anyway.

A useful property of`WITH`queries is that they are evaluated only once per execution of the parent query, even if they are referred to more than once by the parent query or sibling`WITH`queries. Thus, expensive calculations that are needed in multiple places can be placed within a`WITH`query to avoid redundant work. Another possible application is to prevent unwanted multiple evaluations of functions with side-effects. However, the other side of this coin is that the optimizer is less able to push restrictions from the parent query down into a`WITH`query than an ordinary subquery. The`WITH`query will generally be evaluated as written, without suppression of rows that the parent query might discard afterwards. \(But, as mentioned above, evaluation might stop early if the reference\(s\) to the query demand only a limited number of rows.\)

The examples above only show`WITH`being used with`SELECT`, but it can be attached in the same way to`INSERT`,`UPDATE`, or`DELETE`. In each case it effectively provides temporary table\(s\) that can be referred to in the main command.

### 7.8.2. Data-Modifying Statements in`WITH`

You can use data-modifying statements \(`INSERT`,`UPDATE`, or`DELETE`\) in`WITH`. This allows you to perform several different operations in the same query. An example is:

```
WITH moved_rows AS (
    DELETE FROM products
    WHERE
        "date" 
>
= '2010-10-01' AND
        "date" 
<
 '2010-11-01'
    RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;
```

This query effectively moves rows from`products`to`products_log`. The`DELETE`in`WITH`deletes the specified rows from`products`, returning their contents by means of its`RETURNING`clause; and then the primary query reads that output and inserts it into`products_log`.

A fine point of the above example is that the`WITH`clause is attached to the`INSERT`, not the sub-`SELECT`within the`INSERT`. This is necessary because data-modifying statements are only allowed in`WITH`clauses that are attached to the top-level statement. However, normal`WITH`visibility rules apply, so it is possible to refer to the`WITH`statement's output from the sub-`SELECT`.

Data-modifying statements in`WITH`usually have`RETURNING`clauses \(see[Section 6.4](https://www.postgresql.org/docs/10/static/dml-returning.html)\), as shown in the example above. It is the output of the`RETURNING`clause,\_not\_the target table of the data-modifying statement, that forms the temporary table that can be referred to by the rest of the query. If a data-modifying statement in`WITH`lacks a`RETURNING`clause, then it forms no temporary table and cannot be referred to in the rest of the query. Such a statement will be executed nonetheless. A not-particularly-useful example is:

```
WITH t AS (
    DELETE FROM foo
)
DELETE FROM bar;
```

This example would remove all rows from tables`foo`and`bar`. The number of affected rows reported to the client would only include rows removed from`bar`.

Recursive self-references in data-modifying statements are not allowed. In some cases it is possible to work around this limitation by referring to the output of a recursive`WITH`, for example:

```
WITH RECURSIVE included_parts(sub_part, part) AS (
    SELECT sub_part, part FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
  )
DELETE FROM parts
  WHERE part IN (SELECT part FROM included_parts);
```

This query would remove all direct and indirect subparts of a product.

Data-modifying statements in`WITH`are executed exactly once, and always to completion, independently of whether the primary query reads all \(or indeed any\) of their output. Notice that this is different from the rule for`SELECT`in`WITH`: as stated in the previous section, execution of a`SELECT`is carried only as far as the primary query demands its output.

The sub-statements in`WITH`are executed concurrently with each other and with the main query. Therefore, when using data-modifying statements in`WITH`, the order in which the specified updates actually happen is unpredictable. All the statements are executed with the same_snapshot_\(see[Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html)\), so they cannot“see”one another's effects on the target tables. This alleviates the effects of the unpredictability of the actual order of row updates, and means that`RETURNING`data is the only way to communicate changes between different`WITH`sub-statements and the main query. An example of this is that in

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;
```

the outer`SELECT`would return the original prices before the action of the`UPDATE`, while in

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;
```

the outer`SELECT`would return the updated data.

Trying to update the same row twice in a single statement is not supported. Only one of the modifications takes place, but it is not easy \(and sometimes not possible\) to reliably predict which one. This also applies to deleting a row that was already updated in the same statement: only the update is performed. Therefore you should generally avoid trying to modify a single row twice in a single statement. In particular avoid writing`WITH`sub-statements that could affect the same rows changed by the main statement or a sibling sub-statement. The effects of such a statement will not be predictable.

At present, any table used as the target of a data-modifying statement in`WITH`must not have a conditional rule, nor an`ALSO`rule, nor an`INSTEAD`rule that expands to multiple statements.

---

[^1]: [PostgreSQL: Documentation: 10: 7.8. WITH Queries \(Common Table Expressions\)](https://www.postgresql.org/docs/10/static/queries-with.html)

