<a id="RELEASE-15-3"></a>

# E.17. Release 15.3

[E.17.1. Migration to Version 15.3](#id-1.11.6.22.4)

[E.17.2. Changes](#id-1.11.6.22.5)

<strong>Release date: </strong>2023-05-11

This release contains a variety of fixes from 15.2. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.22.4"></a>

## E.17.1. Migration to Version 15.3

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.1, see [Section E.19](e.2.-release-15.1.md).

<a id="id-1.11.6.22.5"></a>

## E.17.2. Changes

* Prevent `CREATE SCHEMA` from defeating changes in `search_path` (Alexander Lakhin) [§](https://postgr.es/c/dbd5795e7) [§](https://postgr.es/c/1b761d896)

  Within a `CREATE SCHEMA` command, objects in the prevailing `search_path`, as well as those in the newly-created schema, would be visible even within a called function or script that attempted to set a secure `search_path`. This could allow any user having permission to create a schema to hijack the privileges of a security definer function or extension script.

  The PostgreSQL Project thanks Alexander Lakhin for reporting this problem. (CVE-2023-2454)
* Enforce row-level security policies correctly after inlining a set-returning function (Stephen Frost, Tom Lane) [§](https://postgr.es/c/04e560604)

  If a set-returning SQL-language function refers to a table having row-level security policies, and it can be inlined into a calling query, those RLS policies would not get enforced properly in some cases involving re-using a cached plan under a different role. This could allow a user to see or modify rows that should have been invisible.

  The PostgreSQL Project thanks Wolfgang Walther for reporting this problem. (CVE-2023-2455)
* Fix potential corruption of the template (source) database after `CREATE DATABASE` with the `STRATEGY WAL_LOG` option (Nathan Bossart, Ryo Matsumura) [§](https://postgr.es/c/fa5dd460c)

  Improper buffer handling created a risk that any later modification of the template's `pg_class` catalog would be lost.
* Fix memory leakage and unnecessary disk reads during `CREATE DATABASE` with the `STRATEGY WAL_LOG` option (Andres Freund) [§](https://postgr.es/c/560bb56c6)
* Avoid crash when the new schema name is omitted in `CREATE SCHEMA` (Michael Paquier) [§](https://postgr.es/c/b9ad73ad2)

  The SQL standard allows writing <code class="literal">CREATE SCHEMA AUTHORIZATION <em class="replaceable"><code>owner&#95;name</code></em></code>, with the schema name defaulting to <em class="replaceable"><code>owner&#95;name</code></em>. However some code paths expected the schema name to be present and would fail.
* Fix various planner failures with `MERGE` commands (Tom Lane) [§](https://postgr.es/c/bf5c4b3d9) [§](https://postgr.es/c/3908d6ae1)

  Planning could fail with errors like “variable not found in subplan target list” or “PlaceHolderVar found where not expected”.
* Fix the row count reported by `MERGE` for some corner cases (Dean Rasheed) [§](https://postgr.es/c/da6257eee) [§](https://postgr.es/c/018af1cc1)

  The row count reported in the command tag counted rows that actually hadn't been modified due to a `BEFORE ROW` trigger returning NULL. This is inconsistent with what happens in plain `UPDATE` or `DELETE`, so change it to not count such rows. Also, avoid counting a row twice when `MERGE` moves it into a different partition of a partitioned table.
* Fix `MERGE` problems with concurrent updates (Dean Rasheed, Álvaro Herrera) [§](https://postgr.es/c/7d9a75713) [§](https://postgr.es/c/5d8ec1b9f)

  Some cases misbehaved if a row to be updated or deleted by `MERGE` had just been updated by a concurrent transaction. This could lead to a crash, or the wrong merge action being executed, or no action at all.
* Add support for decompiling `MERGE` commands (Álvaro Herrera) [§](https://postgr.es/c/f200b9695)

  This was overlooked when `MERGE` was added, but it's essential support for `MERGE` in new-style SQL functions.
* Fix enabling/disabling of foreign-key triggers in partitioned tables (Tom Lane) [§](https://postgr.es/c/f61e60102)

  `ALTER TABLE ... ENABLE/DISABLE TRIGGER` failed if applied to a partitioned table's foreign-key enforcement triggers, because it tried to locate the clone triggers for the partitions by name, and they do not have the same name. Locate them by parent-trigger OID instead.
* Disallow altering composite types that are stored in indexes (Tom Lane) [§](https://postgr.es/c/d90d59e25)

  `ALTER TYPE` disallows non-binary-compatible modifications of composite types if they are stored in any table columns. (Perhaps that will be allowed someday, but it hasn't happened yet; the locking implications of rewriting many tables are daunting.) We overlooked the possibility that an index might contain a composite type that doesn't also appear in its table.
* Disallow system columns as elements of foreign keys (Tom Lane) [§](https://postgr.es/c/6e3698173)

  Since the removal of OID as a system column, there is no plausible use-case for this, and various bits of code no longer support it. Disallow it rather than trying to fix all the cases.
* Ensure that `COPY TO` from an RLS-enabled parent table does not copy any rows from child tables (Antonin Houska) [§](https://postgr.es/c/59947bac7)

  The documentation is quite clear that `COPY TO` copies rows from only the named table, not any inheritance children it may have. However, if row-level security was enabled on the table then this stopped being true.
* Avoid possible crash when `array_position()` or `array_positions()` is passed an empty array (Tom Lane) [§](https://postgr.es/c/ccb479e76)
* Fix possible out-of-bounds fetch in `to_char()` (Tom Lane) [§](https://postgr.es/c/a67c75f82)

  With bad luck this could have resulted in a server crash.
* Avoid buffer overread in `translate()` function (Daniil Anisimov) [§](https://postgr.es/c/eae09137d)

  When using the deletion feature, the function might fetch the byte just after the input string, creating a small risk of crash.
* Adjust text-search-related character classification logic to correctly detect whether the prevailing locale is `C` (Jeff Davis) [§](https://postgr.es/c/8b87e9291)

  This code got confused if the database's default collation uses ICU.
* Avoid possible crash on empty input for type `interval` (Tom Lane) [§](https://postgr.es/c/0ef65d0f5)
* Re-allow exponential notation in ISO-8601 interval fields (Tom Lane) [§](https://postgr.es/c/ded5ede27)

  Interval input like `P0.1e10D` isn't officially sanctioned by ISO-8601, but we accepted it for a long time before version 15, so re-allow it.
* Fix error cursor setting for parse errors in JSON string literals (Tom Lane) [§](https://postgr.es/c/74a1a36d7)

  Most cases in which a syntax error is detected in a string literal within a JSON value failed to set the error cursor appropriately. This led at least to an unhelpful error message (pointing to the token before the string, rather than the actual trouble spot), and could even result in a crash in v14 and later.
* Fix data corruption due to `vacuum_defer_cleanup_age` being larger than the current 64-bit xid (Andres Freund) [§](https://postgr.es/c/391f08fd6)

  In v14 and later with non-default settings of `vacuum_defer_cleanup_age`, it was possible to compute a very large vacuum cleanup horizon xid, leading to vacuum removing rows that are still live. v12 and v13 have a lesser form of the same problem affecting only GiST indexes, which could lead to index pages getting recycled too early.
* Fix parser's failure to detect some cases of improperly-nested aggregates (Tom Lane) [§](https://postgr.es/c/5fd61bdc1)

  This oversight could lead to executor failures for queries that should have been rejected as invalid.
* Fix data structure corruption during parsing of serial `SEQUENCE NAME` options (David Rowley) [§](https://postgr.es/c/df567fbf6)

  This can lead to trouble if an event trigger captures the corrupted parse tree.
* Correctly update plan nodes' parallel-safety markings when moving initplans from one node to another (Tom Lane) [§](https://postgr.es/c/f4badbcf4)

  This planner oversight could lead to “subplan was not initialized” errors at runtime.
* Avoid failure with PlaceHolderVars in extended-statistics code (Tom Lane) [§](https://postgr.es/c/3b4594443)

  Use of dependency-type extended statistics could fail with “PlaceHolderVar found where not expected”.
* Fix incorrect tests for whether a qual clause applied to a subquery can be transformed into a window aggregate “run condition” within the subquery (David Rowley) [§](https://postgr.es/c/371e3daaa)

  A SubPlan within such a clause would cause assertion failures or incorrect answers, as would some other unusual cases.
* Disable the inverse-transition optimization for window aggregates when the call contains sub-SELECTs (David Rowley) [§](https://postgr.es/c/a9fa6d79a)

  This optimization requires that the aggregate's argument expressions have repeatable results, which might not hold for a sub-SELECT.
* Fix oversights in execution of nested `ARRAY[]` constructs (Alexander Lakhin, Tom Lane) [§](https://postgr.es/c/7c4873438)

  Correctly detect overflow of the total space needed for the result array, avoiding a possible crash due to undersized output allocation. Also ensure that any trailing padding space in the result array is zeroed; while leaving garbage there is harmless for most purposes, it can result in odd behavior later.
* Prevent crash when updating a field within an array-of-domain-over-composite-type column (Dmitry Dolgov) [§](https://postgr.es/c/c53ed26ea)
* Fix partition pruning logic for partitioning on boolean columns (David Rowley) [§](https://postgr.es/c/0c09160e1)

  Pruning with a condition like `boolcol IS NOT TRUE` was done incorrectly, leading to possibly not returning rows in which `boolcol` is NULL. Also, the rather unlikely case of partitioning on `NOT boolcol` was handled incorrectly.
* Fix race condition in per-batch cleanup during parallel hash join (Thomas Munro, Melanie Plageman) [§](https://postgr.es/c/c03c6e8cf)

  A crash was possible given unlucky timing and `parallel_leader_participation` = `off` (which is not the default).
* Recalculate `GENERATED` columns after an EvalPlanQual check (Tom Lane) [§](https://postgr.es/c/70ef50954)

  In `READ COMMITTED` isolation mode, the effects of a row update might need to get reapplied to a newer version of the row than the query found originally. If so, we need to recompute any `GENERATED` columns, in case they depend on columns that were changed by the concurrent update.
* Fix memory leak in Memoize plan execution (David Rowley) [§](https://postgr.es/c/8de4660a5)
* Fix buffer refcount leak when using batched inserts for a foreign table included in a partitioned tree (Alexander Pyhalov) [§](https://postgr.es/c/aa6177c88)
* Restore support for sub-millisecond `vacuum_cost_delay` settings (Thomas Munro) [§](https://postgr.es/c/d9c9c43af)
* Don't balance vacuum cost delay when a table has a per-relation `vacuum_cost_delay` setting of zero (Masahiko Sawada) [§](https://postgr.es/c/0319b306e)

  Delay balancing is supposed to be disabled whenever autovacuum is processing a table with a per-relation `vacuum_cost_delay` setting, but this was done only for positive settings, not zero.
* Fix corner-case crashes when columns have been added to the end of a view (Tom Lane) [§](https://postgr.es/c/76d2177fb)
* Repair rare failure of MULTIEXPR_SUBLINK subplans in partitioned updates (Andres Freund, Tom Lane) [§](https://postgr.es/c/a033f9165)

  Use of the syntax `INSERT ... ON CONFLICT DO UPDATE SET (c1, ...) = (SELECT ...)` with a partitioned target table could result in failure if any child table is dissimilar from the parent (for example, different physical column order). This typically manifested as failure of consistency checks in the executor; but a crash or incorrect data updates are also possible.
* Fix handling of `DEFAULT` markers within a multi-row `INSERT ... VALUES` query on a view that has a `DO ALSO INSERT ... SELECT` rule (Dean Rasheed) [§](https://postgr.es/c/940b54743)

  Such cases typically failed with “unrecognized node type” errors or assertion failures.
* Support references to `OLD` and `NEW` within subqueries in rule actions (Dean Rasheed, Tom Lane) [§](https://postgr.es/c/8e5b4e001)

  Such references are really lateral references, but the server could crash if the subquery wasn't explicitly marked with `LATERAL`. Arrange to do that implicitly when necessary.
* When decompiling a rule or SQL function body containing `INSERT`/`UPDATE`/`DELETE` within `WITH`, take care to print the correct alias for the target table (Tom Lane) [§](https://postgr.es/c/c8a5f1685)
* Fix glitches in `SERIALIZABLE READ ONLY` optimization (Thomas Munro) [§](https://postgr.es/c/055990904) [§](https://postgr.es/c/af397c6c2)

  Transactions already marked as “doomed” confused the safe-snapshot optimization for `SERIALIZABLE READ ONLY` transactions. The optimization was unnecessarily skipped in some cases. In other cases an assertion failure occurred (but there was no problem in non-assert builds).
* Avoid leaking cache callback slots in the `pgoutput` logical decoding plugin (Shi Yu) [§](https://postgr.es/c/cef1c9c0c)

  Multiple cycles of starting up and shutting down the plugin within a single session would eventually lead to an “out of relcache_callback_list slots” error.
* Avoid unnecessary calls to custom validators for index operator class options (Alexander Korotkov) [§](https://postgr.es/c/6e7361c85)

  This change fixes some cases where an unexpected error was thrown.
* Avoid useless work while scanning a multi-column BRIN index with multiple scan keys (Tomas Vondra) [§](https://postgr.es/c/305d89ad9)

  The existing code effectively considered only the last scan key while deciding whether a range matched, thus usually scanning more of the index than it needed to.
* Fix netmask handling in BRIN inet_minmax_multi_ops opclass (Tomas Vondra) [§](https://postgr.es/c/0c7726c28)

  This error triggered an assertion failure in assert-enabled builds, but is mostly harmless in production builds.
* Fix dereference of dangling pointer during buffering build of a GiST index (Alexander Lakhin) [§](https://postgr.es/c/2dc77adc7)

  This error seems to usually be harmless in production builds, as the fetched value is noncritical; but in principle it could cause a server crash.
* Ignore dropped columns and generated columns during logical replication of an update or delete action (Onder Kalaci, Shi Yu) [§](https://postgr.es/c/b6bf90edc) [§](https://postgr.es/c/3c12407f4)

  Replication with the `REPLICA IDENTITY FULL` option failed if the table contained such columns.
* Correct the name of the wait event for SLRU buffer I/O for commit timestamps (Alexander Lakhin) [§](https://postgr.es/c/d31dab9a5)

  This wait event is named `CommitTsBuffer` according to the documentation, but the code had it as `CommitTSBuffer`. Change the code to match the documentation, as that way is more consistent with the naming of related wait events.
* Re-activate reporting of wait event `SLRUFlushSync` (Thomas Munro) [§](https://postgr.es/c/1ed1b84bd)

  Reporting of this type of wait was accidentally removed in code refactoring.
* Avoid possible underflow when calculating how many WAL segments to keep (Kyotaro Horiguchi) [§](https://postgr.es/c/c98b06e2f)

  This could result in not honoring `wal_keep_size` accurately.
* Disable startup progress reporting overhead in standby mode (Bharath Rupireddy) [§](https://postgr.es/c/ecb01e6eb)

  In standby mode, we don't actually report progress of recovery, but we were doing work to track it anyway.
* Support RSA-PSS certificates with SCRAM-SHA-256 channel binding (Jacob Champion, Heikki Linnakangas) [§](https://postgr.es/c/5fd61055e)

  This feature requires building with OpenSSL 1.1.1 or newer. Both the server and libpq are affected.
* Avoid race condition with process ID tracking on Windows (Thomas Munro) [§](https://postgr.es/c/06066915d) [§](https://postgr.es/c/75e7378f6) [§](https://postgr.es/c/e8a774d00)

  The operating system could recycle a PID before the postmaster observed that that child process was gone. This could lead to tracking more than one child with the same PID, resulting in confusion.
* Fix `list_copy_head()` to work correctly on an empty List (David Rowley) [§](https://postgr.es/c/63a03aea6)

  This case is not known to be reached by any core PostgreSQL code, but extensions might rely on it working.
* Add missing cases to `SPI_result_code_string()` (Dean Rasheed) [§](https://postgr.es/c/576b25bfd)
* Fix erroneous Valgrind markings in `AllocSetRealloc()` (Karina Litskevich) [§](https://postgr.es/c/f6a55c1d5)

  In the unusual case where the size of a large (>8kB) palloc chunk is decreased, a Valgrind-aware build would mismark the defined-ness state of the memory released from the chunk, possibly causing incorrect results during Valgrind testing.
* Fix assertion failure for `MERGE` into a partitioned table with row-level security enabled (Dean Rasheed) [§](https://postgr.es/c/d8c3b65db)
* Avoid assertion failure when decoding a transactional logical replication message (Tomas Vondra) [§](https://postgr.es/c/949ac32e1)
* Avoid locale sensitivity when processing regular expression escapes (Jeff Davis) [§](https://postgr.es/c/109363de0)

  A backslash followed by a non-ASCII character could sometimes cause an assertion failure, depending on the prevailing locale.
* Avoid trying to write an empty WAL record in `log_newpage_range()` when the last few pages in the specified range are empty (Matthias van de Meent) [§](https://postgr.es/c/2207df7c3)

  It is not entirely clear whether this case is reachable in released branches, but if it is then an assertion failure could occur.
* Fix session-lifespan memory leakage in plpgsql `DO` blocks that use cast expressions (Ajit Awekar, Tom Lane) [§](https://postgr.es/c/c1598d85f)
* Tighten array dimensionality checks when converting Perl list structures to multi-dimensional SQL arrays (Tom Lane) [§](https://postgr.es/c/ce9a1a3ea)

  plperl could misbehave when the nesting of sub-lists is inconsistent so that the data does not represent a rectangular array of values. Such cases now produce errors, but previously they could result in a crash or garbage output.
* Tighten array dimensionality checks when converting Python list structures to multi-dimensional SQL arrays (Tom Lane) [§](https://postgr.es/c/b7001c6b6) [§](https://postgr.es/c/512c55522)

  plpython could misbehave when dealing with empty sub-lists, or when the nesting of sub-lists is inconsistent so that the data does not represent a rectangular array of values. The former should result in an empty output array, and the latter in an error. But some cases resulted in a crash, and others in unexpected output.
* Fix unwinding of exception stack in plpython (Xing Guo) [§](https://postgr.es/c/825ebc984)

  Some rare failure cases could return without cleaning up the PG_TRY exception stack, risking a crash if another error was raised before the next stack level was unwound.
* Fix inconsistent GSS-encryption error handling in libpq's `PQconnectPoll()` (Michael Paquier) [§](https://postgr.es/c/4493256c5)

  With `gssencmode` set to `require`, the connection was not marked dead after a GSS initialization failure. Make it fail immediately, as the equivalent case for TLS encryption has long done.
* Fix possible data corruption in ecpg programs built with the `-C ORACLE` option (Kyotaro Horiguchi) [§](https://postgr.es/c/8c746be44)

  When `ecpg_get_data()` is called with `varcharsize` set to zero, it could write a terminating zero character into the last byte of the preceding field, truncating the data in that field.
* Fix pg_dump so that partitioned tables that are hash-partitioned on an enum-type column can be restored successfully (Tom Lane) [§](https://postgr.es/c/2b216da1e)

  Since the hash codes for enum values depend on the OIDs assigned to the enum, they are typically different after a dump and restore, meaning that rows often need to go into a different partition than they were in originally. Users can work around that by specifying the `--load-via-partition-root` option; but since there is very little chance of success without that, teach pg_dump to apply it automatically to such tables.

  Also, fix pg_restore to not try to `TRUNCATE` target tables before restoring into them when `--load-via-partition-root` mode is used. This avoids a hazard of deadlocks and lost data.
* Correctly detect non-seekable files on Windows (Juan José Santamaría Flecha, Michael Paquier, Daniel Watzinger) [§](https://postgr.es/c/5c3254946) [§](https://postgr.es/c/69b6032e0)

  This bug led to misbehavior when pg_dump writes to a pipe or pg_restore reads from one.
* In pgbench's “prepared” mode, prepare all the commands in a pipeline before starting the pipeline (Álvaro Herrera) [§](https://postgr.es/c/108a22bd1)

  This avoids a failure when a pgbench script tries to start a serializable transaction inside a pipeline.
* In `contrib/amcheck`'s heap checking code, deal correctly with tuples having zero xmin or xmax (Robert Haas) [§](https://postgr.es/c/701ec5557) [§](https://postgr.es/c/453f53821)
* In `contrib/amcheck`, deal sanely with xids that appear to be before epoch zero (Andres Freund) [§](https://postgr.es/c/e8a9750d0)

  In cases of corruption we might see a wrapped-around 32-bit xid that appears to be before the first xid epoch. Promoting such a value to 64-bit form produced a value far in the future, resulting in wrong reports. Return FirstNormalFullTransactionId in such cases so that things work reasonably sanely.
* In `contrib/basebackup_to_shell`, properly detect failure to open a pipe (Robert Haas) [§](https://postgr.es/c/fa83e9e23)
* In `contrib/hstore_plpython`, avoid crashing if the Python value to be transformed isn't a mapping (Dmitry Dolgov, Tom Lane) [§](https://postgr.es/c/85ec8bcce)

  This should give an error, but Python 3 changed some APIs in a way that caused the check to misbehave, allowing a crash to ensue.
* Require the `siglen` option of a GiST index on an `ltree` column, if specified, to be a multiple of 4 (Alexander Korotkov) [§](https://postgr.es/c/214495dc5)

  Other values result in misaligned accesses to index content, which is harmless on Intel-compatible hardware but can cause a crash on some other architectures.
* In `contrib/pageinspect`, add defenses against incorrect input for the `gist_page_items()` function (Dmitry Koval) [§](https://postgr.es/c/9d41ecfcd)
* Fix misbehavior in `contrib/pg_trgm` with an unsatisfiable regular expression (Tom Lane) [§](https://postgr.es/c/6170386c7)

  A regex such as `$foo` is legal but unsatisfiable; the regex compiler recognizes that and produces an empty NFA graph. Attempting to optimize such a graph into a pg_trgm GIN or GiST index qualification resulted in accessing off the end of a work array, possibly leading to crashes.
* Fix handling of escape sequences in `contrib/postgres_fdw`'s `application_name` parameter (Kyotaro Horiguchi, Michael Paquier) [§](https://postgr.es/c/5bace41ab)

  The code to expand these could fail if executed in a background process, as for example during auto-analyze of a foreign table.
* In `contrib/pg_walinspect`, limit memory usage of `pg_get_wal_records_info()` (Bharath Rupireddy) [§](https://postgr.es/c/da32a99df)
* Use the `--strip-unneeded` option when stripping static libraries with GNU-compatible strip (Tom Lane) [§](https://postgr.es/c/a14afd3bd)

  Previously, `make install-strip` used the `-x` option in this case. This change avoids misbehavior of llvm-strip, and gives slightly smaller output as well.
* Stop recommending auto-download of DTD files for building the documentation, and indeed disable it (Aleksander Alekseev, Peter Eisentraut, Tom Lane) [§](https://postgr.es/c/2ee703c9d)

  It appears no longer possible to build the SGML documentation without a local installation of the DocBook DTD files. Formerly xsltproc could download those files on-the-fly from sourceforge.net; but sourceforge.net now permits only HTTPS access, and no common version of xsltproc supports that. Hence, remove the bits of our documentation suggesting that that's possible or useful, and instead add xsltproc's `--nonet` option to the build recipes.
* When running TAP tests in PGXS builds, use a saner location for the temporary `portlock` directory (Peter Eisentraut) [§](https://postgr.es/c/3d37476f5)

  Place it under `tmp_check` in the build directory. With the previous coding, a PGXS build would try to place it in the installation directory, which is not necessarily writable.
* Update time zone data files to tzdata release 2023c for DST law changes in Egypt, Greenland, Morocco, and Palestine. (Tom Lane) [§](https://postgr.es/c/62b22caa5)

  When observing Moscow time, Europe/Kirov and Europe/Volgograd now use the abbreviations MSK/MSD instead of numeric abbreviations, for consistency with other timezones observing Moscow time. Also, America/Yellowknife is no longer distinct from America/Edmonton; this affects some pre-1948 timestamps in that area.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-3.html)（英文原文，待翻譯）
