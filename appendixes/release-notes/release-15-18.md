<a id="RELEASE-15-18"></a>

# E.2. Release 15.18

[E.2.1. Migration to Version 15.18](#id-1.11.6.7.4)

[E.2.2. Changes](#id-1.11.6.7.5)

<strong>Release date: </strong>2026-05-14

This release contains a variety of fixes from 15.17. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.7.4"></a>

## E.2.1. Migration to Version 15.18

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.14, see [Section E.6](release-15-14.md).

<a id="id-1.11.6.7.5"></a>

## E.2.2. Changes

* Prevent unbounded recursion while processing startup packets (Michael Paquier) [§](https://postgr.es/c/3fb66d302) [§](https://postgr.es/c/16fda4df6)

  A malicious client could crash the connected backend by alternating rejected SSL and GSS encryption requests indefinitely.

  The PostgreSQL Project thanks Calif.io (in collaboration with Claude and Anthropic Research) for reporting this problem. (CVE-2026-6479)
* Fix assorted integer overflows in memory-allocation calculations (Tom Lane, Nathan Bossart, Heikki Linnakangas) [§](https://postgr.es/c/bfc5cea76) [§](https://postgr.es/c/4032c9d98) [§](https://postgr.es/c/7fdb0907e) [§](https://postgr.es/c/fb0bc321d) [§](https://postgr.es/c/137013f60) [§](https://postgr.es/c/e49e9590d) [§](https://postgr.es/c/b11c3eadf) [§](https://postgr.es/c/d75b1dc96) [§](https://postgr.es/c/d106295b6) [§](https://postgr.es/c/dc6c85ff4)

  Various places were incautious about the possibility of integer overflow in calculations of how much memory to allocate. Overflow would lead to allocating a too-small buffer which the caller would then write past the end of. This would at least trigger server crashes, and probably could be exploited for arbitrary code execution. In many but by no means all cases, the hazard exists only in 32-bit builds.

  The PostgreSQL Project thanks Xint Code, Bruce Dang, Sven Klemm, and Pavel Kohout for reporting these problems. (CVE-2026-6473)
* Reject over-length options in `ts_headline()` (Michael Paquier) [§](https://postgr.es/c/7fe365693)

  The `StartSel`, `StopSel` and `FragmentDelimiter` strings must not exceed 32Kb in length, but this was not checked for. An over-length value would typically crash the server.

  The PostgreSQL Project thanks Xint Code for reporting this problem. (CVE-2026-6473)
* Guard against malicious time zone names in `timeofday()` and `pg_strftime()` (Tom Lane) [§](https://postgr.es/c/126a236ba) [§](https://postgr.es/c/c3fff3950)

  A crafted time zone setting could pass `%` sequences to `snprintf()`, potentially causing crashes or disclosure of server memory. Another path to similar results was to overflow the limited-size output buffer used by `pg_strftime()`.

  The PostgreSQL Project thanks Xint Code for reporting this problem. (CVE-2026-6474)
* When creating a multirange type, ensure the user has `CREATE` privilege on the schema specified for the multirange type (Jelte Fennema-Nio) [§](https://postgr.es/c/08c397b02)

  The multirange type can be put into a different schema than its parent range type, but we neglected to apply the required privilege check when doing so.

  The PostgreSQL Project thanks Jelte Fennema-Nio for reporting this problem. (CVE-2026-6472)
* Use timing-safe string comparisons in authentication code (Michael Paquier) [§](https://postgr.es/c/c95275f18) [§](https://postgr.es/c/9dcfcb92f)

  Use `timingsafe_bcmp()` instead of `memcmp()` or `strcmp()` when checking passwords, hashes, etc. It is not known whether the data dependency of those functions is usefully exploitable in any of these places, but in the interests of safety, replace them.

  The PostgreSQL Project thanks Joe Conway for reporting this problem. (CVE-2026-6478)
* Mark `PQfn()` as unsafe, and avoid using it within libpq (Nathan Bossart) [§](https://postgr.es/c/e3a1f83ea)

  For a non-integral result type, `PQfn()` is not passed the size of the output buffer, so it cannot check that the data returned by the server will fit. A malicious server could therefore overwrite client memory. This is unfixable without an API change, so mark the function as deprecated. Internally to libpq, use a variant version that can apply the missing check.

  The PostgreSQL Project thanks Yu Kunpeng and Martin Heistermann for reporting this problem. (CVE-2026-6477)
* Prevent path traversal in pg_basebackup and pg_rewind (Michael Paquier) [§](https://postgr.es/c/0c83fe8e4)

  These applications failed to validate output file paths read from their input, so that a malicious source could overwrite any file writable by these applications. Constrain where data can be written by rejecting paths that are absolute or contain parent-directory references.

  The PostgreSQL Project thanks XlabAI Team of Tencent Xuanwu Lab and Valery Gubanov for reporting this problem. (CVE-2026-6475)
* Guard against field overflow within `contrib/intarray`'s `query_int` type and `contrib/ltree`'s `ltxtquery` type (Tom Lane) [§](https://postgr.es/c/84a9f2641) [§](https://postgr.es/c/fc1fd3d97)

  Parsing of these query structures did not check for overflow of 16-bit fields, so that construction of an invalid query tree was possible. This can crash the server when executing the query.

  The PostgreSQL Project thanks Xint Code for reporting this problem. (CVE-2026-6473)
* Guard against overly long values of `contrib/ltree`'s `lquery` type (Michael Paquier) [§](https://postgr.es/c/9c2fa5b6a)

  Values with more than 64K items caused internal overflows, potentially resulting in stack smashes or wrong answers.

  The PostgreSQL Project thanks Vergissmeinnicht, A1ex, and Jihe Wang for reporting this problem. (CVE-2026-6473)
* Prevent SQL injection and buffer overruns in `contrib/spi` (Nathan Bossart) [§](https://postgr.es/c/8053235ab)

  `check_foreign_key()` was insufficiently careful about quoting key values, and also used fixed-length buffers for constructing queries. While this module is only meant as example code, it still shouldn't contain such dangerous errors.

  The PostgreSQL Project thanks Nikolay Samokhvalov for reporting this problem. (CVE-2026-6637)
* Check for nondeterministic collations before assuming that an equality condition on a collatable type implies uniqueness (Richard Guo) [§](https://postgr.es/c/872c9fae7) [§](https://postgr.es/c/bab4f7fa5)

  Numerous planner optimizations assume that, for example, at most one table row can satisfy `WHERE x = 'abc'` if there is a unique index on `x`. However this conclusion is unsafe in general if the index and the `WHERE` clause have different collations attached. It is safe when both collations are deterministic, because that property essentially requires that equality of two strings means bitwise equality. But nondeterministic collations don't act that way, so that optimizing on the assumption of unique matches can give wrong query answers if either the `WHERE` clause or the index has a nondeterministic collation.
* Fix incorrect handling of `NEW` generated columns in rule actions and rule qualifications (Richard Guo, Dean Rasheed) [§](https://postgr.es/c/7062bd577)

  Previously, such column references would produce NULL in `INSERT` cases, or be equivalent to the `OLD` value in `UPDATE` cases.
* Fix spurious “generated columns are not supported in COPY FROM WHERE conditions” errors (Tom Lane) [§](https://postgr.es/c/07e833e3c)

  Use of a system column in a `COPY FROM WHERE` condition could sometimes incorrectly report this error.
* Correctly report a serialization failure when `MERGE` encounters a concurrently-updated tuple in repeatable-read or serializable mode (Tender Wang) [§](https://postgr.es/c/8bfaae6fb)

  Previously, such cases behaved the same as in lower isolation levels.
* Fix `CREATE TABLE ... LIKE ... INCLUDING STATISTICS` for cases where the source table has dropped column(s) (Julien Tachoires) [§](https://postgr.es/c/76d15a7ee)

  In such cases, extended statistics objects could be copied incorrectly, or the command could give an incorrect error.
* Allow `ALTER INDEX ... ATTACH PARTITION` to mark the parent index valid if appropriate (Sami Imseih) [§](https://postgr.es/c/0859000d0)

  There are edge cases in which a partitioned index might remain marked as invalid even when all its leaf indexes are valid. This change provides a mechanism whereby a user can correct such a situation without resorting to manual catalog updates.
* Fix `ALTER FOREIGN DATA WRAPPER` to not drop the wrapper object's dependency on its handler function (Jeff Davis) [§](https://postgr.es/c/3a35ab1d0)
* Disallow making a composite type be a member of itself via a multirange (Heikki Linnakangas) [§](https://postgr.es/c/34ebeb15c)

  We already forbade such cases when the intermediate type is a domain, array, composite type, or range; but multiranges were overlooked.
* Fix datum-image comparisons to be insensitive to sign-extension variations (David Rowley) [§](https://postgr.es/c/6b2e091f0)

  This fixes some situations that previously led to “could not find memoization table entry” errors or wrong query results.
* Fix incorrect logic for hashed `IN`/`NOT IN` with non-strict equality operator (Chengpeng Yan) [§](https://postgr.es/c/622f8b530)

  The previous coding could crash or give wrong answers. All built-in data types have strict equality operators, so that this issue could only arise with an extension data type.
* Truncate overly-long locale-specific numeric symbols in `to_char()` (Tom Lane) [§](https://postgr.es/c/f60d25986)

  If a locale specified a currency symbol, thousands separator, or decimal or sign symbol more than 8 bytes long, a buffer overrun was possible. No such locales exist in the real world, and it's impractical for an unprivileged attacker to install a malicious locale definition underneath a Postgres server; but for safety's sake check for overlength symbols and truncate if needed.
* Prevent buffer overruns when parsing an affix file for an `Ispell` dictionary (Tom Lane) [§](https://postgr.es/c/0b196d3db) [§](https://postgr.es/c/f852c9093)

  A corrupt or malicious affix file could crash the server. This is not considered a security issue because text search configuration files are presumed trustworthy, but it still seems worth fixing.
* Guard against integer overflow in calculations of frame start and end positions for window aggregates (Richard Guo) [§](https://postgr.es/c/4da71fc37)

  Very large user-specified offsets (close to INT64_MAX) could result in errors or incorrect query results.
* Fix incorrect behavior of `pg_stat_reset_single_table_counters()` on a shared catalog (Chao Li) [§](https://postgr.es/c/c6d3f0585)

  Such cases had a side-effect of resetting the current database's `stat_reset_timestamp`, which was unintended.
* Fix buffer overread when `pglz_decompress()` receives corrupt input (Andrew Dunstan) [§](https://postgr.es/c/c88ad3a21)

  It was possible to read a few bytes past the end of the input, which in very unlucky cases might cause a crash.
* Ensure that tuplestore data structures are internally consistent even after an error (Tom Lane) [§](https://postgr.es/c/811f3263a)

  The code was previously careless about this, which is fine most of the time but is problematic for the tuplestore backing a `WITH HOLD` cursor. In v15 and before this leads to easily-reproducible crashes; later branches are not known to be vulnerable, but it seems best to preserve consistency in all.
* Fix premature NULL lag reporting in `pg_stat_replication` (Shinya Kato) [§](https://postgr.es/c/246c296f0)

  The lag columns frequently read as NULL even while replication activity was happening.
* Avoid rare flush failure when working with non-WAL-logged GiST indexes (Tomas Vondra) [§](https://postgr.es/c/ce06b5740)

  A non-logged GiST index could nonetheless sometimes produce “xlog flush request <em class="replaceable"><code>n/nnnn</code></em> is not satisfied” errors, due to incorrect selection of a “fake LSN” to represent an insertion point.
* Fix underestimate of required size of DSA page maps for odd-size segments (Paul Bunn) [§](https://postgr.es/c/46c93b705)

  This miscalculation led to out-of-bounds accesses and hence server crashes.
* Fix possible server crash when processing extended statistics on expressions of extension data types (Michael Paquier) [§](https://postgr.es/c/f033abc6c)

  NULL pointer dereferences were possible if the data type's typanalyze function does not compute any useful statistics. No in-core typanalyze function behaves that way, but extensions could.
* If the startup process fails, properly shut down other child processes before exiting the postmaster (Ayush Tiwari) [§](https://postgr.es/c/23cebf672)

  The handling of this situation relied on a long-obsolete assumption that no other postmaster children exist while the startup process is running, so that immediate postmaster exit is acceptable. Orphaned children would eventually notice the postmaster's death and exit on their own, but a cleaner shutdown procedure is desirable.
* Fix race condition between WAL replay of checkpoints and multixact ID creations (Heikki Linnakangas) [§](https://postgr.es/c/a5f412107)

  A standby server following WAL from a primary of an older minor version could get into a crash-and-restart loop complaining about “could not access status of transaction”.
* Prevent indefinite wait in shutdown of a walsender process (Anthonin Bonnefoy) [§](https://postgr.es/c/42734f296) [§](https://postgr.es/c/fa9f2e317)

  At shutdown of a cluster that is publishing logical replication data, the walsender waits for all pending WAL to be written out. But it did not correctly request that to happen, so that in some cases this could become an indefinite wait.
* Ensure that changes to tables' free space maps are persisted during recovery (Alexey Makhmutov) [§](https://postgr.es/c/ca259b084)

  Previously, while WAL replay did update the free space map while replaying operations that should change it, the map page buffer did not get marked dirty if checksums are enabled, so that the changes might never get written out. On a standby server, over time this would result in a map wildly at variance with the table's actual contents. While the map is only used as a hint, this condition could cause significant performance degradation for some period of time after the standby server is promoted to be active, until most of the map has been repaired by updates.
* Fix crashes in some ecpg functions when called without any established connection (Shruthi Gowda) [§](https://postgr.es/c/6916f4410)
* Fix assorted bugs in backup decompression and tar-parsing code (Andrew Dunstan, Tom Lane, Chao Li) [§](https://postgr.es/c/d3bb7841b) [§](https://postgr.es/c/9a42888a3) [§](https://postgr.es/c/4548e8746)

  The decompression and tar-file reading code used in pg_basebackup and pg_verifybackup mishandled tar-file padding data, could corrupt LZ4-compressed data in edge cases, failed to check for some unusual error conditions, failed to exit after compression/decompression errors (leading to cascading error reports), and leaked memory.
* In pg_upgrade, take care to use the correct protocol version when connecting to older source servers (Jacob Champion) [§](https://postgr.es/c/e726620d2)

  This could be problematic when attempting to upgrade from a pre-2018 server.
* In `contrib/basic_archive`, allow the archive directory to be missing at startup (Nathan Bossart) [§](https://postgr.es/c/8fc45ac5d)

  Previously, the setting of `basic_archive.archive_directory` was rejected if it didn't point to an existing directory. This is undesirable because archiving will be stuck indefinitely, even if the directory appears later.
* Fix `contrib/ltree` to cope when case-folding changes a string's byte length (Jeff Davis) [§](https://postgr.es/c/2b993167f)

  Previously, `lquery` patterns specifying case-insensitive matching might fail to match labels they should match.
* In `contrib/pg_stat_statements`, don't leak memory if an error occurs while parsing the `pgss_query_texts.stat` file (Heikki Linnakangas) [§](https://postgr.es/c/92cf11171)
* In `contrib/postgres_fdw`, avoid crash due to premature cleanup of a failed connection (Etsuro Fujita) [§](https://postgr.es/c/34c18a225)

  If a remote connection fails abort cleanup, we can't use it any longer. But delay closing the connection object until end of transaction, because there might still be references to it within data structures such as open cursors.
* Update time zone data files to tzdata release 2026b (Tom Lane) [§](https://postgr.es/c/e28fc73d5)

  British Columbia (America/Vancouver) will be on year-round UTC-07 (effectively, permanent DST) beginning in November 2026. This release assumes that their TZ abbreviation will be `MST` from that time forward. That seems likely to change, but it's unclear what new abbreviation will be used. Also a historical correction for Moldova: they have followed EU DST transition times since 2022.

---

原文：[PostgreSQL 15.19 Documentation](release-15-18.md)（英文原文，待翻譯）
