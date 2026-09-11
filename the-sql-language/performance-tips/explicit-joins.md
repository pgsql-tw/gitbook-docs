<a id="EXPLICIT-JOINS"></a>

## 14.3. 以明確的 `JOIN` 子句控制規劃器 [#](#EXPLICIT-JOINS)

<a id="id-1.5.13.6.2"></a>

使用明確的 `JOIN` 語法，可以在某種程度上控制查詢規劃器。為了說明這一點的重要性，我們先需要一些背景知識。

在一個簡單的聯結查詢中，例如：

```

SELECT * FROM a, b, c WHERE a.id = b.id AND b.ref = c.id;
```

規劃器可以自由地以任何順序聯結所給的資料表。例如，它可以產生一個查詢計畫，先使用 `WHERE` 條件 `a.id = b.id` 將 A 與 B 聯結，再使用另一個 `WHERE` 條件將 C 與這個聯結後的資料表聯結。或者，它可以先將 B 與 C 聯結，再將 A 與該結果聯結。又或者，它可以先將 A 與 C 聯結，再將它們與 B 聯結——但這樣會很沒有效率，因為 `WHERE` 子句中沒有可以用來最佳化這個聯結的條件，必須建立 A 與 C 的完整笛卡兒積。（PostgreSQL 執行器中的所有聯結都是在兩個輸入資料表之間進行的，因此必須以上述其中一種方式逐步建立結果。）重點是，這些不同的聯結方式會產生語意上相同的結果，但執行成本可能天差地遠。因此，規劃器會探索所有這些可能性，試圖找出最有效率的查詢計畫。

當查詢只涉及兩三個資料表時，需要考慮的聯結順序並不多。但可能的聯結順序數量，會隨著資料表數量的增加而呈指數成長。超過大約十個輸入資料表之後，對所有可能性進行窮舉搜尋就不再可行，甚至只有六、七個資料表時，規劃所需的時間也可能長得令人困擾。當輸入資料表太多時，PostgreSQL 規劃器會從窮舉搜尋切換為在有限數量的可能性中進行*遺傳*（genetic）機率式搜尋。（切換的門檻由執行時期參數 [geqo_threshold](../../server-administration/runtime-config/runtime-config-query.md#GUC-GEQO-THRESHOLD) 設定。）遺傳搜尋所需的時間較少，但不一定能找到最好的計畫。

當查詢涉及外部聯結時，規劃器的自由度會比一般（內部）聯結來得小。例如，考慮：

```

SELECT * FROM a LEFT JOIN (b JOIN c ON (b.ref = c.id)) ON (a.id = b.id);
```

雖然這個查詢的限制條件表面上與前一個範例相似，但語意並不相同，因為對於 A 中每一筆在 B 與 C 的聯結中沒有相符資料列的資料列，都必須輸出一筆資料列。因此，規劃器在這裡沒有選擇聯結順序的餘地：它必須先將 B 與 C 聯結，再將 A 與該結果聯結。相應地，這個查詢的規劃時間會比前一個查詢短。在其他情況下，規劃器也許能判斷出有不只一種聯結順序是安全的。例如，給定：

```

SELECT * FROM a LEFT JOIN b ON (a.bid = b.id) LEFT JOIN c ON (a.cid = c.id);
```

先將 A 與 B 或與 C 聯結都是有效的。目前，只有 `FULL JOIN` 會完全限制聯結順序。大多數涉及 `LEFT JOIN` 或 `RIGHT JOIN` 的實際情況，都可以在某種程度上重新排列。

明確的內部聯結語法（`INNER JOIN`、`CROSS JOIN` 或不加修飾的 `JOIN`）在語意上與在 `FROM` 中列出輸入關聯相同，因此不會限制聯結順序。

儘管大多數種類的 `JOIN` 並不會完全限制聯結順序，但仍然可以指示 PostgreSQL 查詢規劃器，無論如何都將所有 `JOIN` 子句視為對聯結順序的限制。例如，下面這三個查詢在邏輯上是等價的：

```

SELECT * FROM a, b, c WHERE a.id = b.id AND b.ref = c.id;
SELECT * FROM a CROSS JOIN b CROSS JOIN c WHERE a.id = b.id AND b.ref = c.id;
SELECT * FROM a JOIN (b JOIN c ON (b.ref = c.id)) ON (a.id = b.id);
```

但如果我們告訴規劃器要遵循 `JOIN` 的順序，第二個與第三個查詢的規劃時間就會比第一個短。只有三個資料表時，這個效果不值得擔心，但在資料表很多時，它可能是救命的關鍵。

要強制規劃器遵循明確的 `JOIN` 所安排的聯結順序，請將執行時期參數 [join_collapse_limit](../../server-administration/runtime-config/runtime-config-query.md#GUC-JOIN-COLLAPSE-LIMIT) 設為 1。（其他可能的值會在下面討論。）

你不需要完全限制聯結順序才能縮短搜尋時間，因為在一般 `FROM` 清單的項目中使用 `JOIN` 運算子是可以的。例如，考慮：

```

SELECT * FROM a CROSS JOIN b, c, d, e WHERE ...;
```

在 `join_collapse_limit` = 1 的情況下，這會強制規劃器先將 A 與 B 聯結，再將它們與其他資料表聯結，但除此之外不會限制它的選擇。在這個範例中，可能的聯結順序數量會減少為原本的五分之一。

以這種方式限制規劃器的搜尋，是一項實用的技巧，既可以縮短規劃時間，也可以引導規劃器找到良好的查詢計畫。如果規劃器預設選擇了不好的聯結順序，你可以透過 `JOIN` 語法強制它選擇更好的順序——前提是你知道更好的順序是什麼。建議多加實驗。

一個與規劃時間密切相關的議題，是將子查詢摺疊（collapse）到其上層查詢中。例如，考慮：

```

SELECT *
FROM x, y,
    (SELECT * FROM a, b, c WHERE something) AS ss
WHERE somethingelse;
```

這種情況可能源自使用了包含聯結的視圖；該視圖的 `SELECT` 規則會被插入到視圖參照的位置，產生一個很像上面這樣的查詢。通常，規劃器會嘗試將子查詢摺疊到上層查詢中，產生：

```

SELECT * FROM x, y, a, b, c WHERE something AND somethingelse;
```

這通常會產生比分別規劃子查詢更好的計畫。（例如，外層的 `WHERE` 條件可能使得先將 X 與 A 聯結就能排除 A 的許多資料列，從而避免建立子查詢完整的邏輯輸出。）但同時，我們也增加了規劃時間；在這裡，我們以一個五方聯結的問題，取代了兩個各自獨立的三方聯結問題。由於可能性的數量呈指數成長，這會造成很大的差異。規劃器會避免陷入龐大的聯結搜尋問題：如果摺疊子查詢會使上層查詢產生超過 `from_collapse_limit` 個 `FROM` 項目，就不會摺疊該子查詢。你可以藉由調高或調低這個執行時期參數，在規劃時間與計畫品質之間取捨。

[from_collapse_limit](../../server-administration/runtime-config/runtime-config-query.md#GUC-FROM-COLLAPSE-LIMIT) 與 [join_collapse_limit](../../server-administration/runtime-config/runtime-config-query.md#GUC-JOIN-COLLAPSE-LIMIT) 的名稱相似，因為它們做的事情幾乎相同：一個控制規劃器何時會「攤平」子查詢，另一個則控制它何時會攤平明確的聯結。通常，你會將 `join_collapse_limit` 設為與 `from_collapse_limit` 相等（讓明確的聯結與子查詢表現相似），或將 `join_collapse_limit` 設為 1（如果你想以明確的聯結來控制聯結順序）。但如果你想要精細調整規劃時間與執行時間之間的取捨，也可以將它們設為不同的值。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/explicit-joins.html)（原文版本：18.6；核對日期：2026-09-11）
