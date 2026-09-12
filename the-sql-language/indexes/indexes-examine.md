<a id="INDEXES-EXAMINE"></a>

## 11.12. 檢查索引的使用情形 [#](#INDEXES-EXAMINE)

<a id="id-1.5.10.15.2"></a>

雖然 PostgreSQL 中的索引不需要維護或調校，但檢查實際查詢工作負載真正使用了哪些索引仍然很重要。檢查個別查詢的索引使用情形，要使用 [EXPLAIN](../../reference/sql-commands/sql-explain.md) 命令；[第 14.1 節](../performance-tips/using-explain.md)說明了如何將它用於這個目的。也可以收集執行中伺服器之索引使用情形的整體統計資訊，如[第 27.2 節](../../server-administration/monitoring/monitoring-stats.md)所述。

要擬定一套判斷該建立哪些索引的通用程序並不容易。前面各節的範例中已經展示了一些典型的情況。通常需要大量的實驗。本節其餘部分提供一些相關的提示：

* 一定要先執行 [ANALYZE](../../reference/sql-commands/sql-analyze.md)。這個命令會收集資料表中值之分布的統計資訊。估計查詢回傳的資料列數需要這些資訊，而規劃器需要這個估計值，才能為每個可能的查詢計畫指定符合實際的成本。在沒有任何真實統計資訊的情況下，會假設一些預設值，而這些預設值幾乎可以肯定是不準確的。因此，在沒有執行 `ANALYZE` 的情況下檢查應用程式的索引使用情形，是徒勞無功的。更多資訊請參閱[第 24.1.3 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-STATISTICS)與[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)。
* 使用真實資料進行實驗。使用測試資料來建立索引，只會告訴你測試資料需要哪些索引，僅此而已。

  使用非常小的測試資料集尤其致命。從 100000 筆資料列中選取 1000 筆，可能是使用索引的候選情況；但從 100 筆資料列中選取 1 筆就很難是了，因為這 100 筆資料列很可能放得進單一個磁碟頁面，而沒有任何計畫能勝過循序擷取 1 個磁碟頁面。

  編造測試資料時也要小心，在應用程式尚未上線時，這往往是不可避免的。非常相似、完全隨機或依排序順序插入的值，都會使統計資訊偏離真實資料應有的分布。
* 當索引沒有被使用時，為了測試而強制使用它們可能會有幫助。有一些執行時期參數可以關閉各種計畫類型（請參閱[第 19.7.1 節](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)）。例如，關閉循序掃描（`enable_seqscan`）與巢狀迴圈聯結（`enable_nestloop`）這兩種最基本的計畫，就會強制系統使用不同的計畫。如果系統仍然選擇循序掃描或巢狀迴圈聯結，那麼索引沒有被使用大概有更根本的原因；例如，查詢條件與索引不相符。（什麼樣的查詢可以使用什麼樣的索引，在前面各節中已有說明。）
* 如果強制使用索引時確實使用了索引，那麼有兩種可能：一是系統是對的，使用索引確實不合適；二是查詢計畫的成本估計沒有反映實際情況。所以你應該分別量測使用與不使用索引時查詢所花的時間。`EXPLAIN ANALYZE` 命令在這裡會很有用。
* 如果發現成本估計是錯的，同樣有兩種可能。總成本是由每個計畫節點的每筆資料列成本，乘以該計畫節點的選擇率估計值計算而得。計畫節點的估計成本可以透過執行時期參數調整（說明於[第 19.7.2 節](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)）。選擇率估計不準確，則是由於統計資訊不足。或許可以藉由調校統計資訊收集參數來改善這一點（請參閱 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md)）。

  如果你無法成功地將成本調整得更合適，那麼可能就只能明確地強制使用索引。你也可以聯絡 PostgreSQL 開發人員來檢視這個問題。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-examine.html)（原文版本：18.6；核對日期：2026-09-11）
