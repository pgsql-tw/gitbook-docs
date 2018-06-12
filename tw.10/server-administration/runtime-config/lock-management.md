---
description: 版本：10
---

# 19.12. 交易鎖定管理

`deadlock_timeout` \(`integer`\)

這是查看是否存在交易鎖定鎖死情況之前，所等待的時間量（以毫秒為單位）。檢查鎖死是相對昂貴的，所以伺服器在每次等待鎖定時都不會執行這個動作。我們樂觀地認為鎖死在產品應用程式中並不常見，所以在檢查鎖死之前等待鎖定一段時間。增加此值可減少無謂的鎖死檢查所浪費的時間，但會減慢真正鎖死錯誤的回報速度。預設值是 1 秒，這可能是您實際需要的最小值。 在負載很重的伺服器上，您可能需要提升一些。理想情況下，此設定應該超過您典型的交易時間，以便提高在伺服器決定檢查鎖死之前鎖定就被解除的可能性。只有超級使用者可以變更此設定。

當設定 [log\_lock\_waits ](logging.md#19-8-3-what-to-log)時，此參數還會確定在發出有關鎖定等待的日誌消息之前需要等待的時間長度。如果您試圖查看鎖定延遲，則可能需要設定比正常情況更短的 deadlock\_timeout。

`max_locks_per_transaction` \(`integer`\)

The shared lock table tracks locks on `max_locks_per_transaction` \* \([max\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) + [max\_prepared\_transactions](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PREPARED-TRANSACTIONS)\) objects \(e.g., tables\); hence, no more than this many distinct objects can be locked at any one time. This parameter controls the average number of object locks allocated for each transaction; individual transactions can lock more objects as long as the locks of all transactions fit in the lock table. This is _not_ the number of rows that can be locked; that value is unlimited. The default, 64, has historically proven sufficient, but you might need to raise this value if you have queries that touch many different tables in a single transaction, e.g. query of a parent table with many children. This parameter can only be set at server start.

When running a standby server, you must set this parameter to the same or higher value than on the master server. Otherwise, queries will not be allowed in the standby server.

`max_pred_locks_per_transaction` \(`integer`\)

The shared predicate lock table tracks locks on `max_pred_locks_per_transaction` \* \([max\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) + [max\_prepared\_transactions](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PREPARED-TRANSACTIONS)\) objects \(e.g., tables\); hence, no more than this many distinct objects can be locked at any one time. This parameter controls the average number of object locks allocated for each transaction; individual transactions can lock more objects as long as the locks of all transactions fit in the lock table. This is _not_ the number of rows that can be locked; that value is unlimited. The default, 64, has generally been sufficient in testing, but you might need to raise this value if you have clients that touch many different tables in a single serializable transaction. This parameter can only be set at server start.

`max_pred_locks_per_relation` \(`integer`\)

This controls how many pages or tuples of a single relation can be predicate-locked before the lock is promoted to covering the whole relation. Values greater than or equal to zero mean an absolute limit, while negative values mean [max\_pred\_locks\_per\_transaction](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-TRANSACTION) divided by the absolute value of this setting. The default is -2, which keeps the behavior from previous versions of PostgreSQL. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`max_pred_locks_per_page` \(`integer`\)

This controls how many rows on a single page can be predicate-locked before the lock is promoted to covering the whole page. The default is 2. This parameter can only be set in the `postgresql.conf` file or on the server command line.  


