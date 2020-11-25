# 30.5. 架構

邏輯複寫透過複寫發佈者資料庫上的資料快照開始。一旦完成，發佈者的變化就會即時發送給訂閱者。訂閱者按照對發佈者進行提交的順序套用資料，以確保任何單個訂閱中的發佈的交易事務一致性。

邏輯複寫採用類似於實體的串流複寫的體系結構構建立（請參閱[第 26.2.5 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-5-streaming-replication)）。 它由「walsender」和「apply」過程實施。walsender 程序啟動 WAL 的邏輯解碼（在[第 48 章](../../server-programming/logical-decoding/)中介紹）並載入標準的邏輯解碼套件（pgoutput）。該套件將從 WAL 讀取的變更轉換為邏輯複寫協定（請參閱[第 52.5 節](../../internals/52.-frontend-backend-protocol/52.5.-logical-streaming-replication-protocol.md)），並根據發佈規範過濾資料。然後使用串流複寫協定將資料連續傳輸到 apply 程序，後者將資料映射到本地資料表並按照正確的事務順序套用收到的各個變更。

使用者資料庫上的應用程序始終在將 session\_replication\_role 設定為 replica 的情況下運行，這會對事件觸發器和限制條件會產生影響。

邏輯複寫 apply 程序當下只觸發資料列觸發器，而不觸發查詢語句觸發器。但是，初始資料表同步會像 COPY 指令一樣執行，因此會觸發 INSERT 的資料列和查詢語句觸發器。

## 31.5.1. 初始快照

現有訂閱資料表中的初始資料被快照並複寫到特殊型別的 apply 程序的平行程序中。此過程將建立自己的臨時複寫插槽並複寫現有資料。一旦複寫了現有資料，程該序便進入同步模式，透過使用標準邏輯複寫對初始資料複寫過程中發生的任何變更進行串流傳輸，確保該資料表與主應用程序處於同步狀態。同步完成後，資料表的複寫控制將回到正常複寫繼續進行的主應用程序。

