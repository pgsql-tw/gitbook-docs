<a id="FDW-CALLBACKS"></a>

## 58.2. 外部資料包裝器回呼函式 [#](#FDW-CALLBACKS)

[58.2.1. 掃描外部資料表的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-SCAN)

[58.2.2. 掃描外部資料表連接的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-JOIN-SCAN)

[58.2.3. 規劃掃描／連接後處理的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-UPPER-PLANNING)

[58.2.4. 更新外部資料表的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-UPDATE)

[58.2.5. `TRUNCATE` 的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-TRUNCATE)

[58.2.6. 資料列鎖定的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-ROW-LOCKING)

[58.2.7. `EXPLAIN` 的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-EXPLAIN)

[58.2.8. `ANALYZE` 的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-ANALYZE)

[58.2.9. `IMPORT FOREIGN SCHEMA` 的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-IMPORT)

[58.2.10. 平行執行的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-PARALLEL)

[58.2.11. 非同步執行的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-ASYNC)

[58.2.12. 路徑重新參數化的 FDW 函式](fdw-callbacks.md#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

FDW 處理函式會回傳一個以 palloc 配置的 `FdwRoutine` 結構，其中包含指向下文所述各回呼函式的指標。與掃描相關的函式是必要的，其餘則可選擇性提供。

`FdwRoutine` 結構型別宣告於 `src/include/foreign/fdwapi.h`，更多細節請參閱該檔案。

<a id="FDW-CALLBACKS-SCAN"></a>

### 58.2.1. 掃描外部資料表的 FDW 函式 [#](#FDW-CALLBACKS-SCAN)

```

void
GetForeignRelSize(PlannerInfo *root,
                  RelOptInfo *baserel,
                  Oid foreigntableid);
```

取得外部資料表的關聯大小估計值。這會在規劃掃描外部資料表的查詢之初被呼叫。`root` 是規劃器關於該查詢的全域資訊；`baserel` 是規劃器關於此資料表的資訊；`foreigntableid` 則是該外部資料表在 `pg_class` 中的 OID。（`foreigntableid` 其實可以從規劃器的資料結構中取得，但為了省事而明確傳入。）

此函式應該將 `baserel->rows` 更新為資料表掃描預期回傳的資料列數，並將限制性條件（restriction quals）所做的過濾納入考量。`baserel->rows` 的初始值只是一個固定的預設估計值，應該盡可能加以取代。若此函式能計算出更好的平均結果資料列寬度估計值，也可以選擇更新 `baserel->width`。（其初始值是根據欄位的資料型別，以及最近一次 `ANALYZE` 所量測的欄位平均寬度值。）此外，若此函式能計算出更好的外部資料表總資料列數估計值，也可以更新 `baserel->tuples`。（其初始值取自 `pg_class`.`reltuples`，代表最近一次 `ANALYZE` 所看到的總資料列數；若此外部資料表從未執行過 `ANALYZE`，則為 `-1`。）

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

```

void
GetForeignPaths(PlannerInfo *root,
                RelOptInfo *baserel,
                Oid foreigntableid);
```

為外部資料表上的掃描建立可能的存取路徑。這會在查詢規劃期間被呼叫。參數與 `GetForeignRelSize` 相同，而後者此時已被呼叫過。

此函式必須為外部資料表上的掃描產生至少一個存取路徑（`ForeignPath` 節點），並且必須呼叫 `add_path` 將每個這樣的路徑加入 `baserel->pathlist`。建議使用 `create_foreignscan_path` 來建構 `ForeignPath` 節點。此函式可以產生多個存取路徑，例如一個具有有效 `pathkeys` 的路徑，用以表示預先排序的結果。每個存取路徑都必須包含成本估計值，並且可以包含識別所要採用的特定掃描方法所需的任何 FDW 私有資訊。

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

```

ForeignScan *
GetForeignPlan(PlannerInfo *root,
               RelOptInfo *baserel,
               Oid foreigntableid,
               ForeignPath *best_path,
               List *tlist,
               List *scan_clauses,
               Plan *outer_plan);
```

從選定的外部存取路徑建立 `ForeignScan` 計畫節點。這會在查詢規劃的最後被呼叫。參數與 `GetForeignRelSize` 相同，另外加上：選定的 `ForeignPath`（先前由 `GetForeignPaths`、`GetForeignJoinPaths` 或 `GetForeignUpperPaths` 產生）、計畫節點要輸出的目標清單、計畫節點要強制套用的限制子句，以及 `ForeignScan` 的外層子計畫（用於 `RecheckForeignScan` 所執行的重新檢查）。（若該路徑是針對連接而非基礎關聯，則 `foreigntableid` 為 `InvalidOid`。）

此函式必須建立並回傳一個 `ForeignScan` 計畫節點；建議使用 `make_foreignscan` 來建構 `ForeignScan` 節點。

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

```

void
BeginForeignScan(ForeignScanState *node,
                 int eflags);
```

開始執行外部掃描。這會在執行器啟動期間被呼叫。它應該執行掃描開始前所需的任何初始化，但不要開始執行實際的掃描（那應該在第一次呼叫 `IterateForeignScan` 時進行）。`ForeignScanState` 節點已經建立，但其 `fdw_state` 欄位仍為 NULL。要掃描的資料表的相關資訊可以透過 `ForeignScanState` 節點取得（特別是從底層的 `ForeignScan` 計畫節點，其中包含 `GetForeignPlan` 所提供的任何 FDW 私有資訊）。`eflags` 包含描述執行器對此計畫節點之運作模式的旗標位元。

請注意，當 `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` 為真時，此函式不應執行任何外部可見的動作；它只應做到讓節點狀態對 `ExplainForeignScan` 與 `EndForeignScan` 有效所需的最低限度工作。

```

TupleTableSlot *
IterateForeignScan(ForeignScanState *node);
```

從外部來源擷取一個資料列，並以元組表槽（tuple table slot）回傳（應該使用節點的 `ScanTupleSlot` 來達成此目的）。若沒有更多資料列可用，則回傳 NULL。元組表槽基礎架構允許回傳實體元組或虛擬元組；在大多數情況下，從效能的角度來看後者較為理想。請注意，此函式是在一個短生命週期的記憶體上下文中被呼叫，該上下文會在每次呼叫之間重設。若需要生命週期較長的儲存空間，請在 `BeginForeignScan` 中建立一個記憶體上下文，或使用節點之 `EState` 的 `es_query_cxt`。

若有提供 `fdw_scan_tlist` 目標清單，回傳的資料列必須與其相符；否則必須與被掃描之外部資料表的資料列型別相符。若你選擇以最佳化省略擷取不需要的欄位，應該在那些欄位位置填入 null，或者產生一個省略那些欄位的 `fdw_scan_tlist` 清單。

請注意，PostgreSQL 的執行器並不在意回傳的資料列是否違反外部資料表上定義的任何限制條件——但規劃器在意，若外部資料表中有可見的資料列不符合已宣告的限制條件，規劃器可能會錯誤地最佳化查詢。若在使用者已宣告某限制條件應該成立的情況下該限制條件遭到違反，擲出錯誤可能是恰當的（就像在資料型別不相符時你需要做的一樣）。

```

void
ReScanForeignScan(ForeignScanState *node);
```

從頭重新開始掃描。請注意，掃描所依賴的任何參數的值都可能已經改變，因此新的掃描不一定會回傳完全相同的資料列。

```

void
EndForeignScan(ForeignScanState *node);
```

結束掃描並釋放資源。釋放以 palloc 配置的記憶體通常並不重要，但像是開啟的檔案以及與遠端伺服器的連線等，則應該加以清理。

<a id="FDW-CALLBACKS-JOIN-SCAN"></a>

### 58.2.2. 掃描外部資料表連接的 FDW 函式 [#](#FDW-CALLBACKS-JOIN-SCAN)

若 FDW 支援在遠端執行外部資料表之間的連接（而不是擷取兩個資料表的資料後在本地端進行連接），它應該提供這個回呼函式：

```

void
GetForeignJoinPaths(PlannerInfo *root,
                    RelOptInfo *joinrel,
                    RelOptInfo *outerrel,
                    RelOptInfo *innerrel,
                    JoinType jointype,
                    JoinPathExtraData *extra);
```

為兩個（或更多）全都屬於同一外部伺服器的外部資料表之連接，建立可能的存取路徑。這個選擇性函式會在查詢規劃期間被呼叫。與 `GetForeignPaths` 一樣，此函式應該為所提供的 `joinrel` 產生 `ForeignPath` 路徑（使用 `create_foreign_join_path` 來建構），並呼叫 `add_path` 將這些路徑加入此連接所考慮的路徑集合。但與 `GetForeignPaths` 不同的是，此函式不一定要成功建立至少一個路徑，因為涉及本地端連接的路徑總是可行的。

請注意，對於同一個連接關聯，此函式會以不同的內層與外層關聯組合被重複呼叫；將重複工作減到最少是 FDW 的責任。

另請注意，要套用於該連接的連接子句集合（以 `extra->restrictlist` 傳入）會依內層與外層關聯的組合而不同。為 `joinrel` 產生的 `ForeignPath` 路徑必須包含它所使用的連接子句集合；若規劃器選擇該路徑作為 `joinrel` 的最佳路徑，規劃器會用這些子句將該 `ForeignPath` 路徑轉換為計畫。

若某個連接選擇了 `ForeignPath` 路徑，它將代表整個連接處理過程；為組成資料表及附屬連接所產生的路徑將不會被使用。此連接路徑的後續處理，大致與掃描單一外部資料表之路徑的處理相同。差異之一是，所產生的 `ForeignScan` 計畫節點的 `scanrelid` 應該設為零，因為它並不代表單一關聯；取而代之的是，`ForeignScan` 節點的 `fs_relids` 欄位代表被連接的關聯集合。（後者欄位由核心規劃器程式碼自動設定，FDW 不需要填寫。）另一個差異是，由於遠端連接的欄位清單無法從系統目錄中找到，FDW 必須在 `fdw_scan_tlist` 中填入適當的 `TargetEntry` 節點清單，代表它在執行時期所回傳的元組中會提供的欄位集合。

### 注意

從 PostgreSQL 16 開始，若此連接涉及外部連接（outer join），`fs_relids` 會包含這些外部連接的範圍表（rangetable）索引。新的欄位 `fs_base_relids` 只包含基礎關聯的索引，因此模擬了 `fs_relids` 原本的語意。

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

<a id="FDW-CALLBACKS-UPPER-PLANNING"></a>

### 58.2.3. 規劃掃描／連接後處理的 FDW 函式 [#](#FDW-CALLBACKS-UPPER-PLANNING)

若 FDW 支援在遠端執行掃描／連接後的處理（例如遠端彙總），它應該提供這個回呼函式：

```

void
GetForeignUpperPaths(PlannerInfo *root,
                     UpperRelationKind stage,
                     RelOptInfo *input_rel,
                     RelOptInfo *output_rel,
                     void *extra);
```

為*上層關聯*（upper relation）處理建立可能的存取路徑；上層關聯是規劃器用來指稱所有掃描／連接後查詢處理的術語，例如彙總、視窗函式、排序以及資料表更新。這個選擇性函式會在查詢規劃期間被呼叫。目前，只有在查詢所涉及的所有基礎關聯都屬於同一個 FDW 時才會呼叫它。此函式應該為 FDW 知道如何在遠端執行的任何掃描／連接後處理產生 `ForeignPath` 路徑（使用 `create_foreign_upper_path` 來建構），並呼叫 `add_path` 將這些路徑加入指定的上層關聯。與 `GetForeignJoinPaths` 一樣，此函式不一定要成功建立任何路徑，因為涉及本地端處理的路徑總是可行的。

`stage` 參數指出目前正在考慮的是哪一個掃描／連接後步驟。`output_rel` 是應該接收代表此步驟計算之路徑的上層關聯，而 `input_rel` 是代表此步驟輸入的關聯。`extra` 參數提供額外的細節；目前它只會在 `UPPERREL_PARTIAL_GROUP_AGG` 或 `UPPERREL_GROUP_AGG` 時設定，此時它指向一個 `GroupPathExtraData` 結構；或在 `UPPERREL_FINAL` 時設定，此時它指向一個 `FinalPathExtraData` 結構。（請注意，加入 `output_rel` 的 `ForeignPath` 路徑通常不會直接相依於 `input_rel` 的路徑，因為它們的處理預期會在外部完成。不過，檢視先前為前一個處理步驟所產生的路徑，有助於避免重複的規劃工作。）

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

<a id="FDW-CALLBACKS-UPDATE"></a>

### 58.2.4. 更新外部資料表的 FDW 函式 [#](#FDW-CALLBACKS-UPDATE)

若 FDW 支援可寫入的外部資料表，它應該依 FDW 的需求與能力，提供下列部分或全部的回呼函式：

```

void
AddForeignUpdateTargets(PlannerInfo *root,
                        Index rtindex,
                        RangeTblEntry *target_rte,
                        Relation target_relation);
```

`UPDATE` 與 `DELETE` 操作是針對先前由資料表掃描函式所擷取的資料列執行的。FDW 可能需要額外的資訊（例如資料列 ID 或主鍵欄位的值），以確保它能識別出要更新或刪除的確切資料列。為了支援這一點，此函式可以在 `UPDATE` 或 `DELETE` 期間要從外部資料表取回的欄位清單中，加入額外的隱藏（或稱「垃圾」（junk））目標欄位。

做法是建構一個代表你所需額外值的 `Var`，並將它連同垃圾欄位的名稱一起傳給 `add_row_identity_var`。（若需要多個欄位，可以這樣做超過一次。）你所需要的每個不同的 `Var` 都必須選用不同的垃圾欄位名稱，但除了 `varno` 欄位之外完全相同的那些 `Var` 可以、也應該共用同一個欄位名稱。核心系統使用的垃圾欄位名稱如下：資料表的 `tableoid` 欄位使用 `tableoid`；`ctid` 使用 `ctid` 或 `ctidN`；標記為 `vartype` = `RECORD` 的整列 `Var` 使用 `wholerow`；`vartype` 等於資料表所宣告之資料列型別的整列 `Var` 則使用 `wholerowN`。可以的話請重複使用這些名稱（規劃器會合併對相同垃圾欄位的重複請求）。若除此之外還需要其他種類的垃圾欄位，明智的做法可能是選用以你的擴充功能名稱為前綴的名稱，以避免與其他 FDW 衝突。

若 `AddForeignUpdateTargets` 指標設為 `NULL`，則不會加入任何額外的目標運算式。（這會使 `DELETE` 操作無法實作；不過若 FDW 依賴不會變動的主鍵來識別資料列，`UPDATE` 仍可能可行。）

```

List *
PlanForeignModify(PlannerInfo *root,
                  ModifyTable *plan,
                  Index resultRelation,
                  int subplan_index);
```

執行外部資料表上的插入、更新或刪除所需的任何額外規劃動作。此函式會產生 FDW 私有資訊，這些資訊將附加到執行更新動作的 `ModifyTable` 計畫節點上。此私有資訊必須採用 `List` 的形式，並會在執行階段傳遞給 `BeginForeignModify`。

`root` 是規劃器關於該查詢的全域資訊。`plan` 是 `ModifyTable` 計畫節點，除了 `fdwPrivLists` 欄位之外均已完整。`resultRelation` 以範圍表（range table）索引識別目標外部資料表。`subplan_index` 從零開始計數，指出這是 `ModifyTable` 計畫節點的哪一個目標；若你想要索引 `plan` 節點中各目標關聯專屬的子結構，請使用它。

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

若 `PlanForeignModify` 指標設為 `NULL`，則不會執行任何額外的規劃時期動作，而傳遞給 `BeginForeignModify` 的 `fdw_private` 清單將會是 NIL。

```

void
BeginForeignModify(ModifyTableState *mtstate,
                   ResultRelInfo *rinfo,
                   List *fdw_private,
                   int subplan_index,
                   int eflags);
```

開始執行外部資料表的修改操作。此函式會在執行器啟動期間被呼叫。它應該執行實際修改資料表之前所需的任何初始化。之後，對於要插入、更新或刪除的元組，會呼叫 `ExecForeignInsert/ExecForeignBatchInsert`、`ExecForeignUpdate` 或 `ExecForeignDelete`。

`mtstate` 是正在執行的 `ModifyTable` 計畫節點的整體狀態；關於計畫與執行狀態的全域資料可以透過此結構取得。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。（`ResultRelInfo` 的 `ri_FdwState` 欄位可供 FDW 存放此操作所需的任何私有狀態。）`fdw_private` 包含 `PlanForeignModify` 所產生的私有資料（若有的話）。`subplan_index` 指出這是 `ModifyTable` 計畫節點的哪一個目標。`eflags` 包含描述執行器對此計畫節點之運作模式的旗標位元。

請注意，當 `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` 為真時，此函式不應執行任何外部可見的動作；它只應做到讓節點狀態對 `ExplainForeignModify` 與 `EndForeignModify` 有效所需的最低限度工作。

若 `BeginForeignModify` 指標設為 `NULL`，則在執行器啟動期間不會執行任何動作。

```

TupleTableSlot *
ExecForeignInsert(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

將一個元組插入外部資料表。`estate` 是該查詢的全域執行狀態。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。`slot` 包含要插入的元組；它會符合外部資料表的資料列型別定義。`planSlot` 包含由 `ModifyTable` 計畫節點的子計畫所產生的元組；它與 `slot` 的差別在於可能包含額外的「垃圾」欄位。（對於 `INSERT` 的情況，`planSlot` 通常沒有太大用處，但為了完整起見仍會提供。）

回傳值是一個包含實際插入之資料的槽（這可能與所提供的資料不同，例如因觸發程序動作的結果），或者在實際上沒有插入任何資料列時回傳 NULL（同樣地，通常是觸發程序造成的結果）。傳入的 `slot` 可以重複用於此目的。

只有在 `INSERT` 陳述式具有 `RETURNING` 子句、或涉及帶有 `WITH CHECK OPTION` 的檢視表，或者外部資料表具有 `AFTER ROW` 觸發程序時，才會使用回傳之槽中的資料。觸發程序需要所有欄位，但 FDW 可以依 `RETURNING` 子句或 `WITH CHECK OPTION` 限制條件的內容，選擇以最佳化省略回傳部分或全部欄位。無論如何，都必須回傳某個槽以表示成功，否則查詢所回報的資料列數將會錯誤。

若 `ExecForeignInsert` 指標設為 `NULL`，嘗試插入外部資料表時將會失敗並產生錯誤訊息。

請注意，在將路由過來的元組插入外部資料表分割區，或對外部資料表執行 `COPY FROM` 時，也會呼叫此函式，此時它的呼叫方式與 `INSERT` 的情況不同。請參閱下文所述、讓 FDW 能夠支援這些情況的回呼函式。

```

TupleTableSlot **
ExecForeignBatchInsert(EState *estate,
                       ResultRelInfo *rinfo,
                       TupleTableSlot **slots,
                       TupleTableSlot **planSlots,
                       int *numSlots);
```

將多個元組批次插入外部資料表。參數與 `ExecForeignInsert` 相同，差別在於 `slots` 與 `planSlots` 包含多個元組，而 `*numSlots` 指定這些陣列中的元組數量。

回傳值是一個槽陣列，包含實際插入的資料（這可能與所提供的資料不同，例如因觸發程序動作的結果）。傳入的 `slots` 可以重複用於此目的。成功插入的元組數量會透過 `*numSlots` 回傳。

只有在 `INSERT` 陳述式涉及帶有 `WITH CHECK OPTION` 的檢視表，或者外部資料表具有 `AFTER ROW` 觸發程序時，才會使用回傳之槽中的資料。觸發程序需要所有欄位，但 FDW 可以依 `WITH CHECK OPTION` 限制條件的內容，選擇以最佳化省略回傳部分或全部欄位。

若 `ExecForeignBatchInsert` 或 `GetForeignModifyBatchSize` 指標設為 `NULL`，嘗試插入外部資料表時將會使用 `ExecForeignInsert`。若 `INSERT` 帶有 `RETURNING` 子句，則不會使用此函式。

請注意，在將路由過來的元組插入外部資料表分割區，或對外部資料表執行 `COPY FROM` 時，也會呼叫此函式，此時它的呼叫方式與 `INSERT` 的情況不同。請參閱下文所述、讓 FDW 能夠支援這些情況的回呼函式。

```

int
GetForeignModifyBatchSize(ResultRelInfo *rinfo);
```

回報對於指定的外部資料表，單次 `ExecForeignBatchInsert` 呼叫所能處理的最大元組數量。執行器傳給 `ExecForeignBatchInsert` 的元組數量最多就是這個數量。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。FDW 預期會提供外部伺服器選項及（或）外部資料表選項讓使用者設定此值，或者使用某個寫死的值。

若 `ExecForeignBatchInsert` 或 `GetForeignModifyBatchSize` 指標設為 `NULL`，嘗試插入外部資料表時將會使用 `ExecForeignInsert`。

```

TupleTableSlot *
ExecForeignUpdate(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

更新外部資料表中的一個元組。`estate` 是該查詢的全域執行狀態。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。`slot` 包含該元組的新資料；它會符合外部資料表的資料列型別定義。`planSlot` 包含由 `ModifyTable` 計畫節點的子計畫所產生的元組。與 `slot` 不同，此元組只包含被查詢變更之欄位的新值，因此不要依賴外部資料表的屬性編號來索引 `planSlot`。此外，`planSlot` 通常包含額外的「垃圾」欄位。特別是，`AddForeignUpdateTargets` 所請求的任何垃圾欄位都可以從此槽取得。

回傳值是一個包含實際更新後之資料列的槽（這可能與所提供的資料不同，例如因觸發程序動作的結果），或者在實際上沒有更新任何資料列時回傳 NULL（同樣地，通常是觸發程序造成的結果）。傳入的 `slot` 可以重複用於此目的。

只有在 `UPDATE` 陳述式具有 `RETURNING` 子句、或涉及帶有 `WITH CHECK OPTION` 的檢視表，或者外部資料表具有 `AFTER ROW` 觸發程序時，才會使用回傳之槽中的資料。觸發程序需要所有欄位，但 FDW 可以依 `RETURNING` 子句或 `WITH CHECK OPTION` 限制條件的內容，選擇以最佳化省略回傳部分或全部欄位。無論如何，都必須回傳某個槽以表示成功，否則查詢所回報的資料列數將會錯誤。

若 `ExecForeignUpdate` 指標設為 `NULL`，嘗試更新外部資料表時將會失敗並產生錯誤訊息。

```

TupleTableSlot *
ExecForeignDelete(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

從外部資料表刪除一個元組。`estate` 是該查詢的全域執行狀態。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。`slot` 在呼叫時不包含任何有用的內容，但可以用來存放要回傳的元組。`planSlot` 包含由 `ModifyTable` 計畫節點的子計畫所產生的元組；特別是，它會帶有 `AddForeignUpdateTargets` 所請求的任何垃圾欄位。必須使用這些垃圾欄位來識別要刪除的元組。

回傳值是一個包含被刪除之資料列的槽，或者在沒有刪除任何資料列時回傳 NULL（通常是觸發程序造成的結果）。傳入的 `slot` 可以用來存放要回傳的元組。

只有在 `DELETE` 查詢具有 `RETURNING` 子句，或者外部資料表具有 `AFTER ROW` 觸發程序時，才會使用回傳之槽中的資料。觸發程序需要所有欄位，但 FDW 可以依 `RETURNING` 子句的內容，選擇以最佳化省略回傳部分或全部欄位。無論如何，都必須回傳某個槽以表示成功，否則查詢所回報的資料列數將會錯誤。

若 `ExecForeignDelete` 指標設為 `NULL`，嘗試從外部資料表刪除時將會失敗並產生錯誤訊息。

```

void
EndForeignModify(EState *estate,
                 ResultRelInfo *rinfo);
```

結束資料表更新並釋放資源。釋放以 palloc 配置的記憶體通常並不重要，但像是開啟的檔案以及與遠端伺服器的連線等，則應該加以清理。

若 `EndForeignModify` 指標設為 `NULL`，則在執行器關閉期間不會執行任何動作。

由 `INSERT` 或 `COPY FROM` 插入分割資料表的元組會被路由到各分割區。若 FDW 支援可路由的外部資料表分割區，它也應該提供下列回呼函式。對外部資料表執行 `COPY FROM` 時，也會呼叫這些函式。

```

void
BeginForeignInsert(ModifyTableState *mtstate,
                   ResultRelInfo *rinfo);
```

開始執行外部資料表上的插入操作。無論該外部資料表是被選為元組路由目的地的分割區，或是 `COPY FROM` 命令中指定的目標，此函式都會在第一個元組插入該外部資料表之前被呼叫。它應該執行實際插入之前所需的任何初始化。之後，對於要插入外部資料表的元組，會呼叫 `ExecForeignInsert` 或 `ExecForeignBatchInsert`。

`mtstate` 是正在執行的 `ModifyTable` 計畫節點的整體狀態；關於計畫與執行狀態的全域資料可以透過此結構取得。`rinfo` 是描述目標外部資料表的 `ResultRelInfo` 結構。（`ResultRelInfo` 的 `ri_FdwState` 欄位可供 FDW 存放此操作所需的任何私有狀態。）

當此函式由 `COPY FROM` 命令呼叫時，不會提供 `mtstate` 中與計畫相關的全域資料，而且之後為每個插入的元組所呼叫的 `ExecForeignInsert`，其 `planSlot` 參數會是 `NULL`；無論該外部資料表是被選為元組路由目的地的分割區，或是命令中指定的目標，都是如此。

若 `BeginForeignInsert` 指標設為 `NULL`，則不會執行任何初始化動作。

請注意，若 FDW 不支援可路由的外部資料表分割區，及（或）不支援對外部資料表執行 `COPY FROM`，則此函式或之後被呼叫的 `ExecForeignInsert/ExecForeignBatchInsert` 必須視需要擲出錯誤。

```

void
EndForeignInsert(EState *estate,
                 ResultRelInfo *rinfo);
```

結束插入操作並釋放資源。釋放以 palloc 配置的記憶體通常並不重要，但像是開啟的檔案以及與遠端伺服器的連線等，則應該加以清理。

若 `EndForeignInsert` 指標設為 `NULL`，則不會執行任何結束動作。

```

int
IsForeignRelUpdatable(Relation rel);
```

回報指定的外部資料表支援哪些更新操作。回傳值應該是一個規則事件編號的位元遮罩，使用 `CmdType` 列舉表示外部資料表支援哪些操作；也就是說，`UPDATE` 為 `(1 << CMD_UPDATE) = 4`，`INSERT` 為 `(1 << CMD_INSERT) = 8`，`DELETE` 為 `(1 << CMD_DELETE) = 16`。

若 `IsForeignRelUpdatable` 指標設為 `NULL`，則當 FDW 分別提供了 `ExecForeignInsert`、`ExecForeignUpdate` 或 `ExecForeignDelete` 時，外部資料表會分別被視為可插入、可更新或可刪除。只有在 FDW 支援的資料表中有些可更新、有些不可更新時，才需要此函式。（即使如此，也允許在執行函式中擲出錯誤，而不是在此函式中檢查。不過，此函式會用來判斷在 `information_schema` 檢視表中所顯示的可更新性。）

對外部資料表的某些插入、更新與刪除，可以透過實作另一組替代介面來最佳化。一般的插入、更新與刪除介面會從遠端伺服器擷取資料列，然後一次修改一個資料列。在某些情況下，這種逐列處理的方式是必要的，但可能效率不彰。若外部伺服器能夠在不實際取回資料列的情況下判斷哪些資料列應該被修改，而且沒有會影響該操作的本地端結構（資料列層級的本地端觸發程序、儲存的產生欄位，或來自上層檢視表的 `WITH CHECK OPTION` 限制條件），那麼就可以將整個操作安排在遠端伺服器上執行。下文所述的介面讓這件事成為可能。

```

bool
PlanDirectModify(PlannerInfo *root,
                 ModifyTable *plan,
                 Index resultRelation,
                 int subplan_index);
```

判斷在遠端伺服器上執行直接修改是否安全。若安全，則在執行所需的規劃動作後回傳 `true`；否則回傳 `false`。這個選擇性函式會在查詢規劃期間被呼叫。若此函式成功，在執行階段將改為呼叫 `BeginDirectModify`、`IterateDirectModify` 與 `EndDirectModify`；否則，資料表的修改將使用上文所述的資料表更新函式來執行。參數與 `PlanForeignModify` 相同。

為了在遠端伺服器上執行直接修改，此函式必須將目標子計畫改寫為一個在遠端伺服器上執行直接修改的 `ForeignScan` 計畫節點。`ForeignScan` 的 `operation` 與 `resultRelation` 欄位必須適當設定。`operation` 必須設為與陳述式種類相對應的 `CmdType` 列舉值（也就是說，`UPDATE` 為 `CMD_UPDATE`，`INSERT` 為 `CMD_INSERT`，`DELETE` 為 `CMD_DELETE`），而 `resultRelation` 引數必須複製到 `resultRelation` 欄位。

更多資訊請參閱[第 58.4 節](fdw-planning.md)。

若 `PlanDirectModify` 指標設為 `NULL`，則不會嘗試在遠端伺服器上執行直接修改。

```

void
BeginDirectModify(ForeignScanState *node,
                  int eflags);
```

準備在遠端伺服器上執行直接修改。這會在執行器啟動期間被呼叫。它應該執行直接修改之前所需的任何初始化（直接修改本身應該在第一次呼叫 `IterateDirectModify` 時才進行）。`ForeignScanState` 節點已經建立，但其 `fdw_state` 欄位仍為 NULL。要修改的資料表的相關資訊可以透過 `ForeignScanState` 節點取得（特別是從底層的 `ForeignScan` 計畫節點，其中包含 `PlanDirectModify` 所提供的任何 FDW 私有資訊）。`eflags` 包含描述執行器對此計畫節點之運作模式的旗標位元。

請注意，當 `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` 為真時，此函式不應執行任何外部可見的動作；它只應做到讓節點狀態對 `ExplainDirectModify` 與 `EndDirectModify` 有效所需的最低限度工作。

若 `BeginDirectModify` 指標設為 `NULL`，則不會嘗試在遠端伺服器上執行直接修改。

```

TupleTableSlot *
IterateDirectModify(ForeignScanState *node);
```

當 `INSERT`、`UPDATE` 或 `DELETE` 查詢沒有 `RETURNING` 子句時，在遠端伺服器上完成直接修改後只需回傳 NULL。當查詢具有該子句時，擷取一筆包含 `RETURNING` 計算所需資料的結果，並以元組表槽回傳（應該使用節點的 `ScanTupleSlot` 來達成此目的）。實際插入、更新或刪除的資料必須存放在 `node->resultRelInfo->ri_projectReturning->pi_exprContext->ecxt_scantuple` 中。若沒有更多資料列可用，則回傳 NULL。請注意，此函式是在一個短生命週期的記憶體上下文中被呼叫，該上下文會在每次呼叫之間重設。若需要生命週期較長的儲存空間，請在 `BeginDirectModify` 中建立一個記憶體上下文，或使用節點之 `EState` 的 `es_query_cxt`。

若有提供 `fdw_scan_tlist` 目標清單，回傳的資料列必須與其相符；否則必須與被更新之外部資料表的資料列型別相符。若你選擇以最佳化省略擷取 `RETURNING` 計算不需要的欄位，應該在那些欄位位置填入 null，或者產生一個省略那些欄位的 `fdw_scan_tlist` 清單。

無論查詢是否具有該子句，查詢所回報的資料列數都必須由 FDW 自行遞增。當查詢沒有該子句時，在 `EXPLAIN ANALYZE` 的情況下，FDW 也必須遞增 `ForeignScanState` 節點的資料列數。

若 `IterateDirectModify` 指標設為 `NULL`，則不會嘗試在遠端伺服器上執行直接修改。

```

void
EndDirectModify(ForeignScanState *node);
```

在遠端伺服器上完成直接修改後進行清理。釋放以 palloc 配置的記憶體通常並不重要，但像是開啟的檔案以及與遠端伺服器的連線等，則應該加以清理。

若 `EndDirectModify` 指標設為 `NULL`，則不會嘗試在遠端伺服器上執行直接修改。

<a id="FDW-CALLBACKS-TRUNCATE"></a>

### 58.2.5. `TRUNCATE` 的 FDW 函式 [#](#FDW-CALLBACKS-TRUNCATE)

```

void
ExecForeignTruncate(List *rels,
                    DropBehavior behavior,
                    bool restart_seqs);
```

清空外部資料表。對外部資料表執行 [TRUNCATE](../../reference/sql-commands/sql-truncate.md) 時會呼叫此函式。`rels` 是要清空之外部資料表的 `Relation` 資料結構清單。

`behavior` 為 `DROP_RESTRICT` 或 `DROP_CASCADE`，分別表示原本的 `TRUNCATE` 命令要求了 `RESTRICT` 或 `CASCADE` 選項。

若 `restart_seqs` 為 `true`，表示原本的 `TRUNCATE` 命令要求了 `RESTART IDENTITY` 行為；否則表示要求的是 `CONTINUE IDENTITY` 行為。

請注意，原本的 `TRUNCATE` 命令中指定的 `ONLY` 選項不會傳給 `ExecForeignTruncate`。這個行為與外部資料表上 `SELECT`、`UPDATE` 與 `DELETE` 的回呼函式類似。

對於每個有外部資料表要被清空的外部伺服器，`ExecForeignTruncate` 都會被呼叫一次。這表示 `rels` 中包含的所有外部資料表都必須屬於同一個伺服器。

若 `ExecForeignTruncate` 指標設為 `NULL`，嘗試清空外部資料表時將會失敗並產生錯誤訊息。

<a id="FDW-CALLBACKS-ROW-LOCKING"></a>

### 58.2.6. 資料列鎖定的 FDW 函式 [#](#FDW-CALLBACKS-ROW-LOCKING)

若 FDW 希望支援*延遲資料列鎖定*（late row locking，如[第 58.5 節](fdw-row-locking.md)所述），它必須提供下列回呼函式：

```

RowMarkType
GetForeignRowMarkType(RangeTblEntry *rte,
                      LockClauseStrength strength);
```

回報外部資料表要使用哪一種資料列標記選項。`rte` 是該資料表的 `RangeTblEntry` 節點，而 `strength` 描述相關的 `FOR UPDATE/SHARE` 子句（若有的話）所要求的鎖定強度。結果必須是 `RowMarkType` 列舉型別的成員之一。

在查詢規劃期間，對於每個出現在 `UPDATE`、`DELETE` 或 `SELECT
FOR UPDATE/SHARE` 查詢中、且不是 `UPDATE` 或 `DELETE` 目標的外部資料表，都會呼叫此函式。

若 `GetForeignRowMarkType` 指標設為 `NULL`，則一律使用 `ROW_MARK_COPY` 選項。（這意味著 `RefetchForeignRow` 永遠不會被呼叫，因此也不需要提供它。）

更多資訊請參閱[第 58.5 節](fdw-row-locking.md)。

```

void
RefetchForeignRow(EState *estate,
                  ExecRowMark *erm,
                  Datum rowid,
                  TupleTableSlot *slot,
                  bool *updated);
```

從外部資料表重新擷取一個元組槽，若有需要則先將其鎖定。`estate` 是該查詢的全域執行狀態。`erm` 是 `ExecRowMark` 結構，描述目標外部資料表以及要取得的資料列鎖定類型（若有的話）。`rowid` 識別要擷取的元組。`slot` 在呼叫時不包含任何有用的內容，但可以用來存放回傳的元組。`updated` 是一個輸出參數。

此函式應該將元組存入所提供的槽中，若無法取得資料列鎖定則將槽清空。要取得的資料列鎖定類型由 `erm->markType` 定義，其值為先前由 `GetForeignRowMarkType` 回傳的值。（`ROW_MARK_REFERENCE` 表示只重新擷取元組而不取得任何鎖定，而此函式永遠不會看到 `ROW_MARK_COPY`。）

此外，若所擷取的是該元組的更新後版本，而不是先前取得的同一版本，則應該將 `*updated` 設為 `true`。（若 FDW 無法確定這一點，建議一律回傳 `true`。）

請注意，預設情況下，無法取得資料列鎖定時應該擲出錯誤；只有在 `erm->waitPolicy` 指定了 `SKIP LOCKED` 選項時，以空的槽回傳才是恰當的。

`rowid` 是先前為要重新擷取的資料列所讀取的 `ctid` 值。雖然 `rowid` 值是以 `Datum` 傳遞，但目前它只能是 `tid`。之所以選擇這樣的函式 API，是希望將來或許能允許資料列 ID 使用其他資料型別。

若 `RefetchForeignRow` 指標設為 `NULL`，嘗試重新擷取資料列時將會失敗並產生錯誤訊息。

更多資訊請參閱[第 58.5 節](fdw-row-locking.md)。

```

bool
RecheckForeignScan(ForeignScanState *node,
                   TupleTableSlot *slot);
```

重新檢查先前回傳的元組是否仍然符合相關的掃描與連接條件（qualifiers），並可能提供該元組的修改版本。對於不執行連接下推（join pushdown）的外部資料包裝器，通常較方便的做法是將此指標設為 `NULL`，改為適當設定 `fdw_recheck_quals`。然而，當外部連接被下推時，即使所有需要的屬性都存在，僅對結果元組重新套用與所有基礎資料表相關的檢查並不足夠，因為某些條件不符合時，可能導致某些屬性變成 NULL，而不是不回傳任何元組。`RecheckForeignScan` 可以重新檢查條件，若仍然滿足則回傳 true，否則回傳 false；但它也可以將替代元組存入所提供的槽中。

為了實作連接下推，外部資料包裝器通常會建構一個只用於重新檢查的替代本地端連接計畫；它將成為 `ForeignScan` 的外層子計畫。需要重新檢查時，可以執行此子計畫，並將產生的元組存入槽中。此計畫不需要有效率，因為沒有任何基礎資料表會回傳超過一個資料列；例如，它可以將所有連接都實作為巢狀迴圈。函式 `GetExistingLocalJoinPath` 可用於在既有路徑中搜尋合適的本地端連接路徑，作為替代的本地端連接計畫。`GetExistingLocalJoinPath` 會在指定之連接關聯的路徑清單中搜尋未參數化的路徑。（若找不到這樣的路徑，它會回傳 NULL；此時外部資料包裝器可以自行建構本地端路徑，也可以選擇不為該連接建立存取路徑。）

<a id="FDW-CALLBACKS-EXPLAIN"></a>

### 58.2.7. `EXPLAIN` 的 FDW 函式 [#](#FDW-CALLBACKS-EXPLAIN)

```

void
ExplainForeignScan(ForeignScanState *node,
                   ExplainState *es);
```

為外部資料表掃描輸出額外的 `EXPLAIN` 輸出內容。此函式可以呼叫 `ExplainPropertyText` 及相關函式，在 `EXPLAIN` 輸出中加入欄位。`es` 中的旗標欄位可用來決定要輸出什麼，而在 `EXPLAIN
ANALYZE` 的情況下，可以檢視 `ForeignScanState` 節點的狀態以提供執行時期統計資訊。

若 `ExplainForeignScan` 指標設為 `NULL`，則在 `EXPLAIN` 期間不會輸出任何額外資訊。

```

void
ExplainForeignModify(ModifyTableState *mtstate,
                     ResultRelInfo *rinfo,
                     List *fdw_private,
                     int subplan_index,
                     struct ExplainState *es);
```

為外部資料表更新輸出額外的 `EXPLAIN` 輸出內容。此函式可以呼叫 `ExplainPropertyText` 及相關函式，在 `EXPLAIN` 輸出中加入欄位。`es` 中的旗標欄位可用來決定要輸出什麼，而在 `EXPLAIN
ANALYZE` 的情況下，可以檢視 `ModifyTableState` 節點的狀態以提供執行時期統計資訊。前四個引數與 `BeginForeignModify` 相同。

若 `ExplainForeignModify` 指標設為 `NULL`，則在 `EXPLAIN` 期間不會輸出任何額外資訊。

```

void
ExplainDirectModify(ForeignScanState *node,
                    ExplainState *es);
```

為遠端伺服器上的直接修改輸出額外的 `EXPLAIN` 輸出內容。此函式可以呼叫 `ExplainPropertyText` 及相關函式，在 `EXPLAIN` 輸出中加入欄位。`es` 中的旗標欄位可用來決定要輸出什麼，而在 `EXPLAIN
ANALYZE` 的情況下，可以檢視 `ForeignScanState` 節點的狀態以提供執行時期統計資訊。

若 `ExplainDirectModify` 指標設為 `NULL`，則在 `EXPLAIN` 期間不會輸出任何額外資訊。

<a id="FDW-CALLBACKS-ANALYZE"></a>

### 58.2.8. `ANALYZE` 的 FDW 函式 [#](#FDW-CALLBACKS-ANALYZE)

```

bool
AnalyzeForeignTable(Relation relation,
                    AcquireSampleRowsFunc *func,
                    BlockNumber *totalpages);
```

對外部資料表執行 [ANALYZE](../../reference/sql-commands/sql-analyze.md) 時會呼叫此函式。若 FDW 能夠為此外部資料表收集統計資訊，它應該回傳 `true`，並在 *`func`* 中提供一個指向從該資料表收集樣本資料列之函式的指標，以及在 *`totalpages`* 中提供以頁數計的資料表估計大小。否則，回傳 `false`。

若 FDW 不支援為任何資料表收集統計資訊，可以將 `AnalyzeForeignTable` 指標設為 `NULL`。

若有提供，樣本收集函式必須具有下列簽章：

```

int
AcquireSampleRowsFunc(Relation relation,
                      int elevel,
                      HeapTuple *rows,
                      int targrows,
                      double *totalrows,
                      double *totaldeadrows);
```

應該從資料表收集最多 *`targrows`* 個資料列的隨機樣本，並存入呼叫端所提供的 *`rows`* 陣列。必須回傳實際收集到的資料列數。此外，請將資料表中存活資料列與死亡資料列總數的估計值，分別存入輸出參數 *`totalrows`* 與 *`totaldeadrows`*。（若 FDW 沒有死亡資料列的概念，請將 *`totaldeadrows`* 設為零。）

<a id="FDW-CALLBACKS-IMPORT"></a>

### 58.2.9. `IMPORT FOREIGN SCHEMA` 的 FDW 函式 [#](#FDW-CALLBACKS-IMPORT)

```

List *
ImportForeignSchema(ImportForeignSchemaStmt *stmt, Oid serverOid);
```

取得外部資料表建立命令的清單。此函式會在執行 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/sql-importforeignschema.md) 時被呼叫，並傳入該陳述式的剖析樹，以及要使用的外部伺服器的 OID。它應該回傳一個 C 字串清單，其中每個字串都必須包含一個 [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md) 命令。這些字串將由核心伺服器剖析並執行。

在 `ImportForeignSchemaStmt` 結構中，`remote_schema` 是要從中匯入資料表的遠端綱要名稱。`list_type` 指出如何過濾資料表名稱：`FDW_IMPORT_SCHEMA_ALL` 表示應匯入遠端綱要中的所有資料表（此時 `table_list` 為空），`FDW_IMPORT_SCHEMA_LIMIT_TO` 表示只納入 `table_list` 中列出的資料表，而 `FDW_IMPORT_SCHEMA_EXCEPT` 表示排除 `table_list` 中列出的資料表。`options` 是匯入過程所使用的選項清單。這些選項的意義由 FDW 決定。例如，FDW 可以用某個選項來決定是否應匯入欄位的 `NOT NULL` 屬性。這些選項不必與 FDW 作為資料庫物件選項所支援的那些選項有任何關聯。

FDW 可以忽略 `ImportForeignSchemaStmt` 的 `local_schema` 欄位，因為核心伺服器會自動將該名稱插入剖析後的 `CREATE
FOREIGN TABLE` 命令中。

FDW 也不必自行實作 `list_type` 與 `table_list` 所指定的過濾，因為核心伺服器會自動略過依這些選項而被排除之資料表的任何回傳命令。不過，一開始就避免為被排除的資料表建立命令，通常是有用的。函式 `IsImportableForeignTable()` 可用來測試給定的外部資料表名稱是否會通過過濾。

若 FDW 不支援匯入資料表定義，可以將 `ImportForeignSchema` 指標設為 `NULL`。

<a id="FDW-CALLBACKS-PARALLEL"></a>

### 58.2.10. 平行執行的 FDW 函式 [#](#FDW-CALLBACKS-PARALLEL)

`ForeignScan` 節點可以選擇性地支援平行執行。平行的 `ForeignScan` 會在多個程序中執行，並且必須在所有協同運作的程序之間，讓每個資料列恰好只回傳一次。為此，各程序可以透過固定大小的動態共享記憶體區塊來協調。此共享記憶體不保證在每個程序中都對應到相同的位址，因此其中不得包含指標。下列函式全都是選擇性的，但若要支援平行執行，其中大部分都是必要的。

```

bool
IsForeignScanParallelSafe(PlannerInfo *root, RelOptInfo *rel,
                          RangeTblEntry *rte);
```

測試掃描是否可以在平行工作程序中執行。只有在規劃器認為平行計畫可能可行時才會呼叫此函式；若該掃描在平行工作程序中執行是安全的，此函式應該回傳 true。若遠端資料來源具有交易語意，通常就不是這種情況，除非能以某種方式讓工作程序對資料的連線與領導程序共享相同的交易上下文。

若未定義此函式，則會假設掃描必須在平行領導程序中進行。請注意，回傳 true 並不表示掃描本身可以平行進行，只表示掃描可以在平行工作程序中執行。因此，即使不支援平行執行，定義此方法也可能是有用的。

```

Size
EstimateDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt);
```

估計平行操作所需的動態共享記憶體量。此值可以高於實際使用的量，但不得低於實際使用的量。回傳值以位元組為單位。此函式是選擇性的，不需要時可以省略；但若省略此函式，接下來的三個函式也必須一併省略，因為不會配置任何共享記憶體供 FDW 使用。

```

void
InitializeDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt,
                         void *coordinate);
```

初始化平行操作所需的動態共享記憶體。`coordinate` 指向一塊共享記憶體區域，其大小等於 `EstimateDSMForeignScan` 的回傳值。此函式是選擇性的，不需要時可以省略。

```

void
ReInitializeDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt,
                           void *coordinate);
```

當外部掃描計畫節點即將被重新掃描時，重新初始化平行操作所需的動態共享記憶體。此函式是選擇性的，不需要時可以省略。建議的做法是讓此函式只重設共享狀態，而 `ReScanForeignScan` 函式只重設本地端狀態。目前，此函式會在 `ReScanForeignScan` 之前被呼叫，但最好不要依賴這個順序。

```

void
InitializeWorkerForeignScan(ForeignScanState *node, shm_toc *toc,
                            void *coordinate);
```

根據領導程序在 `InitializeDSMForeignScan` 期間所設定的共享狀態，初始化平行工作程序的本地端狀態。此函式是選擇性的，不需要時可以省略。

```

void
ShutdownForeignScan(ForeignScanState *node);
```

當預期節點不會被執行到完成時釋放資源。並非所有情況下都會呼叫此函式；有時候，可能在未先呼叫此函式的情況下就呼叫 `EndForeignScan`。由於平行查詢所使用的 DSM 區段會在此回呼函式被呼叫後隨即被銷毀，希望在 DSM 區段消失之前採取某些動作的外部資料包裝器應該實作此方法。

<a id="FDW-CALLBACKS-ASYNC"></a>

### 58.2.11. 非同步執行的 FDW 函式 [#](#FDW-CALLBACKS-ASYNC)

`ForeignScan` 節點可以選擇性地支援非同步執行，如 `src/backend/executor/README` 中所述。下列函式全都是選擇性的，但若要支援非同步執行，則全部都是必要的。

```

bool
IsForeignPathAsyncCapable(ForeignPath *path);
```

測試給定的 `ForeignPath` 路徑是否能以非同步方式掃描底層的外部關聯。只有在查詢規劃的最後，當給定路徑是某個 `AppendPath` 路徑的直接子路徑，且規劃器認為非同步執行能提升效能時，才會呼叫此函式；若給定路徑能夠以非同步方式掃描外部關聯，此函式應該回傳 true。

若未定義此函式，則會假設給定路徑使用 `IterateForeignScan` 掃描外部關聯。（這意味著下文所述的回呼函式永遠不會被呼叫，因此也不需要提供它們。）

```

void
ForeignAsyncRequest(AsyncRequest *areq);
```

以非同步方式從 `ForeignScan` 節點產生一個元組。`areq` 是 `AsyncRequest` 結構，描述該 `ForeignScan` 節點以及向它請求元組的上層 `Append` 節點。此函式應該將元組存入 `areq->result` 所指定的槽中，並將 `areq->request_complete` 設為 `true`；或者，若它需要等待核心伺服器外部的事件（例如網路 I/O）而無法立即產生任何元組，則將該旗標設為 `false`，並將 `areq->callback_pending` 設為 `true`，讓 `ForeignScan` 節點能從下文所述的回呼函式獲得回呼。若沒有更多元組可用，則將槽設為 NULL 或空的槽，並將 `areq->request_complete` 旗標設為 `true`。建議使用 `ExecAsyncRequestDone` 或 `ExecAsyncRequestPending` 來設定 `areq` 中的輸出參數。

```

void
ForeignAsyncConfigureWait(AsyncRequest *areq);
```

設定 `ForeignScan` 節點希望等待的檔案描述子事件。只有在 `ForeignScan` 節點設定了 `areq->callback_pending` 旗標時才會呼叫此函式，而此函式應該將該事件加入 `areq` 所描述之上層 `Append` 節點的 `as_eventset` 中。更多資訊請參閱 `src/backend/executor/execAsync.c` 中 `ExecAsyncConfigureWait` 的註解。當檔案描述子事件發生時，將會呼叫 `ForeignAsyncNotify`。

```

void
ForeignAsyncNotify(AsyncRequest *areq);
```

處理已發生的相關事件，然後以非同步方式從 `ForeignScan` 節點產生一個元組。此函式應該以與 `ForeignAsyncRequest` 相同的方式設定 `areq` 中的輸出參數。

<a id="FDW-CALLBACKS-REPARAMETERIZE-PATHS"></a>

### 58.2.12. 路徑重新參數化的 FDW 函式 [#](#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

```

List *
ReparameterizeForeignPathByChild(PlannerInfo *root, List *fdw_private,
                                 RelOptInfo *child_rel);
```

當要把一個以給定子關聯 `child_rel` 的最上層父關聯參數化的路徑，轉換為以該子關聯參數化時，會呼叫此函式。此函式用於將 `ForeignPath` 的給定 `fdw_private` 成員中所保存的任何路徑重新參數化，或轉譯其中的任何運算式節點。此回呼函式可以視需要使用 `reparameterize_path_by_child`、`adjust_appendrel_attrs` 或 `adjust_appendrel_attrs_multilevel`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdw-callbacks.html)（原文版本：18.6；核對日期：2026-10-17）
