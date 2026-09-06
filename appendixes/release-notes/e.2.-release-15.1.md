# E.2. Release 15.1

**Release date:** 2022-11-10

This release contains a variety of fixes from 15.0. For information about new features in major release 15, see [Section E.3](https://www.postgresql.org/docs/15/release-15.html).

## E.2.1. Migration to Version 15.1

A dump/restore is not required for those running 15.X.

However, if you regularly create and drop tables exceeding 1GB, see the first changelog entry below.

## E.2.2. Changes

*   Fix failure to remove non-first segments of large tables (Tom Lane)

    PostgreSQL splits large tables into multiple files (normally with 1GB per file). The logic for dropping a table was broken and would miss removing all but the first such file, in two cases: drops of temporary tables and WAL replay of drops of regular tables. Applications that routinely create multi-gigabyte temporary tables could suffer significant disk space leakage.

    Orphaned temporary-table files are removed during postmaster start, so the mere act of updating to 15.1 is sufficient to clear any leaked temporary-table storage. However, if you suffered any database crashes while using 15.0, and there might have been large tables dropped just before such crashes, it's advisable to check the database directories for files named according to the pattern _`NNNN`_`.`_`NN`_. If there is no matching file named just _`NNNN`_ (without the `.`_`NN`_ suffix), these files should be removed manually.
*   Fix handling of `DEFAULT` tokens that appear in a multi-row `VALUES` clause of an `INSERT` on an updatable view (Tom Lane)

    This oversight could lead to “cache lookup failed for type” errors, or in older branches even to crashes.
*   Disallow rules named `_RETURN` that are not `ON SELECT` (Tom Lane)

    This avoids confusion between a view's `ON SELECT` rule and any other rules it may have.
* Avoid failure in `EXPLAIN VERBOSE` for a query using `SEARCH BREADTH FIRST` with constant initial values (Tom Lane)
*   Prevent use of `MERGE` on a partitioned table with foreign-table partitions (Álvaro Herrera)

    The case isn't supported, and previously threw an incomprehensible error.
*   Fix construction of per-partition foreign key constraints while doing `ALTER TABLE ATTACH PARTITION` (Jehan-Guillaume de Rorthais, Álvaro Herrera)

    Previously, incorrect or duplicate constraints could be constructed for the newly-added partition.
*   Fix planner failure with extended statistics on partitioned or inherited tables (Richard Guo, Justin Pryzby)

    Some cases failed with “cache lookup failed for statistics object”.
*   Fix mis-ordering of WAL operations in fast insert path for GIN indexes (Matthias van de Meent, Zhang Mingli)

    This mistake is not known to have any negative consequences within core PostgreSQL, but it did cause issues for some extensions.
*   Fix bugs in logical decoding when replay starts from a point between the beginning of a transaction and the beginning of its subtransaction (Masahiko Sawada, Kuroda Hayato)

    These errors could lead to assertion failures in debug builds, and otherwise to memory leaks.
*   Accept interrupts in more places during logical decoding (Amit Kapila, Masahiko Sawada)

    This ameliorates problems with slow shutdown of replication workers.
*   Prevent attempts to replicate into a foreign-table partition in replication workers (Shi Yu, Tom Lane)

    Although partitioned tables can have foreign tables as partitions, replicating into such a partition isn't currently supported. The logical replication worker process would crash if it was attempted. Now, an error is thrown.
*   Avoid crash after function syntax error in replication workers (Maxim Orlov, Anton Melnikov, Masahiko Sawada, Tom Lane)

    If a syntax error occurred in a SQL-language or PL/pgSQL-language `CREATE FUNCTION` or `DO` command executed in a logical replication worker, the worker process would crash with a null pointer dereference or assertion failure.
* Avoid double call of the shutdown callback of an archiver module (Nathan Bossart, Bharath Rupireddy)
*   Add plan-time check for attempted access to a table that has no table access method (Tom Lane)

    This prevents a crash in some catalog-corruption scenarios, for example use of a view whose `ON SELECT` rule is missing.
*   Prevent postmaster crash when shared-memory state is corrupted (Tom Lane)

    The postmaster process is supposed to survive and initiate a database restart if shared memory becomes corrupted, but one bit of code was being insufficiently cautious about that.
*   In libpq, handle single-row mode correctly when pipelining (Denis Laxalde)

    The single-row flag was not reset at the correct time if pipeline mode was also active.
*   Fix psql's exit status when a command-line query is canceled (Peter Eisentraut)

    `psql -c`` `_`query`_ would exit successfully if the query was canceled. Fix it to exit with nonzero status, as in other error cases.
*   Allow cross-platform tablespace relocation in pg\_basebackup (Robert Haas)

    Allow the remote path in `--tablespace-mapping` to be either a Unix-style or Windows-style absolute path, since the source server could be on a different OS than the local system.
* Fix pg\_dump's failure to dump comments attached to some `CHECK` constraints (Tom Lane)
*   Fix `CREATE DATABASE` to allow its `oid` parameter to exceed 231 (Tom Lane)

    This oversight prevented pg\_upgrade from succeeding when the source installation contained databases with OIDs larger than that.
*   In pg\_stat\_statements, fix access to already-freed memory (zhaoqigui)

    This occurred if pg\_stat\_statements tracked a `ROLLBACK` command issued via extended query protocol. In debug builds it consistently led to an assertion failure. In production builds there would often be no visible ill effect; but if the freed memory had already been reused, the likely result would be to store garbage for the query string.
* Fix incompatibilities with LLVM 15 (Thomas Munro, Andres Freund)
*   Allow use of `__sync_lock_test_and_set()` for spinlocks on any machine (Tom Lane)

    This eases porting to new machine architectures, at least if you're using a compiler that supports this GCC builtin function.
* Rename symbol `REF` to `REF_P` to avoid compile failure on recent macOS (Tom Lane)
* Avoid using `sprintf`, to avoid compile-time deprecation warnings (Tom Lane)
*   Update time zone data files to tzdata release 2022f for DST law changes in Chile, Fiji, Iran, Jordan, Mexico, Palestine, and Syria, plus historical corrections for Chile, Crimea, Iran, and Mexico.

    Also, the Europe/Kiev zone has been renamed to Europe/Kyiv. Also, the following zones have been merged into nearby, more-populous zones whose clocks have agreed with them since 1970: Antarctica/Vostok, Asia/Brunei, Asia/Kuala\_Lumpur, Atlantic/Reykjavik, Europe/Amsterdam, Europe/Copenhagen, Europe/Luxembourg, Europe/Monaco, Europe/Oslo, Europe/Stockholm, Indian/Christmas, Indian/Cocos, Indian/Kerguelen, Indian/Mahe, Indian/Reunion, Pacific/Chuuk, Pacific/Funafuti, Pacific/Majuro, Pacific/Pohnpei, Pacific/Wake and Pacific/Wallis. (This indirectly affects zones that were already links to one of these: Arctic/Longyearbyen, Atlantic/Jan\_Mayen, Iceland, Pacific/Ponape, Pacific/Truk, and Pacific/Yap.) America/Nipigon, America/Rainy\_River, America/Thunder\_Bay, Europe/Uzhgorod, and Europe/Zaporozhye were also merged into nearby zones after discovering that their claimed post-1970 differences from those zones seem to have been errors. In all these cases, the previous zone name remains as an alias; but the actual data is that of the zone that was merged into.

    These zone mergers result in loss of pre-1970 timezone history for the merged zones, which may be troublesome for applications expecting consistency of `timestamptz` display. As an example, the stored value `1944-06-01 12:00 UTC` would previously display as `1944-06-01 13:00:00+01` if the Europe/Stockholm zone is selected, but now it will read out as `1944-06-01 14:00:00+02`.

    It is possible to build the time zone data files with options that will restore the older zone data, but that choice also inserts a lot of other old (and typically poorly-attested) zone data, resulting in more total changes from the previous release than accepting these upstream changes does. PostgreSQL has chosen to ship the tzdb data as-recommended, and so far as we are aware most major operating system distributions are doing likewise. However, if these changes cause significant problems for your application, a possible solution is to install a local build of the time zone data files using tzdb's backwards-compatibility options (see their `PACKRATDATA` and `PACKRATLIST` options).
