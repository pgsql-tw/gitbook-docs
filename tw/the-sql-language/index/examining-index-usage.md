# 11.12. 檢查索引運用

雖然 PostgreSQL 中的索引不需要維護或調教，但檢查查詢工作負載實際使用哪些索引仍然很重要。以 [EXPLAIN](../../reference/sql-commands/explain.md) 指令檢查單個查詢的索引使用情況；[第 14.1 節](../performance-tips/using-explain.md)說明了其應用。如[第 27.2 節](../../server-administration/monitoring-database-activity/the-statistics-collector.md)所述，還可以在正在執行的伺服器中收集有關索引使用情況的整體統計訊息。

決定要建立哪些索引的一般過程是很難確定的。在前面幾節的範例中已經顯示了許多典型案例。通常需要進行大量的實驗。本節的剩餘部分提供了一些提示：

* 始終先執行 [ANALYZE](../../reference/sql-commands/analyze.md)。此指令收集有關資料表中內容的分佈的統計訊息。需要此訊息來估計查詢回傳的資料列數量，計劃程序需要為每個可能的查詢計劃分配實際成本。在沒有任何實際統計資料的情況下，會假設某些預設值，但這幾乎肯定是不準確的。因此，在沒有執行 ANALYZE 的情況下檢查應用程序的索引使用情況是失敗的。有關更多訊息，請參閱[第 24.1.3 節](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-3-geng-xin-qi)和[第 24.1.6 節](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-autovacuum-bei-jing-cheng-xu)。
* 使用真實資料進行實驗。使用測試資料設定索引將告訴您測試資料需要哪些索引，但這就是全部。使用非常小的測試資料集尤其致命。雖然選擇 100000 筆資料中的 1000 個可能是索引的候選者，但選擇 100 筆資料中的 1 個就幾乎不會，因為 100 筆資料可能適合單個磁碟頁面，並且沒有計劃可以比循序讀取 1 個磁碟頁面更好。在編輯測試資料時要小心，這在應用尚未投入産品階段時通常是不可避免的。非常相似，完全隨機或按排序順序插入的值會使統計資料偏離實際資料所具有的分佈。
* 當不使用索引時，它可以用於測試以強制使用它們。有些執行時的參數可以關閉各種計劃類型（參閱[第 19.7.1 節](../../server-administration/server-configuration/query-planning.md#19-7-1-planner-method-configuration)）。例如，關閉循序掃描（enable\_seqscan）和巢狀循環掃描（enable\_nestloop）這些是最基本的計劃，將迫使系統使用不同的計劃。如果系統仍然選擇循序掃描或巢狀循環掃描，則可能存在更為根本的原因，即不使用索引；例如，查詢條件與索引無法搭配。（什麼樣的查詢可以使用前面幾節中解釋的索引類型。）
* 如果強制索引使用也確實使用索引，那麼有兩種可能性：系統是正確的並且使用索引確實不合適，或者查詢計劃的成本估算未反映現實。因此，您應該使用和不使用索引來查詢查詢。EXPLAIN ANALYZE 指令在這裡很有用。
* 如果事實證明成本估算是錯誤的，那麼又有兩種可能性。 總成本是根據每個計劃節點的每行成本乘以計劃節點的可能性估計來計算的。可以透過執行時參數調整計劃節點的估計成本（在[第 19.7.2 節](../../server-administration/server-configuration/query-planning.md#19-7-2-planner-cost-constants)中描述）。可能性估計不準確是由於統計資訊不足。可以透過調整統計訊息收集參數來改進這一點（參閱 [ALTER TABLE](../../reference/sql-commands/alter-table.md)）。

如果您對查詢成本沒有更好的調整方案了，那麼您可能不得不明確強制使用索引。也許你還需要聯繫 PostgreSQL 開發人員來協同檢查問題。

