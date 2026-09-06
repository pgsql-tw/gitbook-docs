<a id="RELEASE-15-11"></a>

# E.9. Release 15.11

[E.9.1. Migration to Version 15.11](#id-1.11.6.14.4)

[E.9.2. Changes](#id-1.11.6.14.5)

<strong>Release date: </strong>2025-02-13

This release contains a variety of fixes from 15.10. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.14.4"></a>

## E.9.1. Migration to Version 15.11

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.9, see [Section E.11](release-15-9.md).

<a id="id-1.11.6.14.5"></a>

## E.9.2. Changes

* Harden `PQescapeString` and allied functions against invalidly-encoded input strings (Andres Freund, Noah Misch) [§](https://postgr.es/c/370c94d4c) [§](https://postgr.es/c/703b3fd5d) [§](https://postgr.es/c/b1756da75) [§](https://postgr.es/c/de4b92f33) [§](https://postgr.es/c/a085fa731) [§](https://postgr.es/c/9862de917)

  Data-quoting functions supplied by libpq now fully check the encoding validity of their input. If invalid characters are detected, they report an error if possible. For the ones that lack an error return convention, the output string is adjusted to ensure that the server will report invalid encoding and no intervening processing will be fooled by bytes that might happen to match single quote, backslash, etc.

  The purpose of this change is to guard against SQL-injection attacks that are possible if one of these functions is used to quote crafted input. There is no hazard when the resulting string is sent directly to a PostgreSQL server (which would check its encoding anyway), but there is a risk when it is passed through psql or other client-side code. Historically such code has not carefully vetted encoding, and in many cases it's not clear what it should do if it did detect such a problem.

  This fix is effective only if the data-quoting function, the server, and any intermediate processing agree on the character encoding that's being used. Applications that insert untrusted input into SQL commands should take special care to ensure that that's true.

  Applications and drivers that quote untrusted input without using these libpq functions may be at risk of similar problems. They should first confirm the data is valid in the encoding expected by the server.

  The PostgreSQL Project thanks Stephen Fewer for reporting this problem. (CVE-2025-1094)
* Exclude parallel workers from connection privilege checks and limits (Tom Lane) [§](https://postgr.es/c/3d1ecc92a)

  Do not check `datallowconn`, `rolcanlogin`, and `ACL_CONNECT` privileges when starting a parallel worker, instead assuming that it's enough for the leader process to have passed similar checks originally. This avoids, for example, unexpected failures of parallelized queries when the leader is running as a role that lacks login privilege. In the same vein, enforce `ReservedConnections`, `datconnlimit`, and `rolconnlimit` limits only against regular backends, and count only regular backends while checking if the limits were already reached. Those limits are meant to prevent excessive consumption of process slots for regular backends --- but parallel workers and other special processes have their own pools of process slots with their own limit checks.
* Fix possible re-use of stale results in window aggregates (David Rowley) [§](https://postgr.es/c/d54378e98)

  A window aggregate with a “run condition” optimization and a pass-by-reference result type might incorrectly return the result from the previous partition instead of performing a fresh calculation.
* Keep `TransactionXmin` in sync with `MyProc->xmin` (Heikki Linnakangas) [§](https://postgr.es/c/acd5c28db)

  This oversight could permit a process to try to access data that had already been vacuumed away. One known consequence is transient “could not access status of transaction” errors.
* Fix race condition that could cause failure to add a newly-inserted catalog entry to a catalog cache list (Heikki Linnakangas) [§](https://postgr.es/c/ce7c406f0)

  This could result, for example, in failure to use a newly-created function within an existing session.
* Prevent possible catalog corruption when a system catalog is vacuumed concurrently with an update (Noah Misch) [§](https://postgr.es/c/dc02b98bd)
* Fix data corruption when relation truncation fails (Thomas Munro) [§](https://postgr.es/c/fb540b6aa) [§](https://postgr.es/c/3181befdc) [§](https://postgr.es/c/190054e61)

  The filesystem calls needed to perform relation truncation could fail, leaving inconsistent state on disk (for example, effectively reviving deleted data). We can't really prevent that, but we can recover by dint of making such failures into PANICs, so that consistency is restored by replaying from WAL up to just before the attempted truncation. This isn't a hugely desirable behavior, but such failures are rare enough that it seems an acceptable solution.
* Prevent checkpoints from starting during relation truncation (Robert Haas) [§](https://postgr.es/c/a501fe5a9)

  This avoids a race condition wherein the modified file might not get fsync'd before completing the checkpoint, creating a risk of data corruption if the operating system crashes soon after.
* Use `rename()` not `link()`/`unlink()` to rename files (Nathan Bossart) [§](https://postgr.es/c/c1c9df315)

  The previous coding was intended to assure that the operation could not accidentally overwrite an existing file. However a failure could leave two links to the same file in existence, confusing subsequent operations and creating a risk of data corruption. In practice we do not use this functionality in places where the target filename could already exist, so it seems better to give up the no-overwrite guarantee to remove the multiple-link hazard.
* Avoid possibly losing an update of `pg_database`.`datfrozenxid` when `VACUUM` runs concurrently with a `REASSIGN OWNED` that changes that database's owner (Kirill Reshke) [§](https://postgr.es/c/83bb52375)
* Fix incorrect `tg_updatedcols` values passed to `AFTER UPDATE` triggers (Tom Lane) [§](https://postgr.es/c/cdeed4de7)

  In some cases the `tg_updatedcols` bitmap could describe the set of columns updated by an earlier command in the same transaction, fooling the trigger into doing the wrong thing.

  Also, prevent memory bloat caused by making too many copies of the `tg_updatedcols` bitmap.
* Fix detach of a partition that has its own foreign-key constraint referencing a partitioned table (Amul Sul) [§](https://postgr.es/c/1bc092519)

  In common cases, foreign keys are defined on a partitioned table's top level; but if instead one is defined on a partition and references a partitioned table, and the referencing partition is detached, the relevant `pg_constraint` entries were updated incorrectly. This led to errors like “could not find ON INSERT check triggers of foreign key constraint”.
* Fix mis-processing of `to_timestamp`'s <code class="literal">FF<em class="replaceable"><code>n</code></em></code> format codes (Tom Lane) [§](https://postgr.es/c/d2f59497a)

  An integer format code immediately preceding <code class="literal">FF<em class="replaceable"><code>n</code></em></code> would consume all available digits, leaving none for <code class="literal">FF<em class="replaceable"><code>n</code></em></code>.
* When deparsing an `XMLTABLE()` expression, ensure that XML namespace names are double-quoted when necessary (Dean Rasheed) [§](https://postgr.es/c/7c0379516)
* Include the `ldapscheme` option in `pg_hba_file_rules()` output (Laurenz Albe) [§](https://postgr.es/c/830215a4c) [§](https://postgr.es/c/9ad7a32b2)
* Don't merge `UNION` operations if their column collations aren't consistent (Tom Lane) [§](https://postgr.es/c/fd3383ff1)

  Previously we ignored collations when deciding if it's safe to merge `UNION` steps into a single N-way `UNION` operation. This was arguably valid before the introduction of nondeterministic collations, but it's not anymore, since the collation in use can affect the definition of uniqueness.
* Fix missed expression processing for partition pruning steps (Tom Lane) [§](https://postgr.es/c/724ebebb1)

  This oversight could lead to “unrecognized node type” errors, and perhaps other problems, in queries accessing partitioned tables.
* Allow dshash tables to grow past 1GB (Matthias van de Meent) [§](https://postgr.es/c/9f7b7d516)

  This avoids errors like “invalid DSA memory alloc request size”. The case can occur for example in transactions that process several million tables.
* Avoid possible integer overflow in `bringetbitmap()` (James Hunter, Evgeniy Gorbanyov) [§](https://postgr.es/c/9e9f30139)

  Since the result is only used for statistical purposes, the effects of this error were mostly cosmetic.
* Prevent streaming standby servers from looping infinitely when reading a WAL record that crosses pages (Kyotaro Horiguchi, Alexander Kukushkin) [§](https://postgr.es/c/26554facc)

  This would happen when the record's continuation is on a page that needs to be read from a different WAL source.
* Fix unintended promotion of FATAL errors to PANIC during early process startup (Noah Misch) [§](https://postgr.es/c/839da50bd)

  This fixes some unlikely cases that would result in “PANIC: proc_exit() called in child process”.
* Fix cases where an operator family member operator or support procedure could become a dangling reference (Tom Lane) [§](https://postgr.es/c/0e4fa06ba) [§](https://postgr.es/c/d40191467)

  In some cases a data type could be dropped while references to its OID still remain in `pg_amop` or `pg_amproc`. While that caused no immediate issues, an attempt to drop the owning operator family would fail, and pg_dump would produce bogus output when dumping the operator family. This fix causes creation and modification of operator families/classes to add needed dependency entries so that dropping a data type will also drop any dependent operator family elements. That does not help vulnerable pre-existing operator families, though, so a band-aid has also been added to `DROP OPERATOR FAMILY` to prevent failure when dropping a family that has dangling members.
* Fix multiple memory leaks in logical decoding output (Vignesh C, Masahiko Sawada, Boyu Yang) [§](https://postgr.es/c/da8bd5d42) [§](https://postgr.es/c/6c9b39754) [§](https://postgr.es/c/6fc30c24c)
* Avoid low-probability crash on out-of-memory, due to missing check for failure return from `malloc()` (Karina Litskevich) [§](https://postgr.es/c/4398507df)
* Avoid integer overflow while testing `wal_skip_threshold` condition (Tom Lane) [§](https://postgr.es/c/b296e55b4)

  A transaction that created a very large relation could mistakenly decide to ensure durability by copying the relation into WAL instead of fsync'ing it, thereby negating the point of `wal_skip_threshold`. (This only matters when `wal_level` is set to `minimal`, else a WAL copy is required anyway.)
* Fix unsafe order of operations during cache lookups (Noah Misch) [§](https://postgr.es/c/941e0c0df)

  The only known consequence was a usually-harmless “you don't own a lock of type ExclusiveLock” warning during `GRANT TABLESPACE`.
* Fix possible “failed to resolve name” failures when using JIT on older ARM platforms (Thomas Munro) [§](https://postgr.es/c/15ab513fe)

  This could occur as a consequence of inconsistency about the default setting of `-moutline-atomics` between gcc and clang. At least Debian and Ubuntu are known to ship gcc and clang compilers that target armv8-a but differ on the use of outline atomics by default.
* Fix handling of Windows junction points that are not of PostgreSQL origin (Thomas Munro) [§](https://postgr.es/c/9b136b0f2) [§](https://postgr.es/c/e708f3188)

  Previously, initdb would fail if the path to the data directory included junction points whose expansion isn't in “drive absolute” format, or whose expansion points to another junction point.
* Fix assertion failure in `WITH RECURSIVE ... UNION` queries (David Rowley) [§](https://postgr.es/c/ef178d38b)
* Avoid assertion failure in rule deparsing if a set operation leaf query contains set operations (Man Zeng, Tom Lane) [§](https://postgr.es/c/9b9689e26)
* Avoid edge-case assertion failure in parallel query startup (Tom Lane) [§](https://postgr.es/c/4089b9bd6)
* Fix assertion failure at shutdown when writing out the statistics file (Michael Paquier) [§](https://postgr.es/c/1df1e1e78)
* In `NULLIF()`, avoid passing a read-write expanded object pointer to the data type's equality function (Tom Lane) [§](https://postgr.es/c/80cd33bad)

  The equality function could modify or delete the object if it's given a read-write pointer, which would be bad if we decide to return it as the `NULLIF()` result. There is probably no problem with any built-in equality function, but it's easy to demonstrate a failure with one coded in PL/pgSQL.
* Ensure that expression preprocessing is applied to a default null value in `INSERT` (Tom Lane) [§](https://postgr.es/c/bb85d0935)

  If the target column is of a domain type, the planner must insert a coerce-to-domain step not just a null constant, and this expression missed going through some required processing steps. There is no known consequence with domains based on core data types, but in theory an error could occur with domains based on extension types.
* Repair memory leaks in PL/Python (Mat Arye, Tom Lane) [§](https://postgr.es/c/71bb9c4b2)

  Repeated use of `PLyPlan.execute` or `plpy.cursor` resulted in memory leakage for the duration of the calling PL/Python function.
* Fix PL/Tcl to compile with Tcl 9 (Peter Eisentraut) [§](https://postgr.es/c/a5f9cbde9)
* In the ecpg preprocessor, fix possible misprocessing of cursors that reference out-of-scope variables (Tom Lane) [§](https://postgr.es/c/60b47525c)
* In ecpg, fix compile-time warnings about unsupported use of `COPY ... FROM STDIN` (Ryo Kanbayashi) [§](https://postgr.es/c/71ef47cf0)

  Previously, the intended warning was not issued due to a typo.
* Fix psql to safely handle file path names that are encoded in SJIS (Tom Lane) [§](https://postgr.es/c/b17e3970c)

  Some two-byte characters in SJIS have a second byte that is equal to ASCII backslash (`\`). These characters were corrupted by path name normalization, preventing access to files whose names include such characters.
* Fix use of wrong version of `pqsignal()` in pgbench and psql (Fujii Masao, Tom Lane) [§](https://postgr.es/c/a3b709cf7)

  This error could lead to misbehavior when using the `-T` option in pgbench or the `\watch` command in psql, due to interrupted system calls not being resumed as expected.
* Fix misexecution of some nested `\if` constructs in pgbench (Michail Nikolaev) [§](https://postgr.es/c/ff88db910)

  An `\if` command appearing within a false (not-being-executed) `\if` branch was incorrectly treated the same as `\elif`.
* In pgbench, fix possible misdisplay of progress messages during table initialization (Yushi Ogiwara, Tatsuo Ishii, Fujii Masao) [§](https://postgr.es/c/1e46f7351) [§](https://postgr.es/c/499d1cf55)
* Make pg_controldata more robust against corrupted `pg_control` files (Ilyasov Ian, Anton Voloshin) [§](https://postgr.es/c/f1e0b078b)

  Since pg_controldata will attempt to print the contents of `pg_control` even if the CRC check fails, it must take care not to misbehave for invalid field values. This patch fixes some issues triggered by invalid timestamps and apparently-negative WAL segment sizes.
* Fix possible crash in pg_dump with identity sequences attached to tables that are extension members (Tom Lane) [§](https://postgr.es/c/6978129b4)
* Fix pg_basebackup to correctly handle `pg_wal.tar` files exceeding 2GB on Windows (Davinder Singh, Thomas Munro) [§](https://postgr.es/c/6b6901a26) [§](https://postgr.es/c/70a7a3761)
* Update configuration probes that determine the compiler switches needed to access ARM CRC instructions (Tom Lane) [§](https://postgr.es/c/851c6ff18)

  On ARM platforms where the baseline CPU target lacks CRC instructions, we need to supply a `-march` switch to persuade the compiler to compile such instructions. Recent versions of gcc reject the value we were trying, leading to silently falling back to software CRC.
* During configure, if a C23 compiler is detected, try asking for C17 (Thomas Munro) [§](https://postgr.es/c/f00c401c6)

  PostgreSQL versions before v16 will not compile under C23 rules. If the chosen compiler defaults to C23 or later, try adding a `-std=gnu17` switch to change that. (If this won't work for your compiler, manually specify `CFLAGS` with a suitable switch.)
* Update time zone data files to tzdata release 2025a for DST law changes in Paraguay, plus historical corrections for the Philippines (Tom Lane) [§](https://postgr.es/c/48bc95d0d)

---

原文：[PostgreSQL 15.19 Documentation](release-15-11.md)（英文原文，待翻譯）
