## E.5. Release 18.1 [#](#RELEASE-18-1)

[E.5.1. Migration to Version 18.1](release-18-1.md#RELEASE-18-1-MIGRATION)

[E.5.2. Changes](release-18-1.md#RELEASE-18-1-CHANGES)

**Release date:**2025-11-13

This release contains a variety of fixes from 18.0.
For information about new features in major release 18, see
[Section E.6](release-18.md).

<a id="RELEASE-18-1-MIGRATION"></a>

### E.5.1. Migration to Version 18.1 [#](#RELEASE-18-1-MIGRATION)

A dump/restore is not required for those running 18.X.

<a id="RELEASE-18-1-CHANGES"></a>

### E.5.2. Changes [#](#RELEASE-18-1-CHANGES)

* Check for `CREATE` privileges on the schema
  in `CREATE STATISTICS` (Jelte Fennema-Nio)
  [§](https://postgr.es/c/00eb646ea)

  This omission allowed table owners to create statistics in any
  schema, potentially leading to unexpected naming conflicts.

  The PostgreSQL Project thanks
  Jelte Fennema-Nio for reporting this problem.
  (CVE-2025-12817)
* Avoid integer overflow in allocation-size calculations
  within libpq (Jacob Champion)
  [§](https://postgr.es/c/7eb8fcad8)

  Several places in libpq were not
  sufficiently careful about computing the required size of a memory
  allocation. Sufficiently large inputs could cause integer overflow,
  resulting in an undersized buffer, which would then lead to writing
  past the end of the buffer.

  The PostgreSQL Project thanks Aleksey
  Solovev of Positive Technologies for reporting this problem.
  (CVE-2025-12818)
* Prevent “unrecognized node type” errors when a SQL/JSON
  function such as `JSON_VALUE` has
  a `DEFAULT` clause containing
  a `COLLATE` expression (Jian He)
  [§](https://postgr.es/c/dc9125111)
  [§](https://postgr.es/c/1baae827e)
* Avoid incorrect optimization of
  variable-free `HAVING` clauses with grouping sets
  (Richard Guo)
  [§](https://postgr.es/c/40c242830)
  [§](https://postgr.es/c/ee49f2cf4)
* Do not use parallelism in hash right semi joins (Richard Guo)
  [§](https://postgr.es/c/ef6168baf)

  The case does not work reliably due to a race condition in updating
  the join's shared hash table.
* Avoid possible division-by-zero when creating ordered-append plans
  (Richard Guo)
  [§](https://postgr.es/c/500f64636)

  This mistake could result in incorrect selection of the cheapest
  path, or in an assertion failure in debug builds.
* Fix planner failure with index types that can do ordered access but
  not index-only scans (Maxime Schoemans)
  [§](https://postgr.es/c/74197bdc8)

  This oversight resulted in errors like “no data returned for
  index-only scan”. The case does not arise with any in-core
  index type, but some extensions encountered the problem.
* Remove faulty assertion in btree index cleanup (Peter Geoghegan)
  [§](https://postgr.es/c/61de81a49)
* Avoid possible out-of-memory or “invalid memory alloc request
  size” failures during parallel GIN index build (Tomas Vondra)
  [§](https://postgr.es/c/a26b753a0)
* Ensure that BRIN autosummarization provides a snapshot for index
  expressions that need one (Álvaro Herrera)
  [§](https://postgr.es/c/419ffde23)
  [§](https://postgr.es/c/8733f0b54)

  Previously, autosummarization would fail for such indexes, and then
  leave placeholder index tuples behind, causing the index to bloat
  over time.
* Fix integer-overflow hazard in BRIN index scans when the table
  contains close to 232 pages (Sunil S)
  [§](https://postgr.es/c/715983a81)

  This oversight could result in an infinite loop or scanning of
  unneeded table pages.
* Fix incorrect zero-extension of stored values in JIT-generated tuple
  deforming code (David Rowley)
  [§](https://postgr.es/c/ceb51d09b)

  When not using JIT, the equivalent code does sign-extension not
  zero-extension, leading to a different Datum representation of small
  integer data types. This inconsistency was masked in most cases,
  but it is known to lead to “could not find memoization table
  entry” errors when using Memoize plan nodes, and there might
  be other symptoms.
* Fix rare crash when processing hashed `GROUPING
  SETS` queries (David Rowley)
  [§](https://postgr.es/c/0b6a02f03)
* Repair faulty hash-table-size-choosing logic in hash joins
  (Tomas Vondra)
  [§](https://postgr.es/c/aa151022e)

  Hash joins sometimes used more memory than intended, or failed to
  divide it in an efficient way.
* Improve relation lookup logic in statistics manipulation functions
  (Nathan Bossart)
  [§](https://postgr.es/c/c8af5019b)
  [§](https://postgr.es/c/15d7dded0)

  Fix `pg_restore_relation_stats()`,
  `pg_clear_relation_stats()`,
  `pg_restore_attribute_stats()`, and
  `pg_clear_attribute_stats()` to check
  privileges before acquiring lock on the target relation
  rather than after.
* Fix incorrect logic for caching result-relation information for
  triggers (David Rowley, Amit Langote)
  [§](https://postgr.es/c/a2387c32f)

  In cases where partitions' column sets aren't physically identical
  to their parent partitioned tables' column sets, this oversight
  could lead to crashes.
* Fix crash during EvalPlanQual rechecks on partitioned tables (David
  Rowley, Amit Langote)
  [§](https://postgr.es/c/1296dcf18)
* Fix EvalPlanQual handling of foreign or custom joins that do not
  have an alternative local-join plan prepared for EPQ (Masahiko
  Sawada, Etsuro Fujita)
  [§](https://postgr.es/c/b14144325)

  In such cases the foreign or custom access method should be invoked
  normally, but that did not happen, typically leading to a crash.
* Avoid duplicating hash partition constraints during `DETACH
  CONCURRENTLY` (Haiyang Li)
  [§](https://postgr.es/c/08c037dff)

  `ALTER TABLE DETACH PARTITION CONCURRENTLY` was
  written to add a copy of the partitioning constraint to the
  now-detached partition. This was misguided, partially because
  non-concurrent `DETACH` doesn't do that, but mostly
  because in the case of hash partitioning the constraint expression
  contains references to the parent table's OID. That causes problems
  during dump/restore, or if the parent table is dropped
  after `DETACH`. In v19 and later, we'll no longer
  create any such copied constraints at all. In released branches, to
  minimize the risk of unforeseen consequences, only skip adding a
  copied constraint if it is for hash partitioning.
* Disallow generated columns in partition keys
  (Jian He, Ashutosh Bapat)
  [§](https://postgr.es/c/ba99c9491)

  This was already not allowed, but the check missed some cases, such
  as where the column reference is implicit in a whole-row reference.
* Disallow generated columns in `COPY ... FROM
  ... WHERE` clauses (Peter Eisentraut, Jian He)
  [§](https://postgr.es/c/0f9e0068b)

  Previously, incorrect behavior or an obscure error message resulted
  from attempting to reference such a column, since generated columns
  have not yet been computed at the point
  where `WHERE` filtering is done.
* Prevent setting a column as identity if it has a not-null constraint
  but the constraint is marked as invalid (Jian He)
  [§](https://postgr.es/c/d9ffc2729)

  Identity columns must be not-null, but the check for that missed
  this edge case.
* Avoid potential use-after-free in parallel vacuum (Kevin Oommen
  Anish)
  [§](https://postgr.es/c/76613b539)

  This bug seems to have no consequences in standard builds, but it's
  theoretically a hazard.
* Fix visibility checking for statistics objects
  in `pg_temp` (Noah Misch)
  [§](https://postgr.es/c/d024160ff)

  A statistics object located in a temporary schema cannot be named
  without schema qualification,
  but `pg_statistics_obj_is_visible()` missed that
  memo and could return “true” regardless. In turn,
  functions such as `pg_describe_object()` could
  fail to schema-qualify the object's name as expected.
* Fix minor memory leak during WAL replay of database creation
  (Nathan Bossart)
  [§](https://postgr.es/c/33e7b4a7c)
* Fix incorrect reporting of replication lag
  in `pg_stat_replication` view (Fujii Masao)
  [§](https://postgr.es/c/9670032cc)

  If any standby server's replay LSN stopped advancing,
  the `write_lag`
  and `flush_lag` columns would eventually
  stop updating.
* Avoid duplicative log messages about
  invalid `primary_slot_name` settings (Fujii Masao)
  [§](https://postgr.es/c/6ff7ba9fe)
* Avoid failures when `synchronized_standby_slots`
  references nonexistent replication slots (Shlok Kyal)
  [§](https://postgr.es/c/b45a8d7d8)
* Remove the unfinished slot state file after failing to write a
  replication slot's state to disk (Michael Paquier)
  [§](https://postgr.es/c/9a6ea00ac)

  Previously, a failure such as out-of-disk-space resulted in leaving
  a temporary `state.tmp` file behind. That's
  problematic because it would block all subsequent attempts to
  write the state, requiring manual intervention to clean up.
* Fix mishandling of lock timeout signals in parallel apply workers
  for logical replication (Hayato Kuroda)
  [§](https://postgr.es/c/37fc5de43)

  The same signal number was being used for both worker shutdown and
  lock timeout, leading to confusion.
* Avoid unwanted WAL receiver shutdown when switching from streaming
  to archive WAL source (Xuneng Zhou)
  [§](https://postgr.es/c/a14201073)

  During a timeline change, a standby server's WAL receiver should
  remain alive, waiting for a new WAL streaming start point. Instead
  it was repeatedly shutting down and immediately getting restarted,
  which could confuse status monitoring code.
* Fix use-after-free issue in the relation synchronization cache
  maintained by the pgoutput logical
  decoding plugin (Vignesh C, Masahiko Sawada)
  [§](https://postgr.es/c/32b95fc71)

  An error during logical decoding could result in crashes in
  subsequent logical decoding attempts in the same session.
  The case is only reachable when pgoutput
  is invoked via SQL functions.
* Avoid unnecessary invalidation of logical replication slots
  (Bertrand Drouvot)
  [§](https://postgr.es/c/bf3dba508)
* Re-establish special case for `C` collation in
  locale setup (Jeff Davis)
  [§](https://postgr.es/c/3ebea75f9)

  This fixes a regression in access to shared catalogs early in
  backend startup, before a database has been selected. It is not
  known to be a problem for any
  core PostgreSQL code, but some extensions
  were broken.
* Fix incorrect printing of messages about failures in checking
  whether the user has Windows administrator privilege (Bryan Green)
  [§](https://postgr.es/c/b48ae226e)

  This code would have crashed or at least printed garbage.
  No such cases have been reported though, indicating that failure of
  these system calls is extremely rare.
* Avoid crash when attempting to
  test PostgreSQL with certain libsanitizer
  options (Emmanuel Sibi, Jacob Champion)
  [§](https://postgr.es/c/6d8acb777)
* Fix false memory-context-checking warnings in debug builds
  on 64-bit Windows (David Rowley)
  [§](https://postgr.es/c/af3a79e08)
* Correctly handle `GROUP BY DISTINCT` in PL/pgSQL
  assignment statements (Tom Lane)
  [§](https://postgr.es/c/78a284b0b)

  The parser failed to record the `DISTINCT` option
  in this context, so that the command would act as if it were
  plain `GROUP BY`.
* Avoid leaking memory when handling a SQL error within PL/Python
  (Tom Lane)
  [§](https://postgr.es/c/447a794f6)

  This fixes a session-lifespan memory leak introduced in our previous
  minor releases.
* Fix libpq's handling of socket-related
  errors on Windows within its GSSAPI logic (Ning Wu, Tom Lane)
  [§](https://postgr.es/c/d83879a32)

  The code for encrypting/decrypting transmitted data using GSSAPI did
  not correctly recognize error conditions on the connection socket,
  since Windows reports those differently than other platforms. This
  led to failure to make such connections on Windows.
* Fix dumping of non-inherited not-null constraints on inherited table
  columns (Dilip Kumar)
  [§](https://postgr.es/c/0fe07fa11)

  pg_dump failed to preserve such
  constraints when dumping from a pre-v18 server.
* Fix pg_dump's sorting of
  foreign key constraints (Álvaro Herrera)
  [§](https://postgr.es/c/162e70ea0)

  Ensure consistent ordering of these database objects, as was
  already done for other object types.
* Fix assorted errors in the data compression logic
  in pg_dump
  and pg_restore
  (Daniel Gustafsson, Tom Lane)
  [§](https://postgr.es/c/8980c724b)
  [§](https://postgr.es/c/6a4009747)
  [§](https://postgr.es/c/aa1fcd087)

  Error checking was missing or incorrect in several places, and there
  were also portability issues that would manifest on big-endian
  hardware. These problems had been missed because this code is only
  used to read compressed TOC files within directory-format
  dumps. pg_dump never produces such a
  dump; the case can be reached only by manually compressing the TOC
  file after the fact, which is a supported thing to do but very
  uncommon.
* Fix pgbench to error out cleanly if
  a `COPY` operation is started (Anthonin Bonnefoy)
  [§](https://postgr.es/c/c00637b5f)

  pgbench doesn't intend to support this
  case, but previously it went into an infinite loop.
* Fix pgbench's reporting of multiple
  errors (Yugo Nagata)
  [§](https://postgr.es/c/29aabbc43)

  In cases where two successive `PQgetResult` calls
  both fail, pgbench might report the wrong
  error message.
* In pgbench, fix faulty assertion about
  errors in pipeline mode (Yugo Nagata)
  [§](https://postgr.es/c/c736808e0)
* Fix per-file memory leakage
  in pg_combinebackup (Tom Lane)
  [§](https://postgr.es/c/e2072b47b)
* Ensure that `contrib/pg_buffercache` functions
  can be canceled (Satyanarayana Narlapuram, Yuhang Qiu)
  [§](https://postgr.es/c/71aa2e114)
  [§](https://postgr.es/c/0beb7e933)

  Some code paths were capable of running for a long time without
  checking for interrupts.
* Fix `contrib/pg_prewarm`'s privilege checks for
  indexes (Ayush Vatsa, Nathan Bossart)
  [§](https://postgr.es/c/3ccf8e9ac)
  [§](https://postgr.es/c/c29d32d27)

  `pg_prewarm()` requires `SELECT`
  privilege on relations to be prewarmed. However, since indexes have
  no SQL privileges of their own, this resulted in non-superusers
  being unable to prewarm indexes. Instead, check
  for `SELECT` privilege on the index's table.
* In `contrib/pg_stat_statements`, avoid
  crash when two or more constants are marked as having the same
  location in the SQL statement text (Sami Imseih, Dmitry Dolgov)
  [§](https://postgr.es/c/b1635c166)
* Make `contrib/pgstattuple` more robust about
  empty or invalid index pages (Nitin Motiani)
  [§](https://postgr.es/c/fc295beb7)

  Count all-zero pages as free space, and ignore pages that are
  invalid according to a check of the page's special-space size.
  The code for btree indexes already counted all-zero pages as free,
  but the hash and gist code would error out, which has been found to
  be much less user-friendly. Similarly, make all three cases agree
  on ignoring corrupted pages rather than throwing errors.
* Harden our read and write barrier macros to satisfy Clang
  (Thomas Munro)
  [§](https://postgr.es/c/f8ccab0e9)

  We supposed that `__atomic_thread_fence()` is a
  sufficient barrier to prevent the C compiler from re-ordering memory
  accesses around it, but it appears that that's not true for Clang,
  allowing it to generate incorrect code for at least RISC-V, MIPS,
  and LoongArch machines. Add explicit compiler barriers to fix that.
* Fix PGXS build infrastructure to support building
  NLS `po` files for extensions (Ryo Matsumura)
  [§](https://postgr.es/c/6aa04a60c)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-1.html)（英文原文，待翻譯）
