---
description: 版本：10
---

# 19.4. 資源配置

## 19.4.1. 記憶體

`shared_buffers` \(`integer`\)

設定資料庫伺服器用於共享記憶體緩衝區的大小。預設值通常為 128 MB，但如果您的核心設定不支援（在 initdb 期間確定），則可能會更少。此設定必須至少為128 KB。（非預設值的 BLCKSZ 會改變最小值。）但是，通常需要高於最小值的設定才能獲得良好的性能。此參數只能在伺服器啟動時設定。

如果您擁有 1GB 或更多記憶體的專用資料庫伺服器，shared\_buffers 的合理起始值是系統記憶體的 25％。有些工作負載甚至可以為 shared\_buffers 設定更大的值，但由於PostgreSQL 依賴於作業系統緩衝區，因此，把 shared\_buffers 分配 40％ 以上的記憶體大小不太可能比少量分配更好。shared\_buffers 較大設定通常需要 max\_wal\_size 相對應的增加，以便分散在較長時間內寫入大量新資料或變更資料的過程。

在 RAM 小於 1GB 的系統上，更小比例是合適的，以便為作業系統留下足夠的空間。

`huge_pages` \(`enum`\)

Enables/disables the use of huge memory pages. Valid values are `try` \(the default\), `on`, and `off`.

At present, this feature is supported only on Linux. The setting is ignored on other systems when set to `try`.

The use of huge pages results in smaller page tables and less CPU time spent on memory management, increasing performance. For more details, see [Section 18.4.5](https://www.postgresql.org/docs/10/static/kernel-resources.html#LINUX-HUGE-PAGES).

With `huge_pages` set to `try`, the server will try to use huge pages, but fall back to using normal allocation if that fails. With `on`, failure to use huge pages will prevent the server from starting up. With `off`, huge pages will not be used.

`temp_buffers` \(`integer`\)

Sets the maximum number of temporary buffers used by each database session. These are session-local buffers used only for access to temporary tables. The default is eight megabytes \(`8MB`\). The setting can be changed within individual sessions, but only before the first use of temporary tables within the session; subsequent attempts to change the value will have no effect on that session.

A session will allocate temporary buffers as needed up to the limit given by `temp_buffers`. The cost of setting a large value in sessions that do not actually need many temporary buffers is only a buffer descriptor, or about 64 bytes, per increment in `temp_buffers`. However if a buffer is actually used an additional 8192 bytes will be consumed for it \(or in general, `BLCKSZ` bytes\).

`max_prepared_transactions` \(`integer`\)

設定可同時處於「prepared」狀態的最大交易事務數量（請參閱 [PREPARE TRANSACTION](../../vi.-can-kao-zi-xun/i.-sql-zhi-ling/prepare-transaction.md)）。將此參數設定為零（這是預設值）的話，會停用預備交易的功能。此參數只能在伺服器啟動時設定。

如果您不打算使用預備交易事務，則應將此參數設定為零以防止意外建立預備的交易事務。如果您正在使用預備的交易事務，那麼您可能希望 max\_prepared\_transactions 至少與 [max\_connections](connections-and-authentication.md#19-3-1-ding) 一樣大，以便每個連線都可以至少有一個準備好的預備交易事務。

運行備用伺服器時，必須將此參數設定為與主服務器上相同或更高的值。 否則，查詢將不被允許在備用伺服器中。

`work_mem` \(`integer`\)

指定寫入暫存檔之前內部排序操作和雜湊表使用的記憶體大小。此值預設為 4 MB。請注意，對於複雜的查詢，可能會同時執行多個排序或雜湊作業；在開始將資料寫入暫存檔之前，每個操作都將被允許盡可能使用記憶體。此外，多個連線可以同時進行這些操作。因此，所使用的總記憶體量可能是 work\_mem 值的許多倍；決定值時必須牢記此一事實。排序操作用於 ORDER BY，DISTINCT 和 merge JOIN。雜湊表用於 hash JOIN，hash aggregation 和 IN 子查詢處理。

`maintenance_work_mem` \(`integer`\)

Specifies the maximum amount of memory to be used by maintenance operations, such as `VACUUM`, `CREATE INDEX`, and `ALTER TABLE ADD FOREIGN KEY`. It defaults to 64 megabytes \(`64MB`\). Since only one of these operations can be executed at a time by a database session, and an installation normally doesn't have many of them running concurrently, it's safe to set this value significantly larger than `work_mem`. Larger settings might improve performance for vacuuming and for restoring database dumps.

Note that when autovacuum runs, up to [autovacuum\_max\_workers](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MAX-WORKERS) times this memory may be allocated, so be careful not to set the default value too high. It may be useful to control for this by separately setting [autovacuum\_work\_mem](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM).

`replacement_sort_tuples` \(`integer`\)

When the number of tuples to be sorted is smaller than this number, a sort will produce its first output run using replacement selection rather than quicksort. This may be useful in memory-constrained environments where tuples that are input into larger sort operations have a strong physical-to-logical correlation. Note that this does not include input tuples with an _inverse_ correlation. It is possible for the replacement selection algorithm to generate one long run that requires no merging, where use of the default strategy would result in many runs that must be merged to produce a final sorted output. This may allow sort operations to complete sooner.

The default is 150,000 tuples. Note that higher values are typically not much more effective, and may be counter-productive, since the priority queue is sensitive to the size of available CPU cache, whereas the default strategy sorts runs using a _cache oblivious_algorithm. This property allows the default sort strategy to automatically and transparently make effective use of available CPU cache.

Setting `maintenance_work_mem` to its default value usually prevents utility command external sorts \(e.g., sorts used by `CREATE INDEX` to build B-Tree indexes\) from ever using replacement selection sort, unless the input tuples are quite wide.

`autovacuum_work_mem` \(`integer`\)

Specifies the maximum amount of memory to be used by each autovacuum worker process. It defaults to -1, indicating that the value of [maintenance\_work\_mem](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM) should be used instead. The setting has no effect on the behavior of `VACUUM` when run in other contexts.

`max_stack_depth` \(`integer`\)

Specifies the maximum safe depth of the server's execution stack. The ideal setting for this parameter is the actual stack size limit enforced by the kernel \(as set by `ulimit -s` or local equivalent\), less a safety margin of a megabyte or so. The safety margin is needed because the stack depth is not checked in every routine in the server, but only in key potentially-recursive routines such as expression evaluation. The default setting is two megabytes \(`2MB`\), which is conservatively small and unlikely to risk crashes. However, it might be too small to allow execution of complex functions. Only superusers can change this setting.

Setting `max_stack_depth` higher than the actual kernel limit will mean that a runaway recursive function can crash an individual backend process. On platforms where PostgreSQL can determine the kernel limit, the server will not allow this variable to be set to an unsafe value. However, not all platforms provide the information, so caution is recommended in selecting a value.

`dynamic_shared_memory_type` \(`enum`\)

Specifies the dynamic shared memory implementation that the server should use. Possible values are `posix` \(for POSIX shared memory allocated using `shm_open`\), `sysv` \(for System V shared memory allocated via `shmget`\), `windows` \(for Windows shared memory\), `mmap`\(to simulate shared memory using memory-mapped files stored in the data directory\), and `none` \(to disable this feature\). Not all values are supported on all platforms; the first supported option is the default for that platform. The use of the `mmap` option, which is not the default on any platform, is generally discouraged because the operating system may write modified pages back to disk repeatedly, increasing system I/O load; however, it may be useful for debugging, when the `pg_dynshmem` directory is stored on a RAM disk, or when other shared memory facilities are not available.

## 19.4.2. 磁碟

`temp_file_limit` \(`integer`\)

指定程序可用於暫存檔的最大磁碟空間大小，例如排序和雜湊暫存檔，或持有游標的檔案。試圖超過此限制的交易將被取消。此值以 KB 為單位指定，-1（預設值）表示無限制。只有超級使用者可以變更改此設定。

此設定限制了給予 PostgreSQL 程序使用的所有暫存檔在任何時刻能使用的總空間。應該注意的是，用於臨時資料表的磁碟空間與在查詢執行過程中使用的暫存檔不同，並不會計入此限制。

## 19.4.3. 核心資源配置

`max_files_per_process` \(`integer`\)

設定每個伺服器子程序允許的同時最大開啓的檔案數。預設值是 1000 個檔案。如果核心可以確保每個程序的安全限制，則不必擔心此設定。但是在某些平台上（特別是大多數 BSD 系統），如果許多程序都嘗試開啓那麼多檔案，核心將允許單個程序打開比系統實際支援的更多的檔案。如果您發現自己看到“Too many open files”失敗，請嘗試減少此設定。此參數只能在伺服器啟動時設定。

## 19.4.4. Cost-based Vacuum Delay

During the execution of [VACUUM](https://www.postgresql.org/docs/10/static/sql-vacuum.html) and [ANALYZE](https://www.postgresql.org/docs/10/static/sql-analyze.html) commands, the system maintains an internal counter that keeps track of the estimated cost of the various I/O operations that are performed. When the accumulated cost reaches a limit \(specified by `vacuum_cost_limit`\), the process performing the operation will sleep for a short period of time, as specified by `vacuum_cost_delay`. Then it will reset the counter and continue execution.

The intent of this feature is to allow administrators to reduce the I/O impact of these commands on concurrent database activity. There are many situations where it is not important that maintenance commands like `VACUUM` and `ANALYZE` finish quickly; however, it is usually very important that these commands do not significantly interfere with the ability of the system to perform other database operations. Cost-based vacuum delay provides a way for administrators to achieve this.

This feature is disabled by default for manually issued `VACUUM` commands. To enable it, set the `vacuum_cost_delay` variable to a nonzero value.

`vacuum_cost_delay` \(`integer`\)

The length of time, in milliseconds, that the process will sleep when the cost limit has been exceeded. The default value is zero, which disables the cost-based vacuum delay feature. Positive values enable cost-based vacuuming. Note that on many systems, the effective resolution of sleep delays is 10 milliseconds; setting `vacuum_cost_delay` to a value that is not a multiple of 10 might have the same results as setting it to the next higher multiple of 10.

When using cost-based vacuuming, appropriate values for `vacuum_cost_delay` are usually quite small, perhaps 10 or 20 milliseconds. Adjusting vacuum's resource consumption is best done by changing the other vacuum cost parameters.

`vacuum_cost_page_hit` \(`integer`\)

The estimated cost for vacuuming a buffer found in the shared buffer cache. It represents the cost to lock the buffer pool, lookup the shared hash table and scan the content of the page. The default value is one.

`vacuum_cost_page_miss` \(`integer`\)

The estimated cost for vacuuming a buffer that has to be read from disk. This represents the effort to lock the buffer pool, lookup the shared hash table, read the desired block in from the disk and scan its content. The default value is 10.

`vacuum_cost_page_dirty` \(`integer`\)

The estimated cost charged when vacuum modifies a block that was previously clean. It represents the extra I/O required to flush the dirty block out to disk again. The default value is 20.

`vacuum_cost_limit` \(`integer`\)

The accumulated cost that will cause the vacuuming process to sleep. The default value is 200.

#### Note

There are certain operations that hold critical locks and should therefore complete as quickly as possible. Cost-based vacuum delays do not occur during such operations. Therefore it is possible that the cost accumulates far higher than the specified limit. To avoid uselessly long delays in such cases, the actual delay is calculated as `vacuum_cost_delay` \* `accumulated_balance` / `vacuum_cost_limit` with a maximum of `vacuum_cost_delay` \* 4.

## 19.4.5. Background Writer

There is a separate server process called the _background writer_, whose function is to issue writes of “dirty” \(new or modified\) shared buffers. It writes shared buffers so server processes handling user queries seldom or never need to wait for a write to occur. However, the background writer does cause a net overall increase in I/O load, because while a repeatedly-dirtied page might otherwise be written only once per checkpoint interval, the background writer might write it several times as it is dirtied in the same interval. The parameters discussed in this subsection can be used to tune the behavior for local needs.

`bgwriter_delay` \(`integer`\)

Specifies the delay between activity rounds for the background writer. In each round the writer issues writes for some number of dirty buffers \(controllable by the following parameters\). It then sleeps for `bgwriter_delay` milliseconds, and repeats. When there are no dirty buffers in the buffer pool, though, it goes into a longer sleep regardless of `bgwriter_delay`. The default value is 200 milliseconds \(`200ms`\). Note that on many systems, the effective resolution of sleep delays is 10 milliseconds; setting `bgwriter_delay` to a value that is not a multiple of 10 might have the same results as setting it to the next higher multiple of 10. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`bgwriter_lru_maxpages` \(`integer`\)

In each round, no more than this many buffers will be written by the background writer. Setting this to zero disables background writing. \(Note that checkpoints, which are managed by a separate, dedicated auxiliary process, are unaffected.\) The default value is 100 buffers. This parameter can only be set in the `postgresql.conf` file or on the server command line.`bgwriter_lru_multiplier` \(`floating point`\)

The number of dirty buffers written in each round is based on the number of new buffers that have been needed by server processes during recent rounds. The average recent need is multiplied by `bgwriter_lru_multiplier` to arrive at an estimate of the number of buffers that will be needed during the next round. Dirty buffers are written until there are that many clean, reusable buffers available. \(However, no more than `bgwriter_lru_maxpages` buffers will be written per round.\) Thus, a setting of 1.0 represents a “just in time”policy of writing exactly the number of buffers predicted to be needed. Larger values provide some cushion against spikes in demand, while smaller values intentionally leave writes to be done by server processes. The default is 2.0. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`bgwriter_flush_after` \(`integer`\)

Whenever more than `bgwriter_flush_after` bytes have been written by the background writer, attempt to force the OS to issue these writes to the underlying storage. Doing so will limit the amount of dirty data in the kernel's page cache, reducing the likelihood of stalls when an `fsync` is issued at the end of a checkpoint, or when the OS writes data back in larger batches in the background. Often that will result in greatly reduced transaction latency, but there also are some cases, especially with workloads that are bigger than [shared\_buffers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-SHARED-BUFFERS), but smaller than the OS's page cache, where performance might degrade. This setting may have no effect on some platforms. The valid range is between `0`, which disables forced writeback, and `2MB`. The default is `512kB` on Linux, `0` elsewhere. \(If `BLCKSZ` is not 8kB, the default and maximum values scale proportionally to it.\) This parameter can only be set in the `postgresql.conf` file or on the server command line.

Smaller values of `bgwriter_lru_maxpages` and `bgwriter_lru_multiplier` reduce the extra I/O load caused by the background writer, but make it more likely that server processes will have to issue writes for themselves, delaying interactive queries.

## 19.4.6. Asynchronous Behavior

`effective_io_concurrency` \(`integer`\)

Sets the number of concurrent disk I/O operations that PostgreSQL expects can be executed simultaneously. Raising this value will increase the number of I/O operations that any individual PostgreSQL session attempts to initiate in parallel. The allowed range is 1 to 1000, or zero to disable issuance of asynchronous I/O requests. Currently, this setting only affects bitmap heap scans.

For magnetic drives, a good starting point for this setting is the number of separate drives comprising a RAID 0 stripe or RAID 1 mirror being used for the database. \(For RAID 5 the parity drive should not be counted.\) However, if the database is often busy with multiple queries issued in concurrent sessions, lower values may be sufficient to keep the disk array busy. A value higher than needed to keep the disks busy will only result in extra CPU overhead. SSDs and other memory-based storage can often process many concurrent requests, so the best value might be in the hundreds.

Asynchronous I/O depends on an effective `posix_fadvise` function, which some operating systems lack. If the function is not present then setting this parameter to anything but zero will result in an error. On some operating systems \(e.g., Solaris\), the function is present but does not actually do anything.

The default is 1 on supported systems, otherwise 0. This value can be overridden for tables in a particular tablespace by setting the tablespace parameter of the same name \(see [ALTER TABLESPACE](https://www.postgresql.org/docs/10/static/sql-altertablespace.html)\).

`max_worker_processes` \(`integer`\)

Sets the maximum number of background processes that the system can support. This parameter can only be set at server start. The default is 8.

When running a standby server, you must set this parameter to the same or higher value than on the master server. Otherwise, queries will not be allowed in the standby server.

When changing this value, consider also adjusting [max\_parallel\_workers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS) and [max\_parallel\_workers\_per\_gather](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER).

`max_parallel_workers_per_gather` \(`integer`\)

Sets the maximum number of workers that can be started by a single `Gather` or `Gather Merge` node. Parallel workers are taken from the pool of processes established by [max\_worker\_processes](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES), limited by [max\_parallel\_workers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS). Note that the requested number of workers may not actually be available at run time. If this occurs, the plan will run with fewer workers than expected, which may be inefficient. The default value is 2. Setting this value to 0 disables parallel query execution.

Note that parallel queries may consume very substantially more resources than non-parallel queries, because each worker process is a completely separate process which has roughly the same impact on the system as an additional user session. This should be taken into account when choosing a value for this setting, as well as when configuring other settings that control resource utilization, such as [work\_mem](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-WORK-MEM). Resource limits such as `work_mem` are applied individually to each worker, which means the total utilization may be much higher across all processes than it would normally be for any single process. For example, a parallel query using 4 workers may use up to 5 times as much CPU time, memory, I/O bandwidth, and so forth as a query which uses no workers at all.

For more information on parallel query, see [Chapter 15](https://www.postgresql.org/docs/10/static/parallel-query.html).

`max_parallel_workers` \(`integer`\)

Sets the maximum number of workers that the system can support for parallel queries. The default value is 8. When increasing or decreasing this value, consider also adjusting [max\_parallel\_workers\_per\_gather](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER). Also, note that a setting for this value which is higher than [max\_worker\_processes](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES) will have no effect, since parallel workers are taken from the pool of worker processes established by that setting.

`backend_flush_after` \(`integer`\)

Whenever more than `backend_flush_after` bytes have been written by a single backend, attempt to force the OS to issue these writes to the underlying storage. Doing so will limit the amount of dirty data in the kernel's page cache, reducing the likelihood of stalls when an `fsync` is issued at the end of a checkpoint, or when the OS writes data back in larger batches in the background. Often that will result in greatly reduced transaction latency, but there also are some cases, especially with workloads that are bigger than [shared\_buffers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-SHARED-BUFFERS), but smaller than the OS's page cache, where performance might degrade. This setting may have no effect on some platforms. The valid range is between `0`, which disables forced writeback, and `2MB`. The default is `0`, i.e., no forced writeback. \(If `BLCKSZ`is not 8kB, the maximum value scales proportionally to it.\)

`old_snapshot_threshold` \(`integer`\)

Sets the minimum time that a snapshot can be used without risk of a `snapshot too old` error occurring when using the snapshot. This parameter can only be set at server start.

Beyond the threshold, old data may be vacuumed away. This can help prevent bloat in the face of snapshots which remain in use for a long time. To prevent incorrect results due to cleanup of data which would otherwise be visible to the snapshot, an error is generated when the snapshot is older than this threshold and the snapshot is used to read a page which has been modified since the snapshot was built.

A value of `-1` disables this feature, and is the default. Useful values for production work probably range from a small number of hours to a few days. The setting will be coerced to a granularity of minutes, and small numbers \(such as `0` or `1min`\) are only allowed because they may sometimes be useful for testing. While a setting as high as `60d` is allowed, please note that in many workloads extreme bloat or transaction ID wraparound may occur in much shorter time frames.

When this feature is enabled, freed space at the end of a relation cannot be released to the operating system, since that could remove information needed to detect the `snapshot too old` condition. All space allocated to a relation remains associated with that relation for reuse only within that relation unless explicitly freed \(for example, with `VACUUM FULL`\).

This setting does not attempt to guarantee that an error will be generated under any particular circumstances. In fact, if the correct results can be generated from \(for example\) a cursor which has materialized a result set, no error will be generated even if the underlying rows in the referenced table have been vacuumed away. Some tables cannot safely be vacuumed early, and so will not be affected by this setting, such as system catalogs. For such tables this setting will neither reduce bloat nor create a possibility of a `snapshot too old` error on scanning.

