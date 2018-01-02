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
>
> ### Tip
>
> 遞迴查詢評估演算法以廣度優先搜尋次序產生其輸出。你也可以按照深度優先的搜尋順序顯示結果，方法是以外部查詢 ORDER BY 「path」欄位。

當你不確定是否可能會形成循環時，測試查詢的一個有用的技巧是在父查詢中放置一個 LIMIT。例如，這個查詢沒有 LIMIT，將會無限循環：

```
WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

這是有效的，因為 PostgreSQL 的實作的關係，看起來像是執行一個 WITH 查詢的許多行，但實際上是由父查詢獲取的。不建議在產品階段中使用這個技巧，因為其他系統的工作方式可能不同。此外，如果你以外部查詢對遞迴查詢的結果進行排序或將它們與某個其他資料表交叉查詢，則通常不可行，因為在這種情況下，外部的查詢通常會嘗試獲取所有 WITH 查詢的輸出。

WITH 查詢的一個有用的屬性是，每次執行父查詢時，它們只被評估一次，即使它們被父查詢或兄弟的 WITH 查詢引用多次。因此，在多個地方需要昂貴的計算可以放在 WITH 查詢中以避免重複的工作。另一個可能的應用是防止不必要多重評估的副作用。然而，如同硬幣有反面一樣，查詢優化器不太可能限制從父查詢向下推入的是 WITH 查詢而不是普通的子查詢。WITH 查詢通常會按其撰寫方式進行評估，而不會抑制父查詢之後可能丟棄的資料列。（但是，如上所述，如果查詢的引用只需要有限的資料列數量，評估可能會提前結束。）

上面的例子只說明 WITH 與 SELECT 一起使用，但是它也可以以同樣的方式附加到INSERT、UPDATE 或 DELETE。在每種情況下，它都有效地提供了可以在主查詢中可引用的臨時資料表。

### 7.8.2. WITH 中的資料修改語法

你可以在 WITH 中使用資料修改語法（INSERT、UPDATE 或 DELETE）。 這使你可以在同一個查詢中執行多個不同的操作。範例如下：

```
WITH moved_rows AS (
    DELETE FROM products
    WHERE "date" >= '2010-10-01' AND
          "date" < '2010-11-01'
    RETURNING *
) INSERT INTO products_log SELECT * FROM moved_rows;
```

這個查詢有效地將資料列從 products 搬移到products\_log。WITH 中的 DELETE 從 products 中刪除指定的資料列，透過 RETURNING 子句回傳其內容；然後主查詢讀取該輸出並將其插入到 products\_log 中。

上面例子的很好的一點是，WITH 子句被附加到 INSERT，而不是使用 INSERT 中的子查詢。這是必要的，因為資料修改語句只能在最上層語句的 WITH 子句中使用。但是，以一般的 WITH 變數可見性規則，可以從子查詢中引用 WITH 語句的輸出。

WITH 中的資料修改語句通常具有 RETURNING 子句（詳見[第 6.4 節](/ii-the-sql-language/data-manipulation/64-returning-data-from-modified-rows.md)），如上例所示。它是 RETURNING 子句的輸出，而不是資料修改語句的目標資料表，它構成了查詢的其餘部分可以引用的臨時資料表。如果 WITH 中的資料修改語句沒有 RETURNING 子句，則它就不構成臨時資料表，並且不能在查詢的其餘部分引用。這樣的陳述將被執行。一個不是特別有用的例子是：

```
WITH t AS (
    DELETE FROM foo
) DELETE FROM bar;
```

這個例子將刪除 foo 和 bar 資料表中的所有資料列。報告給客戶端的受影響資料列的數量將只包括從 bar 中刪除的資料列。

資料修改語句中的遞迴的自我引用是不被允許的。在某些情況下，可以通過引用遞迴 WITH 的輸出來解決這個限制，例如：

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

該查詢將刪除產品的所有直接和間接子部分。

WITH 中的資料修改語句只執行一次，並且一定會完成，與主查詢是否讀取其所有（或者甚至是任何）輸出無關。請注意，這與 SELECT 在 WITH 之中的規則不同：如前一節所述，僅在主要查詢要求其輸出的情況下執行 SELECT。

WITH 中的子語句會與主查詢平行執行。因此，在 WITH 中使用資料修改語句時，指定更新的實際發生順序是不可預知的。所有的語句都使用相同的快照執行（見[第 13 章](/ii-the-sql-language/concurrency-control.md)），所以它們不能在目標資料表上「看到」對方所產生的變更。 這減輕了資料列更新的實際順序時不可預測性的影響，並且意味著回傳資料是在不同 WITH 子語句和主查詢之間傳遞變化的唯一方式。 範例如下所示：

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;
```

外面的 SELECT 將會在 UPDATE 的執行之前就回傳原始價格

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;
```

外面的 SELECT 將會回傳更新後的資料。

企圖在單個語句中更新同一資料列兩次是不被允許的。只有一個修改會發生，但是要可靠地預測哪一個是不容易的（有時不可能）。 這也適用於刪除已在同一語句中更新的資料列：僅更新會被執行。因此，通常你應該避免企圖在單個語句中修改單個資料列兩次。特別注意避免在 WITH 子語句中使用可能會被主語句或其子查詢所影響的資料列。這種查詢語句的效果是不可預測的。

目前來說，在 WITH 中使用資料修改語句的目標資料表都不能有條件規則，也不能有 ALSO 規則，也不能有擴展為多個語句的 INSTEAD 規則。

---

[^1]: [PostgreSQL: Documentation: 10: 7.8. WITH Queries \(Common Table Expressions\)](https://www.postgresql.org/docs/10/static/queries-with.html)

