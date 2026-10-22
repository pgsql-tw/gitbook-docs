<a id="PGOVEREXPLAIN"></a>

## F.29. pg_overexplain — 允許 EXPLAIN 傾印更多細節 [#](#PGOVEREXPLAIN)

[F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)

[F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)

[F.29.3. 作者](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

<a id="id-1.11.7.39.2"></a>

`pg_overexplain` 模組以提供額外輸出的新選項擴充 `EXPLAIN`。
它主要用於協助規劃器的除錯與開發，而非一般用途。由於此模組會顯示規劃器資料結構的內部細節，可能需要參閱原始碼才能理解其輸出。此外，每當這些資料結構變更時，輸出很可能也會隨之變更（而且變更頻率與之相同）。

要使用它，只需將它載入伺服器即可。你可以將它載入個別的工作階段：

```

LOAD 'pg_overexplain';
```

你也可以在 `postgresql.conf` 中將
`pg_overexplain` 加入
[session_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) 或
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)，
以便將它預先載入部分或所有工作階段。

<a id="PGOVEREXPLAIN-DEBUG"></a>

### F.29.1. EXPLAIN (DEBUG) [#](#PGOVEREXPLAIN-DEBUG)

`DEBUG` 選項會顯示計畫樹中的各種資訊，這些資訊通常不會顯示，因為一般認為多數人不會感興趣。對每個個別的計畫節點，它會顯示下列欄位。這些欄位的其他說明，請參閱
`nodes/plannodes.h` 中的 `Plan`。

* `Disabled Nodes`。一般的 `EXPLAIN`
  會檢查節點的停用節點計數是否大於其下層節點計數的總和，藉此判斷該節點是否已停用。此選項會顯示原始的計數器值。
* `Parallel Safe`。表示計畫樹節點出現在 `Gather` 或
  `Gather Merge` 節點之下是否安全，不論它實際上是否位於這類節點之下。
* `Plan Node ID`。內部 ID 編號，對計畫樹中的每個節點應該都是唯一的。它用於協調平行查詢的活動。
* `extParam` 與 `allParam`。關於哪些編號參數會影響此計畫節點或其子節點的資訊。在文字模式下，只有當這些欄位為非空集合時才會顯示。

每個查詢一次，`DEBUG` 選項會顯示下列欄位。其他細節請參閱
`nodes/plannodes.h` 中的 `PlannedStmt`。

* `Command Type`。例如 `select`
  或 `update`。
* `Flags`。以逗號分隔的清單，列出 `PlannedStmt` 中被設為
  `true` 的布林結構成員名稱。它涵蓋下列結構成員：
  `hasReturning`、`hasModifyingCTE`、
  `canSetTag`、`transientPlan`、
  `dependsOnRole`、`parallelModeNeeded`。
* `Subplans Needing Rewind`。可能需要由執行器倒回（rewind）之子計畫的整數 ID。
* `Relation OIDs`。此計畫所相依之關聯的 OID。
* `Executor Parameter Types`。每個執行器參數的型別 OID
  （例如選擇了巢狀迴圈，並使用參數將值向下傳遞給內側索引掃描時）。不包括使用者提供給預備陳述式的參數。
* `Parse Location`。在提供給規劃器的查詢字串中，可找到此查詢文字的位置。在某些情境下可能是
  `Unknown`。否則，可能是某個整數 `NNN` 的
  `NNN to end`，或某些整數
  `NNN` 與 `MMM` 的
  `NNN for MMM bytes`。

<a id="PGOVEREXPLAIN-RANGE-TABLE"></a>

### F.29.2. EXPLAIN (RANGE_TABLE) [#](#PGOVEREXPLAIN-RANGE-TABLE)

`RANGE_TABLE` 選項會顯示計畫樹中特別與查詢的範圍表（range table）相關的資訊。範圍表項目大致對應出現在查詢之
`FROM` 子句中的項目，但有許多例外。例如，經證明不需要的子查詢可能會從範圍表中完全刪除，而繼承展開則會為查詢中未直接指名的子資料表加入範圍表項目。

在查詢計畫中，範圍表項目通常以範圍表索引（range table index，RTI）參照。參照一個或多個 RTI 的計畫節點，會使用下列其中一個欄位相應地標示：`Scan
RTI`、`Nominal RTI`、`Exclude Relation
RTI`、`Append RTIs`。

此外，整個查詢可能會為各種用途維護範圍表索引的清單。這些清單每個查詢顯示一次，並視情況標示為 `Unprunable RTIs` 或
`Result RTIs`。在文字模式下，只有當這些欄位為非空集合時才會顯示。

最後，也是最重要的一點，`RANGE_TABLE` 選項
會顯示查詢整個範圍表的傾印。每個範圍表項目都會標示對應的範圍表索引、範圍表項目的種類（例如 `relation`、
`subquery` 或 `join`），接著是各種範圍表項目欄位的內容，這些欄位通常不屬於
`EXPLAIN` 輸出的一部分。其中部分欄位只會針對特定種類的範圍表項目顯示。例如，
`Eref` 會針對所有類型的範圍表項目顯示，
但 `CTE Name` 只會針對類型為 `cte` 的範圍表項目顯示。

關於範圍表項目的更多資訊，請參閱 `nodes/parsenodes.h` 中 `RangeTblEntry` 的定義。

<a id="PGOVEREXPLAIN-AUTHOR"></a>

### F.29.3. 作者 [#](#PGOVEREXPLAIN-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgoverexplain.html)（原文版本：18.6；核對日期：2026-10-23）
