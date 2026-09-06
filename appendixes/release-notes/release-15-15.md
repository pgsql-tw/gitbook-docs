<a id="RELEASE-15-15"></a>

# E.5. Release 15.15

[E.5.1. Migration to Version 15.15](#id-1.11.6.10.4)

[E.5.2. Changes](#id-1.11.6.10.5)

<strong>Release date: </strong>2025-11-13

This release contains a variety of fixes from 15.14. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.10.4"></a>

## E.5.1. Migration to Version 15.15

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.14, see [Section E.6](release-15-14.md).

<a id="id-1.11.6.10.5"></a>

## E.5.2. Changes

* Check for `CREATE` privileges on the schema in `CREATE STATISTICS` (Jelte Fennema-Nio) [§](https://postgr.es/c/2393d374a)

  This omission allowed table owners to create statistics in any schema, potentially leading to unexpected naming conflicts.

  The PostgreSQL Project thanks Jelte Fennema-Nio for reporting this problem. (CVE-2025-12817)
* Avoid integer overflow in allocation-size calculations within libpq (Jacob Champion) [§](https://postgr.es/c/91421565f)

  Several places in libpq were not sufficiently careful about computing the required size of a memory allocation. Sufficiently large inputs could cause integer overflow, resulting in an undersized buffer, which would then lead to writing past the end of the buffer.

  The PostgreSQL Project thanks Aleksey Solovev of Positive Technologies for reporting this problem. (CVE-2025-12818)
* Further fix processing of character classes within `SIMILAR TO` regular expressions (Laurenz Albe) [§](https://postgr.es/c/9fd531534)

  The previous fix for translating `SIMILAR TO` pattern matching expressions to POSIX-style regular expressions broke a corner case that formerly worked: if there is an escape character right after the opening bracket and then a closing bracket right after the escape sequence (for example `[\w]`), the closing bracket was no longer seen as terminating the character class.
* Fix parsing of aggregate functions whose arguments contain a sub-select with a `FROM` reference to a CTE outside the aggregate function (Tom Lane) [§](https://postgr.es/c/afd18f276)

  Such a CTE reference must act like a outer-level column reference when determining the aggregate's semantic level; but it was not being accounted for, leading to obscure planner or executor errors.
* Fix “no relation entry for relid” errors in corner cases while estimating SubPlan costs (Richard Guo) [§](https://postgr.es/c/53e35fb56)
* Avoid unlikely use-after-free in planner's expansion of partitioned tables (Bernd Reiß) [§](https://postgr.es/c/8286bce0a)

  There was a hazard only when the last live partition was concurrently dropped.
* Remove faulty assertion in btree index cleanup (Peter Geoghegan) [§](https://postgr.es/c/ca0c93908)
* Fix possible infinite loop in GIN index scans with multiple scan conditions (Tom Lane) [§](https://postgr.es/c/34249b3b5)

  GIN can handle scan conditions that can reject non-matching entries but are not useful for searching for relevant entries, for example a `tsquery` clause like `!term`. But such a condition must not be first in the array of scan conditions. The code failed to ensure that in all cases, with the result that a query having a mix of such conditions with normal conditions might work or not depending on the order in which the conditions were given in the query.
* Ensure that GIN index scans can be canceled (Tom Lane) [§](https://postgr.es/c/a9c1b9c1c)

  Some code paths were capable of running for a long time without checking for interrupts.
* Ensure that BRIN autosummarization provides a snapshot for index expressions that need one (Álvaro Herrera) [§](https://postgr.es/c/23ddadf68) [§](https://postgr.es/c/bcfbd3f74)

  Previously, autosummarization would fail for such indexes, and then leave placeholder index tuples behind, causing the index to bloat over time.
* Fix integer-overflow hazard in BRIN index scans when the table contains close to 2<sup>32</sup> pages (Sunil S) [§](https://postgr.es/c/810aaf7f2)

  This oversight could result in an infinite loop or scanning of unneeded table pages.
* Fix incorrect zero-extension of stored values in JIT-generated tuple deforming code (David Rowley) [§](https://postgr.es/c/b8ecfbe5a)

  When not using JIT, the equivalent code does sign-extension not zero-extension, leading to a different Datum representation of small integer data types. This inconsistency was masked in most cases, but it is known to lead to “could not find memoization table entry” errors when using Memoize plan nodes, and there might be other symptoms.
* Fix incorrect logic for caching result-relation information for triggers (David Rowley, Amit Langote) [§](https://postgr.es/c/2992b9a07)

  In cases where partitions' column sets aren't physically identical to their parent partitioned tables' column sets, this oversight could lead to crashes.
* Add missing EvalPlanQual rechecks for TID Scan and TID Range Scan plan nodes (Sophie Alpert, David Rowley) [§](https://postgr.es/c/f00ad440a) [§](https://postgr.es/c/005770203)

  This omission led to possibly not rechecking a condition on `ctid` during concurrent-update situations, causing the update's behavior to vary depending on which plan type had been selected.
* Fix EvalPlanQual handling of foreign or custom joins that do not have an alternative local-join plan prepared for EPQ (Masahiko Sawada, Etsuro Fujita) [§](https://postgr.es/c/4a08603a2)

  In such cases the foreign or custom access method should be invoked normally, but that did not happen, typically leading to a crash.
* Avoid duplicating hash partition constraints during `DETACH CONCURRENTLY` (Haiyang Li) [§](https://postgr.es/c/bdae98495)

  `ALTER TABLE DETACH PARTITION CONCURRENTLY` was written to add a copy of the partitioning constraint to the now-detached partition. This was misguided, partially because non-concurrent `DETACH` doesn't do that, but mostly because in the case of hash partitioning the constraint expression contains references to the parent table's OID. That causes problems during dump/restore, or if the parent table is dropped after `DETACH`. In v19 and later, we'll no longer create any such copied constraints at all. In released branches, to minimize the risk of unforeseen consequences, only skip adding a copied constraint if it is for hash partitioning.
* Disallow generated columns in partition keys (Jian He, Ashutosh Bapat) [§](https://postgr.es/c/643a5e96c)

  This was already not allowed, but the check missed some cases, such as where the column reference is implicit in a whole-row reference.
* Disallow generated columns in `COPY ... FROM ... WHERE` clauses (Peter Eisentraut, Jian He) [§](https://postgr.es/c/8278737bf)

  Previously, incorrect behavior or an obscure error message resulted from attempting to reference such a column, since generated columns have not yet been computed at the point where `WHERE` filtering is done.
* Fix visibility checking for statistics objects in `pg_temp` (Noah Misch) [§](https://postgr.es/c/d202ec1fb)

  A statistics object located in a temporary schema cannot be named without schema qualification, but `pg_statistics_obj_is_visible()` missed that memo and could return “true” regardless. In turn, functions such as `pg_describe_object()` could fail to schema-qualify the object's name as expected.
* Fix `pg_event_trigger_dropped_objects()`'s reporting of temporary status (Antoine Violin, Tom Lane) [§](https://postgr.es/c/451373dc5) [§](https://postgr.es/c/33e49ee01)

  If a dropped column default, trigger, or RLS policy belongs to a temporary table, report it with `is_temporary` true.
* Fix memory leakage in hashed subplans (Haiyang Li) [§](https://postgr.es/c/5ac973892)

  Any memory consumed by the hash functions used for hashing tuples constituted a query-lifespan memory leak. One way that could happen is if the values being hashed require de-toasting.
* Fix minor memory leak during WAL replay of database creation (Nathan Bossart) [§](https://postgr.es/c/23b316c36)
* Fix corruption of the shared statistics table after out-of-memory failures (Mikhail Kot) [§](https://postgr.es/c/1852ec5db)

  Previously, an out-of-memory failure partway through creating a new hash table entry left a broken entry behind, potentially causing errors in other sessions later.
* Fix concurrent update issue in `MERGE` (Yugo Nagata) [§](https://postgr.es/c/f871fbae9)

  When executing a `MERGE UPDATE` action, if there is more than one concurrent update of the target row, the lock-and-retry code would sometimes incorrectly identify the latest version of the target tuple, leading to incorrect results.
* Add missing replica identity checks in `MERGE` and `INSERT ... ON CONFLICT DO UPDATE` (Zhijie Hou) [§](https://postgr.es/c/5481cc332) [§](https://postgr.es/c/451b22efd) [§](https://postgr.es/c/a4624929d)

  If `MERGE` may require update or delete actions, and the target table publishes updates or deletes, insist that it have a `REPLICA IDENTITY` defined. Failing to require this can silently break replication. Likewise, `INSERT` with an `UPDATE` option must require `REPLICA IDENTITY` if the target table publishes either inserts or updates.
* Avoid deadlock during `DROP SUBSCRIPTION` when publisher is on the same server as subscriber (Dilip Kumar) [§](https://postgr.es/c/e41137155)
* Fix incorrect reporting of replication lag in `pg_stat_replication` view (Fujii Masao) [§](https://postgr.es/c/59b215f72)

  If any standby server's replay LSN stopped advancing, the `write_lag` and `flush_lag` columns would eventually stop updating.
* Avoid duplicative log messages about invalid `primary_slot_name` settings (Fujii Masao) [§](https://postgr.es/c/caf529aba)
* Remove the unfinished slot state file after failing to write a replication slot's state to disk (Michael Paquier) [§](https://postgr.es/c/0adf424b4)

  Previously, a failure such as out-of-disk-space resulted in leaving a temporary `state.tmp` file behind. That's problematic because it would block all subsequent attempts to write the state, requiring manual intervention to clean up.
* Avoid unwanted WAL receiver shutdown when switching from streaming to archive WAL source (Xuneng Zhou) [§](https://postgr.es/c/da5ea6c70)

  During a timeline change, a standby server's WAL receiver should remain alive, waiting for a new WAL streaming start point. Instead it was repeatedly shutting down and immediately getting restarted, which could confuse status monitoring code.
* Avoid failures in logical replication due to chance collisions of file numbers between regular and temporary tables (Vignesh C) [§](https://postgr.es/c/ec471008c)

  This low-probability problem manifested as transient errors like “unexpected duplicate for tablespace <em class="replaceable"><code>X</code></em>, relfilenode <em class="replaceable"><code>Y</code></em>”. `contrib/autoprewarm` was also affected. A side-effect of the fix is that the SQL function `pg_filenode_relation()` will now ignore temporary tables.
* Fix use-after-free issue in the relation synchronization cache maintained by the pgoutput logical decoding plugin (Vignesh C, Masahiko Sawada) [§](https://postgr.es/c/c40761759)

  An error during logical decoding could result in crashes in subsequent logical decoding attempts in the same session. The case is only reachable when pgoutput is invoked via SQL functions.
* Avoid assertion failure when trying to release a replication slot in single-user mode (Hayato Kuroda) [§](https://postgr.es/c/818be9b73)
* Fix incorrect printing of messages about failures in checking whether the user has Windows administrator privilege (Bryan Green) [§](https://postgr.es/c/f91666c83)

  This code would have crashed or at least printed garbage. No such cases have been reported though, indicating that failure of these system calls is extremely rare.
* Avoid startup failure on macOS and BSD platforms when there is a collision with a pre-existing semaphore set (Tom Lane) [§](https://postgr.es/c/f4c088344)

  If the pre-existing set has fewer semaphores than we asked for, these platforms return EINVAL not EEXIST as our code expected, resulting in failure to start the database.
* Fix false memory-context-checking warnings in debug builds on 64-bit Windows (David Rowley) [§](https://postgr.es/c/f3420e006)
* Correctly handle `GROUP BY DISTINCT` in PL/pgSQL assignment statements (Tom Lane) [§](https://postgr.es/c/9ca79896a)

  The parser failed to record the `DISTINCT` option in this context, so that the command would act as if it were plain `GROUP BY`.
* Avoid leaking memory when handling a SQL error within PL/Python (Tom Lane) [§](https://postgr.es/c/4cde73259)

  This fixes a session-lifespan memory leak introduced in our previous minor releases.
* Fix libpq's trace output of characters with the high bit set (Ran Benita) [§](https://postgr.es/c/0b274c475)

  On platforms where `char` is considered signed, the output included unsightly `\xffffff` decoration.
* Fix libpq's handling of socket-related errors on Windows within its GSSAPI logic (Ning Wu, Tom Lane) [§](https://postgr.es/c/771b106d1)

  The code for encrypting/decrypting transmitted data using GSSAPI did not correctly recognize error conditions on the connection socket, since Windows reports those differently than other platforms. This led to failure to make such connections on Windows.
* In pg_dump, dump security labels on subscriptions and event triggers (Jian He, Fujii Masao) [§](https://postgr.es/c/165b07efe)

  Labels on these types of objects were previously missed.
* Fix pg_dump's sorting of default ACLs and foreign key constraints (Kirill Reshke, Álvaro Herrera) [§](https://postgr.es/c/fbf967e99) [§](https://postgr.es/c/090c9c960) [§](https://postgr.es/c/4cc3b4445)

  Ensure consistent ordering of these database object types, as was already done for other object types.
* In pg_dump, label comments for separately-dumped domain constraints with the proper dependency (Noah Misch) [§](https://postgr.es/c/0773f3a87)

  This error could lead to parallel pg_restore attempting to create the comment before the constraint itself has been restored.
* In pg_restore, skip comments and security labels for publications and subscriptions that are not being restored (Jian He, Fujii Masao) [§](https://postgr.es/c/c8ed16050) [§](https://postgr.es/c/5f42008f9)

  Do not emit `COMMENT` or `SECURITY LABEL` commands for these objects when `--no-publications` or `--no-subscriptions` is specified.
* Fix assorted errors in the data compression logic in pg_dump and pg_restore (Daniel Gustafsson, Tom Lane) [§](https://postgr.es/c/8b9924bce)

  Error checking was missing or incorrect in several places, and there were also portability issues that would manifest on big-endian hardware. These problems had been missed because this code is only used to read compressed TOC files within directory-format dumps. pg_dump never produces such a dump; the case can be reached only by manually compressing the TOC file after the fact, which is a supported thing to do but very uncommon.
* Fix pgbench to error out cleanly if a `COPY` operation is started (Anthonin Bonnefoy) [§](https://postgr.es/c/b5cefc197)

  pgbench doesn't intend to support this case, but previously it went into an infinite loop.
* Fix pgbench's reporting of multiple errors (Yugo Nagata) [§](https://postgr.es/c/bdccb6302)

  In cases where two successive `PQgetResult` calls both fail, pgbench might report the wrong error message.
* In pgbench, fix faulty assertion about errors in pipeline mode (Yugo Nagata) [§](https://postgr.es/c/704f51771)
* Ensure that `contrib/pg_buffercache` functions can be canceled (Satyanarayana Narlapuram, Yuhang Qiu) [§](https://postgr.es/c/eb9ee4d18)

  Some code paths were capable of running for a long time without checking for interrupts.
* Fix `contrib/pg_prewarm`'s privilege checks for indexes (Ayush Vatsa, Nathan Bossart) [§](https://postgr.es/c/6c03ae8d6)

  `pg_prewarm()` requires `SELECT` privilege on relations to be prewarmed. However, since indexes have no SQL privileges of their own, this resulted in non-superusers being unable to prewarm indexes. Instead, check for `SELECT` privilege on the index's table.
* Make `contrib/pgstattuple` more robust about empty or invalid index pages (Nitin Motiani) [§](https://postgr.es/c/49b5f0b53)

  Count all-zero pages as free space, and ignore pages that are invalid according to a check of the page's special-space size. The code for btree indexes already counted all-zero pages as free, but the hash and gist code would error out, which has been found to be much less user-friendly. Similarly, make all three cases agree on ignoring corrupted pages rather than throwing errors.
* Harden our read and write barrier macros to satisfy Clang (Thomas Munro) [§](https://postgr.es/c/1c7cba4c5)

  We supposed that `__atomic_thread_fence()` is a sufficient barrier to prevent the C compiler from re-ordering memory accesses around it, but it appears that that's not true for Clang, allowing it to generate incorrect code for at least RISC-V, MIPS, and LoongArch machines. Add explicit compiler barriers to fix that.
* Fix building with LLVM version 21 and later (Holger Hoffstätte) [§](https://postgr.es/c/72a24bebc)
* Fix PGXS build infrastructure to support building NLS `po` files for extensions (Ryo Matsumura) [§](https://postgr.es/c/33202cba8)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-15.html)（英文原文，待翻譯）
