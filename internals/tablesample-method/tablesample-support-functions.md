<a id="TABLESAMPLE-SUPPORT-FUNCTIONS"></a>

## 59.1. 取樣方法支援函式 [#](#TABLESAMPLE-SUPPORT-FUNCTIONS)

TSM 處理函式會傳回一個以 palloc 配置的 `TsmRoutine` 結構，其中包含指向下述各支援函式的指標。大部分函式都是必要的，但有些是選用的，這些函式的指標可以是 NULL。

```

void
SampleScanGetSampleSize (PlannerInfo *root,
                         RelOptInfo *baserel,
                         List *paramexprs,
                         BlockNumber *pages,
                         double *tuples);
```

此函式在規劃期間呼叫。它必須估計取樣掃描期間將讀取的關聯頁面數，以及該掃描將選取的 tuple 數。（例如，可以先估計取樣比例，再將
`baserel->pages` 與 `baserel->tuples`
這兩個數字乘上該比例，並務必將結果捨入為整數值，以求得這些估計。）
`paramexprs` 清單包含作為 `TABLESAMPLE` 子句參數的運算式。若估計時需要這些運算式的值，建議使用 `estimate_expression_value()` 嘗試將它們化簡為常數；但即使無法化簡，此函式也必須提供大小估計，而且即使這些值看起來無效，也不應該失敗（請記得它們只是執行時期值的估計）。
`pages` 與 `tuples` 參數是輸出參數。

```

void
InitSampleScan (SampleScanState *node,
                int eflags);
```

為執行 SampleScan 計畫節點進行初始化。
此函式在執行器啟動期間呼叫。
它應該執行處理開始之前所需的任何初始化。
`SampleScanState` 節點已經建立，但其 `tsm_state` 欄位為 NULL。
`InitSampleScan` 函式可以用 palloc 配置取樣方法所需的任何內部狀態資料，並將指向它的指標儲存在 `node->tsm_state` 中。
要掃描之資料表的相關資訊，可以透過 `SampleScanState` 節點的其他欄位取得（但請注意，
`node->ss.ss_currentScanDesc` 掃描描述子尚未設定）。
`eflags` 包含描述執行器對此計畫節點之運作模式的旗標位元。

當 `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` 為真時，
掃描並不會實際執行，因此此函式應該只做最低限度的工作，讓節點狀態對 `EXPLAIN`
與 `EndSampleScan` 而言有效即可。

此函式可以省略（將指標設為 NULL），此時
`BeginSampleScan` 必須執行取樣方法所需的所有初始化。

```

void
BeginSampleScan (SampleScanState *node,
                 Datum *params,
                 int nparams,
                 uint32 seed);
```

開始執行取樣掃描。
此函式在第一次嘗試擷取 tuple 之前呼叫；若掃描需要重新開始，則可能會再次呼叫。
要掃描之資料表的相關資訊，可以透過 `SampleScanState` 節點的欄位取得（但請注意，
`node->ss.ss_currentScanDesc` 掃描描述子尚未設定）。
長度為 `nparams` 的 `params` 陣列，包含 `TABLESAMPLE` 子句中所提供之參數的值。
這些參數的數量與型別會符合取樣方法的 `parameterTypes` 清單所指定的內容，而且已經檢查過不為 null。
`seed` 包含一個種子，供取樣方法內產生任何亂數時使用；若有提供
`REPEATABLE` 值，它是由該值衍生的雜湊值，否則是
`random()` 的結果。

此函式可以調整 `node->use_bulkread`
與 `node->use_pagemode` 欄位。
若 `node->use_bulkread` 為 `true`（這是預設值），
掃描會使用一種鼓勵在使用後回收緩衝區的緩衝區存取策略。如果掃描只會造訪資料表頁面中的一小部分，將它設為 `false` 可能是合理的。
若 `node->use_pagemode` 為 `true`（這是預設值），
掃描會在單一遍歷中，對每個造訪頁面上的所有 tuple 執行可見性檢查。如果掃描只會選取每個造訪頁面上一小部分的 tuple，將它設為 `false` 可能是合理的。這樣執行的 tuple 可見性檢查次數會較少，不過每一次檢查的成本會較高，因為需要更多的鎖定。

如果取樣方法標記為 `repeatable_across_scans`，它必須能在重新掃描時選取與原本相同的 tuple 集合，也就是說，重新呼叫 `BeginSampleScan` 必須導致選取與先前相同的 tuple（前提是 `TABLESAMPLE` 參數與種子沒有改變）。

```

BlockNumber
NextSampleBlock (SampleScanState *node, BlockNumber nblocks);
```

傳回下一個要掃描之頁面的區塊編號；若沒有剩餘要掃描的頁面，則傳回
`InvalidBlockNumber`。

此函式可以省略（將指標設為 NULL），此時核心程式碼會對整個關聯執行循序掃描。
這種掃描可能使用同步掃描，因此取樣方法不能假設每次掃描造訪關聯頁面的順序都相同。

```

OffsetNumber
NextSampleTuple (SampleScanState *node,
                 BlockNumber blockno,
                 OffsetNumber maxoffset);
```

傳回指定頁面上下一個要取樣之 tuple 的位移編號；若沒有剩餘要取樣的 tuple，則傳回 `InvalidOffsetNumber`。`maxoffset` 是該頁面上使用中的最大位移編號。

### 注意

`NextSampleTuple` 不會被明確告知範圍 `1 .. maxoffset` 中的哪些位移編號實際包含有效的 tuple。這通常不成問題，因為核心程式碼會忽略對不存在或不可見 tuple 的取樣請求；這不應該使樣本產生任何偏差。不過，如有必要，此函式可以使用
`node->donetuples` 檢查它所傳回的 tuple 中有多少是有效且可見的。

### 注意

`NextSampleTuple` *不可*假設
`blockno` 就是最近一次 `NextSampleBlock` 呼叫所傳回的頁面編號。它是由先前某一次 `NextSampleBlock` 呼叫所傳回的，但核心程式碼可以在實際掃描頁面之前預先呼叫 `NextSampleBlock`，以支援預先擷取。可以假設的是：一旦開始對某個頁面取樣，在傳回 `InvalidOffsetNumber` 之前，連續的 `NextSampleTuple`
呼叫都會指向同一個頁面。

```

void
EndSampleScan (SampleScanState *node);
```

結束掃描並釋放資源。釋放以 palloc 配置的記憶體通常並不重要，但任何外部可見的資源都應該清理。
在不存在這類資源的常見情況下，此函式可以省略（將指標設為 NULL）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tablesample-support-functions.html)（原文版本：18.6；核對日期：2026-10-12）
