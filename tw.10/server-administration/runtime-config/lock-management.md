---
description: 版本：10
---

# 19.12. 交易鎖定管理

#### `deadlock_timeout` \(`integer`\)

這是查看是否存在交易鎖定鎖死情況之前，所等待的時間量（以毫秒為單位）。檢查鎖死是相對昂貴的，所以伺服器在每次等待鎖定時都不會執行這個動作。我們樂觀地認為鎖死在產品應用程式中並不常見，所以在檢查鎖死之前等待鎖定一段時間。增加此值可減少無謂的鎖死檢查所浪費的時間，但會減慢真正鎖死錯誤的回報速度。預設值是 1 秒，這可能是您實際需要的最小值。 在負載很重的伺服器上，您可能需要提升一些。理想情況下，此設定應該超過您典型的交易時間，以便提高在伺服器決定檢查鎖死之前鎖定就被解除的可能性。只有超級使用者可以變更此設定。

當設定 [log\_lock\_waits ](logging.md#19-8-3-what-to-log)時，此參數還會確定在發出有關鎖定等待的日誌消息之前需要等待的時間長度。如果您試圖查看鎖定延遲，則可能需要設定比正常情況更短的 deadlock\_timeout。

#### `max_locks_per_transaction` \(`integer`\)

共享鎖定資料表追踪 max\_locks\_per\_transaction \*（[max\_connections](connections-and-authentication.md#19-3-1-ding) + [max\_prepared\_transactions](resource-consumption.md#19-4-1-memory)）個物件（例如資料表）上的交易鎖定；因此，在任何時候都可以鎖定許多不同的物件。 此參數控制為每個交易事務分配的平均對象鎖數量; 只要所有交易的鎖定符合鎖定資料表，個別交易就可以鎖定更多的對象。 這不是可以鎖定的資料列數；該值是無限的。預設值 64 在歷史上證明是足夠的，但如果在單個交易事務中有許多不同資料表的查詢，則可能需要提高此值。例如有很多子資料表的父資料表的查詢。此參數只能在伺服器啟動時設定。

運行備用伺服器時，必須將此參數設定為與主服務器上相同或更高的值。 否則，查詢將不被允許在備用伺服器中。

#### `max_pred_locks_per_transaction` \(`integer`\)

共享的 predicate lock 資料表追踪 max\_pred\_locks\_per\_transaction \*（[max\_connections](connections-and-authentication.md#19-3-1-ding) + [max\_prepared\_transactions](resource-consumption.md#19-4-1-memory)）個物件（例如資料表）上的交易鎖定；因此，在任何時候不會有比這個數字更多的物件被鎖定。此參數控制為每個交易事務分配的平均物件鎖定的數量；只要所有交易的鎖定符合鎖定資料表，個別交易就可以鎖定更多的物件。不是可以鎖定的資料列數；該值是無限的。預設值 64 通常在測試中足夠了，但如果您的用戶端在單個可序列化交易事務中觸及許多不同的資料表，您可能需要提高此值。此參數只能在伺服器啟動時設定。

#### `max_pred_locks_per_relation` \(`integer`\)

這可以控制在鎖定被提升為鎖定整個關連之前，單個關連的多少個 page 或 tuple 可以被 predicate-lock。大於或等於零的值表示絕對限制，而負值表示 [max\_pred\_locks\_per\_transaction](lock-management.md#max_pred_locks_per_transaction-integer) 除以此設定的絕對值。預設值是 -2，它保留了先前版本 PostgreSQL 的行為。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

`max_pred_locks_per_page` \(`integer`\)

這可以控制在將鎖定升級為覆蓋整個 page 之前，單個 page 上有多少資料列可以 predicate-locked。 預設值是 2。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。  


