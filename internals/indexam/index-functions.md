<a id="INDEX-FUNCTIONS"></a>

## 63.2. 索引存取方法函式 [#](#INDEX-FUNCTIONS)

索引存取方法必須在 `IndexAmRoutine` 中提供的索引建構與維護函式如下：

```

IndexBuildResult *
ambuild (Relation heapRelation,
         Relation indexRelation,
         IndexInfo *indexInfo);
```

建立新的索引。索引關聯已經以實體方式建立，但仍是空的。它必須填入存取方法所需的任何固定資料，以及資料表中所有既有元組（tuple）的項目。通常 `ambuild` 函式會呼叫 `table_index_build_scan()` 來掃描資料表中既有的元組，並計算需要插入索引的鍵。此函式必須傳回一個以 palloc 配置的結構，其中包含新索引的統計資訊。`amcanbuildparallel` 旗標表示該存取方法是否支援平行建立索引。設為 `true` 時，系統會嘗試為建立作業配置平行工作程序。只支援非平行建立索引的存取方法，應將此旗標保持設為 `false`。

```

void
ambuildempty (Relation indexRelation);
```

建立一個空的索引，並將它寫入給定關聯的初始化分支（init fork，`INIT_FORKNUM`）。此方法只會針對無日誌（unlogged）索引呼叫；寫入初始化分支的空索引，會在每次伺服器重新啟動時複製並覆蓋主要關聯分支。

```

bool
aminsert (Relation indexRelation,
          Datum *values,
          bool *isnull,
          ItemPointer heap_tid,
          Relation heapRelation,
          IndexUniqueCheck checkUnique,
          bool indexUnchanged,
          IndexInfo *indexInfo);
```

將新的元組插入既有的索引。`values` 與 `isnull` 陣列提供要建立索引的鍵值，而 `heap_tid` 是要建立索引的 TID。若存取方法支援唯一值索引（其 `amcanunique` 旗標為 true），則 `checkUnique` 表示要執行的唯一性檢查類型。這會依唯一性限制條件是否可延遲而有所不同；詳情請參閱[第 63.5 節](index-unique-checks.md)。通常存取方法只有在執行唯一性檢查時才需要 `heapRelation` 參數（因為此時它必須查看堆積以確認元組的存活狀態）。

`indexUnchanged` 布林值提供關於要建立索引之元組性質的提示。當它為 true 時，該元組是索引中某個既有元組的重複項。新元組是邏輯上未變更的後繼 MVCC 元組版本。當執行的 `UPDATE` 沒有修改索引所涵蓋的任何欄位，但仍需要在索引中建立新版本時，就會發生這種情況。索引 AM 可以利用這個提示，決定在索引中同一邏輯資料列累積了許多版本的部分，套用由下而上索引刪除（bottom-up index deletion）。請注意，更新非鍵欄位，或只出現在部分索引述詞中的欄位，並不會影響 `indexUnchanged` 的值。核心程式碼使用一種低負擔的方法來決定每個元組的 `indexUnchanged` 值，這種方法同時允許偽陽性與偽陰性。索引 AM 不得將 `indexUnchanged` 視為關於元組可見性或版本的權威資訊來源。

此函式的布林結果值只有在 `checkUnique` 為 `UNIQUE_CHECK_PARTIAL` 時才有意義。在這種情況下，結果為 true 表示已知新項目是唯一的，而 false 表示它可能不是唯一的（因此必須排程一次延遲的唯一性檢查）。在其他情況下，建議一律傳回常數結果 false。

有些索引可能不會為所有元組建立索引。若元組不需要建立索引，`aminsert` 應該直接返回，不做任何事。

如果索引 AM 希望在一個 SQL 陳述式內的連續索引插入之間快取資料，它可以在 `indexInfo->ii_Context` 中配置空間，並將指向該資料的指標存放在 `indexInfo->ii_AmCache` 中（其初始值為 NULL）。若在索引插入之後，除了記憶體之外還有其他資源需要釋放，可以提供 `aminsertcleanup`，它會在記憶體釋放之前被呼叫。

```

void
aminsertcleanup (Relation indexRelation,
                 IndexInfo *indexInfo);
```

清理在 `indexInfo->ii_AmCache` 中跨連續插入所維護的狀態。當資料需要額外的清理步驟（例如釋放已釘住（pinned）的緩衝區），而只釋放記憶體並不足夠時，這就很有用。

```

IndexBulkDeleteResult *
ambulkdelete (IndexVacuumInfo *info,
              IndexBulkDeleteResult *stats,
              IndexBulkDeleteCallback callback,
              void *callback_state);
```

從索引中刪除元組。這是一種「批次刪除」操作，預期的實作方式是掃描整個索引，並檢查每個項目以判斷是否應該刪除它。必須以 `callback(TID, callback_state) returns bool` 的形式呼叫傳入的 `callback` 函式，以判斷某個特定的索引項目（以其參照的 TID 識別）是否要刪除。必須傳回 NULL，或傳回一個以 palloc 配置、包含刪除操作效果之統計資訊的結構。若不需要將任何資訊傳遞給 `amvacuumcleanup`，傳回 NULL 是可以的。

由於 `maintenance_work_mem` 有限，當有許多元組要刪除時，`ambulkdelete` 可能需要被呼叫超過一次。`stats` 引數是先前對此索引呼叫的結果（在一次 `VACUUM` 操作中的第一次呼叫時為 NULL）。這讓 AM 能夠在整個操作期間累積統計資訊。通常，如果傳入的 `stats` 不是 null，`ambulkdelete` 會修改並傳回同一個結構。

```

IndexBulkDeleteResult *
amvacuumcleanup (IndexVacuumInfo *info,
                 IndexBulkDeleteResult *stats);
```

在 `VACUUM` 操作（零次或多次 `ambulkdelete` 呼叫）之後進行清理。除了傳回索引統計資訊之外，它不必做任何事，但它可能會執行批次清理，例如回收空的索引頁面。`stats` 是最後一次 `ambulkdelete` 呼叫所傳回的內容；若因為沒有元組需要刪除而未呼叫 `ambulkdelete`，則為 NULL。若結果不是 NULL，它必須是以 palloc 配置的結構。其中包含的統計資訊會用來更新 `pg_class`，而且在指定 `VERBOSE` 時會由 `VACUUM` 回報。若在 `VACUUM` 操作期間索引完全沒有變更，傳回 NULL 是可以的，否則應該傳回正確的統計資訊。

`amvacuumcleanup` 也會在 `ANALYZE` 操作完成時被呼叫。在這種情況下，`stats` 一律為 NULL，且任何傳回值都會被忽略。可以藉由檢查 `info->analyze_only` 來區分這種情況。建議存取方法在這種呼叫中，除了插入後的清理之外什麼都不做，而且只在 autovacuum 工作程序中才這樣做。

```

bool
amcanreturn (Relation indexRelation, int attno);
```

檢查索引是否能藉由傳回欄位原始的索引值，在給定欄位上支援[*僅索引掃描*](../../the-sql-language/indexes/indexes-index-only-scans.md)。屬性編號從 1 開始，也就是第一個欄位的 attno 為 1。若支援則傳回 true，否則傳回 false。對於內含（included）欄位（若有支援的話），此函式應該一律傳回 true，因為無法擷取的內含欄位幾乎沒有意義。若存取方法完全不支援僅索引掃描，可以將其 `IndexAmRoutine` 結構中的 `amcanreturn` 欄位設為 NULL。

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

估計索引掃描的成本。此函式在下文的[第 63.6 節](index-cost-estimation.md)中有完整說明。

```

int
amgettreeheight (Relation rel);
```

計算樹狀索引的高度。此資訊會透過 `path->indexinfo->tree_height` 提供給 `amcostestimate` 函式，可用來支援成本估算。這個結果不會用在其他任何地方，因此這個函式實際上可以用來計算成本估算函式可能想知道的、關於該索引的任何種類資料（只要能放進一個整數）。若計算的代價很高，將結果快取為 `RelationData.rd_amcache` 的一部分可能會有幫助。

```

bytea *
amoptions (ArrayType *reloptions,
           bool validate);
```

剖析並驗證索引的 reloptions 陣列。只有在該索引存在非 null 的 reloptions 陣列時才會呼叫此函式。
*`reloptions`* 是一個 `text` 陣列，其中的項目格式為 *`name`*`=`*`value`*。
此函式應該建構一個 `bytea` 值，該值會被複製到索引之 relcache 項目的 `rd_options` 欄位中。`bytea` 值的資料內容由存取方法自行定義；大多數標準存取方法使用 `StdRdOptions` 結構。當 *`validate`* 為 true 時，若有任何選項無法辨識或具有無效的值，此函式應該回報適當的錯誤訊息；當 *`validate`* 為 false 時，應該默默忽略無效的項目。（載入已儲存在 `pg_catalog` 中的選項時，*`validate`* 為 false；只有在存取方法變更了其選項規則時，才可能發現無效的項目，而在這種情況下，忽略過時的項目是恰當的。）若想要預設行為，傳回 NULL 是可以的。

```

bool
amproperty (Oid index_oid, int attno,
            IndexAMProperty prop, const char *propname,
            bool *res, bool *isnull);
```

`amproperty` 方法讓索引存取方法可以覆寫 `pg_index_column_has_property` 及相關函式的預設行為。若存取方法對索引屬性查詢沒有任何特殊行為，可以將其 `IndexAmRoutine` 結構中的 `amproperty` 欄位設為 NULL。否則，對於 `pg_indexam_has_property` 呼叫，呼叫 `amproperty` 方法時 *`index_oid`* 與 *`attno`* 都為零；對於 `pg_index_has_property` 呼叫，*`index_oid`* 有效而 *`attno`* 為零；對於 `pg_index_column_has_property` 呼叫，*`index_oid`* 有效且 *`attno`* 大於零。*`prop`* 是識別要測試之屬性的列舉值，而 *`propname`* 是原始的屬性名稱字串。若核心程式碼無法辨識該屬性名稱，則 *`prop`* 為 `AMPROP_UNKNOWN`。存取方法可以藉由檢查 *`propname`* 是否相符來定義自訂的屬性名稱（為了與核心程式碼一致，請使用 `pg_strcasecmp` 來比對）；對於核心程式碼已知的名稱，最好檢查 *`prop`*。若 `amproperty` 方法傳回 `true`，表示它已決定屬性測試的結果：它必須將 `*res` 設為要傳回的布林值，或將 `*isnull` 設為 `true` 以傳回 NULL。（這兩個被參照的變數在呼叫前都會初始化為 `false`。）若 `amproperty` 方法傳回 `false`，核心程式碼會以其一般邏輯繼續決定屬性測試的結果。

支援排序運算子的存取方法應該實作 `AMPROP_DISTANCE_ORDERABLE` 屬性測試，因為核心程式碼不知道如何進行這項測試，會傳回 NULL。如果實作 `AMPROP_RETURNABLE` 測試的成本，可以比開啟索引並呼叫 `amcanreturn`（這是核心程式碼的預設行為）更低，那麼實作它也可能有好處。對於所有其他標準屬性，預設行為應該就令人滿意。

```

char *
ambuildphasename (int64 phasenum);
```

傳回給定建立階段編號的文字名稱。階段編號是在建立索引期間透過 `pgstat_progress_update_param` 介面回報的編號。接著，階段名稱會呈現在 `pg_stat_progress_create_index` 檢視表中。

```

bool
amvalidate (Oid opclassoid);
```

在存取方法能合理做到的範圍內，驗證指定運算子類別的目錄項目。例如，這可能包括測試是否已提供所有必要的支援函式。若運算子類別無效，`amvalidate` 函式必須傳回 false。問題應該以 `ereport` 訊息回報，通常是 `INFO` 等級。

```

void
amadjustmembers (Oid opfamilyoid,
                 Oid opclassoid,
                 List *operators,
                 List *functions);
```

在存取方法能合理做到的範圍內，驗證運算子家族中提議新增的運算子與函式成員，並在預設的相依類型不令人滿意時設定它們的相依類型。此函式會在 `CREATE OPERATOR CLASS` 期間以及 `ALTER OPERATOR FAMILY ADD` 期間被呼叫；在後者的情況下，*`opclassoid`* 為 `InvalidOid`。`List` 引數是 `OpFamilyMember` 結構的清單，定義於 `amapi.h` 中。此函式所做的測試通常是 `amvalidate` 所做測試的子集，因為 `amadjustmembers` 不能假設它看到的是完整的成員集合。例如，檢查支援函式的簽章是合理的，但檢查是否已提供所有必要的支援函式則不合理。任何問題都可以藉由擲出錯誤來回報。如果這是 `CREATE OPERATOR CLASS`，核心程式碼會將 `OpFamilyMember` 結構中與相依性相關的欄位初始化為對運算子類別的硬相依；如果這是 `ALTER OPERATOR FAMILY ADD`，則初始化為對運算子家族的軟相依。如果其他行為較為適當，`amadjustmembers` 可以調整這些欄位。例如，GIN、GiST 與 SP-GiST 一律將運算子成員設為對運算子家族的軟相依，因為在這些索引類型中，運算子與運算子類別之間的關聯相對薄弱；因此允許自由新增與移除運算子成員是合理的。選用的支援函式通常也會被設為軟相依，以便在必要時可以移除它們。

當然，索引的目的是支援掃描符合可索引之 `WHERE` 條件式的元組，這種條件式通常稱為*條件*（qualifier）或*掃描鍵*（scan key）。索引掃描的語意在下文的[第 63.3 節](index-scanning.md)中有更完整的說明。索引存取方法可以支援「一般」索引掃描、「點陣圖」（bitmap）索引掃描，或兩者都支援。索引存取方法必須或可以提供的掃描相關函式如下：

```

IndexScanDesc
ambeginscan (Relation indexRelation,
             int nkeys,
             int norderbys);
```

準備進行索引掃描。`nkeys` 與 `norderbys` 參數指出掃描中將使用的條件（quals）與排序運算子的數量；這些數字可能有助於配置空間。請注意，掃描鍵的實際值尚未提供。結果必須是以 palloc 配置的結構。基於實作上的原因，索引存取方法*必須*藉由呼叫 `RelationGetIndexScan()` 來建立此結構。在大多數情況下，`ambeginscan` 除了進行該呼叫、或許再取得鎖定之外，幾乎不做其他事；索引掃描啟動中值得注意的部分都在 `amrescan` 裡。

```

void
amrescan (IndexScanDesc scan,
          ScanKey keys,
          int nkeys,
          ScanKey orderbys,
          int norderbys);
```

開始或重新開始索引掃描，可能使用新的掃描鍵。（若要使用先前傳入的鍵重新開始，會對 `keys` 和／或 `orderbys` 傳入 NULL。）請注意，鍵或 ORDER BY 運算子的數量不允許大於傳給 `ambeginscan` 的數量。實務上，重新開始的功能用於巢狀迴圈連接選取了新的外側元組、因而需要新的鍵比較值，但掃描鍵結構保持不變的情況。

```

bool
amgettuple (IndexScanDesc scan,
            ScanDirection direction);
```

擷取給定掃描中的下一個元組，並依給定方向（在索引中向前或向後）移動。若取得元組則傳回 true，若已沒有符合的元組則傳回 false。在 true 的情況下，元組的 TID 會存放在 `scan` 結構中。請注意，「成功」只表示索引包含符合掃描鍵的項目，並不表示該元組一定仍存在於堆積中，也不表示它一定會通過呼叫者的快照測試。成功時，`amgettuple` 還必須將 `scan->xs_recheck` 設為 true 或 false。false 表示確定該索引項目符合掃描鍵。true 表示這並不確定，在擷取堆積元組之後，必須對它重新檢查掃描鍵所代表的條件。這項機制用來支援「有損」（lossy）的索引運算子。請注意，重新檢查只會涵蓋掃描條件；`amgettuple` 的呼叫者永遠不會重新檢查部分索引述詞（若有的話）。

若索引支援[僅索引掃描](../../the-sql-language/indexes/indexes-index-only-scans.md)（也就是 `amcanreturn` 對其任一欄位傳回 true），則成功時 AM 還必須檢查 `scan->xs_want_itup`，若其為 true，就必須傳回該索引項目原始的索引資料。`amcanreturn` 傳回 false 的欄位可以傳回 null。資料可以用存放在 `scan->xs_itup` 的 `IndexTuple` 指標形式傳回，搭配元組描述子 `scan->xs_itupdesc`；或以存放在 `scan->xs_hitup` 的 `HeapTuple` 指標形式傳回，搭配元組描述子 `scan->xs_hitupdesc`。（重建的資料若可能無法放入 `IndexTuple`，應使用後者的格式。）無論哪種情況，管理該指標所參照的資料都是存取方法的責任。這些資料必須至少保持有效，直到對該掃描進行下一次 `amgettuple`、`amrescan` 或 `amendscan` 呼叫為止。

只有在存取方法支援「一般」索引掃描時，才需要提供 `amgettuple` 函式。若不支援，其 `IndexAmRoutine` 結構中的 `amgettuple` 欄位必須設為 NULL。

```

int64
amgetbitmap (IndexScanDesc scan,
             TIDBitmap *tbm);
```

擷取給定掃描中的所有元組，並將它們加入呼叫者提供的 `TIDBitmap`（也就是將元組 ID 的集合以 OR 合併到點陣圖中已有的任何集合）。傳回值是擷取到的元組數量（這可能只是近似的計數，例如有些 AM 不會偵測重複項）。在將元組 ID 插入點陣圖時，`amgetbitmap` 可以指出特定元組 ID 需要重新檢查掃描條件。這類似於 `amgettuple` 的 `xs_recheck` 輸出參數。注意：在目前的實作中，對這項功能的支援與對點陣圖本身之有損儲存的支援混在一起，因此對於需要重新檢查的元組，呼叫者會同時重新檢查掃描條件與部分索引述詞（若有的話）。不過，情況未必永遠如此。`amgetbitmap` 與 `amgettuple` 不能在同一次索引掃描中使用；使用 `amgetbitmap` 時還有其他限制，如[第 63.3 節](index-scanning.md)所述。

只有在存取方法支援「點陣圖」索引掃描時，才需要提供 `amgetbitmap` 函式。若不支援，其 `IndexAmRoutine` 結構中的 `amgetbitmap` 欄位必須設為 NULL。

```

void
amendscan (IndexScanDesc scan);
```

結束掃描並釋放資源。不應釋放 `scan` 結構本身，但存取方法在內部取得的任何鎖定或釘住（pin）都必須釋放，由 `ambeginscan` 及其他掃描相關函式配置的任何其他記憶體也必須釋放。

```

void
ammarkpos (IndexScanDesc scan);
```

標記目前的掃描位置。存取方法只需要支援每次掃描記住一個掃描位置。

只有在存取方法支援有序掃描時，才需要提供 `ammarkpos` 函式。若不支援，可以將其 `IndexAmRoutine` 結構中的 `ammarkpos` 欄位設為 NULL。

```

void
amrestrpos (IndexScanDesc scan);
```

將掃描還原到最近一次標記的位置。

只有在存取方法支援有序掃描時，才需要提供 `amrestrpos` 函式。若不支援，可以將其 `IndexAmRoutine` 結構中的 `amrestrpos` 欄位設為 NULL。

除了支援一般的索引掃描之外，某些類型的索引可能希望支援*平行索引掃描*，讓多個後端合作執行一次索引掃描。索引存取方法應該妥善安排，讓每個合作的程序傳回一般非平行索引掃描會傳回之元組的一個子集（原文此處寫作 performed，依上下文應指傳回），而且這些子集的聯集要等於一般非平行索引掃描會傳回的元組集合。此外，雖然平行掃描傳回的元組不需要有任何全域順序，但在每個合作後端內傳回的那個元組子集，其順序必須符合所要求的順序。可以實作下列函式來支援平行索引掃描：

```

Size
amestimateparallelscan (Relation indexRelation,
                        int nkeys,
                        int norderbys);
```

估計並傳回存取方法執行平行掃描所需的動態共享記憶體位元組數。（這個數字是在 `ParallelIndexScanDescData` 中與 AM 無關之資料所需的空間之外額外增加的，而不是取代它。）

`nkeys` 與 `norderbys` 參數指出掃描中將使用的條件（quals）與排序運算子的數量；相同的值會傳給 `amrescan`。請注意，掃描鍵的實際值尚未提供。

對於不支援平行掃描的存取方法，或所需額外儲存空間位元組數為零的存取方法，不需要實作此函式。

```

void
aminitparallelscan (void *target);
```

此函式會在平行掃描開始時被呼叫，以初始化動態共享記憶體。*`target`* 會指向至少為先前 `amestimateparallelscan` 所傳回之位元組數的空間，而此函式可以使用這些空間存放它想要的任何資料。

對於不支援平行掃描的存取方法，或所需的共享記憶體空間不需要初始化的情況，不需要實作此函式。

```

void
amparallelrescan (IndexScanDesc scan);
```

此函式若有實作，會在平行索引掃描必須重新開始時被呼叫。它應該重設 `aminitparallelscan` 所建立的任何共享狀態，使掃描從頭重新開始。

```

CompareType
amtranslatestrategy (StrategyNumber strategy, Oid opfamily, Oid opcintype);

StrategyNumber
amtranslatecmptype (CompareType cmptype, Oid opfamily, Oid opcintype);
```

這些函式若有實作，會由規劃器與執行器呼叫，用來在固定的 `CompareType` 值與存取方法所使用的特定策略編號之間進行轉換。實作了類似內建 btree 或雜湊存取方法之功能的存取方法，可以實作這些函式；藉由實作這些轉換，系統就能了解該存取方法之操作的語意，並在多處用它們取代 btree 或雜湊索引。若存取方法的功能與這些內建存取方法不相似，就不需要實作這些函式。若未實作這些函式，在某些規劃器與執行器的決策中會忽略該存取方法，但除此之外它仍可完整運作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/index-functions.html)（原文版本：18.6；核對日期：2026-10-17）
