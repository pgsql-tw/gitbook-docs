<a id="RELEASE-15-4"></a>

# E.16. Release 15.4

[E.16.1. Migration to Version 15.4](#id-1.11.6.21.4)

[E.16.2. Changes](#id-1.11.6.21.5)

<strong>Release date: </strong>2023-08-10

This release contains a variety of fixes from 15.3. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.21.4"></a>

## E.16.1. Migration to Version 15.4

A dump/restore is not required for those running 15.X.

However, if you use BRIN indexes, it may be advisable to reindex them; see the third changelog entry below.

Also, if you are upgrading from a version earlier than 15.1, see [Section E.19](e.2.-release-15.1.md).

<a id="id-1.11.6.21.5"></a>

## E.16.2. Changes

* Disallow substituting a schema or owner name into an extension script if the name contains a quote, backslash, or dollar sign (Noah Misch) [§](https://postgr.es/c/de494ec14)

  This restriction guards against SQL-injection hazards for trusted extensions.

  The PostgreSQL Project thanks Micah Gates, Valerie Woolard, Tim Carey-Smith, and Christoph Berg for reporting this problem. (CVE-2023-39417)
* Fix `MERGE` to enforce row security policies properly (Dean Rasheed) [§](https://postgr.es/c/cb2ae5741)

  When `MERGE` performs an `UPDATE` action, it should enforce any `UPDATE` or `SELECT` RLS policies defined on the target table, to be consistent with the way that a plain `UPDATE` with a `WHERE` clause works. Instead it was enforcing `INSERT` RLS policies for both `INSERT` and `UPDATE` actions.

  In addition, when `MERGE` performs a `DO NOTHING` action, it applied the target table's `DELETE` RLS policies to existing rows, even though those rows are not being deleted. While it's not a security problem, this could result in unwanted errors.

  The PostgreSQL Project thanks Dean Rasheed for reporting this problem. (CVE-2023-39418)
* Fix confusion between empty (no rows) ranges and all-NULL ranges in BRIN indexes, as well as incorrect merging of all-NULL summaries (Tomas Vondra) [§](https://postgr.es/c/e18769323) [§](https://postgr.es/c/80f64b900)

  Each of these oversights could result in forgetting that a BRIN index range contains any NULL values, potentially allowing subsequent queries that should return NULL values to miss doing so.

  This fix will not in itself correct faulty BRIN entries. It's recommended to `REINDEX` any BRIN indexes that may be used to search for nulls.
* Avoid leaving a corrupted database behind when `DROP DATABASE` is interrupted (Andres Freund) [§](https://postgr.es/c/f66403749)

  If `DROP DATABASE` was interrupted after it had already begun taking irreversible steps, the target database remained accessible (because the removal of its `pg_database` row would roll back), but it would have corrupt contents. Fix by marking the database as inaccessible before we begin to perform irreversible operations. A failure after that will leave the database still partially present, but nothing can be done with it except to issue another `DROP DATABASE`.
* Ensure that partitioned indexes are correctly marked as valid or not at creation (Michael Paquier) [§](https://postgr.es/c/cb4ac3e56)

  If a new partitioned index matches an existing but invalid index on one of the partitions, the partitioned index could end up being marked valid prematurely. This could lead to misbehavior or assertion failures in subsequent queries on the partitioned table.
* Ignore invalid child indexes when matching partitioned indexes to child indexes during `ALTER TABLE ATTACH PARTITION` (Michael Paquier) [§](https://postgr.es/c/7aa17b498)

  Such an index will now be ignored, and a new child index created instead.
* Fix possible failure when marking a partitioned index valid after all of its partitions have been attached (Michael Paquier) [§](https://postgr.es/c/c0dc97c7b)

  The update of the index's `pg_index` entry could use stale data for other columns. One reported symptom is an “attempted to update invisible tuple” error.
* Fix `ALTER EXTENSION SET SCHEMA` to complain if the extension contains any objects outside the extension's schema (Michael Paquier, Heikki Linnakangas) [§](https://postgr.es/c/d1e0f408c)

  Erroring out if the extension contains objects in multiple schemas was always intended; but the check was mis-coded so that it would fail to detect some cases, leading to surprising behavior.
* Fix tracking of tables' access method dependencies (Michael Paquier) [§](https://postgr.es/c/93401ec02)

  `ALTER TABLE ... SET ACCESS METHOD` failed to update relevant `pg_depend` entries when changing a table's access method. When using non-built-in access methods, this creates a risk that an access method could be dropped even though tables still depend on it. This fix corrects the logic in `ALTER TABLE`, but it will not adjust any already-missing `pg_depend` entries.
* Don't use partial unique indexes for uniqueness proofs in the planner (David Rowley) [§](https://postgr.es/c/8f2ec8cc7)

  This could give rise to incorrect plans, since the presumed uniqueness of rows read from a table might not hold if the index in question isn't used to scan the table.
* Don't Memoize lateral joins with volatile join conditions (Richard Guo) [§](https://postgr.es/c/71662373b)

  Applying Memoize to a sub-plan that contains volatile filter conditions is likely to lead to wrong answers. The check to avoid doing this missed some cases that can arise when using `LATERAL`.
* Avoid producing incorrect plans for foreign joins with pseudoconstant join clauses (Etsuro Fujita) [§](https://postgr.es/c/d1ef5631e)

  The planner currently lacks support for attaching pseudoconstant join clauses to a pushed-down remote join, so disable generation of remote joins in such cases. (A better solution will require ABI-breaking changes of planner data structures, so it will have to wait for a future major release.)
* Correctly handle sub-SELECTs in RLS policy expressions and security-barrier views when expanding rule actions (Tom Lane) [§](https://postgr.es/c/cc6974df1)
* Fix race conditions in conflict detection for `SERIALIZABLE` isolation mode (Thomas Munro) [§](https://postgr.es/c/d34aa0a2f) [§](https://postgr.es/c/ab265e985) [§](https://postgr.es/c/0f275b0ee)

  Conflicts could be missed when using bitmap heap scans, when using GIN indexes, and when examining an initially-empty btree index. All these cases could lead to serializability failures due to improperly allowing conflicting transactions to commit.
* Fix misbehavior of EvalPlanQual checks with inherited or partitioned target tables (Tom Lane) [§](https://postgr.es/c/4729d1e8a)

  This oversight could lead to update or delete actions in `READ COMMITTED` isolation mode getting performed when they should have been skipped because of a conflicting concurrent update.
* Fix hash join with an inner-side hash key that contains Params coming from an outer nested loop (Tom Lane) [§](https://postgr.es/c/c2f974fff)

  When rescanning the join after the values of such Params have changed, we must rebuild the hash table, but neglected to do so. This could result in missing join output rows.
* Fix intermittent failures when trying to update a field of a composite column (Tom Lane) [§](https://postgr.es/c/cc8cca3c2)

  If the overall value of the composite column is wide enough to require out-of-line toasting, then an unluckily-timed cache flush could cause errors or server crashes.
* Prevent query-lifespan memory leaks in some `UPDATE` queries with triggers (Tomas Vondra) [§](https://postgr.es/c/ee87f8b63) [§](https://postgr.es/c/7ae4e7868)
* Prevent query-lifespan memory leaks when an Incremental Sort plan node is rescanned (James Coleman, Laurenz Albe, Tom Lane) [§](https://postgr.es/c/0c5fe4ff6)
* Accept fractional seconds in the input to `jsonpath`'s `datetime()` method (Tom Lane) [§](https://postgr.es/c/bd590d1fe)
* Prevent stack-overflow crashes with very complex text search patterns (Tom Lane) [§](https://postgr.es/c/a77d90171)
* Allow tokens up to 10240 bytes long in `pg_hba.conf` and `pg_ident.conf` (Tom Lane) [§](https://postgr.es/c/313ceda2f)

  The previous limit of 256 bytes has been found insufficient for some use-cases.
* Ensure that all existing placeholders are checked for matches when an extension declares its GUC prefix to be reserved (Karina Litskevich, Ekaterina Sokolova) [§](https://postgr.es/c/a5f312c58)

  Faulty loop logic could cause some entries to be skipped.
* Fix mishandling of C++ out-of-memory conditions (Heikki Linnakangas) [§](https://postgr.es/c/fa96a74a0)

  If JIT is in use, running out of memory in a C++ `new` call would lead to a PostgreSQL FATAL error, instead of the expected C++ exception.
* Fix rare null-pointer crash in `plancache.c` (Tom Lane) [§](https://postgr.es/c/fbaf65cd6)
* Avoid leaking a stats entry for a subscription when it is dropped (Masahiko Sawada) [§](https://postgr.es/c/66f8a1397)
* Avoid losing track of possibly-useful shared memory segments when a page free results in coalescing ranges of free space (Dongming Liu) [§](https://postgr.es/c/9ffb10f18)

  Ensure that the segment is moved into the appropriate “bin” for its new amount of free space, so that it will be found by subsequent searches.
* Allow `VACUUM` to continue after detecting certain types of b-tree index corruption (Peter Geoghegan) [§](https://postgr.es/c/642bec1f8) [§](https://postgr.es/c/6983a5112)

  If an invalid sibling-page link is detected, log the issue and press on, rather than throwing an error as before. Nothing short of `REINDEX` will fix the broken index, but preventing `VACUUM` from completing until that is done risks making matters far worse.
* Ensure that `WrapLimitsVacuumLock` is released after `VACUUM` detects invalid data in `pg_database`.`datfrozenxid` or `pg_database`.`datminmxid` (Andres Freund) [§](https://postgr.es/c/82e97b864)

  Failure to release this lock could lead to a deadlock later, although the lock would be cleaned up if the session exits or encounters some other error.
* Avoid double replay of prepared transactions during crash recovery (suyu.cmj, Michael Paquier) [§](https://postgr.es/c/a878eff6b) [§](https://postgr.es/c/f6ecd2622)

  After a crash partway through a checkpoint with some two-phase transaction state data already flushed to disk by this checkpoint, crash recovery could attempt to replay the prepared transaction(s) twice, leading to a fatal error such as “lock is already held” in the startup process.
* Ensure that a newly created, but still empty table is `fsync`'ed at the next checkpoint (Heikki Linnakangas) [§](https://postgr.es/c/e24c02e4d)

  Without this, if there is an operating system crash causing the empty file to disappear, subsequent operations on the table might fail with “could not open file” errors.
* Ensure that creation of the init fork of an unlogged index is WAL-logged (Heikki Linnakangas) [§](https://postgr.es/c/25624c5d3)

  While an unlogged index's main data fork is not WAL-logged, its init fork should be, to ensure that we have a consistent state to restore the index to after a crash. This step was missed if the init fork contains no data, which is a case not used by any standard index AM; but perhaps some extension behaves that way.
* Silence bogus “missing contrecord” errors (Thomas Munro) [§](https://postgr.es/c/f50200c01)

  Treat this case as plain end-of-WAL to avoid logging inaccurate complaints from pg_waldump and walsender.
* Fix overly strict assertion in `jsonpath` code (David Rowley) [§](https://postgr.es/c/67f3a697b)

  This assertion failed if a query applied the `.type()` operator to a `like_regex` result. There was no bug in non-assert builds.
* Avoid assertion failure when processing an empty statement via the extended query protocol in an already-aborted transaction (Tom Lane) [§](https://postgr.es/c/cb74f7bec)
* Avoid assertion failure when the `stats_fetch_consistency` setting is changed intra-transaction (Kyotaro Horiguchi) [§](https://postgr.es/c/ccd21e1cf)
* Fix `contrib/fuzzystrmatch`'s Soundex `difference()` function to handle empty input sanely (Alexander Lakhin, Tom Lane) [§](https://postgr.es/c/eaf99e4c4)

  An input string containing no alphabetic characters resulted in unpredictable output.
* Tighten whitespace checks in `contrib/hstore` input (Evan Jones) [§](https://postgr.es/c/3a5222a43)

  In some cases, characters would be falsely recognized as whitespace and hence discarded.
* Disallow oversize input arrays with `contrib/intarray`'s `gist__int_ops` index opclass (Ankit Kumar Pandey, Alexander Lakhin) [§](https://postgr.es/c/4be308ede)

  Previously this code would report a `NOTICE` but press on anyway, creating an invalid index entry that presents a risk of crashes when the index is read.
* Avoid useless double decompression of GiST index entries in `contrib/intarray` (Konstantin Knizhnik, Matthias van de Meent, Tom Lane) [§](https://postgr.es/c/5cb461989)
* Fix `contrib/pageinspect`'s `gist_page_items()` function to work when there are included index columns (Alexander Lakhin, Michael Paquier) [§](https://postgr.es/c/2dd778221)

  Previously, if the index has included columns, `gist_page_items()` would fail to display those values on index leaf pages, or crash outright on non-leaf pages.
* In psql, ignore the `PSQL_WATCH_PAGER` environment variable when stdin/stdout are not a terminal (Tom Lane) [§](https://postgr.es/c/bc478a0a8)

  This corresponds to the treatment of `PSQL_PAGER` in commands besides `\watch`.
* Fix pg_dump to correctly handle new-style SQL-language functions whose bodies require parse-time dependencies on unique indexes (Tom Lane) [§](https://postgr.es/c/ca9e79274)

  Such cases can arise from `GROUP BY` and `ON CONFLICT` clauses, for example. The function must then be postponed until after the unique index in the dump output, but pg_dump did not do that and instead printed a warning about “could not resolve dependency loop”.
* Improve pg_dump's display of details about dependency-loop problems (Tom Lane) [§](https://postgr.es/c/751ba1a7c)
* Avoid crash in pgbench with an empty pipeline and prepared mode (Álvaro Herrera) [§](https://postgr.es/c/34f511965)
* Ensure that `pg_index`.`indisreplident` is kept up-to-date in relation cache entries (Shruthi Gowda) [§](https://postgr.es/c/eb3abec4b)

  This value could be stale in some cases. There is no core code that relies on the relation cache's copy, so this is only a latent bug as far as Postgres itself is concerned; but there may be extensions for which it is a live bug.
* Fix make_etags script to work with non-Exuberant ctags (Masahiko Sawada) [§](https://postgr.es/c/af26f28b9)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-4.html)（英文原文，待翻譯）
