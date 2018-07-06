---
description: 版本：10
---

# 24.1. 例行性資料清理

PostgreSQL 資料庫需要定期維護，稱為資料庫清理\(vacuum\)。 對於一裝的執行環境而言，透過 autovacuum 背景程序進行資料庫清理就足夠了，這在 [24.1.6 節](routine-vacuuming.md#24-1-6-the-autovacuum-daemon)中有描述。您可能需要調整其中所描述的自動清除參數，以獲得您的情況的最佳結果。 一些資料庫管理員希望用手動管理的 VACUUM 命令來補充或替換背景程序的活動，這些命令通常根據 cron 或 Task Scheduler 的腳本計劃執行。 要正確設定手動管理的資料庫清理，了解接下來幾小節中討論的問題至關重要。依靠自動清理的管理員可能仍然希望瀏覽這些內容以幫助他們理解和調整自動清理。

## 24.1.1. 資料庫清理的基本概念

必須以 PostgreSQL [VACUUM](../../reference/sql-commands/vacuum.md) 命令處理每個資料表，原因如下：

1. 恢復或回收使用因更新或刪除資料列所佔用的磁碟空間。
2. 更新 PostgreSQL 查詢計劃器使用的資料統計資訊。
3. 更新可視性結構，這會增加[索引限定掃描](../../the-sql-language/11.-suo-yin/11.11.-suo-yin-xian-ding-cha-xun.md)的效率。
4. 防止由於事務 ID 重覆或 multixact ID 重覆而失去非常舊的資料。

這些原因中的每一個都會要求執行不同頻率和範圍的 VACUUM 操作，如以下小節所述。

VACUUM 有兩種變形：標準 VACUUM 和 VACUUM FULL。VACUUM FULL 可以回收更多磁碟空間，但執行速度要慢得多。而且，VACUUM 的標準形式可以與產品資料庫同時操作運行。（SELECT、INSERT、UPDATE 和 DELETE 等指令將繼續正常工作，但在 VACUUM FULL 時，您將無法使用諸如 ALTER TABLE 之類的指令修改資料表的定義。）VACUUM FULL 需要獨占鎖定它正在處理的資料表，因此無法與其他資料表的使用同時進行。因此，一般來說，管理員應該努力使用標準 VACUUM 並避免VACUUM FULL。

VACUUM 會產生大量的 I/O流量，這會導致其他正在進行的連線效能較差。有一些配置參數可以調整以減少背景資料庫清理對效能的影響 - 參閱[第 19.4.4 節](../server-configuration/resource-consumption.md#19-4-4-cost-based-vacuum-delay)`。`

## 24.1.2. 恢復磁碟空間

在 PostgreSQL 中，資料列的 UPDATE 或 DELETE 不會立即刪除該資料列的舊版本。這種方法對於獲得多版本平行控制（MVCC，參閱[第 13 章](../../the-sql-language/concurrency-control/)）的好處是必要的：資料列的版本不能被刪除，而其他事務仍然可以看到。 但最終，過時或刪除的資料列版本不再讓任何交易感興趣。它佔用的空間必須被新行重新使用以避免無限增長的磁碟空間需求。這是透過執行 VACUUM 來完成的。

VACUUM 的標準作法是移除資料表和索引中過時的資料列版本，並標記可供將來重複使用的空間。 但是，除非資料表末端的一個或多個頁面變為完全空閒並且可以輕鬆獲取排他資料表鎖的特殊情況，否則它不會將空間還給作業系統。相比之下，VACUUM FULL 透過寫入完整新版本使其沒有空閒的空間來主動壓縮資料表。這最大限度地減少了資料表的大小，但可能需要很長時間。 它還需要用於資料表的新副本的額外磁碟空間，直到操作完成。

常態的資料庫清理通常目標是經常足夠地執行標準 VACUUM 以避免需要 VACUUM FULL。autovacuum 背景程序嘗試以這種方式工作，實際上永遠不會發出 VACUUM FULL。在這種方法中，這個想法並不是將資料表保持在最小尺寸，而是為了保持磁碟空間的穩定狀態使用：每個資料表都佔用相當於其最小尺寸的空間，再加上在 VACUUM 之間使用的空間很大，儘管可以使用 VACUUM FULL 將表縮回到最小大小並將磁碟空間還回到作業系統，但如果資料表將來會再次增長，則沒有多大意義。 因此，適度頻繁的標準 VACUUM 運行比用於維護大量更新資料表的罕見 VACUUM FULL 運行更好。

有些管理者更喜歡自己安排資料庫清理作業，例如在負載較低時在夜間進行所有工作。按照固定的時間表進行資料庫清理作業的困難在於，如果資料表在更新活動中出現意外的峰值，則可能會變得臃腫到 VACUUM FULL 真的需要回收空間。使用自動清理背景程序緩解了這個問題，因為背景程序會根據更新活動動態調度清理作業。除非您有一個非常可預測的工作量，否則完全停用該背景程序是不明智的。一個可能的折衷辦法是設定背景程序的參數，以便它僅對異常繁重的更新活動作出反應，從而避免事情失控，而預定的 VACUUM 參數是能在典型的情況下完成大部分工作。

對於那些不使用自動清理的人來說，一種典型的方法是在低使用期內每天安排一次資料庫範圍內的 VACUUM，並根據需要更頻繁地清空大量更新的資料表。（一些具有極高更新率的設定每隔幾分鐘就會清理一次最繁忙的資料表，如此頻繁。）如果叢集中有多個資料庫，請不要忘記每個資料庫都有 VACUUM；[vacuumdb](../../reference/ii.-postgresql-yong-hu-duan-gong-ju/vacuumdb.md) 工作可能會有所幫助。

#### 小技巧

當一個資料表由於大量更新或刪除活動而包含大量過時資料列版本時，一般的 VACUUM 可能不能令人滿意。如果您有這樣一個資料表並且您需要回收佔用的多餘磁碟空間，則需要使用 VACUUM FULL 或 [CLUSTER](../../reference/sql-commands/cluster.md) 或 [ALTER TABLE](../../reference/sql-commands/alter-table.md) 的資料表重寫變形之一。這些命令重寫整個資料表的新副本並為其構建新的索引。所有這些選項都需要獨占鎖定。請注意，它們也暫時使用大約等於資料表大小的額外磁碟空間，因為資料表和索引的舊副本只有在新資料表完成後才能完全釋放。

#### 小技巧

如果您有一張定期刪除整個內容的資料表，請考慮使用 TRUNCATE 而不是使用 DELETE 和 VACUUM。[TRUNCATE](../../reference/sql-commands/truncate.md) 會立即刪除資料表的全部內容，而不需要後續的 VACUUM 或 VACUUM FULL 來回收現在未使用的磁碟空間。缺點是違反了嚴格的 MVCC 意義。

## 24.1.3. 更新規劃器統計資訊

PostgreSQL 查詢規劃器依賴於關於表格內容的統計資訊，以便為查詢産生良好的查詢計劃。這些統計資訊由 [ANALYZE](../../reference/sql-commands/analyze.md) 指令收集，該指令可以單獨呼叫，也可以作為 VACUUM 中的選擇性的使用。有足夠準確的統計數據非常重要，糟糕的計劃選擇可能會降低資料庫效能。PostgreSQL 查詢規劃器依賴於關於表格內容的統計資訊，以便為查詢産生良好的查詢計劃。這些統計資訊由 ANALYZE 指令收集，該指令可以單獨呼叫，也可以作為 VACUUM 中的選擇性的使用。有足夠準確的統計數據非常重要，糟糕的計劃選擇可能會降低資料庫效能。

autovacuum 背景程序（如果啟用的話）會在資料表內容發生相當的變化時自動發出 ANALYZE 指令。但是，管理員可能更喜歡依靠手動調度的 ANALYZE 操作，尤其是如果知道資料表上的更新活動不會影響「有興趣的」欄位的統計信息。背景程序嚴格按照插入或更新的資料列數的安排 ANALYZE；不過它並不知道這是否會導致有意義的統計變化。

與資料清理恢復空間一樣，頻繁更新統計數據對於大量更新的資料表比對很少更新的資料表更有用。但即使對於大量更新的資料表，如果資料的統計分佈變化不大，也可能不需要進行統計更新。一個簡單的經驗法則是考慮資料表中欄位的最小值和最大值的變化。例如，包含行更新時間的 timestamp 欄在插入和更新資料列時會不斷增加最大值；這樣的欄位可能需要更頻繁的統計更新，而不是包含網頁內容的網址欄位。URL 欄位可能會經常收到更新，但其內容的統計分佈可能變化比較慢。

可以在特定的資料表上執行 ANALYZE，甚至可以在資料表中特定的欄位上執行ANALYZE，因此如果應用程序需要，可以更靈活地更新某些統計資訊。然而，在實務上，通常最好僅分析整個資料庫，因為這是一種快速操作。ANALYZE 以資料表中資料列的隨機抽樣而不是讀取每一個資料列。

#### 小技巧

儘管 ANALYZE 頻率對每個欄位的調整可能效率不高，但您可能會發現值得對 ANALYZE 統計資訊的詳細程度進行每個欄位調整。在 WHERE 子句中大量使用且具有高度不規則資料分佈的欄位可能需要比其他欄位更精細的資料直方圖。請參閱 ALTER TABLE SET STATISTICS，或使用 [default\_statistics\_target](../server-configuration/19.7.-cha-xun-gui-hua.md#19-7-4-other-planner-options) 組態參數變更資料庫層級的預設值。

此外，預設情況下，有關 SELECT 函數的訊息有限。但是，如果建立使用函數呼叫的表示式索引，則會收集有關該函數的有用統計訊息，這可以極大地改進使用表示式索引的查詢計劃。

#### 小技巧

autovacuum 背景程序不會為外部資料表發出 ANALYZE 指令，因為它無法確定可能有用的頻率。如果您的查詢需要統計外部資料表的正確計劃，最好在適當的時間表上執行手動管理的 ANALYZE 指令。

## 24.1.4. 更新可見性映射表（Visibility Map）

Vacuum 為每個資料表維護一個[可見性映射表（Visibility Map）](../../internals/database-physical-storage/visibility-map.md)，以追踪哪些頁面包含對所有進行中事務（以及所有未來事務，直到頁面再次被修改）可見的 tuple。這有兩個目的，首先，資料庫清理本身可以在下一次運行中跳過這些頁面，因為沒有什麼要清理的。

其次，它允許 PostgreSQL [僅使用索引](../../the-sql-language/11.-suo-yin/11.11.-suo-yin-xian-ding-cha-xun.md)來回應某些查詢，而無需參考基本資料表。 由於 PostgreSQL 索引不包含 tuple 的可見性資訊，因此普通的索引掃描會取得每個匹配索引項目的 heap tuple，以檢查目前事務是否應該看到它。另一方面，僅索引掃描首先檢查可見性映射表。如果知道頁面上的所有 tuple 都可見，則可以跳過 heap 取回。這對於可見性映射表可以防止磁碟存取的大型資料集非常有用。可見性映射表遠小於 heap，因此即使 heap 非常大，也可以輕鬆地進行快取。

## 24.1.5. Preventing Transaction ID Wraparound Failures

PostgreSQL's [MVCC](https://www.postgresql.org/docs/10/static/mvcc-intro.html) transaction semantics depend on being able to compare transaction ID \(XID\) numbers: a row version with an insertion XID greater than the current transaction's XID is “in the future” and should not be visible to the current transaction. But since transaction IDs have limited size \(32 bits\) a cluster that runs for a long time \(more than 4 billion transactions\) would suffer _transaction ID wraparound_: the XID counter wraps around to zero, and all of a sudden transactions that were in the past appear to be in the future — which means their output become invisible. In short, catastrophic data loss. \(Actually the data is still there, but that's cold comfort if you cannot get at it.\) To avoid this, it is necessary to vacuum every table in every database at least once every two billion transactions.

The reason that periodic vacuuming solves the problem is that `VACUUM` will mark rows as _frozen_, indicating that they were inserted by a transaction that committed sufficiently far in the past that the effects of the inserting transaction are certain to be visible to all current and future transactions. Normal XIDs are compared using modulo-232 arithmetic. This means that for every normal XID, there are two billion XIDs that are “older” and two billion that are “newer”; another way to say it is that the normal XID space is circular with no endpoint. Therefore, once a row version has been created with a particular normal XID, the row version will appear to be “in the past” for the next two billion transactions, no matter which normal XID we are talking about. If the row version still exists after more than two billion transactions, it will suddenly appear to be in the future. To prevent this, PostgreSQL reserves a special XID, `FrozenTransactionId`, which does not follow the normal XID comparison rules and is always considered older than every normal XID. Frozen row versions are treated as if the inserting XID were `FrozenTransactionId`, so that they will appear to be “in the past” to all normal transactions regardless of wraparound issues, and so such row versions will be valid until deleted, no matter how long that is.

#### Note

In PostgreSQL versions before 9.4, freezing was implemented by actually replacing a row's insertion XID with `FrozenTransactionId`, which was visible in the row's `xmin` system column. Newer versions just set a flag bit, preserving the row's original `xmin` for possible forensic use. However, rows with `xmin` equal to `FrozenTransactionId` \(2\) may still be found in databases pg\_upgrade'd from pre-9.4 versions.

Also, system catalogs may contain rows with `xmin` equal to `BootstrapTransactionId` \(1\), indicating that they were inserted during the first phase of initdb. Like `FrozenTransactionId`, this special XID is treated as older than every normal XID.

[vacuum\_freeze\_min\_age](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-VACUUM-FREEZE-MIN-AGE) controls how old an XID value has to be before rows bearing that XID will be frozen. Increasing this setting may avoid unnecessary work if the rows that would otherwise be frozen will soon be modified again, but decreasing this setting increases the number of transactions that can elapse before the table must be vacuumed again.

`VACUUM` uses the [visibility map](https://www.postgresql.org/docs/10/static/storage-vm.html) to determine which pages of a table must be scanned. Normally, it will skip pages that don't have any dead row versions even if those pages might still have row versions with old XID values. Therefore, normal `VACUUM`s won't always freeze every old row version in the table. Periodically, `VACUUM` will perform an _aggressive vacuum_, skipping only those pages which contain neither dead rows nor any unfrozen XID or MXID values. [vacuum\_freeze\_table\_age](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-VACUUM-FREEZE-TABLE-AGE) controls when `VACUUM` does that: all-visible but not all-frozen pages are scanned if the number of transactions that have passed since the last such scan is greater than `vacuum_freeze_table_age` minus `vacuum_freeze_min_age`. Setting `vacuum_freeze_table_age` to 0 forces `VACUUM` to use this more aggressive strategy for all scans.

The maximum time that a table can go unvacuumed is two billion transactions minus the `vacuum_freeze_min_age` value at the time of the last aggressive vacuum. If it were to go unvacuumed for longer than that, data loss could result. To ensure that this does not happen, autovacuum is invoked on any table that might contain unfrozen rows with XIDs older than the age specified by the configuration parameter [autovacuum\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE). \(This will happen even if autovacuum is disabled.\)

This implies that if a table is not otherwise vacuumed, autovacuum will be invoked on it approximately once every `autovacuum_freeze_max_age` minus `vacuum_freeze_min_age` transactions. For tables that are regularly vacuumed for space reclamation purposes, this is of little importance. However, for static tables \(including tables that receive inserts, but no updates or deletes\), there is no need to vacuum for space reclamation, so it can be useful to try to maximize the interval between forced autovacuums on very large static tables. Obviously one can do this either by increasing `autovacuum_freeze_max_age` or decreasing `vacuum_freeze_min_age`.

The effective maximum for `vacuum_freeze_table_age` is 0.95 \* `autovacuum_freeze_max_age`; a setting higher than that will be capped to the maximum. A value higher than `autovacuum_freeze_max_age` wouldn't make sense because an anti-wraparound autovacuum would be triggered at that point anyway, and the 0.95 multiplier leaves some breathing room to run a manual `VACUUM` before that happens. As a rule of thumb, `vacuum_freeze_table_age` should be set to a value somewhat below `autovacuum_freeze_max_age`, leaving enough gap so that a regularly scheduled `VACUUM` or an autovacuum triggered by normal delete and update activity is run in that window. Setting it too close could lead to anti-wraparound autovacuums, even though the table was recently vacuumed to reclaim space, whereas lower values lead to more frequent aggressive vacuuming.

The sole disadvantage of increasing `autovacuum_freeze_max_age` \(and `vacuum_freeze_table_age` along with it\) is that the `pg_xact` and `pg_commit_ts` subdirectories of the database cluster will take more space, because it must store the commit status and \(if `track_commit_timestamp` is enabled\) timestamp of all transactions back to the `autovacuum_freeze_max_age` horizon. The commit status uses two bits per transaction, so if `autovacuum_freeze_max_age` is set to its maximum allowed value of two billion, `pg_xact` can be expected to grow to about half a gigabyte and `pg_commit_ts` to about 20GB. If this is trivial compared to your total database size, setting `autovacuum_freeze_max_age` to its maximum allowed value is recommended. Otherwise, set it depending on what you are willing to allow for `pg_xact` and `pg_commit_ts` storage. \(The default, 200 million transactions, translates to about 50MB of `pg_xact` storage and about 2GB of `pg_commit_ts` storage.\)

One disadvantage of decreasing `vacuum_freeze_min_age` is that it might cause `VACUUM` to do useless work: freezing a row version is a waste of time if the row is modified soon thereafter \(causing it to acquire a new XID\). So the setting should be large enough that rows are not frozen until they are unlikely to change any more.

To track the age of the oldest unfrozen XIDs in a database, `VACUUM` stores XID statistics in the system tables `pg_class` and `pg_database`. In particular, the `relfrozenxid` column of a table's `pg_class` row contains the freeze cutoff XID that was used by the last aggressive `VACUUM` for that table. All rows inserted by transactions with XIDs older than this cutoff XID are guaranteed to have been frozen. Similarly, the `datfrozenxid` column of a database's `pg_database` row is a lower bound on the unfrozen XIDs appearing in that database — it is just the minimum of the per-table `relfrozenxid` values within the database. A convenient way to examine this information is to execute queries such as:

```text
SELECT c.oid::regclass as table_name,
       greatest(age(c.relfrozenxid),age(t.relfrozenxid)) as age
FROM pg_class c
LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relkind IN ('r', 'm');

SELECT datname, age(datfrozenxid) FROM pg_database;
```

The `age` column measures the number of transactions from the cutoff XID to the current transaction's XID.

`VACUUM` normally only scans pages that have been modified since the last vacuum, but `relfrozenxid` can only be advanced when every page of the table that might contain unfrozen XIDs is scanned. This happens when `relfrozenxid` is more than `vacuum_freeze_table_age`transactions old, when `VACUUM`'s `FREEZE` option is used, or when all pages that are not already all-frozen happen to require vacuuming to remove dead row versions. When `VACUUM` scans every page in the table that is not already all-frozen, it should set `age(relfrozenxid)` to a value just a little more than the `vacuum_freeze_min_age` setting that was used \(more by the number of transactions started since the `VACUUM` started\). If no `relfrozenxid`-advancing `VACUUM` is issued on the table until `autovacuum_freeze_max_age` is reached, an autovacuum will soon be forced for the table.

If for some reason autovacuum fails to clear old XIDs from a table, the system will begin to emit warning messages like this when the database's oldest XIDs reach ten million transactions from the wraparound point:

```text
WARNING:  database "mydb" must be vacuumed within 177009986 transactions
HINT:  To avoid a database shutdown, execute a database-wide VACUUM in "mydb".
```

\(A manual `VACUUM` should fix the problem, as suggested by the hint; but note that the `VACUUM` must be performed by a superuser, else it will fail to process system catalogs and thus not be able to advance the database's `datfrozenxid`.\) If these warnings are ignored, the system will shut down and refuse to start any new transactions once there are fewer than 1 million transactions left until wraparound:

```text
ERROR:  database is not accepting commands to avoid wraparound data loss in database "mydb"
HINT:  Stop the postmaster and vacuum that database in single-user mode.
```

The 1-million-transaction safety margin exists to let the administrator recover without data loss, by manually executing the required `VACUUM` commands. However, since the system will not execute commands once it has gone into the safety shutdown mode, the only way to do this is to stop the server and start the server in single-user mode to execute `VACUUM`. The shutdown mode is not enforced in single-user mode. See the [postgres](https://www.postgresql.org/docs/10/static/app-postgres.html) reference page for details about using single-user mode.

### **24.1.5.1. Multixacts and Wraparound**

_Multixact IDs_ are used to support row locking by multiple transactions. Since there is only limited space in a tuple header to store lock information, that information is encoded as a “multiple transaction ID”, or multixact ID for short, whenever there is more than one transaction concurrently locking a row. Information about which transaction IDs are included in any particular multixact ID is stored separately in the `pg_multixact` subdirectory, and only the multixact ID appears in the `xmax` field in the tuple header. Like transaction IDs, multixact IDs are implemented as a 32-bit counter and corresponding storage, all of which requires careful aging management, storage cleanup, and wraparound handling. There is a separate storage area which holds the list of members in each multixact, which also uses a 32-bit counter and which must also be managed.

Whenever `VACUUM` scans any part of a table, it will replace any multixact ID it encounters which is older than [vacuum\_multixact\_freeze\_min\_age](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE) by a different value, which can be the zero value, a single transaction ID, or a newer multixact ID. For each table,`pg_class`.`relminmxid` stores the oldest possible multixact ID still appearing in any tuple of that table. If this value is older than [vacuum\_multixact\_freeze\_table\_age](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE), an aggressive vacuum is forced. As discussed in the previous section, an aggressive vacuum means that only those pages which are known to be all-frozen will be skipped. `mxid_age()` can be used on `pg_class`.`relminmxid` to find its age.

Aggressive `VACUUM` scans, regardless of what causes them, enable advancing the value for that table. Eventually, as all tables in all databases are scanned and their oldest multixact values are advanced, on-disk storage for older multixacts can be removed.

As a safety device, an aggressive vacuum scan will occur for any table whose multixact-age is greater than [autovacuum\_multixact\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE). Aggressive vacuum scans will also occur progressively for all tables, starting with those that have the oldest multixact-age, if the amount of used member storage space exceeds the amount 50% of the addressable storage space. Both of these kinds of aggressive scans will occur even if autovacuum is nominally disabled.

## 24.1.6. Autovacuum 背景程序

PostgreSQL 有一個選用但強烈推薦的 autovacuum 功能，其目的是自動執行 VACUUM 和 ANALYZE 指令。啟用後，autovacuum 將檢查已插入、更新或刪除大量 tuple 的資料表。這些檢查使用統計資訊收集工具；因此，除非將 [track\_counts](../server-configuration/19.9.-run-time-statistics.md#19-9-1-query-and-index-statistics-collector) 設定為 true，否則無法使用 autovacuum。在預設配置中，啟用 autovacuuming 並相對應地設定相關的配置參數。

「autovacuum 背景程序」實際上由多個程序所組成。有一個主控的背景程序，稱為 autovacuum 啟動程序，負責啟動所有資料庫的 autovacuum 工作程序。啟動程序將跨時間分配工作，嘗試在每個 [autovacuum\_naptime](../server-configuration/automatic-vacuuming.md) 秒內啟動每個資料庫中的一個工作程序。（因此，如果安裝 N 個資料庫，則每個 autovacuum\_naptime / N 秒將啟動一個新工作程序。）允許最多同時運行 [autovacuum\_max\_workers](../server-configuration/automatic-vacuuming.md) 工作程序。如果要處理的 autovacuum\_max\_workers 資料庫不止一個，則第一個工作程序完成後將立即處理下一個資料庫。每個工作程序將檢查其資料庫中的每個資料表，並根據需要執行 VACUUM 或 ANALYZE。log\_autovacuum\_min\_duration 可以設定為監控 autovacuum 工作程序的活動。

If several large tables all become eligible for vacuuming in a short amount of time, all autovacuum workers might become occupied with vacuuming those tables for a long period. This would result in other tables and databases not being vacuumed until a worker becomes available. There is no limit on how many workers might be in a single database, but workers do try to avoid repeating work that has already been done by other workers. Note that the number of running workers does not count towards [max\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) or [superuser\_reserved\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-SUPERUSER-RESERVED-CONNECTIONS) limits.

Tables whose `relfrozenxid` value is more than [autovacuum\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE) transactions old are always vacuumed \(this also applies to those tables whose freeze max age has been modified via storage parameters; see below\). Otherwise, if the number of tuples obsoleted since the last `VACUUM` exceeds the “vacuum threshold”, the table is vacuumed. The vacuum threshold is defined as:

```text
vacuum threshold = vacuum base threshold + vacuum scale factor * number of tuples
```

where the vacuum base threshold is [autovacuum\_vacuum\_threshold](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-THRESHOLD), the vacuum scale factor is [autovacuum\_vacuum\_scale\_factor](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR), and the number of tuples is `pg_class`.`reltuples`. The number of obsolete tuples is obtained from the statistics collector; it is a semi-accurate count updated by each `UPDATE` and `DELETE` operation. \(It is only semi-accurate because some information might be lost under heavy load.\) If the `relfrozenxid` value of the table is more than `vacuum_freeze_table_age` transactions old, an aggressive vacuum is performed to freeze old tuples and advance `relfrozenxid`; otherwise, only pages that have been modified since the last vacuum are scanned.

For analyze, a similar condition is used: the threshold, defined as:

```text
analyze threshold = analyze base threshold + analyze scale factor * number of tuples
```

is compared to the total number of tuples inserted, updated, or deleted since the last `ANALYZE`.

Temporary tables cannot be accessed by autovacuum. Therefore, appropriate vacuum and analyze operations should be performed via session SQL commands.

The default thresholds and scale factors are taken from `postgresql.conf`, but it is possible to override them \(and many other autovacuum control parameters\) on a per-table basis; see [Storage Parameters](https://www.postgresql.org/docs/10/static/sql-createtable.html#SQL-CREATETABLE-STORAGE-PARAMETERS) for more information. If a setting has been changed via a table's storage parameters, that value is used when processing that table; otherwise the global settings are used. See [Section 19.10](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html) for more details on the global settings.

When multiple workers are running, the autovacuum cost delay parameters \(see [Section 19.4.4](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)\) are “balanced” among all the running workers, so that the total I/O impact on the system is the same regardless of the number of workers actually running. However, any workers processing tables whose per-table `autovacuum_vacuum_cost_delay` or `autovacuum_vacuum_cost_limit` storage parameters have been set are not considered in the balancing algorithm.

