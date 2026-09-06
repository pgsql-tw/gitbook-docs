## E.2. Release 18.4 [#](#RELEASE-18-4)

[E.2.1. Migration to Version 18.4](release-18-4.md#RELEASE-18-4-MIGRATION)

[E.2.2. Changes](release-18-4.md#RELEASE-18-4-CHANGES)

**Release date:**2026-05-14

This release contains a variety of fixes from 18.3.
For information about new features in major release 18, see
[Section E.6](release-18.md).

<a id="RELEASE-18-4-MIGRATION"></a>

### E.2.1. Migration to Version 18.4 [#](#RELEASE-18-4-MIGRATION)

A dump/restore is not required for those running 18.X.

However, if you are upgrading from a version earlier than 18.2,
see [Section E.4](release-18-2.md).

<a id="RELEASE-18-4-CHANGES"></a>

### E.2.2. Changes [#](#RELEASE-18-4-CHANGES)

* Prevent unbounded recursion while processing startup packets
  (Michael Paquier)
  [§](https://postgr.es/c/f7a191f53)

  A malicious client could crash the connected backend by alternating
  rejected SSL and GSS encryption requests indefinitely.

  The PostgreSQL Project thanks Calif.io
  (in collaboration with Claude and Anthropic Research) for reporting
  this problem.
  (CVE-2026-6479)
* Fix assorted integer overflows in memory-allocation calculations
  (Tom Lane, Nathan Bossart, Heikki Linnakangas)
  [§](https://postgr.es/c/e1c30458a)
  [§](https://postgr.es/c/01e568b8c)
  [§](https://postgr.es/c/f3cee4dc4)
  [§](https://postgr.es/c/dd8af778d)
  [§](https://postgr.es/c/55328e3a9)
  [§](https://postgr.es/c/67dd6243d)
  [§](https://postgr.es/c/8d1489d50)
  [§](https://postgr.es/c/c7fb9f765)
  [§](https://postgr.es/c/3fbec9e50)

  Various places were incautious about the possibility of integer
  overflow in calculations of how much memory to allocate. Overflow
  would lead to allocating a too-small buffer which the caller would
  then write past the end of. This would at least trigger server
  crashes, and probably could be exploited for arbitrary code
  execution. In many but by no means all cases, the hazard exists
  only in 32-bit builds.

  The PostgreSQL Project thanks Xint Code,
  Bruce Dang, Sven Klemm, and Pavel Kohout for reporting these problems.
  (CVE-2026-6473)
* Properly quote subscription names
  in pg_createsubscriber (Nathan Bossart)
  [§](https://postgr.es/c/c2e44c370)

  The given subscription name was inserted into SQL commands without
  quoting, so that SQL injection could be achieved in the (perhaps
  unlikely) case that the subscription name comes from an untrusted
  source.

  The PostgreSQL Project thanks
  Yu Kunpeng for reporting this problem.
  (CVE-2026-6476)
* Properly quote object names in logical replication origin checks
  (Pavel Kohout)
  [§](https://postgr.es/c/cb35d7306)

  `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`
  interpolated schema and relation names into SQL commands without
  quoting them, allowing execution of arbitrary SQL on the publisher.

  The PostgreSQL Project thanks
  Pavel Kohout for reporting this problem.
  (CVE-2026-6638)
* Reject over-length options in `ts_headline()`
  (Michael Paquier)
  [§](https://postgr.es/c/62ad26266)

  The `StartSel`, `StopSel`
  and `FragmentDelimiter` strings must not exceed
  32Kb in length, but this was not checked for. An over-length value
  would typically crash the server.

  The PostgreSQL Project thanks
  Xint Code for reporting this problem.
  (CVE-2026-6473)
* Detect faulty input when restoring attribute MCV statistics
  (Michael Paquier)
  [§](https://postgr.es/c/661095c40)

  The statistics restore functions were insufficiently careful about
  validating most-common-value statistics, and would accept values
  that could crash the planner later on.

  The PostgreSQL Project thanks
  Jeroen Gui for reporting this problem.
  (CVE-2026-6575)
* Guard against malicious time zone names
  in `timeofday()`
  and `pg_strftime()` (Tom Lane)
  [§](https://postgr.es/c/ba27389c2)
  [§](https://postgr.es/c/c6e7a9ef3)

  A crafted time zone setting could pass `%`
  sequences to `snprintf()`, potentially causing
  crashes or disclosure of server memory. Another path to similar
  results was to overflow the limited-size output buffer used
  by `pg_strftime()`.

  The PostgreSQL Project thanks
  Xint Code for reporting this problem.
  (CVE-2026-6474)
* When creating a multirange type, ensure the user
  has `CREATE` privilege on the schema specified for
  the multirange type (Jelte Fennema-Nio)
  [§](https://postgr.es/c/a44780f41)

  The multirange type can be put into a different schema than its
  parent range type, but we neglected to apply the required privilege
  check when doing so.

  The PostgreSQL Project thanks
  Jelte Fennema-Nio for reporting this problem.
  (CVE-2026-6472)
* Use timing-safe string comparisons in authentication code
  (Michael Paquier)
  [§](https://postgr.es/c/d93ef4131)

  Use `timingsafe_bcmp()` instead
  of `memcmp()` or `strcmp()`
  when checking passwords, hashes, etc. It is not known whether the
  data dependency of those functions is usefully exploitable in any of
  these places, but in the interests of safety, replace them.

  The PostgreSQL Project thanks
  Joe Conway for reporting this problem.
  (CVE-2026-6478)
* Mark `PQfn()` as unsafe, and avoid using it
  within libpq (Nathan Bossart)
  [§](https://postgr.es/c/be0136440)

  For a non-integral result type, `PQfn()` is not
  passed the size of the output buffer, so it cannot check that the
  data returned by the server will fit. A malicious server could
  therefore overwrite client memory. This is unfixable without an
  API change, so mark the function as deprecated. Internally
  to libpq, use a variant version that can
  apply the missing check.

  The PostgreSQL Project thanks
  Yu Kunpeng and Martin Heistermann for reporting this problem.
  (CVE-2026-6477)
* Prevent path traversal in pg_basebackup
  and pg_rewind (Michael Paquier)
  [§](https://postgr.es/c/6a67c540a)

  These applications failed to validate output file paths read from
  their input, so that a malicious source could overwrite any file
  writable by these applications. Constrain where data can be written
  by rejecting paths that are absolute or contain parent-directory
  references.

  The PostgreSQL Project thanks XlabAI Team
  of Tencent Xuanwu Lab and Valery Gubanov for reporting this problem.
  (CVE-2026-6475)
* Guard against field overflow
  within `contrib/intarray`'s `query_int`
  type and `contrib/ltree`'s `ltxtquery`
  type (Tom Lane)
  [§](https://postgr.es/c/c5790ec4f)
  [§](https://postgr.es/c/05e73b5c3)

  Parsing of these query structures did not check for overflow of
  16-bit fields, so that construction of an invalid query tree was
  possible. This can crash the server when executing the query.

  The PostgreSQL Project thanks
  Xint Code for reporting this problem.
  (CVE-2026-6473)
* Guard against overly long values
  of `contrib/ltree`'s `lquery` type
  (Michael Paquier)
  [§](https://postgr.es/c/7f019f341)

  Values with more than 64K items caused internal overflows,
  potentially resulting in stack smashes or wrong answers.

  The PostgreSQL Project thanks
  Vergissmeinnicht, A1ex, and Jihe Wang
  for reporting this problem.
  (CVE-2026-6473)
* Prevent SQL injection and buffer overruns
  in `contrib/spi` (Nathan Bossart)
  [§](https://postgr.es/c/1ebda7da9)

  `check_foreign_key()` was insufficiently careful
  about quoting key values, and also used fixed-length buffers for
  constructing queries. While this module is only meant as example
  code, it still shouldn't contain such dangerous errors.

  The PostgreSQL Project thanks
  Nikolay Samokhvalov for reporting this problem.
  (CVE-2026-6637)
* Check for nondeterministic collations before assuming that an
  equality condition on a collatable type implies uniqueness
  (Richard Guo)
  [§](https://postgr.es/c/e8fd5e579)
  [§](https://postgr.es/c/1132af22c)
  [§](https://postgr.es/c/5c214b58b)
  [§](https://postgr.es/c/b62f514ac)
  [§](https://postgr.es/c/bed3ffbf9)

  Numerous planner optimizations assume that, for example, at most one
  table row can satisfy `WHERE x = 'abc'` if there is
  a unique index on `x`. However this conclusion is
  unsafe in general if the index and the `WHERE`
  clause have different collations attached. It is safe when both
  collations are deterministic, because that property essentially
  requires that equality of two strings means bitwise equality. But
  nondeterministic collations don't act that way, so that optimizing
  on the assumption of unique matches can give wrong query answers if
  either the `WHERE` clause or the index has a
  nondeterministic collation.
* Fix incomplete removal of relation references
  in `RestrictInfo` structs during join removal
  (Tom Lane)
  [§](https://postgr.es/c/16fb94605)

  This oversight has been shown to result in planner failures such as
  unexpected “FULL JOIN is only supported with merge-joinable or
  hash-joinable join conditions” errors. It may also have
  caused failure to consider valid plans in other cases.
* Improve planner's matching of partition key columns to sub-query
  outputs (Richard Guo)
  [§](https://postgr.es/c/8e8b2bef7)

  Strip no-op PlaceHolderVars from operands before comparing them to
  partition keys. This change enables partition pruning to succeed in
  some cases where it previously failed to recognize that a partition
  need not be scanned.
* Fix self-join removal to handle join clauses that are bare boolean
  columns, e.g. `ON t1.boolcol` (Andrei Lepikhov,
  Tender Wang, Alexander Korotkov)
  [§](https://postgr.es/c/e8b9d6497)

  Previously such a case led to a “no relation entry
  for relid *`N`*” error.
* Fix `UPDATE/DELETE ... WHERE CURRENT OF` to work on
  tables with virtual generated columns (Satyanarayana Narlapuram,
  Dean Rasheed)
  [§](https://postgr.es/c/f3d03fbd5)
* Fix expansion of virtual generated columns
  in `EXCLUDED` column references in `INSERT
  ... ON CONFLICT` (Satyanarayana Narlapuram, Dean Rasheed)
  [§](https://postgr.es/c/cf38dedf6)
* Fix incorrect handling of `NEW` generated columns
  in rule actions and rule qualifications (Richard Guo, Dean Rasheed)
  [§](https://postgr.es/c/e528bfe97)

  Previously, such column references would produce NULL
  in `INSERT` cases, or be equivalent to
  the `OLD` value in `UPDATE` cases.
* Fix spurious “indexes on virtual generated columns are not
  supported” errors (Robert Haas)
  [§](https://postgr.es/c/cceb9c18a)

  Creation of an expression index could sometimes incorrectly report
  this error.
* Fix spurious “generated columns are not supported in COPY FROM
  WHERE conditions” errors (Tom Lane)
  [§](https://postgr.es/c/11c2c0cc8)

  Use of a system column in a `COPY FROM WHERE`
  condition could sometimes incorrectly report this error.
* Correctly report a serialization failure
  when `MERGE` encounters a concurrently-updated
  tuple in repeatable-read or serializable mode (Tender Wang)
  [§](https://postgr.es/c/13fab378e)

  Previously, such cases behaved the same as in lower isolation
  levels.
* Fix `CREATE TABLE ... LIKE ... INCLUDING
  STATISTICS` for cases where the source table has dropped
  column(s) (Julien Tachoires)
  [§](https://postgr.es/c/149c875fc)

  In such cases, extended statistics objects could be copied
  incorrectly, or the command could give an incorrect error.
* Allow `ALTER INDEX ... ATTACH PARTITION` to mark
  the parent index valid if appropriate (Sami Imseih)
  [§](https://postgr.es/c/5713ac248)

  There are edge cases in which a partitioned index might remain
  marked as invalid even when all its leaf indexes are valid. This
  change provides a mechanism whereby a user can correct such a
  situation without resorting to manual catalog updates.
* Fix `ALTER TABLE ... SET NOT NULL` to invoke
  object-access hook functions only after completing the catalog
  change (Artur Zakirov)
  [§](https://postgr.es/c/6958077ce)
* Fix `ALTER FOREIGN DATA WRAPPER` to not drop the
  wrapper object's dependency on its handler function (Jeff Davis)
  [§](https://postgr.es/c/c11f87b1a)
* Fix loss of deferrability of foreign-key triggers (Yasuo Honda)
  [§](https://postgr.es/c/5db5e3396)

  Previously, a foreign key defined as `DEFERRABLE INITIALLY
  DEFERRED` would behave as `NOT DEFERRABLE`
  after being set to `NOT ENFORCED` status and then
  back to `ENFORCED`.

  If you have a foreign key with this problem, it can be repaired
  (after installing this update) by again setting it to `NOT
  ENFORCED` and then back to `ENFORCED`.
* Fix `WITHOUT OVERLAPS` to allow domains (Jian He)
  [§](https://postgr.es/c/49f3cb453)

  `UNIQUE/PRIMARY KEY ... WITHOUT OVERLAPS` requires
  the no-overlap column to be a range or multirange, but it should
  allow a domain over such a type too.
* Disallow making a composite type be a member of itself via a
  multirange (Heikki Linnakangas)
  [§](https://postgr.es/c/ff8f27d6e)

  We already forbade such cases when the intermediate type is a
  domain, array, composite type, or range; but multiranges were
  overlooked.
* Fix datum-image comparisons to be insensitive to sign-extension
  variations (David Rowley)
  [§](https://postgr.es/c/49315de0c)

  This fixes some situations that previously led to “could not
  find memoization table entry” errors or wrong query results.
* Fix incorrect logic for hashed `IN`/`NOT
  IN` with non-strict equality operator (Chengpeng Yan)
  [§](https://postgr.es/c/035c520db)

  The previous coding could crash or give wrong answers. All built-in
  data types have strict equality operators, so that this issue could
  only arise with an extension data type.
* Truncate overly-long locale-specific numeric symbols
  in `to_char()` (Tom Lane)
  [§](https://postgr.es/c/580e7be88)

  If a locale specified a currency symbol, thousands separator, or
  decimal or sign symbol more than 8 bytes long, a buffer overrun was
  possible. No such locales exist in the real world, and it's
  impractical for an unprivileged attacker to install a malicious
  locale definition underneath a Postgres server; but for safety's
  sake check for overlength symbols and truncate if needed.
* Prevent buffer overruns when parsing an affix file for
  an `Ispell` dictionary (Tom Lane)
  [§](https://postgr.es/c/00c6e0819)
  [§](https://postgr.es/c/c2bfeb3bb)

  A corrupt or malicious affix file could crash the server.
  This is not considered a security issue because text search
  configuration files are presumed trustworthy, but it still seems
  worth fixing.
* Guard against integer overflow in calculations of frame start and
  end positions for window aggregates (Richard Guo)
  [§](https://postgr.es/c/bfc7dff26)

  Very large user-specified offsets (close to INT64_MAX) could result
  in errors or incorrect query results.
* Fix `array_agg_array_combine()` to combine the
  arrays' null bitmaps correctly (Dmytro Astapov)
  [§](https://postgr.es/c/14bf2c39e)

  This mistake resulted in sometimes-incorrect output from
  parallelized `array_agg(anyarray)` calculations.
* Retry `sync_file_range()` if it returns error
  code `EINTR` (DaeMyung Kang)
  [§](https://postgr.es/c/6cb307251)
* Fix incorrect behavior
  of `pg_stat_reset_single_table_counters()` on a
  shared catalog (Chao Li)
  [§](https://postgr.es/c/b081c5b07)

  Such cases had a side-effect of resetting the
  current database's `stat_reset_timestamp`, which
  was unintended.
* Update activity statistics when a parallel apply worker is idle
  (Zhijie Hou)
  [§](https://postgr.es/c/44c8dc280)

  Previously, statistics from a recently-completed transaction might
  go unreported for long intervals, particularly if the workload is
  light.
* Fix “no relation entry for relid 0” failure while
  estimating array lengths in set operations (Tender Wang)
  [§](https://postgr.es/c/13e20d1c9)
* Fix buffer overread when `pglz_decompress()`
  receives corrupt input (Andrew Dunstan)
  [§](https://postgr.es/c/c3e436b1c)

  It was possible to read a few bytes past the end of the input, which
  in very unlucky cases might cause a crash.
* Fix incremental JSON parser's handling of numeric tokens that cross
  input buffer boundaries (Andrew Dunstan)
  [§](https://postgr.es/c/3e4955630)

  It was possible to accept an incorrectly-formatted number, leading
  to failures later.
* Prevent bloating relation visibility maps during restore of an
  incremental backup (Robert Haas)
  [§](https://postgr.es/c/9540c0e5d)

  Restore could append many blocks of zeroes to a visibility map, due
  to incorrect computation of the expected file length. This does not
  result in data corruption, but it could waste a substantial amount
  of disk space.
* Use C collation, not the database's default collation, in catalog
  cache lookups on text columns (Jeff Davis)
  [§](https://postgr.es/c/03c4f243e)

  This avoids failures in edge cases such as physical replication
  startup, where there is no identified database so that a default
  collation cannot be determined.
* Prevent stuck slotsync worker processes from blocking promotion of a
  standby server (Nisha Moond, Ajin Cherian)
  [§](https://postgr.es/c/58c1188a3)
  [§](https://postgr.es/c/acf49bfed)
  [§](https://postgr.es/c/94efd308b)

  A worker process that was vainly waiting for a response from the
  primary would delay promotion for an unreasonable amount of time.
* Fix excessive log output from idle slotsync worker processes
  (Zhijie Hou)
  [§](https://postgr.es/c/540fe8fb5)
* Ensure that tuplestore data structures are internally consistent
  even after an error (Tom Lane)
  [§](https://postgr.es/c/adb7873bb)

  The code was previously careless about this, which is fine most of
  the time but is problematic for the tuplestore backing
  a `WITH HOLD` cursor. In v15 and before this
  leads to easily-reproducible crashes; later branches are not known
  to be vulnerable, but it seems best to preserve consistency in all.
* Make the `pg_aios` system
  view's `pid` column show NULL not
  0 when an entry has no owning process (ChangAo Chen)
  [§](https://postgr.es/c/882bdcf9f)
* Fix premature NULL lag reporting
  in `pg_stat_replication` (Shinya Kato)
  [§](https://postgr.es/c/98e96e579)

  The lag columns frequently read as NULL even while replication
  activity was happening.
* Fix under-allocation of shared memory used for parallel btree index
  scans (Siddharth Kothari)
  [§](https://postgr.es/c/1e71970d2)

  In edge cases this could result in a server crash.
* Avoid rare flush failure when working with non-WAL-logged GiST
  indexes (Tomas Vondra)
  [§](https://postgr.es/c/5b3f63a1b)

  A non-logged GiST index could nonetheless sometimes
  produce “xlog flush request *`n/nnnn`*
  is not satisfied” errors, due to incorrect selection of
  a “fake LSN” to represent an insertion point.
* Fix underestimate of required size of DSA page maps for odd-size
  segments (Paul Bunn)
  [§](https://postgr.es/c/a0f38604d)

  This miscalculation led to out-of-bounds accesses and hence server
  crashes.
* Fix indexing of oldest-multixact arrays in shared memory
  (Yura Sokolov)
  [§](https://postgr.es/c/0a50ef094)
  [§](https://postgr.es/c/fa3b328e6)

  This mistake could cause a prepared-but-not-yet-committed
  transaction's row locks to appear invisible to other sessions, or
  other visibility issues for the results of such a transaction.
  With a very small max_connections setting, memory stomps were also
  possible.
* Fix array overrun when too many `EXPLAIN` extension
  options are installed (Joel Jacobson)
  [§](https://postgr.es/c/730c98d03)
* Fix possible server crash when processing extended statistics on
  expressions of extension data types (Michael Paquier)
  [§](https://postgr.es/c/83671c0da)

  NULL pointer dereferences were possible if the data type's
  typanalyze function does not compute any useful statistics.
  No in-core typanalyze function behaves that way, but extensions
  could.
* Correctly display join alias Vars that are used in `GROUP
  BY` (Tom Lane)
  [§](https://postgr.es/c/c2c1962a6)

  In views containing queries like `SELECT ... t1 LEFT JOIN t2
  USING (x) GROUP BY x`, the `GROUP BY`
  clause could be displayed incorrectly by deparsing, leading to
  dump/restore failures. Failures occurred only
  if `t1.x` and `t2.x` were not of
  identical data types and `t1.x` was the side that
  required an implicit coercion.
* Fix minor memory leaks in ICU-based string processing (Jeff Davis)
  [§](https://postgr.es/c/4abf63c62)
* If the startup process fails, properly shut down other child
  processes before exiting the postmaster (Ayush Tiwari)
  [§](https://postgr.es/c/affdb2dd5)

  The handling of this situation relied on a long-obsolete assumption
  that no other postmaster children exist while the startup process is
  running, so that immediate postmaster exit is acceptable.
  Orphaned children would eventually notice the postmaster's death and
  exit on their own, but a cleaner shutdown procedure is desirable.
* Fix race condition between WAL replay of checkpoints and multixact
  ID creations (Heikki Linnakangas)
  [§](https://postgr.es/c/0852643e1)

  A standby server following WAL from a primary of an older minor
  version could get into a crash-and-restart loop complaining
  about “could not access status of transaction”.
* Prevent indefinite wait in shutdown of a walsender process
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/3eb2fecdb)
  [§](https://postgr.es/c/980498138)

  At shutdown of a cluster that is publishing logical replication
  data, the walsender waits for all pending WAL to be written out.
  But it did not correctly request that to happen, so that in some
  cases this could become an indefinite wait.
* Ensure that changes to tables' free space maps are persisted during
  recovery (Alexey Makhmutov)
  [§](https://postgr.es/c/ac3b97db3)

  Previously, while WAL replay did update the free space map while
  replaying operations that should change it, the map page buffer did
  not get marked dirty if checksums are enabled, so that the changes
  might never get written out. On a standby server, over time this
  would result in a map wildly at variance with the table's actual
  contents. While the map is only used as a hint, this condition
  could cause significant performance degradation for some period of
  time after the standby server is promoted to be active, until most
  of the map has been repaired by updates.
* Fix crashes in some ecpg functions when
  called without any established connection (Shruthi Gowda)
  [§](https://postgr.es/c/e2688ea5e)
* Harden tar-file parsing logic against archives it can't handle
  (Tom Lane)
  [§](https://postgr.es/c/698eae7db)

  The tar-file reading code used
  in pg_basebackup
  and pg_verifybackup failed to verify that
  the input is a tar file at all, let alone that it fits into the
  subset of valid tar files that we can handle. This isn't a problem
  for the normal scenario where the input file was generated
  by PostgreSQL code, but it can be an
  issue if the input has been generated by some
  other tar program.
* Fix assorted bugs in backup decompression and tar-parsing code
  (Andrew Dunstan, Tom Lane, Chao Li)
  [§](https://postgr.es/c/5095f3f4a)
  [§](https://postgr.es/c/a01a592b1)
  [§](https://postgr.es/c/78dc9a808)

  The decompression and tar-file reading code used
  in pg_basebackup
  and pg_verifybackup mishandled tar-file
  padding data, could corrupt LZ4-compressed data in edge cases,
  failed to check for some unusual error conditions, failed to exit
  after compression/decompression errors (leading to cascading error
  reports), and leaked memory.
* In pg_dump, preserve `NO
  INHERIT` property of `NOT NULL`
  constraints (Jian He)
  [§](https://postgr.es/c/c3c8b63d7)

  Some cases missed printing the `NO INHERIT` clause.
* In pg_dumpall, don't skip
  role `GRANT`s with dangling grantor OIDs
  (Tom Lane)
  [§](https://postgr.es/c/b09158cc7)

  Instead, handle such cases by emitting `GRANT`
  without any `GRANTED BY` clause, as we did before
  v16. This avoids losing the grant in foreseeable cases, since
  pre-v16 servers didn't prevent dropping the grantor role. Continue
  to emit a warning about the missing grantor, but only if the source
  server is v16 or later.
* In pg_upgrade, take care to use the
  correct protocol version when connecting to older source servers
  (Jacob Champion)
  [§](https://postgr.es/c/1b2773179)

  This could be problematic when attempting to upgrade from a pre-2018
  server.
* In `contrib/basic_archive`, allow the archive
  directory to be missing at startup (Nathan Bossart)
  [§](https://postgr.es/c/bde9ad315)

  Previously, the setting
  of `basic_archive.archive_directory` was rejected
  if it didn't point to an existing directory. This is undesirable
  because archiving will be stuck indefinitely, even if the directory
  appears later.
* Fix `contrib/ltree` to cope when case-folding
  changes a string's byte length (Jeff Davis)
  [§](https://postgr.es/c/b3c2a3d38)
  [§](https://postgr.es/c/53a57cae1)

  Previously, `lquery` patterns specifying case-insensitive
  matching might fail to match labels they should match.
* Fix mis-structured output
  from `contrib/pg_overexplain`'s
  `RANGE_TABLE` option (Satyanarayana Narlapuram)
  [§](https://postgr.es/c/6723d462d)

  Some fields were misplaced in JSON, YAML, and XML formats, resulting
  in structurally invalid output.
* In `contrib/pg_stat_statements`, don't leak
  memory if an error occurs while parsing the
  `pgss_query_texts.stat` file (Heikki Linnakangas)
  [§](https://postgr.es/c/25b02320e)
* In `contrib/postgres_fdw`, avoid crash due to
  premature cleanup of a failed connection (Etsuro Fujita)
  [§](https://postgr.es/c/c318777da)

  If a remote connection fails abort cleanup, we can't use it any
  longer. But delay closing the connection object until end of
  transaction, because there might still be references to it within
  data structures such as open cursors.
* Update time zone data files to tzdata
  release 2026b (Tom Lane)
  [§](https://postgr.es/c/8a431b6d6)

  British Columbia (America/Vancouver) will be on year-round UTC-07
  (effectively, permanent DST) beginning in November 2026. This
  release assumes that their TZ abbreviation will
  be `MST` from that time forward. That seems likely
  to change, but it's unclear what new abbreviation will be used.
  Also a historical correction for Moldova: they have followed EU DST
  transition times since 2022.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-4.html)（英文原文，待翻譯）
