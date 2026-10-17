<a id="INDEX-COST-ESTIMATION"></a>

## 63.6. 索引成本估算函式 [#](#INDEX-COST-ESTIMATION)

`amcostestimate` 函式會收到描述某個可能之索引掃描的資訊，包括已判定可搭配該索引使用的 WHERE 與 ORDER BY 子句清單。它必須傳回存取該索引之成本的估計值，以及 WHERE 子句的選擇率（也就是在索引掃描期間將被擷取的父資料表資料列所佔的比例）。在簡單的情況下，成本估算器幾乎所有的工作都可以藉由呼叫最佳化器中的標準常式來完成；提供 `amcostestimate` 函式的用意，是讓索引存取方法能夠提供索引類型特有的知識，以便在有可能改進標準估計時加以改進。

每個 `amcostestimate` 函式都必須具有以下簽章：

```

void
amcostestimate (PlannerInfo *root,
                IndexPath *path,
                double loop_count,
                Cost *indexStartupCost,
                Cost *indexTotalCost,
                Selectivity *indexSelectivity,
                double *indexCorrelation,
                double *indexPages);
```

前三個參數是輸入：

*`root`*
:   規劃器關於正在處理之查詢的資訊。

*`path`*
:   正在考慮的索引存取路徑。除了成本與選擇率的值以外，所有欄位都是有效的。

*`loop_count`*
:   應納入成本估計的索引掃描重複次數。在考慮於巢狀迴圈連接的內側使用參數化掃描時，這個值通常會大於一。請注意，成本估計仍應只針對單次掃描；較大的 *`loop_count`* 表示可能適合將多次掃描之間的某些快取效應納入考量。

後五個參數是以傳址方式傳遞的輸出：

*`*indexStartupCost`*
:   設為索引啟動處理的成本

*`*indexTotalCost`*
:   設為索引處理的總成本

*`*indexSelectivity`*
:   設為索引選擇率

*`*indexCorrelation`*
:   設為索引掃描順序與底層資料表順序之間的相關係數

*`*indexPages`*
:   設為索引葉頁面的數量

請注意，成本估算函式必須以 C 撰寫，而不是用 SQL 或任何可用的程序語言撰寫，因為它們必須存取規劃器／最佳化器的內部資料結構。

索引存取成本應該使用 `src/backend/optimizer/path/costsize.c` 所使用的參數來計算：循序擷取一個磁碟區塊的成本為 `seq_page_cost`，非循序擷取的成本為 `random_page_cost`，而處理一個索引資料列的成本通常應取 `cpu_index_tuple_cost`。此外，對於索引處理期間所呼叫的任何比較運算子（特別是索引條件（indexquals）本身的求值），都應該計入 `cpu_operator_cost` 的適當倍數。

存取成本應該包含與掃描索引本身相關的所有磁碟與 CPU 成本，但*不*包含擷取或處理由索引所識別之父資料表資料列的成本。

「啟動成本」是總掃描成本中，在我們能夠開始擷取第一個資料列之前就必須花費的部分。對大多數索引而言，這可以視為零，但啟動成本高的索引類型可能會想將它設為非零值。

*`indexSelectivity`* 應設為在索引掃描期間將被擷取之父資料表資料列的估計比例。在有損查詢的情況下，這個值通常會高於實際通過給定條件之資料列的比例。

*`indexCorrelation`* 應設為索引順序與資料表順序之間的相關性（範圍介於 -1.0 與 1.0 之間）。這用來調整從父資料表擷取資料列之成本的估計。

*`indexPages`* 應設為葉頁面的數量。這用來估計平行索引掃描的工作程序數量。

當 *`loop_count`* 大於一時，傳回的數字應該是對索引進行任何一次掃描時預期的平均值。

<a id="id-1.10.15.12.13"></a>

**成本估算**

典型的成本估算器會依下列步驟進行：

1. 根據給定的條件，估計並傳回將被存取之父資料表資料列的比例。在沒有任何索引類型特有知識的情況下，使用標準的最佳化器函式 `clauselist_selectivity()`：

   ```

   *indexSelectivity = clauselist_selectivity(root, path->indexquals,
                                              path->indexinfo->rel->relid,
                                              JOIN_INNER, NULL);
   ```
2. 估計掃描期間將被存取的索引資料列數量。對許多索引類型而言，這等於 *`indexSelectivity`* 乘以索引中的資料列數，但也可能更多。（請注意，索引以頁面與資料列計的大小可以從 `path->indexinfo` 結構取得。）
3. 估計掃描期間將被擷取的索引頁面數量。這可能就是 *`indexSelectivity`* 乘以索引以頁面計的大小。
4. 計算索引存取成本。通用的估算器可能會這樣做：

   ```

   /*
    * Our generic assumption is that the index pages will be read
    * sequentially, so they cost seq_page_cost each, not random_page_cost.
    * Also, we charge for evaluation of the indexquals at each index row.
    * All the costs are assumed to be paid incrementally during the scan.
    */
   cost_qual_eval(&index_qual_cost, path->indexquals, root);
   *indexStartupCost = index_qual_cost.startup;
   *indexTotalCost = seq_page_cost * numIndexPages +
       (cpu_index_tuple_cost + index_qual_cost.per_tuple) * numIndexTuples;
   ```

   不過，上述做法並未考慮到索引讀取在重複索引掃描之間的攤提效果。
5. 估計索引相關性。對於單一欄位上的簡單有序索引，這可以從 pg_statistic 取得。若相關性未知，保守的估計值為零（無相關性）。

成本估算函式的範例可以在 `src/backend/utils/adt/selfuncs.c` 中找到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/index-cost-estimation.html)（原文版本：18.6；核對日期：2026-10-17）
