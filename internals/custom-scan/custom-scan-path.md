<a id="CUSTOM-SCAN-PATH"></a>

## 60.1. 建立自訂掃描路徑 [#](#CUSTOM-SCAN-PATH)

[60.1.1. 自訂掃描路徑回呼函式](custom-scan-path.md#CUSTOM-SCAN-PATH-CALLBACKS)

自訂掃描提供者通常會藉由設定下列掛鉤，為基礎關聯加入路徑；這個掛鉤會在核心程式碼為該關聯產生它所能產生的所有存取路徑之後被呼叫（Gather 與 Gather Merge 路徑除外，這兩種路徑會在此呼叫之後才建立，以便能使用該掛鉤所加入的部分路徑）：

```

typedef void (*set_rel_pathlist_hook_type) (PlannerInfo *root,
                                            RelOptInfo *rel,
                                            Index rti,
                                            RangeTblEntry *rte);
extern PGDLLIMPORT set_rel_pathlist_hook_type set_rel_pathlist_hook;
```

雖然這個掛鉤函式可以用來檢查、修改或移除核心系統所產生的路徑，但自訂掃描提供者通常只會產生 `CustomPath` 物件，並使用 `add_path` 將它們加入 `rel`；如果是部分路徑，則使用 `add_partial_path`。自訂掃描提供者負責初始化 `CustomPath` 物件，其宣告如下：

```

typedef struct CustomPath
{
    Path      path;
    uint32    flags;
    List     *custom_paths;
    List     *custom_restrictinfo;
    List     *custom_private;
    const CustomPathMethods *methods;
} CustomPath;
```

`path` 必須像其他任何路徑一樣初始化，包括資料列數估計值、啟動成本與總成本，以及此路徑所提供的排序順序。`flags` 是一個位元遮罩，用來指定掃描提供者是否能支援某些選用功能。如果自訂路徑能支援反向掃描，`flags` 應該包含 `CUSTOMPATH_SUPPORT_BACKWARD_SCAN`；如果它能支援標記與還原（mark and restore），應該包含 `CUSTOMPATH_SUPPORT_MARK_RESTORE`；如果它能執行投影（projection），則應該包含 `CUSTOMPATH_SUPPORT_PROJECTION`。（如果未設定 `CUSTOMPATH_SUPPORT_PROJECTION`，掃描節點只會被要求產生所掃描關聯的 Var；而如果設定了該旗標，掃描節點就必須能夠對這些 Var 計算純量運算式。）選用的 `custom_paths` 是此自訂路徑節點所使用的 `Path` 節點清單；規劃器會將它們轉換為 `Plan` 節點。如下文所述，也可以為連接關聯建立自訂路徑。在這種情況下，應該使用 `custom_restrictinfo` 來儲存要套用到該自訂路徑所取代之連接的連接子句集合。否則它應該為 NIL。`custom_private` 可以用來儲存自訂路徑的私有資料。私有資料應該以 `nodeToString` 能夠處理的形式儲存，如此嘗試印出自訂路徑的除錯常式才能如設計般運作。`methods` 必須指向一個實作所需自訂路徑方法的物件（通常是靜態配置的），這些方法將在下文進一步詳述。

自訂掃描提供者也可以提供連接路徑。如同基礎關聯的情況，這種路徑必須產生與它所取代之連接通常會產生的相同輸出。為此，連接提供者應該設定下列掛鉤，然後在掛鉤函式中，為該連接關聯建立 `CustomPath` 路徑。

```

typedef void (*set_join_pathlist_hook_type) (PlannerInfo *root,
                                             RelOptInfo *joinrel,
                                             RelOptInfo *outerrel,
                                             RelOptInfo *innerrel,
                                             JoinType jointype,
                                             JoinPathExtraData *extra);
extern PGDLLIMPORT set_join_pathlist_hook_type set_join_pathlist_hook;
```

對同一個連接關聯，這個掛鉤會以內側與外側關聯的不同組合被重複呼叫；將重複的工作減到最少是掛鉤的責任。

另請注意，要套用到該連接的連接子句集合（以 `extra->restrictlist` 傳入）會依內側與外側關聯的組合而有所不同。為 `joinrel` 產生的 `CustomPath` 路徑必須包含它所使用的連接子句集合；如果規劃器選中該路徑作為 `joinrel` 的最佳路徑，規劃器就會使用這些子句將該 `CustomPath` 路徑轉換為計畫。

<a id="CUSTOM-SCAN-PATH-CALLBACKS"></a>

### 60.1.1. 自訂掃描路徑回呼函式 [#](#CUSTOM-SCAN-PATH-CALLBACKS)

```

Plan *(*PlanCustomPath) (PlannerInfo *root,
                         RelOptInfo *rel,
                         CustomPath *best_path,
                         List *tlist,
                         List *clauses,
                         List *custom_plans);
```

將自訂路徑轉換為完成的計畫。傳回值通常會是一個 `CustomScan` 物件，回呼函式必須配置並初始化該物件。詳情請參閱[第 60.2 節](custom-scan-plan.md)。

```

List *(*ReparameterizeCustomPathByChild) (PlannerInfo *root,
                                          List *custom_private,
                                          RelOptInfo *child_rel);
```

當要把一條以給定子關聯 `child_rel` 的最上層父關聯參數化的路徑，轉換為以該子關聯參數化時，會呼叫此回呼函式。此回呼函式用來將 `CustomPath` 的給定 `custom_private` 成員中所儲存的任何路徑重新參數化，或轉換其中所儲存的任何運算式節點。回呼函式可以視需要使用 `reparameterize_path_by_child`、`adjust_appendrel_attrs` 或 `adjust_appendrel_attrs_multilevel`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/custom-scan-path.html)（原文版本：18.6；核對日期：2026-10-17）
