<a id="LOGICAL-REPLICATION-ARCHITECTURE"></a>

## 29.9. 架構 [#](#LOGICAL-REPLICATION-ARCHITECTURE)

[29.9.1. 初始快照](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)

邏輯複寫的架構，與實體串流複寫類似（見[26.2.5 節](../high-availability/warm-standby.md#STREAMING-REPLICATION)）。
它是由 `walsender` 與 `apply`
程序所實作的。walsender 程序會對 WAL 啟動邏輯解碼
（說明於[第 47 章](../../server-programming/logicaldecoding/README.md)），
並載入標準的邏輯解碼輸出外掛（`pgoutput`）。
這個外掛會將從 WAL 讀取到的異動，轉換為邏輯複寫協定
（見[54.5 節](../../internals/protocol/protocol-logical-replication.md)）的格式，
並依照發布規格篩選資料。接著，資料會持續透過串流複寫協定，
傳輸給 apply 工作者，由它將資料對應到本地資料表，
並依照正確的交易順序，逐一套用各項異動。

訂閱端資料庫上的 apply 程序，一律會在
[`session_replication_role`](../runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE)
設為 `replica` 的情況下執行。這代表，在預設情況下，
觸發程序與規則不會在訂閱端上觸發。使用者可以選擇透過
[`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 指令
搭配 `ENABLE TRIGGER` 與 `ENABLE RULE`
子句，在某個資料表上啟用觸發程序與規則。

邏輯複寫的 apply 程序目前只會觸發資料列觸發程序，
不會觸發陳述式觸發程序。不過，初始的資料表同步作業，
其實作方式類似 `COPY` 指令，因此會針對
`INSERT` 同時觸發資料列與陳述式觸發程序。

<a id="LOGICAL-REPLICATION-SNAPSHOT"></a>

### 29.9.1. 初始快照 [#](#LOGICAL-REPLICATION-SNAPSHOT)

現有已訂閱資料表中的初始資料，會被建立快照，並在特殊種類 apply
程序的多個平行實例中複製。這些特殊的 apply 程序，是專門的資料表
同步工作者，會針對每個要同步的資料表各自產生一個。每個資料表
同步程序都會建立自己的複寫槽，並複製現有的資料。一旦複製完成，
該資料表的內容就會變得對其他後端可見。既有資料複製完成後，
這個工作者會進入同步模式，透過使用標準邏輯複寫，串流傳輸初始
資料複製期間所發生的任何異動，確保該資料表能與主要 apply 程序
達成同步狀態。在這個同步階段中，異動會依照它們在發布端發生的
相同順序被套用並提交。同步完成後，該資料表的複寫控制權，
會交還給主要 apply 程序，之後複寫便照常繼續進行。

### 注意

發布的
[`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
參數，只會影響哪些 DML 操作會被複寫。在複製現有資料表資料時，
初始資料同步並不會考慮這個參數。

### 注意

如果資料表同步工作者在複製期間失敗，apply 工作者會偵測到這個
失敗，並重新產生資料表同步工作者，以繼續同步程序。這項行為
確保暫時性的錯誤不會永久中斷複寫設定。另請參閱
[`wal_retrieve_retry_interval`](../runtime-config/runtime-config-replication.md#GUC-WAL-RETRIEVE-RETRY-INTERVAL)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-architecture.html)（原文版本：18.6；核對日期：2026-09-25）
