<a id="RELEASE-15-5"></a>

# E.15. Release 15.5

[E.15.1. Migration to Version 15.5](#id-1.11.6.20.4)

[E.15.2. Changes](#id-1.11.6.20.5)

<strong>Release date: </strong>2023-11-09

This release contains a variety of fixes from 15.4. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.20.4"></a>

## E.15.1. Migration to Version 15.5

A dump/restore is not required for those running 15.X.

However, several mistakes have been discovered that could lead to certain types of indexes yielding wrong search results or being unnecessarily inefficient. It is advisable to `REINDEX` potentially-affected indexes after installing this update. See the fourth through seventh changelog entries below.

Also, if you are upgrading from a version earlier than 15.4, see [Section E.16](release-15-4.md).

<a id="id-1.11.6.20.5"></a>

## E.15.2. Changes

* Fix handling of unknown-type arguments in `DISTINCT` `"any"` aggregate functions (Tom Lane) [§](https://postgr.es/c/4f4a422fb)

  This error led to a `text`-type value being interpreted as an `unknown`-type value (that is, a zero-terminated string) at runtime. This could result in disclosure of server memory following the `text` value.

  The PostgreSQL Project thanks Jingzhou Fu for reporting this problem. (CVE-2023-5868)
* Detect integer overflow while computing new array dimensions (Tom Lane) [§](https://postgr.es/c/3bc6bc3ee)

  When assigning new elements to array subscripts that are outside the current array bounds, an undetected integer overflow could occur in edge cases. Memory stomps that are potentially exploitable for arbitrary code execution are possible, and so is disclosure of server memory.

  The PostgreSQL Project thanks Pedro Gallegos for reporting this problem. (CVE-2023-5869)
* Prevent the `pg_signal_backend` role from signalling background workers and autovacuum processes (Noah Misch, Jelte Fennema-Nio) [§](https://postgr.es/c/595c988c9) [§](https://postgr.es/c/fbc371909)

  The documentation says that `pg_signal_backend` cannot issue signals to superuser-owned processes. It was able to signal these background processes, though, because they advertise a role OID of zero. Treat that as indicating superuser ownership. The security implications of cancelling one of these process types are fairly small so far as the core code goes (we'll just start another one), but extensions might add background workers that are more vulnerable.

  Also ensure that the `is_superuser` parameter is set correctly in such processes. No specific security consequences are known for that oversight, but it might be significant for some extensions.

  The PostgreSQL Project thanks Hemanth Sandrana and Mahendrakar Srinivasarao for reporting this problem. (CVE-2023-5870)
* Fix misbehavior during recursive page split in GiST index build (Heikki Linnakangas) [§](https://postgr.es/c/c3c284b37)

  Fix a case where the location of a page downlink was incorrectly tracked, and introduce some logic to allow recovering from such situations rather than silently doing the wrong thing. This error could result in incorrect answers from subsequent index searches. It may be advisable to reindex all GiST indexes after installing this update.
* Prevent de-duplication of btree index entries for `interval` columns (Noah Misch) [§](https://postgr.es/c/782be0f71)

  There are `interval` values that are distinguishable but compare equal, for example `24:00:00` and `1 day`. This breaks assumptions made by btree de-duplication, so `interval` columns need to be excluded from de-duplication. This oversight can cause incorrect results from index-only scans. Moreover, after updating amcheck will report an error for almost all such indexes. Users should reindex any btree indexes on `interval` columns.
* Process `date` values more sanely in BRIN `datetime_minmax_multi_ops` indexes (Tomas Vondra) [§](https://postgr.es/c/088233f8d)

  The distance calculation for dates was backward, causing poor decisions about which entries to merge. The index still produces correct results, but is much less efficient than it should be. Reindexing BRIN `minmax_multi` indexes on `date` columns is advisable.
* Process large `timestamp` and `timestamptz` values more sanely in BRIN `datetime_minmax_multi_ops` indexes (Tomas Vondra) [§](https://postgr.es/c/d04a9283b) [§](https://postgr.es/c/daa7b0d7c)

  Infinities were mistakenly treated as having distance zero rather than a large distance from other values, causing poor decisions about which entries to merge. Also, finite-but-very-large values (near the endpoints of the representable timestamp range) could result in internal overflows, again causing poor decisions. The index still produces correct results, but is much less efficient than it should be. Reindexing BRIN `minmax_multi` indexes on `timestamp` and `timestamptz` columns is advisable if the column contains, or has contained, infinities or large finite values.
* Avoid calculation overflows in BRIN `interval_minmax_multi_ops` indexes with extreme interval values (Tomas Vondra) [§](https://postgr.es/c/2fbb2fcb0)

  This bug might have caused unexpected failures while trying to insert large interval values into such an index.
* Fix partition step generation and runtime partition pruning for hash-partitioned tables with multiple partition keys (David Rowley) [§](https://postgr.es/c/1e81d3e6e) [§](https://postgr.es/c/916adc7c5)

  Some cases involving an `IS NULL` condition on one of the partition keys could result in a crash.
* Fix inconsistent rechecking of concurrently-updated rows during `MERGE` (Dean Rasheed) [§](https://postgr.es/c/3c1a1af91)

  In `READ COMMITTED` mode, an update that finds that its target row was just updated by a concurrent transaction will recheck the query's `WHERE` conditions on the updated row. `MERGE` failed to ensure that the proper rows of other joined tables were used during this recheck, possibly resulting in incorrect decisions about whether the newly-updated row should be updated again by `MERGE`.
* Correctly identify the target table in an inherited `UPDATE`/`DELETE`/`MERGE` even when the parent table is excluded by constraints (Amit Langote, Tom Lane) [§](https://postgr.es/c/1268e7378)

  If the initially-named table is excluded by constraints, but not all its inheritance descendants are, the first non-excluded descendant was identified as the primary target table. This would lead to firing statement-level triggers associated with that table, rather than the initially-named table as should happen. In v16, the same oversight could also lead to “invalid perminfoindex 0 in RTE with relid NNNN” errors.
* Fix edge case in btree mark/restore processing of ScalarArrayOpExpr clauses (Peter Geoghegan) [§](https://postgr.es/c/cac37c1a1)

  When restoring an indexscan to a previously marked position, the code could miss required setup steps if the scan had advanced exactly to the end of the matches for a ScalarArrayOpExpr (that is, an `indexcol = ANY(ARRAY[])`) clause. This could result in missing some rows that should have been fetched.
* Fix intra-query memory leak in Memoize execution (Orlov Aleksej, David Rowley) [§](https://postgr.es/c/689af6db6)
* Fix intra-query memory leak when a set-returning function repeatedly returns zero rows (Tom Lane) [§](https://postgr.es/c/592cb11fb)
* Don't crash if `cursor_to_xmlschema()` is applied to a non-data-returning Portal (Boyu Yang) [§](https://postgr.es/c/95f54f0d0)
* Throw the intended error if `pgrowlocks()` is applied to a partitioned table (David Rowley) [§](https://postgr.es/c/136068353)

  Previously, a not-on-point complaint “only heap AM is supported” would be raised.
* Handle invalid indexes more cleanly in assorted SQL functions (Noah Misch) [§](https://postgr.es/c/e633e9b13)

  Report an error if `pgstatindex()`, `pgstatginindex()`, `pgstathashindex()`, or `pgstattuple()` is applied to an invalid index. If `brin_desummarize_range()`, `brin_summarize_new_values()`, `brin_summarize_range()`, or `gin_clean_pending_list()` is applied to an invalid index, do nothing except to report a debug-level message. Formerly these functions attempted to process the index, and might fail in strange ways depending on what the failed `CREATE INDEX` had left behind.
* Fix `pg_stat_reset_single_table_counters()` to do the right thing for a shared catalog (Masahiro Ikeda) [§](https://postgr.es/c/ad8753a3a)

  Previously the reset would be ineffective.
* Avoid premature memory allocation failure with long inputs to `to_tsvector()` (Tom Lane) [§](https://postgr.es/c/71bb73f60)
* Fix over-allocation of the constructed `tsvector` in `tsvectorrecv()` (Denis Erokhin) [§](https://postgr.es/c/55e188a15)

  If the incoming vector includes position data, the binary receive function left wasted space (roughly equal to the size of the position data) in the finished `tsvector`. In extreme cases this could lead to “maximum total lexeme length exceeded” failures for vectors that were under the length limit when emitted. In any case it could lead to wasted space on-disk.
* Fix incorrect coding in `gtsvector_picksplit()` (Alexander Lakhin) [§](https://postgr.es/c/88aa4a049)

  This could lead to poor page-split decisions in GiST indexes on `tsvector` columns.
* Improve checks for corrupt PGLZ compressed data (Flavien Guedez) [§](https://postgr.es/c/985ac5ce2)
* In `COPY FROM`, fail cleanly when an unsupported encoding conversion is needed (Tom Lane) [§](https://postgr.es/c/95fd5c89f)

  Recent refactoring accidentally removed the intended error check for this, such that it ended in “cache lookup failed for function 0” instead of a useful error message.
* Avoid crash in `EXPLAIN` if a parameter marked to be displayed by `EXPLAIN` has a NULL boot-time value (Xing Guo, Aleksander Alekseev, Tom Lane) [§](https://postgr.es/c/ae33659d4)

  No built-in parameter fits this description, but an extension could define such a parameter.
* Ensure we have a snapshot while dropping `ON COMMIT DROP` temp tables (Tom Lane) [§](https://postgr.es/c/0d1a7cd14)

  This prevents possible misbehavior if any catalog entries for the temp tables have fields wide enough to require toasting (such as a very complex `CHECK` condition).
* Avoid improper response to shutdown signals in child processes just forked by `system()` (Nathan Bossart) [§](https://postgr.es/c/c9265ae80)

  This fix avoids a race condition in which a child process that has been forked off by `system()`, but hasn't yet exec'd the intended child program, might receive and act on a signal intended for the parent server process. That would lead to duplicate cleanup actions being performed, which will not end well.
* Cope with torn reads of `pg_control` in frontend programs (Thomas Munro) [§](https://postgr.es/c/5e39884d3)

  On some file systems, reading `pg_control` may not be an atomic action when the server concurrently writes that file. This is detectable via a bad CRC. Retry a few times to see if the file becomes valid before we report error.
* Avoid torn reads of `pg_control` in relevant SQL functions (Thomas Munro) [§](https://postgr.es/c/606be8a35)

  Acquire the appropriate lock before reading `pg_control`, to ensure we get a consistent view of that file.
* Avoid integer overflow when computing size of backend activity string array (Jakub Wartak) [§](https://postgr.es/c/95e91da66)

  On 64-bit machines we will allow values of `track_activity_query_size` large enough to cause 32-bit overflow when multiplied by the allowed number of connections. The code actually allocating the per-backend local array was careless about this though, and allocated the array incorrectly.
* Fix briefly showing inconsistent progress statistics for `ANALYZE` on inherited tables (Heikki Linnakangas) [§](https://postgr.es/c/5ae245664)

  The block-level counters should be reset to zero at the same time we update the current-relation field.
* Fix the background writer to report any WAL writes it makes to the statistics counters (Nazir Bilal Yavuz) [§](https://postgr.es/c/0684d1949)
* Fix confusion about forced-flush behavior in `pgstat_report_wal()` (Ryoga Yoshida, Michael Paquier) [§](https://postgr.es/c/802fcb9ed)

  This could result in some statistics about WAL I/O being forgotten in a shutdown.
* Track the dependencies of cached `CALL` statements, and re-plan them when needed (Tom Lane) [§](https://postgr.es/c/0e59266a5)

  DDL commands, such as replacement of a function that has been inlined into a `CALL` argument, can create the need to re-plan a `CALL` that has been cached by PL/pgSQL. That was not happening, leading to misbehavior or strange errors such as “cache lookup failed”.
* Avoid a possible pfree-a-NULL-pointer crash after an error in OpenSSL connection setup (Sergey Shinderuk) [§](https://postgr.es/c/9dc85806d)
* Track nesting depth correctly when inspecting `RECORD`-type Vars from outer query levels (Richard Guo) [§](https://postgr.es/c/2679a107a)

  This oversight could lead to assertion failures, core dumps, or “bogus varno” errors.
* Track hash function and negator function dependencies of ScalarArrayOpExpr plan nodes (David Rowley) [§](https://postgr.es/c/17a3f1c34)

  In most cases this oversight was harmless, since these functions would be unlikely to disappear while the node's original operator remains present.
* Fix error-handling bug in `RECORD` type cache management (Thomas Munro) [§](https://postgr.es/c/a26cc0334)

  An out-of-memory error occurring at just the wrong point could leave behind inconsistent state that would lead to an infinite loop.
* Fix assertion failure when logical decoding is retried in the same session after an error (Hou Zhijie) [§](https://postgr.es/c/c7256e656)
* Treat out-of-memory failures as fatal while reading WAL (Michael Paquier) [§](https://postgr.es/c/afc79591d)

  Previously this would be treated as a bogus-data condition, leading to the conclusion that we'd reached the end of WAL, which is incorrect and could lead to inconsistent WAL replay.
* Fix possible recovery failure due to trying to allocate memory based on a bogus WAL record length field (Thomas Munro, Michael Paquier) [§](https://postgr.es/c/f4d152edd) [§](https://postgr.es/c/99d334a18)
* Fix race condition in database dropping that could lead to the autovacuum launcher getting stuck (Andres Freund, Will Mortensen, Jacob Speidel) [§](https://postgr.es/c/5a9325fdd)

  The race could lead to a statistics entry for the removed database remaining present, confusing the launcher's selection of which database to process.
* Fix datatype size confusion in logical tape management (Ranier Vilela) [§](https://postgr.es/c/5180160c1)

  Integer overflow was possible on platforms where long is wider than int, although it would take a multiple-terabyte temporary file to cause a problem.
* Avoid unintended close of syslogger process's stdin (Heikki Linnakangas) [§](https://postgr.es/c/0c1024060)
* Avoid doing plan cache revalidation of utility statements that do not receive interesting processing during parse analysis (Tom Lane) [§](https://postgr.es/c/870085135)

  Aside from saving a few cycles, this prevents failure after a cache invalidation for statements that must not set a snapshot, such as `SET TRANSACTION ISOLATION LEVEL`.
* Keep by-reference `attmissingval` values in a long-lived context while they are being used (Andrew Dunstan) [§](https://postgr.es/c/75f323aa1)

  This avoids possible use of dangling pointers when a tuple slot outlives the tuple descriptor with which its value was constructed.
* Recalculate the effective value of `search_path` after `ALTER ROLE` (Jeff Davis) [§](https://postgr.es/c/9f3343e40) [§](https://postgr.es/c/1bc19dfcf)

  This ensures that after renaming a role, the meaning of the special string `$user` is re-determined.
* Fix “could not duplicate handle” error occurring on Windows when `min_dynamic_shared_memory` is set above zero (Thomas Munro) [§](https://postgr.es/c/f72790b29)
* Fix order of operations in `GenericXLogFinish` (Jeff Davis) [§](https://postgr.es/c/b9bb02620)

  This code violated the conditions required for crash safety by writing WAL before marking changed buffers dirty. No core code uses this function, but extensions do (`contrib/bloom` does, for example).
* Remove incorrect assertion in PL/Python exception handling (Alexander Lakhin) [§](https://postgr.es/c/9e0ce80f3)
* Fix assertion failure in pg_dump when it's asked to dump the `pg_catalog` schema (Peter Eisentraut) [§](https://postgr.es/c/1d9976d1b) [§](https://postgr.es/c/3a788447d)
* Fix pg_restore so that selective restores will include both table-level and column-level ACLs for selected tables (Euler Taveira, Tom Lane) [§](https://postgr.es/c/10e705bd2)

  Formerly, only the table-level ACL would get restored if both types were present.
* Add logic to pg_upgrade to check for use of `abstime`, `reltime`, and `tinterval` data types (Álvaro Herrera) [§](https://postgr.es/c/8845d8597) [§](https://postgr.es/c/04d2d605f)

  These obsolete data types were removed in PostgreSQL version 12, so check to make sure they aren't present in an older database before claiming it can be upgraded.
* Avoid generating invalid temporary slot names in pg_basebackup (Jelte Fennema) [§](https://postgr.es/c/574bff7bd)

  This has only been seen to occur when the server connection runs through pgbouncer.
* Avoid false “too many client connections” errors in pgbench on Windows (Noah Misch) [§](https://postgr.es/c/1102f4ece)
* In `contrib/amcheck`, do not report interrupted page deletion as corruption (Noah Misch) [§](https://postgr.es/c/6f81386a9)

  This fix prevents false-positive reports of “the first child of leftmost target page is not leftmost of its level”, “block NNNN is not leftmost” or “left link/right link pair in index XXXX not in agreement”. They appeared if amcheck ran after an unfinished btree index page deletion and before `VACUUM` had cleaned things up.
* Fix failure of `contrib/btree_gin` indexes on `interval` columns, when an indexscan using the `<` or `<=` operator is performed (Dean Rasheed) [§](https://postgr.es/c/5f0691839)

  Such an indexscan failed to return all the entries it should.
* Add support for LLVM 16 and 17 (Thomas Munro, Dmitry Dolgov) [§](https://postgr.es/c/b60e3ac76) [§](https://postgr.es/c/eed1feb3f) [§](https://postgr.es/c/b2e097788)
* Suppress assorted build-time warnings on recent macOS (Tom Lane) [§](https://postgr.es/c/be3398ea1) [§](https://postgr.es/c/78f17fb97)

  Xcode 15 (released with macOS Sonoma) changed the linker's behavior in a way that causes many duplicate-library warnings while building PostgreSQL. These were harmless, but they're annoying so avoid citing the same libraries twice. Also remove use of the `-multiply_defined suppress` linker switch, which apparently has been a no-op for a long time, and is now actively complained of.
* When building `contrib/unaccent`'s rules file, fall back to using `python` if `--with-python` was not given and make variable `PYTHON` was not set (Japin Li) [§](https://postgr.es/c/8a9e4e84e)
* Remove `PHOT` (Phoenix Islands Time) from the default timezone abbreviations list (Tom Lane) [§](https://postgr.es/c/85b98a70b)

  Presence of this abbreviation in the default list can cause failures on recent Debian and Ubuntu releases, as they no longer install the underlying tzdb entry by default. Since this is a made-up abbreviation for a zone with a total human population of about two dozen, it seems unlikely that anyone will miss it. If someone does, they can put it back via a custom abbreviations file.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-5.html)（英文原文，待翻譯）
