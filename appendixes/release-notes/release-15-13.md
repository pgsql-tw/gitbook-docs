<a id="RELEASE-15-13"></a>

# E.7. Release 15.13

[E.7.1. Migration to Version 15.13](#id-1.11.6.12.4)

[E.7.2. Changes](#id-1.11.6.12.5)

<strong>Release date: </strong>2025-05-08

This release contains a variety of fixes from 15.12. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.12.4"></a>

## E.7.1. Migration to Version 15.13

A dump/restore is not required for those running 15.X.

However, if you have any self-referential foreign key constraints on partitioned tables, it may be necessary to recreate those constraints to ensure that they are being enforced correctly. See the second changelog entry below.

Also, if you have any BRIN bloom indexes, it may be advisable to reindex them after updating. See the third changelog entry below.

Also, if you are upgrading from a version earlier than 15.9, see [Section E.11](release-15-9.md).

<a id="id-1.11.6.12.5"></a>

## E.7.2. Changes

* Avoid one-byte buffer overread when examining invalidly-encoded strings that are claimed to be in GB18030 encoding (Noah Misch, Andres Freund) [§](https://postgr.es/c/44ba3f55f) [§](https://postgr.es/c/45fe7e08f)

  While unlikely, a SIGSEGV crash could occur if an incomplete multibyte character appeared at the end of memory. This was possible both in the server and in libpq-using applications. (CVE-2025-4207)
* Handle self-referential foreign keys on partitioned tables correctly (Álvaro Herrera) [§](https://postgr.es/c/6ba979cf5)

  Creating or attaching partitions failed to make the required catalog entries for a foreign-key constraint, if the table referenced by the constraint was the same partitioned table. This resulted in failure to enforce the constraint fully.

  To fix this, you should drop and recreate any self-referential foreign keys on partitioned tables, if partitions have been created or attached since the constraint was created. Bear in mind that violating rows might already be present, in which case recreating the constraint will fail, and you'll need to fix up those rows before trying again.
* Avoid data loss when merging compressed BRIN summaries in `brin_bloom_union()` (Tomas Vondra) [§](https://postgr.es/c/e064b770c)

  The code failed to account for decompression results not being identical to the input objects, which would result in failure to add some of the data to the merged summary, leading to missed rows in index searches.

  This mistake was present back to v14 where BRIN bloom indexes were introduced, but this code path was only rarely reached then. It's substantially more likely to be hit in v17 because parallel index builds now use the code.
* Fix unexpected “attribute has wrong type” errors in `UPDATE`, `DELETE`, and `MERGE` queries that use whole-row table references to views or functions in `FROM` (Tom Lane) [§](https://postgr.es/c/ae0be2f0b) [§](https://postgr.es/c/317aba70e) [§](https://postgr.es/c/7713f4592)
* Fix `MERGE` into a partitioned table with `DO NOTHING` actions (Tender Wang) [§](https://postgr.es/c/14a33d3f0)

  Some cases failed with “unknown action in MERGE WHEN clause” errors.
* Prevent failure in `INSERT` commands when the table has a `GENERATED` column of a domain data type and the domain's constraints disallow null values (Jian He) [§](https://postgr.es/c/97d671672)

  Constraint failure was reported even if the generation expression produced a perfectly okay result.
* Correctly process references to outer CTE names that appear within a `WITH` clause attached to an `INSERT`/`UPDATE`/`DELETE`/`MERGE` command that's inside `WITH` (Tom Lane) [§](https://postgr.es/c/ede29a1e4)

  The parser failed to detect disallowed recursion cases, nor did it account for such references when sorting CTEs into a usable order.
* Fix <code class="literal">ARRAY(<em class="replaceable"><code>subquery</code></em>)</code> and <code class="literal">ARRAY&#91;<em class="replaceable"><code>expression, ...</code></em>&#93;</code> constructs to produce sane results when the input is of type `int2vector` or `oidvector` (Tom Lane) [§](https://postgr.es/c/13dd6f772)

  This patch restores the behavior that existed before PostgreSQL 9.5: the result is of type `int2vector[]` or `oidvector[]`.
* Fix possible erroneous reports of invalid affixes while parsing Ispell dictionaries (Jacob Brazeal) [§](https://postgr.es/c/e2921c0e9)
* Fix `ALTER TABLE ADD COLUMN` to correctly handle the case of a domain type that has a default (Jian He, Tom Lane, Tender Wang) [§](https://postgr.es/c/1d180931c) [§](https://postgr.es/c/2d6cfb0cd)

  If a domain type has a default, adding a column of that type (without any explicit `DEFAULT` clause) failed to install the domain's default value in existing rows, instead leaving the new column null.
* Repair misbehavior when there are duplicate column names in a foreign key constraint's `ON DELETE SET DEFAULT` or `SET NULL` action (Tom Lane) [§](https://postgr.es/c/f5069f026)
* Improve the error message for disallowed attempts to alter the properties of a foreign key constraint (Álvaro Herrera) [§](https://postgr.es/c/bf1e2d2db)
* Avoid error when resetting the `relhassubclass` flag of a temporary table that's marked `ON COMMIT DELETE ROWS` (Noah Misch) [§](https://postgr.es/c/e0f53e669)
* Fix planner's failure to identify more than one hashable ScalarArrayOpExpr subexpression within a top-level expression (David Geier) [§](https://postgr.es/c/a7f213b11)

  This resulted in unnecessarily-inefficient execution of any additional subexpressions that could have been processed with a hash table (that is, `IN`, `NOT IN`, or `= ANY` clauses with all-constant right-hand sides).
* Disable “skip fetch” optimization in bitmap heap scan (Matthias van de Meent) [§](https://postgr.es/c/77d90d6d6)

  It turns out that this optimization can result in returning dead tuples when a concurrent vacuum marks a page all-visible.
* Fix performance issues in GIN index search startup when there are many search keys (Tom Lane, Vinod Sridharan) [§](https://postgr.es/c/2d313375c) [§](https://postgr.es/c/9a8c16aec)

  An indexable clause with many keys (for example, `jsonbcol ?| array[...]` with tens of thousands of array elements) took O(N<sup>2</sup>) time to start up, and was uncancelable for that interval too.
* Detect missing support procedures in a BRIN index operator class, and report an error instead of crashing (Álvaro Herrera) [§](https://postgr.es/c/5d8c58800)
* Respond to interrupts (such as query cancel) while waiting for asynchronous subplans of an Append plan node (Heikki Linnakangas) [§](https://postgr.es/c/d4d34c08c)

  Previously, nothing would happen until one of the subplans becomes ready.
* Fix race condition in handling of `synchronous_standby_names` immediately after startup (Melnikov Maksim, Michael Paquier) [§](https://postgr.es/c/ec59500a1)

  For a short period after system startup, backends might fail to wait for synchronous commit even though `synchronous_standby_names` is enabled.
* Fix `pg_strtof()` to not crash with null endptr (Alexander Lakhin, Tom Lane) [§](https://postgr.es/c/c7303f01c)
* Avoid crash when a Snowball stemmer encounters an out-of-memory condition (Maksim Korotkov) [§](https://postgr.es/c/9c46d902b)
* Prevent over-advancement of catalog xmin in “fast forward” mode of logical decoding (Zhijie Hou) [§](https://postgr.es/c/f6429bd7d)

  This mistake could allow deleted catalog entries to be vacuumed away even though they were still potentially needed by the WAL-reading process.
* Avoid data loss when DDL operations that don't take a strong lock affect tables that are being logically replicated (Shlok Kyal, Hayato Kuroda) [§](https://postgr.es/c/9f21be08e) [§](https://postgr.es/c/90bc4523f)

  The catalog changes caused by the DDL command were not reflected into WAL-decoding processes, allowing them to decode subsequent changes using stale catalog data, probably resulting in data corruption.
* Avoid duplicate snapshot creation in logical replication index lookups (Heikki Linnakangas) [§](https://postgr.es/c/50c589992) [§](https://postgr.es/c/d765226cb)
* Fix wrong checkpoint details in error message about incorrect recovery timeline choice (David Steele) [§](https://postgr.es/c/62bed7bb0)

  If the requested recovery timeline is not reachable, the reported checkpoint and timeline should be the values read from the backup_label, if there is one. This message previously reported values from the control file, which is correct when recovering from the control file without a backup_label, but not when there is a backup_label.
* Fix assertion failure in snapshot building (Masahiko Sawada) [§](https://postgr.es/c/0f404c581)
* Remove incorrect assertion in `pgstat_report_stat()` (Michael Paquier) [§](https://postgr.es/c/c1201ffcf)
* Fix overly-strict assertion in `gistFindCorrectParent()` (Heikki Linnakangas) [§](https://postgr.es/c/3c0fe75c4)
* Fix rare assertion failure in standby servers when the primary is restarted (Heikki Linnakangas) [§](https://postgr.es/c/b30c77a0e)
* In PL/pgSQL, avoid “unexpected plan node type” error when a scrollable cursor is defined on a simple <code class="literal">SELECT <em class="replaceable"><code>expression</code></em></code> query (Andrei Lepikhov) [§](https://postgr.es/c/5e56efa7c)
* Don't try to drop individual index partitions in pg_dump's `--clean` mode (Jian He) [§](https://postgr.es/c/7144cd538)

  The server rejects such `DROP` commands. That has no real consequences, since the partitions will go away anyway in the subsequent `DROP`s of either their parent tables or their partitioned index. However, the error reported for the attempted drop causes problems when restoring in `--single-transaction` mode.
* In pg_dumpall, avoid emitting invalid role `GRANT` commands if `pg_auth_members` contains invalid role OIDs (Tom Lane) [§](https://postgr.es/c/6df3be415)

  Instead, print a warning and skip the entry. This copes better with catalog corruption that has been seen to occur in back branches as a result of race conditions between `GRANT` and `DROP ROLE`.
* In pg_amcheck and pg_upgrade, use the correct function to free allocations made by libpq (Michael Paquier, Ranier Vilela) [§](https://postgr.es/c/ec741d480)

  These oversights could result in crashes in certain Windows build configurations, such as a debug build of libpq used by a non-debug build of the calling application.
* Allow `contrib/dblink` queries to be interrupted by query cancel (Noah Misch) [§](https://postgr.es/c/63f6ecb6b) [§](https://postgr.es/c/9e129a224)

  This change back-patches a v17-era fix. It prevents possible hangs in `CREATE DATABASE` and `DROP DATABASE` due to failure to detect deadlocks.
* Avoid crashing with corrupt input data in `contrib/pageinspect`'s `heap_page_items()` (Dmitry Kovalenko) [§](https://postgr.es/c/90a3fd811)
* Prevent assertion failure in `contrib/pg_freespacemap`'s `pg_freespacemap()` (Tender Wang) [§](https://postgr.es/c/0e86bad38)

  Applying `pg_freespacemap()` to a relation lacking storage (such as a view) caused an assertion failure, although there was no ill effect in non-assert builds. Add an error check to reject that case.
* Fix build failure on macOS 15.4 (Tom Lane, Peter Eisentraut) [§](https://postgr.es/c/0de9560ba)

  This macOS update broke our configuration probe for `strchrnul()`.
* Update time zone data files to tzdata release 2025b for DST law changes in Chile, plus historical corrections for Iran (Tom Lane) [§](https://postgr.es/c/a144cf145)

  There is a new time zone America/Coyhaique for Chile's Aysén Region, to account for it changing to UTC-03 year-round and thus diverging from America/Santiago.

---

原文：[PostgreSQL 15.19 Documentation](release-15-13.md)（英文原文，待翻譯）
