# E.1. Release 13.3

**Release date:** 2021-05-13

This release contains a variety of fixes from 13.2. For information about new features in major release 13, see [Section E.4](https://www.postgresql.org/docs/13/release-13.html).

#### E.1.1. Migration to Version 13.3

A dump/restore is not required for those running 13.X.

However, if you are upgrading from a version earlier than 13.2, see [Section E.2](https://www.postgresql.org/docs/13/release-13-2.html).

#### E.1.2. Changes

* Prevent integer overflows in array subscripting calculations \(Tom Lane\)

  The array code previously did not complain about cases where an array's lower bound plus length overflows an integer. This resulted in later entries in the array becoming inaccessible \(since their subscripts could not be written as integers\), but more importantly it confused subsequent assignment operations. This could lead to memory overwrites, with ensuing crashes or unwanted data modifications. \(CVE-2021-32027\)

* Fix mishandling of “junk” columns in `INSERT ... ON CONFLICT ... UPDATE` target lists \(Tom Lane\)

  If the `UPDATE` list contains any multi-column sub-selects \(which give rise to junk columns in addition to the results proper\), the `UPDATE` path would end up storing tuples that include the values of the extra junk columns. That's fairly harmless in the short run, but if new columns are added to the table then the values would become accessible, possibly leading to malfunctions if they don't match the datatypes of the added columns.

  In addition, in versions supporting cross-partition updates, a cross-partition update triggered by such a case had the reverse problem: the junk columns were removed from the target list, typically causing an immediate crash due to malfunction of the multi-column sub-select mechanism. \(CVE-2021-32028\)

* Fix possibly-incorrect computation of `UPDATE ... RETURNING` outputs for joined cross-partition updates \(Amit Langote, Etsuro Fujita\)

  If an `UPDATE` for a partitioned table caused a row to be moved to another partition with a physically different row type \(for example, one with a different set of dropped columns\), computation of `RETURNING` results for that row could produce errors or wrong answers. No error is observed unless the `UPDATE` involves other tables being joined to the target table. \(CVE-2021-32029\)

* Fix adjustment of constraint deferrability properties in partitioned tables \(Álvaro Herrera\)

  When applied to a foreign-key constraint of a partitioned table, `ALTER TABLE ... ALTER CONSTRAINT` failed to adjust the `DEFERRABLE` and/or `INITIALLY DEFERRED` markings of the constraints and triggers of leaf partitions. This led to unexpected behavior of such constraints. After updating to this version, any misbehaving partitioned tables can be fixed by executing a new `ALTER` command to set the desired properties.

  This change also disallows applying such an `ALTER` directly to the constraints of leaf partitions. The only supported case is for the whole partitioning hierarchy to have identical constraint properties, so such `ALTER`s must be applied at the partition root.

* When attaching a child table with `ALTER TABLE ... INHERIT`, insist that any generated columns in the parent be generated the same way in the child \(Peter Eisentraut\)
* Forbid marking an identity column as nullable \(Vik Fearing\)

  `GENERATED ALWAYS AS IDENTITY` implies `NOT NULL`, so don't allow it to be combined with an explicit `NULL` specification.

* Allow `ALTER ROLE/DATABASE ... SET` to set the `role`, `session_authorization`, and `temp_buffers` parameters \(Tom Lane\)

  Previously, over-eager validity checks might reject these commands, even if the values would have worked when used later. This created a command ordering hazard for dump/reload and upgrade scenarios.

* Ensure that `REINDEX CONCURRENTLY` preserves any statistics target that's been set for the index \(Michael Paquier\)
* Fix `COMMIT AND CHAIN` to work correctly when the current transaction has live savepoints \(Fujii Masao\)
* Fix list-manipulation bug in `WITH RECURSIVE` processing \(Michael Paquier, Tom Lane\)

  Sufficiently deep nesting of `WITH` constructs \(at least seven levels\) triggered core dumps or incorrect complaints of faulty `WITH` nesting.

* Fix bug with coercing the result of a `COLLATE` expression to a non-collatable type \(Tom Lane\)

  This led to a parse tree in which the `COLLATE` appears to be applied to a non-collatable value. While that normally has no real impact \(since `COLLATE` has no effect at runtime\), it was possible to construct views that would be rejected during dump/reload.

* Fix use-after-free bug in saving tuples for `AFTER` triggers \(Amit Langote\)

  This could cause crashes in some situations.

* Disallow calling window functions and procedures via the “fast path” wire protocol message \(Tom Lane\)

  Only plain functions are supported here. While trying to call an aggregate function failed already, calling a window function would crash, and calling a procedure would work only if the procedure did no transaction control.

* Extend `pg_identify_object_as_address()` to support event triggers \(Joel Jacobson\)
* Fix `to_char()`'s handling of Roman-numeral month format codes with negative intervals \(Julien Rouhaud\)

  Previously, such cases would usually cause a crash.

* Check that the argument of `pg_import_system_collations()` is a valid schema OID \(Tom Lane\)
* Fix use of uninitialized value while parsing an `\{`_`m`_,_`n`_\} quantifier in a BRE-mode regular expression \(Tom Lane\)

  This error could cause the quantifier to act non-greedy, that is behave like an `{`_`m`_,_`n`_}? quantifier would do in full regular expressions.

* Fix “could not find pathkey item to sort” planner errors in some situations where the sort key involves an aggregate or window function \(James Coleman, Tom Lane\)
* Don't ignore system columns when estimating the number of groups using extended statistics \(Tomas Vondra\)

  This led to strange estimates for queries such as `SELECT ... GROUP BY a, b, ctid`.

* Avoid divide-by-zero when estimating selectivity of a regular expression with a very long fixed prefix \(Tom Lane\)

  This typically led to a `NaN` selectivity value, causing assertion failures or strange planner behavior.

* Fix access-off-the-end-of-the-table error in BRIN index bitmap scans \(Tomas Vondra\)

  If the page range size used by a BRIN index isn't a power of two, there were corner cases in which a bitmap scan could try to fetch pages past the actual end of the table, leading to “could not open file” errors.

* Fix potentially wrong answers from GIN `tsvector` index searches, when there are many matching tuples \(Tom Lane\)

  If the number of index matches became large enough to make the bitmap holding them become lossy \(a threshold that depends on `work_mem`\), the code could get confused about whether rechecks are required, allowing rows to be returned that don't actually match the query.

* Fix concurrency issues with WAL segment recycling on Windows \(Michael Paquier\)

  This reverts a change that caused intermittent “could not rename file ...: Permission denied” log messages. While there were not serious consequences, the log spam was annoying.

* Avoid incorrect timeline change while recovering uncommitted two-phase transactions from WAL \(Soumyadeep Chakraborty, Jimmy Yih, Kevin Yeap\)

  This error could lead to subsequent WAL records being written under the wrong timeline ID, leading to consistency problems, or even complete failure to be able to restart the server, later on.

* Ensure that locks are released while shutting down a standby server's startup process \(Fujii Masao\)

  When a standby server is shut down while still in recovery, some locks might be left held. This causes assertion failures in debug builds; it's unclear whether any serious consequence could occur in production builds.

* Fix crash when a logical replication worker does `ALTER SUBSCRIPTION REFRESH` \(Peter Smith\)

  The core code won't do this, but a replica trigger could.

* Ensure we default to `wal_sync_method` = `fdatasync` on recent FreeBSD \(Thomas Munro\)

  FreeBSD 13 supports `open_datasync`, which would normally become the default choice. However, it's unclear whether that is actually an improvement for Postgres, so preserve the existing default for now.

* Disable the `vacuum_cleanup_index_scale_factor` parameter and storage option \(Peter Geoghegan\)

  The notion of tracking “stale” index statistics proved to interact badly with the `autovacuum_vacuum_insert_threshold` parameter, resulting in unnecessary full-index scans and consequent degradation of autovacuum performance. The latter mechanism seems superior, so remove the stale-statistics logic. The control parameter for that, `vacuum_cleanup_index_scale_factor`, will be removed entirely in v14. In v13, it remains present to avoid breaking existing configuration files, but it no longer does anything.

* Pass the correct trigger OID to object post-alter hooks during `ALTER CONSTRAINT` \(Álvaro Herrera\)

  When updating trigger properties during `ALTER CONSTRAINT`, the post-alter hook was told that we are updating a trigger, but the constraint's OID was passed instead of the trigger's.

* Ensure we finish cleaning up when interrupted while detaching a DSM segment \(Thomas Munro\)

  This error could result in temporary files not being cleaned up promptly after a parallel query.

* Fix assorted minor memory leaks in the server \(Tom Lane, Andres Freund\)
* Fix uninitialized variable in walreceiver's statistics in shared memory \(Fujii Masao\)

  This error was harmless on most platforms, but could cause issues on platforms lacking atomic variables and/or spinlock support.

* Reduce the overhead of dtrace probes for LWLock operations, when dtrace support is compiled in but not active \(Peter Eisentraut\)
* Fix failure when a PL/pgSQL `DO` block makes use of both composite-type variables and transaction control \(Tom Lane\)

  Previously, such cases led to errors about leaked tuple descriptors.

* Prevent infinite loop in libpq if a ParameterDescription message with a corrupt length is received \(Tom Lane\)
* When initdb prints instructions about how to start the server, make the path shown for pg\_ctl use backslash separators on Windows \(Nitin Jadhav\)
* Fix psql to restore the previous behavior of `\connect service=`_`something`_ \(Tom Lane\)

  A previous bug fix caused environment variables \(such as `PGPORT`\) to override entries in the service file in this context. Restore the previous behavior, in which the priority is the other way around.

* Fix psql's `ON_ERROR_ROLLBACK` feature to handle `COMMIT AND CHAIN` commands correctly \(Arthur Nascimento\)

  Previously, this case failed with “savepoint "pg\_psql\_temporary\_savepoint" does not exist”.

* In psql, avoid repeated “could not print result table” failures after the first such error \(Álvaro Herrera\)
* Fix race condition in detection of file modification by psql's `\e` and related commands \(Laurenz Albe\)

  A very fast typist could fool the code's file-timestamp-based detection of whether the temporary edit file was changed.

* Fix pg\_dump's dumping of generated columns in partitioned tables \(Peter Eisentraut\)

  A fix introduced in the previous minor release should not be applied to partitioned tables, only traditionally-inherited tables.

* Fix missed file version check in pg\_restore \(Tom Lane\)

  When reading a custom-format archive from a non-seekable source, pg\_restore neglected to check the archive version. If it was fed a newer archive version than it can support, it would fail messily later on.

* Add some more checks to pg\_upgrade for user tables containing non-upgradable data types \(Tom Lane\)

  Fix detection of some cases where a non-upgradable data type is embedded within a container type \(such as an array or range\). Also disallow upgrading when user tables contain columns of system-defined composite types, since those types' OIDs are not stable across versions.

* Fix incorrect progress-reporting calculation in pg\_checksums \(Shinya Kato\)
* Fix pg\_waldump to count `XACT` records correctly when generating per-record statistics \(Kyotaro Horiguchi\)
* Fix `contrib/amcheck` to not complain about the tuple flags `HEAP_XMAX_LOCK_ONLY` and `HEAP_KEYS_UPDATED` both being set \(Julien Rouhaud\)

  This is a valid state after `SELECT FOR UPDATE`.

* Adjust VPATH build rules to support recent Oracle Developer Studio compiler versions \(Noah Misch\)
* Fix testing of PL/Python for Python 3 on Solaris \(Noah Misch\)

