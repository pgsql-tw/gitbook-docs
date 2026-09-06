<a id="RELEASE-15-7"></a>

# E.13. Release 15.7

[E.13.1. Migration to Version 15.7](#id-1.11.6.18.4)

[E.13.2. Changes](#id-1.11.6.18.5)

<strong>Release date: </strong>2024-05-09

This release contains a variety of fixes from 15.6. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.18.4"></a>

## E.13.1. Migration to Version 15.7

A dump/restore is not required for those running 15.X.

However, a security vulnerability was found in the system views `pg_stats_ext` and `pg_stats_ext_exprs`, potentially allowing authenticated database users to see data they shouldn't. If this is of concern in your installation, follow the steps in the first changelog entry below to rectify it.

Also, if you are upgrading from a version earlier than 15.6, see [Section E.14](release-15-6.md).

<a id="id-1.11.6.18.5"></a>

## E.13.2. Changes

* Restrict visibility of `pg_stats_ext` and `pg_stats_ext_exprs` entries to the table owner (Nathan Bossart) [§](https://postgr.es/c/9cc2b6289)

  These views failed to hide statistics for expressions that involve columns the accessing user does not have permission to read. View columns such as `most_common_vals` might expose security-relevant data. The potential interactions here are not fully clear, so in the interest of erring on the side of safety, make rows in these views visible only to the owner of the associated table.

  The PostgreSQL Project thanks Lukas Fittl for reporting this problem. (CVE-2024-4317)

  By itself, this fix will only fix the behavior in newly initdb'd database clusters. If you wish to apply this change in an existing cluster, you will need to do the following:

  1. Find the SQL script `fix-CVE-2024-4317.sql` in the <em class="replaceable"><code>share</code></em> directory of the PostgreSQL installation (typically located someplace like `/usr/share/postgresql/`). Be sure to use the script appropriate to your PostgreSQL major version. If you do not see this file, either your version is not vulnerable (only v14–v16 are affected) or your minor version is too old to have the fix.
  2. In <em>each</em> database of the cluster, run the `fix-CVE-2024-4317.sql` script as superuser. In psql this would look like

     ```

     \i /usr/share/postgresql/fix-CVE-2024-4317.sql
     ```

     (adjust the file path as appropriate). Any error probably indicates that you've used the wrong script version. It will not hurt to run the script more than once.
  3. Do not forget to include the `template0` and `template1` databases, or the vulnerability will still exist in databases you create later. To fix `template0`, you'll need to temporarily make it accept connections. Do that with

     ```

     ALTER DATABASE template0 WITH ALLOW_CONNECTIONS true;
     ```

     and then after fixing `template0`, undo it with

     ```

     ALTER DATABASE template0 WITH ALLOW_CONNECTIONS false;
     ```
* Fix `INSERT` from multiple `VALUES` rows into a target column that is a domain over an array or composite type (Tom Lane) [§](https://postgr.es/c/7c61d2342)

  Such cases would either fail with surprising complaints about mismatched datatypes, or insert unexpected coercions that could lead to odd results.
* Require `SELECT` privilege on the target table for `MERGE` with a `DO NOTHING` clause (Álvaro Herrera) [§](https://postgr.es/c/90ad85db6)

  `SELECT` privilege would be required in all practical cases anyway, but require it even if the query reads no columns of the target table. This avoids an edge case in which `MERGE` would require no privileges whatever, which seems undesirable even when it's a do-nothing command.
* Fix handling of self-modified tuples in `MERGE` (Dean Rasheed) [§](https://postgr.es/c/b5c645d2a)

  Throw an error if a target row joins to more than one source row, as required by the SQL standard. (The previous coding could silently ignore this condition if a concurrent update was involved.) Also, throw a non-misleading error if a target row is already updated by a later command in the current transaction, thanks to a `BEFORE` trigger or a volatile function used in the query.
* Fix incorrect pruning of NULL partition when a table is partitioned on a boolean column and the query has a boolean `IS NOT` clause (David Rowley) [§](https://postgr.es/c/1b3495e29)

  A NULL value satisfies a clause such as <code class="literal"><em class="replaceable"><code>boolcol</code></em> IS NOT FALSE</code>, so pruning away a partition containing NULLs yielded incorrect answers.
* Make `ALTER FOREIGN TABLE SET SCHEMA` move any owned sequences into the new schema (Tom Lane) [§](https://postgr.es/c/b48eda4e5)

  Moving a regular table to a new schema causes any sequences owned by the table to be moved to that schema too (along with indexes and constraints). This was overlooked for foreign tables, however.
* Make `ALTER TABLE ... ADD COLUMN` create identity/serial sequences with the same persistence as their owning tables (Peter Eisentraut) [§](https://postgr.es/c/d17a3a4c6)

  `CREATE UNLOGGED TABLE` will make any owned sequences be unlogged too. `ALTER TABLE` missed that consideration, so that an added identity column would have a logged sequence, which seems pointless.
* Improve `ALTER TABLE ... ALTER COLUMN TYPE`'s error message when there is a dependent function or publication (Tom Lane) [§](https://postgr.es/c/5f4a1a0a7) [§](https://postgr.es/c/9b41d1d63)
* In `CREATE DATABASE`, recognize strategy keywords case-insensitively for consistency with other options (Tomas Vondra) [§](https://postgr.es/c/276b7888f)
* Fix `EXPLAIN`'s counting of heap pages accessed by a bitmap heap scan (Melanie Plageman) [§](https://postgr.es/c/d3d95f583)

  Previously, heap pages that contain no visible tuples were not counted; but it seems more consistent to count all pages returned by the bitmap index scan.
* Fix `EXPLAIN`'s output for subplans in `MERGE` (Dean Rasheed) [§](https://postgr.es/c/89ee14a2f)

  `EXPLAIN` would sometimes fail to properly display subplan Params referencing variables in other parts of the plan tree.
* Avoid deadlock during removal of orphaned temporary tables (Mikhail Zhilin) [§](https://postgr.es/c/4fb56a734)

  If the session that creates a temporary table crashes without removing the table, autovacuum will eventually try to remove the orphaned table. However, an incoming session that's been assigned the same temporary namespace will do that too. If a temporary table has a dependency (such as an owned sequence) then a deadlock could result between these two cleanup attempts.
* Avoid race condition while examining per-relation frozen-XID values (Noah Misch) [§](https://postgr.es/c/7c5915c4b)

  `VACUUM`'s computation of per-database frozen-XID values from per-relation values could get confused by a concurrent update of those values by another `VACUUM`.
* Fix buffer usage reporting for parallel vacuuming (Anthonin Bonnefoy) [§](https://postgr.es/c/faba2f8f3)

  Buffer accesses performed by parallel workers were not getting counted in the statistics reported in `VERBOSE` mode.
* Disallow converting a table to a view within an outer SQL command that is using that table (Tom Lane) [§](https://postgr.es/c/bf379b555)

  This avoids possible crashes.
* Ensure that join conditions generated from equivalence classes are applied at the correct plan level (Tom Lane) [§](https://postgr.es/c/5aacfa64e)

  In versions before PostgreSQL 16, it was possible for generated conditions to be evaluated below outer joins when they should be evaluated above (after) the outer join, leading to incorrect query results. All versions have a similar hazard when considering joins to `UNION ALL` trees that have constant outputs for the join column in some `SELECT` arms.
* Prevent potentially-incorrect optimization of some window functions (David Rowley) [§](https://postgr.es/c/7e5d20bbd)

  Disable “run condition” optimization of `ntile()` and `count()` with non-constant arguments. This avoids possible misbehavior with sub-selects, typically leading to errors like “WindowFunc not found in subplan target lists”.
* Avoid unnecessary use of moving-aggregate mode with a non-moving window frame (Vallimaharajan G) [§](https://postgr.es/c/03561a6c7)

  When a plain aggregate is used as a window function, and the window frame start is specified as `UNBOUNDED PRECEDING`, the frame's head cannot move so we do not need to use the special (and more expensive) moving-aggregate mode. This optimization was intended all along, but due to a coding error it never triggered.
* Avoid use of already-freed data while planning partition-wise joins under GEQO (Tom Lane) [§](https://postgr.es/c/37bbe3d3a)

  This would typically end in a crash or unexpected error message.
* Avoid freeing still-in-use data in Memoize (Tender Wang, Andrei Lepikhov) [§](https://postgr.es/c/74530804f)

  In production builds this error frequently didn't cause any problems, as the freed data would most likely not get overwritten before it was used.
* Fix incorrectly-reported statistics kind codes in “requested statistics kind <em class="replaceable"><code>X</code></em> is not yet built” error messages (David Rowley) [§](https://postgr.es/c/164fe7a6e)
* Be more careful with `RECORD`-returning functions in `FROM` (Tom Lane) [§](https://postgr.es/c/09989ba84) [§](https://postgr.es/c/3b671dcf5)

  The output columns of such a function call must be defined by an `AS` clause that specifies the column names and data types. If the actual function output value doesn't match that, an error is supposed to be thrown at runtime. However, some code paths would examine the actual value prematurely, and potentially issue strange errors or suffer assertion failures if it doesn't match expectations.
* Fix confusion about the return rowtype of SQL-language procedures (Tom Lane) [§](https://postgr.es/c/6f66fadad)

  A procedure implemented in SQL language that returns a single composite-type column would cause an assertion failure or core dump.
* Add protective stack depth checks to some recursive functions (Egor Chindyaskin) [§](https://postgr.es/c/84788ee5b)
* Fix mis-rounding and overflow hazards in `date_bin()` (Moaaz Assali) [§](https://postgr.es/c/db8855b66)

  In the case where the source timestamp is before the origin timestamp and their difference is already an exact multiple of the stride, the code incorrectly subtracted the stride anyway. Also, detect some integer-overflow cases that would have produced incorrect results.
* Detect integer overflow when adding or subtracting an `interval` to/from a `timestamp` (Joseph Koshakow) [§](https://postgr.es/c/e6e3ee5b7)

  Some cases that should cause an out-of-range error produced an incorrect result instead.
* Avoid race condition in `pg_get_expr()` (Tom Lane) [§](https://postgr.es/c/26c89d105)

  If the relation referenced by the argument is dropped concurrently, the function's intention is to return NULL, but sometimes it failed instead.
* Fix detection of old transaction IDs in XID status functions (Karina Litskevich) [§](https://postgr.es/c/503299b7f)

  Transaction IDs more than 2<sup>31</sup> transactions in the past could be misidentified as recent, leading to misbehavior of `pg_xact_status()` or `txid_status()`.
* Ensure that a table's freespace map won't return a page that's past the end of the table (Ronan Dunklau) [§](https://postgr.es/c/7c490a18b)

  Because the freespace map isn't WAL-logged, this was possible in edge cases involving an OS crash, a replica promote, or a PITR restore. The result would be a “could not read block” error.
* Fix file descriptor leakage when an error is thrown while waiting in `WaitEventSetWait` (Etsuro Fujita) [§](https://postgr.es/c/b82dca2a5)
* Avoid corrupting exception stack if an FDW implements async append but doesn't configure any wait conditions for the Append plan node to wait for (Alexander Pyhalov) [§](https://postgr.es/c/3f96d113f)
* Throw an error if an index is accessed while it is being reindexed (Tom Lane) [§](https://postgr.es/c/940489b46)

  Previously this was just an assertion check, but promote it into a regular runtime error. This will provide a more on-point error message when reindexing a user-defined index expression that attempts to access its own table.
* Ensure that index-only scans on `name` columns return a fully-padded value (David Rowley) [§](https://postgr.es/c/52f21f928)

  The value physically stored in the index is truncated, and previously a pointer to that value was returned to callers. This provoked complaints when testing under valgrind. In theory it could result in crashes, though none have been reported.
* Fix race condition in deciding whether a table sync operation is needed in logical replication (Vignesh C) [§](https://postgr.es/c/28a8cc457)

  An invalidation event arriving while a subscriber identifies which tables need to be synced would be forgotten about, so that any tables newly in need of syncing might not get processed in a timely fashion.
* Fix crash with DSM allocations larger than 4GB (Heikki Linnakangas) [§](https://postgr.es/c/d46c26961)
* Disconnect if a new server session's client socket cannot be put into non-blocking mode (Heikki Linnakangas) [§](https://postgr.es/c/4fce5f970)

  It was once theoretically possible for us to operate with a socket that's in blocking mode; but that hasn't worked fully in a long time, so fail at connection start rather than misbehave later.
* Fix inadequate error reporting with OpenSSL 3.0.0 and later (Heikki Linnakangas, Tom Lane) [§](https://postgr.es/c/0fe82e45c)

  System-reported errors passed through by OpenSSL were reported with a numeric error code rather than anything readable.
* Avoid concurrent calls to `bindtextdomain()` in libpq and ecpglib (Tom Lane) [§](https://postgr.es/c/806f98951) [§](https://postgr.es/c/9f041b041)

  Although GNU gettext's implementation seems to be fine with concurrent calls, the version available on Windows is not.
* Fix crash in ecpg's preprocessor if the program tries to redefine a macro that was defined on the preprocessor command line (Tom Lane) [§](https://postgr.es/c/25f937217) [§](https://postgr.es/c/1e7b1b026) [§](https://postgr.es/c/f7e891748)
* In ecpg, avoid issuing false “unsupported feature will be passed to server” warnings (Tom Lane) [§](https://postgr.es/c/f159f1814)
* Ensure that the string result of ecpg's `intoasc()` function is correctly zero-terminated (Oleg Tselebrovskiy) [§](https://postgr.es/c/b5cb6022b)
* In psql, avoid leaking a query result after the query is cancelled (Tom Lane) [§](https://postgr.es/c/4f1d33d70)

  This happened only when cancelling a non-last query in a query string made with `\;` separators.
* Fix pg_dumpall so that role comments, if present, will be dumped regardless of the setting of `--no-role-passwords` (Daniel Gustafsson, Álvaro Herrera) [§](https://postgr.es/c/12128be62)
* Skip files named `.DS_Store` in pg_basebackup, pg_checksums, and pg_rewind (Daniel Gustafsson) [§](https://postgr.es/c/29f005238)

  This avoids problems on macOS, where the Finder may create such files.
* Fix PL/pgSQL's parsing of single-line comments (`--`-style comments) following expressions (Erik Wienhold, Tom Lane) [§](https://postgr.es/c/d85db0a8e)

  This mistake caused parse errors if such a comment followed a `WHEN` expression in a PL/pgSQL `CASE` statement.
* In `contrib/amcheck`, don't report false match failures due to short- versus long-header values (Andrey Borodin, Michael Zhilin) [§](https://postgr.es/c/0d466bce9) [§](https://postgr.es/c/54e6184db)

  A variable-length datum in a heap tuple or index tuple could have either a short or a long header, depending on compression parameters that applied when it was made. Treat these cases as equivalent rather than complaining if there's a difference.
* Fix bugs in BRIN output functions (Tomas Vondra) [§](https://postgr.es/c/3cd413511)

  These output functions are only used for displaying index entries in `contrib/pageinspect`, so the errors are of limited practical concern.
* In `contrib/postgres_fdw`, avoid emitting requests to sort by a constant (David Rowley) [§](https://postgr.es/c/ab64b275a)

  This could occur in cases involving `UNION ALL` with constant-emitting subqueries. Sorting by a constant is useless of course, but it also risks being misinterpreted by the remote server, leading to “ORDER BY position <em class="replaceable"><code>N</code></em> is not in select list” errors.
* Make `contrib/postgres_fdw` set the remote session's time zone to `GMT` not `UTC` (Tom Lane) [§](https://postgr.es/c/6c85e3359)

  This should have the same results for practical purposes. However, `GMT` is recognized by hard-wired code in the server, while `UTC` is looked up in the timezone database. So the old code could fail in the unlikely event that the remote server's timezone database is missing entries.
* In `contrib/xml2`, avoid use of library functions that have been deprecated in recent versions of libxml2 (Dmitry Koval) [§](https://postgr.es/c/689ba4f1c)
* Fix incompatibility with LLVM 18 (Thomas Munro, Dmitry Dolgov) [§](https://postgr.es/c/74992929a)
* Allow `make check` to work with the musl C library (Thomas Munro, Bruce Momjian, Tom Lane) [§](https://postgr.es/c/3c3f4fd74)

---

原文：[PostgreSQL 15.19 Documentation](release-15-7.md)（英文原文，待翻譯）
