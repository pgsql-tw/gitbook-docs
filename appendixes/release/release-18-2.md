## E.4. Release 18.2 [#](#RELEASE-18-2)

[E.4.1. Migration to Version 18.2](release-18-2.md#RELEASE-18-2-MIGRATION)

[E.4.2. Changes](release-18-2.md#RELEASE-18-2-CHANGES)

**Release date:**2026-02-12

This release contains a variety of fixes from 18.1.
For information about new features in major release 18, see
[Section E.6](release-18.md).

<a id="RELEASE-18-2-MIGRATION"></a>

### E.4.1. Migration to Version 18.2 [#](#RELEASE-18-2-MIGRATION)

A dump/restore is not required for those running 18.X.

However, if you have any indexes on `ltree` columns, it may
be necessary to reindex them after updating. See the sixth changelog
entry below.

<a id="RELEASE-18-2-CHANGES"></a>

### E.4.2. Changes [#](#RELEASE-18-2-CHANGES)

* Guard against unexpected dimensions
  of `oidvector`/`int2vector` (Tom Lane)
  [§](https://postgr.es/c/3b6588cd9)

  These data types are expected to be 1-dimensional arrays containing
  no nulls, but there are cast pathways that permit violating those
  expectations. Add checks to some functions that were depending on
  those expectations without verifying them, and could misbehave in
  consequence.

  The PostgreSQL Project thanks
  Altan Birler for reporting this problem.
  (CVE-2026-2003)
* Harden selectivity estimators against being attached to operators
  that accept unexpected data types (Tom Lane)
  [§](https://postgr.es/c/66ddac698)
  [§](https://postgr.es/c/b69af3dda)

  `contrib/intarray` contained a selectivity
  estimation function that could be abused for arbitrary code
  execution, because it did not check that its input was of the
  expected data type. Third-party extensions should check for similar
  hazards and add defenses using the technique intarray now uses.
  Since such extension fixes will take time, we now require superuser
  privilege to attach a non-built-in selectivity estimator to an
  operator.

  The PostgreSQL Project thanks
  Daniel Firer, as part of zeroday.cloud, for reporting this problem.
  (CVE-2026-2004)
* Fix buffer overrun in `contrib/pgcrypto`'s
  PGP decryption functions (Michael Paquier)
  [§](https://postgr.es/c/209f387b8)

  Decrypting a crafted message with an overlength session key caused a
  buffer overrun, with consequences as bad as arbitrary code
  execution.

  The PostgreSQL Project thanks
  Team Xint Code, as part of zeroday.cloud, for reporting this problem.
  (CVE-2026-2005)
* Fix inadequate validation of multibyte character lengths
  (Thomas Munro, Noah Misch)
  [§](https://postgr.es/c/df0852fe0)
  [§](https://postgr.es/c/efef05ba9)
  [§](https://postgr.es/c/7b5fc85be)
  [§](https://postgr.es/c/b0f5d25bc)
  [§](https://postgr.es/c/b42709194)
  [§](https://postgr.es/c/4543b02af)

  Assorted bugs allowed an attacker able to issue crafted SQL to
  overrun string buffers, with consequences as bad as arbitrary code
  execution. After these fixes, applications may
  observe “invalid byte sequence for encoding” errors
  when string functions process invalid text that has been stored in
  the database.

  The PostgreSQL Project thanks Paul Gerste
  and Moritz Sanft, as part of zeroday.cloud, for reporting this
  problem.
  (CVE-2026-2006)
* Harden `contrib/pg_trgm` against changes in
  string lowercasing behavior (Heikki Linnakangas)
  [§](https://postgr.es/c/e0965fb1a)
  [§](https://postgr.es/c/18548681d)

  Fix potential buffer overruns arising from the fact that in some
  locales lower-casing a string can produce more characters (not
  bytes) than were in the original. That behavior is new in version
  18, and so is the bug.

  The PostgreSQL Project thanks
  Heikki Linnakangas for reporting this problem.
  (CVE-2026-2007)
* Fix inconsistent case-insensitive matching
  in `contrib/ltree` (Jeff Davis)
  [§](https://postgr.es/c/806555e30)
  [§](https://postgr.es/c/8993bf099)

  Index-related routines in `ltree` used a
  different implementation of case-folding than the primary operators
  did. Their behavior was equivalent only if the default collation
  provider was libc and the encoding was single-byte.

  To fix, change the code to use case-folding with the database's
  default collation.
  This change will require reindexing indexes on `ltree`
  columns (regardless of the index access method) unless the database
  uses libc as collation provider and its encoding is single-byte.
  Without that, searches of such indexes will fail to locate relevant
  entries.
* When using `ALTER TABLE ... ADD CONSTRAINT` to add
  a not-null constraint with an explicit name, if the column is
  already marked NOT NULL, require that the provided name match the
  existing constraint name (Álvaro Herrera, Srinath Reddy Sadipiralla)
  [§](https://postgr.es/c/492a69e14)
* Don't allow CTE references in sub-selects to determine semantic
  levels of aggregate functions (Tom Lane)
  [§](https://postgr.es/c/12bc32917)

  This change undoes a change made two minor releases ago, instead
  throwing an error if a sub-select references a CTE that's below the
  semantic level that standard SQL rules would assign to the aggregate
  based on contained column references and aggregates. The attempted
  fix turned out to cause problems of its own, and it's unclear what
  to do instead. Since sub-selects within aggregates are disallowed
  altogether by the SQL standard, treating such cases as errors seems
  sufficient.
* Fix trigger transition table capture for `MERGE`
  in CTE queries (Dean Rasheed)
  [§](https://postgr.es/c/c6ce4dcf9)

  When executing a data-modifying CTE query containing both
  a `MERGE` and another DML operation on a table with
  statement-level `AFTER` triggers, the transition
  tables passed to the triggers would not include the rows affected by
  the `MERGE`, only those affected by the other
  operation(s).
* Fix incorrect pruning of rowmarks belonging to non-relation
  rangetable entries, such as subqueries (Dean Rasheed)
  [§](https://postgr.es/c/f335457e8)

  This led to incorrect results if a proposed row update needed to be
  modified by EvalPlanQual rechecking, as could happen if there was a
  concurrent update to that row.
* Fix failure when all children of a partitioned target table
  of an update or delete have been pruned (Amit Langote)
  [§](https://postgr.es/c/9f4b7bfc5)

  In such cases, the executor could report “could not find junk
  ctid column” errors, even though nothing needs to be done.
* Fix expression evaluation bug for a sub-select within an array
  subscript (Andres Freund)
  [§](https://postgr.es/c/bdc5dedfc)
* Fix text substring search for non-deterministic collations
  (Laurenz Albe)
  [§](https://postgr.es/c/18b349315)

  When using a non-deterministic collation, we failed to detect a
  match occurring at the very end of the searched string.
* Avoid possible planner failure when a query contains duplicate
  window function calls (Meng Zhang, David Rowley)
  [§](https://postgr.es/c/ccde5be68)

  Confusion over de-duplication of such calls could result in errors
  like “WindowFunc with winref 2 assigned to WindowAgg with
  winref 1”.
* Fix planner error with set-returning functions and grouping sets
  (Richard Guo)
  [§](https://postgr.es/c/382ce9cb7)

  When constructing a ProjectSet plan node, the planner failed to
  detect that subexpressions involving grouping expressions were
  already computed by the input plan. This led to inefficient plans
  or errors such as “variable not found in subplan target
  list”.
* Avoid incorrect optimization when a subquery's grouping clause
  contains a volatile or set-returning function (Richard Guo)
  [§](https://postgr.es/c/7650eabb6)

  The planner was willing to push down outer-query restrictions
  referencing such a grouping column, leading to incorrect behavior
  due to multiple evaluation of a volatile function, or errors caused
  by introduction of a set-returning function into the
  subquery's `WHERE`/`HAVING`
  clauses.
* Look through PlaceHolderVar nodes when searching for statistics
  about an expression (Richard Guo)
  [§](https://postgr.es/c/7e9f852a7)

  This change allows the planner to find relevant statistics about
  expressions pulled up from subqueries or used in `GROUP
  BY`, avoiding falling back to a default estimate.
  (Arguably we should adjust any found statistics to account for an
  increased probability of the value being NULL, but we've never done
  the equivalent thing for plain Vars either.) While this restriction
  is old, changes in PostgreSQL version 18
  made PlaceHolderVars more common than before, so make the change to
  avoid plan regressions in affected cases.
* Look through no-op PlaceHolderVar nodes when matching expressions to
  indexes (Richard Guo)
  [§](https://postgr.es/c/b4cf74420)

  Because PostgreSQL version 18 uses
  PlaceHolderVars in more cases than before, some queries that
  formerly could use an index failed to do so. Add logic to prevent
  that regression.
* Fix planner's conversion of `OR` clauses to
  ScalarArrayOp index conditions (Tender Wang, Tom Lane)
  [§](https://postgr.es/c/bf5b13a8a)

  The code did not handle RelabelType nodes correctly, and could
  generate invalid expressions or fail to perform a valid conversion.
* Allow indexscans on partial hash indexes even when the index's
  predicate implies the truth of the WHERE clause (Tom Lane)
  [§](https://postgr.es/c/a212877dc)

  Normally we drop a WHERE clause that is implied by the predicate,
  since it's pointless to test it; it must hold for every index
  entry. However that can prevent creation of an indexscan plan if
  the index is one that requires a WHERE clause on the leading index
  key, as hash indexes do. Don't drop implied clauses when
  considering such an index.
* Do not emit WAL for unlogged BRIN indexes (Kirill Reshke)
  [§](https://postgr.es/c/d77a5f981)

  One seldom-taken code path incorrectly emitted a WAL record
  relating to a BRIN index even if the index was marked unlogged.
  Crash recovery would then fail to replay that record, complaining
  that the file already exists.
* Use the correct ordering function in parallel GIN index builds
  (Tomas Vondra)
  [§](https://postgr.es/c/eee71a66c)

  The parallel code used the default ordering operator (which is
  determined by the column data type's btree opclass), whereas it
  should use the ordering function specified by the GIN opclass, if
  any. This led to a failure if the data type has no btree opclass,
  or to an invalid index if the opclass specifies an ordering function
  that doesn't agree with the btree opclass.
* Prevent truncation of CLOG that is still needed by
  unread `NOTIFY` messages (Joel Jacobson, Heikki
  Linnakangas)
  [§](https://postgr.es/c/321ec5462)
  [§](https://postgr.es/c/7b069a187)
  [§](https://postgr.es/c/82fa6b78d)

  This fix prevents “could not access status of
  transaction” errors when a backend is slow to
  absorb `NOTIFY` messages.
* Escalate errors occurring during `NOTIFY` message
  processing to FATAL, i.e. close the connection (Heikki Linnakangas)
  [§](https://postgr.es/c/aab4a84bb)

  Formerly, if a backend got an error while absorbing
  a `NOTIFY` message, it would advance past that
  message, report the error to the client, and move on. That behavior
  was fraught with problems though. One big concern is that the
  client has no good way to know that a notification was lost, and
  certainly no way to know what was in it. Depending on the
  application logic, missing a notification could cause the
  application to get stuck waiting, for example. Also, any remaining
  messages would not get processed until someone sent a
  new `NOTIFY`.

  Also, if the connection is idle at the time of receiving
  a `NOTIFY` signal, any ERROR would be escalated to
  FATAL anyway, due to unrelated concerns. Therefore, we've chosen to
  make that happen in all cases, for consistency and to provide a
  clear signal to the application that it might have missed some
  notifications.
* Consider grouping expressions when computing a query ID hash
  (Jian He)
  [§](https://postgr.es/c/9c3caad02)

  Previously, two queries that were the same except in `GROUP
  BY` expressions would be merged
  by `contrib/pg_stat_statements` and other users
  of query IDs.
* Fix erroneous counting of updates in `EXPLAIN ANALYZE
  MERGE` with a concurrent update (Dean Rasheed)
  [§](https://postgr.es/c/5749d95d4)

  This situation led to an incorrect count of “skipped”
  tuples in `EXPLAIN`'s output, or to an assertion
  failure in an assert-enabled build.
* Fix bug in following update chain when locking a tuple (Jasper
  Smit)
  [§](https://postgr.es/c/3e3a80f62)

  This code path neglected to check the xmin of the first new tuple in
  the update chain, making it possible to lock an unrelated tuple if
  the original updater aborted and the space was immediately reclaimed
  by `VACUUM` and then re-used.
  That could cause unexpected transaction delays or deadlocks.
  Errors associated with having identified the wrong tuple have also
  been observed.
* Fix incorrect handling of incremental backups of large tables
  (Robert Haas, Oleg Tkachenko)
  [§](https://postgr.es/c/c80b0c9d6)

  If a table exceeding 1GB (or in general, the installation's segment
  size) is truncated by `VACUUM` between the base
  backup and the incremental
  backup, pg_combinebackup could fail with
  an error about “truncation block length in excess of segment
  size”. This prevented restoring the incremental backup.
* Fix potential backend process crash at process exit due to trying to
  release a lock in an already-unmapped shared memory segment
  (Rahila Syed)
  [§](https://postgr.es/c/1943ceb38)
* Fix race condition in async I/O code (Andres Freund)
  [§](https://postgr.es/c/7f1b3a4ce)

  It was possible for the result code of an asynchronous I/O operation
  to be overwritten before it was fetched.
* Guard against incorrect truncation of the multixact log after a
  crash (Heikki Linnakangas)
  [§](https://postgr.es/c/09532a78b)
* Fix possibly mis-encoded result
  of `pg_stat_get_backend_activity()` (Chao Li)
  [§](https://postgr.es/c/06907e864)

  The shared-memory buffer holding a session's activity string can
  end with an incomplete multibyte character. Readers are supposed
  to truncate off any such incomplete character, but this function
  failed to do so.
* Guard against recursive memory context logging (Fujii Masao)
  [§](https://postgr.es/c/b863d8d87)

  A constant flow of signals requesting memory context logging could
  cause recursive execution of the logging code, which in theory could
  lead to stack overflow.
* Fix memory context usage when reinitializing a parallel execution
  context (Jakub Wartak, Jeevan Chalke)
  [§](https://postgr.es/c/57df5ab80)

  This error could result in a crash due to a subsidiary data
  structure having a shorter lifespan than the parallel context.
  The problem is not known to be reachable using only
  core PostgreSQL, but we have reports of
  trouble in extensions.
* Set next multixid's offset when creating a new multixid, to remove
  the wait loop that was needed in corner cases (Andrey Borodin)
  [§](https://postgr.es/c/e46041fd9)
  [§](https://postgr.es/c/02ba5e3be)

  The previous logic could get stuck waiting for an update that would
  never occur.
* Avoid rewriting data-modifying CTEs more than once (Bernice Southey,
  Dean Rasheed)
  [§](https://postgr.es/c/b880d9a02)

  Formerly, when updating an auto-updatable view or a relation with
  rules, if the original query had any data-modifying CTEs, the rewriter
  would rewrite those CTEs multiple times due to recursion. This was
  inefficient and could produce false errors if a CTE included an
  update of an always-generated column.
* Allow retrying initialization of a DSM registry entry
  (Nathan Bossart)
  [§](https://postgr.es/c/b83bcc0df)

  If we fail partway through initialization of a dynamic shared memory
  entry, allow the next attempt to use that entry to retry
  initialization. Previously the entry was left in a
  permanently-failed state.
* Avoid failure of NUMA status views when a page has been swapped out
  (Tomas Vondra)
  [§](https://postgr.es/c/9796c4f56)
* Avoid “operation not permitted” errors when querying
  NUMA page status with older libnuma versions (Tomas Vondra)
  [§](https://postgr.es/c/482e98ac4)
* Fail recovery if WAL does not exist back to the redo point indicated
  by the checkpoint record (Nitin Jadhav)
  [§](https://postgr.es/c/68ebdf2b0)

  Add an explicit check for this before starting recovery, so that no
  harm is done and a useful error message is provided. Previously,
  recovery might crash or corrupt the database in this situation.
* Avoid scribbling on the source query tree during `ALTER
  PUBLICATION` (Sunil S)
  [§](https://postgr.es/c/bea57a6b4)

  This error had the visible effect that an event trigger fired for
  the query would see only the first `publish`
  option, even if several had been specified. If such a query were
  set up as a prepared statement, re-executions would misbehave too.
* Pass connection options specified in `CREATE SUBSCRIPTION
  ... CONNECTION` to the publisher's walsender (Fujii Masao)
  [§](https://postgr.es/c/797fc5d1b)

  Before this fix, the `options` connection option
  (if any) was ignored, thus for example preventing setting custom
  server parameter values in the walsender session. It was intended
  for that to work, and it did work before refactoring
  in PostgreSQL version 15 broke it, so
  restore the previous behavior.
* Prevent invalidation of newly created or newly synced replication
  slots (Zhijie Hou)
  [§](https://postgr.es/c/919c9fa13)
  [§](https://postgr.es/c/1c60f7236)
  [§](https://postgr.es/c/d3ceb2084)

  A race condition with a concurrent checkpoint could allow WAL to be
  removed that is needed by the replication slot, causing the slot to
  immediately get marked invalid.
* Fix race condition in computing a replication slot's required xmin
  (Zhijie Hou)
  [§](https://postgr.es/c/fd7c86cfa)

  This could lead to the error “cannot build an initial slot
  snapshot as oldest safe xid follows snapshot's xmin”.
* During initial synchronization of a logical replication
  subscription, commit the addition of
  a `pg_replication_origin` entry before
  starting to copy data (Zhijie Hou)
  [§](https://postgr.es/c/b07c32619)

  Previously, if the copy step failed, the
  new `pg_replication_origin` entry would be
  lost due to transaction rollback. This led to inconsistent state in
  shared memory.
* Don't advance logical replication progress after a parallel worker
  apply failure (Zhijie Hou)
  [§](https://postgr.es/c/2f7ffe124)

  The previous behavior allowed transactions to be lost by a
  subscriber.
* Fix logical replication slotsync worker processes to handle
  LOCK_TIMEOUT signals correctly (Zhijie Hou)
  [§](https://postgr.es/c/6c61c69d5)

  Previously, timeout signals were effectively ignored.
* Fix possible failure with “unexpected data beyond EOF”
  during restart of a streaming replica server (Anthonin Bonnefoy)
  [§](https://postgr.es/c/9ed411e08)
* Fix error reporting for SQL/JSON path type mismatches (Jian He)
  [§](https://postgr.es/c/15ba0702c)

  The code could produce a “cache lookup failed for type 0”
  error instead of the intended complaint about the path expression
  not being of the right type.
* Fix erroneous tracking of column position when parsing partition
  range bounds (myzhen)
  [§](https://postgr.es/c/c35e5dd9a)

  This could, for example, lead to the wrong column name being cited
  in error messages about casting partition bound values to the
  column's data type.
* Fix assorted minor errors in error messages (Man Zeng, Tianchen Zhang)
  [§](https://postgr.es/c/acfa422c3)
  [§](https://postgr.es/c/2ca4464b6)
  [§](https://postgr.es/c/ab61f0087)
  [§](https://postgr.es/c/69ee81932)
  [§](https://postgr.es/c/cff2ef984)

  For example, an error report about mismatched timeline number in a
  backup manifest showed the starting timeline number where it meant
  to show the ending timeline number.
* Fix failure to perform function inlining when doing JIT compilation
  with LLVM version 17 or later (Anthonin Bonnefoy)
  [§](https://postgr.es/c/f1c6b153c)
* Adjust our JIT code to work with LLVM 21 (Holger Hoffstätte)
  [§](https://postgr.es/c/912cfa314)

  The previous coding failed to compile on aarch64 machines.
* Fix aarch64-specific code to build with old (RHEL7-era) system
  header files (Tom Lane)
  [§](https://postgr.es/c/db4eba152)
  [§](https://postgr.es/c/6a5170755)
* Fix incorrect configure probe
  for `io_uring_queue_init_mem()` (Masahiko Sawada)
  [§](https://postgr.es/c/640772c6d)

  This error resulted in failure to optimize async I/O buffer
  allocations in autotools-based builds, though the code did work when
  building with meson. The main impact of the omission was
  slower-than-necessary backend process exits.
* Add new server parameter [file_extend_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-EXTEND-METHOD) to
  control use of `posix_fallocate()` (Thomas Munro)
  [§](https://postgr.es/c/33e3de6d7)

  PostgreSQL version 16 and later will
  use `posix_fallocate()`, if the platform provides
  it, to extend relation files. However, this has been reported to
  interact poorly with some file systems: BTRFS compression is
  disabled by the use of `posix_fallocate()`, and
  XFS could produce spurious `ENOSPC` errors in older
  Linux kernel versions. To provide a workaround, introduce this new
  server parameter. Setting `file_extend_method`
  to `write_zeros` will cause the server to return to
  the old method of extending files by writing blocks of zeroes.
* Honor `open()`'s `O_CLOEXEC`
  flag on Windows (Bryan Green, Thomas Munro)
  [§](https://postgr.es/c/bebb281b0)
  [§](https://postgr.es/c/a7d06e74d)
  [§](https://postgr.es/c/4da5c33a3)

  Make this flag work like it does on POSIX platforms, so that we
  don't leak file handles into child processes such as `COPY
  TO/FROM PROGRAM`. While that leakage hasn't caused many
  problems, it seems undesirable.
* Fix failure to parse long options on the server command line in
  Solaris executables built with meson (Tom Lane)
  [§](https://postgr.es/c/5eac1d68f)
* Support process title changes on GNU/Hurd (Michael Banck)
  [§](https://postgr.es/c/bcfca332f)
* Fix psql's tab completion
  for `VACUUM` option values (Yugo Nagata)
  [§](https://postgr.es/c/4e1376900)
* In psql command prompts,
  do not show a value for `%P` (pipeline status) when
  there is no server connection (Chao Li)
  [§](https://postgr.es/c/d42735b1e)

  This makes `%P` act like other prompt escape
  sequences whose values depend on the active connection.
* Fix pg_dump's logic for collecting
  sequence values (Nathan Bossart)
  [§](https://postgr.es/c/39d555576)
  [§](https://postgr.es/c/56e1f5010)

  pg_dump failed if a sequence was dropped
  concurrently with the dump, even if the sequence was not among the
  database objects to be dumped. Also, if the calling user lacks
  privileges to read a sequence's
  value, pg_dump emitted incorrect values
  rather than failing as expected.
* Fix potentially-incorrect quoting
  of `oauth_validator_libraries` values
  by pg_dump (ChangAo Chen)
  [§](https://postgr.es/c/61c78e1f4)

  pg_dump applied the wrong quoting rule if
  it needed to dump a value of this setting.
* Avoid pg_dump assertion failure in
  binary-upgrade mode (Vignesh C)
  [§](https://postgr.es/c/573e679a2)

  Failure to handle subscription-relation objects in the object
  sorting code triggered an assertion, though there were no serious
  ill effects in production builds.
* Fix incorrect error handling in pgbench
  with multiple `\syncpipeline` commands
  in pipeline mode (Yugo Nagata)
  [§](https://postgr.es/c/00e64e35c)

  If multiple `\syncpipeline` commands are
  encountered after a query error, pgbench
  would report “failed to exit pipeline mode”, or get an
  assertion failure in an assert-enabled build.
* Make pg_resetwal print the updated value
  when changing OldestXID (Heikki Linnakangas)
  [§](https://postgr.es/c/19594271c)

  It already did that for every other variable it can change.
* Make pg_resetwal allow setting next
  multixact xid to 0 or next multixact offset to UINT32_MAX (Maxim
  Orlov)
  [§](https://postgr.es/c/8747b969f)

  These are valid values, so rejecting them was incorrect. In the
  worst case, if a pg_upgrade is attempted when exactly at the point
  of multixact wraparound, the upgrade would fail.
* In `contrib/amcheck`, use the correct snapshot
  for btree index parent checks (Mihail Nikalayeu)
  [§](https://postgr.es/c/df93f94dd)
  [§](https://postgr.es/c/3c83a2a0a)

  The previous coding caused spurious errors when examining indexes
  created with `CREATE INDEX CONCURRENTLY`.
* Fix `contrib/amcheck` to
  handle “half-dead” btree index pages correctly
  (Heikki Linnakangas)
  [§](https://postgr.es/c/19e786727)

  `amcheck` expected such a page to have a parent
  downlink, but it does not, leading to a false error report
  about “mismatch between parent key and child high key”.
* Fix `contrib/amcheck` to
  handle incomplete btree root page splits correctly
  (Heikki Linnakangas)
  [§](https://postgr.es/c/50c63ebb0)

  `amcheck` could report a false error
  about “block is not true root”.
* Fix excessive memory allocation
  in `contrib/pg_buffercache` (David Geier)
  [§](https://postgr.es/c/580b5c2f3)

  The code allocated twice as much memory as it needed for NUMA
  page status.
* Fix edge-case integer overflow
  in `contrib/intarray`'s selectivity estimator
  for `@@` (Chao Li)
  [§](https://postgr.es/c/07c1c6ec5)

  This could cause poor selectivity estimates to be produced for cases
  involving the maximum integer value.
* Fix multibyte-encoding issue in `contrib/ltree`
  (Jeff Davis)
  [§](https://postgr.es/c/f79e239e0)

  The previous coding could pass an incomplete multibyte character
  to `lower()`, probably resulting in incorrect
  behavior.
* Avoid crash in `contrib/pg_stat_statements` when
  an `IN` list contains both constants and
  non-constant expressions (Sami Imseih)
  [§](https://postgr.es/c/3304e97b1)
* Update time zone data files to tzdata
  release 2025c (Tom Lane)
  [§](https://postgr.es/c/6574bee64)

  The only change is in historical data for pre-1976 timestamps in
  Baja California.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-2.html)（英文原文，待翻譯）
