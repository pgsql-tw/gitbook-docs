<a id="RELEASE-15-6"></a>

# E.14. Release 15.6

[E.14.1. Migration to Version 15.6](#id-1.11.6.19.4)

[E.14.2. Changes](#id-1.11.6.19.5)

<strong>Release date: </strong>2024-02-08

This release contains a variety of fixes from 15.5. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.19.4"></a>

## E.14.1. Migration to Version 15.6

A dump/restore is not required for those running 15.X.

However, one bug was fixed that could have resulted in corruption of GIN indexes during concurrent updates. If you suspect such corruption, reindex affected indexes after installing this update.

Also, if you are upgrading from a version earlier than 15.5, see [Section E.15](release-15-5.md).

<a id="id-1.11.6.19.5"></a>

## E.14.2. Changes

* Tighten security restrictions within `REFRESH MATERIALIZED VIEW CONCURRENTLY` (Heikki Linnakangas) [§](https://postgr.es/c/f2fdea198) [§](https://postgr.es/c/06f36bc01)

  One step of a concurrent refresh command was run under weak security restrictions. If a materialized view's owner could persuade a superuser or other high-privileged user to perform a concurrent refresh on that view, the view's owner could control code executed with the privileges of the user running `REFRESH`. Fix things so that all user-determined code is run as the view's owner, as expected.

  The only known exploit for this error does not work in PostgreSQL 16.0 and later, so it may be that v16 is not vulnerable in practice.

  The PostgreSQL Project thanks Pedro Gallegos for reporting this problem. (CVE-2024-0985)
* Fix memory leak when performing JIT inlining (Andres Freund, Daniel Gustafsson) [§](https://postgr.es/c/aef521849)

  There have been multiple reports of backend processes suffering out-of-memory conditions after sufficiently many JIT compilations. This fix should resolve that.
* When dequeueing from an LWLock, avoid needing to search the list of waiting processes (Andres Freund) [§](https://postgr.es/c/f374fb4aa)

  This fixes O(N^2) behavior when the list of waiters is long. In some use-cases this results in substantial throughput improvements.
* Avoid generating incorrect partitioned-join plans (Richard Guo) [§](https://postgr.es/c/12ec16d11)

  Some uncommon situations involving lateral references could create incorrect plans. Affected queries could produce wrong answers, or odd failures such as “variable not found in subplan target list”, or executor crashes.
* Fix incorrect wrapping of subquery output expressions in PlaceHolderVars (Tom Lane) [§](https://postgr.es/c/a0b4fda44)

  This fixes incorrect results when a subquery is underneath an outer join and has an output column that laterally references something outside the outer join's scope. The output column might not appear as NULL when it should do so due to the action of the outer join.
* Fix misprocessing of window function run conditions (Richard Guo) [§](https://postgr.es/c/c3f52fd5d)

  This oversight could lead to “WindowFunc not found in subplan target lists” errors.
* Skip inappropriate actions when `MERGE` causes a cross-partition update (Dean Rasheed) [§](https://postgr.es/c/c0bfdaf2b)

  When executing a `MERGE UPDATE` action on a partitioned table, if the `UPDATE` is turned into a `DELETE` and `INSERT` due to changing a partition key column, skip firing `AFTER UPDATE ROW` triggers, as well as other post-update actions such as RLS checks. These actions would typically fail, which is why a regular `UPDATE` doesn't do them in such cases; `MERGE` shouldn't either.
* Cope with `BEFORE ROW DELETE` triggers in cross-partition `MERGE` updates (Dean Rasheed) [§](https://postgr.es/c/7e8c6d7af)

  If such a trigger attempted to prevent the update by returning NULL, `MERGE` would suffer an error or assertion failure.
* Prevent access to a no-longer-pinned buffer in `BEFORE ROW UPDATE` triggers (Alexander Lakhin, Tom Lane) [§](https://postgr.es/c/1a4e54617)

  If the tuple being updated had just been updated and moved to another page by another session, there was a narrow window where we would attempt to fetch data from the new tuple version without any pin on its buffer. In principle this could result in garbage data appearing in non-updated columns of the proposed new tuple. The odds of problems in practice seem rather low, however.
* Avoid requesting an oversize shared-memory area in parallel hash join (Thomas Munro, Andrei Lepikhov, Alexander Korotkov) [§](https://postgr.es/c/1a7c03e6f) [§](https://postgr.es/c/6eecc3a62)

  The limiting value was too large, allowing “invalid DSA memory alloc request size” errors to occur with sufficiently large expected hash table sizes.
* Avoid assertion failures in `heap_update()` and `heap_delete()` when a tuple to be updated by a foreign-key enforcement trigger fails the extra visibility crosscheck (Alexander Lakhin) [§](https://postgr.es/c/2873fbfe0)

  This error had no impact in non-assert builds.
* Fix overly tight assertion about `false_positive_rate` parameter of BRIN bloom operator classes (Alexander Lakhin) [§](https://postgr.es/c/7e18c0bd6)

  This error had no impact in non-assert builds, either.
* Fix possible failure during `ALTER TABLE ADD COLUMN` on a complex inheritance tree (Tender Wang) [§](https://postgr.es/c/ad6fbbeeb)

  If a grandchild table would inherit the new column via multiple intermediate parents, the command failed with “tuple already updated by self”.
* Fix problems with duplicate token names in `ALTER TEXT SEARCH CONFIGURATION ... MAPPING` commands (Tender Wang, Michael Paquier) [§](https://postgr.es/c/41fa4b31c)
* Properly lock the associated table during `DROP STATISTICS` (Tomas Vondra) [§](https://postgr.es/c/0177fc773)

  Failure to acquire the lock could result in “tuple concurrently deleted” errors if the `DROP` executes concurrently with `ANALYZE`.
* Fix function volatility checking for `GENERATED` and `DEFAULT` expressions (Tom Lane) [§](https://postgr.es/c/9057ddbef)

  These places could fail to detect insertion of a volatile function default-argument expression, or decide that a polymorphic function is volatile although it is actually immutable on the datatype of interest. This could lead to improperly rejecting or accepting a `GENERATED` clause, or to mistakenly applying the constant-default-value optimization in `ALTER TABLE ADD COLUMN`.
* Detect that a new catalog cache entry became stale while detoasting its fields (Tom Lane) [§](https://postgr.es/c/2a46a0df4) [§](https://postgr.es/c/d41358f4b)

  We expand any out-of-line fields in a catalog tuple before inserting it into the catalog caches. That involves database access which might cause invalidation of catalog cache entries — but the new entry isn't in the cache yet, so we would miss noticing that it should get invalidated. The result is a race condition in which an already-stale cache entry could get made, and then persist indefinitely. This would lead to hard-to-predict misbehavior. Fix by rechecking the tuple's visibility after detoasting.
* Fix edge-case integer overflow detection bug on some platforms (Dean Rasheed) [§](https://postgr.es/c/308a69a98)

  Computing `0 - INT64_MIN` should result in an overflow error, and did on most platforms. However, platforms with neither integer overflow builtins nor 128-bit integers would fail to spot the overflow, instead returning `INT64_MIN`.
* Detect Julian-date overflow when adding or subtracting an `interval` to/from a `timestamp` (Tom Lane) [§](https://postgr.es/c/86b6243a8)

  Some cases that should cause an out-of-range error produced an incorrect result instead.
* Add more checks for overflow in `interval_mul()` and `interval_div()` (Dean Rasheed) [§](https://postgr.es/c/2851aa7d1)

  Some cases that should cause an out-of-range error produced an incorrect result instead.
* Ensure cached statistics are discarded after a change to `stats_fetch_consistency` (Shinya Kato) [§](https://postgr.es/c/171d21f50)

  In some code paths, it was possible for stale statistics to be returned.
* Make the `pg_file_settings` view check validity of unapplied values for settings with `backend` or `superuser-backend` context (Tom Lane) [§](https://postgr.es/c/76dd3d94a)

  Invalid values were not noted in the view as intended. This escaped detection because there are very few settings in these groups.
* Match collation too when matching an existing index to a new partitioned index (Peter Eisentraut) [§](https://postgr.es/c/15d485921)

  Previously we could accept an index that has a different collation from the corresponding element of the partition key, possibly leading to misbehavior.
* Avoid failure if a child index is dropped concurrently with `REINDEX INDEX` on a partitioned index (Fei Changhong) [§](https://postgr.es/c/a0c19de11) [§](https://postgr.es/c/1cf2dba84)
* Fix insufficient locking when cleaning up an incomplete split of a GIN index's internal page (Fei Changhong, Heikki Linnakangas) [§](https://postgr.es/c/e43425f48)

  The code tried to do this with shared rather than exclusive lock on the buffer. This could lead to index corruption if two processes attempted the cleanup concurrently.
* Avoid premature release of buffer pin in GIN index insertion (Tom Lane) [§](https://postgr.es/c/4c73ec604)

  If an index root page split occurs concurrently with our own insertion, the code could fail with “buffer NNNN is not owned by resource owner”.
* Avoid failure with partitioned SP-GiST indexes (Tom Lane) [§](https://postgr.es/c/ab04c1901)

  Trying to use an index of this kind could lead to “No such file or directory” errors.
* Fix ownership change reporting for large objects (Tom Lane) [§](https://postgr.es/c/7a99fb6e1)

  A no-op `ALTER LARGE OBJECT OWNER` command (that is, one selecting the existing owner) passed the wrong class ID to the `PostAlterHook`, probably confusing any extension using that hook.
* Fix reporting of I/O timing data in `EXPLAIN (BUFFERS)` (Michael Paquier) [§](https://postgr.es/c/8dd70828b)

  The numbers labeled as “shared/local” actually refer only to shared buffers, so change that label to “shared”.
* Ensure durability of `CREATE DATABASE` (Noah Misch) [§](https://postgr.es/c/d493bed28) [§](https://postgr.es/c/8fa4a1ac6)

  If an operating system crash occurred during or shortly after `CREATE DATABASE`, recovery could fail, or subsequent connections to the new database could fail. If a base backup was taken in that window, similar problems could be observed when trying to use the backup. The symptom would be that the database directory, `PG_VERSION` file, or `pg_filenode.map` file was missing or empty.
* Add more `LOG` messages when starting and ending recovery from a backup (Andres Freund) [§](https://postgr.es/c/8b34cff33)

  This change provides additional information in the postmaster log that may be useful for diagnosing recovery problems.
* Prevent standby servers from incorrectly processing dead index tuples during subtransactions (Fei Changhong) [§](https://postgr.es/c/f5d8f59ca)

  The `startedInRecovery` flag was not correctly set for a subtransaction. This affects only processing of dead index tuples. It could allow a query in a subtransaction to ignore index entries that it should return (if they are already dead on the primary server, but not dead to the standby transaction), or to prematurely mark index entries as dead that are not yet dead on the primary. It is not clear that the latter case has any serious consequences, but it's not the intended behavior.
* Fix integer overflow hazard in checking whether a record will fit into the WAL decoding buffer (Thomas Munro) [§](https://postgr.es/c/b9f687f5a)

  This bug appears to be only latent except when running a 32-bit PostgreSQL build on a 64-bit platform.
* Fix deadlock between a logical replication apply worker, its tablesync worker, and a session process trying to alter the subscription (Shlok Kyal) [§](https://postgr.es/c/332b43063)

  One edge of the deadlock loop did not involve a lock wait, so the deadlock went undetected and would persist until manual intervention.
* Ensure that column default values are correctly transmitted by the pgoutput logical replication plugin (Nikhil Benesch) [§](https://postgr.es/c/a77fb8c68)

  `ALTER TABLE ADD COLUMN` with a constant default value for the new column avoids rewriting existing tuples, instead expecting that reading code will insert the correct default into a tuple that lacks that column. If replication was subsequently initiated on the table, pgoutput would transmit NULL instead of the correct default for such a column, causing incorrect replication on the subscriber.
* Fix failure of logical replication's initial sync for a table with no columns (Vignesh C) [§](https://postgr.es/c/57aae65ae)

  This case generated an improperly-formatted `COPY` command.
* Prevent examining system catalogs with the wrong snapshot during logical decoding (Fei Changhong) [§](https://postgr.es/c/b793a416b)

  If decoding begins partway through a transaction that modifies system catalogs, the decoder may not recognize that, causing it to fail to treat that transaction as in-progress for catalog lookups. This fix deals with the case that a top-level transaction is already marked as containing catalog changes, but its subtransaction(s) are not.
* Return the correct status code when a new client disconnects without responding to the server's password challenge (Liu Lang, Tom Lane) [§](https://postgr.es/c/a0d016393)

  In some cases we'd treat this as a loggable error, which was not the intention and tends to create log spam, since common clients like psql frequently do this. It may also confuse extensions that use `ClientAuthentication_hook`.
* Fix incompatibility with OpenSSL 3.2 (Tristan Partin, Bo Andreson) [§](https://postgr.es/c/5dd30bb54)

  Use the BIO “app_data” field for our private storage, instead of assuming it's okay to use the “data” field. This mistake didn't cause problems before, but with 3.2 it leads to crashes and complaints about double frees.
* Be more wary about OpenSSL not setting `errno` on error (Tom Lane) [§](https://postgr.es/c/551d4b28e)

  If `errno` isn't set, assume the cause of the reported failure is read EOF. This fixes rare cases of strange error reports like “could not accept SSL connection: Success”.
* Fix file descriptor leakage when a foreign data wrapper's `ForeignAsyncRequest` function fails (Heikki Linnakangas) [§](https://postgr.es/c/481d7d1c0)
* Report ENOMEM errors from file-related system calls as `ERRCODE_OUT_OF_MEMORY`, not `ERRCODE_INTERNAL_ERROR` (Alexander Kuzmenkov) [§](https://postgr.es/c/3766b8b64)
* In PL/pgSQL, support SQL commands that are `CREATE FUNCTION`/`CREATE PROCEDURE` with SQL-standard bodies (Tom Lane) [§](https://postgr.es/c/de2d393a8)

  Previously, such cases failed with parsing errors due to the semicolon(s) appearing in the function body.
* Fix libpq's handling of errors in pipelines (Álvaro Herrera) [§](https://postgr.es/c/1171c6e74) [§](https://postgr.es/c/2b656cbd2)

  The pipeline state could get out of sync if an error is returned for reasons other than a query problem (for example, if the connection is lost). Potentially this would lead to a busy-loop in the calling application.
* Make libpq's `PQsendFlushRequest()` function flush the client output buffer under the same rules as other `PQsend` functions (Jelte Fennema-Nio) [§](https://postgr.es/c/0e28091d5)

  In pipeline mode, it may still be necessary to call `PQflush()` as well; but this change removes some inconsistency.
* Avoid race condition when libpq initializes OpenSSL support concurrently in two different threads (Willi Mann, Michael Paquier) [§](https://postgr.es/c/b97226815)
* Fix timing-dependent failure in GSSAPI data transmission (Tom Lane) [§](https://postgr.es/c/a50053777)

  When using GSSAPI encryption in non-blocking mode, libpq sometimes failed with “GSSAPI caller failed to retransmit all data needing to be retried”.
* In pg_dump, don't dump RLS policies or security labels for extension member objects (Tom Lane, Jacob Champion) [§](https://postgr.es/c/f15147df6) [§](https://postgr.es/c/63c1b4d88)

  Previously, commands would be included in the dump to set these properties, which is really incorrect since they should be considered as internal affairs of the extension. Moreover, the restoring user might not have adequate privilege to set them, and indeed the dumping user might not have enough privilege to dump them (since dumping RLS policies requires acquiring lock on their table).
* In pg_dump, don't dump an extended statistics object if its underlying table isn't being dumped (Rian McGuire, Tom Lane) [§](https://postgr.es/c/1e0841426)

  This conforms to the behavior for other dependent objects such as indexes.
* Make it an error for a pgbench script to end with an open pipeline (Anthonin Bonnefoy) [§](https://postgr.es/c/3fd36be52)

  Previously, pgbench would behave oddly if a `\startpipeline` command lacked a matching `\endpipeline`. This seems like a scripting mistake rather than a case that pgbench needs to handle nicely, so throw an error.
* Fix crash in `contrib/intarray` if an array with an element equal to `INT_MAX` is inserted into a `gist__int_ops` index (Alexander Lakhin, Tom Lane) [§](https://postgr.es/c/940ab02b5)
* Report a better error when `contrib/pageinspect`'s `hash_bitmap_info()` function is applied to a partitioned hash index (Alexander Lakhin, Michael Paquier) [§](https://postgr.es/c/2e08440d6)
* Report a better error when `contrib/pgstattuple`'s `pgstathashindex()` function is applied to a partitioned hash index (Alexander Lakhin) [§](https://postgr.es/c/b745f1680)
* On Windows, suppress autorun options when launching subprocesses in pg_ctl and pg_regress (Kyotaro Horiguchi) [§](https://postgr.es/c/33d1be06a) [§](https://postgr.es/c/7e7d827f5)

  When launching a child process via `cmd.exe`, pass the `/D` flag to prevent executing any autorun commands specified in the registry. This avoids possibly-surprising side effects.
* Move `is_valid_ascii()` from `mb/pg_wchar.h` to `utils/ascii.h` (Jubilee Young) [§](https://postgr.es/c/3726c1cb0)

  This change avoids the need to include `<simd.h>` in `pg_wchar.h`, which was causing problems for some third-party code.
* Fix compilation failures with libxml2 version 2.12.0 and later (Tom Lane) [§](https://postgr.es/c/3f8ac13b1)
* Fix compilation failure of `WAL_DEBUG` code on Windows (Bharath Rupireddy) [§](https://postgr.es/c/87ed81a87)
* Suppress compiler warnings from Python's header files (Peter Eisentraut, Tom Lane) [§](https://postgr.es/c/5f8d6d709)

  Our preferred compiler options provoke warnings about constructs appearing in recent versions of Python's header files. When using gcc, we can suppress these warnings with a pragma.
* Avoid deprecation warning when compiling with LLVM 18 (Thomas Munro) [§](https://postgr.es/c/67f7aaa38)
* Update time zone data files to tzdata release 2024a for DST law changes in Greenland, Kazakhstan, and Palestine, plus corrections for the Antarctic stations Casey and Vostok. Also historical corrections for Vietnam, Toronto, and Miquelon. (Tom Lane) [§](https://postgr.es/c/970b1aeeb)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-6.html)（英文原文，待翻譯）
