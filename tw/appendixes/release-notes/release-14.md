# E.1. Release 14

**Release date:** 2021-09-30

## E.1.1. Overview

PostgreSQL 14 contains many new features and enhancements, including:

* Stored procedures can now return data via `OUT` parameters.
* The SQL-standard `SEARCH` and `CYCLE` options for common table expressions have been implemented.
* Subscripting can now be applied to any data type for which it is a useful notation, not only arrays. In this release, the `jsonb` and `hstore` types have gained subscripting operators.
* Range types have been extended by adding multiranges, allowing representation of noncontiguous data ranges.
* Numerous performance improvements have been made for parallel queries, heavily-concurrent workloads, partitioned tables, logical replication, and vacuuming.
* B-tree index updates are managed more efficiently, reducing index bloat.
* `VACUUM` automatically becomes more aggressive, and skips inessential cleanup, if the database starts to approach a transaction ID wraparound condition.
* Extended statistics can now be collected on expressions, allowing better planning results for complex queries.
* libpq now has the ability to pipeline multiple queries, which can boost throughput over high-latency connections.

The above items and other new features of PostgreSQL 14 are explained in more detail in the sections below.

## E.1.2. Migration to Version 14

A dump/restore using [pg\_dumpall](https://www.postgresql.org/docs/14/app-pg-dumpall.html) or use of [pg\_upgrade](https://www.postgresql.org/docs/14/pgupgrade.html) or logical replication is required for those wishing to migrate data from any previous release. See [Section 19.6](https://www.postgresql.org/docs/14/upgrading.html) for general information on migrating to new major releases.

Version 14 contains a number of changes that may affect compatibility with previous releases. Observe the following incompatibilities:

* User-defined objects that reference certain built-in array functions along with their argument types must be recreated \(Tom Lane\)

  Specifically, [`array_append()`](https://www.postgresql.org/docs/14/functions-array.html), `array_prepend()`, `array_cat()`, `array_position()`, `array_positions()`, `array_remove()`, `array_replace()`, and [`width_bucket()`](https://www.postgresql.org/docs/14/functions-math.html) used to take `anyarray` arguments but now take `anycompatiblearray`. Therefore, user-defined objects like aggregates and operators that reference those array function signatures must be dropped before upgrading, and recreated once the upgrade completes.

* Remove deprecated containment operators `@` and `~` for built-in [geometric data types](https://www.postgresql.org/docs/14/functions-geometry.html) and contrib modules [cube](https://www.postgresql.org/docs/14/cube.html), [hstore](https://www.postgresql.org/docs/14/hstore.html), [intarray](https://www.postgresql.org/docs/14/intarray.html), and [seg](https://www.postgresql.org/docs/14/seg.html) \(Justin Pryzby\)

  The more consistently named `<@` and `@>` have been recommended for many years.

* Fix [`to_tsquery()`](https://www.postgresql.org/docs/14/functions-textsearch.html) and `websearch_to_tsquery()` to properly parse query text containing discarded tokens \(Alexander Korotkov\)

  Certain discarded tokens, like underscore, caused the output of these functions to produce incorrect tsquery output, e.g., both `websearch_to_tsquery('"pg_class pg"')` and `to_tsquery('pg_class <-> pg')` used to output `( 'pg' & 'class' ) <-> 'pg'`, but now both output `'pg' <-> 'class' <-> 'pg'`.

* Fix [`websearch_to_tsquery()`](https://www.postgresql.org/docs/14/functions-textsearch.html) to properly parse multiple adjacent discarded tokens in quotes \(Alexander Korotkov\)

  Previously, quoted text that contained multiple adjacent discarded tokens was treated as multiple tokens, causing incorrect tsquery output, e.g., `websearch_to_tsquery('"aaa: bbb"')` used to output `'aaa' <2> 'bbb'`, but now outputs `'aaa' <-> 'bbb'`.

* Change [`EXTRACT()`](https://www.postgresql.org/docs/14/functions-datetime.html) to return type `numeric` instead of `float8` \(Peter Eisentraut\)

  This avoids loss-of-precision issues in some usages. The old behavior can still be obtained by using the old underlying function `date_part()`.

  Also, `EXTRACT(date)` now throws an error for units that are not part of the `date` data type.

* Change [`var_samp()`](https://www.postgresql.org/docs/14/functions-aggregate.html) and `stddev_samp()` with numeric parameters to return NULL when the input is a single NaN value \(Tom Lane\)

  Previously `NaN` was returned.

* Return false for [`has_column_privilege()`](https://www.postgresql.org/docs/14/functions-info.html) checks on non-existent or dropped columns when using attribute numbers \(Joe Conway\)

  Previously such attribute numbers returned an invalid-column error.

* Fix handling of infinite [window function](https://www.postgresql.org/docs/14/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) ranges \(Tom Lane\)

  Previously window frame clauses like `'inf' PRECEDING AND 'inf' FOLLOWING` returned incorrect results.

* Remove factorial operators `!` and `!!`, as well as function `numeric_fac()` \(Mark Dilger\)

  The [`factorial()`](https://www.postgresql.org/docs/14/functions-math.html) function is still supported.

* Disallow `factorial()` of negative numbers \(Peter Eisentraut\)

  Previously such cases returned 1.

* Remove support for [postfix](https://www.postgresql.org/docs/14/sql-createoperator.html) \(right-unary\) operators \(Mark Dilger\)

  pg\_dump and pg\_upgrade will warn if postfix operators are being dumped.

* Allow `\D` and `\W` shorthands to match newlines in [regular expression](https://www.postgresql.org/docs/14/functions-matching.html#FUNCTIONS-POSIX-REGEXP) newline-sensitive mode \(Tom Lane\)

  Previously they did not match newlines in this mode, but that disagrees with the behavior of other common regular expression engines. `[^[:digit:]]` or `[^[:word:]]` can be used to get the old behavior.

* Disregard constraints when matching regular expression [back-references](https://www.postgresql.org/docs/14/functions-matching.html#POSIX-ESCAPE-SEQUENCES) \(Tom Lane\)

  For example, in `(^\d+).*\1`, the `^` constraint should be applied at the start of the string, but not when matching `\1`.

* Disallow `\w` as a range start or end in regular expression character classes \(Tom Lane\)

  This previously was allowed but produced unexpected results.

* Require [custom server parameter](https://www.postgresql.org/docs/14/runtime-config-custom.html) names to use only characters that are valid in unquoted SQL identifiers \(Tom Lane\)
* Change the default of the [password\_encryption](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) server parameter to `scram-sha-256` \(Peter Eisentraut\)

  Previously it was `md5`. All new passwords will be stored as SHA256 unless this server setting is changed or the password is specified in MD5 format. Also, the legacy \(and undocumented\) Boolean-like values which were previously synonyms for `md5` are no longer accepted.

* Remove server parameter `vacuum_cleanup_index_scale_factor` \(Peter Geoghegan\)

  This setting was ignored starting in PostgreSQL version 13.3.

* Remove server parameter `operator_precedence_warning` \(Tom Lane\)

  This setting was used for warning applications about PostgreSQL 9.5 changes.

* Overhaul the specification of `clientcert` in [`pg_hba.conf`](https://www.postgresql.org/docs/14/auth-pg-hba-conf.html) \(Kyotaro Horiguchi\)

  Values `1`/`0`/`no-verify` are no longer supported; only the strings `verify-ca` and `verify-full` can be used. Also, disallow `verify-ca` if cert authentication is enabled since cert requires `verify-full` checking.

* Remove support for [SSL](https://www.postgresql.org/docs/14/runtime-config-connection.html#RUNTIME-CONFIG-CONNECTION-SSL) compression \(Daniel Gustafsson, Michael Paquier\)

  This was already disabled by default in previous PostgreSQL releases, and most modern OpenSSL and TLS versions no longer support it.

* Remove server and [libpq](https://www.postgresql.org/docs/14/libpq.html) support for the version 2 [wire protocol](https://www.postgresql.org/docs/14/protocol.html) \(Heikki Linnakangas\)

  This was last used as the default in PostgreSQL 7.3 \(released in 2002\).

* Disallow single-quoting of the language name in the [`CREATE/DROP LANGUAGE`](https://www.postgresql.org/docs/14/sql-createlanguage.html) command \(Peter Eisentraut\)
* Remove the [composite types](https://www.postgresql.org/docs/14/xfunc-sql.html#XFUNC-SQL-COMPOSITE-FUNCTIONS) that were formerly created for sequences and toast tables \(Tom Lane\)
* Process doubled quote marks in [ecpg](https://www.postgresql.org/docs/14/ecpg.html) SQL command strings correctly \(Tom Lane\)

  Previously `'abc''def'` was passed to the server as `'abc'def'`, and `"abc""def"` was passed as `"abc"def"`, causing syntax errors.

* Prevent the containment operators \(`<@` and `@>`\) for [intarray](https://www.postgresql.org/docs/14/intarray.html) from using GiST indexes \(Tom Lane\)

  Previously a full GiST index scan was required, so just avoid that and scan the heap, which is faster. Indexes created for this purpose should be removed.

* Remove contrib program pg\_standby \(Justin Pryzby\)
* Prevent [tablefunc](https://www.postgresql.org/docs/14/tablefunc.html)'s function `normal_rand()` from accepting negative values \(Ashutosh Bapat\)

  Negative values produced undesirable results.

## E.1.3. Changes

Below you will find a detailed account of the changes between PostgreSQL 14 and the previous major release.

### **E.1.3.1. Server**

* Add predefined roles [`pg_read_all_data`](https://www.postgresql.org/docs/14/predefined-roles.html) and `pg_write_all_data` \(Stephen Frost\)

  These non-login roles can be used to give read or write permission to all tables, views, and sequences.

* Add predefined role [`pg_database_owner`](https://www.postgresql.org/docs/14/predefined-roles.html) that contains only the current database's owner \(Noah Misch\)

  This is especially useful in template databases.

* Remove temporary files after backend crashes \(Euler Taveira\)

  Previously, such files were retained for debugging purposes. If necessary, deletion can be disabled with the new server parameter [remove\_temp\_files\_after\_crash](https://www.postgresql.org/docs/14/runtime-config-developer.html#GUC-REMOVE-TEMP-FILES-AFTER-CRASH).

* Allow long-running queries to be canceled if the client disconnects \(Sergey Cherkashin, Thomas Munro\)

  The server parameter [client\_connection\_check\_interval](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-CLIENT-CONNECTION-CHECK-INTERVAL) allows control over whether loss of connection is checked for intra-query. \(This is supported on Linux and a few other operating systems.\)

* Add an optional timeout parameter to [`pg_terminate_backend()`](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL)
* Allow wide tuples to be always added to almost-empty heap pages \(John Naylor, Floris van Nee\)

  Previously tuples whose insertion would have exceeded the page's [fill factor](https://www.postgresql.org/docs/14/sql-createtable.html) were instead added to new pages.

* Add Server Name Indication \(SNI\) in SSL connection packets \(Peter Eisentraut\)

  This can be disabled by turning off client connection option [`sslsni`](https://www.postgresql.org/docs/14/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

#### **E.1.3.1.1. Vacuuming**

* Allow vacuum to skip index vacuuming when the number of removable index entries is insignificant \(Masahiko Sawada, Peter Geoghegan\)

  The vacuum parameter [`INDEX_CLEANUP`](https://www.postgresql.org/docs/14/sql-vacuum.html) has a new default of `auto` that enables this optimization.

* Allow vacuum to more eagerly add deleted btree pages to the free space map \(Peter Geoghegan\)

  Previously vacuum could only add pages to the free space map that were marked as deleted by previous vacuums.

* Allow vacuum to reclaim space used by unused trailing heap line pointers \(Matthias van de Meent, Peter Geoghegan\)
* Allow vacuum to be more aggressive in removing dead rows during minimal-locking index operations \(Álvaro Herrera\)

  Specifically, `CREATE INDEX CONCURRENTLY` and `REINDEX CONCURRENTLY` no longer limit the dead row removal of other relations.

* Speed up vacuuming of databases with many relations \(Tatsuhito Kasahara\)
* Reduce the default value of [vacuum\_cost\_page\_miss](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-MISS) to better reflect current hardware capabilities \(Peter Geoghegan\)
* Add ability to skip vacuuming of TOAST tables \(Nathan Bossart\)

  [`VACUUM`](https://www.postgresql.org/docs/14/sql-vacuum.html) now has a `PROCESS_TOAST` option which can be set to false to disable TOAST processing, and [vacuumdb](https://www.postgresql.org/docs/14/app-vacuumdb.html) has a `--no-process-toast` option.

* Have [`COPY FREEZE`](https://www.postgresql.org/docs/14/sql-copy.html) appropriately update page visibility bits \(Anastasia Lubennikova, Pavan Deolasee, Jeff Janes\)
* Cause vacuum operations to be more aggressive if the table is near xid or multixact wraparound \(Masahiko Sawada, Peter Geoghegan\)

  This is controlled by [vacuum\_failsafe\_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-FAILSAFE-AGE) and [vacuum\_multixact\_failsafe\_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-MULTIXACT-FAILSAFE-AGE).

* Increase warning time and hard limit before transaction id and multi-transaction wraparound \(Noah Misch\)

  This should reduce the possibility of failures that occur without having issued warnings about wraparound.

* Add per-index information to [autovacuum logging output](https://www.postgresql.org/docs/14/runtime-config-logging.html#GUC-LOG-AUTOVACUUM-MIN-DURATION) \(Masahiko Sawada\)

#### **E.1.3.1.2. Partitioning**

* Improve the performance of updates and deletes on partitioned tables with many partitions \(Amit Langote, Tom Lane\)

  This change greatly reduces the planner's overhead for such cases, and also allows updates/deletes on partitioned tables to use execution-time partition pruning.

* Allow partitions to be [detached](https://www.postgresql.org/docs/14/sql-altertable.html) in a non-blocking manner \(Álvaro Herrera\)

  The syntax is `ALTER TABLE ... DETACH PARTITION ... CONCURRENTLY`, and `FINALIZE`.

* Ignore `COLLATE` clauses in partition boundary values \(Tom Lane\)

  Previously any such clause had to match the collation of the partition key; but it's more consistent to consider that it's automatically coerced to the collation of the partition key.

#### **E.1.3.1.3. Indexes**

* Allow btree index additions to [remove expired index entries](https://www.postgresql.org/docs/14/btree-implementation.html#BTREE-DELETION) to prevent page splits \(Peter Geoghegan\)

  This is particularly helpful for reducing index bloat on tables whose indexed columns are frequently updated.

* Allow [BRIN](https://www.postgresql.org/docs/14/brin.html) indexes to record multiple min/max values per range \(Tomas Vondra\)

  This is useful if there are groups of values in each page range.

* Allow BRIN indexes to use bloom filters \(Tomas Vondra\)

  This allows BRIN indexes to be used effectively with data that is not well-localized in the heap.

* Allow some [GiST](https://www.postgresql.org/docs/14/gist.html) indexes to be built by presorting the data \(Andrey Borodin\)

  Presorting happens automatically and allows for faster index creation and smaller indexes.

* Allow [SP-GiST](https://www.postgresql.org/docs/14/spgist.html) indexes to contain `INCLUDE`'d columns \(Pavel Borisov\)

#### **E.1.3.1.4. Optimizer**

* Allow hash lookup for `IN` clauses with many constants \(James Coleman, David Rowley\)

  Previously the code always sequentially scanned the list of values.

* Increase the number of places [extended statistics](https://www.postgresql.org/docs/14/planner-stats.html#PLANNER-STATS-EXTENDED) can be used for `OR` clause estimation \(Tomas Vondra, Dean Rasheed\)
* Allow extended statistics on expressions \(Tomas Vondra\)

  This allows statistics on a group of expressions and columns, rather than only columns like previously. System view [`pg_stats_ext_exprs`](https://www.postgresql.org/docs/14/view-pg-stats-ext-exprs.html) reports such statistics.

* Allow efficient heap scanning of a range of [`TIDs`](https://www.postgresql.org/docs/14/datatype-oid.html#DATATYPE-OID-TABLE) \(Edmund Horner, David Rowley\)

  Previously a sequential scan was required for non-equality `TID` specifications.

* Fix [`EXPLAIN CREATE TABLE AS`](https://www.postgresql.org/docs/14/sql-explain.html) and `EXPLAIN CREATE MATERIALIZED VIEW` to honor `IF NOT EXISTS` \(Bharath Rupireddy\)

  Previously, if the object already existed, `EXPLAIN` would fail.

#### **E.1.3.1.5. General Performance**

* Improve the speed of computing MVCC [visibility snapshots](https://www.postgresql.org/docs/14/mvcc.html) on systems with many CPUs and high session counts \(Andres Freund\)

  This also improves performance when there are many idle sessions.

* Add executor method to memoize results from the inner side of a nested-loop join \(David Rowley\)

  This is useful if only a small percentage of rows is checked on the inner side. It can be disabled via server parameter [enable\_memoize](https://www.postgresql.org/docs/14/runtime-config-query.html#GUC-ENABLE-MEMOIZE).

* Allow [window functions](https://www.postgresql.org/docs/14/functions-window.html) to perform incremental sorts \(David Rowley\)
* Improve the I/O performance of parallel sequential scans \(Thomas Munro, David Rowley\)

  This was done by allocating blocks in groups to [parallel workers](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS).

* Allow a query referencing multiple [foreign tables](https://www.postgresql.org/docs/14/sql-createforeigntable.html) to perform foreign table scans in parallel \(Robert Haas, Kyotaro Horiguchi, Thomas Munro, Etsuro Fujita\)

  [postgres\_fdw](https://www.postgresql.org/docs/14/postgres-fdw.html) supports this type of scan if `async_capable` is set.

* Allow [analyze](https://www.postgresql.org/docs/14/routine-vacuuming.html#VACUUM-FOR-STATISTICS) to do page prefetching \(Stephen Frost\)

  This is controlled by [maintenance\_io\_concurrency](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-MAINTENANCE-IO-CONCURRENCY).

* Improve performance of [regular expression](https://www.postgresql.org/docs/14/functions-matching.html#FUNCTIONS-POSIX-REGEXP) searches \(Tom Lane\)
* Dramatically improve Unicode normalization \(John Naylor\)

  This speeds [`normalize()`](https://www.postgresql.org/docs/14/functions-string.html) and `IS NORMALIZED`.

* Add ability to use [LZ4 compression](https://www.postgresql.org/docs/14/sql-createtable.html) on TOAST data \(Dilip Kumar\)

  This can be set at the column level, or set as a default via server parameter [default\_toast\_compression](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TOAST-COMPRESSION). The server must be compiled with [`--with-lz4`](https://www.postgresql.org/docs/14/install-procedure.html#CONFIGURE-OPTIONS-FEATURES) to support this feature. The default setting is still pglz.

#### **E.1.3.1.6. Monitoring**

* If server parameter [compute\_query\_id](https://www.postgresql.org/docs/14/runtime-config-statistics.html#GUC-COMPUTE-QUERY-ID) is enabled, display the query id in [`pg_stat_activity`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW), [`EXPLAIN VERBOSE`](https://www.postgresql.org/docs/14/sql-explain.html), [csvlog](https://www.postgresql.org/docs/14/runtime-config-logging.html), and optionally in [log\_line\_prefix](https://www.postgresql.org/docs/14/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) \(Julien Rouhaud\)

  A query id computed by an extension will also be displayed.

* Improve logging of [auto-vacuum](https://www.postgresql.org/docs/14/routine-vacuuming.html#AUTOVACUUM) and auto-analyze \(Stephen Frost, Jakub Wartak\)

  This reports I/O timings for auto-vacuum and auto-analyze if [track\_io\_timing](https://www.postgresql.org/docs/14/runtime-config-statistics.html#GUC-TRACK-IO-TIMING) is enabled. Also, report buffer read and dirty rates for auto-analyze.

* Add information about the original user name supplied by the client to the output of [log\_connections](https://www.postgresql.org/docs/14/runtime-config-logging.html#GUC-LOG-CONNECTIONS) \(Jacob Champion\)

#### **E.1.3.1.7. System Views**

* Add system view [`pg_stat_progress_copy`](https://www.postgresql.org/docs/14/progress-reporting.html#COPY-PROGRESS-REPORTING) to report `COPY` progress \(Josef Šimánek, Matthias van de Meent\)
* Add system view [`pg_stat_wal`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-PG-STAT-WAL-VIEW) to report WAL activity \(Masahiro Ikeda\)
* Add system view [`pg_stat_replication_slots`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) to report replication slot activity \(Sawada Masahiko, Amit Kapila, Vignesh C\)

  The function [`pg_stat_reset_replication_slot()`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-STATS-FUNCTIONS) resets slot statistics.

* Add system view [`pg_backend_memory_contexts`](https://www.postgresql.org/docs/14/view-pg-backend-memory-contexts.html) to report session memory usage \(Atsushi Torikoshi, Fujii Masao\)
* Add function [`pg_log_backend_memory_contexts()`](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL) to output the memory contexts of arbitrary backends \(Atsushi Torikoshi\)
* Add session statistics to the [`pg_stat_database`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-VIEW) system view \(Laurenz Albe\)
* Add columns to [`pg_prepared_statements`](https://www.postgresql.org/docs/14/view-pg-prepared-statements.html) to report generic and custom plan counts \(Atsushi Torikoshi, Kyotaro Horiguchi\)
* Add lock wait start time to [`pg_locks`](https://www.postgresql.org/docs/14/view-pg-locks.html) \(Atsushi Torikoshi\)
* Make the archiver process visible in `pg_stat_activity` \(Kyotaro Horiguchi\)
* Add wait event [`WalReceiverExit`](https://www.postgresql.org/docs/14/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW) to report WAL receiver exit wait time \(Fujii Masao\)
* Implement information schema view [`routine_column_usage`](https://www.postgresql.org/docs/14/infoschema-routine-column-usage.html) to track columns referenced by function and procedure default expressions \(Peter Eisentraut\)

#### **E.1.3.1.8. Authentication**

* Allow an SSL certificate's distinguished name \(DN\) to be matched for client certificate authentication \(Andrew Dunstan\)

  The new [`pg_hba.conf`](https://www.postgresql.org/docs/14/auth-pg-hba-conf.html) option `clientname=DN` allows comparison with certificate attributes beyond the `CN` and can be combined with ident maps.

* Allow `pg_hba.conf` and [`pg_ident.conf`](https://www.postgresql.org/docs/14/auth-username-maps.html) records to span multiple lines \(Fabien Coelho\)

  A backslash at the end of a line allows record contents to be continued on the next line.

* Allow the specification of a certificate revocation list \(CRL\) directory \(Kyotaro Horiguchi\)

  This is controlled by server parameter [ssl\_crl\_dir](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-SSL-CRL-DIR) and libpq connection option [sslcrldir](https://www.postgresql.org/docs/14/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR). Previously only single CRL files could be specified.

* Allow passwords of an arbitrary length \(Tom Lane, Nathan Bossart\)

#### **E.1.3.1.9. Server Configuration**

* Add server parameter [idle\_session\_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-IDLE-SESSION-TIMEOUT) to close idle sessions \(Li Japin\)

  This is similar to [idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT).

* Change [checkpoint\_completion\_target](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET) default to 0.9 \(Stephen Frost\)

  The previous default was 0.5.

* Allow `%P` in [log\_line\_prefix](https://www.postgresql.org/docs/14/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) to report the parallel group leader's PID for a parallel worker \(Justin Pryzby\)
* Allow [unix\_socket\_directories](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-UNIX-SOCKET-DIRECTORIES) to specify paths as individual, comma-separated quoted strings \(Ian Lawrence Barwick\)

  Previously all the paths had to be in a single quoted string.

* Allow startup allocation of dynamic shared memory \(Thomas Munro\)

  This is controlled by [min\_dynamic\_shared\_memory](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-MIN-DYNAMIC-SHARED-MEMORY). This allows more use of huge pages.

* Add server parameter [huge\_page\_size](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-HUGE-PAGE-SIZE) to control the size of huge pages used on Linux \(Odin Ugedal\)

### **E.1.3.2. Streaming Replication And Recovery**

* Allow standby servers to be rewound via [pg\_rewind](https://www.postgresql.org/docs/14/app-pgrewind.html) \(Heikki Linnakangas\)
* Allow the [restore\_command](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RESTORE-COMMAND) setting to be changed during a server reload \(Sergei Kornilov\)

  You can also set `restore_command` to an empty string and reload to force recovery to only read from the [`pg_wal`](https://www.postgresql.org/docs/14/storage-file-layout.html) directory.

* Add server parameter [log\_recovery\_conflict\_waits](https://www.postgresql.org/docs/14/runtime-config-logging.html#GUC-LOG-RECOVERY-CONFLICT-WAITS) to report long recovery conflict wait times \(Bertrand Drouvot, Masahiko Sawada\)
* Pause recovery on a hot standby server if the primary changes its parameters in a way that prevents replay on the standby \(Peter Eisentraut\)

  Previously the standby would shut down immediately.

* Add function [`pg_get_wal_replay_pause_state()`](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL) to report the recovery state \(Dilip Kumar\)

  It gives more detailed information than [`pg_is_wal_replay_paused()`](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL), which still exists.

* Add new read-only server parameter [in\_hot\_standby](https://www.postgresql.org/docs/14/runtime-config-preset.html#GUC-IN-HOT-STANDBY) \(Haribabu Kommi, Greg Nancarrow, Tom Lane\)

  This allows clients to easily detect whether they are connected to a hot standby server.

* Speed truncation of small tables during recovery on clusters with a large number of shared buffers \(Kirk Jamison\)
* Allow file system sync at the start of crash recovery on Linux \(Thomas Munro\)

  By default, PostgreSQL opens and fsyncs each data file in the database cluster at the start of crash recovery. A new setting, [recovery\_init\_sync\_method](https://www.postgresql.org/docs/14/runtime-config-error-handling.html#GUC-RECOVERY-INIT-SYNC-METHOD)`=syncfs`, instead syncs each filesystem used by the cluster. This allows for faster recovery on systems with many database files.

* Add function [`pg_xact_commit_timestamp_origin()`](https://www.postgresql.org/docs/14/functions-info.html) to return the commit timestamp and replication origin of the specified transaction \(Movead Li\)
* Add the replication origin to the record returned by [`pg_last_committed_xact()`](https://www.postgresql.org/docs/14/functions-info.html) \(Movead Li\)
* Allow replication [origin functions](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-REPLICATION) to be controlled using standard function permission controls \(Martín Marqués\)

  Previously these functions could only be executed by superusers, and this is still the default.

#### **E.1.3.2.1. Logical Replication**

* Allow logical replication to stream long in-progress transactions to subscribers \(Dilip Kumar, Amit Kapila, Ajin Cherian, Tomas Vondra, Nikhil Sontakke, Stas Kelvich\)

  Previously transactions that exceeded [logical\_decoding\_work\_mem](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-LOGICAL-DECODING-WORK-MEM) were written to disk until the transaction completed.

* Enhance the logical replication API to allow streaming large in-progress transactions \(Tomas Vondra, Dilip Kumar, Amit Kapila\)

  The output functions begin with [`stream`](https://www.postgresql.org/docs/14/logicaldecoding-output-plugin.html#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-START). test\_decoding also supports these.

* Allow multiple transactions during table sync in logical replication \(Peter Smith, Amit Kapila, and Takamichi Osumi\)
* Immediately WAL-log subtransaction and top-level `XID` association \(Tomas Vondra, Dilip Kumar, Amit Kapila\)

  This is useful for logical decoding.

* Enhance logical decoding APIs to handle two-phase commits \(Ajin Cherian, Amit Kapila, Nikhil Sontakke, Stas Kelvich\)

  This is controlled via [`pg_create_logical_replication_slot()`](https://www.postgresql.org/docs/14/functions-admin.html#FUNCTIONS-REPLICATION).

* Generate WAL invalidation messages during command completion when using logical replication \(Dilip Kumar, Tomas Vondra, Amit Kapila\)

  When logical replication is disabled, WAL invalidation messages are generated at transaction completion. This allows logical streaming of in-progress transactions.

* Allow logical decoding to more efficiently process cache invalidation messages \(Dilip Kumar\)

  This allows [logical decoding](https://www.postgresql.org/docs/14/logicaldecoding.html) to work efficiently in presence of a large amount of DDL.

* Allow control over whether logical decoding messages are sent to the replication stream \(David Pirotte, Euler Taveira\)
* Allow logical replication subscriptions to use binary transfer mode \(Dave Cramer\)

  This is faster than text mode, but slightly less robust.

* Allow logical decoding to be filtered by xid \(Markus Wanner\)

### **E.1.3.3. SELECT, INSERT**

* Reduce the number of keywords that can't be used as column labels without `AS` \(Mark Dilger\)

  There are now 90% fewer restricted keywords.

* Allow an alias to be specified for `JOIN`'s `USING` clause \(Peter Eisentraut\)

  The alias is created by writing `AS` after the `USING` clause. It can be used as a table qualification for the merged `USING` columns.

* Allow `DISTINCT` to be added to `GROUP BY` to remove duplicate `GROUPING SET` combinations \(Vik Fearing\)

  For example, `GROUP BY CUBE (a,b), CUBE (b,c)` will generate duplicate grouping combinations without `DISTINCT`.

* Properly handle `DEFAULT` entries in multi-row `VALUES` lists in `INSERT` \(Dean Rasheed\)

  Such cases used to throw an error.

* Add SQL-standard `SEARCH` and `CYCLE` clauses for [common table expressions](https://www.postgresql.org/docs/14/queries-with.html) \(Peter Eisentraut\)

  The same results could be accomplished using existing syntax, but much less conveniently.

* Allow column names in the `WHERE` clause of `ON CONFLICT` to be table-qualified \(Tom Lane\)

  Only the target table can be referenced, however.

### **E.1.3.4. Utility Commands**

* Allow [`REFRESH MATERIALIZED VIEW`](https://www.postgresql.org/docs/14/sql-refreshmaterializedview.html) to use parallelism \(Bharath Rupireddy\)
* Allow [`REINDEX`](https://www.postgresql.org/docs/14/sql-reindex.html) to change the tablespace of the new index \(Alexey Kondratov, Michael Paquier, Justin Pryzby\)

  This is done by specifying a `TABLESPACE` clause. A `--tablespace` option was also added to [reindexdb](https://www.postgresql.org/docs/14/app-reindexdb.html) to control this.

* Allow `REINDEX` to process all child tables or indexes of a partitioned relation \(Justin Pryzby, Michael Paquier\)
* Allow index commands using `CONCURRENTLY` to avoid waiting for the completion of other operations using `CONCURRENTLY` \(Álvaro Herrera\)
* Improve the performance of [`COPY FROM`](https://www.postgresql.org/docs/14/sql-copy.html) in binary mode \(Bharath Rupireddy, Amit Langote\)
* Preserve SQL standard syntax for SQL-defined functions in [view definitions](https://www.postgresql.org/docs/14/sql-createview.html) \(Tom Lane\)

  Previously, calls to SQL-standard functions such as [`EXTRACT()`](https://www.postgresql.org/docs/14/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT) were shown in plain function-call syntax. The original syntax is now preserved when displaying a view or rule.

* Add the SQL-standard clause `GRANTED BY` to [`GRANT`](https://www.postgresql.org/docs/14/sql-grant.html) and [`REVOKE`](https://www.postgresql.org/docs/14/sql-revoke.html) \(Peter Eisentraut\)
* Add `OR REPLACE` option for [`CREATE TRIGGER`](https://www.postgresql.org/docs/14/sql-createtrigger.html) \(Takamichi Osumi\)

  This allows pre-existing triggers to be conditionally replaced.

* Allow [`TRUNCATE`](https://www.postgresql.org/docs/14/sql-truncate.html) to operate on foreign tables \(Kazutaka Onishi, Kohei KaiGai\)

  The [postgres\_fdw](https://www.postgresql.org/docs/14/postgres-fdw.html) module also now supports this.

* Allow publications to be more easily added to and removed from a subscription \(Japin Li\)

  The new syntax is [`ALTER SUBSCRIPTION ... ADD/DROP PUBLICATION`](https://www.postgresql.org/docs/14/sql-altersubscription.html). This avoids having to specify all publications to add/remove entries.

* Add primary keys, unique constraints, and foreign keys to [system catalogs](https://www.postgresql.org/docs/14/catalogs.html) \(Peter Eisentraut\)

  These changes help GUI tools analyze the system catalogs. The existing unique indexes of catalogs now have associated `UNIQUE` or `PRIMARY KEY` constraints. Foreign key relationships are not actually stored or implemented as constraints, but can be obtained for display from the function [pg\_get\_catalog\_foreign\_keys\(\)](https://www.postgresql.org/docs/14/functions-info.html#FUNCTIONS-INFO-CATALOG-TABLE).

* Allow [`CURRENT_ROLE`](https://www.postgresql.org/docs/14/functions-info.html) every place `CURRENT_USER` is accepted \(Peter Eisentraut\)

### **E.1.3.5. Data Types**

* Allow extensions and built-in data types to implement [subscripting](https://www.postgresql.org/docs/14/sql-altertype.html) \(Dmitry Dolgov\)

  Previously subscript handling was hard-coded into the server, so that subscripting could only be applied to array types. This change allows subscript notation to be used to extract or assign portions of a value of any type for which the concept makes sense.

* Allow subscripting of [`JSONB`](https://www.postgresql.org/docs/14/datatype-json.html) \(Dmitry Dolgov\)

  `JSONB` subscripting can be used to extract and assign to portions of `JSONB` documents.

* Add support for [multirange data types](https://www.postgresql.org/docs/14/rangetypes.html) \(Paul Jungwirth, Alexander Korotkov\)

  These are like range data types, but they allow the specification of multiple, ordered, non-overlapping ranges. An associated multirange type is automatically created for every range type.

* Add support for the [stemming](https://www.postgresql.org/docs/14/textsearch-dictionaries.html#TEXTSEARCH-SNOWBALL-DICTIONARY) of languages Armenian, Basque, Catalan, Hindi, Serbian, and Yiddish \(Peter Eisentraut\)
* Allow [tsearch data files](https://www.postgresql.org/docs/14/textsearch-intro.html#TEXTSEARCH-INTRO-CONFIGURATIONS) to have unlimited line lengths \(Tom Lane\)

  The previous limit was 4K bytes. Also remove function `t_readline()`.

* Add support for `Infinity` and `-Infinity` values in the [numeric data type](https://www.postgresql.org/docs/14/datatype-numeric.html) \(Tom Lane\)

  Floating-point data types already supported these.

* Add [point operators](https://www.postgresql.org/docs/14/functions-geometry.html) `<<|` and `|>>` representing strictly above/below tests \(Emre Hasegeli\)

  Previously these were called `>^` and `<^`, but that naming is inconsistent with other geometric data types. The old names remain available, but may someday be removed.

* Add operators to add and subtract [`LSN`](https://www.postgresql.org/docs/14/datatype-pg-lsn.html) and numeric \(byte\) values \(Fujii Masao\)
* Allow [binary data transfer](https://www.postgresql.org/docs/14/protocol-overview.html#PROTOCOL-FORMAT-CODES) to be more forgiving of array and record `OID` mismatches \(Tom Lane\)
* Create composite array types for system catalogs \(Wenjing Zeng\)

  User-defined relations have long had composite types associated with them, and also array types over those composite types. System catalogs now do as well. This change also fixes an inconsistency that creating a user-defined table in single-user mode would fail to create a composite array type.

### **E.1.3.6. Functions**

* Allow SQL-language [functions](https://www.postgresql.org/docs/14/sql-createfunction.html) and [procedures](https://www.postgresql.org/docs/14/sql-createprocedure.html) to use SQL-standard function bodies \(Peter Eisentraut\)

  Previously only string-literal function bodies were supported. When writing a function or procedure in SQL-standard syntax, the body is parsed immediately and stored as a parse tree. This allows better tracking of function dependencies, and can have security benefits.

* Allow [procedures](https://www.postgresql.org/docs/14/sql-createprocedure.html) to have `OUT` parameters \(Peter Eisentraut\)
* Allow some array functions to operate on a mix of compatible data types \(Tom Lane\)

  The functions [`array_append()`](https://www.postgresql.org/docs/14/functions-array.html), `array_prepend()`, `array_cat()`, `array_position()`, `array_positions()`, `array_remove()`, `array_replace()`, and [`width_bucket()`](https://www.postgresql.org/docs/14/functions-math.html) now take `anycompatiblearray` instead of `anyarray` arguments. This makes them less fussy about exact matches of argument types.

* Add SQL-standard [`trim_array()`](https://www.postgresql.org/docs/14/functions-array.html) function \(Vik Fearing\)

  This could already be done with array slices, but less easily.

* Add `bytea` equivalents of [`ltrim()`](https://www.postgresql.org/docs/14/functions-binarystring.html) and `rtrim()` \(Joel Jacobson\)
* Support negative indexes in [`split_part()`](https://www.postgresql.org/docs/14/functions-string.html) \(Nikhil Benesch\)

  Negative values start from the last field and count backward.

* Add [`string_to_table()`](https://www.postgresql.org/docs/14/functions-string.html) function to split a string on delimiters \(Pavel Stehule\)

  This is similar to the [`regexp_split_to_table()`](https://www.postgresql.org/docs/14/functions-string.html) function.

* Add [`unistr()`](https://www.postgresql.org/docs/14/functions-string.html) function to allow Unicode characters to be specified as backslash-hex escapes in strings \(Pavel Stehule\)

  This is similar to how Unicode can be specified in literal strings.

* Add [`bit_xor()`](https://www.postgresql.org/docs/14/functions-aggregate.html) XOR aggregate function \(Alexey Bashtanov\)
* Add function [`bit_count()`](https://www.postgresql.org/docs/14/functions-binarystring.html) to return the number of bits set in a bit or byte string \(David Fetter\)
* Add [`date_bin()`](https://www.postgresql.org/docs/14/functions-datetime.html#FUNCTIONS-DATETIME-BIN) function \(John Naylor\)

  This function “bins” input timestamps, grouping them into intervals of a uniform length aligned with a specified origin.

* Allow [`make_timestamp()`](https://www.postgresql.org/docs/14/functions-datetime.html)/`make_timestamptz()` to accept negative years \(Peter Eisentraut\)

  Negative values are interpreted as `BC` years.

* Add newer regular expression [`substring()`](https://www.postgresql.org/docs/14/functions-string.html) syntax \(Peter Eisentraut\)

  The new SQL-standard syntax is `SUBSTRING(text SIMILAR pattern ESCAPE escapechar)`. The previous standard syntax was `SUBSTRING(text FROM pattern FOR escapechar)`, which is still accepted by PostgreSQL.

* Allow complemented character class escapes [\D](https://www.postgresql.org/docs/14/functions-matching.html#POSIX-ESCAPE-SEQUENCES), `\S`, and `\W` within regular expression brackets \(Tom Lane\)
* Add [`[[:word:]]`](https://www.postgresql.org/docs/14/functions-matching.html#POSIX-BRACKET-EXPRESSIONS) as a regular expression character class, equivalent to `\w` \(Tom Lane\)
* Allow more flexible data types for default values of [`lead()`](https://www.postgresql.org/docs/14/functions-window.html) and `lag()` window functions \(Vik Fearing\)
* Make non-zero [floating-point values](https://www.postgresql.org/docs/14/datatype-numeric.html#DATATYPE-FLOAT) divided by infinity return zero \(Kyotaro Horiguchi\)

  Previously such operations produced underflow errors.

* Make floating-point division of NaN by zero return NaN \(Tom Lane\)

  Previously this returned an error.

* Cause [`exp()`](https://www.postgresql.org/docs/14/functions-math.html) and `power()` for negative-infinity exponents to return zero \(Tom Lane\)

  Previously they often returned underflow errors.

* Improve the accuracy of geometric computations involving infinity \(Tom Lane\)
* Mark built-in type coercion functions as leakproof where possible \(Tom Lane\)

  This allows more use of functions that require type conversion in security-sensitive situations.

* Change [`pg_describe_object()`](https://www.postgresql.org/docs/14/functions-info.html), `pg_identify_object()`, and `pg_identify_object_as_address()` to always report helpful error messages for non-existent objects \(Michael Paquier\)

### **E.1.3.7. PL/PgSQL**

* Improve PL/pgSQL's [expression](https://www.postgresql.org/docs/14/plpgsql-expressions.html) and [assignment](https://www.postgresql.org/docs/14/plpgsql-statements.html#PLPGSQL-STATEMENTS-ASSIGNMENT) parsing \(Tom Lane\)

  This change allows assignment to array slices and nested record fields.

* Allow plpgsql's [`RETURN QUERY`](https://www.postgresql.org/docs/14/plpgsql-control-structures.html) to execute its query using parallelism \(Tom Lane\)
* Improve performance of repeated [CALL](https://www.postgresql.org/docs/14/plpgsql-transactions.html)s within plpgsql procedures \(Pavel Stehule, Tom Lane\)

### **E.1.3.8. Client Interfaces**

* Add [pipeline](https://www.postgresql.org/docs/14/libpq-pipeline-mode.html#LIBPQ-PIPELINE-SENDING) mode to libpq \(Craig Ringer, Matthieu Garrigues, Álvaro Herrera\)

  This allows multiple queries to be sent, only waiting for completion when a specific synchronization message is sent.

* Enhance libpq's [`target_session_attrs`](https://www.postgresql.org/docs/14/libpq-connect.html#LIBPQ-PARAMKEYWORDS) parameter options \(Haribabu Kommi, Greg Nancarrow, Vignesh C, Tom Lane\)

  The new options are `read-only`, `primary`, `standby`, and `prefer-standby`.

* Improve the output format of libpq's [`PQtrace()`](https://www.postgresql.org/docs/14/libpq-control.html) \(Aya Iwata, Álvaro Herrera\)
* Allow an ECPG SQL identifier to be linked to a specific connection \(Hayato Kuroda\)

  This is done via [`DECLARE ... STATEMENT`](https://www.postgresql.org/docs/14/ecpg-sql-declare-statement.html).

### **E.1.3.9. Client Applications**

* Allow [vacuumdb](https://www.postgresql.org/docs/14/app-vacuumdb.html) to skip index cleanup and truncation \(Nathan Bossart\)

  The options are `--no-index-cleanup` and `--no-truncate`.

* Allow [pg\_dump](https://www.postgresql.org/docs/14/app-pgdump.html) to dump only certain extensions \(Guillaume Lelarge\)

  This is controlled by option `--extension`.

* Add [pgbench](https://www.postgresql.org/docs/14/pgbench.html) `permute()` function to randomly shuffle values \(Fabien Coelho, Hironobu Suzuki, Dean Rasheed\)
* Include disconnection times in the reconnection overhead measured by pgbench with `-C` \(Yugo Nagata\)
* Allow multiple verbose option specifications \(`-v`\) to increase the logging verbosity \(Tom Lane\)

  This behavior is supported by [pg\_dump](https://www.postgresql.org/docs/14/app-pgdump.html), [pg\_dumpall](https://www.postgresql.org/docs/14/app-pg-dumpall.html), and [pg\_restore](https://www.postgresql.org/docs/14/app-pgrestore.html).

### **E.1.3.9.1. psql**

* Allow psql's `\df` and `\do` commands to specify function and operator argument types \(Greg Sabino Mullane, Tom Lane\)

  This helps reduce the number of matches printed for overloaded names.

* Add an access method column to psql's `\d[i|m|t]+` output \(Georgios Kokolatos\)
* Allow psql's `\dt` and `\di` to show TOAST tables and their indexes \(Justin Pryzby\)
* Add psql command `\dX` to list extended statistics objects \(Tatsuro Yamada\)
* Fix psql's `\dT` to understand array syntax and backend grammar aliases, like `int` for `integer` \(Greg Sabino Mullane, Tom Lane\)
* When editing the previous query or a file with psql's `\e`, or using `\ef` and `\ev`, ignore the results if the editor exits without saving \(Laurenz Albe\)

  Previously, such edits would load the previous query into the query buffer, and typically execute it immediately. This was deemed to be probably not what the user wants.

* Improve tab completion \(Vignesh C, Michael Paquier, Justin Pryzby, Georgios Kokolatos, Julien Rouhaud\)

### **E.1.3.10. Server Applications**

* Add command-line utility [pg\_amcheck](https://www.postgresql.org/docs/14/app-pgamcheck.html) to simplify running `contrib/amcheck` tests on many relations \(Mark Dilger\)
* Add `--no-instructions` option to [initdb](https://www.postgresql.org/docs/14/app-initdb.html) \(Magnus Hagander\)

  This suppresses the server startup instructions that are normally printed.

* Stop [pg\_upgrade](https://www.postgresql.org/docs/14/pgupgrade.html) from creating `analyze_new_cluster` script \(Magnus Hagander\)

  Instead, give comparable [vacuumdb](https://www.postgresql.org/docs/14/app-vacuumdb.html) instructions.

* Remove support for the [postmaster](https://www.postgresql.org/docs/14/app-postgres.html) `-o` option \(Magnus Hagander\)

  This option was unnecessary since all passed options could already be specified directly.

### **E.1.3.11. Documentation**

* Rename "Default Roles" to ["Predefined Roles"](https://www.postgresql.org/docs/14/predefined-roles.html) \(Bruce Momjian, Stephen Frost\)
* Add documentation for the [`factorial()`](https://www.postgresql.org/docs/14/functions-math.html#FUNCTION-FACTORIAL) function \(Peter Eisentraut\)

  With the removal of the ! operator in this release, `factorial()` is the only built-in way to compute a factorial.

### **E.1.3.12. Source Code**

* Add configure option [`--with-ssl={openssl}`](https://www.postgresql.org/docs/14/install-procedure.html#CONFIGURE-OPTIONS-FEATURES) to allow future choice of the SSL library to use \(Daniel Gustafsson, Michael Paquier\)

  The spelling `--with-openssl` is kept for compatibility.

* Add support for [abstract Unix-domain sockets](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-UNIX-SOCKET-DIRECTORIES) \(Peter Eisentraut\)

  This is currently supported on Linux and Windows.

* Allow Windows to properly handle files larger than four gigabytes \(Juan José Santamaría Flecha\)

  For example this allows [`COPY,`](https://www.postgresql.org/docs/14/sql-copy.html) [WAL](https://www.postgresql.org/docs/14/install-procedure.html#CONFIGURE-OPTIONS-MISC) files, and relation segment files to be larger than four gigabytes.

* Add server parameter [debug\_discard\_caches](https://www.postgresql.org/docs/14/runtime-config-developer.html#GUC-DEBUG-DISCARD-CACHES) to control cache flushing for test purposes \(Craig Ringer\)

  Previously this behavior could only be set at compile time. To invoke it during initdb, use the new option `--discard-caches`.

* Various improvements in valgrind error detection ability \(Álvaro Herrera, Peter Geoghegan\)
* Add a test module for the regular expression package \(Tom Lane\)
* Add support for LLVM version 12 \(Andres Freund\)
* Change SHA1, SHA2, and MD5 hash computations to use the OpenSSL EVP API \(Michael Paquier\)

  This is more modern and supports FIPS mode.

* Remove separate build-time control over the choice of random number generator \(Daniel Gustafsson\)

  This is now always determined by the choice of SSL library.

* Add direct conversion routines between EUC\_TW and Big5 encodings \(Heikki Linnakangas\)
* Add collation version support for FreeBSD \(Thomas Munro\)
* Add [`amadjustmembers`](https://www.postgresql.org/docs/14/index-api.html) to the index access method API \(Tom Lane\)

  This allows an index access method to provide validity checking during creation of a new operator class or family.

* Provide feature-test macros in `libpq-fe.h` for recently-added libpq features \(Tom Lane, Álvaro Herrera\)

  Historically, applications have usually used compile-time checks of `PG_VERSION_NUM` to test whether a feature is available. But that's normally the server version, which might not be a good guide to libpq's version. `libpq-fe.h` now offers `#define` symbols denoting application-visible features added in v14; the intent is to keep adding symbols for such features in future versions.

### **E.1.3.13. Additional Modules**

* Allow subscripting of [hstore](https://www.postgresql.org/docs/14/hstore.html) values \(Tom Lane, Dmitry Dolgov\)
* Allow GiST/GIN [pg\_trgm](https://www.postgresql.org/docs/14/pgtrgm.html) indexes to do equality lookups \(Julien Rouhaud\)

  This is similar to `LIKE` except no wildcards are honored.

* Allow the [cube](https://www.postgresql.org/docs/14/cube.html) data type to be transferred in binary mode \(KaiGai Kohei\)
* Allow [`pgstattuple_approx()`](https://www.postgresql.org/docs/14/pgstattuple.html) to report on TOAST tables \(Peter Eisentraut\)
* Add contrib module [pg\_surgery](https://www.postgresql.org/docs/14/pgsurgery.html) which allows changes to row visibility \(Ashutosh Sharma\)

  This is useful for correcting database corruption.

* Add contrib module [old\_snapshot](https://www.postgresql.org/docs/14/oldsnapshot.html) to report the `XID`/time mapping used by an active [old\_snapshot\_threshold](https://www.postgresql.org/docs/14/runtime-config-resource.html#GUC-OLD-SNAPSHOT-THRESHOLD) \(Robert Haas\)
* Allow [amcheck](https://www.postgresql.org/docs/14/amcheck.html) to also check heap pages \(Mark Dilger\)

  Previously it only checked B-Tree index pages.

* Allow [pageinspect](https://www.postgresql.org/docs/14/pageinspect.html) to inspect GiST indexes \(Andrey Borodin, Heikki Linnakangas\)
* Change pageinspect block numbers to be [`bigints`](https://www.postgresql.org/docs/14/datatype-numeric.html#DATATYPE-INT) \(Peter Eisentraut\)
* Mark [btree\_gist](https://www.postgresql.org/docs/14/btree-gist.html) functions as parallel safe \(Steven Winfield\)

#### **E.1.3.13.1. pg\_stat\_statements**

* Move query hash computation from pg\_stat\_statements to the core server \(Julien Rouhaud\)

  The new server parameter [compute\_query\_id](https://www.postgresql.org/docs/14/runtime-config-statistics.html#GUC-COMPUTE-QUERY-ID)'s default of `auto` will automatically enable query id computation when this extension is loaded.

* Cause pg\_stat\_statements to track top and nested statements separately \(Julien Rohaud\)

  Previously, when tracking all statements, identical top and nested statements were tracked as a single entry; but it seems more useful to separate such usages.

* Add row counts for utility commands to pg\_stat\_statements \(Fujii Masao, Katsuragi Yuta, Seino Yuki\)
* Add `pg_stat_statements_info` system view to show pg\_stat\_statements activity \(Katsuragi Yuta, Yuki Seino, Naoki Nakamichi\)

#### **E.1.3.13.2. postgres\_fdw**

* Allow postgres\_fdw to `INSERT` rows in bulk \(Takayuki Tsunakawa, Tomas Vondra, Amit Langote\)
* Allow postgres\_fdw to import table partitions if specified by [`IMPORT FOREIGN SCHEMA ... LIMIT TO`](https://www.postgresql.org/docs/14/sql-importforeignschema.html) \(Matthias van de Meent\)

  By default, only the root of a partitioned table is imported.

* Add postgres\_fdw function `postgres_fdw_get_connections()` to report open foreign server connections \(Bharath Rupireddy\)
* Allow control over whether foreign servers keep connections open after transaction completion \(Bharath Rupireddy\)

  This is controlled by `keep_connections` and defaults to on.

* Allow postgres\_fdw to reestablish foreign server connections if necessary \(Bharath Rupireddy\)

  Previously foreign server restarts could cause foreign table access errors.

* Add postgres\_fdw functions to discard cached connections \(Bharath Rupireddy\)

## E.1.4. Acknowledgments

The following individuals \(in alphabetical order\) have contributed to this release as patch authors, committers, reviewers, testers, or reporters of issues.

| Abhijit Menon-Sen |
| :--- |
| Ádám Balogh |
| Adrian Ho |
| Ahsan Hadi |
| Ajin Cherian |
| Aleksander Alekseev |
| Alessandro Gherardi |
| Alex Kozhemyakin |
| Alexander Korotkov |
| Alexander Lakhin |
| Alexander Nawratil |
| Alexander Pyhalov |
| Alexandra Wang |
| Alexey Bashtanov |
| Alexey Bulgakov |
| Alexey Kondratov |
| Álvaro Herrera |
| Amit Kapila |
| Amit Khandekar |
| Amit Langote |
| Amul Sul |
| Anastasia Lubennikova |
| Andreas Grob |
| Andreas Kretschmer |
| Andreas Seltenreich |
| Andreas Wicht |
| Andres Freund |
| Andrew Bille |
| Andrew Dunstan |
| Andrew Gierth |
| Andrey Borodin |
| Andrey Lepikhov |
| Andy Fan |
| Anton Voloshin |
| Antonin Houska |
| Arne Roland |
| Arseny Sher |
| Arthur Nascimento |
| Arthur Zakirov |
| Ashutosh Bapat |
| Ashutosh Sharma |
| Ashwin Agrawal |
| Asif Rehman |
| Asim Praveen |
| Atsushi Torikoshi |
| Aya Iwata |
| Barry Pederson |
| Bas Poot |
| Bauyrzhan Sakhariyev |
| Beena Emerson |
| Benoît Lobréau |
| Bernd Helmle |
| Bernhard M. Wiedemann |
| Bertrand Drouvot |
| Bharath Rupireddy |
| Boris Kolpackov |
| Brar Piening |
| Brian Ye |
| Bruce Momjian |
| Bryn Llewellyn |
| Cameron Daniel |
| Chapman Flack |
| Charles Samborski |
| Charlie Hornsby |
| Chen Jiaoqian |
| Chris Wilson |
| Christian Quest |
| Christoph Berg |
| Christophe Courtois |
| Corey Huinker |
| Craig Ringer |
| Dagfinn Ilmari Mannsåker |
| Dana Burd |
| Daniel Cherniy |
| Daniel Gustafsson |
| Daniel Vérité |
| Daniel Westermann |
| Daniele Varrazzo |
| Dar Alathar-Yemen |
| Darafei Praliaskouski |
| Dave Cramer |
| David Christensen |
| David Fetter |
| David G. Johnston |
| David Geier |
| David Gilman |
| David Pirotte |
| David Rowley |
| David Steele |
| David Turon |
| David Zhang |
| Dean Rasheed |
| Denis Patron |
| Dian Fay |
| Dilip Kumar |
| Dimitri Nüscheler |
| Dmitriy Kuzmin |
| Dmitry Dolgov |
| Dmitry Marakasov |
| Domagoj Smoljanovic |
| Dong Wook |
| Douglas Doole |
| Duncan Sands |
| Edmund Horner |
| Edson Richter |
| Egor Rogov |
| Ekaterina Kiryanova |
| Elena Indrupskaya |
| Emil Iggland |
| Emre Hasegeli |
| Eric Thinnes |
| Erik Rijkers |
| Erwin Brandstetter |
| Etienne Stalmans |
| Etsuro Fujita |
| Eugen Konkov |
| Euler Taveira |
| Fabien Coelho |
| Fabrízio de Royes Mello |
| Federico Caselli |
| Felix Lechner |
| Filip Gospodinov |
| Floris Van Nee |
| Frank Gagnepain |
| Frits Jalvingh |
| Georgios Kokolatos |
| Greg Nancarrow |
| Greg Rychlewski |
| Greg Sabino Mullane |
| Gregory Smith |
| Grigory Smolkin |
| Guillaume Lelarge |
| Guy Burgess |
| Guyren Howe |
| Haiying Tang |
| Hamid Akhtar |
| Hans Buschmann |
| Hao Wu |
| Haribabu Kommi |
| Harisai Hari |
| Hayato Kuroda |
| Heath Lord |
| Heikki Linnakangas |
| Henry Hinze |
| Herwig Goemans |
| Himanshu Upadhyaya |
| Hironobu Suzuki |
| Hiroshi Inoue |
| Hisanori Kobayashi |
| Honza Horak |
| Hou Zhijie |
| Hubert Lubaczewski |
| Hubert Zhang |
| Ian Barwick |
| Ibrar Ahmed |
| Ildus Kurbangaliev |
| Isaac Morland |
| Israel Barth |
| Itamar Gafni |
| Jacob Champion |
| Jaime Casanova |
| Jaime Soler |
| Jakub Wartak |
| James Coleman |
| James Hilliard |
| James Hunter |
| James Inform |
| Jan Mussler |
| Japin Li |
| Jasen Betts |
| Jason Harvey |
| Jason Kim |
| Jeevan Ladhe |
| Jeff Davis |
| Jeff Janes |
| Jelte Fennema |
| Jeremy Evans |
| Jeremy Finzel |
| Jeremy Smith |
| Jesse Kinkead |
| Jesse Zhang |
| Jie Zhang |
| Jim Doty |
| Jim Nasby |
| Jimmy Angelakos |
| Jimmy Yih |
| Jiri Fejfar |
| Joe Conway |
| Joel Jacobson |
| John Naylor |
| John Thompson |
| Jonathan Katz |
| Josef Šimánek |
| Joseph Nahmias |
| Josh Berkus |
| Juan José Santamaría Flecha |
| Julien Rouhaud |
| Junfeng Yang |
| Jürgen Purtz |
| Justin Pryzby |
| Kazutaka Onishi |
| Keisuke Kuroda |
| Kelly Min |
| Kensuke Okamura |
| Kevin Sweet |
| Kevin Yeap |
| Kirk Jamison |
| Kohei KaiGai |
| Konstantin Knizhnik |
| Kota Miyake |
| Krzysztof Gradek |
| Kuntal Ghosh |
| Kyle Kingsbury |
| Kyotaro Horiguchi |
| Laurent Hasson |
| Laurenz Albe |
| Lee Dong Wook |
| Li Japin |
| Liu Huailing |
| Luc Vlaming |
| Ludovic Kuty |
| Luis Roberto |
| Lukas Eder |
| Ma Liangzhu |
| Maciek Sakrejda |
| Madan Kumar |
| Magnus Hagander |
| Mahendra Singh Thalor |
| Maksim Milyutin |
| Marc Boeren |
| Marcin Krupowicz |
| Marco Atzeri |
| Marek Szuba |
| Marina Polyakova |
| Mario Emmenlauer |
| Mark Dilger |
| Mark Wong |
| Mark Zhao |
| Markus Wanner |
| Martín Marqués |
| Martin Visser |
| Masahiko Sawada |
| Masahiro Ikeda |
| Masao Fujii |
| Mathis Rudolf |
| Matthias van de Meent |
| Matthieu Garrigues |
| Matthijs van der Vleuten |
| Maxim Orlov |
| Melanie Plageman |
| Merlin Moncure |
| Michael Banck |
| Michael Brown |
| Michael Meskes |
| Michael Paquier |
| Michael Paul Killian |
| Michael Powers |
| Michael Vastola |
| Michail Nikolaev |
| Michal Albrycht |
| Mikael Gustavsson |
| Movead Li |
| Muhammad Usama |
| Nagaraj Raj |
| Naoki Nakamichi |
| Nathan Bossart |
| Nathan Long |
| Nazli Ugur Koyluoglu |
| Neha Sharma |
| Neil Chen |
| Nick Cleaton |
| Nico Williams |
| Nikhil Benesch |
| Nikhil Sontakke |
| Nikita Glukhov |
| Nikita Konev |
| Nikolai Berkoff |
| Nikolay Samokhvalov |
| Nikolay Shaplov |
| Nitin Jadhav |
| Noah Misch |
| Noriyoshi Shinoda |
| Odin Ugedal |
| Oleg Bartunov |
| Oleg Samoilov |
| Önder Kalaci |
| Pascal Legrand |
| Paul Förster |
| Paul Guo |
| Paul Jungwirth |
| Paul Martinez |
| Paul Sivash |
| Pavan Deolasee |
| Pavel Boev |
| Pavel Borisov |
| Pavel Luzanov |
| Pavel Stehule |
| Pengcheng Liu |
| Peter Eisentraut |
| Peter Geoghegan |
| Peter Smith |
| Peter Vandivier |
| Petr Fedorov |
| Petr Jelínek |
| Phil Krylov |
| Philipp Gramzow |
| Philippe Beaudoin |
| Phillip Menke |
| Pierre Giraud |
| Prabhat Sahu |
| Quan Zongliang |
| Rafi Shamim |
| Rahila Syed |
| Rajkumar Raghuwanshi |
| Ranier Vilela |
| Regina Obe |
| Rémi Lapeyre |
| Robert Foggia |
| Robert Grange |
| Robert Haas |
| Robert Kahlert |
| Robert Sosinski |
| Robert Treat |
| Robin Abbi |
| Robins Tharakan |
| Roger Mason |
| Rohit Bhogate |
| Roman Zharkov |
| Ron L. Johnson |
| Ronan Dunklau |
| Ryan Lambert |
| Ryo Matsumura |
| Saeed Hubaishan |
| Sait Talha Nisanci |
| Sandro Mani |
| Santosh Udupi |
| Scott Ribe |
| Sehrope Sarkuni |
| Sergei Kornilov |
| Sergey Bernikov |
| Sergey Cherkashin |
| Sergey Koposov |
| Sergey Shinderuk |
| Sergey Zubkovsky |
| Shawn Wang |
| Shay Rojansky |
| Shi Yu |
| Shinya Kato |
| Shinya Okano |
| Sigrid Ehrenreich |
| Simon Norris |
| Simon Riggs |
| Sofoklis Papasofokli |
| Soumyadeep Chakraborty |
| Stas Kelvich |
| Stephan Springl |
| Stéphane Lorek |
| Stephen Frost |
| Steven Winfield |
| Surafel Temesgen |
| Suraj Kharage |
| Sven Klemm |
| Takamichi Osumi |
| Takashi Menjo |
| Takayuki Tsunakawa |
| Tang Haiying |
| Tatsuhito Kasahara |
| Tatsuo Ishii |
| Tatsuro Yamada |
| Theodor Arsenij Larionov-Trichkin |
| Thomas Kellerer |
| Thomas Munro |
| Thomas Trenz |
| Tijs van Dam |
| Tom Ellis |
| Tom Gottfried |
| Tom Lane |
| Tom Vijlbrief |
| Tomas Barton |
| Tomas Vondra |
| Tomohiro Hiramitsu |
| Tony Reix |
| Vaishnavi Prabakaran |
| Valentin Gatien-Baron |
| Victor Wagner |
| Victor Yegorov |
| Vignesh C |
| Vik Fearing |
| Vitaly Ustinov |
| Vladimir Sitnikov |
| Vyacheslav Shablistyy |
| Wang Shenhao |
| Wei Wang |
| Wells Oliver |
| Wenjing Zeng |
| Wolfgang Walther |
| Yang Lin |
| Yanliang Lei |
| Yaoguang Chen |
| Yaroslav Pashinsky |
| Yaroslav Schekin |
| Yasushi Yamashita |
| Yoran Heling |
| YoungHwan Joo |
| Yugo Nagata |
| Yuki Seino |
| Yukun Wang |
| Yulin Pei |
| Yura Sokolov |
| Yuta Katsuragi |
| Yuta Kondo |
| Yuzuko Hosoya |
| Zhihong Yu |
| Zhiyong Wu |
| Zsolt Ero |

