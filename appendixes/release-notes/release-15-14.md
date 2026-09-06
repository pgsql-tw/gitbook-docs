<a id="RELEASE-15-14"></a>

# E.6. Release 15.14

[E.6.1. Migration to Version 15.14](#id-1.11.6.11.4)

[E.6.2. Changes](#id-1.11.6.11.5)

<strong>Release date: </strong>2025-08-14

This release contains a variety of fixes from 15.13. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.11.4"></a>

## E.6.1. Migration to Version 15.14

A dump/restore is not required for those running 15.X.

However, if you have any BRIN `numeric_minmax_multi_ops` indexes, it is advisable to reindex them after updating. See the fourth changelog entry below.

Also, if you are upgrading from a version earlier than 15.13, see [Section E.7](release-15-13.md).

<a id="id-1.11.6.11.5"></a>

## E.6.2. Changes

* Tighten security checks in planner estimation functions (Dean Rasheed) [§](https://postgr.es/c/415badc13)

  The fix for CVE-2017-7484, plus followup fixes, intended to prevent leaky functions from being applied to statistics data for columns that the calling user does not have permission to read. Two gaps in that protection have been found. One gap applies to partitioning and inheritance hierarchies where RLS policies on the tables should restrict access to statistics data, but did not.

  The other gap applies to cases where the query accesses a table via a view, and the view owner has permissions to read the underlying table but the calling user does not have permissions on the view. The view owner's permissions satisfied the security checks, and the leaky function would get applied to the underlying table's statistics before we check the calling user's permissions on the view. This has been fixed by making security checks on views occur at the start of planning. That might cause permissions failures to occur earlier than before.

  The PostgreSQL Project thanks Dean Rasheed for reporting this problem. (CVE-2025-8713)
* Prevent pg_dump scripts from being used to attack the user running the restore (Nathan Bossart) [§](https://postgr.es/c/424040506)

  Since dump/restore operations typically involve running SQL commands as superuser, the target database installation must trust the source server. However, it does not follow that the operating system user who executes psql to perform the restore should have to trust the source server. The risk here is that an attacker who has gained superuser-level control over the source server might be able to cause it to emit text that would be interpreted as psql meta-commands. That would provide shell-level access to the restoring user's own account, independently of access to the target database.

  To provide a positive guarantee that this can't happen, extend psql with a `\restrict` command that prevents execution of further meta-commands, and teach pg_dump to issue that before any data coming from the source server.

  The PostgreSQL Project thanks Martin Rakhmanov, Matthieu Denais, and RyotaK for reporting this problem. (CVE-2025-8714)
* Convert newlines to spaces in names included in comments in pg_dump output (Noah Misch) [§](https://postgr.es/c/9751f934a)

  Object names containing newlines offered the ability to inject arbitrary SQL commands into the output script. (Without the preceding fix, injection of psql meta-commands would also be possible this way.) CVE-2012-0868 fixed this class of problem at the time, but later work reintroduced several cases.

  The PostgreSQL Project thanks Noah Misch for reporting this problem. (CVE-2025-8715)
* Fix incorrect distance calculation in BRIN `numeric_minmax_multi_ops` support function (Peter Eisentraut, Tom Lane) [§](https://postgr.es/c/835c9374d)

  The results were sometimes wrong on 64-bit platforms, and wildly wrong on 32-bit platforms. This did not produce obvious failures because the logic is only used to choose how to merge values into ranges; at worst the index would become inefficient and bloated. Nonetheless it's recommended to reindex any BRIN indexes that use the `numeric_minmax_multi_ops` operator class.
* Avoid regression in the size of XML input that we will accept (Michael Paquier, Erik Wienhold) [§](https://postgr.es/c/0ffbd345e) [§](https://postgr.es/c/0928e18eb)

  Our workaround for a bug in early 2.13.x releases of libxml2 made use of a code path that rejects text chunks exceeding 10MB, whereas the previous coding did not. Those early releases are presumably extinct in the wild by now, so revert to the previous coding.
* Fix `MERGE` into a plain-inheritance parent table (Dean Rasheed) [§](https://postgr.es/c/d6a3f3272)

  Insertions into such a target table could crash or produce incorrect query results due to failing to handle `WITH CHECK OPTION` and `RETURNING` actions.
* Allow tables with statement-level triggers to become partitions or inheritance children (Etsuro Fujita) [§](https://postgr.es/c/f39a7f32a)

  We do not allow partitions or inheritance child tables to have row-level triggers with transition tables, because an operation on the whole inheritance tree would need to maintain a separate transition table for each such child table. But that problem does not apply for statement-level triggers, because only the parent's statement-level triggers will be fired. The code that checks whether an existing table can become a partition or inheritance child nonetheless rejected both kinds of trigger.
* Disallow collecting transition tuples from child foreign tables (Etsuro Fujita) [§](https://postgr.es/c/d642d2306)

  We do not support triggers with transition tables on foreign tables. However, the case of a partition or inheritance child that is a foreign table was overlooked. If the parent has such a trigger, incorrect transition tuples were collected from the foreign child. Instead throw an error, reporting that the case is not supported.
* Allow resetting unknown custom parameters with reserved prefixes (Nathan Bossart) [§](https://postgr.es/c/f79ca73d7)

  Previously, if a parameter setting had been stored using `ALTER DATABASE/ROLE/SYSTEM`, the stored setting could not be removed if the parameter was unknown but had a reserved prefix. This case could arise if an extension used to have a parameter, but that parameter had been removed in an upgrade.
* Fix a potential deadlock during `ALTER SUBSCRIPTION ... DROP PUBLICATION` (Ajin Cherian) [§](https://postgr.es/c/434d2d147)

  Ensure that server processes acquire catalog locks in a consistent order during replication origin drops.
* Shorten the race condition window for creating indexes with conflicting names (Tom Lane) [§](https://postgr.es/c/75b8982ea)

  When choosing an auto-generated name for an index, avoid conflicting with not-yet-committed `pg_class` rows as well as fully-valid ones. This avoids possibly choosing the same name as some concurrent `CREATE INDEX` did, when that command is still in process of filling its index, or is done but is part of a not-yet-committed transaction. There's still a window for trouble, but it's only as long as the time needed to validate a new index's parameters and insert its `pg_class` row.
* Prevent usage of incorrect `VACUUM` options in some cases where multiple tables are vacuumed in a single command (Nathan Bossart, Michael Paquier) [§](https://postgr.es/c/354944663)

  The `TRUNCATE` and `INDEX_CLEANUP` options of one table could be applied to others.
* Fix processing of character classes within `SIMILAR TO` regular expressions (Laurenz Albe) [§](https://postgr.es/c/b3e99115e) [§](https://postgr.es/c/4dc642e75)

  The code that translates `SIMILAR TO` pattern matching expressions to POSIX-style regular expressions did not consider that square brackets can be nested. For example, in a pattern like `[[:alpha:]%_]`, the code treated the `%` and `_` characters as metacharacters when they should be literals.
* When deparsing queries, always add parentheses around the expression in <code class="literal">FETCH FIRST <em class="replaceable"><code>expression</code></em> ROWS WITH TIES</code> clauses (Heikki Linnakangas) [§](https://postgr.es/c/72fe74ca5)

  This avoids some cases where the deparsed result wasn't syntactically valid.
* Limit the checkpointer process's fsync request queue size (Alexander Korotkov, Xuneng Zhou) [§](https://postgr.es/c/b248a3ba4) [§](https://postgr.es/c/73f897ba5)

  With very large `shared_buffers` settings, it was possible for the checkpointer to attempt to allocate more than 1GB for fsync requests, leading to failure and an infinite loop. Clamp the queue size to prevent this scenario.
* Avoid infinite wait in logical decoding when reading a partially-written WAL record (Vignesh C) [§](https://postgr.es/c/9f270f48f)

  If the server crashes after writing the first part of a WAL record that would span multiple pages, subsequent logical decoding of the WAL stream would wait for data to arrive on the next WAL page. That might never happen if the server is now idle.
* Fix inconsistent quoting of role names in ACL strings (Tom Lane) [§](https://postgr.es/c/de73cb3ed)

  The previous quoting rule was locale-sensitive, which could lead to portability problems when transferring `aclitem` values across installations. (pg_dump does not do that, but other tools might.) To ensure consistency, always quote non-ASCII characters in `aclitem` output; but to preserve backward compatibility, never require that they be quoted during `aclitem` input.
* Reject equal signs (`=`) in the names of relation options and foreign-data options (Tom Lane) [§](https://postgr.es/c/e76097124)

  There's no evident use-case for option names like this, and allowing them creates ambiguity in the stored representation.
* Fix potentially-incorrect decompression of LZ4-compressed archive data (Mikhail Gribkov) [§](https://postgr.es/c/d44efe87e)

  This error seems to manifest only with not-very-compressible input data, which may explain why it escaped detection.
* Avoid a rare scenario where a btree index scan could mark the wrong index entries as dead (Peter Geoghegan) [§](https://postgr.es/c/d2ec67109)
* Avoid re-distributing cache invalidation messages from other transactions during logical replication (vignesh C) [§](https://postgr.es/c/fc0fb77c5)

  Our previous round of minor releases included a bug fix to ensure that replication receiver processes would respond to cross-process cache invalidation messages, preventing them from using stale catalog data while performing replication updates. However, the fix unintentionally made them also redistribute those messages again, leading to an exponential increase in the number of invalidation messages, which would often end in a memory allocation failure. Fix by not redistributing received messages.
* Avoid premature removal of old WAL during checkpoints (Vitaly Davydov) [§](https://postgr.es/c/dd9bc1a17)

  If a replication slot's restart point is advanced while a checkpoint is in progress, no-longer-needed WAL segments could get removed too soon, leading to recovery failure if the database crashes immediately afterwards. Fix by keeping them for one additional checkpoint cycle.
* Never move a replication slot's confirmed-flush position backwards (Shveta Malik) [§](https://postgr.es/c/9d1a62359)

  In some cases a replication client could acknowledge an LSN that's past what it has stored persistently, and then perhaps send an older LSN after a restart. We consider this not-a-bug so long as the client did not have anything it needed to do for the WAL between the two points. However, we should not re-send that WAL for fear of data duplication, so make sure we always believe the latest confirmed LSN for a given slot.
* Allow waiting for a transaction on a standby server to be interrupted (Kevin K Biju) [§](https://postgr.es/c/405cca9da)

  Creation of a replication slot on a standby server may require waiting for some active transaction(s) to finish on the primary and then be replayed on the standby. Since that could be an indefinite wait, it's desirable to allow the operation to be cancelled, but there was no check for query cancel in the loop.
* Fix per-relation memory leakage in autovacuum (Tom Lane) [§](https://postgr.es/c/13d21b48a)
* Fix some places that might try to fetch toasted fields of system catalogs without any snapshot (Nathan Bossart) [§](https://postgr.es/c/ddfcfb7ce)

  This could result in an assertion failure or “cannot fetch toast data without an active snapshot” error.
* Avoid assertion failure during cross-table constraint updates (Tom Lane, Jian He) [§](https://postgr.es/c/614ffb26d) [§](https://postgr.es/c/e6dd6e6ee)
* Remove faulty assertion that a command tag must have been determined by the end of `PortalRunMulti()` (Álvaro Herrera) [§](https://postgr.es/c/c2720ac60)

  This failed in edge cases such as an empty prepared statement.
* Fix assertion failure in `XMLTABLE` parsing (Richard Guo) [§](https://postgr.es/c/666103090)
* Restore the ability to run PL/pgSQL expressions in parallel (Dipesh Dhameliya) [§](https://postgr.es/c/c65c36ab5)

  PL/pgSQL's notion of an “expression” is very broad, encompassing any SQL `SELECT` query that returns a single column and no more than one row. So there are cases, for example evaluation of an aggregate function, where the query involves significant work and it'd be useful to run it with parallel workers. This used to be possible, but a previous bug fix unintentionally disabled it.
* Fix edge-case resource leaks in PL/Python error reporting (Tom Lane) [§](https://postgr.es/c/b56a92651) [§](https://postgr.es/c/b898bb2a7)

  An out-of-memory failure while reporting an error from Python could result in failure to drop reference counts on Python objects, leading to session-lifespan memory leakage.
* Fix libpq's `PQport()` function to never return NULL unless the passed connection is NULL (Daniele Varrazzo) [§](https://postgr.es/c/a372a64db)

  This is the documented behavior, but recent libpq versions would return NULL in some cases where the user had not provided a port specification. Revert to our historical behavior of returning an empty string in such cases. (v18 and later will return the compiled-in default port number, typically `"5432"`, instead.)
* Avoid failure when GSSAPI authentication requires packets larger than 16kB (Jacob Champion, Tom Lane) [§](https://postgr.es/c/39b1d1907)

  Larger authentication packets are needed for Active Directory users who belong to many AD groups. This limitation manifested in connection failures with unintelligible error messages, typically “GSSAPI context establishment error: The routine must be called again to complete its function: Unknown error”.
* Fix timing-dependent failures in SSL and GSSAPI data transmission (Tom Lane) [§](https://postgr.es/c/6a4d93eda)

  When using SSL or GSSAPI encryption in non-blocking mode, libpq sometimes failed with “SSL error: bad length” or “GSSAPI caller failed to retransmit all data needing to be retried”.
* Avoid null-pointer dereference during connection lookup in ecpg applications (Aleksander Alekseev) [§](https://postgr.es/c/0123922f8)

  The case could occur only if the application has some connections that are named and some that are not.
* Improve psql's tab completion for `COPY` and `\copy` options (Atsushi Torikoshi) [§](https://postgr.es/c/e3584e457)

  The same completions were offered for both `COPY FROM` and `COPY TO`, although some options are only valid for one case or the other. Distinguish these cases to provide more accurate suggestions.
* Avoid assertion failure in pgbench when multiple pipeline sync messages are received (Fujii Masao) [§](https://postgr.es/c/6914a330f)
* Ensure that pg_dump dumps comments on domain constraints in a valid order (Jian He) [§](https://postgr.es/c/5a261c135)

  In some cases the comment command could appear before creation of the constraint.
* Ensure stable sort ordering in pg_dump for all types of database objects (Noah Misch, Andreas Karlsson) [§](https://postgr.es/c/22f126da6) [§](https://postgr.es/c/e99010cbd) [§](https://postgr.es/c/70637d7ae)

  pg_dump sorts objects by their logical names before performing dependency-driven reordering. This sort did not account for the full unique key identifying certain object types such as rules and constraints, and thus it could produce dissimilar sort orders for logically-identical databases. That made it difficult to compare databases by diff'ing pg_dump output, so improve the logic to ensure stable sort ordering in all cases.
* In pg_upgrade, check for inconsistent inherited not-null constraints (Ali Akbar) [§](https://postgr.es/c/0f4958685) [§](https://postgr.es/c/bd48455d8) [§](https://postgr.es/c/63c79a6fc) [§](https://postgr.es/c/22d783350) [§](https://postgr.es/c/a8b31b160) [§](https://postgr.es/c/18d2d8ae4)

  PostgreSQL versions before 18 allow an inherited column not-null constraint to be dropped. However, this results in a schema that cannot be restored, leading to failure in pg_upgrade. Detect such cases during pg_upgrade's preflight checks to allow users to fix them before initiating the upgrade.
* Avoid assertion failure if `track_commit_timestamp` is enabled during initdb (Hayato Kuroda, Andy Fan) [§](https://postgr.es/c/dcbbd4331)
* Fix pg_waldump to show information about dropped statistics in `PREPARE TRANSACTION` WAL records (Daniil Davydov) [§](https://postgr.es/c/0e0174b49)
* Avoid possible leak of the open connection during `contrib/dblink` connection establishment (Tom Lane) [§](https://postgr.es/c/09c9ae8f6)

  In the rare scenario where we hit out-of-memory while inserting the new connection object into dblink's hashtable, the open connection would be leaked until end of session, leaving an idle session sitting on the remote server.
* Make `contrib/pg_prewarm` cope with very large `shared_buffers` settings (Daria Shanina) [§](https://postgr.es/c/d59ff3be2)

  Autoprewarm failed with a memory allocation error if `shared_buffers` was larger than about 50 million buffers (400GB).
* In `contrib/pg_stat_statements`, avoid leaving gaps in the set of parameter numbers used in a normalized query (Sami Imseih) [§](https://postgr.es/c/130300a15)
* Fix memory leakage in `contrib/postgres_fdw`'s DirectModify methods (Tom Lane) [§](https://postgr.es/c/3c31594f5)

  The `PGresult` holding the results of the remote modify command would be leaked for the rest of the session if the query fails between invocations of the DirectModify methods, which could happen when there's `RETURNING` data to process.
* Ensure that directories listed in configure's `--with-includes` and `--with-libraries` options are searched before system-supplied directories (Tom Lane) [§](https://postgr.es/c/19857437b)

  A common reason for using these options is to allow a user-built version of some library to override the system-supplied version. However, that failed to work in some environments because of careless ordering of switches in the commands issued by the makefiles.
* Fix configure's checks for `__cpuid()` and `__cpuidex()` (Lukas Fittl, Michael Paquier) [§](https://postgr.es/c/d6ffc43f9)

  configure failed to detect these Windows-specific functions, so that they would not be used, leading to slower-than-necessary CRC computations since the availability of hardware instructions could not be verified. The practical impact of this error was limited, because production builds for Windows typically do not use the Autoconf toolchain.
* Fix build failure with `--with-pam` option on Solaris-based platforms (Tom Lane) [§](https://postgr.es/c/b252ce311)

  Solaris is inconsistent with other Unix platforms about the API for PAM authentication. This manifested as an “inconsistent pointer” compiler warning, which we never did anything about. But as of GCC 14 it's an error not warning by default, so fix it.
* Make our code portable to GNU Hurd (Michael Banck, Christoph Berg, Samuel Thibault) [§](https://postgr.es/c/0fb496c70)

  Fix assumptions about `IOV_MAX` and `O_RDONLY` that don't hold on Hurd.
* Make our usage of `memset_s()` conform strictly to the C11 standard (Tom Lane) [§](https://postgr.es/c/00652b3c9)

  This avoids compile failures on some platforms.
* Prevent uninitialized-value compiler warnings in JSONB comparison code (Tom Lane) [§](https://postgr.es/c/f32e45641)
* Avoid deprecation warnings when building with libxml2 2.14 and later (Michael Paquier) [§](https://postgr.es/c/75c1eb60b)
* Avoid problems when compiling `pg_locale.h` under C++ (John Naylor) [§](https://postgr.es/c/baacfb9e6)

  PostgreSQL header files generally need to be wrapped in `extern "C" { ... }` in order to be included in extensions written in C++. This failed for `pg_locale.h` because of its use of libicu headers, but we can work around that by suppressing C++-only declarations in those headers. C++ extensions that want to use libicu's C++ APIs can do so by including the libicu headers ahead of `pg_locale.h`.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/release-15-14.html)（英文原文，待翻譯）
