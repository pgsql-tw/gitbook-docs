<a id="ROUTINE-VACUUMING"></a>

## 24.1. 例行性資料庫清理 [#](#routine-vacuuming) <a href="#routine-vacuuming" id="routine-vacuuming"></a>

[24.1.1. 清理基本概念](routine-vacuuming.md#VACUUM-BASICS)

[24.1.2. 回收磁碟空間](routine-vacuuming.md#VACUUM-FOR-SPACE-RECOVERY)

[24.1.3. 更新規劃器統計資訊](routine-vacuuming.md#VACUUM-FOR-STATISTICS)

[24.1.4. 更新可見性映射](routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)

[24.1.5. 防止交易 ID 回捲失敗](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)

[24.1.6. Autovacuum 常駐程式](routine-vacuuming.md#AUTOVACUUM)

<a id="id-1.6.11.10.2"></a>

PostgreSQL 資料庫需要定期進行稱為*清理*（vacuuming）的維護工作。對許多安裝而言，讓 *autovacuum 常駐程式*（autovacuum daemon）負責清理就已足夠，該常駐程式的說明請參閱[第 24.1.6 節](routine-vacuuming.md#AUTOVACUUM)。你可能需要調整該節所述的 autovacuum 參數，才能針對你的情況取得最佳效果。有些資料庫管理者則希望以手動管理的
`VACUUM` 指令來補充甚至取代常駐程式的工作，這類指令通常是透過 cron 或工作排程器（Task
Scheduler）腳本依排程執行。若要正確設定手動管理的清理作業，就必須理解接下來幾個小節所討論的議題。即使是依賴 autovacuum 的管理者，也可能想略讀這部分內容，以協助理解並調整 autovacuum 的運作。

<a id="VACUUM-BASICS"></a>

### 24.1.1. 清理基本概念 [#](#VACUUM-BASICS)

PostgreSQL 的
[`VACUUM`](../../reference/sql-commands/sql-vacuum.md) 指令必須定期處理每個資料表，原因有以下幾點：

1. 回收或重複使用被更新或刪除之資料列所占用的磁碟空間。
2. 更新
   PostgreSQL 查詢規劃器所使用的資料統計資訊。
3. 更新可見性映射，藉此加速[僅索引
   掃描](../../the-sql-language/indexes/indexes-index-only-scans.md)。
4. 防止因
   *交易 ID 回捲*（transaction ID wraparound）或
   *多重交易 ID 回捲*（multixact ID wraparound）而遺失非常舊的資料。

如接下來各小節所述，這些原因各自要求以不同的頻率與範圍執行 `VACUUM` 作業。

`VACUUM` 有兩種形式：標準 `VACUUM`
與 `VACUUM FULL`。`VACUUM FULL` 能回收較多
磁碟空間，但執行速度慢得多。此外，
標準形式的 `VACUUM` 可以與正式營運中的資料庫作業並行執行。（`SELECT`、
`INSERT`、`UPDATE` 與
`DELETE` 等指令仍會照常運作，不過在資料表被清理期間，你
無法用 `ALTER TABLE` 之類的指令修改該資料表的定義。）
`VACUUM FULL` 需要對其所處理的
資料表取得 `ACCESS EXCLUSIVE` 鎖定，因此無法與該資料表的其他使用
並行進行。所以一般而言，
管理者應盡量使用標準 `VACUUM`，
避免使用 `VACUUM FULL`。

`VACUUM` 會產生大量的 I/O
流量，可能導致其他使用中的工作階段效能變差。
有一些組態參數可以調整，用來降低背景清理作業對效能的影響——請參閱
[第 19.10.2 節](../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)。

<a id="VACUUM-FOR-SPACE-RECOVERY"></a>

### 24.1.2. 回收磁碟空間 [#](#VACUUM-FOR-SPACE-RECOVERY)

<a id="id-1.6.11.10.5.2"></a>

在 PostgreSQL 中，對資料列執行
`UPDATE` 或 `DELETE` 並不會立即移除該資料列的舊版本。
採取這種做法是為了取得多版本並行控制
（MVCC，請參閱[第 13 章](../../the-sql-language/mvcc/README.md)）的好處：只要資料列版本
仍可能對其他交易可見，就不能將其刪除。但最終，過時或已刪除的資料列版本會不再受任何交易關注。這時就
必須回收其所占用的空間，供新的資料列重複使用，以避免磁碟空間需求無止境地成長。這項工作由執行 `VACUUM` 來完成。

標準形式的 `VACUUM` 會移除資料表與索引中的死亡資料列
版本，並將該空間標記為可供日後重複使用。不過，除了資料表末端有一
個或多個頁面完全變空、且能夠輕易取得資料表獨占鎖定的特殊情況之外，它並不會把
空間歸還給作業系統。相對地，`VACUUM FULL` 會主動壓實
資料表，寫出一份完全沒有死亡空間的全新資料表檔案版本。這能把資料表縮到最小，但可能要花很長時間。
而且在作業完成之前，還需要額外的磁碟空間來存放資料表的新副本。

例行性清理作業通常的目標，是夠頻繁地執行標準 `VACUUM`
，藉此避免需要用到 `VACUUM FULL`。
autovacuum 常駐程式正是嘗試以這種方式運作，而且事實上它永遠不會發出
`VACUUM FULL`。在這種做法下，目標並
不是讓資料表維持在最小大小，而是讓磁碟空間的使用維持穩定狀態：每個資料表
所占用的空間，等於其最小大小加上兩次清理之間所耗用的空間。
雖然可以用 `VACUUM FULL` 把資料表縮回
最小大小並將磁碟空間歸還給作業系統，但如果資料表未來還
會再次成長，這麼做的意義不大。因此，對於頻繁更新的資料表而言，適度頻繁地執行標準 `VACUUM`，會比偶爾執行
`VACUUM FULL` 更好。

有些管理者偏好自行排程清理作業，例如
把所有工作都安排在負載較低的夜間進行。
依固定排程執行清理作業的困難之處在於：如果某個資料表的更新活動出現非預期的暴增，它可能
膨脹到必須動用 `VACUUM FULL` 才能回收
空間的地步。使用 autovacuum 常駐程式可以緩解這個問題，因為它會依更新
活動動態排程清理作業。除非你的工作負載極度可預測，否則完全停用該常駐程式並不明智。一個可能的折衷做法，
是設定常駐程式的參數，讓它只在更新活動異常
繁重時才有反應，藉此避免情況失控，而在負載正常時，則由排定的 `VACUUM`
承擔大部分的工作。

對於不使用 autovacuum 的環境，典型的做法是在使用量較低的時段，每天
排程執行一次涵蓋整個資料庫的 `VACUUM`，
並視需要對更新頻繁的資料表加做更頻繁的清理。（有些更新率極高的安裝環境，甚至
每隔幾分鐘就會清理一次最忙碌的資料表。）如果叢集中有
多個資料庫，別忘了要對每一個都執行
`VACUUM`；[vacuumdb](../../reference/reference-client/app-vacuumdb.md) 這支程式可能會有幫助。

<a id="VACUUM-FOR-SPACE-RECOVERY-TIP"></a>

### 提示

當資料表因大量更新或刪除活動而含有大量死亡資料列版本時，
單純的 `VACUUM` 可能無法令人滿意。如果你的資料表遇到這種情況，且
需要回收它所占用的多餘磁碟空間，就需要
使用 `VACUUM FULL`，或者改用
[`CLUSTER`](../../reference/sql-commands/sql-cluster.md)
，或是
[`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 的某個資料表重寫變體。
這些指令會重寫整份資料表的全新副本，並為其建立
新索引。以上所有選項都需要
`ACCESS EXCLUSIVE` 鎖定。請注意，
由於舊版的資料表與索引在新版完成之前無法釋放，這些指令也會暫時使用大約等同於
該資料表大小的額外磁碟空間。

<a id="VACUUM-FOR-SPACE-RECOVERY-TIP-2"></a>

### 提示

如果你有一個資料表，其全部內容會定期被刪除，請考慮改用
[`TRUNCATE`](../../reference/sql-commands/sql-truncate.md)，而不是先
`DELETE` 再
`VACUUM`。`TRUNCATE` 會立即移除
資料表的全部內容，不需要接著執行
`VACUUM` 或 `VACUUM
FULL` 來回收現在已不再使用的磁碟空間。
其缺點是會違反嚴格的 MVCC 語意。

<a id="VACUUM-FOR-STATISTICS"></a>

### 24.1.3. 更新規劃器統計資訊 [#](#VACUUM-FOR-STATISTICS)

<a id="id-1.6.11.10.6.2"></a><a id="id-1.6.11.10.6.3"></a>

PostgreSQL
查詢規劃器依賴關於資料表內容的統計資訊，才能為查詢
產生良好的執行計畫。這些統計資訊是由
[`ANALYZE`](../../reference/sql-commands/sql-analyze.md) 指令蒐集的，它可以單獨呼叫，
也可以作為 `VACUUM` 的選用步驟執行。擁有相當準確的
統計資訊十分重要，否則不佳的執行計畫選擇可能會降低資料庫效能。

若啟用了 autovacuum 常駐程式，只要資料表內容變動達到一定程度，它就會自動發出
`ANALYZE` 指令。不過，若已知某資料表的更新活動不會影響「感興趣」
欄位的統計資訊，管理者可能會偏好依賴
手動排程的 `ANALYZE` 作業。常駐程式排程
`ANALYZE` 時，純粹是依插入或更新的資料列數量
而定，並不知道這是否會導致有意義的統計變化。

分割區與繼承子資料表中變動的 tuple，並不會觸發
父資料表的 analyze。如果父資料表是空的或很少變動，autovacuum 可能永遠不會處理它，
導致整個繼承體系的統計資訊都不會被蒐集。此時必須手動對父資料表
執行 `ANALYZE`，才能讓統計資訊保持最新。

與為了回收空間而清理一樣，頻繁更新統計資訊對更新頻繁的資料表
比對少更新的資料表更有用。但即使是更新頻繁的資料表，如果資料的統計分布變化不大，也可能不需要
更新統計資訊。一個簡單的經驗法則，是思考資料表中各欄位的最小值與
最大值變動了多少。舉例來說，一個記錄資料列更新時間
的 `timestamp` 欄位，會隨著資料列的新增與更新而
持續增大其最大值；這樣的欄位可能需要比某個儲存
網站存取頁面 URL 的欄位更頻繁地更新統計資訊。URL 欄位受到的變動頻率
可能一樣高，但其值的統計分布變化通常相對緩慢。

可以只針對特定資料表，甚至只針對資料表的特定
欄位執行 `ANALYZE`，因此如果你的應用程式需要，可以有彈性地讓部分
統計資訊比其他統計資訊更新得更頻繁。不過在實務上，通常最好的
做法是直接分析整個資料庫，因為這是一項快速的作業。`ANALYZE` 是以統計學上的隨機取樣方式讀取資料表的
資料列，而不是讀取每一筆資料列。

<a id="VACUUM-FOR-STATISTICS-TIP"></a>

### 提示

雖然逐欄位調整 `ANALYZE` 的執行頻率可能
效益不大，但你可能會發現，逐欄位調整
`ANALYZE` 所蒐集統計資訊的詳細程度是值得的。經常用於 `WHERE`
子句、且資料分布極不規則的欄位，可能需要比其他欄位
更精細的資料直方圖。請參閱 `ALTER TABLE
SET STATISTICS`，或使用 [default_statistics_target](../runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 組態參數變更資料庫層級的預設值。

此外，在預設情況下，關於函式選擇率的資訊十分有限。
不過，如果你建立了統計物件，或是建立使用函式呼叫的運算式
索引，就會蒐集到與該函式有關的有用統計資訊，可以大幅改善使用該運算式索引的查詢
執行計畫。

<a id="VACUUM-FOR-STATISTICS-TIP-2"></a>

### 提示

autovacuum 常駐程式不會對外部資料表發出 `ANALYZE`
指令，因為它沒有辦法判斷這麼做多久一次才有用。如果你的查詢需要
外部資料表的統計資訊才能正確規劃，建議依合適的排程，對這些資料表手動執行
`ANALYZE` 指令。

<a id="VACUUM-FOR-STATISTICS-TIP-3"></a>

### 提示

autovacuum 常駐程式不會對分割資料表發出
`ANALYZE` 指令。繼承父資料表只有在其本身
發生變動時才會被分析——子資料表的變動不會觸發父資料表的 autoanalyze。如果你的查詢需要
父資料表的統計資訊才能正確規劃，就必須定期
對這些資料表手動執行 `ANALYZE`，以讓統計資訊保持最新。

<a id="VACUUM-FOR-VISIBILITY-MAP"></a>

### 24.1.4. 更新可見性映射 [#](#VACUUM-FOR-VISIBILITY-MAP)

清理作業會為每個
資料表維護一份[可見性映射](../../internals/storage/storage-vm.md)，用來追蹤哪些頁面只包含已知對所有使用中交易
（以及在該頁面再次被修改之前的所有未來交易）皆為可見的 tuple。這有兩個目的。第一，清理作業
本身可以在下一次執行時跳過這些頁面，因為沒有需要清理的內容。

第二，這讓 PostgreSQL 能夠只靠索引就回答某些
查詢，而不必參照底層資料表。由於 PostgreSQL 的
索引不包含 tuple 可見性資訊，一般的索引掃描會針對每一個符合的
索引項目取得堆積 tuple，以檢查目前交易是否應該看到它。
相對地，[*僅索引
掃描*](../../the-sql-language/indexes/indexes-index-only-scans.md)會先檢查可見性映射。
如果已知頁面上的所有 tuple 都是
可見的，就可以跳過堆積存取。這在大型資料集上特別有用，因為可見性映射可以避免磁碟存取。
可見性映射遠比堆積小得多，因此即使堆積非常龐大，它也能輕易被
快取。

<a id="VACUUM-FOR-WRAPAROUND"></a>

### 24.1.5. 防止交易 ID 回捲失敗 [#](#VACUUM-FOR-WRAPAROUND)

<a id="id-1.6.11.10.8.2"></a><a id="id-1.6.11.10.8.3"></a>

PostgreSQL 的
[MVCC](../../the-sql-language/mvcc/mvcc-intro.md) 交易語意，依賴能夠比較交易 ID（XID）
數值：若某個資料列版本的插入 XID 大於目前
交易的 XID，就代表它「在未來」，不應該
對目前交易可見。但由於交易 ID 的大小有限（32 位元），長時間運作的叢集（超過
40 億筆交易）就會遭遇*交易 ID
回捲*（transaction ID wraparound）：XID 計數器會繞回到零，於是突然間
原本屬於過去的交易看起來像是在未來——這代表它們的輸出變得不可見。簡言之，這是災難性的資料遺失。
（實際上資料仍然存在，但如果你無法存取到它，這也毫無安慰可言。）為了避免這種情況，必須至少每
20 億筆交易，就對每個資料庫中的每個資料表清理一次。

定期清理之所以能解決這個問題，原因在於
`VACUUM` 會將資料列標記為
*已凍結*（frozen），表示它們是由一個提交時間已足夠久
遠的交易所插入，因此可以確定該插入交易的效果對所有目前
與未來的交易都是可見的。
正常的 XID 是以模數 2^32 的算術方式來比較。這代表
對每一個正常 XID 而言，都有 20 億個「較舊」的 XID
以及 20 億個「較新」的 XID；換句話說，正常 XID 的空間是循環而
沒有終點的。因此，一旦某個資料列版本以某個特定的
正常 XID 建立，不論所談的是哪一個正常 XID，在接下來的 20 億筆交易之內，該資料列版本都會顯得「在過去」。如果該資料列版本
存在超過 20 億筆交易之後仍未刪除，它就會突然顯得在未來。為了
防止這種情況，PostgreSQL 保留了一個特殊的 XID，即
`FrozenTransactionId`，它不遵循一般的 XID
比較規則，且永遠被視為比任何正常 XID 都舊。
已凍結的資料列版本，會被當作其插入 XID 就是
`FrozenTransactionId` 一樣看待，因此不論回捲
問題為何，它們對所有正常交易而言都會顯得「在過去」，也因此這類資料列版本
無論存在多久，只要尚未被刪除就一律有效。

<a id="VACUUM-FOR-WRAPAROUND-NOTE"></a>

### 注意

在 9.4 之前的 PostgreSQL
版本中，凍結是透過實際將資料列的插入 XID
替換成 `FrozenTransactionId` 來實作的，這在該
資料列的 `xmin` 系統欄位中可以看得到。較新版本只是
設定一個旗標位元，保留資料列原始的 `xmin`，以供
可能的鑑識用途。不過，在從 9.4 之前版本經 pg_upgrade
而來的資料庫中，仍可能找到 `xmin` 等於
`FrozenTransactionId`（2）的資料列。

此外，系統目錄中可能會有 `xmin` 等於
`BootstrapTransactionId`（1）的資料列，表示它們是在
initdb 的第一階段插入的。
與 `FrozenTransactionId` 一樣，這個特殊 XID 也被視為比任何正常 XID
都舊。

[vacuum_freeze_min_age](../runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-MIN-AGE)
控制的是，帶有某個 XID 值的資料列，其 XID 必須舊到什麼程度才會被
凍結。調高這個設定，可以在原本會被凍結的
資料列即將再次被修改時，避免不必要的工作；而
調低這個設定，則可以增加在資料表必須再次被
清理之前所能經過的交易數量。

`VACUUM` 使用[可見性映射](../../internals/storage/storage-vm.md)
來判斷資料表中哪些頁面必須被掃描。正常情況下，即使某些頁面
可能仍含有帶舊 XID 值的資料列版本，它也
會跳過不含任何死亡資料列版本的頁面。因此，一般的
`VACUUM` 不一定每次都會凍結資料表中所有的舊資料列版本。
發生這種情況時，`VACUUM` 最終就需要執行一次
*積極清理*（aggressive vacuum），將所有符合條件、尚未凍結的
XID 與 MXID 值全部凍結，包括來自全部可見但尚未全部凍結頁面的那些。

如果某個資料表累積了大量全部可見但尚未全部凍結的
頁面，一般清理可能會選擇掃描本可跳過的頁面，以
嘗試將其凍結。這麼做會減少下一次積極清理
必須掃描的頁面數量。這類頁面稱為*主動
掃描*（eagerly scanned）頁面。可以藉由調高 [vacuum_max_eager_freeze_failure_rate](../runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE)，調校主動掃描，
讓它嘗試凍結更多全部可見的頁面。即使主動
掃描已將全部可見但尚未全部凍結的頁面數量維持在最低，大多數資料表仍然
需要定期進行積極清理。不過，任何已成功被主動凍結的
頁面，在積極清理期間都可能被跳過，因此主動凍結可能可以將積極清理的額外負擔降到最低。

[vacuum_freeze_table_age](../runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-TABLE-AGE)
控制的是資料表何時會被積極清理。若自上次這類掃描以來所經過的交易數量，
超過 `vacuum_freeze_table_age` 減去
`vacuum_freeze_min_age`，就會掃描所有全部可見但尚未全部凍結的
頁面。將
`vacuum_freeze_table_age` 設為 0，會強制 `VACUUM` 一律
使用積極策略。

資料表能夠不被清理的最長時間，是 20 億筆
交易減去上一次積極清理時的
`vacuum_freeze_min_age` 值。如果超過這段時間
仍未清理，就可能導致資料遺失。為確保不會發生這種情況，只要
資料表可能含有 XID 舊於組態參數 [autovacuum_freeze_max_age](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 所指定年齡的未凍結資料列，就會對該資料表啟動 autovacuum。（即使
停用了 autovacuum，這種情況仍會發生。）

這意味著，如果某個資料表沒有以其他方式被
清理，autovacuum 大約每經過
`autovacuum_freeze_max_age` 減去
`vacuum_freeze_min_age` 筆交易，就會對它啟動一次。
對於為了回收空間而定期被清理的資料表來說，
這一點不太重要。不過，對於靜態資料表
（包括只接受插入、沒有更新或刪除的資料表），並不需要為了
回收空間而清理，因此對於非常大的靜態資料表，嘗試將強制 autovacuum
之間的間隔拉到最大會很有用。顯然可以透過調高
`autovacuum_freeze_max_age` 或調低
`vacuum_freeze_min_age` 來達成這一點。

`vacuum_freeze_table_age` 的有效上限是 0.95 \*
`autovacuum_freeze_max_age`；設定高於此值時會被限制在此
上限。設得比
`autovacuum_freeze_max_age` 還高並不合理，因為到了那個時間點，防回捲
autovacuum 無論如何都會被觸發，而 0.95 這個乘數則保留了一些
餘裕，讓你能在那之前手動執行
`VACUUM`。經驗法則是，
`vacuum_freeze_table_age` 應設定為略低於
`autovacuum_freeze_max_age` 的值，留出足夠的間隔，讓定期排程的
`VACUUM` 或由正常刪除、更新活動觸發的
autovacuum 能在該時間窗內執行。設得太接近，可能導致即使資料表最近才為了回收空間而
被清理過，仍會觸發防回捲 autovacuum；而設得較低，則會導致更
頻繁的積極清理。

調高 `autovacuum_freeze_max_age`
（以及隨之調高的 `vacuum_freeze_table_age`）的唯一缺點，是
資料庫叢集的 `pg_xact` 與 `pg_commit_ts`
子目錄會占用更多空間，因為它們必須儲存回溯到
`autovacuum_freeze_max_age` 這個時間界線為止、所有交易的提交狀態
（以及在啟用 `track_commit_timestamp` 時的
時間戳記）。提交狀態每筆交易使用兩個位元，所以如果
將 `autovacuum_freeze_max_age` 設為其允許的最大值
20 億，`pg_xact` 預期會成長到大約半個 GB，而
`pg_commit_ts` 則約為 20GB。如果相較於
你的資料庫總大小，這樣的空間微不足道，
建議將 `autovacuum_freeze_max_age` 設為其允許的最大值。否則，就依你願意讓 `pg_xact` 與
`pg_commit_ts` 使用多少儲存空間來設定。
（預設值 2 億筆交易，換算下來大約是 50MB
的 `pg_xact` 儲存空間，以及約 2GB 的 `pg_commit_ts`
儲存空間。）

調低 `vacuum_freeze_min_age` 的一個缺點，是可能
導致 `VACUUM` 做無用的工作：如果資料列
在被凍結後不久就被修改（因而取得新的 XID），那麼凍結該資料列
版本就是在浪費時間。因此該設定值應該大到足以讓資料列在不太可能
再變動之前都不會被凍結。

為了追蹤資料庫中最舊未凍結 XID 的年齡，
`VACUUM` 會將 XID
統計資訊儲存在系統資料表 `pg_class` 與
`pg_database` 中。具體來說，
資料表在 `pg_class` 中對應資料列的
`relfrozenxid` 欄位，記錄的是最近一次成功推進
`relfrozenxid` 的 `VACUUM`（通常是最近一次
積極 VACUUM）結束時，所剩下最舊的未凍結
XID。同樣地，資料庫在
`pg_database` 中對應資料列的
`datfrozenxid` 欄位，則是該資料庫中出現之未凍結 XID
的下界——它就是該資料庫內各資料表
`relfrozenxid` 值的最小值。
要檢視這項資訊，一個方便的方式是執行如下查詢：

```

SELECT c.oid::regclass as table_name,
       greatest(age(c.relfrozenxid),age(t.relfrozenxid)) as age
FROM pg_class c
LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relkind IN ('r', 'm');

SELECT datname, age(datfrozenxid) FROM pg_database;
```

`age` 欄位量測的是，從門檻 XID 到目前
交易 XID 之間所經過的交易數量。

<a id="VACUUM-FOR-WRAPAROUND-TIP"></a>

### 提示

當 `VACUUM` 指令指定了 `VERBOSE`
參數時，`VACUUM` 會印出
關於該資料表的各項統計資訊。其中包括
`relfrozenxid` 與
`relminmxid` 如何推進，以及
新凍結頁面的數量等資訊。當 autovacuum 記錄功能（由 [log_autovacuum_min_duration](../runtime-config/runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION) 控制）針對由
autovacuum 執行的
`VACUUM` 作業回報時，伺服器日誌中也會出現相同的細節。

雖然 `VACUUM` 主要掃描的是自上次
清理以來已被修改的頁面，但它也可能主動掃描一些
全部可見但尚未全部凍結的頁面，嘗試將其凍結；不過，
只有在資料表中所有可能含有未凍結 XID 的頁面都被掃描過之後，
`relfrozenxid` 才會被推進。
這會發生在以下情況：
`relfrozenxid` 已超過
`vacuum_freeze_table_age` 筆交易之久、使用了
`VACUUM` 的 `FREEZE` 選項，或所有
尚未全部凍結的頁面恰好都
需要清理以移除死亡資料列版本。當 `VACUUM`
掃描過資料表中所有尚未全部凍結的頁面時，它應該
會將 `age(relfrozenxid)` 設為略高於所使用之
`vacuum_freeze_min_age` 設定值
（高出的部分，是 `VACUUM` 開始執行後所啟動的
交易數量）。`VACUUM`
會將 `relfrozenxid` 設為資料表中剩餘的最舊 XID，
因此最終值有可能遠比嚴格要求的更新。
如果在達到 `autovacuum_freeze_max_age` 之前，該
資料表都沒有執行過能推進 `relfrozenxid` 的
`VACUUM`，很快就會對該資料表強制執行一次 autovacuum。

如果由於某些原因，autovacuum 未能清除資料表中的舊 XID，那麼
當資料庫最舊的 XID 距離回捲點只剩四千萬筆交易時，系統就會開始發出如下的警告
訊息：

```

WARNING:  database "mydb" must be vacuumed within 39985967 transactions
HINT:  To avoid XID assignment failures, execute a database-wide VACUUM in that database.
```

（如提示所建議，手動執行 `VACUUM` 應該
能解決這個問題；但請注意，該
`VACUUM` 應由超級使用者執行，否則它將
無法處理系統目錄，因而無法推進資料庫的
`datfrozenxid`。）
如果忽略這些警告，一旦距離回捲只剩不到三百萬筆交易，系統就會拒絕指派新的 XID：

```

ERROR:  database is not accepting commands that assign new transaction IDs to avoid wraparound data loss in database "mydb"
HINT:  Execute a database-wide VACUUM in that database.
```

在這種情況下，任何已經在進行中的交易都可以繼續，
但只能啟動唯讀交易。任何會
修改資料庫記錄或截斷關聯的操作都會失敗。
`VACUUM` 指令仍然可以正常執行。
請注意，與早期版本有時建議的做法相反，
為了恢復正常運作，並不需要、也不建議停止 postmaster 或進入單使用
者模式。請改為依循以下步驟：

1. 解決舊的已備妥交易（prepared transaction）。你可以透過檢查
   [`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md) 中
   `age(transactionid)` 很大的資料列來找出這些交易。這類交易
   應該被提交或復原（rollback）。
2. 結束執行時間過長的開啟中交易。你可以透過檢查
   [`pg_stat_activity`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW) 中
   `age(backend_xid)` 或 `age(backend_xmin)` 很大的資料列來找出這些交易。這類交易
   應該被提交或復原，或者可以用 `pg_terminate_backend` 終止該工作階段。
3. 移除任何舊的複寫插槽（replication slot）。使用
   [`pg_replication_slots`](../../internals/views/view-pg-replication-slots.md) 來
   找出 `age(xmin)` 或 `age(catalog_xmin)`
   很大的插槽。在許多情況下，這類插槽是為了複寫到已不存在、或已停機很長時間
   的伺服器而建立的。如果你移除的插槽所對應的伺服器仍然存在，且可能仍會嘗試連接到該插槽，那麼該複本可能
   需要重建。
4. 在目標資料庫中執行 `VACUUM`。涵蓋整個資料庫的
   `VACUUM` 是最簡單的做法；為了縮短所需時間，也可以
   對 relfrozenxid 最舊的資料表手動發出 `VACUUM` 指令（原文此處寫作 `relminxid`，但 pg_class 中追蹤資料表最舊未凍結 XID 的欄位是 relfrozenxid，此為原文誤植）。
   在這種情況下請不要使用 `VACUUM FULL`，
   因為它需要一個 XID，因此除非在超級使用者模式下，否則它會失敗；而在超級使用者
   模式下，它反而會消耗一個 XID，進而增加交易 ID
   回捲的風險。也不要使用 `VACUUM FREEZE`，因為它做的
   工作會超出恢復正常運作所需的最低限度。
5. 一旦恢復正常運作，請確保目標資料庫中的 autovacuum 已正確設定，
   以避免未來再次發生問題。

<a id="VACUUM-FOR-WRAPAROUND-NOTE-2"></a>

### 注意

在較早的版本中，有時必須停止 postmaster，並在單使用者模式下對資料庫執行
`VACUUM`。在典型情境下，這已
不再需要，也應盡量避免，因為這會使系統停機。這麼做
風險也更高，因為它會停用旨在防止資料遺失的交易 ID 回捲防護
機制。在這種情況下，使用單使用者模式的唯一理由，是你想要
`TRUNCATE` 或 `DROP` 不需要的
資料表，以避免需要對它們執行 `VACUUM`。留有
三百萬筆交易的安全餘裕，正是為了讓管理者能夠這麼做。關於使用單使用者模式的詳情，請參閱
[postgres](../../reference/reference-server/app-postgres.md) 參考頁面。

<a id="VACUUM-FOR-MULTIXACT-WRAPAROUND"></a>

#### 24.1.5.1. 多重交易與回捲 [#](#VACUUM-FOR-MULTIXACT-WRAPAROUND)

<a id="id-1.6.11.10.8.21.2"></a><a id="id-1.6.11.10.8.21.3"></a>

*多重交易 ID*（multixact ID）用來支援多個
交易對資料列上鎖。由於 tuple 標頭中可用來儲存
鎖定資訊的空間有限，每當有超過一個交易同時對某資料列
上鎖時，這項資訊就會被編碼為「多重交易 ID」（multiple transaction ID），
簡稱 multixact ID。關於某個特定 multixact ID 包含哪些交易 ID 的
資訊，是另外儲存在
`pg_multixact` 子目錄中，只有 multixact ID
會出現在 tuple 標頭的 `xmax` 欄位中。
與交易 ID 一樣，multixact ID 也是以
32 位元計數器及對應的儲存機制實作，這一切都需要謹慎管理老化、清理
儲存空間及處理回捲問題。
另外還有一個獨立的儲存區域，用來保存每個 multixact
中的成員清單，同樣使用 32 位元計數器，也必須
加以管理。[表 9.84](../../the-sql-language/functions/functions-info.md#FUNCTIONS-PG-SNAPSHOT) 中所述的系統函式
`pg_get_multixact_members()`，可用來檢視與
某個 multixact ID 相關聯的交易 ID。

每當 `VACUUM` 掃描資料表的任何部分時，只要遇到
舊於 [vacuum_multixact_freeze_min_age](../runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE)
的 multixact ID，就會將其替換為另一個值，這個值可以是
零、一個單一交易 ID，或是一個較新的 multixact ID。對每個
資料表而言，`pg_class`.`relminmxid` 儲存的是該
資料表任一 tuple 中仍可能出現的最舊 multixact ID。
如果這個值舊於
[vacuum_multixact_freeze_table_age](../runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE)，就會強制執行
積極清理。如前一節所述，積極
清理代表只會跳過已知全部凍結的頁面。可以對
`pg_class`.`relminmxid` 使用 `mxid_age()` 來
取得其年齡。

不論觸發原因為何，積極
`VACUUM` 都*保證*能夠推進
資料表的 `relminmxid`。
最終，隨著所有資料庫中的所有資料表都被掃描過、其最舊的
multixact 值都被推進，較舊
multixact 的磁碟儲存空間就可以被移除。

作為一種安全機制，只要資料表的
multixact 年齡超過 [autovacuum_multixact_freeze_max_age](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE)，就會對該
資料表進行積極清理掃描。此外，如果
multixact 成員所占用的儲存空間超過約 10GB，所有資料表的積極清理
掃描就會更頻繁地發生，優先從
multixact 年齡最舊的資料表開始。這兩種
積極掃描，即使名義上停用了 autovacuum，也都仍會發生。成員儲存區域
最多可以成長到約 20GB，才會到達回捲。

與 XID 的情況類似，如果 autovacuum 未能清除資料表中的舊 MXID，那麼
當資料庫最舊的 MXID 距離回捲點只剩四千萬筆交易時，系統就會開始發出
警告訊息。而且，就跟 XID 的情況一樣，如果忽略這些
警告，一旦距離回捲只剩不到三百萬個 MXID，系統就會拒絕產生新的
MXID。

當 MXID 耗盡時，可以用與 XID 耗盡時大致相同的方式
恢復正常運作。請依循前一節相同的步驟，但有
以下差異：

1. 如果執行中的交易與已備妥交易不可能出現在 multixact 中，
   就可以忽略它們。
2. 與交易 ID 回捲不同，複寫插槽並不會
   直接阻礙 multixact 的清理。因此，移除過期的複寫
   插槽通常與解決 multixact ID 回捲問題無關。
3. MXID 資訊不會直接顯示在
   `pg_stat_activity` 之類的系統檢視表中；不過，尋找舊的 XID 仍然是判斷哪些
   交易造成 MXID 回捲問題的好方法。
4. XID 耗盡會阻擋所有寫入交易，但 MXID 耗盡則
   只會阻擋一部分的寫入交易，具體來說，是那些涉及
   需要 MXID 之資料列鎖定的交易。

<a id="AUTOVACUUM"></a>

### 24.1.6. Autovacuum 常駐程式 [#](#AUTOVACUUM)

<a id="id-1.6.11.10.9.2"></a>

PostgreSQL 有一項選用但強烈
建議啟用的功能，稱為 *autovacuum*，
其目的是自動執行
`VACUUM` 與 `ANALYZE` 指令。
啟用後，autovacuum 會檢查是否有
資料表發生了大量的插入、更新或刪除
tuple。這些檢查會用到統計蒐集機制；
因此，除非將 [track_counts](../runtime-config/runtime-config-statistics.md#GUC-TRACK-COUNTS) 設為 `true`，否則無法使用 autovacuum。
在預設組態中，autovacuum 是啟用的，相關組態參數也都已適當設定。

「autovacuum 常駐程式」實際上是由多個程序組成的。
其中有一個持續存在的常駐程序，稱為
*autovacuum launcher*（啟動器），負責為所有
資料庫啟動 *autovacuum worker*（工作程序）。
啟動器會將工作分散在不同時間進行，嘗試每隔 [autovacuum_naptime](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-NAPTIME)
秒，就在每個資料庫內啟動一個工作程序。（因此，如果該安裝環境有 *`N`* 個資料庫，
就會每隔
`autovacuum_naptime`/*`N`* 秒啟動一個新的工作程序。）
同一時間最多允許 [autovacuum_max_workers](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS) 個工作程序
執行。如果需要處理的資料庫數量超過
`autovacuum_max_workers`，
一旦第一個工作程序完成，就會立即開始處理下一個資料庫。
每個工作程序都會檢查其所屬資料庫中的每個資料表，
並視需要執行 `VACUUM` 及（或）`ANALYZE`。
可以設定 [log_autovacuum_min_duration](../runtime-config/runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION) 來監控
autovacuum 工作程序的活動。

如果短時間內有數個大型資料表同時符合清理條件，
所有的 autovacuum 工作程序可能會長時間都忙於清理
這些資料表。這會導致其他資料表與資料庫在有工作程序可用
之前都無法被清理。單一資料庫中可以同時有的工作
程序數量並無上限，但工作程序會盡量避免重複其他工作程序
已經完成的工作。請注意，執行中的工作程序數量並不計入 [max_connections](../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 或
[superuser_reserved_connections](../runtime-config/runtime-config-connection.md#GUC-SUPERUSER-RESERVED-CONNECTIONS) 的限制。

`relfrozenxid` 值超過 [autovacuum_freeze_max_age](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 筆交易之久
的資料表，一律會被清理（這也適用於已透過儲存
參數修改其 freeze max age 的資料表；請參閱下文）。否則，如果
自上次 `VACUUM` 以來已過時的 tuple 數量
超過「清理閾值」，該資料表就會被清理。清理閾值的
定義如下：

```

vacuum threshold = Minimum(vacuum max threshold, vacuum base threshold + vacuum scale factor * number of tuples)
```

其中，清理上限閾值（vacuum max threshold）是
[autovacuum_vacuum_max_threshold](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD)，
清理基準閾值（vacuum base threshold）是
[autovacuum_vacuum_threshold](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-THRESHOLD)，
清理比例因子（vacuum scale factor）是
[autovacuum_vacuum_scale_factor](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR)，
tuple 數量則是
`pg_class`.`reltuples`。

如果自上次清理以來插入的 tuple 數量，超過所定義的插入
閾值，該資料表也會被清理。插入閾值的定義如下：

```

vacuum insert threshold = vacuum base insert threshold + vacuum insert scale factor * number of tuples * percent of table not frozen
```

其中，插入基準閾值（vacuum insert base threshold）是
[autovacuum_vacuum_insert_threshold](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD)，
插入比例因子（vacuum insert scale factor）是
[autovacuum_vacuum_insert_scale_factor](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR)，
tuple 數量是
`pg_class`.`reltuples`，
未凍結的資料表百分比則是
`1 - pg_class.relallfrozen / pg_class.relpages`。
這類清理可能會讓資料表的部分區域被標記為
*全部可見*，也可能讓 tuple 被凍結，這
可以減少後續清理所需的工作量。
對於只接收 `INSERT` 操作，但沒有或幾乎沒有
`UPDATE`／`DELETE` 操作的資料表而言，
調低該資料表的
[autovacuum_freeze_min_age](../../reference/sql-commands/sql-createtable.md#RELOPTION-AUTOVACUUM-FREEZE-MIN-AGE) 可能會有幫助，因為這可能讓
tuple 在較早的清理中就被凍結。過時的 tuple 數量與插入的 tuple 數量，是從累計統計系統取得的；
這是一個最終一致的計數，會隨每次 `UPDATE`、
`DELETE` 與 `INSERT` 操作而更新。
如果資料表的 `relfrozenxid` 值
超過 `vacuum_freeze_table_age` 筆交易之久，
就會執行積極清理，以凍結舊 tuple 並推進
`relfrozenxid`。

對於 analyze，使用的是類似的條件：其閾值定義如下：

```

analyze threshold = analyze base threshold + analyze scale factor * number of tuples
```

會與自上次 `ANALYZE` 以來，插入、更新或刪除的 tuple
總數進行比較。

分割資料表本身並不直接儲存 tuple，因此
不會被 autovacuum 處理。（Autovacuum 確實會像處理其他資料表一樣處理資料表
分割區。）遺憾的是，這代表 autovacuum 不會對分割
資料表執行 `ANALYZE`，這可能導致參照分割資料表統計資訊的
查詢得到不理想的執行計畫。你可以在分割資料表
初次填入資料時，以及日後其分割區中資料分布
發生重大變化時，手動對分割資料表執行 `ANALYZE`，
藉此解決這個問題。

暫存資料表無法被 autovacuum 存取。因此，
適當的清理與分析作業應該透過工作階段內的 SQL 指令來
執行。

預設的閾值與比例因子取自
`postgresql.conf`，但也可以在個別資料表層級覆寫這些值
（以及許多其他 autovacuum 控制參數）；詳情請參閱
[儲存參數](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。
如果某項設定已透過資料表的儲存參數變更，處理該資料表時
就會使用該值；否則就會使用全域設定。關於全域設定的更多細節，請參閱
[第 19.10.1 節](../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)。

當有多個工作程序在執行時，autovacuum 成本延遲參數
（請參閱[第 19.10.2 節](../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)）會在所有執行中的工作程序之間「平衡」，讓
系統上的總 I/O 影響不論實際有多少工作程序
在執行都維持相同。不過，任何正在處理已個別設定
`autovacuum_vacuum_cost_delay` 或
`autovacuum_vacuum_cost_limit` 儲存參數之資料表的工作程序，
都不會被納入這個平衡演算法的考量。

Autovacuum 工作程序通常不會阻擋其他指令。如果有
程序嘗試取得與 autovacuum 所持有的
`SHARE UPDATE EXCLUSIVE` 鎖定衝突的鎖定，取得鎖定的動作就會中斷該
autovacuum。關於會衝突的鎖定模式，請參閱[表 13.2](../../the-sql-language/mvcc/explicit-locking.md#TABLE-LOCK-COMPATIBILITY)。不過，如果該 autovacuum
是為了防止交易 ID 回捲而執行（也就是說，
`pg_stat_activity` 檢視表中該 autovacuum 的查詢名稱
以 `(to prevent wraparound)` 結尾），這個
autovacuum 就不會被自動中斷。

<a id="AUTOVACUUM-WARNING"></a>

### 警告

經常執行會取得與
`SHARE UPDATE EXCLUSIVE` 鎖定衝突之鎖定的指令（例如 ANALYZE），
實際上可能導致 autovacuum 永遠無法完成。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/routine-vacuuming.html)（原文版本：18.6；核對日期：2026-10-10）
