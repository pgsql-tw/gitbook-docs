# 25.1. 例行性資料清理

PostgreSQL 資料庫需要定期維護，稱為資料庫清理\(vacuum\)。 對於一裝的執行環境而言，透過 autovacuum 背景程序進行資料庫清理就足夠了，這在 [24.1.6 節](routine-vacuuming.md#24-1-6-the-autovacuum-daemon)中有描述。您可能需要調整其中所描述的自動清除參數，以獲得您的情況的最佳結果。 一些資料庫管理員希望用手動管理的 VACUUM 命令來補充或替換背景程序的活動，這些命令通常根據 cron 或 Task Scheduler 的腳本計劃執行。 要正確設定手動管理的資料庫清理，了解接下來幾小節中討論的問題至關重要。依靠自動清理的管理員可能仍然希望瀏覽這些內容以幫助他們理解和調整自動清理。

## 25.1.1. 資料庫清理的基本概念

必須以 PostgreSQL [VACUUM](../../reference/sql-commands/vacuum.md) 命令處理每個資料表，原因如下：

1. 恢復或回收使用因更新或刪除資料列所佔用的磁碟空間。
2. 更新 PostgreSQL 查詢計劃器使用的資料統計資訊。
3. 更新可視性結構，這會增加[索引限定掃描](../../the-sql-language/index/index-only-scans-and-covering-indexes.md)的效率。
4. 防止由於事務 ID 重覆或 multixact ID 重覆而失去非常舊的資料。

這些原因中的每一個都會要求執行不同頻率和範圍的 VACUUM 操作，如以下小節所述。

VACUUM 有兩種執行方式：標準 VACUUM 和 VACUUM FULL。VACUUM FULL 可以回收更多磁碟空間，但執行速度要慢得多。而且，VACUUM 的標準形式可以與線上資料庫同時運作。（SELECT、INSERT、UPDATE 和 DELETE 等指令將繼續正常工作，但在 VACUUM FULL 時，您將無法使用諸如 ALTER TABLE 之類的指令修改資料表的定義。）VACUUM FULL 需要獨占鎖定它正在處理的資料表，因此無法與其他資料表的使用同時進行。因此，一般來說，管理員應該努力使用一般的 VACUUM 而避免進行 VACUUM FULL。

VACUUM 會產生大量的 I/O流量，這會導致其他正在進行的連線效能較差。有一些配置參數可以調整以減少背景資料庫清理對效能的影響 - 參閱[第 19.4.4 節](../server-configuration/resource-consumption.md#19-4-4-cost-based-vacuum-delay)`。`

## 25.1.2. 回收磁碟空間

在 PostgreSQL 中，資料列的 UPDATE 或 DELETE 不會立即刪除該資料列的舊版本。這種方法對於獲得多版本平行控制（MVCC，參閱[第 13 章](../../the-sql-language/concurrency-control/)）的好處是必要的：資料列的版本不能被刪除，而其他事務仍然可以看到。 但最終，過時或刪除的資料列版本不再讓任何交易感興趣。它佔用的空間必須被新的資料列重新使用以避免無限增長的磁碟空間需求。這就是透過執行 VACUUM 來完成的。

VACUUM 的標準作法是移除資料表和索引中過時的資料列版本，並標記可供將來重複使用的空間。 但是，除非資料表末端的一個或多個頁面變為完全空閒並且可以輕鬆獲取排他資料表鎖定的特殊情況，否則它不會將空間還給作業系統。相比之下，VACUUM FULL 透過寫入完整新版本使其沒有空閒的空間來主動壓縮資料表。這最大限度地減少了資料表的大小，但可能需要很長時間。 它還需要用於資料表新副本的額外磁碟空間，直到操作完成。

常態的資料庫清理通常目標是經常足夠地執行標準 VACUUM 以避免需要 VACUUM FULL。autovacuum 背景程序嘗試以這種方式工作，實際上永遠不會發出 VACUUM FULL。在這種方法中，這個想法並不是將資料表保持在最小尺寸，而是為了保持磁碟空間的穩定狀態使用：每個資料表都佔用相當於其最小尺寸的空間，再加上在 VACUUM 之間使用的空間很大，儘管可以使用 VACUUM FULL 將表縮回到最小大小並將磁碟空間還回到作業系統，但如果資料表將來會再次增長，則沒有多大意義。 因此，適度頻繁的標準 VACUUM 運行比用於維護大量更新資料表的罕見 VACUUM FULL 運行更好。

有些管理者更喜歡自己安排資料庫清理作業，例如在負載較低時在夜間進行所有工作。按照固定的時間表進行資料庫清理作業的困難在於，如果資料表在更新活動中出現意外的峰值，則可能會變得臃腫到 VACUUM FULL 真的需要回收空間。使用自動清理背景程序緩解了這個問題，因為背景程序會根據更新活動動態調度清理作業。除非您有一個非常可預測的工作量，否則完全停用該背景程序是不明智的。一個可能的折衷辦法是設定背景程序的參數，以便它僅對異常繁重的更新活動作出反應，從而避免事情失控，而預定的 VACUUM 參數是能在典型的情況下完成大部分工作。

對於那些不使用自動清理的人來說，一種典型的方法是在低使用期內每天安排一次資料庫範圍內的 VACUUM，並根據需要更頻繁地清空大量更新的資料表。（一些具有極高更新率的設定每隔幾分鐘就會清理一次最繁忙的資料表，如此頻繁。）如果叢集中有多個資料庫，請不要忘記每個資料庫都有 VACUUM；[vacuumdb](../../reference/client-applications/vacuumdb.md) 工作可能會有所幫助。

{% hint style="info" %}
當一個資料表由於大量更新或刪除活動而包含大量過時資料列版本時，一般的 VACUUM 可能不能令人滿意。如果您有這樣一個資料表並且您需要回收佔用的多餘磁碟空間，則需要使用 VACUUM FULL 或 [CLUSTER](../../reference/sql-commands/cluster.md) 或一些 [ALTER TABLE](../../reference/sql-commands/alter-table.md) 的資料表重寫的方式。這些命令重寫整個資料表的新副本並為其建構新的索引。所有這些執行選項都需要獨占鎖定。請注意，它們也需要暫時使用大約等於一倍資料表大小的額外磁碟空間，因為資料表和索引的舊副本只有在新資料表完成後才能完全釋放。
{% endhint %}

{% hint style="info" %}
如果您有一張定期刪除整個內容的資料表，請考慮使用 TRUNCATE 而不是使用 DELETE 和 VACUUM。[TRUNCATE](../../reference/sql-commands/truncate.md) 會立即刪除資料表的全部內容，而不需要後續的 VACUUM 或 VACUUM FULL 來回收現在未使用的磁碟空間。缺點是違反了嚴格的 MVCC 意義。
{% endhint %}

## 25.1.3. 更新規劃器統計資訊

PostgreSQL 查詢規劃器依賴於關於表格內容的統計資訊，以便為查詢産生良好的查詢計劃。這些統計資訊由 [ANALYZE](../../reference/sql-commands/analyze.md) 指令收集，該指令可以單獨呼叫，也可以作為 VACUUM 中的選擇性的使用。有足夠準確的統計數據非常重要，糟糕的計劃選擇可能會降低資料庫效能。PostgreSQL 查詢規劃器依賴於關於表格內容的統計資訊，以便為查詢産生良好的查詢計劃。這些統計資訊由 ANALYZE 指令收集，該指令可以單獨呼叫，也可以作為 VACUUM 中的選擇性的使用。有足夠準確的統計數據非常重要，糟糕的計劃選擇可能會降低資料庫效能。

autovacuum 背景程序（如果啟用的話）會在資料表內容發生相當的變化時自動發出 ANALYZE 指令。但是，管理員可能更喜歡依靠手動調度的 ANALYZE 操作，尤其是如果知道資料表上的更新活動不會影響「有興趣的」欄位的統計信息。背景程序嚴格按照插入或更新的資料列數的安排 ANALYZE；不過它並不知道這是否會導致有意義的統計變化。

與資料清理恢復空間一樣，頻繁更新統計數據對於大量更新的資料表比對很少更新的資料表更有用。但即使對於大量更新的資料表，如果資料的統計分佈變化不大，也可能不需要進行統計更新。一個簡單的經驗法則是考慮資料表中欄位的最小值和最大值的變化。例如，包含行更新時間的 timestamp 欄在插入和更新資料列時會不斷增加最大值；這樣的欄位可能需要更頻繁的統計更新，而不是包含網頁內容的網址欄位。URL 欄位可能會經常收到更新，但其內容的統計分佈可能變化比較慢。

可以在特定的資料表上執行 ANALYZE，甚至可以在資料表中特定的欄位上執行ANALYZE，因此如果應用程序需要，可以更靈活地更新某些統計資訊。然而，在實務上，通常最好僅分析整個資料庫，因為這是一種快速操作。ANALYZE 以資料表中資料列的隨機抽樣而不是讀取每一個資料列。

{% hint style="info" %}
儘管 ANALYZE 頻率對每個欄位的調整可能效率不高，但您可能會發現值得對 ANALYZE 統計資訊的詳細程度進行每個欄位調整。在 WHERE 子句中大量使用且具有高度不規則資料分佈的欄位可能需要比其他欄位更精細的資料直方圖。請參閱 ALTER TABLE SET STATISTICS，或使用 [default\_statistics\_target](../server-configuration/query-planning.md#19-7-4-other-planner-options) 組態參數變更資料庫層級的預設值。
{% endhint %}

此外，預設情況下，有關 SELECT 函數的訊息有限。但是，如果建立使用函數呼叫的表示式索引，則會收集有關該函數的有用統計訊息，這可以極大地改進使用表示式索引的查詢計劃。

{% hint style="info" %}
autovacuum 背景程序不會為外部資料表發出 ANALYZE 指令，因為它無法確定可能有用的頻率。如果您的查詢需要統計外部資料表的正確計劃，最好在適當的時間表上執行手動管理的 ANALYZE 指令。
{% endhint %}

## 25.1.4. 更新可見性映射表（Visibility Map）

Vacuum 為每個資料表維護一個[可見性映射表（Visibility Map）](../../internals/database-physical-storage/visibility-map.md)，以追踪哪些頁面包含對所有進行中事務（以及所有未來事務，直到頁面再次被修改）可見的 tuple。這有兩個目的，首先，資料庫清理本身可以在下一次運行中跳過這些頁面，因為沒有什麼要清理的。

其次，它允許 PostgreSQL [僅使用索引](../../the-sql-language/index/index-only-scans-and-covering-indexes.md)來回應某些查詢，而無需參考基本資料表。 由於 PostgreSQL 索引不包含 tuple 的可見性資訊，因此普通的索引掃描會取得每個匹配索引項目的 heap tuple，以檢查目前事務是否應該看到它。另一方面，僅索引掃描首先檢查可見性映射表。如果知道頁面上的所有 tuple 都可見，則可以跳過 heap 取回。這對於可見性映射表可以防止磁碟存取的大型資料集非常有用。可見性映射表遠小於 heap，因此即使 heap 非常大，也可以輕鬆地進行快取。

## 25.1.5. 防止交易事務 ID 重覆

PostgreSQL 的 [MVCC](../../the-sql-language/concurrency-control/introduction.md) 交易事務處理相依於比較交易事務 ID（XID）：插入 XID 大於目前事務的 XID 的資料列版本是「未來」，則目前事務不應該是可見的。但由於事務 ID 的大小有限（32 位元），運行了很長時間（超過 40 億次事務）的叢集將遭受事務 ID 重覆：XID 計數器繞回到零，並且所有突然發生的事務在過去似乎變得是在未來 - 這意味著他們的輸出變得不可見。簡而言之，就是災難性的資料遺失。（實際上資料仍然存在，但如果你無法獲得它，那就沒意義了。）為了避免這種情況，有必要每 20 億次交易至少清理一次每個資料庫中的每個資料表。

定期清理能解決問題的原因是 VACUUM 會將資料列標記為凍結，表明它們是由過去的事務插入的，以至於插入事務的影響肯定對所有目前和未來的事務都可見。使用 modulo-232 運算比較普通 XID。這意味著對於每個普通的 XID，有20億個「較舊」的 XID 和 20 個「較新」的 XID；另一種說法是普通的 XID 空間是圓形的，沒有端點。因此，一旦使用特定的普通 XID 建立了資料列版本，無論我們在談論哪種正常的 XID，資料列版本對於接下來的 20 億次交易看起來都是“過去的”。如果資料列版本在超過 20 億次交易後仍然存在，那麼它將來會突然出現。為了防止這種情況，PostgreSQL 保留了一個特殊的 XID，FrozenTransactionId，它不遵循正常的 XID 比較規則，並且總是被認為比每個普通的 XID 都舊。凍結資料列版本被視為插入 XID 是 FrozenTransactionId，因此它們對於所有正常事務而言似乎都是「過去」而不管繞回重覆的問題，因此這些資料列版本在刪除之前有效，無論多長時間都是。

{% hint style="info" %}
在 9.4 之前的 PostgreSQL 版本中，透過實際用 FrozenTransactionId 替換資料列的插入 XID 來實現凍結，這在資料列的 xmin 系統欄位中是可見的。較新版本只設置一個指標，保留資料列的原始 xmin 以便進行可能的查證使用。但是，仍然可以在 9.4 之前版本的資料庫 pg\_upgrade 中找到 xmin 等於 FrozenTransactionId（2）的資料列。
{% endhint %}

此外，系統目錄可能包含 xmin 等於 BootstrapTransactionId\(1\) 的資料列，表示它們是在 initdb 的第一階段插入的。與 FrozenTransactionId 一樣，此特殊 XID 被視為比每個普通 XID 更舊。

[vacuum\_freeze\_min\_age](../server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang) 控制在凍結該 XID 的資料列之前 XID 值的大小。增加此設定可以避免不必要的維護工作，否則將很快再次修改否則交易事務將被凍結，但減少此設定會增加在必須再次對資料表進行清理之前可以處理的交易事務數量。

VACUUM 使用[可見性映射表](../../internals/database-physical-storage/visibility-map.md)來確定必須掃描資料表的哪些頁面。通常，它會跳過沒有任何過期資料列版本的頁面，即使這些頁面可能仍然具有舊 XID 值的資料列版本。因此，正常的 VACUUM 並不總是凍結資料表中每個舊的資料列版本。 VACUUM 會定期執行積極的清理，僅跳過既不包含過期資料列也不包含任何未凍結的 XID 或 MXID 值的頁面。[vacuum\_freeze\_table\_age](../server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang) 控制 VACUUM 何時執行此操作：如果自上次此類掃描以來已經處理過的事務數量大於 vacuum\_freeze\_table\_age 減去 vacuum\_freeze\_min\_age，則掃描全部可見但未全部凍結的頁面。將 vacuum\_freeze\_table\_age 設定為 0 會強制 VACUUM 對所有掃描使用此更積極的策略。

資料表可以不清理的最長時間是 20 億個事務減去上次積極清理時的 vacuum\_freeze\_min\_age 值。如果它不清理超過了那個時間，可能會導致資料遺失。為確保不會發生這種情況，將在任何可能包含 XID 未滿配定參數 [autovacuum\_freeze\_max\_age ](../server-configuration/automatic-vacuuming.md)指定的年齡的未凍結資料列的資料表上呼叫autovacuum。（即使禁用 autovacuum，也會執行這個動作。）

這意味著如果資料表沒有以其他方式進行清理，則每次 autovacuum\_freeze\_max\_age 減去 vacuum\_freeze\_min\_age 的事務數量時，將在其上執行 autovacuum。對於經常用於空間回收目的而被清理的資料表，這一點並不重要。但是，對於靜態資料表（包括接收插入但沒有更新或刪除的資料表），不需要清理進行空間回收，因此嘗試最大化非常大的靜態資料表上強制自動清理之間的間隔會很有用。顯然，可以透過增加 autovacuum\_freeze\_max\_age 或減少 vacuum\_freeze\_min\_age 來達到此目的。

vacuum\_freeze\_table\_age 的有效最大值為 0.95 \* autovacuum\_freeze\_max\_age；高於此值的設定將被限制為最大值。高於 autovacuum\_freeze\_max\_age 的值是沒有意義的，因為無論如何都會在該點觸發n防止交易重疊的自動清理，並且 0.95 乘數在此之前留下一些喘息空間來執行手動 VACUUM。根據經驗，vacuum\_freeze\_table\_age 應設定為略低於 autovacuum\_freeze\_max\_age 的值，留下足夠的間隙，以便在該間隙中執行由日常刪除和更新活動觸發定期的 VACUUM 或 autovacuum。將它設定得太近可能會導致防止交易重疊的自動清理，即使該資料表最近被清理以回收空間，而較低的值還是會導致更頻繁的積極清理。

增加 autovacuum\_freeze\_max\_age（以及 vacuum\_freeze\_table\_age）的唯一缺點是資料庫叢集的 pg\_xact 和 pg\_commit\_ts 子目錄將佔用更多空間，因為它必須儲存提交狀態和（如果啟用了 track\_commit\_timestamp）所有事務的時間戳記回到 autovacuum\_freeze\_max\_age horizon。提交狀態每個交易事務使用兩個位元，因此如果 autovacuum\_freeze\_max\_age 設定為其最大允許值 20 億，則 pg\_xact 可以增長到大約 0.5 GB，pg\_commit\_ts 可以增長到大約 20 GB，這與總資料庫大小相比這是微不足道的。建議將 autovacuum\_freeze\_max\_age 設定為其最大允許值。否則，根據您願意允許 pg\_xact 和 pg\_commit\_ts 儲存的內容進行設定。（一般情況下，2 億次交易，轉換為大約 50 MB 的 pg\_xact 儲存空間和大約 2 GB 的pg\_commit\_ts 儲存空間。）

減少 vacuum\_freeze\_min\_age 的一個缺點是它可能導致 VACUUM 進行無謂的工作：如果此後很快更新資料列（導致它獲取新的 XID），凍結資料列版本會浪費時間。因此，設定應該足夠大，以至於資料列不會被凍結，直到它們不再可能更新為止。

為了追踪資料庫中最早解凍的 XID 的值，VACUUM 將 XID 統計訊息儲存在系統資料表 pg\_class 和 pg\_database 中。特別是，資料表 pg\_class 的 relfrozenxid 欄位包含該資料表的最後一個積極 VACUUM 使用的凍結截止 XID。由 XID 早於此截止 XID 的事務插入，則所有資料列都保證已被凍結。同理，資料庫的 pg\_database 的 datfrozenxid 欄位是該資料庫中出現的未凍結 XID 的下限 - 它只是資料庫中每個資料表 relfrozenxid 的最小值。檢查此訊息的便捷方法是執行以下查詢：

```text
SELECT c.oid::regclass as table_name,
       greatest(age(c.relfrozenxid),age(t.relfrozenxid)) as age
FROM pg_class c
LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relkind IN ('r', 'm');

SELECT datname, age(datfrozenxid) FROM pg_database;
```

age 欄位測量從截止 XID 到目前事務的 XID 的事務數。

VACUUM 通常僅掃描自上次清理以來已修改的頁面，但只有在掃描可能包含未凍結 XID 資料表的每個頁面時才能提升 relfrozenxid。當 relfrozenxid 超過 vacuum\_freeze\_table\_agetransactions 時，或當使用 VACUUM 的 FREEZE 選項時，又或當所有尚未全部凍結的頁面碰巧需要清理以刪除過期資料列版本時，才會發生這種情況。當 VACUUM 掃描資料表中尚未全部凍結的每個頁面時，應將 age（relfrozenxid）設定為比 vacuum\_freeze\_min\_age 設定略多一點的值（更多是自 VACUUM 啟動以來啟動的事務數量）。如果在達到 autovacuum\_freeze\_max\_age 之前沒有在資料表上發出 relfrozenxid-advance 的 VACUUM，則很快將強制執行該資料表的 autovacuum。

如果由於某種原因 autovacuum 無法從資料表中清除舊的 XID，當資料庫最舊的 XID 從重疊點到達一千萬個事務時，系統將開始發出這樣的警告消息：

```text
WARNING:  database "mydb" must be vacuumed within 177009986 transactions
HINT:  To avoid a database shutdown, execute a database-wide VACUUM in "mydb".
```

（應該按照提示的建議進行手動 VACUUM 解決問題；但請注意，VACUUM 必須由超級使用者執行，否則它將無法處理系統目錄，就無法推進資料庫的 datfrozenxid。）這些警告如果被忽略，系統將關閉並拒絕啟動任何新的事務，一旦剩下的事務 XID 在重疊前少於 100 萬：

```text
ERROR:  database is not accepting commands to avoid wraparound data loss in database "mydb"
HINT:  Stop the postmaster and vacuum that database in single-user mode.
```

透過手動執行所需的 VACUUM 命令，可以讓管理員在沒有資料遺失的情況下恢復 100 萬個事務安全邊界。但是，由於系統一旦進入安全關閉模式就不會執行命令，唯一的方法是停止伺服器並以單一使用者模式啟動伺服器再執行 VACUUM。在單一使用者模式下不會強制執行關閉。有關使用單一使用者模式的詳細訊息，請參閱 [postgres](../../reference/server-applications/postgres.md) 參考頁面。

### **25.1.5.1. Multixacts and Wraparound**

Multixact ID 用於支援多個事務的資料列鎖定。由於 tuple 標頭中只有有限的空間來儲存鎖定訊息，因此只要有多個事務同時鎖定一個資料列，該訊息就會被編碼為“multiple transaction ID”或簡稱 Multixact ID。 有關哪些事務 ID 包含在任何特定 multixact ID 中的訊息將單獨儲存在 pg\_multixact 目錄中，並且只有 multixact ID 出現在 tuple 標頭中的 xmax 字串中。與事務 ID 一樣，multixact ID 實作為 32 位元計數器和相對應的儲存，所有這些都需要仔細的存續管理，儲存清理和環繞處理。有一個單獨的儲存區域，用於保存每個 multixact 中的成員列表，該列表也使用 32 位元計數器，必須進行管理。

每當 VACUUM 掃描資料表時，它將替換任何比 [vacuum\_multixact\_freeze\_min\_age](../server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang) 更舊的多重 ID（Multixact ID），其值可以是零值，單個事務 ID 或更新的多重 ID。對於每個資料表，pg\_class.relminmxid 儲存仍出現在該資料表的任何 tuple 中的最舊的多重 ID。如果此值早於 [vacuum\_multixact\_freeze\_table\_age](../server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang)，則強制使用積極地清理。如前一節所述，積極的清理意味著只會跳過那些已知全凍結的頁面。可以在 pg\_class.relminmxid 上使用 mxid\_age\(\) 來查詢其存在時間。

無論是什麼原因導致積極的 VACUUM 掃描都能夠提升該資料表的值。最終，由於掃描了所有資料庫中的所有資料表並提升了其最舊的 multixact 值，因此可以移除舊的 multixacts 的磁碟儲存。

作為安全設備，對於 multixact-age 大於 [autovacuum\_multixact\_freeze\_max\_age](../server-configuration/automatic-vacuuming.md) 的任何資料表，都將進行積極的清理掃描。如果使用的成員儲存空間量超過可定址儲存空間的 50％，那麼對於所有資料表，從具有最早的 multixact-age 的那些開始，也將逐步進行積極的清理掃描。即使名義上停用了 autovacuum，也會發生這兩種積極性掃描。

## 25.1.6. Autovacuum 背景程序

PostgreSQL 有一個選用但強烈推薦的 autovacuum 功能，其目的是自動執行 VACUUM 和 ANALYZE 指令。啟用後，autovacuum 將檢查已插入、更新或刪除大量 tuple 的資料表。這些檢查使用統計資訊收集工具；因此，除非將 [track\_counts](../server-configuration/run-time-statistics.md#19-9-1-query-and-index-statistics-collector) 設定為 true，否則無法使用 autovacuum。在預設配置中，啟用 autovacuuming 並相對應地設定相關的配置參數。

「autovacuum 背景程序」實際上由多個程序所組成。有一個主控的背景程序，稱為 autovacuum 啟動程序，負責啟動所有資料庫的 autovacuum 工作程序。啟動程序將跨時間分配工作，嘗試在每個 [autovacuum\_naptime](../server-configuration/automatic-vacuuming.md) 秒內啟動每個資料庫中的一個工作程序。（因此，如果安裝 N 個資料庫，則每個 autovacuum\_naptime / N 秒將啟動一個新工作程序。）允許最多同時運行 [autovacuum\_max\_workers](../server-configuration/automatic-vacuuming.md) 工作程序。如果要處理的 autovacuum\_max\_workers 資料庫不止一個，則第一個工作程序完成後將立即處理下一個資料庫。每個工作程序將檢查其資料庫中的每個資料表，並根據需要執行 VACUUM 或 ANALYZE。log\_autovacuum\_min\_duration 可以設定為監控 autovacuum 工作程序的活動。

如果幾個大型資料表都有資格在短時間內進行清理，那麼所有自動清理工作程序可能會長時間針對這些資料表進行清理。這將導致其他資料表和資料庫在工作程序可用之前無法被清理。單個資料庫中可能有多少程序沒有限制，但工作程序確實會試圖避免重複已經由其他工作程序完成的工作。請注意，正在運行的 worker 的數量不計入 [max\_connections](../server-configuration/connections-and-authentication.md#19-3-1-ding) 或 [superuser\_reserved\_connections](../server-configuration/connections-and-authentication.md#19-3-1-ding) 限制。

其 relfrozenxid 值大於 autovacuum\_freeze\_max\_age 事務舊的資料表總是被清理（這也適用於那些已通過儲存參數修改了凍結最大年齡的資料表；請參閱下文）。 否則，如果自上一個 VACUUM 以來廢棄的 tuple 數超過“清理閾值（vacuum threshold）”，則對該資料表進行清理。 清理閾值的定義為：

```text
vacuum threshold = vacuum base threshold + vacuum scale factor * number of tuples
```

自動清理的基準閾值為 [autovacuum\_vacuum\_threshold](../server-configuration/automatic-vacuuming.md)，自動清理比例因子為 [autovacuum\_vacuum\_scale\_factor](../server-configuration/automatic-vacuuming.md)，tuple 數為 pg\_class.reltuples。從統計資訊收集器獲取過時 tuple 的數量；它是由每個 UPDATE 和 DELETE 操作時的半精確計數。（這只是半精確的，因為某些資訊可能會在負載較重時下遺失。）如果資料表的 relfrozenxid 值超過 vacuum\_freeze\_table\_age 時，則執行積極的清理以凍結舊 tuple 並提前 relfrozenxid；否則，僅掃描自上次清理以來已修改的頁面。

對於分析，使用類似的條件：此閾值定義為：

```text
analyze threshold = analyze base threshold + analyze scale factor * number of tuples
```

與自上次 ANALYZE 以來插入、更新或刪除的 tuple 總數進行比較。

autovacuum 無法存取臨時資料表。因此，應透過直接執行 SQL 指令進行適當的清理和分析操作。

預設閾值和比例因子來自 postgresql.conf，但可以基於每個資料表覆寫它們（以及許多其他 autovacuum 控制參數）；有關更多訊息，請參閱[儲存參數](../../reference/sql-commands/create-table.md#storage-parameters)。如果透過資料表的儲存參數變更了設定，則在處理該資料表時使用該值；否則使用全域設定。 有關全域設定的更多詳細訊息，請參閱[第 19.10 節](../server-configuration/automatic-vacuuming.md)。

當多個工作程序執行時，autovacuum 成本延遲參數（參閱[第 19.4.4 節](../server-configuration/resource-consumption.md#19-4-4-cost-based-vacuum-delay)）在所有正在執行的工作程序中是「平衡的」，因此無論實際執行的工作程序數量如何，對系統的總 I/O 影響都是相同的。但是，在平衡算法中不考慮任何處理已設定每表 autovacuum\_vacuum\_cost\_delay 或 autovacuum\_vacuum\_cost\_limit 儲存參數的資料表工作程序。

