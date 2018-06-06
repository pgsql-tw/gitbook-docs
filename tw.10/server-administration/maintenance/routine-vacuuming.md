# 24.1. 例行性資料清理

PostgreSQL 資料庫需要定期維護，稱為資料庫清理\(vacuum\)。 對於一裝的執行環境而言，透過 autovacuum 背景程序進行資料庫清理就足夠了，這在 [24.1.6 節](routine-vacuuming.md#24-1-6-the-autovacuum-daemon)中有描述。您可能需要調整其中所描述的自動清除參數，以獲得您的情況的最佳結果。 一些資料庫管理員希望用手動管理的 VACUUM 命令來補充或替換背景程序的活動，這些命令通常根據 cron 或 Task Scheduler 的腳本計劃執行。 要正確設定手動管理的資料庫清理，了解接下來幾小節中討論的問題至關重要。依靠自動清理的管理員可能仍然希望瀏覽這些內容以幫助他們理解和調整自動清理。

## 24.1.1. 資料庫清理的基本概念

必須以 PostgreSQL [VACUUM](../../reference/sql-commands/vacuum.md) 命令處理每個資料表，原因如下：

1. 恢復或回收使用因更新或刪除資料列所佔用的磁碟空間。
2. 更新 PostgreSQL 查詢計劃器使用的資料統計資訊。
3. 更新可視性結構，這會增加[索引限定掃描](../../sql/index/index-only-scans.md)的效率。
4. 防止由於事務 ID 重覆或 multixact ID 重覆而失去非常舊的資料。

這些原因中的每一個都會要求執行不同頻率和範圍的 VACUUM 操作，如以下小節所述。

VACUUM 有兩種變形：標準 VACUUM 和 VACUUM FULL。VACUUM FULL 可以回收更多磁碟空間，但執行速度要慢得多。而且，VACUUM 的標準形式可以與產品資料庫同時操作運行。（SELECT、INSERT、UPDATE 和 DELETE 等指令將繼續正常工作，但在 VACUUM FULL 時，您將無法使用諸如 ALTER TABLE 之類的指令修改資料表的定義。）VACUUM FULL 需要獨占鎖定它正在處理的資料表，因此無法與其他資料表的使用同時進行。因此，一般來說，管理員應該努力使用標準 VACUUM 並避免VACUUM FULL。

VACUUM 會產生大量的 I/O流量，這會導致其他正在進行的連線效能較差。有一些配置參數可以調整以減少背景資料庫清理對效能的影響 - 參閱[第 19.4.4 節](../runtime-config/resource-consumption.md#19-4-4-cost-based-vacuum-delay)`。`

## 24.1.2. 恢復磁碟空間

在 PostgreSQL 中，資料列的 UPDATE 或 DELETE 不會立即刪除該資料列的舊版本。這種方法對於獲得多版本平行控制（MVCC，參閱[第 13 章](../../sql/mvcc/)）的好處是必要的：資料列的版本不能被刪除，而其他事務仍然可以看到。 但最終，過時或刪除的資料列版本不再讓任何交易感興趣。它佔用的空間必須被新行重新使用以避免無限增長的磁碟空間需求。這是透過執行 VACUUM 來完成的。

VACUUM 的標準作法是移除資料表和索引中過時的資料列版本，並標記可供將來重複使用的空間。 但是，除非資料表末端的一個或多個頁面變為完全空閒並且可以輕鬆獲取排他資料表鎖的特殊情況，否則它不會將空間還給作業系統。相比之下，VACUUM FULL 透過寫入完整新版本使其沒有空閒的空間來主動壓縮資料表。這最大限度地減少了資料表的大小，但可能需要很長時間。 它還需要用於資料表的新副本的額外磁碟空間，直到操作完成。

常態的資料庫清理通常目標是經常足夠地執行標準 VACUUM 以避免需要 VACUUM FULL。autovacuum 背景程序嘗試以這種方式工作，實際上永遠不會發出 VACUUM FULL。在這種方法中，這個想法並不是將資料表保持在最小尺寸，而是為了保持磁碟空間的穩定狀態使用：每個資料表都佔用相當於其最小尺寸的空間，再加上在 VACUUM 之間使用的空間很大，儘管可以使用 VACUUM FULL 將表縮回到最小大小並將磁碟空間還回到作業系統，但如果資料表將來會再次增長，則沒有多大意義。 因此，適度頻繁的標準 VACUUM 運行比用於維護大量更新資料表的罕見 VACUUM FULL 運行更好。

有些管理者更喜歡自己安排資料庫清理作業，例如在負載較低時在夜間進行所有工作。按照固定的時間表進行資料庫清理作業的困難在於，如果資料表在更新活動中出現意外的峰值，則可能會變得臃腫到 VACUUM FULL 真的需要回收空間。使用自動清理背景程序緩解了這個問題，因為背景程序會根據更新活動動態調度清理作業。除非您有一個非常可預測的工作量，否則完全停用該背景程序是不明智的。一個可能的折衷辦法是設定背景程序的參數，以便它僅對異常繁重的更新活動作出反應，從而避免事情失控，而預定的 VACUUM 參數是能在典型的情況下完成大部分工作。

對於那些不使用自動清理的人來說，一種典型的方法是在低使用期內每天安排一次資料庫範圍內的 VACUUM，並根據需要更頻繁地清空大量更新的資料表。（一些具有極高更新率的設定每隔幾分鐘就會清理一次最繁忙的資料表，如此頻繁。）如果叢集中有多個資料庫，請不要忘記每個資料庫都有 VACUUM；[vacuumdb](../../reference/client/vacuumdb.md) 工作可能會有所幫助。

#### 小技巧

當一個資料表由於大量更新或刪除活動而包含大量過時資料列版本時，一般的 VACUUM 可能不能令人滿意。如果您有這樣一個資料表並且您需要回收佔用的多餘磁碟空間，則需要使用 VACUUM FULL 或 [CLUSTER](../../reference/sql-commands/cluster.md) 或 [ALTER TABLE](../../reference/sql-commands/alter-table.md) 的資料表重寫變形之一。這些命令重寫整個資料表的新副本並為其構建新的索引。所有這些選項都需要獨占鎖定。請注意，它們也暫時使用大約等於資料表大小的額外磁碟空間，因為資料表和索引的舊副本只有在新資料表完成後才能完全釋放。

#### 小技巧

如果您有一張定期刪除整個內容的資料表，請考慮使用 TRUNCATE 而不是使用 DELETE 和 VACUUM。[TRUNCATE](../../reference/sql-commands/truncate.md) 會立即刪除資料表的全部內容，而不需要後續的 VACUUM 或 VACUUM FULL 來回收現在未使用的磁碟空間。缺點是違反了嚴格的 MVCC 意義。

## 24.1.3. Updating Planner Statistics

The PostgreSQL query planner relies on statistical information about the contents of tables in order to generate good plans for queries. These statistics are gathered by the [ANALYZE](https://www.postgresql.org/docs/10/static/sql-analyze.html) command, which can be invoked by itself or as an optional step in `VACUUM`. It is important to have reasonably accurate statistics, otherwise poor choices of plans might degrade database performance.

The autovacuum daemon, if enabled, will automatically issue `ANALYZE` commands whenever the content of a table has changed sufficiently. However, administrators might prefer to rely on manually-scheduled `ANALYZE` operations, particularly if it is known that update activity on a table will not affect the statistics of “interesting” columns. The daemon schedules `ANALYZE` strictly as a function of the number of rows inserted or updated; it has no knowledge of whether that will lead to meaningful statistical changes.

As with vacuuming for space recovery, frequent updates of statistics are more useful for heavily-updated tables than for seldom-updated ones. But even for a heavily-updated table, there might be no need for statistics updates if the statistical distribution of the data is not changing much. A simple rule of thumb is to think about how much the minimum and maximum values of the columns in the table change. For example, a `timestamp` column that contains the time of row update will have a constantly-increasing maximum value as rows are added and updated; such a column will probably need more frequent statistics updates than, say, a column containing URLs for pages accessed on a website. The URL column might receive changes just as often, but the statistical distribution of its values probably changes relatively slowly.

It is possible to run `ANALYZE` on specific tables and even just specific columns of a table, so the flexibility exists to update some statistics more frequently than others if your application requires it. In practice, however, it is usually best to just analyze the entire database, because it is a fast operation. `ANALYZE` uses a statistically random sampling of the rows of a table rather than reading every single row.

#### Tip

Although per-column tweaking of `ANALYZE` frequency might not be very productive, you might find it worthwhile to do per-column adjustment of the level of detail of the statistics collected by `ANALYZE`. Columns that are heavily used in `WHERE` clauses and have highly irregular data distributions might require a finer-grain data histogram than other columns. See `ALTER TABLE SET STATISTICS`, or change the database-wide default using the [default\_statistics\_target](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) configuration parameter.

Also, by default there is limited information available about the selectivity of functions. However, if you create an expression index that uses a function call, useful statistics will be gathered about the function, which can greatly improve query plans that use the expression index.

#### Tip

The autovacuum daemon does not issue `ANALYZE` commands for foreign tables, since it has no means of determining how often that might be useful. If your queries require statistics on foreign tables for proper planning, it's a good idea to run manually-managed `ANALYZE`commands on those tables on a suitable schedule.

## 24.1.4. Updating The Visibility Map

Vacuum maintains a [visibility map](https://www.postgresql.org/docs/10/static/storage-vm.html) for each table to keep track of which pages contain only tuples that are known to be visible to all active transactions \(and all future transactions, until the page is again modified\). This has two purposes. First, vacuum itself can skip such pages on the next run, since there is nothing to clean up.

Second, it allows PostgreSQL to answer some queries using only the index, without reference to the underlying table. Since PostgreSQL indexes don't contain tuple visibility information, a normal index scan fetches the heap tuple for each matching index entry, to check whether it should be seen by the current transaction. An [_index-only scan_](https://www.postgresql.org/docs/10/static/indexes-index-only-scans.html), on the other hand, checks the visibility map first. If it's known that all tuples on the page are visible, the heap fetch can be skipped. This is most useful on large data sets where the visibility map can prevent disk accesses. The visibility map is vastly smaller than the heap, so it can easily be cached even when the heap is very large.

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

## 24.1.6. The Autovacuum Daemon

PostgreSQL has an optional but highly recommended feature called _autovacuum_, whose purpose is to automate the execution of `VACUUM` and `ANALYZE` commands. When enabled, autovacuum checks for tables that have had a large number of inserted, updated or deleted tuples. These checks use the statistics collection facility; therefore, autovacuum cannot be used unless [track\_counts](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-COUNTS) is set to `true`. In the default configuration, autovacuuming is enabled and the related configuration parameters are appropriately set.

The “autovacuum daemon” actually consists of multiple processes. There is a persistent daemon process, called the _autovacuum launcher_, which is in charge of starting _autovacuum worker_ processes for all databases. The launcher will distribute the work across time, attempting to start one worker within each database every [autovacuum\_naptime](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME) seconds. \(Therefore, if the installation has _`N`_ databases, a new worker will be launched every `autovacuum_naptime`/_`N`_ seconds.\) A maximum of [autovacuum\_max\_workers](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MAX-WORKERS) worker processes are allowed to run at the same time. If there are more than `autovacuum_max_workers` databases to be processed, the next database will be processed as soon as the first worker finishes. Each worker process will check each table within its database and execute `VACUUM` and/or `ANALYZE` as needed. [log\_autovacuum\_min\_duration](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-LOG-AUTOVACUUM-MIN-DURATION) can be set to monitor autovacuum workers' activity.

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

