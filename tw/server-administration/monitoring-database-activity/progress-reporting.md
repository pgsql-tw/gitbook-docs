# 27.4. Progress Reporting

PostgreSQL has the ability to report the progress of certain commands during command execution. Currently, the only commands which support progress reporting are `CREATE INDEX`, `VACUUM` and `CLUSTER`. This may be expanded in the future.

## 27.4.1. CREATE INDEX Progress Reporting

Whenever `CREATE INDEX` or `REINDEX` is running, the `pg_stat_progress_create_index` view will contain one row for each backend that is currently creating indexes. The tables below describe the information that will be reported and provide information about how to interpret it.

#### **Table 27.22. `pg_stat_progress_create_index` View**

| Column | Type | Description |
| :--- | :--- | :--- |
| `pid` | `integer` | Process ID of backend. |
| `datid` | `oid` | OID of the database to which this backend is connected. |
| `datname` | `name` | Name of the database to which this backend is connected. |
| `relid` | `oid` | OID of the table on which the index is being created. |
| `index_relid` | `oid` | OID of the index being created or reindexed. During a non-concurrent `CREATE INDEX`, this is 0. |
| `command` | `text` | The command that is running: `CREATE INDEX`, `CREATE INDEX CONCURRENTLY`, `REINDEX`, or `REINDEX CONCURRENTLY`. |
| `phase` | `text` | Current processing phase of index creation. See [Table 27.23](https://www.postgresql.org/docs/12/progress-reporting.html#CREATE-INDEX-PHASES). |
| `lockers_total` | `bigint` | Total number of lockers to wait for, when applicable. |
| `lockers_done` | `bigint` | Number of lockers already waited for. |
| `current_locker_pid` | `bigint` | Process ID of the locker currently being waited for. |
| `blocks_total` | `bigint` | Total number of blocks to be processed in the current phase. |
| `blocks_done` | `bigint` | Number of blocks already processed in the current phase. |
| `tuples_total` | `bigint` | Total number of tuples to be processed in the current phase. |
| `tuples_done` | `bigint` | Number of tuples already processed in the current phase. |
| `partitions_total` | `bigint` | When creating an index on a partitioned table, this column is set to the total number of partitions on which the index is to be created. |
| `partitions_done` | `bigint` | When creating an index on a partitioned table, this column is set to the number of partitions on which the index has been completed. |

#### **Table 27.23. CREATE INDEX Phases**

| Phase | Description |
| :--- | :--- |
| `initializing` | `CREATE INDEX` or `REINDEX` is preparing to create the index. This phase is expected to be very brief. |
| `waiting for writers before build` | `CREATE INDEX CONCURRENTLY` or `REINDEX CONCURRENTLY` is waiting for transactions with write locks that can potentially see the table to finish. This phase is skipped when not in concurrent mode. Columns `lockers_total`, `lockers_done` and `current_locker_pid` contain the progress information for this phase. |
| `building index` | The index is being built by the access method-specific code. In this phase, access methods that support progress reporting fill in their own progress data, and the subphase is indicated in this column. Typically, `blocks_total` and `blocks_done` will contain progress data, as well as potentially `tuples_total` and `tuples_done`. |
| `waiting for writers before validation` | `CREATE INDEX CONCURRENTLY` or `REINDEX CONCURRENTLY` is waiting for transactions with write locks that can potentially write into the table to finish. This phase is skipped when not in concurrent mode. Columns `lockers_total`, `lockers_done` and `current_locker_pid` contain the progress information for this phase. |
| `index validation: scanning index` | `CREATE INDEX CONCURRENTLY` is scanning the index searching for tuples that need to be validated. This phase is skipped when not in concurrent mode. Columns `blocks_total` \(set to the total size of the index\) and `blocks_done` contain the progress information for this phase. |
| `index validation: sorting tuples` | `CREATE INDEX CONCURRENTLY` is sorting the output of the index scanning phase. |
| `index validation: scanning table` | `CREATE INDEX CONCURRENTLY` is scanning the table to validate the index tuples collected in the previous two phases. This phase is skipped when not in concurrent mode. Columns `blocks_total` \(set to the total size of the table\) and `blocks_done` contain the progress information for this phase. |
| `waiting for old snapshots` | `CREATE INDEX CONCURRENTLY` or `REINDEX CONCURRENTLY` is waiting for transactions that can potentially see the table to release their snapshots. This phase is skipped when not in concurrent mode. Columns `lockers_total`, `lockers_done` and `current_locker_pid` contain the progress information for this phase. |
| `waiting for readers before marking dead` | `REINDEX CONCURRENTLY` is waiting for transactions with read locks on the table to finish, before marking the old index dead. This phase is skipped when not in concurrent mode. Columns `lockers_total`, `lockers_done` and `current_locker_pid` contain the progress information for this phase. |
| `waiting for readers before dropping` | `REINDEX CONCURRENTLY` is waiting for transactions with read locks on the table to finish, before dropping the old index. This phase is skipped when not in concurrent mode. Columns `lockers_total`, `lockers_done` and `current_locker_pid` contain the progress information for this phase. |

## 27.4.2. VACUUM Progress Reporting

Whenever `VACUUM` is running, the `pg_stat_progress_vacuum` view will contain one row for each backend \(including autovacuum worker processes\) that is currently vacuuming. The tables below describe the information that will be reported and provide information about how to interpret it. Progress for `VACUUM FULL` commands is reported via `pg_stat_progress_cluster` because both `VACUUM FULL` and `CLUSTER` rewrite the table, while regular `VACUUM` only modifies it in place. See [Section 27.4.3](https://www.postgresql.org/docs/12/progress-reporting.html#CLUSTER-PROGRESS-REPORTING).

#### **Table 27.24. `pg_stat_progress_vacuum` View**

| Column | Type | Description |
| :--- | :--- | :--- |
| `pid` | `integer` | Process ID of backend. |
| `datid` | `oid` | OID of the database to which this backend is connected. |
| `datname` | `name` | Name of the database to which this backend is connected. |
| `relid` | `oid` | OID of the table being vacuumed. |
| `phase` | `text` | Current processing phase of vacuum. See [Table 27.25](https://www.postgresql.org/docs/12/progress-reporting.html#VACUUM-PHASES). |
| `heap_blks_total` | `bigint` | Total number of heap blocks in the table. This number is reported as of the beginning of the scan; blocks added later will not be \(and need not be\) visited by this `VACUUM`. |
| `heap_blks_scanned` | `bigint` | Number of heap blocks scanned. Because the [visibility map](https://www.postgresql.org/docs/12/storage-vm.html) is used to optimize scans, some blocks will be skipped without inspection; skipped blocks are included in this total, so that this number will eventually become equal to `heap_blks_total` when the vacuum is complete. This counter only advances when the phase is `scanning heap`. |
| `heap_blks_vacuumed` | `bigint` | Number of heap blocks vacuumed. Unless the table has no indexes, this counter only advances when the phase is `vacuuming heap`. Blocks that contain no dead tuples are skipped, so the counter may sometimes skip forward in large increments. |
| `index_vacuum_count` | `bigint` | Number of completed index vacuum cycles. |
| `max_dead_tuples` | `bigint` | Number of dead tuples that we can store before needing to perform an index vacuum cycle, based on [maintenance\_work\_mem](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM). |
| `num_dead_tuples` | `bigint` | Number of dead tuples collected since the last index vacuum cycle. |

#### **Table 27.25. VACUUM Phases**

| Phase | Description |
| :--- | :--- |
| `initializing` | `VACUUM` is preparing to begin scanning the heap. This phase is expected to be very brief. |
| `scanning heap` | `VACUUM` is currently scanning the heap. It will prune and defragment each page if required, and possibly perform freezing activity. The `heap_blks_scanned` column can be used to monitor the progress of the scan. |
| `vacuuming indexes` | `VACUUM` is currently vacuuming the indexes. If a table has any indexes, this will happen at least once per vacuum, after the heap has been completely scanned. It may happen multiple times per vacuum if [maintenance\_work\_mem](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM) is insufficient to store the number of dead tuples found. |
| `vacuuming heap` | `VACUUM` is currently vacuuming the heap. Vacuuming the heap is distinct from scanning the heap, and occurs after each instance of vacuuming indexes. If `heap_blks_scanned` is less than `heap_blks_total`, the system will return to scanning the heap after this phase is completed; otherwise, it will begin cleaning up indexes after this phase is completed. |
| `cleaning up indexes` | `VACUUM` is currently cleaning up indexes. This occurs after the heap has been completely scanned and all vacuuming of the indexes and the heap has been completed. |
| `truncating heap` | `VACUUM` is currently truncating the heap so as to return empty pages at the end of the relation to the operating system. This occurs after cleaning up indexes. |
| `performing final cleanup` | `VACUUM` is performing final cleanup. During this phase, `VACUUM` will vacuum the free space map, update statistics in `pg_class`, and report statistics to the statistics collector. When this phase is completed, `VACUUM` will end. |

## 27.4.3. CLUSTER Progress Reporting

Whenever `CLUSTER` or `VACUUM FULL` is running, the `pg_stat_progress_cluster` view will contain a row for each backend that is currently running either command. The tables below describe the information that will be reported and provide information about how to interpret it.

#### **Table 27.26. `pg_stat_progress_cluster` View**

| Column | Type | Description |
| :--- | :--- | :--- |
| `pid` | `integer` | Process ID of backend. |
| `datid` | `oid` | OID of the database to which this backend is connected. |
| `datname` | `name` | Name of the database to which this backend is connected. |
| `relid` | `oid` | OID of the table being clustered. |
| `command` | `text` | The command that is running. Either `CLUSTER` or `VACUUM FULL`. |
| `phase` | `text` | Current processing phase. See [Table 27.27](https://www.postgresql.org/docs/12/progress-reporting.html#CLUSTER-PHASES). |
| `cluster_index_relid` | `oid` | If the table is being scanned using an index, this is the OID of the index being used; otherwise, it is zero. |
| `heap_tuples_scanned` | `bigint` | Number of heap tuples scanned. This counter only advances when the phase is `seq scanning heap`, `index scanning heap` or `writing new heap`. |
| `heap_tuples_written` | `bigint` | Number of heap tuples written. This counter only advances when the phase is `seq scanning heap`, `index scanning heap` or `writing new heap`. |
| `heap_blks_total` | `bigint` | Total number of heap blocks in the table. This number is reported as of the beginning of `seq scanning heap`. |
| `heap_blks_scanned` | `bigint` | Number of heap blocks scanned. This counter only advances when the phase is `seq scanning heap`. |
| `index_rebuild_count` | `bigint` | Number of indexes rebuilt. This counter only advances when the phase is `rebuilding index`. |

#### **Table 27.27. CLUSTER and VACUUM FULL Phases**

| Phase | Description |
| :--- | :--- |
| `initializing` | The command is preparing to begin scanning the heap. This phase is expected to be very brief. |
| `seq scanning heap` | The command is currently scanning the table using a sequential scan. |
| `index scanning heap` | `CLUSTER` is currently scanning the table using an index scan. |
| `sorting tuples` | `CLUSTER` is currently sorting tuples. |
| `writing new heap` | `CLUSTER` is currently writing the new heap. |
| `swapping relation files` | The command is currently swapping newly-built files into place. |
| `rebuilding index` | The command is currently rebuilding an index. |
| `performing final cleanup` | The command is performing final cleanup. When this phase is completed, `CLUSTER` or `VACUUM FULL` will end. |

