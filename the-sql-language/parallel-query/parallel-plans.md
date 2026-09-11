<a id="PARALLEL-PLANS"></a>

## 15.3. 平行計畫 [#](#PARALLEL-PLANS)

[15.3.1. 平行掃描](parallel-plans.md#PARALLEL-SCANS)

[15.3.2. 平行聯結](parallel-plans.md#PARALLEL-JOINS)

[15.3.3. 平行彙總](parallel-plans.md#PARALLEL-AGGREGATION)

[15.3.4. 平行 Append](parallel-plans.md#PARALLEL-APPEND)

[15.3.5. 平行計畫的提示](parallel-plans.md#PARALLEL-PLAN-TIPS)

由於每個工作程序都會將計畫的平行部分執行到完成，因此不能單純拿一個一般的查詢計畫，以多個工作程序來執行它。每個工作程序都會產生一份完整的輸出結果集合副本，因此查詢不但不會比平常快，還會產生錯誤的結果。相反地，計畫的平行部分必須是查詢最佳化器內部所稱的*部分計畫*（partial plan）；也就是說，它的建構方式必須讓執行該計畫的每個程序只產生輸出資料列的一個子集合，並保證每一筆必要的輸出資料列都恰好由其中一個協作程序產生。一般而言，這表示對查詢驅動資料表的掃描必須是具平行感知能力（parallel-aware）的掃描。

<a id="PARALLEL-SCANS"></a>

### 15.3.1. 平行掃描 [#](#PARALLEL-SCANS)

目前支援下列類型具平行感知能力的資料表掃描。

* 在*平行循序掃描*（parallel sequential scan）中，資料表的區塊會被分成若干範圍，並由各協作程序分擔。每個工作程序會先完成所分配區塊範圍的掃描，再要求另一個區塊範圍。
* 在*平行 bitmap heap 掃描*（parallel bitmap heap scan）中，會選出一個程序作為領導程序。該程序會掃描一個或多個索引，並建立一個點陣圖，指出需要走訪哪些資料表區塊。接著，這些區塊會像平行循序掃描一樣，分配給各協作程序。換句話說，heap 掃描是平行執行的，但底層的索引掃描則不是。
* 在*平行索引掃描*（parallel index scan）或*平行僅索引掃描*（parallel index-only scan）中，各協作程序會輪流從索引讀取資料。目前只有 btree 索引支援平行索引掃描。每個程序會認領一個索引區塊，並掃描並回傳該區塊所參照的所有 tuple；其他程序可以同時回傳來自其他索引區塊的 tuple。平行 btree 掃描的結果在每個工作程序內會以排序好的順序回傳。

其他掃描類型（例如非 btree 索引的掃描）未來可能會支援平行掃描。

<a id="PARALLEL-JOINS"></a>

### 15.3.2. 平行聯結 [#](#PARALLEL-JOINS)

就像在非平行計畫中一樣，驅動資料表可以使用巢狀迴圈、雜湊聯結或合併聯結與一個或多個其他資料表聯結。聯結的內側可以是規劃器原本就支援的任何一種非平行計畫，只要它在平行工作程序中執行是安全的即可。依聯結類型而定，內側也可以是平行計畫。

* 在*巢狀迴圈聯結*（nested loop join）中，內側一律是非平行的。雖然它會被完整執行，但如果內側是索引掃描，這樣做仍然很有效率，因為外側的 tuple，以及因此在索引中查找值的迴圈，都會分配給各協作程序。
* 在*合併聯結*（merge join）中，內側一律是非平行計畫，因此會被完整執行。這可能缺乏效率，特別是在必須進行排序時，因為工作與產生的資料會在每個協作程序中重複。
* 在*雜湊聯結*（hash join，沒有「parallel」前綴）中，每個協作程序都會完整執行內側，以建立相同的雜湊表副本。如果雜湊表很大或計畫的成本很高，這可能缺乏效率。在*平行雜湊聯結*（parallel hash join）中，內側是一個*平行雜湊*（parallel hash），會將建立共用雜湊表的工作分配給各協作程序。

<a id="PARALLEL-AGGREGATION"></a>

### 15.3.3. 平行彙總 [#](#PARALLEL-AGGREGATION)

PostgreSQL 以兩個階段進行彙總來支援平行彙總。首先，參與查詢平行部分的每個程序都會執行一個彙總步驟，為該程序所知道的每個群組產生部分結果。這在計畫中會顯示為 `Partial Aggregate` 節點。接著，部分結果會透過 `Gather` 或 `Gather Merge` 傳送給領導程序。最後，領導程序會跨所有工作程序重新彙總結果，以產生最終結果。這在計畫中會顯示為 `Finalize Aggregate` 節點。

由於 `Finalize Aggregate` 節點是在領導程序上執行的，因此相對於輸入資料列數量會產生較多群組的查詢，在查詢規劃器看來就比較不划算。例如，在最壞的情況下，`Finalize Aggregate` 節點所看到的群組數量，可能與所有工作程序在 `Partial Aggregate` 階段所看到的輸入資料列數量一樣多。在這種情況下，使用平行彙總顯然不會帶來任何效能上的好處。查詢規劃器在規劃過程中會考量這一點，因此在這種情況下不太可能選擇平行彙總。

並非所有情況都支援平行彙總。每個彙總函式都必須是可[安全](parallel-safety.md)平行執行的，而且必須有合併函式（combine function）。如果彙總函式的轉移狀態是 `internal` 型別，它就必須有序列化與反序列化函式。更多細節請參閱 [CREATE AGGREGATE](../../reference/sql-commands/sql-createaggregate.md)。如果任何彙總函式呼叫包含 `DISTINCT` 或 `ORDER BY` 子句，就不支援平行彙總；對於有序集合彙總函式，或查詢涉及 `GROUPING SETS` 時，也不支援平行彙總。只有在查詢所涉及的所有聯結也都屬於計畫的平行部分時，才能使用平行彙總。

<a id="PARALLEL-APPEND"></a>

### 15.3.4. 平行 Append [#](#PARALLEL-APPEND)

每當 PostgreSQL 需要將來自多個來源的資料列合併成單一結果集合時，它會使用 `Append` 或 `MergeAppend` 計畫節點。這通常發生在實作 `UNION ALL` 或掃描分割資料表時。這類節點可以像在任何其他計畫中一樣用在平行計畫中。不過，在平行計畫中，規劃器也可能改用 `Parallel Append` 節點。

在平行計畫中使用 `Append` 節點時，每個程序都會依子計畫出現的順序執行它們，因此所有參與的程序會合作執行第一個子計畫直到完成，然後大約在同一時間移到第二個計畫。改用 `Parallel Append` 時，執行器則會盡可能平均地將參與的程序分散到各個子計畫上，讓多個子計畫同時執行。這樣可以避免競爭，也可以避免在從未執行某個子計畫的程序中支付該子計畫的啟動成本。

此外，一般的 `Append` 節點在平行計畫中使用時只能有部分子計畫（partial child），而 `Parallel Append` 節點則可以同時擁有部分與非部分子計畫。非部分子計畫只會由單一程序掃描，因為掃描它們多次會產生重複的結果。因此，涉及附加多個結果集合的計畫，即使在沒有有效率的部分計畫可用時，也能達成粗粒度的平行處理。例如，考慮一個針對分割資料表的查詢，它只能透過使用不支援平行掃描的索引才能有效率地實作。規劃器可能會選擇由一般 `Index Scan` 計畫組成的 `Parallel Append`；每個個別的索引掃描都必須由單一程序執行到完成，但不同的掃描可以由不同的程序同時進行。

可以使用 [enable_parallel_append](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARALLEL-APPEND) 停用這項功能。

<a id="PARALLEL-PLAN-TIPS"></a>

### 15.3.5. 平行計畫的提示 [#](#PARALLEL-PLAN-TIPS)

如果某個預期會產生平行計畫的查詢並沒有產生，可以嘗試降低 [parallel_setup_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-PARALLEL-SETUP-COST) 或 [parallel_tuple_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-PARALLEL-TUPLE-COST)。當然，這個計畫最後可能比規劃器原本偏好的循序計畫還慢，但並不一定總是如此。如果即使將這些設定設為非常小的值（例如將兩者都設為零）仍然得不到平行計畫，可能有某些原因使查詢規劃器無法為你的查詢產生平行計畫。可能的原因請參閱[第 15.2 節](when-can-parallel-query-be-used.md)與[第 15.4 節](parallel-safety.md)。

執行平行計畫時，可以使用 `EXPLAIN (ANALYZE, VERBOSE)` 顯示每個計畫節點的各工作程序統計資訊。這有助於判斷工作是否平均分配到所有計畫節點，並更廣泛地瞭解計畫的效能特性。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/parallel-plans.html)（原文版本：18.6；核對日期：2026-09-11）
