<a id="QUERIES-WITH"></a>

## 7.8. `WITH` 查詢（通用資料表運算式） [#](#QUERIES-WITH)

[7.8.1. `WITH` 中的 `SELECT`](queries-with.md#QUERIES-WITH-SELECT)

[7.8.2. 遞迴查詢](queries-with.md#QUERIES-WITH-RECURSIVE)

[7.8.3. 通用資料表運算式的具體化](queries-with.md#QUERIES-WITH-CTE-MATERIALIZATION)

[7.8.4. `WITH` 中的資料修改陳述式](queries-with.md#QUERIES-WITH-MODIFYING)

<a id="id-1.5.6.12.2"></a><a id="id-1.5.6.12.3"></a>

`WITH` 提供了一種撰寫輔助陳述式的方式，供較大的查詢使用。這些陳述式通常稱為通用資料表運算式（Common Table Expression，CTE），可以把它們想成是定義了只為單一查詢而存在的暫存資料表。`WITH` 子句中的每個輔助陳述式可以是 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 或 `MERGE`；而 `WITH` 子句本身則附加在一個主要陳述式上，該陳述式同樣可以是 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 或 `MERGE`。

<a id="QUERIES-WITH-SELECT"></a>

### 7.8.1. `WITH` 中的 `SELECT` [#](#QUERIES-WITH-SELECT)

在 `WITH` 中使用 `SELECT` 的基本價值，在於將複雜的查詢拆解為較簡單的部分。例如：

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

這會只顯示銷售額最高的地區中，各產品的銷售總額。`WITH` 子句定義了兩個名為 `regional_sales` 與 `top_regions` 的輔助陳述式，其中 `regional_sales` 的輸出用在 `top_regions` 中，而 `top_regions` 的輸出則用在主要的 `SELECT` 查詢中。這個範例也可以不用 `WITH` 撰寫，但那樣就需要兩層巢狀的子 `SELECT`。以這種方式撰寫會比較容易理解一些。

<a id="QUERIES-WITH-RECURSIVE"></a>

### 7.8.2. 遞迴查詢 [#](#QUERIES-WITH-RECURSIVE)

<a id="id-1.5.6.12.6.2.1"></a>
選用的 `RECURSIVE` 修飾詞，讓 `WITH` 從單純的語法便利，變成一項能完成標準 SQL 中原本無法做到之事的功能。使用 `RECURSIVE` 時，`WITH` 查詢可以參照自己的輸出。一個非常簡單的範例，是下面這個計算 1 到 100 整數總和的查詢：

```

WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

遞迴 `WITH` 查詢的一般形式，一律是先有一個*非遞迴項*（non-recursive term），接著是 `UNION`（或 `UNION ALL`），然後是一個*遞迴項*（recursive term），其中只有遞迴項可以包含對查詢自身輸出的參照。這樣的查詢會依下列方式執行：

<a id="id-1.5.6.12.6.3"></a>

**遞迴查詢的求值**

1. 對非遞迴項求值。如果是 `UNION`（而不是 `UNION ALL`），就捨棄重複的資料列。將其餘的所有資料列納入遞迴查詢的結果中，同時也放入一個暫時的*工作資料表*（working table）。
2. 只要工作資料表不是空的，就重複下列步驟：

   1. 對遞迴項求值，並以工作資料表目前的內容取代遞迴的自我參照。如果是 `UNION`（而不是 `UNION ALL`），就捨棄重複的資料列，以及與先前任何結果資料列重複的資料列。將其餘的所有資料列納入遞迴查詢的結果中，同時也放入一個暫時的*中間資料表*（intermediate table）。
   2. 以中間資料表的內容取代工作資料表的內容，然後清空中間資料表。

### 注意

雖然 `RECURSIVE` 允許以遞迴方式指定查詢，但在內部，這類查詢是以迭代方式求值的。

在上面的範例中，工作資料表在每一步都只有一筆資料列，並在連續的步驟中依序取得 1 到 100 的值。在第 100 步時，由於 `WHERE` 子句的關係沒有任何輸出，因此查詢就結束了。

遞迴查詢通常用來處理階層式或樹狀結構的資料。一個實用的範例，是在只有一個顯示直接包含關係之資料表的情況下，找出某產品所有直接與間接子零件的查詢：

```

WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity * pr.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part
```

<a id="QUERIES-WITH-SEARCH"></a>

#### 7.8.2.1. 搜尋順序 [#](#QUERIES-WITH-SEARCH)

使用遞迴查詢計算樹狀結構的走訪時，你可能會想以深度優先或廣度優先的順序排列結果。做法是在其他資料欄位之外，再計算一個排序欄位，並在最後用它來排序結果。請注意，這實際上並不會控制查詢求值時走訪資料列的順序；與 SQL 中的一切一樣，那取決於實作。這種做法只是提供一種方便的方式，在事後排列結果。

要產生深度優先的順序，我們為每一筆結果資料列計算一個陣列，記錄到目前為止已走訪過的資料列。例如，考慮下面這個使用 `link` 欄位搜尋資料表 `tree` 的查詢：

```

WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree;
```

要加入深度優先的排序資訊，可以這樣寫：

```

WITH RECURSIVE search_tree(id, link, data, path) AS (
    SELECT t.id, t.link, t.data, ARRAY[t.id]
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, path || t.id
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

在需要使用多個欄位才能識別一筆資料列的一般情況下，請使用資料列的陣列。例如，如果我們需要追蹤欄位 `f1` 與 `f2`：

```

WITH RECURSIVE search_tree(id, link, data, path) AS (
    SELECT t.id, t.link, t.data, ARRAY[ROW(t.f1, t.f2)]
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, path || ROW(t.f1, t.f2)
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

### 提示

在只需要追蹤一個欄位的常見情況下，請省略 `ROW()` 語法。這樣就可以使用簡單的陣列，而不是複合型別的陣列，進而提升效率。

要產生廣度優先的順序，可以加入一個追蹤搜尋深度的欄位，例如：

```

WITH RECURSIVE search_tree(id, link, data, depth) AS (
    SELECT t.id, t.link, t.data, 0
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, depth + 1
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY depth;
```

要得到穩定的排序，請將資料欄位加入作為次要的排序欄位。

### 提示

遞迴查詢的求值演算法會以廣度優先搜尋的順序產生輸出。不過，這是實作細節，依賴它或許並不妥當。每一層中資料列的順序肯定是未定義的，因此無論如何可能都會需要某種明確的排序。

系統有內建的語法可以計算深度優先或廣度優先的排序欄位。例如：

```

WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
) SEARCH DEPTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;

WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
) SEARCH BREADTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;
```

這種語法在內部會被展開成類似上述手寫形式的內容。`SEARCH` 子句指定要進行深度優先還是廣度優先搜尋、要追蹤以供排序的欄位清單，以及一個將包含可用於排序之結果資料的欄位名稱。該欄位會被隱含地加入 CTE 的輸出資料列中。

<a id="QUERIES-WITH-CYCLE"></a>

#### 7.8.2.2. 循環偵測 [#](#QUERIES-WITH-CYCLE)

使用遞迴查詢時，重要的是要確保查詢的遞迴部分最終不會再回傳任何 tuple，否則查詢會無限迴圈下去。有時候，使用 `UNION` 取代 `UNION ALL`，捨棄與先前輸出資料列重複的資料列，就能做到這一點。不過，循環往往並不涉及完全重複的輸出資料列：可能只需要檢查一個或幾個欄位，就能判斷是否曾經到達過同一個點。處理這類情況的標準方法，是計算一個由已走訪過之值組成的陣列。例如，再次考慮下面這個使用 `link` 欄位搜尋資料表 `graph` 的查詢：

```

WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 0
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
)
SELECT * FROM search_graph;
```

如果 `link` 關係中包含循環，這個查詢就會陷入迴圈。由於我們需要「depth」輸出，單純將 `UNION ALL` 改為 `UNION` 並不能消除迴圈。我們需要的是，在沿著特定的連結路徑前進時，能夠辨識是否再次到達了同一筆資料列。我們在這個容易陷入迴圈的查詢中加入兩個欄位 `is_cycle` 與 `path`：

```

WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path) AS (
    SELECT g.id, g.link, g.data, 0,
      false,
      ARRAY[g.id]
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      g.id = ANY(path),
      path || g.id
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

除了防止循環之外，這個陣列值本身也常常很有用，因為它代表了到達任何特定資料列所經過的「路徑」。

在需要檢查多個欄位才能辨識循環的一般情況下，請使用資料列的陣列。例如，如果我們需要比較欄位 `f1` 與 `f2`：

```

WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path) AS (
    SELECT g.id, g.link, g.data, 0,
      false,
      ARRAY[ROW(g.f1, g.f2)]
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      ROW(g.f1, g.f2) = ANY(path),
      path || ROW(g.f1, g.f2)
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

### 提示

在只需要檢查一個欄位就能辨識循環的常見情況下，請省略 `ROW()` 語法。這樣就可以使用簡單的陣列，而不是複合型別的陣列，進而提升效率。

系統有內建的語法可以簡化循環偵測。上面的查詢也可以寫成這樣：

```

WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 1
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
) CYCLE id SET is_cycle USING path
SELECT * FROM search_graph;
```

它在內部會被改寫成上面的形式。`CYCLE` 子句依序指定要追蹤以偵測循環的欄位清單、一個顯示是否偵測到循環的欄位名稱，以及最後另一個用來追蹤路徑的欄位名稱。循環欄位與路徑欄位會被隱含地加入 CTE 的輸出資料列中。

### 提示

循環路徑欄位的計算方式，與上一節所示的深度優先排序欄位相同。一個查詢可以同時有 `SEARCH` 與 `CYCLE` 子句，但深度優先搜尋規格與循環偵測規格會造成重複的計算，因此只使用 `CYCLE` 子句並依路徑欄位排序會比較有效率。如果需要廣度優先的順序，那麼同時指定 `SEARCH` 與 `CYCLE` 就可能有用。

在不確定查詢是否可能陷入迴圈時，一個有用的測試技巧是在上層查詢中加上 `LIMIT`。例如，如果沒有 `LIMIT`，下面這個查詢就會永遠迴圈下去：

```

WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

這之所以可行，是因為 PostgreSQL 的實作只會對 `WITH` 查詢求值上層查詢實際取出的資料列數量。不建議在正式環境中使用這個技巧，因為其他系統的運作方式可能不同。此外，如果讓外層查詢對遞迴查詢的結果排序，或將它們與其他資料表聯結，這個技巧通常就不會奏效，因為在這些情況下，外層查詢通常無論如何都會試圖取出 `WITH` 查詢的所有輸出。

<a id="QUERIES-WITH-CTE-MATERIALIZATION"></a>

### 7.8.3. 通用資料表運算式的具體化 [#](#QUERIES-WITH-CTE-MATERIALIZATION)

`WITH` 查詢的一個實用特性是，即使上層查詢或同層的 `WITH` 查詢多次參照它，在上層查詢的每次執行中，它通常也只會求值一次。因此，需要在多處使用的高成本計算，可以放在 `WITH` 查詢中，以避免重複的工作。另一個可能的應用，是防止具有副作用的函式被不必要地多次求值。不過，這件事的另一面是，最佳化器無法將上層查詢的限制條件下推到被多次參照的 `WITH` 查詢中，因為那可能會影響 `WITH` 查詢輸出的所有用途，而它原本應該只影響其中一個。被多次參照的 `WITH` 查詢會照原本的寫法求值，而不會抑制上層查詢之後可能會捨棄的資料列。（但如上所述，如果對該查詢的參照只需要有限數量的資料列，求值可能會提早停止。）

不過，如果 `WITH` 查詢是非遞迴且沒有副作用的（也就是說，它是不包含 volatile 函式的 `SELECT`），就可以將它摺疊進上層查詢中，讓兩個查詢層級能夠一起最佳化。預設情況下，如果上層查詢只參照 `WITH` 查詢一次，就會這麼做；但如果上層查詢參照 `WITH` 查詢不只一次，則不會。你可以指定 `MATERIALIZED` 強制分開計算 `WITH` 查詢，或指定 `NOT MATERIALIZED` 強制將它合併到上層查詢中，以覆寫這項決定。後一種選擇有重複計算 `WITH` 查詢的風險，但如果每次使用 `WITH` 查詢時只需要 `WITH` 查詢完整輸出的一小部分，整體上仍然可能有所節省。

這些規則的一個簡單範例是

```

WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w WHERE key = 123;
```

這個 `WITH` 查詢會被摺疊，產生與下列查詢相同的執行計畫

```

SELECT * FROM big_table WHERE key = 123;
```

特別是，如果 `key` 上有索引，就很可能會使用它來只取出 `key = 123` 的資料列。另一方面，在

```

WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

中，`WITH` 查詢會被具體化，產生一份 `big_table` 的暫時副本，然後與自身聯結，完全無法受益於任何索引。如果寫成下面這樣，這個查詢的執行效率會高得多

```

WITH w AS NOT MATERIALIZED (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

這樣上層查詢的限制條件就可以直接套用在對 `big_table` 的掃描上。

以下是一個 `NOT MATERIALIZED` 可能不理想的範例

```

WITH w AS (
    SELECT key, very_expensive_function(val) as f FROM some_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.f = w2.f;
```

在這裡，將 `WITH` 查詢具體化可以確保 `very_expensive_function` 對每一筆資料表資料列只求值一次，而不是兩次。

上面的範例只顯示 `WITH` 與 `SELECT` 一起使用，但它也可以用相同的方式附加到 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 上。在每一種情況下，它實際上都提供了可以在主要指令中參照的暫存資料表。

<a id="QUERIES-WITH-MODIFYING"></a>

### 7.8.4. `WITH` 中的資料修改陳述式 [#](#QUERIES-WITH-MODIFYING)

你可以在 `WITH` 中使用資料修改陳述式（`INSERT`、`UPDATE`、`DELETE` 或 `MERGE`）。這讓你可以在同一個查詢中執行多種不同的操作。例如：

```

WITH moved_rows AS (
    DELETE FROM products
    WHERE
        "date" >= '2010-10-01' AND
        "date" < '2010-11-01'
    RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;
```

這個查詢實際上會將資料列從 `products` 搬移到 `products_log`。`WITH` 中的 `DELETE` 會從 `products` 刪除指定的資料列，並透過它的 `RETURNING` 子句回傳這些資料列的內容；接著主要查詢會讀取該輸出，並將它插入 `products_log`。

上面這個範例的一個細節是，`WITH` 子句是附加在 `INSERT` 上，而不是 `INSERT` 中的子 `SELECT` 上。這是必要的，因為資料修改陳述式只允許出現在附加於最上層陳述式的 `WITH` 子句中。不過，一般的 `WITH` 可見性規則仍然適用，因此可以從子 `SELECT` 參照 `WITH` 陳述式的輸出。

如上面的範例所示，`WITH` 中的資料修改陳述式通常會有 `RETURNING` 子句（請參閱[第 6.4 節](../dml/dml-returning.md)）。形成可供查詢其餘部分參照之暫存資料表的，是 `RETURNING` 子句的輸出，*而不是*資料修改陳述式的目標資料表。如果 `WITH` 中的資料修改陳述式沒有 `RETURNING` 子句，它就不會形成暫存資料表，也無法在查詢的其餘部分中被參照。不過，這樣的陳述式仍然會被執行。一個不太有用的範例是：

```

WITH t AS (
    DELETE FROM foo
)
DELETE FROM bar;
```

這個範例會移除資料表 `foo` 與 `bar` 中的所有資料列。回報給用戶端的受影響資料列數，只會包含從 `bar` 移除的資料列。

資料修改陳述式中不允許遞迴的自我參照。在某些情況下，可以透過參照遞迴 `WITH` 的輸出來繞過這項限制，例如：

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

這個查詢會移除某個產品所有直接與間接的子零件。

`WITH` 中的資料修改陳述式只會執行一次，而且一定會執行到完成，無論主要查詢是否讀取了它們的全部（甚至任何）輸出。請注意，這與 `WITH` 中 `SELECT` 的規則不同：如上一節所述，`SELECT` 的執行只會進行到主要查詢需要其輸出的程度為止。

`WITH` 中的子陳述式會彼此並行執行，也會與主要查詢並行執行。因此，在 `WITH` 中使用資料修改陳述式時，指定的更新實際發生的順序是無法預測的。所有陳述式都以相同的*快照*（snapshot）執行（請參閱[第 13 章](../mvcc/README.md)），因此它們無法「看到」彼此對目標資料表所造成的影響。這減輕了資料列更新實際順序不可預測所帶來的影響，也表示 `RETURNING` 資料是在不同的 `WITH` 子陳述式與主要查詢之間傳遞變更的唯一方式。舉例來說，在

```

WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;
```

中，外層的 `SELECT` 會回傳 `UPDATE` 動作之前的原始價格；而在

```

WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;
```

中，外層的 `SELECT` 則會回傳更新後的資料。

不支援在單一陳述式中更新同一筆資料列兩次。只有其中一項修改會生效，但要可靠地預測是哪一項並不容易（有時甚至不可能）。這也適用於刪除在同一個陳述式中已經更新過的資料列：只會執行更新。因此，一般而言，應該避免在單一陳述式中修改同一筆資料列兩次。特別是，避免撰寫可能影響到主要陳述式或同層子陳述式所變更之相同資料列的 `WITH` 子陳述式。這種陳述式的效果將無法預測。

目前，在 `WITH` 中作為資料修改陳述式目標的任何資料表，都不能有條件式規則、`ALSO` 規則，或展開為多個陳述式的 `INSTEAD` 規則。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-with.html)（原文版本：18.6；核對日期：2026-09-11）
