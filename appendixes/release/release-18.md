## E.6. Release 18 [#](#RELEASE-18)

[E.6.1. Overview](release-18.md#RELEASE-18-HIGHLIGHTS)

[E.6.2. Migration to Version 18](release-18.md#RELEASE-18-MIGRATION)

[E.6.3. Changes](release-18.md#RELEASE-18-CHANGES)

[E.6.4. Acknowledgments](release-18.md#RELEASE-18-ACKNOWLEDGEMENTS)

**Release date:**2025-09-25

<a id="RELEASE-18-HIGHLIGHTS"></a>

### E.6.1. Overview [#](#RELEASE-18-HIGHLIGHTS)

PostgreSQL 18 contains many new features
and enhancements, including:

* An asynchronous I/O (AIO) subsystem that can improve performance of
  sequential scans, bitmap heap scans, vacuums, and other operations.
* [pg_upgrade](../../reference/reference-server/pgupgrade.md)
  now retains optimizer statistics.
* Support for "skip scan" lookups that allow using
  [multicolumn B-tree indexes](../../the-sql-language/indexes/indexes-multicolumn.md) in
  more cases.
* [`uuidv7()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)
  function for generating timestamp-ordered
  [UUIDs](../../the-sql-language/datatype/datatype-uuid.md).
* Virtual
  [generated columns](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED)
  that compute their values during read operations. This is now the
  default for generated columns.
* [OAuth authentication](../../server-administration/client-authentication/auth-oauth.md) support.
* `OLD` and `NEW` support for
  [`RETURNING`](../../the-sql-language/dml/dml-returning.md) clauses
  in [INSERT](../../reference/sql-commands/sql-insert.md), [UPDATE](../../reference/sql-commands/sql-update.md),
  [DELETE](../../reference/sql-commands/sql-delete.md), and [MERGE](../../reference/sql-commands/sql-merge.md) commands.
* Temporal constraints, or constraints over ranges, for
  [PRIMARY KEY](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY),
  [UNIQUE](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE), and
  [FOREIGN KEY](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  constraints.

The above items and other new features of
PostgreSQL 18 are explained in more detail
in the sections below.

<a id="RELEASE-18-MIGRATION"></a>

### E.6.2. Migration to Version 18 [#](#RELEASE-18-MIGRATION)

A dump/restore using [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md) or use of
[pg_upgrade](../../reference/reference-server/pgupgrade.md) or logical replication is required for
those wishing to migrate data from any previous release. See [Section 18.6](../../server-administration/runtime/upgrading.md) for general information on migrating to new
major releases.

Version 18 contains a number of changes that may affect compatibility
with previous releases. Observe the following incompatibilities:

* Change [initdb](../../reference/reference-server/app-initdb.md) default to enable data checksums
  (Greg Sabino Mullane)
  [§](https://postgr.es/c/04bec894a04)

  Checksums can be disabled with the
  new initdb option
  `--no-data-checksums`. [pg_upgrade](../../reference/reference-server/pgupgrade.md)
  requires matching cluster checksum settings, so this new option can
  be useful to upgrade non-checksum old clusters.
* Change time zone abbreviation handling (Tom Lane)
  [§](https://postgr.es/c/d7674c9fa)

  The system will now favor the current session's time
  zone abbreviations before checking the server variable
  [timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS). Previously
  `timezone_abbreviations` was checked first.
* Deprecate [MD5 password](../../server-administration/client-authentication/auth-password.md)
  authentication (Nathan Bossart)
  [§](https://postgr.es/c/db6a4a985)

  Support for MD5 passwords will be removed in a future major
  version release. [CREATE ROLE](../../reference/sql-commands/sql-createrole.md) and [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) now emit deprecation warnings when
  setting MD5 passwords. These warnings can be disabled by setting
  the [md5_password_warnings](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MD5-PASSWORD-WARNINGS) parameter to
  `off`.
* Change [VACUUM](../../reference/sql-commands/sql-vacuum.md) and [ANALYZE](../../reference/sql-commands/sql-analyze.md)
  to process the inheritance children of a parent (Michael Harris)
  [§](https://postgr.es/c/62ddf7ee9)

  The previous behavior can be performed by using the new
  `ONLY` option.
* Prevent [`COPY FROM`](../../reference/sql-commands/sql-copy.md)
  from treating `\.` as an end-of-file marker when
  reading CSV files (Daniel Vérité, Tom Lane)
  [§](https://postgr.es/c/770233748)
  [§](https://postgr.es/c/da8a4c166)

  [psql](../../reference/reference-client/app-psql.md) will still treat
  `\.` as an end-of-file marker when reading
  CSV files from `STDIN`.
  Older psql clients connecting to
  PostgreSQL 18 servers might experience [`\copy`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMANDS-COPY)
  problems. This release also enforces that `\.`
  must appear alone on a line.
* Disallow unlogged partitioned tables (Michael Paquier)
  [§](https://postgr.es/c/e2bab2d79)

  Previously [`ALTER TABLE SET
  [UN]LOGGED`](../../reference/sql-commands/sql-altertable.md) did nothing, and the creation of an
  unlogged partitioned table did not cause its children to be unlogged.
* Execute `AFTER` [triggers](../../server-programming/triggers/README.md) as the role that was active when
  trigger events were queued (Laurenz Albe)
  [§](https://postgr.es/c/01463e1cc)

  Previously such triggers were run as the role that was active at
  trigger execution time (e.g., at [COMMIT](../../reference/sql-commands/sql-commit.md)).
  This is significant for cases where the role is changed between queue
  time and transaction commit.
* Remove non-functional support for rule privileges in [GRANT](../../reference/sql-commands/sql-grant.md)/[REVOKE](../../reference/sql-commands/sql-revoke.md) (Fujii Masao)
  [§](https://postgr.es/c/fefa76f70)

  These have been non-functional since
  PostgreSQL 8.2.
* Remove column [`pg_backend_memory_contexts`](../../internals/views/view-pg-backend-memory-contexts.md).`parent`
  (Melih Mutlu)
  [§](https://postgr.es/c/f0d112759)

  This is no longer needed since
  `pg_backend_memory_contexts`.`path`
  was added.
* Change
  `pg_backend_memory_contexts`.`level`
  and [`pg_log_backend_memory_contexts()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE)
  to be one-based (Melih Mutlu, Atsushi Torikoshi, David Rowley,
  Fujii Masao)
  [§](https://postgr.es/c/32d3ed816)
  [§](https://postgr.es/c/d9e03864b)
  [§](https://postgr.es/c/706cbed35)

  These were previously zero-based.
* Change [full text search](../../the-sql-language/textsearch/README.md) to use the
  default collation provider of the cluster to read configuration files
  and dictionaries, rather than always using libc (Peter Eisentraut)
  [§](https://postgr.es/c/fb1a18810f0)

  Clusters that default to non-libc collation providers (e.g., ICU,
  builtin) that behave differently than libc for characters processed
  by LC_CTYPE could observe changes in behavior of some full-text
  search functions, as well as the [pg_trgm](../contrib/pgtrgm.md) extension.
  When upgrading such clusters using [pg_upgrade](../../reference/reference-server/pgupgrade.md), it
  is recommended to reindex all indexes related to full-text search
  and pg_trgm after the upgrade.

<a id="RELEASE-18-CHANGES"></a>

### E.6.3. Changes [#](#RELEASE-18-CHANGES)

Below you will find a detailed account of the changes between
PostgreSQL 18 and the previous major
release.

<a id="RELEASE-18-SERVER"></a>

#### E.6.3.1. Server [#](#RELEASE-18-SERVER)

<a id="RELEASE-18-OPTIMIZER"></a>

##### E.6.3.1.1. Optimizer [#](#RELEASE-18-OPTIMIZER)

* Automatically remove some unnecessary table self-joins (Andrey
  Lepikhov, Alexander Kuzmenkov, Alexander Korotkov, Alena Rybakina)
  [§](https://postgr.es/c/fc069a3a6)

  This optimization can be disabled using server variable [enable_self_join_elimination](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-SELF-JOIN-ELIMINATION).
* Convert some [`IN (VALUES
  ...)`](../../the-sql-language/functions/functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR) to `x = ANY ...` for better
  optimizer statistics (Alena Rybakina, Andrei Lepikhov)
  [§](https://postgr.es/c/c0962a113)
* Allow transforming [`OR`](../../the-sql-language/functions/functions-logical.md)-clauses
  to arrays for faster index processing (Alexander Korotkov, Andrey
  Lepikhov)
  [§](https://postgr.es/c/ae4569161)
* Speed up the processing of [`INTERSECT`](../../reference/sql-commands/sql-select.md#SQL-INTERSECT),
  [`EXCEPT`](../../reference/sql-commands/sql-select.md#SQL-EXCEPT), [window aggregates](../../tutorial/tutorial-advanced/tutorial-window.md), and [view column aliases](../../reference/sql-commands/sql-createview.md) (Tom Lane,
  David Rowley)
  [§](https://postgr.es/c/52c707483)
  [§](https://postgr.es/c/276279295)
  [§](https://postgr.es/c/8d96f57d5)
  [§](https://postgr.es/c/908a96861)
* Allow the keys of [`SELECT
  DISTINCT`](../../reference/sql-commands/sql-select.md#SQL-DISTINCT) to be internally reordered to avoid sorting
  (Richard Guo)
  [§](https://postgr.es/c/a8ccf4e93)

  This optimization can be disabled using [enable_distinct_reordering](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-DISTINCT-REORDERING).
* Ignore [`GROUP BY`](../../reference/sql-commands/sql-select.md#SQL-GROUPBY)
  columns that are functionally dependent on other columns (Zhang
  Mingli, Jian He, David Rowley)
  [§](https://postgr.es/c/bd10ec529)

  If a `GROUP BY` clause includes all columns of
  a unique index, as well as other columns of the same table, those
  other columns are redundant and can be dropped from the grouping.
  This was already true for non-deferred primary keys.
* Allow some [`HAVING`](../../reference/sql-commands/sql-select.md#SQL-HAVING) clauses
  on [`GROUPING
  SETS`](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-GROUPING-SETS) to be pushed to [`WHERE`](../../reference/sql-commands/sql-select.md#SQL-WHERE) clauses
  (Richard Guo)
  [§](https://postgr.es/c/67a54b9e8)
  [§](https://postgr.es/c/247dea89f)
  [§](https://postgr.es/c/f5050f795)
  [§](https://postgr.es/c/cc5d98525)

  This allows earlier row filtering. This release also fixes some
  `GROUPING SETS` queries that used to return
  incorrect results.
* Improve row estimates for [`generate_series()`](../../the-sql-language/functions/functions-srf.md#FUNCTIONS-SRF-SERIES)
  using [`numeric`](../../the-sql-language/datatype/datatype-numeric.md)
  and [`timestamp`](../../the-sql-language/datatype/datatype-datetime.md)
  values (David Rowley, Song Jinzhou)
  [§](https://postgr.es/c/036bdcec9)
  [§](https://postgr.es/c/97173536e)
* Allow the optimizer to use `Right Semi Join` plans
  (Richard Guo)
  [§](https://postgr.es/c/aa86129e1)

  Semi-joins are used when needing to find if there is at least
  one match.
* Allow merge joins to use [incremental sorts](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-INCREMENTAL-SORT)
  (Richard Guo)
  [§](https://postgr.es/c/828e94c9d)
* Improve the efficiency of planning queries accessing many partitions
  (Ashutosh Bapat, Yuya Watari, David Rowley)
  [§](https://postgr.es/c/88f55bc97)
  [§](https://postgr.es/c/d69d45a5a)
* Allow [partitionwise
  joins](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARTITIONWISE-JOIN) in more cases, and reduce its memory usage (Richard Guo,
  Tom Lane, Ashutosh Bapat)
  [§](https://postgr.es/c/9b282a935)
  [§](https://postgr.es/c/513f4472a)
* Improve cost estimates of partition queries (Nikita Malakhov,
  Andrei Lepikhov)
  [§](https://postgr.es/c/fae535da0)
* Improve [SQL-language
  function](../../server-programming/extend/xfunc-sql.md) plan caching (Alexander Pyhalov, Tom Lane)
  [§](https://postgr.es/c/0dca5d68d)
  [§](https://postgr.es/c/09b07c295)
* Improve handling of disabled optimizer features (Robert Haas)
  [§](https://postgr.es/c/e22253467)

<a id="RELEASE-18-INDEXES"></a>

##### E.6.3.1.2. Indexes [#](#RELEASE-18-INDEXES)

* Allow skip scans of [btree](../../server-programming/extend/xfunc-sql.md) indexes
  (Peter Geoghegan)
  [§](https://postgr.es/c/92fe23d93)
  [§](https://postgr.es/c/8a510275d)

  This allows multi-column btree indexes to be used in more cases such
  as when there are no restrictions on the first or early indexed
  columns (or there are non-equality ones), and there are useful
  restrictions on later indexed columns.
* Allow non-btree unique indexes to be used as partition keys and in
  materialized views (Mark Dilger)
  [§](https://postgr.es/c/f278e1fe3)
  [§](https://postgr.es/c/9d6db8bec)

  The index type must still support equality.
* Allow [`GIN`](../../internals/indextypes/gin.md) indexes to
  be created in parallel (Tomas Vondra, Matthias van de Meent)
  [§](https://postgr.es/c/8492feb98)
* Allow values to be sorted to speed range-type [GiST](../../internals/indextypes/gist.md) and [btree](../../internals/indextypes/btree.md)
  index builds (Bernd Helmle)
  [§](https://postgr.es/c/e9e7b6604)

<a id="RELEASE-18-PERFORMANCE"></a>

##### E.6.3.1.3. General Performance [#](#RELEASE-18-PERFORMANCE)

* Add an asynchronous I/O subsystem (Andres Freund, Thomas Munro,
  Nazir Bilal Yavuz, Melanie Plageman)
  [§](https://postgr.es/c/02844012b)
  [§](https://postgr.es/c/da7226993)
  [§](https://postgr.es/c/55b454d0e)
  [§](https://postgr.es/c/247ce06b8)
  [§](https://postgr.es/c/10f664684)
  [§](https://postgr.es/c/06fb5612c)
  [§](https://postgr.es/c/c325a7633)
  [§](https://postgr.es/c/50cb7505b)
  [§](https://postgr.es/c/047cba7fa)
  [§](https://postgr.es/c/12ce89fd0)
  [§](https://postgr.es/c/2a5e709e7)

  This feature allows backends to queue multiple read requests,
  which allows for more efficient sequential scans, bitmap
  heap scans, vacuums, etc. This is enabled by server
  variable [io_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-METHOD), with server
  variables [io_combine_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-COMBINE-LIMIT) and [io_max_combine_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-MAX-COMBINE-LIMIT) added to control it.
  This also enables [effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY)
  and [maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)
  values greater than zero for systems without
  `fadvise()` support. The new system view [`pg_aios`](../../internals/views/view-pg-aios.md)
  shows the file handles being used for asynchronous I/O.
* Improve the locking performance of queries that access many relations
  (Tomas Vondra)
  [§](https://postgr.es/c/c4d5cb71d)
* Improve the performance and reduce memory usage of hash joins and
  [`GROUP BY`](../../reference/sql-commands/sql-select.md#SQL-GROUPBY)
  (David Rowley, Jeff Davis)
  [§](https://postgr.es/c/adf97c156)
  [§](https://postgr.es/c/0f5738202)
  [§](https://postgr.es/c/4d143509c)
  [§](https://postgr.es/c/a0942f441)
  [§](https://postgr.es/c/626df47ad)

  This also improves hash set operations used by [`EXCEPT`](../../reference/sql-commands/sql-select.md#SQL-EXCEPT), and hash
  lookups of subplan values.
* Allow normal vacuums to freeze some pages, even though they are
  all-visible (Melanie Plageman)
  [§](https://postgr.es/c/052026c9b)
  [§](https://postgr.es/c/06eae9e62)

  This reduces the overhead of later full-relation
  freezing. The aggressiveness of this can be
  controlled by server variable and per-table setting [vacuum_max_eager_freeze_failure_rate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE). Previously
  vacuum never processed all-visible pages until freezing was required.
* Add server variable [vacuum_truncate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE) to control
  file truncation during [VACUUM](../../reference/sql-commands/sql-vacuum.md) (Nathan Bossart,
  Gurjeet Singh)
  [§](https://postgr.es/c/0164a0f9e)

  A storage-level parameter with the same name and behavior already
  existed.
* Increase server variables [effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY)'s and [maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)'s default values to 16
  (Melanie Plageman)
  [§](https://postgr.es/c/ff79b5b2a)
  [§](https://postgr.es/c/cc6be07eb)

  This more accurately reflects modern hardware.

<a id="RELEASE-18-MONITORING"></a>

##### E.6.3.1.4. Monitoring [#](#RELEASE-18-MONITORING)

* Increase the logging granularity of server variable [log_connections](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-CONNECTIONS) (Melanie Plageman)
  [§](https://postgr.es/c/9219093ca)

  This server variable was previously only boolean, which is still
  supported.
* Add `log_connections` option to report the duration
  of connection stages (Melanie Plageman)
  [§](https://postgr.es/c/18cd15e70)
* Add [log_line_prefix](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-LINE-PREFIX) escape
  `%L` to output the client IP
  address (Greg Sabino Mullane)
  [§](https://postgr.es/c/3516ea768)
* Add server variable [log_lock_failures](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-LOCK-FAILURES) to log
  lock acquisition failures (Yuki Seino, Fujii Masao)
  [§](https://postgr.es/c/6d376c3b0)
  [§](https://postgr.es/c/73bdcfab3)

  Specifically it reports [`SELECT
  ... NOWAIT`](../../reference/sql-commands/sql-select.md#SQL-FOR-UPDATE-SHARE) lock failures.
* Modify [`pg_stat_all_tables`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)
  and its variants to report the time spent in [VACUUM](../../reference/sql-commands/sql-vacuum.md), [ANALYZE](../../reference/sql-commands/sql-analyze.md), and their
  [automatic](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM) variants (Sami Imseih)
  [§](https://postgr.es/c/30a6ed0ce)

  The new columns are `total_vacuum_time`,
  `total_autovacuum_time`,
  `total_analyze_time`, and
  `total_autoanalyze_time`.
* Add delay time reporting to [VACUUM](../../reference/sql-commands/sql-vacuum.md) and [ANALYZE](../../reference/sql-commands/sql-analyze.md) (Bertrand Drouvot, Nathan Bossart)
  [§](https://postgr.es/c/bb8dff999)
  [§](https://postgr.es/c/7720082ae)

  This information appears in the server log, the system views [`pg_stat_progress_vacuum`](../../server-administration/monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING)
  and [`pg_stat_progress_analyze`](../../server-administration/monitoring/progress-reporting.md#PG-STAT-PROGRESS-ANALYZE-VIEW),
  and the output of [VACUUM](../../reference/sql-commands/sql-vacuum.md) and [ANALYZE](../../reference/sql-commands/sql-analyze.md) when in `VERBOSE`
  mode; tracking must be enabled with the server variable [track_cost_delay_timing](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING).
* Add WAL, CPU, and average
  read statistics output to `ANALYZE VERBOSE`
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/4c1b4cdb8)
  [§](https://postgr.es/c/bb7775234)
* Add full WAL buffer count to
  `VACUUM`/`ANALYZE (VERBOSE)`
  and autovacuum log output (Bertrand Drouvot)
  [§](https://postgr.es/c/6a8a7ce47)
* Add per-backend I/O statistics reporting (Bertrand Drouvot)
  [§](https://postgr.es/c/9aea73fc6)
  [§](https://postgr.es/c/3f1db99bf)

  The statistics are accessed via [`pg_stat_get_backend_io()`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO).
  Per-backend I/O statistics can be cleared via [`pg_stat_reset_backend_stats()`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE).
* Add [`pg_stat_io`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)
  columns to report I/O activity in bytes (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/f92c854cf)

  The new columns are `read_bytes`,
  `write_bytes`, and
  `extend_bytes`. The
  `op_bytes` column, which always equaled
  [`BLCKSZ`](../../server-administration/runtime-config/runtime-config-preset.md#GUC-BLOCK-SIZE),
  has been removed.
* Add WAL I/O activity rows to
  `pg_stat_io` (Nazir Bilal Yavuz, Bertrand
  Drouvot, Michael Paquier)
  [§](https://postgr.es/c/a051e71e2)
  [§](https://postgr.es/c/4538bd3f1)
  [§](https://postgr.es/c/7f7f324eb)

  This includes WAL receiver activity and a wait
  event for such writes.
* Change server variable [track_wal_io_timing](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING)
  to control tracking WAL timing
  in `pg_stat_io` instead of [`pg_stat_wal`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-WAL-VIEW)
  (Bertrand Drouvot)
  [§](https://postgr.es/c/6c349d83b)
* Remove read/sync columns from `pg_stat_wal`
  (Bertrand Drouvot)
  [§](https://postgr.es/c/2421e9a51)
  [§](https://postgr.es/c/6c349d83b)

  This removes columns `wal_write`,
  `wal_sync`,
  `wal_write_time`, and
  `wal_sync_time`.
* Add function [`pg_stat_get_backend_wal()`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-WAL)
  to return per-backend WAL statistics (Bertrand
  Drouvot)
  [§](https://postgr.es/c/76def4cdd)

  Per-backend WAL
  statistics can be cleared via [`pg_stat_reset_backend_stats()`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE).
* Add function [`pg_ls_summariesdir()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-GENFILE-TABLE)
  to specifically list the contents of [`PGDATA`](../../internals/storage/storage-file-layout.md)/[`pg_wal/summaries`](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-SUMMARY-KEEP-TIME)
  (Yushi Ogiwara)
  [§](https://postgr.es/c/4e1fad378)
* Add column [`pg_stat_checkpointer`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW).`num_done`
  to report the number of completed checkpoints (Anton A. Melnikov)
  [§](https://postgr.es/c/559efce1d)

  Columns `num_timed` and
  `num_requested` count both completed and
  skipped checkpoints.
* Add column
  `pg_stat_checkpointer`.`slru_written`
  to report SLRU buffers written (Nitin Jadhav)
  [§](https://postgr.es/c/17cc5f666)

  Also, modify the checkpoint server log message to report separate
  shared buffer and SLRU buffer values.
* Add columns to [`pg_stat_database`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)
  to report parallel worker activity (Benoit Lobréau)
  [§](https://postgr.es/c/e7a9496de)

  The new columns are
  `parallel_workers_to_launch` and
  `parallel_workers_launched`.
* Have [query id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) computation
  of constant lists consider only the first and last constants (Dmitry
  Dolgov, Sami Imseih)
  [§](https://postgr.es/c/62d712ecf)
  [§](https://postgr.es/c/9fbd53dea)
  [§](https://postgr.es/c/c2da1a5d6)

  Jumbling is used by [pg_stat_statements](../contrib/pgstatstatements.md).
* Adjust query id computations to group together queries using the
  same relation name (Michael Paquier, Sami Imseih)
  [§](https://postgr.es/c/787514b30)

  This is true even if the tables in different schemas have different
  column names.
* Add column [`pg_backend_memory_contexts`](../../internals/views/view-pg-backend-memory-contexts.md).`type`
  to report the type of memory context (David Rowley)
  [§](https://postgr.es/c/12227a1d5)
* Add column
  `pg_backend_memory_contexts`.`path`
  to show memory context parents (Melih Mutlu)
  [§](https://postgr.es/c/32d3ed816)

<a id="RELEASE-18-PRIVILEGES"></a>

##### E.6.3.1.5. Privileges [#](#RELEASE-18-PRIVILEGES)

* Add function [`pg_get_acl()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE)
  to retrieve database access control details (Joel Jacobson)
  [§](https://postgr.es/c/4564f1ceb)
  [§](https://postgr.es/c/d898665bf)
* Add function [`has_largeobject_privilege()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE)
  to check large object privileges (Yugo Nagata)
  [§](https://postgr.es/c/4eada203a)
* Allow [ALTER DEFAULT PRIVILEGES](../../reference/sql-commands/sql-alterdefaultprivileges.md) to define
  large object default privileges (Takatsuka Haruka, Yugo Nagata,
  Laurenz Albe)
  [§](https://postgr.es/c/0d6c47766)
* Add predefined role [`pg_signal_autovacuum_worker`](../../server-administration/user-manag/predefined-roles.md)
  (Kirill Reshke)
  [§](https://postgr.es/c/ccd38024b)

  This allows sending signals to autovacuum workers.

<a id="RELEASE-18-SERVER-CONFIG"></a>

##### E.6.3.1.6. Server Configuration [#](#RELEASE-18-SERVER-CONFIG)

* Add support for the [OAuth authentication
  method](../../server-administration/client-authentication/auth-oauth.md) (Jacob Champion, Daniel Gustafsson, Thomas Munro)
  [§](https://postgr.es/c/b3f0be788)

  This adds an `oauth` authentication method to [`pg_hba.conf`](../../server-administration/client-authentication/auth-pg-hba-conf.md),
  libpq OAuth options, a server variable [oauth_validator_libraries](../../server-administration/runtime-config/runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES) to load
  token validation libraries, and a configure flag [`--with-libcurl`](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)
  to add the required compile-time libraries.
* Add server variable [ssl_tls13_ciphers](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-TLS13-CIPHERS) to allow
  specification of multiple colon-separated TLSv1.3 cipher suites
  (Erica Zhang, Daniel Gustafsson)
  [§](https://postgr.es/c/45188c2ea)
* Change server variable [ssl_groups](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-GROUPS)'s default
  to include elliptic curve X25519 (Daniel Gustafsson, Jacob Champion)
  [§](https://postgr.es/c/daa02c6bd)
* Rename server variable `ssl_ecdh_curve` to [ssl_groups](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-GROUPS) and allow multiple colon-separated
  ECDH curves to be specified (Erica Zhang,
  Daniel Gustafsson)
  [§](https://postgr.es/c/3d1ef3a15)

  The previous name still works.
* Make [cancel request
  keys](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE) 256 bits (Heikki Linnakangas, Jelte Fennema-Nio)
  [§](https://postgr.es/c/a460251f0)
  [§](https://postgr.es/c/9d9b9d46f)

  This is only possible when the server and client support wire
  protocol version 3.2, introduced in this release.
* Add server variable [autovacuum_worker_slots](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)
  to specify the maximum number of background workers (Nathan Bossart)
  [§](https://postgr.es/c/c758119e5)

  With this variable set, [autovacuum_max_workers](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)
  can be adjusted at runtime up to this maximum without a server
  restart.
* Allow specification of the fixed number of dead tuples that will
  trigger an [autovacuum](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM) (Nathan
  Bossart, Frédéric Yhuel)
  [§](https://postgr.es/c/306dc520b)

  The server variable is [autovacuum_vacuum_max_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD). Percentages are
  still used for triggering.
* Change server variable [max_files_per_process](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-FILES-PER-PROCESS)
  to limit only files opened by a backend (Andres Freund)
  [§](https://postgr.es/c/adb5f85fa)

  Previously files opened by the postmaster were also counted toward
  this limit.
* Add server variable [num_os_semaphores](../../server-administration/runtime-config/runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES) to
  report the required number of semaphores (Nathan Bossart)
  [§](https://postgr.es/c/0dcaea569)

  This is useful for operating system configuration.
* Add server variable [extension_control_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) to
  specify the location of extension control files (Peter Eisentraut,
  Matheus Alcantara)
  [§](https://postgr.es/c/4f7f7b037)
  [§](https://postgr.es/c/81eaaa2c4)

<a id="RELEASE-18-REPLICATION"></a>

##### E.6.3.1.7. Streaming Replication and Recovery [#](#RELEASE-18-REPLICATION)

* Allow inactive replication slots to be automatically invalidated using
  server variable [idle_replication_slot_timeout](../../server-administration/runtime-config/runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT)
  (Nisha Moond, Bharath Rupireddy)
  [§](https://postgr.es/c/ac0e33136)
* Add server variable [max_active_replication_origins](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) to control the
  maximum active replication origins (Euler Taveira)
  [§](https://postgr.es/c/04ff636cb)

  This was previously controlled by [max_replication_slots](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS), but this new setting allows
  a higher origin count in cases where fewer slots are required.

<a id="RELEASE-18-LOGICAL"></a>

##### E.6.3.1.8. [Logical Replication](../../server-administration/logical-replication/README.md) [#](#RELEASE-18-LOGICAL)

* Allow the values of [generated
  columns](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED) to be logically replicated (Shubham Khanna, Vignesh C,
  Zhijie Hou, Shlok Kyal, Peter Smith)
  [§](https://postgr.es/c/745217a05)
  [§](https://postgr.es/c/7054186c4)
  [§](https://postgr.es/c/87ce27de6)
  [§](https://postgr.es/c/6252b1eaf)

  If the publication specifies a column list, all specified
  columns, generated and non-generated, are published.
  Without a specified column list, publication option
  `publish_generated_columns` controls whether
  generated columns are published. Previously generated columns
  were not replicated and the subscriber had to compute
  the values if possible; this is particularly useful for
  non-PostgreSQL subscribers which lack
  such a capability.
* Change the default [CREATE SUBSCRIPTION](../../reference/sql-commands/sql-createsubscription.md) streaming
  option from `off` to `parallel`
  (Vignesh C)
  [§](https://postgr.es/c/1bf1140be)
* Allow [ALTER SUBSCRIPTION](../../reference/sql-commands/sql-altersubscription.md) to change the
  replication slot's two-phase commit behavior (Hayato Kuroda, Ajin
  Cherian, Amit Kapila, Zhijie Hou)
  [§](https://postgr.es/c/1462aad2e)
  [§](https://postgr.es/c/4868c96bc)
* Log [conflicts](../../server-administration/high-availability/hot-standby.md#HOT-STANDBY-CONFLICT) while
  applying logical replication changes (Zhijie Hou, Nisha Moond)
  [§](https://postgr.es/c/9758174e2)
  [§](https://postgr.es/c/edcb71258)
  [§](https://postgr.es/c/640178c92)
  [§](https://postgr.es/c/6c2b5edec)
  [§](https://postgr.es/c/73eba5004)

  Also report in new columns of [`pg_stat_subscription_stats`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS).

<a id="RELEASE-18-UTILITY"></a>

#### E.6.3.2. Utility Commands [#](#RELEASE-18-UTILITY)

* Allow [generated
  columns](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED) to be virtual, and make them the default (Peter
  Eisentraut, Jian He, Richard Guo, Dean Rasheed)
  [§](https://postgr.es/c/83ea6c540)
  [§](https://postgr.es/c/cdc168ad4)
  [§](https://postgr.es/c/1e4351af3)

  Virtual generated columns generate their values when the columns
  are read, not written. The write behavior can still be specified
  via the `STORED` option.
* Add `OLD`/`NEW` support to [`RETURNING`](../../the-sql-language/dml/dml-returning.md) in
  DML queries (Dean Rasheed)
  [§](https://postgr.es/c/80feb727c)

  Previously `RETURNING` only returned new values for
  [INSERT](../../reference/sql-commands/sql-insert.md) and [UPDATE](../../reference/sql-commands/sql-update.md), and old
  values for [DELETE](../../reference/sql-commands/sql-delete.md); [MERGE](../../reference/sql-commands/sql-merge.md)
  would return the appropriate value for the internal query executed.
  This new syntax allows the `RETURNING` list of
  `INSERT`/`UPDATE`/`DELETE`/`MERGE`
  to explicitly return old and new values by using the special aliases
  `old` and `new`. These aliases
  can be renamed to avoid identifier conflicts.
* Allow foreign tables to be created like existing local tables
  (Zhang Mingli)
  [§](https://postgr.es/c/302cf1575)

  The syntax is [`CREATE
  FOREIGN TABLE ... LIKE`](../../reference/sql-commands/sql-createforeigntable.md).
* Allow [`LIKE`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-LIKE)
  with [nondeterministic
  collations](../../server-administration/charset/collation.md#COLLATION-NONDETERMINISTIC) (Peter Eisentraut)
  [§](https://postgr.es/c/85b7efa1c)
* Allow text position search functions with nondeterministic collations
  (Peter Eisentraut)
  [§](https://postgr.es/c/329304c90)

  These used to generate an error.
* Add builtin collation provider [`PG_UNICODE_FAST`](../../server-administration/charset/locale.md#LOCALE-PROVIDERS)
  (Jeff Davis)
  [§](https://postgr.es/c/d3d098316)

  This locale supports case mapping, but sorts in code point order,
  not natural language order.
* Allow [VACUUM](../../reference/sql-commands/sql-vacuum.md) and [ANALYZE](../../reference/sql-commands/sql-analyze.md)
  to process partitioned tables without processing their children
  (Michael Harris)
  [§](https://postgr.es/c/62ddf7ee9)

  This is enabled with the new `ONLY` option. This is
  useful since autovacuum does not process partitioned tables, just
  its children.
* Add functions to modify per-relation and per-column optimizer
  statistics (Corey Huinker)
  [§](https://postgr.es/c/e839c8ecc)
  [§](https://postgr.es/c/d32d14639)
  [§](https://postgr.es/c/650ab8aaf)

  The functions are [`pg_restore_relation_stats()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-STATSMOD),
  `pg_restore_attribute_stats()`,
  `pg_clear_relation_stats()`, and
  `pg_clear_attribute_stats()`.
* Add server variable [file_copy_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-COPY-METHOD) to control
  the file copying method (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/f78ca6f3e)

  This controls whether [`CREATE DATABASE
  ... STRATEGY=FILE_COPY`](../../reference/sql-commands/sql-createdatabase.md) and [`ALTER DATABASE ... SET
  TABLESPACE`](../../reference/sql-commands/sql-alterdatabase.md) uses file copy or clone.

<a id="RELEASE-18-CONSTRAINTS"></a>

##### E.6.3.2.1. [Constraints](../../the-sql-language/ddl/ddl-constraints.md) [#](#RELEASE-18-CONSTRAINTS)

* Allow the specification of non-overlapping [`PRIMARY
  KEY`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY), [`UNIQUE`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE), and
  [foreign key](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  constraints (Paul A. Jungwirth)
  [§](https://postgr.es/c/fc0438b4e)
  [§](https://postgr.es/c/89f908a6d)

  This is specified by `WITHOUT OVERLAPS` for
  `PRIMARY KEY` and `UNIQUE`, and by
  `PERIOD` for foreign keys, all applied to the last
  specified column.
* Allow [`CHECK`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-CHECK)
  and [foreign
  key](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES) constraints to be specified as `NOT
  ENFORCED` (Amul Sul)
  [§](https://postgr.es/c/ca87c415e)
  [§](https://postgr.es/c/eec0040c4)

  This also adds column [`pg_constraint`](../../internals/catalogs/catalog-pg-constraint.md).`conenforced`.
* Require [primary/foreign key](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  relationships to use either deterministic collations or the the
  same nondeterministic collations (Peter Eisentraut)
  [§](https://postgr.es/c/9321d2fdf)

  The restore of a [pg_dump](../../reference/reference-client/app-pgdump.md), also used by [pg_upgrade](../../reference/reference-server/pgupgrade.md), will fail if these requirements are not met;
  schema changes must be made for these upgrade methods to succeed.
* Store column [`NOT
  NULL`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-NOT-NULL) specifications in [`pg_constraint`](../../internals/catalogs/catalog-pg-constraint.md)
  (Álvaro Herrera, Bernd Helmle)
  [§](https://postgr.es/c/14e87ffa5)
  [§](https://postgr.es/c/81ce602d4)

  This allows names to be specified for `NOT NULL`
  constraint. This also adds `NOT NULL` constraints
  to foreign tables and `NOT NULL` inheritance
  control to local tables.
* Allow [ALTER TABLE](../../reference/sql-commands/sql-altertable.md) to set the `NOT
  VALID` attribute of `NOT NULL` constraints
  (Rushabh Lathia, Jian He)
  [§](https://postgr.es/c/a379061a2)
* Allow modification of the inheritability of `NOT
  NULL` constraints (Suraj Kharage, Álvaro Herrera)
  [§](https://postgr.es/c/f4e53e10b)
  [§](https://postgr.es/c/4a02af8b1)

  The syntax is [`ALTER TABLE
  ... ALTER CONSTRAINT ... [NO] INHERIT`](../../reference/sql-commands/sql-altertable.md).
* Allow `NOT VALID` foreign key constraints on
  partitioned tables (Amul Sul)
  [§](https://postgr.es/c/b663b9436)
* Allow [dropping](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-DESC-DROP-CONSTRAINT)
  of constraints `ONLY` on partitioned tables
  (Álvaro Herrera)
  [§](https://postgr.es/c/4dea33ce7)

  This was previously erroneously prohibited.

<a id="RELEASE-18-COPY"></a>

##### E.6.3.2.2. [COPY](../../reference/sql-commands/sql-copy.md) [#](#RELEASE-18-COPY)

* Add `REJECT_LIMIT` to control the number of invalid
  rows `COPY FROM` can ignore (Atsushi Torikoshi)
  [§](https://postgr.es/c/4ac2a9bec)

  This is available when `ON_ERROR = 'ignore'`.
* Allow `COPY TO` to copy rows from populated
  materialized views (Jian He)
  [§](https://postgr.es/c/534874fac)
* Add `COPY` `LOG_VERBOSITY` level
  `silent` to suppress log output of ignored rows
  (Atsushi Torikoshi)
  [§](https://postgr.es/c/e7834a1a2)

  This new level suppresses output for discarded input rows when
  `on_error = 'ignore'`.
* Disallow `COPY FREEZE` on foreign tables (Nathan
  Bossart)
  [§](https://postgr.es/c/401a6956f)

  Previously, the `COPY` worked but the
  `FREEZE` was ignored, so disallow this command.

<a id="RELEASE-18-EXPLAIN"></a>

##### E.6.3.2.3. [EXPLAIN](../../reference/sql-commands/sql-explain.md) [#](#RELEASE-18-EXPLAIN)

* Automatically include `BUFFERS` output in
  `EXPLAIN ANALYZE` (Guillaume Lelarge, David Rowley)
  [§](https://postgr.es/c/c2a4078eb)
* Add full WAL buffer count to `EXPLAIN
  (WAL)` output (Bertrand Drouvot)
  [§](https://postgr.es/c/320545bfc)
* In `EXPLAIN ANALYZE`, report the number of index
  lookups used per index scan node (Peter Geoghegan)
  [§](https://postgr.es/c/0fbceae84)
* Modify `EXPLAIN` to output fractional row counts
  (Ibrar Ahmed, Ilia Evdokimov, Robert Haas)
  [§](https://postgr.es/c/ddb17e387)
  [§](https://postgr.es/c/95dbd827f)
* Add memory and disk usage details to `Material`,
  `Window Aggregate`, and common table expression
  nodes to `EXPLAIN` output (David Rowley, Tatsuo
  Ishii)
  [§](https://postgr.es/c/1eff8279d)
  [§](https://postgr.es/c/53abb1e0e)
  [§](https://postgr.es/c/95d6e9af0)
  [§](https://postgr.es/c/40708acd6)
* Add details about window function arguments to
  `EXPLAIN` output (Tom Lane)
  [§](https://postgr.es/c/8b1b34254)
* Add `Parallel Bitmap Heap Scan` worker cache
  statistics to `EXPLAIN ANALYZE` (David Geier,
  Heikki Linnakangas, Donghang Lin, Alena Rybakina, David Rowley)
  [§](https://postgr.es/c/5a1e6df3b)
* Indicate disabled nodes in `EXPLAIN ANALYZE` output
  (Robert Haas, David Rowley, Laurenz Albe)
  [§](https://postgr.es/c/c01743aa4)
  [§](https://postgr.es/c/161320b4b)
  [§](https://postgr.es/c/84b8fccbe)

<a id="RELEASE-18-DATATYPES"></a>

#### E.6.3.3. Data Types [#](#RELEASE-18-DATATYPES)

* Improve [Unicode](../../server-administration/charset/collation.md#COLLATION-MANAGING-STANDARD)
  full case mapping and conversion (Jeff Davis)
  [§](https://postgr.es/c/4e7f62bc3)
  [§](https://postgr.es/c/286a365b9)

  This adds the ability to do conditional and title case mapping,
  and case map single characters to multiple characters.
* Allow [`jsonb`](../../the-sql-language/datatype/datatype-json.md)
  `null` values to be cast to scalar types as
  `NULL` (Tom Lane)
  [§](https://postgr.es/c/a5579a90a)

  Previously such casts generated an error.
* Add optional parameter to [`json{b}_strip_nulls`](../../the-sql-language/functions/functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE)
  to allow removal of null array elements (Florents Tselai)
  [§](https://postgr.es/c/4603903d2)
* Add function [`array_sort()`](../../the-sql-language/functions/functions-array.md#ARRAY-FUNCTIONS-TABLE)
  which sorts an array's first dimension (Junwang Zhao, Jian He)
  [§](https://postgr.es/c/6c12ae09f)
* Add function [`array_reverse()`](../../the-sql-language/functions/functions-array.md#ARRAY-FUNCTIONS-TABLE)
  which reverses an array's first dimension (Aleksander Alekseev)
  [§](https://postgr.es/c/49d6c7d8d)
* Add function [`reverse()`](../../the-sql-language/functions/functions-string.md#FUNCTIONS-STRING-OTHER)
  to reverse bytea bytes (Aleksander Alekseev)
  [§](https://postgr.es/c/0697b2390)
* Allow casting between integer types and [`bytea`](../../the-sql-language/datatype/datatype-binary.md) (Aleksander
  Alekseev)
  [§](https://postgr.es/c/6da469bad)

  The integer values are stored as `bytea` two's complement
  values.
* Update Unicode data to [Unicode](../../server-administration/charset/collation.md#COLLATION-MANAGING-STANDARD) 16.0.0 (Peter
  Eisentraut)
  [§](https://postgr.es/c/82a46cca9)
* Add full text search [stemming](../../the-sql-language/textsearch/textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY) for Estonian
  (Tom Lane)
  [§](https://postgr.es/c/b464e51ab)
* Improve the [`XML`](../../the-sql-language/datatype/datatype-xml.md)
  error codes to more closely match the SQL standard
  (Tom Lane)
  [§](https://postgr.es/c/cd838e200)

  These errors are reported via [`SQLSTATE`](../errcodes-appendix/README.md).

<a id="RELEASE-18-FUNCTIONS"></a>

#### E.6.3.4. Functions [#](#RELEASE-18-FUNCTIONS)

* Add function [`casefold()`](../../the-sql-language/functions/functions-string.md#FUNCTIONS-STRING-OTHER)
  to allow for more sophisticated case-insensitive matching (Jeff Davis)
  [§](https://postgr.es/c/bfc599206)

  This allows more accurate comparisons, i.e., a character can have
  multiple upper or lower case equivalents, or upper or lower case
  conversion changes the number of characters.
* Allow [`MIN()`](../../the-sql-language/functions/functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE)/[`MAX()`](../../the-sql-language/functions/functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE)
  aggregates on arrays and composite types (Aleksander Alekseev,
  Marat Buharov)
  [§](https://postgr.es/c/a0f1fce80)
  [§](https://postgr.es/c/2d24fd942)
* Add a `WEEK` option to [`EXTRACT()`](../../the-sql-language/functions/functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)
  (Tom Lane)
  [§](https://postgr.es/c/6be39d77a)
* Improve the output `EXTRACT(QUARTER ...)` for
  negative values (Tom Lane)
  [§](https://postgr.es/c/6be39d77a)
* Add roman numeral support to [`to_number()`](../../the-sql-language/functions/functions-formatting.md#FUNCTIONS-FORMATTING-TABLE)
  (Hunaid Sohail)
  [§](https://postgr.es/c/172e6b3ad)

  This is accessed via the `RN` pattern.
* Add [`UUID`](../../the-sql-language/datatype/datatype-uuid.md)
  version 7 generation function [`uuidv7()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)
  (Andrey Borodin)
  [§](https://postgr.es/c/78c5e141e)

  This `UUID` value is
  temporally sortable. Function alias [`uuidv4()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)
  has been added to explicitly generate version 4 UUIDs.
* Add functions [`crc32()`](../../the-sql-language/functions/functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)
  and [`crc32c()`](../../the-sql-language/functions/functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)
  to compute CRC values (Aleksander Alekseev)
  [§](https://postgr.es/c/760162fed)
* Add math functions [`gamma()`](../../the-sql-language/functions/functions-math.md#FUNCTIONS-MATH-FUNC-TABLE)
  and [`lgamma()`](../../the-sql-language/functions/functions-math.md#FUNCTIONS-MATH-FUNC-TABLE)
  (Dean Rasheed)
  [§](https://postgr.es/c/a3b6dfd41)
* Allow `=>` syntax for named cursor arguments in
  [PL/pgSQL](../../server-programming/plpgsql/README.md) (Pavel Stehule)
  [§](https://postgr.es/c/246dedc5d)

  We previously only accepted `:=`.
* Allow [`regexp_match[es]()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_like()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_replace()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_count()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_instr()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_substr()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_split_to_table()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_split_to_array()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)
  to use named arguments (Jian He)
  [§](https://postgr.es/c/580f8727c)

<a id="RELEASE-18-LIBPQ"></a>

#### E.6.3.5. [Libpq](../../client-interfaces/libpq/README.md) [#](#RELEASE-18-LIBPQ)

* Add function [`PQfullProtocolVersion()`](../../client-interfaces/libpq/libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION)
  to report the full, including minor, protocol version number (Jacob
  Champion, Jelte Fennema-Nio)
  [§](https://postgr.es/c/cdb6b0fdb)
* Add libpq connection [parameters](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION)
  and [environment variables](../../client-interfaces/libpq/libpq-envars.md) to
  specify the minimum and maximum acceptable protocol version for
  connections (Jelte Fennema-Nio)
  [§](https://postgr.es/c/285613c60)
  [§](https://postgr.es/c/507034910)
* Report [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) changes to the client
  (Alexander Kukushkin, Jelte Fennema-Nio, Tomas Vondra)
  [§](https://postgr.es/c/28a1121fd)
  [§](https://postgr.es/c/0d06a7eac)
* Add [`PQtrace()`](../../client-interfaces/libpq/libpq-control.md#LIBPQ-PQTRACE) output
  for all message types, including authentication (Jelte Fennema-Nio)
  [§](https://postgr.es/c/ea92f3a0a)
  [§](https://postgr.es/c/a5c6b8f22)
  [§](https://postgr.es/c/b8b3f861f)
  [§](https://postgr.es/c/e87c14b19)
  [§](https://postgr.es/c/7adec2d5f)
* Add libpq connection parameter [`sslkeylogfile`](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-SSLKEYLOGFILE)
  which dumps out SSL key material (Abhishek Chanda,
  Daniel Gustafsson)
  [§](https://postgr.es/c/2da74d8d6)

  This is useful for debugging.
* Modify some libpq function signatures to use
  `int64_t` (Thomas Munro)
  [§](https://postgr.es/c/3c86223c9)

  These previously used `pg_int64`, which is now
  deprecated.

<a id="RELEASE-18-PSQL"></a>

#### E.6.3.6. [psql](../../reference/reference-client/app-psql.md) [#](#RELEASE-18-PSQL)

* Allow psql to parse, bind, and close
  named prepared statements (Anthonin Bonnefoy, Michael Paquier)
  [§](https://postgr.es/c/d55322b0d)
  [§](https://postgr.es/c/fc39b286a)

  This is accomplished with new commands [`\parse`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-PARSE),
  [`\bind_named`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-BIND-NAMED),
  and [`\close_prepared`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-CLOSE-PREPARED).
* Add psql backslash commands to allowing
  issuance of pipeline queries (Anthonin Bonnefoy)
  [§](https://postgr.es/c/41625ab8e)
  [§](https://postgr.es/c/17caf6644)
  [§](https://postgr.es/c/2cce0fe44)

  The new commands are [`\startpipeline`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-PIPELINE),
  `\syncpipeline`, `\sendpipeline`,
  `\endpipeline`, `\flushrequest`,
  `\flush`, and `\getresults`.
* Allow adding pipeline status to the psql
  prompt and add related state variables (Anthonin Bonnefoy)
  [§](https://postgr.es/c/3ce357584)

  The new prompt character is `%P` and
  the new psql variables are [`PIPELINE_SYNC_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT),
  [`PIPELINE_COMMAND_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-COMMAND-COUNT),
  and [`PIPELINE_RESULT_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT).
* Allow adding the connection service name to the
  psql prompt or access it via
  psql variable (Michael Banck)
  [§](https://postgr.es/c/477728b5d)
* Add psql option to use expanded mode on
  all list commands (Dean Rasheed)
  [§](https://postgr.es/c/00f4c2959)

  Adding backslash suffix `x` enables this.
* Change psql's [`\conninfo`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-CONNINFO) to use tabular format
  and include more information (Álvaro Herrera, Maiquel Grassi,
  Hunaid Sohail)
  [§](https://postgr.es/c/bba2fbc62)
* Add function's leakproof indicator
  to psql's [`\df+`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DF-LC),
  `\do+`, `\dAo+`, and
  `\dC+` outputs (Yugo Nagata)
  [§](https://postgr.es/c/2355e5111)
* Add access method details for partitioned relations in [`\dP+`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DP-UC)
  (Justin Pryzby)
  [§](https://postgr.es/c/978f38c77)
* Add `default_version`
  to the psql [`\dx`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DX-LC)
  extension output (Magnus Hagander)
  [§](https://postgr.es/c/d696406a9)
* Add psql variable [`WATCH_INTERVAL`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-WATCH-INTERVAL) to set the default [`\watch`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-WATCH)
  wait time (Daniel Gustafsson)
  [§](https://postgr.es/c/1a759c832)

<a id="RELEASE-18-SERVER-APPS"></a>

#### E.6.3.7. Server Applications [#](#RELEASE-18-SERVER-APPS)

* Change [initdb](../../reference/reference-server/app-initdb.md) to default to enabling checksums
  (Greg Sabino Mullane)
  [§](https://postgr.es/c/983a588e0)
  [§](https://postgr.es/c/04bec894a)

  The new initdb option
  `--no-data-checksums` disables checksums.
* Add initdb option
  `--no-sync-data-files` to avoid syncing heap/index
  files (Nathan Bossart)
  [§](https://postgr.es/c/cf131fa94)

  initdb option `--no-sync`
  is still available to avoid syncing any files.
* Add [vacuumdb](../../reference/reference-client/app-vacuumdb.md) option
  `--missing-stats-only` to compute only missing
  optimizer statistics (Corey Huinker, Nathan Bossart)
  [§](https://postgr.es/c/edba754f0)
  [§](https://postgr.es/c/987910502)

  This option can only be run by superusers and can only
  be used with options `--analyze-only` and
  `--analyze-in-stages`.
* Add [pg_combinebackup](../../reference/reference-client/app-pgcombinebackup.md) option
  `-k`/`--link` to enable hard linking
  (Israel Barth Rubio, Robert Haas)
  [§](https://postgr.es/c/99aeb8470)

  Only some files can be hard linked. This should not be used if the
  backups will be used independently.
* Allow [pg_verifybackup](../../reference/reference-client/app-pgverifybackup.md) to verify tar-format
  backups (Amul Sul)
  [§](https://postgr.es/c/8dfd31290)
* If [pg_rewind](../../reference/reference-server/app-pgrewind.md)'s `--source-server`
  specifies a database name, use it in
  `--write-recovery-conf` output (Masahiko Sawada)
  [§](https://postgr.es/c/4ecdd4110)
* Add [pg_resetwal](../../reference/reference-server/app-pgresetwal.md) option
  `--char-signedness` to change the default
  `char` signedness (Masahiko Sawada)
  [§](https://postgr.es/c/30666d185)

<a id="RELEASE-18-PGDUMP"></a>

##### E.6.3.7.1. [pg_dump](../../reference/reference-client/app-pgdump.md)/[pg_dumpall](../../reference/reference-client/app-pg-dumpall.md)/[pg_restore](../../reference/reference-client/app-pgrestore.md) [#](#RELEASE-18-PGDUMP)

* Add [pg_dump](../../reference/reference-client/app-pgdump.md) option `--statistics`
  (Jeff Davis)
  [§](https://postgr.es/c/bde2fb797)
  [§](https://postgr.es/c/a3e8dc143)
* Add pg_dump and [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md) option `--sequence-data` to
  dump sequence data that would normally be excluded (Nathan Bossart)
  [§](https://postgr.es/c/9c49f0e8c)
  [§](https://postgr.es/c/acea3fc49)
* Add [pg_dump](../../reference/reference-client/app-pgdump.md), [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md),
  and [pg_restore](../../reference/reference-client/app-pgrestore.md) options
  `--statistics-only`, `--no-statistics`,
  `--no-data`, and `--no-schema`
  (Corey Huinker, Jeff Davis)
  [§](https://postgr.es/c/1fd1bd871)
* Add option `--no-policies` to disable row level
  security policy processing in [pg_dump](../../reference/reference-client/app-pgdump.md),
  [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md), [pg_restore](../../reference/reference-client/app-pgrestore.md)
  (Nikolay Samokhvalov)
  [§](https://postgr.es/c/cd3c45125)

  This is useful for migrating to systems with different policies.

<a id="RELEASE-18-PGUPGRADE"></a>

##### E.6.3.7.2. [pg_upgrade](../../reference/reference-server/pgupgrade.md) [#](#RELEASE-18-PGUPGRADE)

* Allow pg_upgrade to preserve optimizer
  statistics (Corey Huinker, Jeff Davis, Nathan Bossart)
  [§](https://postgr.es/c/1fd1bd871)
  [§](https://postgr.es/c/c9d502eb6)
  [§](https://postgr.es/c/d5f1b6a75)
  [§](https://postgr.es/c/1fd1bd871)

  Extended statistics are not preserved. Also add
  pg_upgrade option
  `--no-statistics` to disable statistics preservation.
* Allow pg_upgrade to process database
  checks in parallel (Nathan Bossart)
  [§](https://postgr.es/c/40e2e5e92)
  [§](https://postgr.es/c/6d3d2e8e5)
  [§](https://postgr.es/c/7baa36de5)
  [§](https://postgr.es/c/46cad8b31)
  [§](https://postgr.es/c/6ab8f27bc)
  [§](https://postgr.es/c/bbf83cab9)
  [§](https://postgr.es/c/9db3018cf)
  [§](https://postgr.es/c/c34eabfbb)
  [§](https://postgr.es/c/cf2f82a37)
  [§](https://postgr.es/c/f93f5f7b9)
  [§](https://postgr.es/c/c880cf258)

  This is controlled by the existing `--jobs` option.
* Add pg_upgrade option
  `--swap` to swap directories rather than copy, clone,
  or link files (Nathan Bossart)
  [§](https://postgr.es/c/626d7236b)

  This mode is potentially the fastest.
* Add pg_upgrade option
  `--set-char-signedness` to set the default
  `char` signedness of new cluster (Masahiko Sawada)
  [§](https://postgr.es/c/a8238f87f)
  [§](https://postgr.es/c/1aab68059)

  This is to handle cases where a
  pre-PostgreSQL 18 cluster's default
  CPU signedness does not match the new cluster.

<a id="RELEASE-18-LOGICALREP-APP"></a>

##### E.6.3.7.3. Logical Replication Applications [#](#RELEASE-18-LOGICALREP-APP)

* Add [pg_createsubscriber](../../reference/reference-server/app-pgcreatesubscriber.md) option
  `--all` to create logical replicas for all databases
  (Shubham Khanna)
  [§](https://postgr.es/c/fb2ea12f4)
* Add pg_createsubscriber option
  `--clean` to remove publications (Shubham Khanna)
  [§](https://postgr.es/c/e5aeed4b8)
  [§](https://postgr.es/c/60dda7bbc)
* Add pg_createsubscriber option
  `--enable-two-phase` to enable prepared transactions
  (Shubham Khanna)
  [§](https://postgr.es/c/e117cfb2f)
* Add [pg_recvlogical](../../reference/reference-client/app-pgrecvlogical.md) option
  `--enable-failover` to specify failover slots (Hayato Kuroda)
  [§](https://postgr.es/c/cf2655a90)

  Also add option `--enable-two-phase` as a synonym
  for `--two-phase`, and deprecate the latter.
* Allow pg_recvlogical
  `--drop-slot` to work without
  `--dbname` (Hayato Kuroda)
  [§](https://postgr.es/c/c68100aa4)

<a id="RELEASE-18-SOURCE-CODE"></a>

#### E.6.3.8. Source Code [#](#RELEASE-18-SOURCE-CODE)

* Separate the loading and running of [injection points](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)
  (Michael Paquier, Heikki Linnakangas)
  [§](https://postgr.es/c/4b211003e)
  [§](https://postgr.es/c/a0a5869a8)

  Injection points can now be created, but not run, via [`INJECTION_POINT_LOAD()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS),
  and such injection points can be run via [`INJECTION_POINT_CACHED()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS).
* Support runtime arguments in injection points (Michael Paquier)
  [§](https://postgr.es/c/371f2db8b)
* Allow inline injection point test code with [`IS_INJECTION_POINT_ATTACHED()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)
  (Heikki Linnakangas)
  [§](https://postgr.es/c/20e0e7da9)
* Improve the performance of processing long [`JSON`](../../the-sql-language/datatype/datatype-json.md) strings using
  SIMD (Single Instruction Multiple Data) (David
  Rowley)
  [§](https://postgr.es/c/ca6fde922)
* Speed up CRC32C calculations using x86 AVX-512
  instructions (Raghuveer Devulapalli, Paul Amonson)
  [§](https://postgr.es/c/3c6e8c123)
* Add ARM Neon and SVE CPU
  intrinsics for popcount (integer bit counting) (Chiranmoy
  Bhattacharya, Devanga Susmitha, Rama Malladi)
  [§](https://postgr.es/c/6be53c276)
  [§](https://postgr.es/c/519338ace)
* Improve the speed of numeric multiplication and division (Joel
  Jacobson, Dean Rasheed)
  [§](https://postgr.es/c/ca481d3c9)
  [§](https://postgr.es/c/c4e44224c)
  [§](https://postgr.es/c/8dc28d7eb)
  [§](https://postgr.es/c/9428c001f)
* Add configure option [`--with-libnuma`](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBNUMA)
  to enable NUMA awareness (Jakub Wartak, Bertrand
  Drouvot)
  [§](https://postgr.es/c/65c298f61)
  [§](https://postgr.es/c/8cc139bec)
  [§](https://postgr.es/c/ba2a3c230)

  The function [`pg_numa_available()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)
  reports on NUMA awareness, and system views [`pg_shmem_allocations_numa`](../../internals/views/view-pg-shmem-allocations-numa.md)
  and [`pg_buffercache_numa`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)
  which report on shared memory distribution across
  NUMA nodes.
* Add [TOAST](../../internals/storage/storage-toast.md) table to [`pg_index`](../../internals/catalogs/catalog-pg-index.md)
  to allow for very large expression indexes (Nathan Bossart)
  [§](https://postgr.es/c/b52c4fc3c)
* Remove column [`pg_attribute`](../../internals/catalogs/catalog-pg-attribute.md).`attcacheoff`
  (David Rowley)
  [§](https://postgr.es/c/02a8d0c45)
* Add column [`pg_class`](../../internals/catalogs/catalog-pg-class.md).`relallfrozen`
  (Melanie Plageman)
  [§](https://postgr.es/c/99f8f3fbb)
* Add [`amgettreeheight`](../../internals/indexam/README.md),
  `amconsistentequality`, and
  `amconsistentordering` to the index access method
  API (Mark Dilger)
  [§](https://postgr.es/c/56fead44d)
  [§](https://postgr.es/c/af4002b38)
* Add GiST support function [`stratnum()`](../../internals/indextypes/gist.md#GIST-EXTENSIBILITY)
  (Paul A. Jungwirth)
  [§](https://postgr.es/c/7406ab623)
* Record the default CPU signedness of
  `char` in [pg_controldata](../../reference/reference-server/app-pgcontroldata.md)
  (Masahiko Sawada)
  [§](https://postgr.es/c/44fe30fda)
* Add support for Python "Limited API" in [PL/Python](../../server-programming/plpython/README.md) (Peter Eisentraut)
  [§](https://postgr.es/c/72a3d0462)
  [§](https://postgr.es/c/0793ab810)

  This helps prevent problems caused by
  Python 3.x version mismatches.
* Change the minimum supported Python
  version to 3.6.8 (Jacob Champion)
  [§](https://postgr.es/c/45363fca6)
* Remove support for OpenSSL versions older
  than 1.1.1 (Daniel Gustafsson)
  [§](https://postgr.es/c/a70e01d43)
  [§](https://postgr.es/c/6c66b7443)
* If LLVM is enabled, require version 14
  or later (Thomas Munro)
  [§](https://postgr.es/c/972c2cd28)
* Add macro [`PG_MODULE_MAGIC_EXT`](../../the-sql-language/functions/functions-info.md)
  to allow extensions to report their name and version (Andrei Lepikhov)
  [§](https://postgr.es/c/9324c8c58)

  This information can be access via the new function [`pg_get_loaded_modules()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE).
* Document that [`SPI_connect()`](../../server-programming/spi/spi-spi-connect.md)/[`SPI_connect_ext()`](../../server-programming/spi/spi-spi-connect.md)
  always returns success (`SPI_OK_CONNECT`) (Stepan
  Neretin)
  [§](https://postgr.es/c/218527d01)

  Errors are always reported via `ereport()`.
* Add [documentation
  section](../../server-programming/extend/xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE) about API and ABI
  compatibility (David Wheeler, Peter Eisentraut)
  [§](https://postgr.es/c/e54a42ac9)
* Remove the experimental designation of
  Meson builds on Windows (Aleksander Alekseev)
  [§](https://postgr.es/c/5afaba629)
* Remove configure options `--disable-spinlocks` and
  `--disable-atomics` (Thomas Munro)
  [§](https://postgr.es/c/e25626677)
  [§](https://postgr.es/c/813852613)

  Thirty-two-bit atomic operations are now required.
* Remove support for the
  HPPA/PA-RISC architecture
  (Tom Lane)
  [§](https://postgr.es/c/edadeb071)

<a id="RELEASE-18-MODULES"></a>

#### E.6.3.9. Additional Modules [#](#RELEASE-18-MODULES)

* Add extension [pg_logicalinspect](../contrib/pglogicalinspect.md) to inspect logical
  snapshots (Bertrand Drouvot)
  [§](https://postgr.es/c/7cdfeee32)
* Add extension [pg_overexplain](../contrib/pgoverexplain.md) which adds debug details
  to [`EXPLAIN`](../../reference/sql-commands/sql-explain.md)
  output (Robert Haas)
  [§](https://postgr.es/c/8d5ceb113)
* Add output columns to [`postgres_fdw_get_connections()`](../contrib/postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)
  (Hayato Kuroda, Sagar Dilip Shedge)
  [§](https://postgr.es/c/c297a47c5)
  [§](https://postgr.es/c/857df3cef)
  [§](https://postgr.es/c/4f08ab554)
  [§](https://postgr.es/c/fe186bda7)

  New output column `used_in_xact` indicates
  if the foreign data wrapper is being used by a current transaction,
  `closed` indicates if it is closed,
  `user_name` indicates the user name, and
  `remote_backend_pid` indicates the remote
  backend process identifier.
* Allow [SCRAM](../../server-administration/client-authentication/auth-password.md)
  authentication from the client to be passed to [postgres_fdw](../contrib/postgres-fdw.md) servers (Matheus Alcantara, Peter Eisentraut)
  [§](https://postgr.es/c/761c79508)

  This avoids storing postgres_fdw
  authentication information in the database, and is
  enabled with the postgres_fdw [`use_scram_passthrough`](../contrib/postgres-fdw.md#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH)
  connection option. libpq uses new connection parameters
  [scram_client_key](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-SCRAM-CLIENT-KEY) and [scram_server_key](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-SCRAM-SERVER-KEY).
* Allow SCRAM authentication from the client to be
  passed to [dblink](../contrib/dblink.md) servers (Matheus Alcantara)
  [§](https://postgr.es/c/3642df265)
* Add `on_error` and `log_verbosity`
  options to [file_fdw](../contrib/file-fdw.md) (Atsushi Torikoshi)
  [§](https://postgr.es/c/a1c4c8a9e)

  These control how file_fdw handles and
  reports invalid file rows.
* Add `reject_limit` to control the number of
  invalid rows file_fdw can ignore (Atsushi
  Torikoshi)
  [§](https://postgr.es/c/6c8f67032)

  This is active when `ON_ERROR = 'ignore'`.
* Add configurable variable `min_password_length` to
  [passwordcheck](../contrib/passwordcheck.md) (Emanuele Musella, Maurizio Boriani)
  [§](https://postgr.es/c/f7e1b3828)

  This controls the minimum password length.
* Have [pgbench](../../reference/reference-client/pgbench.md) report the number of failed, retried,
  or skipped transactions in per-script reports (Yugo Nagata)
  [§](https://postgr.es/c/cae0f3c40)
* Add [isn](../contrib/isn.md) server variable `weak`
  to control invalid check digit acceptance (Viktor Holmberg)
  [§](https://postgr.es/c/448904423)

  This was previously only controlled by function [`isn_weak()`](../contrib/isn.md#ISN-FUNCTIONS).
* Allow values to be sorted to speed [btree_gist](../contrib/btree-gist.md)
  index builds (Bernd Helmle, Andrey Borodin)
  [§](https://postgr.es/c/e4309f73f)
* Add [amcheck](../contrib/amcheck.md) check function [`gin_index_check()`](../contrib/amcheck.md#AMCHECK-FUNCTIONS)
  to verify `GIN` indexes (Grigory Kryachko, Heikki
  Linnakangas, Andrey Borodin)
  [§](https://postgr.es/c/14ffaece0)
* Add functions [`pg_buffercache_evict_relation()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)
  and [`pg_buffercache_evict_all()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)
  to evict unpinned shared buffers (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/dcf7e1697)

  The existing function [`pg_buffercache_evict()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)
  now returns the buffer flush status.
* Allow extensions to install custom [EXPLAIN](../../reference/sql-commands/sql-explain.md)
  options (Robert Haas, Sami Imseih)
  [§](https://postgr.es/c/c65bc2e1d)
  [§](https://postgr.es/c/4fd02bf7c)
  [§](https://postgr.es/c/50ba65e73)
* Allow extensions to use the server's cumulative statistics
  API (Michael Paquier)
  [§](https://postgr.es/c/7949d9594)
  [§](https://postgr.es/c/2eff9e678)

<a id="RELEASE-18-PGSTATSTATEMENTS"></a>

##### E.6.3.9.1. [pg_stat_statements](../contrib/pgstatstatements.md) [#](#RELEASE-18-PGSTATSTATEMENTS)

* Allow the queries of [CREATE TABLE AS](../../reference/sql-commands/sql-createtableas.md)
  and [DECLARE](../../reference/sql-commands/sql-declare.md) to be tracked by
  pg_stat_statements (Anthonin Bonnefoy)
  [§](https://postgr.es/c/6b652e6ce)

  They are also now assigned query ids.
* Allow the parameterization of [SET](../../reference/sql-commands/sql-set.md) values in
  pg_stat_statements (Greg Sabino Mullane,
  Michael Paquier)
  [§](https://postgr.es/c/dc6851596)

  This reduces the bloat caused by `SET` statements
  with differing constants.
* Add [`pg_stat_statements`](../contrib/pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)
  columns to report parallel activity (Guillaume Lelarge)
  [§](https://postgr.es/c/cf54a2c00)

  The new columns are
  `parallel_workers_to_launch` and
  `parallel_workers_launched`.
* Add
  `pg_stat_statements`.`wal_buffers_full`
  to report full WAL buffers (Bertrand Drouvot)
  [§](https://postgr.es/c/ce5bcc4a9)

<a id="RELEASE-18-PGCRYPTO"></a>

##### E.6.3.9.2. [pgcrypto](../contrib/pgcrypto.md) [#](#RELEASE-18-PGCRYPTO)

* Add pgcrypto algorithms [`sha256crypt`](../contrib/pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS)
  and [`sha512crypt`](../contrib/pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS)
  (Bernd Helmle)
  [§](https://postgr.es/c/749a9e20c)
* Add [CFB](../contrib/pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS) mode
  to pgcrypto encryption and decryption
  (Umar Hayat)
  [§](https://postgr.es/c/9ad1b3d01)
* Add function [`fips_mode()`](../contrib/pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)
  to report the server's FIPS mode (Daniel
  Gustafsson)
  [§](https://postgr.es/c/924d89a35)
* Add pgcrypto server variable [`builtin_crypto_enabled`](../contrib/pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED)
  to allow disabling builtin non-FIPS mode
  cryptographic functions (Daniel Gustafsson, Joe Conway)
  [§](https://postgr.es/c/035f99cbe)

  This is useful for guaranteeing FIPS mode behavior.

<a id="RELEASE-18-ACKNOWLEDGEMENTS"></a>

### E.6.4. Acknowledgments [#](#RELEASE-18-ACKNOWLEDGEMENTS)

The following individuals (in alphabetical order) have contributed
to this release as patch authors, committers, reviewers, testers,
or reporters of issues.

<table border="0" class="simplelist" summary="Simple list"><tr><td>Abhishek Chanda</td></tr><tr><td>Adam Guo</td></tr><tr><td>Adam Rauch</td></tr><tr><td>Aidar Imamov</td></tr><tr><td>Ajin Cherian</td></tr><tr><td>Alastair Turner</td></tr><tr><td>Alec Cozens</td></tr><tr><td>Aleksander Alekseev</td></tr><tr><td>Alena Rybakina</td></tr><tr><td>Alex Friedman</td></tr><tr><td>Alex Richman</td></tr><tr><td>Alexander Alehin</td></tr><tr><td>Alexander Borisov</td></tr><tr><td>Alexander Korotkov</td></tr><tr><td>Alexander Kozhemyakin</td></tr><tr><td>Alexander Kukushkin</td></tr><tr><td>Alexander Kuzmenkov</td></tr><tr><td>Alexander Kuznetsov</td></tr><tr><td>Alexander Lakhin</td></tr><tr><td>Alexander Pyhalov</td></tr><tr><td>Alexandra Wang</td></tr><tr><td>Alexey Dvoichenkov</td></tr><tr><td>Alexey Makhmutov</td></tr><tr><td>Alexey Shishkin</td></tr><tr><td>Ali Akbar</td></tr><tr><td>Álvaro Herrera</td></tr><tr><td>Álvaro Mongil</td></tr><tr><td>Amit Kapila</td></tr><tr><td>Amit Langote</td></tr><tr><td>Amul Sul</td></tr><tr><td>Andreas Karlsson</td></tr><tr><td>Andreas Scherbaum</td></tr><tr><td>Andreas Ulbrich</td></tr><tr><td>Andrei Lepikhov</td></tr><tr><td>Andres Freund</td></tr><tr><td>Andrew</td></tr><tr><td>Andrew Bille</td></tr><tr><td>Andrew Dunstan</td></tr><tr><td>Andrew Jackson</td></tr><tr><td>Andrew Kane</td></tr><tr><td>Andrew Watkins</td></tr><tr><td>Andrey Borodin</td></tr><tr><td>Andrey Chudnovsky</td></tr><tr><td>Andrey Rachitskiy</td></tr><tr><td>Andrey Rudometov</td></tr><tr><td>Andy Alsup</td></tr><tr><td>Andy Fan</td></tr><tr><td>Anthonin Bonnefoy</td></tr><tr><td>Anthony Hsu</td></tr><tr><td>Anthony Leung</td></tr><tr><td>Anton Melnikov</td></tr><tr><td>Anton Voloshin</td></tr><tr><td>Antonin Houska</td></tr><tr><td>Antti Lampinen</td></tr><tr><td>Arseniy Mukhin</td></tr><tr><td>Artur Zakirov</td></tr><tr><td>Arun Thirupathi</td></tr><tr><td>Ashutosh Bapat</td></tr><tr><td>Asphator</td></tr><tr><td>Atsushi Torikoshi</td></tr><tr><td>Avi Weinberg</td></tr><tr><td>Aya Iwata</td></tr><tr><td>Ayush Tiwari</td></tr><tr><td>Ayush Vatsa</td></tr><tr><td>Bastien Roucariès</td></tr><tr><td>Ben Peachey Higdon</td></tr><tr><td>Benoit Lobréau</td></tr><tr><td>Bernd Helmle</td></tr><tr><td>Bernd Reiß</td></tr><tr><td>Bernhard Wiedemann</td></tr><tr><td>Bertrand Drouvot</td></tr><tr><td>Bertrand Mamasam</td></tr><tr><td>Bharath Rupireddy</td></tr><tr><td>Bogdan Grigorenko</td></tr><tr><td>Boyu Yang</td></tr><tr><td>Braulio Fdo Gonzalez</td></tr><tr><td>Bruce Momjian</td></tr><tr><td>Bykov Ivan</td></tr><tr><td>Cameron Vogt</td></tr><tr><td>Cary Huang</td></tr><tr><td>Cédric Villemain</td></tr><tr><td>Cees van Zeeland</td></tr><tr><td>ChangAo Chen</td></tr><tr><td>Chao Li</td></tr><tr><td>Chapman Flack</td></tr><tr><td>Charles Samborski</td></tr><tr><td>Chengwen Wu</td></tr><tr><td>Chengxi Sun</td></tr><tr><td>Chiranmoy Bhattacharya</td></tr><tr><td>Chris Gooch</td></tr><tr><td>Christian Charukiewicz</td></tr><tr><td>Christoph Berg</td></tr><tr><td>Christophe Courtois</td></tr><tr><td>Christopher Inokuchi</td></tr><tr><td>Clemens Ruck</td></tr><tr><td>Corey Huinker</td></tr><tr><td>Craig Milhiser</td></tr><tr><td>Crisp Lee</td></tr><tr><td>Dagfinn Ilmari Mannsåker</td></tr><tr><td>Daniel Elishakov</td></tr><tr><td>Daniel Gustafsson</td></tr><tr><td>Daniel Vérité</td></tr><tr><td>Daniel Westermann</td></tr><tr><td>Daniele Varrazzo</td></tr><tr><td>Daniil Davydov</td></tr><tr><td>Daria Shanina</td></tr><tr><td>Dave Cramer</td></tr><tr><td>Dave Page</td></tr><tr><td>David Benjamin</td></tr><tr><td>David Christensen</td></tr><tr><td>David Fiedler</td></tr><tr><td>David G. Johnston</td></tr><tr><td>David Geier</td></tr><tr><td>David Rowley</td></tr><tr><td>David Steele</td></tr><tr><td>David Wheeler</td></tr><tr><td>David Zhang</td></tr><tr><td>Davinder Singh</td></tr><tr><td>Dean Rasheed</td></tr><tr><td>Devanga Susmitha</td></tr><tr><td>Devrim Gündüz</td></tr><tr><td>Dian Fay</td></tr><tr><td>Dilip Kumar</td></tr><tr><td>Dimitrios Apostolou</td></tr><tr><td>Dipesh Dhameliya</td></tr><tr><td>Dmitrii Bondar</td></tr><tr><td>Dmitry Dolgov</td></tr><tr><td>Dmitry Koval</td></tr><tr><td>Dmitry Kovalenko</td></tr><tr><td>Dmitry Yurichev</td></tr><tr><td>Dominique Devienne</td></tr><tr><td>Donghang Lin</td></tr><tr><td>Dorjpalam Batbaatar</td></tr><tr><td>Drew Callahan</td></tr><tr><td>Duncan Sands</td></tr><tr><td>Dwayne Towell</td></tr><tr><td>Dzmitry Jachnik</td></tr><tr><td>Egor Chindyaskin</td></tr><tr><td>Egor Rogov</td></tr><tr><td>Emanuel Ionescu</td></tr><tr><td>Emanuele Musella</td></tr><tr><td>Emre Hasegeli</td></tr><tr><td>Eric Cyr</td></tr><tr><td>Erica Zhang</td></tr><tr><td>Erik Nordström</td></tr><tr><td>Erik Rijkers</td></tr><tr><td>Erik Wienhold</td></tr><tr><td>Erki Eessaar</td></tr><tr><td>Ethan Mertz</td></tr><tr><td>Etienne LAFARGE</td></tr><tr><td>Etsuro Fujita</td></tr><tr><td>Euler Taveira</td></tr><tr><td>Evan Si</td></tr><tr><td>Evgeniy Gorbanev</td></tr><tr><td>Fabio R. Sluzala</td></tr><tr><td>Fabrízio de Royes Mello</td></tr><tr><td>Feike Steenbergen</td></tr><tr><td>Feliphe Pozzer</td></tr><tr><td>Felix</td></tr><tr><td>Fire Emerald</td></tr><tr><td>Florents Tselai</td></tr><tr><td>Francesco Degrassi</td></tr><tr><td>Frank Streitzig</td></tr><tr><td>Frédéric Yhuel</td></tr><tr><td>Fredrik Widlert</td></tr><tr><td>Gabriele Bartolini</td></tr><tr><td>Gavin Panella</td></tr><tr><td>Geoff Winkless</td></tr><tr><td>George MacKerron</td></tr><tr><td>Gilles Darold</td></tr><tr><td>Grant Gryczan</td></tr><tr><td>Greg Burd</td></tr><tr><td>Greg Sabino Mullane</td></tr><tr><td>Greg Stark</td></tr><tr><td>Grigory Kryachko</td></tr><tr><td>Guillaume Lelarge</td></tr><tr><td>Gunnar Morling</td></tr><tr><td>Gunnar Wagner</td></tr><tr><td>Gurjeet Singh</td></tr><tr><td>Haifang Wang</td></tr><tr><td>Hajime Matsunaga</td></tr><tr><td>Hamid Akhtar</td></tr><tr><td>Hannu Krosing</td></tr><tr><td>Hari Krishna Sunder</td></tr><tr><td>Haruka Takatsuka</td></tr><tr><td>Hayato Kuroda</td></tr><tr><td>Heikki Linnakangas</td></tr><tr><td>Hironobu Suzuki</td></tr><tr><td>Holger Jakobs</td></tr><tr><td>Hubert Lubaczewski</td></tr><tr><td>Hugo Dubois</td></tr><tr><td>Hugo Zhang</td></tr><tr><td>Hunaid Sohail</td></tr><tr><td>Hywel Carver</td></tr><tr><td>Ian Barwick</td></tr><tr><td>Ibrar Ahmed</td></tr><tr><td>Igor Gnatyuk</td></tr><tr><td>Igor Korot</td></tr><tr><td>Ilia Evdokimov</td></tr><tr><td>Ilya Gladyshev</td></tr><tr><td>Ilyasov Ian</td></tr><tr><td>Imran Zaheer</td></tr><tr><td>Isaac Morland</td></tr><tr><td>Israel Barth Rubio</td></tr><tr><td>Ivan Kush</td></tr><tr><td>Jacob Brazeal</td></tr><tr><td>Jacob Champion</td></tr><tr><td>Jaime Casanova</td></tr><tr><td>Jakob Egger</td></tr><tr><td>Jakub Wartak</td></tr><tr><td>James Coleman</td></tr><tr><td>James Hunter</td></tr><tr><td>Jan Behrens</td></tr><tr><td>Japin Li</td></tr><tr><td>Jason Smith</td></tr><tr><td>Jayesh Dehankar</td></tr><tr><td>Jeevan Chalke</td></tr><tr><td>Jeff Davis</td></tr><tr><td>Jehan-Guillaume de Rorthais</td></tr><tr><td>Jelte Fennema-Nio</td></tr><tr><td>Jian He</td></tr><tr><td>Jianghua Yang</td></tr><tr><td>Jiao Shuntian</td></tr><tr><td>Jim Jones</td></tr><tr><td>Jim Nasby</td></tr><tr><td>Jingtang Zhang</td></tr><tr><td>Jingzhou Fu</td></tr><tr><td>Joe Conway</td></tr><tr><td>Joel Jacobson</td></tr><tr><td>John Hutchins</td></tr><tr><td>John Naylor</td></tr><tr><td>Jonathan Katz</td></tr><tr><td>Jorge Solórzano</td></tr><tr><td>José Villanova</td></tr><tr><td>Josef Šimánek</td></tr><tr><td>Joseph Koshakow</td></tr><tr><td>Julien Rouhaud</td></tr><tr><td>Junwang Zhao</td></tr><tr><td>Justin Pryzby</td></tr><tr><td>Kaido Vaikla</td></tr><tr><td>Kaimeh</td></tr><tr><td>Karina Litskevich</td></tr><tr><td>Karthik S</td></tr><tr><td>Kartyshov Ivan</td></tr><tr><td>Kashif Zeeshan</td></tr><tr><td>Keisuke Kuroda</td></tr><tr><td>Kevin Hale Boyes</td></tr><tr><td>Kevin K Biju</td></tr><tr><td>Kirill Reshke</td></tr><tr><td>Kirill Zdornyy</td></tr><tr><td>Koen De Groote</td></tr><tr><td>Koichi Suzuki</td></tr><tr><td>Koki Nakamura</td></tr><tr><td>Konstantin Knizhnik</td></tr><tr><td>Kouhei Sutou</td></tr><tr><td>Kuntal Ghosh</td></tr><tr><td>Kyotaro Horiguchi</td></tr><tr><td>Lakshmi Narayana Velayudam</td></tr><tr><td>Lars Kanis</td></tr><tr><td>Laurence Parry</td></tr><tr><td>Laurenz Albe</td></tr><tr><td>Lele Gaifax</td></tr><tr><td>Li Yong</td></tr><tr><td>Lilian Ontowhee</td></tr><tr><td>Lingbin Meng</td></tr><tr><td>Luboslav Špilák</td></tr><tr><td>Luca Vallisa</td></tr><tr><td>Lukas Fittl</td></tr><tr><td>Maciek Sakrejda</td></tr><tr><td>Magnus Hagander</td></tr><tr><td>Mahendra Singh Thalor</td></tr><tr><td>Mahendrakar Srinivasarao</td></tr><tr><td>Maiquel Grassi</td></tr><tr><td>Maksim Korotkov</td></tr><tr><td>Maksim Melnikov</td></tr><tr><td>Man Zeng</td></tr><tr><td>Marat Buharov</td></tr><tr><td>Marc Balmer</td></tr><tr><td>Marco Nenciarini</td></tr><tr><td>Marcos Pegoraro</td></tr><tr><td>Marina Polyakova</td></tr><tr><td>Mark Callaghan</td></tr><tr><td>Mark Dilger</td></tr><tr><td>Marlene Brandstaetter</td></tr><tr><td>Marlene Reiterer</td></tr><tr><td>Martin Rakhmanov</td></tr><tr><td>Masahiko Sawada</td></tr><tr><td>Masahiro Ikeda</td></tr><tr><td>Masao Fujii</td></tr><tr><td>Mason Mackaman</td></tr><tr><td>Mat Arye</td></tr><tr><td>Matheus Alcantara</td></tr><tr><td>Mats Kindahl</td></tr><tr><td>Matthew Gabeler-Lee</td></tr><tr><td>Matthew Kim</td></tr><tr><td>Matthew Sterrett</td></tr><tr><td>Matthew Woodcraft</td></tr><tr><td>Matthias van de Meent</td></tr><tr><td>Matthieu Denais</td></tr><tr><td>Maurizio Boriani</td></tr><tr><td>Max Johnson</td></tr><tr><td>Max Madden</td></tr><tr><td>Maxim Boguk</td></tr><tr><td>Maxim Orlov</td></tr><tr><td>Maximilian Chrzan</td></tr><tr><td>Melanie Plageman</td></tr><tr><td>Melih Mutlu</td></tr><tr><td>Mert Alev</td></tr><tr><td>Michael Banck</td></tr><tr><td>Michael Bondarenko</td></tr><tr><td>Michael Christofides</td></tr><tr><td>Michael Guissine</td></tr><tr><td>Michael Harris</td></tr><tr><td>Michaël Paquier</td></tr><tr><td>Michail Nikolaev</td></tr><tr><td>Michal Kleczek</td></tr><tr><td>Michel Pelletier</td></tr><tr><td>Mikaël Gourlaouen</td></tr><tr><td>Mikhail Gribkov</td></tr><tr><td>Mikhail Kot</td></tr><tr><td>Milosz Chmura</td></tr><tr><td>Muralikrishna Bandaru</td></tr><tr><td>Murat Efendioglu</td></tr><tr><td>Mutaamba Maasha</td></tr><tr><td>Naeem Akhter</td></tr><tr><td>Nat Makarevitch</td></tr><tr><td>Nathan Bossart</td></tr><tr><td>Navneet Kumar</td></tr><tr><td>Nazir Bilal Yavuz</td></tr><tr><td>Neil Conway</td></tr><tr><td>Niccolò Fei</td></tr><tr><td>Nick Davies</td></tr><tr><td>Nicolas Maus</td></tr><tr><td>Niek Brasa</td></tr><tr><td>Nikhil Raj</td></tr><tr><td>Nikita</td></tr><tr><td>Nikita Kalinin</td></tr><tr><td>Nikita Malakhov</td></tr><tr><td>Nikolay Samokhvalov</td></tr><tr><td>Nikolay Shaplov</td></tr><tr><td>Nisha Moond</td></tr><tr><td>Nitin Jadhav</td></tr><tr><td>Nitin Motiani</td></tr><tr><td>Noah Misch</td></tr><tr><td>Noboru Saito</td></tr><tr><td>Noriyoshi Shinoda</td></tr><tr><td>Ole Peder Brandtzæg</td></tr><tr><td>Oleg Sibiryakov</td></tr><tr><td>Oleg Tselebrovskiy</td></tr><tr><td>Olleg Samoylov</td></tr><tr><td>Onder Kalaci</td></tr><tr><td>Ondrej Navratil</td></tr><tr><td>Patrick Stählin</td></tr><tr><td>Paul Amonson</td></tr><tr><td>Paul Jungwirth</td></tr><tr><td>Paul Ramsey</td></tr><tr><td>Pavel Borisov</td></tr><tr><td>Pavel Luzanov</td></tr><tr><td>Pavel Nekrasov</td></tr><tr><td>Pavel Stehule</td></tr><tr><td>Peter Eisentraut</td></tr><tr><td>Peter Geoghegan</td></tr><tr><td>Peter Mittere</td></tr><tr><td>Peter Smith</td></tr><tr><td>Phil Eaton</td></tr><tr><td>Philipp Salvisberg</td></tr><tr><td>Philippe Beaudoin</td></tr><tr><td>Pierre Giraud</td></tr><tr><td>Pixian Shi</td></tr><tr><td>Polina Bungina</td></tr><tr><td>Przemyslaw Sztoch</td></tr><tr><td>Quynh Tran</td></tr><tr><td>Rafia Sabih</td></tr><tr><td>Raghuveer Devulapalli</td></tr><tr><td>Rahila Syed</td></tr><tr><td>Rama Malladi</td></tr><tr><td>Ran Benita</td></tr><tr><td>Ranier Vilela</td></tr><tr><td>Renan Alves Fonseca</td></tr><tr><td>Richard Guo</td></tr><tr><td>Richard Neill</td></tr><tr><td>Rintaro Ikeda</td></tr><tr><td>Robert Haas</td></tr><tr><td>Robert Treat</td></tr><tr><td>Robins Tharakan</td></tr><tr><td>Roman Zharkov</td></tr><tr><td>Ronald Cruz</td></tr><tr><td>Ronan Dunklau</td></tr><tr><td>Rui Zhao</td></tr><tr><td>Rushabh Lathia</td></tr><tr><td>Rustam Allakov</td></tr><tr><td>Ryo Kanbayashi</td></tr><tr><td>Ryohei Takahashi</td></tr><tr><td>RyotaK</td></tr><tr><td>Sagar Dilip Shedge</td></tr><tr><td>Salvatore Dipietro</td></tr><tr><td>Sam Gabrielsson</td></tr><tr><td>Sam James</td></tr><tr><td>Sameer Kumar</td></tr><tr><td>Sami Imseih</td></tr><tr><td>Samuel Thibault</td></tr><tr><td>Satyanarayana Narlapuram</td></tr><tr><td>Sebastian Skalacki</td></tr><tr><td>Senglee Choi</td></tr><tr><td>Sergei Kornilov</td></tr><tr><td>Sergey Belyashov</td></tr><tr><td>Sergey Dudoladov</td></tr><tr><td>Sergey Prokhorenko</td></tr><tr><td>Sergey Sargsyan</td></tr><tr><td>Sergey Soloviev</td></tr><tr><td>Sergey Tatarintsev</td></tr><tr><td>Shaik Mohammad Mujeeb</td></tr><tr><td>Shawn McCoy</td></tr><tr><td>Shenhao Wang</td></tr><tr><td>Shihao Zhong</td></tr><tr><td>Shinya Kato</td></tr><tr><td>Shlok Kyal</td></tr><tr><td>Shubham Khanna</td></tr><tr><td>Shveta Malik</td></tr><tr><td>Simon Riggs</td></tr><tr><td>Smolkin Grigory</td></tr><tr><td>Sofia Kopikova</td></tr><tr><td>Song Hongyu</td></tr><tr><td>Song Jinzhou</td></tr><tr><td>Soumyadeep Chakraborty</td></tr><tr><td>Sravan Kumar</td></tr><tr><td>Srinath Reddy</td></tr><tr><td>Stan Hu</td></tr><tr><td>Stepan Neretin</td></tr><tr><td>Stephen Fewer</td></tr><tr><td>Stephen Frost</td></tr><tr><td>Steve Chavez</td></tr><tr><td>Steven Niu</td></tr><tr><td>Suraj Kharage</td></tr><tr><td>Sven Klemm</td></tr><tr><td>Takamichi Osumi</td></tr><tr><td>Takeshi Ideriha</td></tr><tr><td>Tatsuo Ishii</td></tr><tr><td>Ted Yu</td></tr><tr><td>Tels</td></tr><tr><td>Tender Wang</td></tr><tr><td>Teodor Sigaev</td></tr><tr><td>Thom Brown</td></tr><tr><td>Thomas Baehler</td></tr><tr><td>Thomas Krennwallner</td></tr><tr><td>Thomas Munro</td></tr><tr><td>Tim Wood</td></tr><tr><td>Timur Magomedov</td></tr><tr><td>Tobias Wendorff</td></tr><tr><td>Todd Cook</td></tr><tr><td>Tofig Aliev</td></tr><tr><td>Tom Lane</td></tr><tr><td>Tomas Vondra</td></tr><tr><td>Tomasz Rybak</td></tr><tr><td>Tomasz Szypowski</td></tr><tr><td>Torsten Foertsch</td></tr><tr><td>Toshi Harada</td></tr><tr><td>Tristan Partin</td></tr><tr><td>Triveni N</td></tr><tr><td>Umar Hayat</td></tr><tr><td>Vallimaharajan G</td></tr><tr><td>Vasya Boytsov</td></tr><tr><td>Victor Yegorov</td></tr><tr><td>Vignesh C</td></tr><tr><td>Viktor Holmberg</td></tr><tr><td>Vinícius Abrahão</td></tr><tr><td>Vinod Sridharan</td></tr><tr><td>Virender Singla</td></tr><tr><td>Vitaly Davydov</td></tr><tr><td>Vladlen Popolitov</td></tr><tr><td>Vladyslav Nebozhyn</td></tr><tr><td>Walid Ibrahim</td></tr><tr><td>Webbo Han</td></tr><tr><td>Wenhui Qiu</td></tr><tr><td>Will Mortensen</td></tr><tr><td>Will Storey</td></tr><tr><td>Wolfgang Walther</td></tr><tr><td>Xin Zhang</td></tr><tr><td>Xing Guo</td></tr><tr><td>Xuneng Zhou</td></tr><tr><td>Yan Chengpen</td></tr><tr><td>Yang Lei</td></tr><tr><td>Yaroslav Saburov</td></tr><tr><td>Yaroslav Syrytsia</td></tr><tr><td>Yasir Hussain</td></tr><tr><td>Yasuo Honda</td></tr><tr><td>Yogesh Sharma</td></tr><tr><td>Yonghao Lee</td></tr><tr><td>Yoran Heling</td></tr><tr><td>Yu Liang</td></tr><tr><td>Yugo Nagata</td></tr><tr><td>Yuhang Qiu</td></tr><tr><td>Yuki Seino</td></tr><tr><td>Yura Sokolov</td></tr><tr><td>Yurii Rashkovskii</td></tr><tr><td>Yushi Ogiwara</td></tr><tr><td>Yusuke Sugie</td></tr><tr><td>Yuta Katsuragi</td></tr><tr><td>Yuto Sasaki</td></tr><tr><td>Yuuki Fujii</td></tr><tr><td>Yuya Watari</td></tr><tr><td>Zane Duffield</td></tr><tr><td>Zeyuan Hu</td></tr><tr><td>Zhang Mingli</td></tr><tr><td>Zhihong Yu</td></tr><tr><td>Zhijie Hou</td></tr><tr><td>Zsolt Parragi</td></tr></table>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18.html)（英文原文，待翻譯）
