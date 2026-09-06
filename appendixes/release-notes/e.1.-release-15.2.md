# E.1. Release 15.2

**Release date:** 2023-02-09

This release contains a variety of fixes from 15.1. For information about new features in major release 15, see [Section E.3](https://www.postgresql.org/docs/15/release-15.html).

## E.1.1. Migration to Version 15.2

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.1, see [Section E.2](https://www.postgresql.org/docs/15/release-15-1.html).

## E.1.2. Changes

*   libpq can leak memory contents after GSSAPI transport encryption initiation fails (Jacob Champion)

    A modified server, or an unauthenticated man-in-the-middle, can send a not-zero-terminated error message during setup of GSSAPI (Kerberos) transport encryption. libpq will then copy that string, as well as following bytes in application memory up to the next zero byte, to its error report. Depending on what the calling application does with the error report, this could result in disclosure of application memory contents. There is also a small probability of a crash due to reading beyond the end of memory. Fix by properly zero-terminating the server message. (CVE-2022-41862)
*   Fix calculation of which `GENERATED` columns need to be updated in child tables during an `UPDATE` on a partitioned table or inheritance tree (Amit Langote, Tom Lane)

    This fixes failure to update `GENERATED` columns that do not exist in the parent table, or that have different dependencies than are in the parent column's generation expression.
*   Fix possible failure of `MERGE` to compute `GENERATED` columns (Dean Rasheed)

    When the first row-level action of the `MERGE` was an `UPDATE`, any subsequent `INSERT` actions would fail to compute `GENERATED` columns that were deemed unnecessary to compute for the `UPDATE` action (due to not depending on any of the `UPDATE` target columns).
*   Fix `MERGE`'s check for unreachable `WHEN` clauses (Dean Rasheed)

    A `WHEN` clause following an unconditional `WHEN` clause should be rejected as unreachable, but this case was not always detected.
*   Fix `MERGE`'s rule-detection test (Dean Rasheed)

    `MERGE` is not supported on tables with rules; but it also failed on tables that once had rules but no longer do.
*   In `MERGE`, don't count a `DO NOTHING` action as a processed tuple (Álvaro Herrera)

    This makes the code's behavior match the documentation.
*   Allow a `WITH RECURSIVE ... CYCLE` CTE to access its output column (Tom Lane)

    A reference to the `SET` column from within the CTE would fail with “cache lookup failed for type 0”.
*   Fix handling of pending inserts when doing a bulk insertion to a foreign table (Etsuro Fujita)

    In some cases pending insertions were not flushed to the FDW soon enough, leading to logical inconsistencies, for example `BEFORE ROW` triggers not seeing rows they should be able to see.
*   Allow `REPLICA IDENTITY` to be set on an index that's not (yet) valid (Tom Lane)

    When pg\_dump dumps a partitioned index that's marked `REPLICA IDENTITY`, it generates a command sequence that applies `REPLICA IDENTITY` before the partitioned index has been marked valid, causing restore to fail. There seems no very good reason to prohibit doing it in that order, so allow it. The marking will have no effect anyway until the index becomes valid.
*   Fix handling of `DEFAULT` markers in rules that perform an `INSERT` from a multi-row `VALUES` list (Dean Rasheed)

    In some cases a `DEFAULT` marker would not get replaced with the proper default-value expression, leading to an “unrecognized node type” error.
*   Reject uses of undefined variables in `jsonpath` existence checks (Alexander Korotkov, David G. Johnston)

    While `jsonpath` match operators threw an error for an undefined variable in the path pattern, the existence operators silently treated it as a match.
*   Fix `jsonb` subscripting to cope with toasted subscript values (Tom Lane, David G. Johnston)

    Using a text value fetched directly from a table as a `jsonb` subscript was likely to fail. Fetches would usually not find any matching element. Assignments could store the value with a garbage key, although keys long enough to cause that problem are probably rare in the field.
*   Fix edge-case data corruption in parallel hash joins (Dmitry Astapov)

    If the final chunk of a large tuple being written out to a temporary file was exactly 32760 bytes, it would be corrupted due to a fencepost bug. The query would typically fail later with corrupted-data symptoms.
*   Honor non-default settings of `checkpoint_completion_target` (Bharath Rupireddy)

    Internal state was not updated after a change in `checkpoint_completion_target`, possibly resulting in performing checkpoint I/O faster or slower than desired, especially if that setting was changed on-the-fly.
*   Log the correct ending timestamp in `recovery_target_xid` mode (Tom Lane)

    When ending recovery based on the `recovery_target_xid` setting with `recovery_target_inclusive` = `off`, we printed an incorrect timestamp (always 2000-01-01) in the “recovery stopping before ... transaction” log message.
*   Improve error reporting for some buffered file read failures (Peter Eisentraut)

    Correctly report a short read, giving the numbers of bytes desired and actually read, instead of reporting an irrelevant error code. Most places got this right already, but some recently-written replication logic did not.
*   Remove arbitrary limit on number of elements in `int2vector` and `oidvector` (Tom Lane)

    The input functions for these types previously rejected more than 100 elements. With the introduction of the logical replication column list feature, it's necessary to accept `int2vector`s having up to 1600 columns, otherwise long column lists cause logical-replication failures.
*   In extended query protocol, avoid an immediate commit after `ANALYZE` if we're running a pipeline (Tom Lane)

    If there's not been an explicit `BEGIN TRANSACTION`, `ANALYZE` would take it on itself to commit, which should not happen within a pipelined series of commands.
*   Reject cancel request packets having the wrong length (Andrey Borodin)

    The server would process a cancel request even if its length word was too small. This led to reading beyond the end of the allocated buffer. In theory that could cause a segfault, but it seems quite unlikely to happen in practice, since the buffer would have to be very close to the end of memory. The more likely outcome was a bogus log message about wrong backend PID or cancel code. Complain about the wrong length, instead.
*   Fix planner preprocessing oversights for window function run-condition expressions (Richard Guo, David Rowley)

    This could lead to planner errors such as “WindowFunc not found in subplan target lists”.
*   Fix possible dangling-pointer access during execution of window function run-condition expressions (David Rowley)

    In practice, because the run-condition optimization is only applied to certain window functions that happen to all return `int8`, this only manifested as a problem on 32-bit builds.
*   Add recursion and looping defenses in subquery pullup (Tom Lane)

    A contrived query can result in deep recursion and unreasonable amounts of time spent trying to flatten subqueries. A proper fix for that seems unduly invasive for a back-patch, but we can at least add stack depth checks and an interrupt check to allow the query to be cancelled.
*   Fix planner issues when combining Memoize nodes with partitionwise joins or parameterized nestloops (Richard Guo)

    These errors could lead to not using Memoize in contexts where it would be useful, or possibly to wrong query plans.
*   Fix partitionwise-join code to tolerate failure to produce a plan for each partition (Tom Lane)

    This could result in “could not devise a query plan for the given query” errors.
*   Limit the amount of cleanup work done by `get_actual_variable_range` (Simon Riggs)

    Planner runs occurring just after deletion of a large number of tuples appearing at the end of an index could expend significant amounts of work setting the “killed” bits for those index entries. Limit the amount of work done in any one query by giving up on this process after examining 100 heap pages. All the cleanup will still happen eventually, but without so large a performance hiccup.
*   Prevent the statistics machinery from getting confused when a relation's relkind changes (Andres Freund)

    Converting a table to a view could lead to crashes or assertion failures.
*   Fix under-parenthesized display of `AT TIME ZONE` constructs (Tom Lane)

    This could result in dump/restore failures for rules or views in which an argument of `AT TIME ZONE` is itself an expression.
*   Prevent clobbering of cached parsetrees for utility statements in SQL functions (Tom Lane, Daniel Gustafsson)

    If a SQL-language function executes the same utility command more than once within a single calling query, it could crash or report strange errors such as “unrecognized node type”.
* Ensure that execution of full-text-search queries can be cancelled while they are performing phrase matches (Tom Lane)
* Fix memory leak in hashing strings with nondeterministic collations (Jeff Davis)
*   Fix deadlock between `DROP DATABASE` and logical replication worker process (Hou Zhijie)

    This was caused by an ill-advised choice to block interrupts while creating a logical replication slot in the worker. In version 15 that could lead to an undetected deadlock. In version 14, no deadlock has been observed, but it's still a bad idea to block interrupts while waiting for network I/O.
*   Clean up the libpq connection object after a failed replication connection attempt (Andres Freund)

    The previous coding leaked the connection object. In background code paths that's pretty harmless because the calling process will give up and exit. But in commands such as `CREATE SUBSCRIPTION`, such a failure resulted in a small session-lifespan memory leak.
*   In hot-standby servers, reduce processing effort for tracking XIDs known to be active on the primary (Simon Riggs, Michail Nikolaev)

    Insufficiently-aggressive cleanup of the KnownAssignedXids array could lead to poor performance, particularly when `max_connections` is set to a large value on the standby.
*   Ignore invalidated logical-replication slots while determining oldest catalog xmin (Sirisha Chamarthi)

    A replication slot could prevent cleanup of dead tuples in the system catalogs even after it becomes invalidated due to exceeding `max_slot_wal_keep_size`. Thus, failure of a replication consumer could lead to indefinitely-large catalog bloat.
*   In logical decoding, notify the remote node when a transaction is detected to have crashed (Hou Zhijie)

    After a server restart, we'll re-stream the changes for transactions occurring shortly before the restart. Some of these transactions probably never completed; when we realize that one didn't we throw away the relevant decoding state locally, but we neglected to tell the subscriber about it. That led to the subscriber keeping useless streaming files until it's next restarted.
*   Fix uninitialized-memory usage in logical decoding (Masahiko Sawada)

    In certain cases, resumption of logical decoding could try to re-use XID data that had already been freed, leading to unpredictable behavior.
*   Acquire spinlock while updating shared state during logical decoding context creation (Masahiko Sawada)

    We neglected to acquire the appropriate lock while updating data about two-phase transactions, potentially allowing other processes to see inconsistent data.
*   Fix pgoutput replication plug-in to not send columns not listed in a table's replication column list (Hou Zhijie)

    `UPDATE` and `DELETE` events did not pay attention to the configured column list, thus sending more data than expected. This did not cause a problem when the receiver is our built-in logical replication code, but it might confuse other receivers, and in any case it wasted network bandwidth.
* Avoid rare “failed to acquire cleanup lock” panic during WAL replay of hash-index page split operations (Robert Haas)
*   Advance a heap page's LSN when setting its all-visible bit during WAL replay (Jeff Davis)

    Failure to do this left the page possibly different on standby servers than the primary, and violated some other expectations about when the LSN changes. This seems only a theoretical hazard so far as PostgreSQL itself is concerned, but it could upset third-party tools.
*   Fix `int64_div_fast_to_numeric()` to work for a wider range of inputs (Dean Rasheed)

    This function misbehaved with some values of its second argument. No such usages exist in core PostgreSQL, but it's clearly a hazard for external modules, so repair.
*   Fix latent buffer-overrun problem in `WaitEventSet` logic (Thomas Munro)

    The `epoll`-based and `kqueue`-based implementations could ask the kernel for too many events if the size of their internal buffer was different from the size of the caller's output buffer. That case is not known to occur in released PostgreSQL versions, but this error is a hazard for external modules and future bug fixes.
*   Avoid nominally-undefined behavior when accessing shared memory in 32-bit builds (Andres Freund)

    clang's undefined-behavior sanitizer complained about use of a pointer that was less aligned than it should be. It's very unlikely that this would cause a problem in non-debug builds, but it's worth fixing for testing purposes.
*   Fix assertion failure in BRIN minmax-multi opclasses (Tomas Vondra)

    The assertion was overly strict, so this mistake was harmless in non-assert builds.
* Remove faulty assertion in useless-RESULT-RTE optimization logic (Tom Lane)
*   Fix copy-and-paste errors in cache-lookup-failure messages for ACL checks (Justin Pryzby)

    In principle these errors should never be reached. But if they are, some of them reported the wrong type of object.
* Fix possible corruption of very large tablespace map files in pg\_basebackup (Antonin Houska)
*   Avoid harmless warning from pg\_dump in `--if-exists` mode (Tom Lane)

    If the `public` schema has a non-default owner then use of pg\_dump's `--if-exists` option resulted in a warning message “warning: could not find where to insert IF EXISTS in statement "-- \*not\* dropping schema, since initdb creates it"”. The dump output was okay, though.
*   Fix psql's `\sf` and `\ef` commands to handle SQL-language functions that have SQL-standard function bodies (Tom Lane)

    These commands misidentified the start of the function body when it used new-style syntax.
* Fix tab completion of `ALTER FUNCTION/PROCEDURE/ROUTINE` ... `SET SCHEMA` (Dean Rasheed)
*   Update `contrib/pageinspect` to mark its disk-accessing functions as `PARALLEL RESTRICTED` (Tom Lane)

    This avoids possible failure if one of these functions is used to examine a temporary table, since a session's temporary tables are not accessible from parallel workers.
* Fix `contrib/seg` to not crash or print garbage if an input number has more than 127 digits (Tom Lane)
*   Fix build on Microsoft Visual Studio 2013 (Tom Lane)

    A previous patch supposed that all platforms of interest have `snprintf()`, but MSVC 2013 isn't quite there yet. Revert to using `sprintf()` on that platform.
* Fix compile failure in building PL/Perl with MSVC when using Strawberry Perl (Andrew Dunstan)
*   Fix mismatch of PL/Perl built with MSVC versus a Perl library built with gcc (Andrew Dunstan)

    Such combinations could previously fail with “loadable library and perl binaries are mismatched” errors.
*   Suppress compiler warnings from Perl's header files (Andres Freund)

    Our preferred compiler options provoke warnings about constructs appearing in recent versions of Perl's header files. When using gcc, we can suppress these warnings with a pragma.
* Fix pg\_waldump to build on compilers that don't discard unused static-inline functions (Tom Lane)
*   Update time zone data files to tzdata release 2022g for DST law changes in Greenland and Mexico, plus historical corrections for northern Canada, Colombia, and Singapore.

    Notably, a new timezone America/Ciudad\_Juarez has been split off from America/Ojinaga.
