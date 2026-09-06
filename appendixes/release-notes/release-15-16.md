<a id="RELEASE-15-16"></a>

# E.4. Release 15.16

[E.4.1. Migration to Version 15.16](#id-1.11.6.9.4)

[E.4.2. Changes](#id-1.11.6.9.5)

<strong>Release date: </strong>2026-02-12

This release contains a variety of fixes from 15.15. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.9.4"></a>

## E.4.1. Migration to Version 15.16

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.14, see [Section E.6](release-15-14.md).

<a id="id-1.11.6.9.5"></a>

## E.4.2. Changes

* Guard against unexpected dimensions of `oidvector`/`int2vector` (Tom Lane) [§](https://postgr.es/c/429aeaebd)

  These data types are expected to be 1-dimensional arrays containing no nulls, but there are cast pathways that permit violating those expectations. Add checks to some functions that were depending on those expectations without verifying them, and could misbehave in consequence.

  The PostgreSQL Project thanks Altan Birler for reporting this problem. (CVE-2026-2003)
* Harden selectivity estimators against being attached to operators that accept unexpected data types (Tom Lane) [§](https://postgr.es/c/b764b26f2) [§](https://postgr.es/c/deb464a40) [§](https://postgr.es/c/3ecc84cce)

  `contrib/intarray` contained a selectivity estimation function that could be abused for arbitrary code execution, because it did not check that its input was of the expected data type. Third-party extensions should check for similar hazards and add defenses using the technique intarray now uses. Since such extension fixes will take time, we now require superuser privilege to attach a non-built-in selectivity estimator to an operator.

  The PostgreSQL Project thanks Daniel Firer, as part of zeroday.cloud, for reporting this problem. (CVE-2026-2004)
* Fix buffer overrun in `contrib/pgcrypto`'s PGP decryption functions (Michael Paquier) [§](https://postgr.es/c/9a9982ec6)

  Decrypting a crafted message with an overlength session key caused a buffer overrun, with consequences as bad as arbitrary code execution.

  The PostgreSQL Project thanks Team Xint Code, as part of zeroday.cloud, for reporting this problem. (CVE-2026-2005)
* Fix inadequate validation of multibyte character lengths (Thomas Munro, Noah Misch) [§](https://postgr.es/c/b2c81ac86) [§](https://postgr.es/c/50863be0b) [§](https://postgr.es/c/fd82ddb67) [§](https://postgr.es/c/757bf8145) [§](https://postgr.es/c/8f8b1ffac) [§](https://postgr.es/c/6f741bcb6)

  Assorted bugs allowed an attacker able to issue crafted SQL to overrun string buffers, with consequences as bad as arbitrary code execution. After these fixes, applications may observe “invalid byte sequence for encoding” errors when string functions process invalid text that has been stored in the database.

  The PostgreSQL Project thanks Paul Gerste and Moritz Sanft, as part of zeroday.cloud, for reporting this problem. (CVE-2026-2006)
* Don't allow CTE references in sub-selects to determine semantic levels of aggregate functions (Tom Lane) [§](https://postgr.es/c/9f5a58aac)

  This change undoes a change made two minor releases ago, instead throwing an error if a sub-select references a CTE that's below the semantic level that standard SQL rules would assign to the aggregate based on contained column references and aggregates. The attempted fix turned out to cause problems of its own, and it's unclear what to do instead. Since sub-selects within aggregates are disallowed altogether by the SQL standard, treating such cases as errors seems sufficient.
* Fix trigger transition table capture for `MERGE` in CTE queries (Dean Rasheed) [§](https://postgr.es/c/c5824536e)

  When executing a data-modifying CTE query containing both a `MERGE` and another DML operation on a table with statement-level `AFTER` triggers, the transition tables passed to the triggers would not include the rows affected by the `MERGE`, only those affected by the other operation(s).
* Fix failure when all children of a partitioned target table of an update or delete have been pruned (Amit Langote) [§](https://postgr.es/c/687533b39)

  In such cases, the executor could report “could not find junk ctid column” errors, even though nothing needs to be done.
* Allow indexscans on partial hash indexes even when the index's predicate implies the truth of the WHERE clause (Tom Lane) [§](https://postgr.es/c/f19502f04)

  Normally we drop a WHERE clause that is implied by the predicate, since it's pointless to test it; it must hold for every index entry. However that can prevent creation of an indexscan plan if the index is one that requires a WHERE clause on the leading index key, as hash indexes do. Don't drop implied clauses when considering such an index.
* Do not emit WAL for unlogged BRIN indexes (Kirill Reshke) [§](https://postgr.es/c/460d97020)

  One seldom-taken code path incorrectly emitted a WAL record relating to a BRIN index even if the index was marked unlogged. Crash recovery would then fail to replay that record, complaining that the file already exists.
* Prevent truncation of CLOG that is still needed by unread `NOTIFY` messages (Joel Jacobson, Heikki Linnakangas) [§](https://postgr.es/c/1a469d7b5) [§](https://postgr.es/c/0c862646c) [§](https://postgr.es/c/21a9014cf)

  This fix prevents “could not access status of transaction” errors when a backend is slow to absorb `NOTIFY` messages.
* Escalate errors occurring during `NOTIFY` message processing to FATAL, i.e. close the connection (Heikki Linnakangas) [§](https://postgr.es/c/b1da37de2)

  Formerly, if a backend got an error while absorbing a `NOTIFY` message, it would advance past that message, report the error to the client, and move on. That behavior was fraught with problems though. One big concern is that the client has no good way to know that a notification was lost, and certainly no way to know what was in it. Depending on the application logic, missing a notification could cause the application to get stuck waiting, for example. Also, any remaining messages would not get processed until someone sent a new `NOTIFY`.

  Also, if the connection is idle at the time of receiving a `NOTIFY` signal, any ERROR would be escalated to FATAL anyway, due to unrelated concerns. Therefore, we've chosen to make that happen in all cases, for consistency and to provide a clear signal to the application that it might have missed some notifications.
* Fix bug in following update chain when locking a tuple (Jasper Smit) [§](https://postgr.es/c/5d5487cd2)

  This code path neglected to check the xmin of the first new tuple in the update chain, making it possible to lock an unrelated tuple if the original updater aborted and the space was immediately reclaimed by `VACUUM` and then re-used. That could cause unexpected transaction delays or deadlocks. Errors associated with having identified the wrong tuple have also been observed.
* Fix issues around in-place catalog updates (Noah Misch) [§](https://postgr.es/c/05d605b6c) [§](https://postgr.es/c/20a48c156) [§](https://postgr.es/c/86091202a)

  Send a nontransactional invalidation message for an in-place update, since such an update will survive transaction rollback. Also ensure that the update is WAL-logged before other sessions can see it. These fixes primarily prevent scenarios in which relations' frozen-XID attributes become inconsistent, possibly allowing premature CLOG truncation and subsequent “could not access status of transaction” errors.
* Fix potential backend process crash at process exit due to trying to release a lock in an already-unmapped shared memory segment (Rahila Syed) [§](https://postgr.es/c/b926ff137)
* Guard against incorrect truncation of the multixact log after a crash (Heikki Linnakangas) [§](https://postgr.es/c/a563ac619)
* Fix possibly mis-encoded result of `pg_stat_get_backend_activity()` (Chao Li) [§](https://postgr.es/c/300575fe2)

  The shared-memory buffer holding a session's activity string can end with an incomplete multibyte character. Readers are supposed to truncate off any such incomplete character, but this function failed to do so.
* Guard against recursive memory context logging (Fujii Masao) [§](https://postgr.es/c/0fc2f533a)

  A constant flow of signals requesting memory context logging could cause recursive execution of the logging code, which in theory could lead to stack overflow.
* Fix memory context usage when reinitializing a parallel execution context (Jakub Wartak, Jeevan Chalke) [§](https://postgr.es/c/bd2726d3e)

  This error could result in a crash due to a subsidiary data structure having a shorter lifespan than the parallel context. The problem is not known to be reachable using only core PostgreSQL, but we have reports of trouble in extensions.
* Set next multixid's offset when creating a new multixid, to remove the wait loop that was needed in corner cases (Andrey Borodin) [§](https://postgr.es/c/8cfb174a6) [§](https://postgr.es/c/b9a02b978)

  The previous logic could get stuck waiting for an update that would never occur.
* Avoid rewriting data-modifying CTEs more than once (Bernice Southey, Dean Rasheed) [§](https://postgr.es/c/134a8ee22)

  Formerly, when updating an auto-updatable view or a relation with rules, if the original query had any data-modifying CTEs, the rewriter would rewrite those CTEs multiple times due to recursion. This was inefficient and could produce false errors if a CTE included an update of an always-generated column.
* Fail recovery if WAL does not exist back to the redo point indicated by the checkpoint record (Nitin Jadhav) [§](https://postgr.es/c/95ef6f490)

  Add an explicit check for this before starting recovery, so that no harm is done and a useful error message is provided. Previously, recovery might crash or corrupt the database in this situation.
* Avoid scribbling on the source query tree during `ALTER PUBLICATION` (Sunil S) [§](https://postgr.es/c/f20b79059)

  This error had the visible effect that an event trigger fired for the query would see only the first `publish` option, even if several had been specified. If such a query were set up as a prepared statement, re-executions would misbehave too.
* Pass connection options specified in `CREATE SUBSCRIPTION ... CONNECTION` to the publisher's walsender (Fujii Masao) [§](https://postgr.es/c/f7eb44e0f)

  Before this fix, the `options` connection option (if any) was ignored, thus for example preventing setting custom server parameter values in the walsender session. It was intended for that to work, and it did work before refactoring in PostgreSQL version 15 broke it, so restore the previous behavior.
* Prevent invalidation of newly created or newly synced replication slots (Zhijie Hou) [§](https://postgr.es/c/aae05622a)

  A race condition with a concurrent checkpoint could allow WAL to be removed that is needed by the replication slot, causing the slot to immediately get marked invalid.
* Fix race condition in computing a replication slot's required xmin (Zhijie Hou) [§](https://postgr.es/c/fa557d300)

  This could lead to the error “cannot build an initial slot snapshot as oldest safe xid follows snapshot's xmin”.
* During initial synchronization of a logical replication subscription, commit the addition of a `pg_replication_origin` entry before starting to copy data (Zhijie Hou) [§](https://postgr.es/c/90d1beef6)

  Previously, if the copy step failed, the new `pg_replication_origin` entry would be lost due to transaction rollback. This led to inconsistent state in shared memory.
* Fix possible failure with “unexpected data beyond EOF” during restart of a streaming replica server (Anthonin Bonnefoy) [§](https://postgr.es/c/ef8465588)
* Fix erroneous tracking of column position when parsing partition range bounds (myzhen) [§](https://postgr.es/c/3ad05640b)

  This could, for example, lead to the wrong column name being cited in error messages about casting partition bound values to the column's data type.
* Fix assorted minor errors in error messages (Man Zeng, Tianchen Zhang) [§](https://postgr.es/c/4ec943f7d) [§](https://postgr.es/c/fbf8df580) [§](https://postgr.es/c/9dcd0b3de)

  For example, an error report about mismatched timeline number in a backup manifest showed the starting timeline number where it meant to show the ending timeline number.
* Fix failure to perform function inlining when doing JIT compilation with LLVM version 17 or later (Anthonin Bonnefoy) [§](https://postgr.es/c/cbdd09ae1)
* Adjust our JIT code to work with LLVM 21 (Holger Hoffstätte) [§](https://postgr.es/c/55164852d)

  The previous coding failed to compile on aarch64 machines.
* Support process title changes on GNU/Hurd (Michael Banck) [§](https://postgr.es/c/3995e4a9d)
* Make pg_resetwal print the updated value when changing OldestXID (Heikki Linnakangas) [§](https://postgr.es/c/7c494072b)

  It already did that for every other variable it can change.
* Make pg_resetwal allow setting next multixact xid to 0 or next multixact offset to UINT32_MAX (Maxim Orlov) [§](https://postgr.es/c/97cd4b65a)

  These are valid values, so rejecting them was incorrect. In the worst case, if a pg_upgrade is attempted when exactly at the point of multixact wraparound, the upgrade would fail.
* In `contrib/amcheck`, use the correct snapshot for btree index parent checks (Mihail Nikalayeu) [§](https://postgr.es/c/dcddd6987)

  The previous coding caused spurious errors when examining indexes created with `CREATE INDEX CONCURRENTLY`.
* Fix `contrib/amcheck` to handle “half-dead” btree index pages correctly (Heikki Linnakangas) [§](https://postgr.es/c/7792bdc45)

  `amcheck` expected such a page to have a parent downlink, but it does not, leading to a false error report about “mismatch between parent key and child high key”.
* Fix `contrib/amcheck` to handle incomplete btree root page splits correctly (Heikki Linnakangas) [§](https://postgr.es/c/721b58fbe)

  `amcheck` could report a false error about “block is not true root”.
* Fix edge-case integer overflow in `contrib/intarray`'s selectivity estimator for `@@` (Chao Li) [§](https://postgr.es/c/c89510431)

  This could cause poor selectivity estimates to be produced for cases involving the maximum integer value.
* Fix multibyte-encoding issue in `contrib/ltree` (Jeff Davis) [§](https://postgr.es/c/335b2f30b)

  The previous coding could pass an incomplete multibyte character to `lower()`, probably resulting in incorrect behavior.
* Update time zone data files to tzdata release 2025c (Tom Lane) [§](https://postgr.es/c/00410b76d)

  The only change is in historical data for pre-1976 timestamps in Baja California.

---

原文：[PostgreSQL 15.19 Documentation](release-15-16.md)（英文原文，待翻譯）
