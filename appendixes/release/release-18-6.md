## E.1. Release 18.6 [#](#RELEASE-18-6)

[E.1.1. Migration to Version 18.6](release-18-6.md#RELEASE-18-6-MIGRATION)

[E.1.2. Changes](release-18-6.md#RELEASE-18-6-CHANGES)

**Release date:**2026-08-13

This release contains a variety of fixes from 18.4.
For information about new features in major release 18, see
[Section E.6](release-18.md).

Note: 18.5 was never released, due to a regression discovered
post-wrap.

<a id="RELEASE-18-6-MIGRATION"></a>

### E.1.1. Migration to Version 18.6 [#](#RELEASE-18-6-MIGRATION)

A dump/restore is not required for those running 18.X.

However, the first three security entries below describe configuration
adjustments and data cleanups that you may need to make after updating.

Also, if you have any GIN indexes, see the changelog entry below
about possibly-corrupt `reltuples` values for
their tables.

Also, if you use `contrib/btree_gist`
or `contrib/ltree`, you may need to reindex indexes
made with those extensions; see the relevant entries below.

Also, if you are upgrading from a version earlier than 18.2,
see [Section E.4](release-18-2.md).

<a id="RELEASE-18-6-CHANGES"></a>

### E.1.2. Changes [#](#RELEASE-18-6-CHANGES)

* Restrict logical decoding output plugins to the set specified by a
  new server parameter `output_plugin_libraries`
  (Jacob Champion)
  [§](https://postgr.es/c/2a29b607d)
  [§](https://postgr.es/c/82fd68801)

  Previously, a replication user could select any loadable library for
  logical decoding, allowing exploits of various sorts. To allow
  locking this down without breaking setups that worked before,
  introduce a whitelist of allowed output plugins.

  By default, only the output plugins shipped as part
  of PostgreSQL
  (`pgoutput` and `test_decoding`)
  are included in `output_plugin_libraries`.
  Installations that rely on other output plugins must add them
  after updating the server, for example

  ```

  output_plugin_libraries = 'pgoutput, test_decoding, my_trusted_decoder'
  ```

  Additionally, `pg_upgrade --check` will fail if the
  `output_plugin_libraries` parameter on the new
  cluster does not permit the plugins of logical replication slots
  on the old cluster, when migrating from versions 17 and later.
  Make necessary additions to the new cluster's setting before
  performing pg_upgrade.

  The PostgreSQL Project thanks
  Vladimir Tokarev and Yu Kunpeng
  for reporting this problem.
  (CVE-2026-6471)
* Fix `contrib/pgcrypto`'s PGP encryption to detect
  unsupported ciphers (Daniel Gustafsson)
  [§](https://postgr.es/c/fe32b10fc)
  [§](https://postgr.es/c/4c5128ca0)

  Previously, if OpenSSL rejected the requested cipher (for example,
  because it is running in FIPS mode, or the legacy provider hasn't
  been loaded), pgcrypto failed to notice
  the failure and simply XOR'd the non-encrypted block with the
  plaintext, rendering the “encryption” trivially
  breakable. This will typically occur with deprecated or non-FIPS
  cipher algorithms (cipher-algo=blowfish/bf, twofish, cast5, or
  3des).

  By default, pgcrypto will now fail to
  decrypt any messages that were affected in this way. To allow
  retrieval of such data, a new
  option `ignore-cipher-failure` has been added
  to `pgp_pub_decrypt()`
  and `pgp_sym_decrypt()`.
  Setting `ignore-cipher-failure=1` will restore
  their previous behavior, allowing the faulty encryption wrapper to
  be stripped off:

  ```

  pgp_sym_decrypt(encrypted_column, any key, 'ignore-cipher-failure=1')
  ```

  Once the affected messages are identified and stripped of their
  wrappers, they can then be re-encrypted with a modern algorithm. It
  is important however that the behavior of OpenSSL be the same as it
  was when the faulty messages were created: if the set of unsupported
  algorithms is not the same, this approach will not work. See the
  documentation for `ignore-cipher-failure`.

  The PostgreSQL Project thanks
  Shishir Sharma
  for reporting this problem.
  (CVE-2026-14663)
* Fix psql to skip in-line data following a
  scripted `COPY ... FROM STDIN` command, even if
  the `COPY` fails before
  sending `PGRES_COPY_IN` (Tom Lane)
  [§](https://postgr.es/c/29921259e)
  [§](https://postgr.es/c/900894d35)

  Previously, if a `COPY` command failed at startup
  (for instance, because the target table doesn't exist)
  psql would not realize that and would
  proceed to read the following in-line data as SQL commands. In the
  best case that's wrong and in the worst case it's a SQL-injection
  hazard. Teach psql to recognize
  syntactically-valid `COPY ... FROM STDIN` commands
  and to skip data on its own authority if the server doesn't respond
  with `PGRES_COPY_IN`.

  While this fix is unlikely to affect any production SQL scripts,
  test scripts might intentionally exercise failing `COPY
  ... FROM STDIN` commands. Those will need to gain
  a `\.` data terminator line after each such
  command.

  The PostgreSQL Project thanks
  Alexander Lakhin
  for reporting this problem.
  (CVE-2026-6464)
* Cross-check the output row type of a portal
  running `EXECUTE` or `FETCH`
  (Robert Haas)
  [§](https://postgr.es/c/37b8f3b0e)

  `EXECUTE` and `FETCH` use two
  portals: an outer one for the statement itself, and an inner one
  running the query being executed on its behalf. It was previously
  possible to make the declared row types of the two portals diverge,
  leading to server memory disclosure and arbitrary code execution.

  The PostgreSQL Project thanks
  Ben Morris (in collaboration with Claude and Anthropic Research)
  and Peter Geoghegan
  for reporting this problem.
  (CVE-2026-16239)
* Fix buffer overrun with long time zone abbreviation in
  `to_char()` (Tom Lane)
  [§](https://postgr.es/c/4fafe2380)

  This can easily crash the server, and exploits leading to arbitrary
  code execution have been reported.

  The PostgreSQL Project thanks
  Hcamael, Amjad Shahzad, Tan Zhen of AntAISecurityLab, Tomer Fichman,
  Zheng Yu, Amy Burnett (OpenAI Codex Security), Rick de Jager, Heewon
  Song, Sylvie Mayer, Aleksander Alekseev, and Hillai Ben Sasson
  for reporting this problem.
  (CVE-2026-14669)
* Fix buffer overrun in regexp match/split functions (Masahiko Sawada)
  [§](https://postgr.es/c/b7e5c3f63)

  If passed invalidly-encoded data, these functions could write past
  the end of their conversion buffer.

  The PostgreSQL Project thanks
  Francesco Verardi
  for reporting this problem.
  (CVE-2026-14664)
* Harden the `ascii()` function against invalid
  input (Michael Paquier)
  [§](https://postgr.es/c/08e812c02)

  By supplying invalidly-encoded input, this function could be coaxed
  to read and return a few bytes of data that it shouldn't. In
  assert-enabled builds, its assertions could be triggered too.

  The PostgreSQL Project thanks
  Hcamael
  for reporting this problem.
  (CVE-2026-18024)
* Fix multirange type handling
  in `pg_restore_attribute_stats()`
  (OpenAI Security Research Team)
  [§](https://postgr.es/c/08454e8b2)
  [§](https://postgr.es/c/8d428c6e6)

  `pg_restore_attribute_stats()` treated multirange
  types just like their underlying range type. This works correctly
  for the bounds histogram, but it was wrong for all the other
  statistics kinds.

  The PostgreSQL Project thanks
  Amy Burnett (OpenAI Codex Security)
  for reporting this problem.
  (CVE-2026-16238)
* Make `scalarineqsel()` check that a constant it
  expects to be of type `tid` actually is (Tom Lane)
  [§](https://postgr.es/c/a2cb5a1cf)

  This expectation will hold for all the built-in operators that use
  this estimator, but a maliciously-constructed operator could violate
  it, leading to a crash or server memory disclosure.

  The PostgreSQL Project thanks
  Hcamael
  for reporting this problem.
  (CVE-2026-14668)
* Harden `tsvector` and `tsquery` code against
  overly long values (both individual lexemes and total vector/query
  length) (Tom Lane)
  [§](https://postgr.es/c/e25135057)
  [§](https://postgr.es/c/dddc8a69f)

  The documented limits were not enforced in all code paths.

  The PostgreSQL Project thanks
  Yuhang Wu, Zhenpeng Lin, Zheng Yu, and Hcamael
  for reporting these problems.
  (CVE-2026-14662)
* Fix various places that mistakenly assumed they would not have to
  deal with more than `FUNC_MAX_ARGS` function
  arguments (Tom Lane)
  [§](https://postgr.es/c/7f0e1aac7)
  [§](https://postgr.es/c/2a03f21da)

  Notably, the server's actual limit on the number of arguments to an
  aggregate function is `FUNC_MAX_ARGS - 1`, but the
  parser failed to enforce that, creating hazards downstream.

  The PostgreSQL Project thanks
  Zheng Yu, ylwangtju, and Masahiko Sawada
  for reporting these problems.
  (CVE-2026-14679)
* Reject calls from SQL to functions that take or return
  type `internal` (Tom Lane)
  [§](https://postgr.es/c/54649de65)
  [§](https://postgr.es/c/722695db1)

  The existing defenses against doing this have been shown to be
  insufficient, so add more explicit checks.

  The PostgreSQL Project thanks
  Amy Burnett (OpenAI Codex Security)
  for reporting this problem.
  (CVE-2026-14680)
* Preserve the ownership of extended statistics objects when they are
  rebuilt by `ALTER TABLE` (Masahiko Sawada)
  [§](https://postgr.es/c/a1fa24127)

  Previously, the role running `ALTER TABLE` gained
  ownership of such objects, but that seems inappropriate.

  The PostgreSQL Project thanks
  Noah Misch
  for reporting this problem.
  (CVE-2026-6469)
* When deparsing an `EXTRACT()` function call,
  quote the field name if needed (Nathan Bossart)
  [§](https://postgr.es/c/0ddd9098a)

  The parser accepts any string literal as a field name
  in `EXTRACT()`, deferring validation to
  execution. If the call is stored and deparsed (for example
  during pg_dump), the string body was
  regurgitated verbatim, allowing SQL injection.

  The PostgreSQL Project thanks
  Ben Morris (in collaboration with Claude and Anthropic Research)
  for reporting this problem.
  (CVE-2026-15741)
* Check for `USAGE` privilege on data types in places
  that formerly failed to check that (Nathan Bossart)
  [§](https://postgr.es/c/2e91f8548)
  [§](https://postgr.es/c/57f59ca1d)
  [§](https://postgr.es/c/278053843)

  `CREATE TYPE AS RANGE` did not check, nor
  did `ALTER TABLE OF`, nor did commands that create
  stored expressions. These omissions allowed roles
  without `USAGE` privilege to nonetheless create
  objects depending on the type, possibly blocking the type's owner
  from changing the type later.

  The PostgreSQL Project thanks
  Jingzhou Fu
  for reporting this problem.
  (CVE-2026-6470)
* Invalidate role-dependent cached plans after role changes
  (Ilya Staroverov, Shinya Kato, Nathan Bossart)
  [§](https://postgr.es/c/0b12f56bf)

  Role membership, role attribute, and database ownership changes may
  impact the expected behavior of row-level security policies, but
  previously we'd continue to use cached plans that were made
  according to the old state of affairs.

  The PostgreSQL Project thanks
  Ilya Staroverov and Shinya Kato
  for reporting this problem.
  (CVE-2026-14666)
* Reject GSSEncRequest after direct SSL connection (Michael Paquier)
  [§](https://postgr.es/c/203a48209)

  After establishing a TLS-encrypted connection, the server would
  still accept a request for GSSAPI encryption. If that succeeded,
  the connection would proceed using TLS encryption, but it would look
  like a GSS connection to the `pg_hba` rules.
  Thus, a `pg_hba` policy intending to disallow TLS
  would not be enforced correctly.

  The PostgreSQL Project thanks
  p4p3r
  for reporting this problem.
  (CVE-2026-14681)
* Make mock SCRAM authentication secrets more plausible (Nathan Bossart)
  [§](https://postgr.es/c/822143c4d)

  If a SCRAM login is attempted against a role that doesn't exist or
  doesn't have a SCRAM secret, we generate a mock secret and carry out
  the authentication handshake anyway, to avoid revealing these facts
  to an attacker. But the mock secret was made with a fixed iteration
  count, which in itself can be an observable response discrepancy.
  Use the configuration setting `scram_iterations`
  instead, to make the mock secret look more like the installation's
  real secrets.

  The PostgreSQL Project thanks
  Radim Marek
  for reporting this problem.
  (CVE-2026-14672)
* Fix out-of-bounds writes in ecpg
  applications caused by invalid `bytea` data received from
  the server (Michael Paquier)
  [§](https://postgr.es/c/a14ba29b1)

  ecpg assumed without checking that
  any `bytea` value must begin with `\x`.
  A broken or malicious server might send a string shorter than 2
  bytes, resulting in memory clobber in the application.

  The PostgreSQL Project thanks
  ylwangtju
  for reporting this problem.
  (CVE-2026-16241)
* Do not do backquote expansion on the argument
  of psql's `\unrestrict`
  command (Nathan Bossart)
  [§](https://postgr.es/c/71ca694c7)

  This oversight in the fix for CVE-2025-8714 allows a malicious
  server to inject shell commands into plain-text dump output that
  will be run at restore time on the machine
  running psql, the exact scenario that
  CVE-2025-8714 intended to prevent.

  The PostgreSQL Project thanks
  Lucas Velgus, Filip Janus, and Daniel Bakker
  for reporting this problem.
  (CVE-2026-18408)
* Remove pg_dump's assumption that
  `pg_proc`.`protrftypes`
  cannot have more than `FUNC_MAX_ARGS` entries
  (Tom Lane)
  [§](https://postgr.es/c/3392cce5c)

  Since there could be entries for both input and output arguments,
  it's feasible for this array's length to exceed
  `FUNC_MAX_ARGS` (which constrains only input
  arguments). Even if that were not so,
  pg_dump cannot assume that the server was
  built with the same value of `FUNC_MAX_ARGS` that
  it has. An overrun would lead to a memory clobber
  inside pg_dump.

  The PostgreSQL Project thanks
  Masahiko Sawada
  for reporting this problem.
  (CVE-2026-19385)
* Harden PL/Perl
  against “tied” Perl arrays and hashes (Tom Lane)
  [§](https://postgr.es/c/87c4b8219)

  A tied object that doesn't behave like a regular one could lead to
  memory overwrite, or to constructing a corrupt result array (which
  would likely cause problems later).

  The PostgreSQL Project thanks
  Hcamael
  for reporting this problem.
  (CVE-2026-14670)
* Fix integer overflows in memory-allocation calculations
  in PL/Perl
  and PL/Tcl (Heikki Linnakangas)
  [§](https://postgr.es/c/028ee716a)

  This is the same type of problem as CVE-2026-6473, just in a
  different part of the code, and is fixed in the same way.

  The PostgreSQL Project thanks
  the Tulya Project (Team Dhiutsa, Bitecope Technologies Private Ltd)
  for reporting this problem.
  (CVE-2026-14677)
* Ensure that `contrib/amcheck` functions
  restrict `search_path` before executing index
  expressions (Noah Misch)
  [§](https://postgr.es/c/0a61fcde0)

  Because amcheck will run such index expressions as the owner of
  their tables, a caller could potentially
  hijack `search_path`-dependent functions to run
  arbitrary code as the table owner. By default this is not a
  vulnerability because only superusers are allowed to call amcheck
  functions; but if that privilege was granted out, it created a
  larger hazard than the documentation suggests.

  The PostgreSQL Project thanks
  Yuelin Wang and Jacob Brazeal
  for reporting this problem.
  (CVE-2026-14673)
* Fix integer overflows in `contrib/fuzzystrmatch`'s
  `levenshtein()`
  and `levenshtein_less_equal()` functions
  (Nathan Bossart)
  [§](https://postgr.es/c/e88eb4e76)

  Passing large cost values to these functions could cause integer
  overflows, thereby producing nonsensical results, and even causing
  out-of-bounds writes in some cases.

  The PostgreSQL Project thanks
  Ben Morris (in collaboration with Claude and Anthropic Research)
  for reporting this problem.
  (CVE-2026-15742)
* Fix buffer overrun
  in `contrib/pg_stat_statements` (Álvaro Herrera)
  [§](https://postgr.es/c/8a31ffc2d)

  Query normalization didn't accurately account for the amount of
  space the normalized string would require.

  The PostgreSQL Project thanks
  Sajeeb Lohani (with TrendAI Zero Day Initiative) and Yuelin Wang
  for reporting this problem.
  (CVE-2026-14676)
* Fix datatype error in `contrib/pg_trgm`'s GiST
  picksplit function (Heikki Linnakangas)
  [§](https://postgr.es/c/849019a50)

  This mistake resulted in reading past the end of the buffer,
  typically causing bad split decisions; but a crash could ensue
  if you're very unlucky.

  The PostgreSQL Project thanks
  Mehmet D. Ince
  for reporting this problem.
  (CVE-2026-14678)
* Remove the plan cache in `contrib/refint`
  (Ayush Tiwari)
  [§](https://postgr.es/c/79a506228)

  This caching behavior has several serious bugs, notably that
  `check_foreign_key()` embeds the new key values
  in its cascade-UPDATE queries, so a cached plan reuses the
  originally-needed values rather than the key values that should be
  used. The simplest solution is to remove it.

  The PostgreSQL Project thanks
  Hcamael
  for reporting this problem.
  (CVE-2026-14671)
* Ensure that parallel GIN index builds update the table's
  `pg_class`.`reltuples`
  value correctly (Jan Nidzwetzki, Tomas Vondra)
  [§](https://postgr.es/c/d4420a972)

  A parallel worker could report an uninitialized value for the
  number of rows it processed, leading to a bogus value
  for `reltuples`, even Infinity or NaN.
  Such values could lead to subsequent autovacuum and autoanalyze
  operations never deciding that the table needs to be processed.
  If so, the situation will not self-heal. A manual
  `ANALYZE` command, or creation of another index,
  will be needed to reset `reltuples` to
  the correct value. If you have any tables with GIN indexes, it's
  recommended to check to see if
  their `reltuples` entries look sane.
  A query such as this may be helpful:

  ```

  SELECT DISTINCT t.oid::regclass, t.reltuples
  FROM pg_class t
    JOIN pg_index i ON t.oid = i.indrelid
    JOIN pg_class ic ON i.indexrelid = ic.oid
  WHERE t.relhasindex AND ic.relam = 2742;
  ```
* Fix mis-handling of asynchronous reads when rescanning an
  asynchronous Append plan node (Alexander Korotkov, Gleb Kashkin,
  Etsuro Fujita)
  [§](https://postgr.es/c/4ea497a92)

  When an upper plan node rescans an Append before having read the
  entire Append output, we need to discard any in-flight requests sent
  to external servers (by `postgres_fdw` for
  example). This was not done correctly in cases where a subplan has
  parameter changes or is discarded by partition pruning in the next
  scan. The outcome could be incorrect query results, an infinite
  loop, or an assertion failure.
* Fix error in partition pruning for RANGE-partitioned tables
  (David Rowley)
  [§](https://postgr.es/c/02e69be47)

  In some cases the DEFAULT partition would be skipped when it should
  not be, which could lead to rows missing from query results.
* Correctly update foreign-data-wrapper state in a ModifyTable plan
  node after pruning result relations (Ayush Tiwari, Rafia Sabih)
  [§](https://postgr.es/c/1ef917e3a)
  [§](https://postgr.es/c/bba4e095d)

  Previously, if run-time partition pruning determined that some
  partitions of a partitioned target table need not be scanned
  and the table had any foreign-table partitions, a crash
  or erroneous behavior was likely.
* Fix missed concurrent update in `UPDATE`
  with `RETURNING OLD` on a table that has
  a `BEFORE UPDATE` trigger (Dean Rasheed)
  [§](https://postgr.es/c/4908225be)

  If the target row was concurrently updated, then at isolation
  level `READ COMMITTED` any `OLD`
  values in `RETURNING` should reflect the updated
  row. But stale values were returned if there was a trigger
  (although the trigger itself, and the final output row, saw the
  correct values).
* Fix hash join performance issue when there are multiple join keys
  and many NULL values (David Rowley)
  [§](https://postgr.es/c/f70acc8a2)

  Null-keyed tuples should not get inserted into the hash table, since
  they will never match any other tuples. The code got this wrong if
  the null was in a non-last join column, bloating the hash table
  quite a lot if many inputs contain nulls.
* Fix parsing of
  parenthesized `OLD`/`NEW`
  in `RETURNING` expressions (Marko Grujic)
  [§](https://postgr.es/c/9108fed3e)

  Expressions such as `(old).colname`
  and `(old).*` were mis-handled, effectively
  converting them to `NEW` references.
* Fix planner's nullability and strictness checks
  for `value IN
  (array)` expressions
  (Ayush Tiwari)
  [§](https://postgr.es/c/277122036)

  These checks should only succeed if the array operand is known to be
  non-empty, but that consideration was missed, allowing optimizations
  to be applied that should not be. This could result in wrong query
  answers if the array actually was empty.
* Fix incorrect join removal logic (Matheus Alcantara, Richard Guo)
  [§](https://postgr.es/c/21f5e659e)
  [§](https://postgr.es/c/9e40d07e1)

  In edge cases, it was possible for a constant output value coming
  from within the nullable side of an outer join to not be replaced by
  NULL when it should be.
* Clean up PlaceHolderVars more thoroughly during join removal
  (Richard Guo, Arne Roland)
  [§](https://postgr.es/c/e02526795)
  [§](https://postgr.es/c/18105e6db)

  This fix corrects various edge cases that could trip assertions or
  result in incorrect plans.
* Add missed checks for hashability of equality comparisons on
  container datatypes (arrays, composites, ranges) (Andrei Lepikhov,
  Tom Lane)
  [§](https://postgr.es/c/11aed8d19)

  The planner must verify hashability of the container's component
  type(s) before deciding it can use a hash-based plan type. This
  step was missed in some places, leading to “could not identify
  a hash function” failures at execution.
* Avoid pushing `WHERE` clauses down past a grouping
  step that has a different equivalence rule (Richard Guo)
  [§](https://postgr.es/c/fe5d62951)

  A test on a grouping column that is grouped by a nondeterministic
  collation is safe to push down only if it is a comparison using that
  same collation. Otherwise it might filter some rows the grouping
  would have merged.
* Fix mis-optimization of `COUNT` window functions
  that have an `EXCLUDE` clause or
  lack `ORDER BY` (Chengpeng Yan, David Rowley)
  [§](https://postgr.es/c/cf184ec77)

  These window functions were treated as monotonic when they should
  not be, allowing wrong answers to be computed.
* Avoid “cache lookup failed for collation 0” error when
  planner looks up statistics for a column of type `"char"`
  (Feng Wu)
  [§](https://postgr.es/c/5fd1c3f28)
* Fix `ALTER COLUMN ... DROP EXPRESSION` to work when
  there are multiple levels of partitions (Alberto Piai)
  [§](https://postgr.es/c/c374f2807)
* Fix attaching partitions of indexes that are exclusion constraints
  (Japin Li)
  [§](https://postgr.es/c/19e3aa704)

  Notably, this oversight broke dump/restore of partitioned exclusion
  constraints.
* Prevent setting `NO INHERIT` on
  partitioned `NOT NULL` constraints
  via `ALTER CONSTRAINT` (Andreas Karlsson)
  [§](https://postgr.es/c/41247cdf6)

  `NOT NULL` constraints on partitioned tables are
  supposed to be inherited by all partitions, and therefore must not
  be marked `NO INHERIT`. This rule was correctly
  enforced by constraint creation, but not by `ALTER TABLE
  ... ALTER CONSTRAINT`.
* Disallow renaming a rule to `_RETURN` (Tom Lane)
  [§](https://postgr.es/c/a7f7958ab)

  That name is reserved for a view's `ON SELECT`
  rule, but `ALTER RULE` allowed renaming other rules
  to `_RETURN`, causing trouble later.
* Fix missing lock release for role membership grants in `DROP
  OWNED BY` (Jeff Davis)
  [§](https://postgr.es/c/a0daa0b41)

  This oversight resulted in a warning message, followed by retaining
  a lock on the membership grant until the end of the transaction.
* Fix failure of `EXPLAIN` when
  deparsing `SQL/JSON` aggregates (Richard Guo)
  [§](https://postgr.es/c/45364e496)

  Some plan structures resulted in “invalid
  JsonConstructorExpr underlying node type” errors.
* Fix use of `REINDEX CONCURRENTLY` with
  a deferred uniqueness constraint (Nitin Motiani)
  [§](https://postgr.es/c/e4527519b)

  The transient index copy created during `REINDEX
  CONCURRENTLY` was incorrectly marked as enforcing immediate
  uniqueness, causing spurious reports of constraint violation.
* Fix `LIKE` matching with nondeterministic
  collations and backslashes (Nitin Motiani, Tom Lane)
  [§](https://postgr.es/c/a99bd8d58)
  [§](https://postgr.es/c/51652c42d)

  When using a nondeterministic collation, `LIKE`
  mishandled an escaped backslash (`\\`), treating it
  as effectively not there. It also did the wrong thing with a
  leading backslash preceding an ordinary character; in that case the
  backslash should be effectively ignored, but it caused the ordinary
  character to be matched exactly rather than allowing the
  nondeterministic collation to decide if there's a match.
* Fix `LIKE`/regex optimization for indexscan with
  exact-match pattern (Jelte Fennema-Nio)
  [§](https://postgr.es/c/d0bb49e61)

  Refactoring for `LIKE` with non-deterministic
  collations accidentally broke the optimization for converting
  a `LIKE` or regex exact-match pattern to an
  equality index condition when the index collation doesn't match
  the expression collation. Among other things, that
  made psql's
  `\d tablename`
  command much slower.
* Fix matching of localized month/day names
  in `to_date()` (Heikki Linnakangas)
  [§](https://postgr.es/c/011384ba4)
  [§](https://postgr.es/c/5f003855e)

  The matching logic misbehaved in cases where case-folding changes
  the byte length of the string.
* Correct case-folding rules for Greek final sigma (Jeff Davis)
  [§](https://postgr.es/c/66ec24276)

  If the string is preceded only by Case Ignorable characters, don't
  consider it to be a final sigma. This only affects the
  built-in `pg_unicode_fast` locale.
* Fix incorrect NFC recomposition for Hangul U+11A7 (TBASE)
  (Diego Frias, Michael Paquier)
  [§](https://postgr.es/c/273fe9485)

  This character was treated as a valid T syllable, which it is not,
  and hence silently swallowed during normalization.
* Avoid possible truncation of output lexemes in case-insensitive
  `synonym` dictionaries (Jeff Davis)
  [§](https://postgr.es/c/89e648498)

  If folding to lower case increased the byte length of a lexeme, it
  was incorrectly truncated to its original byte length when emitted.
* Defend against truncated UTF-8 characters in case-conversion logic
  (Jeff Davis)
  [§](https://postgr.es/c/9021c8f3c)
* Fix typo in `hash_record_extended()` (Man Zeng)
  [§](https://postgr.es/c/b3f13c032)

  The code failed to initialize the second isnull argument passed to
  FunctionCallInvoke(). This is harmless for existing in-core
  extended hash support functions, which will not examine that value.
  However, extension-provided hash functions could be affected if they
  inspect `PG_ARGISNULL(1)`.
* Fix `pg_get_publication_tables()` to not fail if
  a publishable table is dropped concurrently (Bharath Rupireddy)
  [§](https://postgr.es/c/73d63d1c1)
* Prevent `satisfies_hash_partition()` from
  crashing with `VARIADIC NULL` (Robert Haas)
  [§](https://postgr.es/c/0c06ebf12)
* Report invalid-weight errors more cleanly and consistently
  in `tsvector_filter()` and allied functions
  (Ewan Young)
  [§](https://postgr.es/c/c5194139c)

  In particular, report weight characters that are not printable ASCII
  in octal form (`\nnn`),
  as `charout()` would render them. This avoids
  possibly producing an invalidly-encoded error message.
* Reject out-of-range timestamp shift values
  in `uuidv7()` (Baji Shaik)
  [§](https://postgr.es/c/c31b0fca0)

  The shift value must not be so large as to produce a timestamp out
  of the range that a v7 UUID can represent. Previously, a garbage
  UUID value was produced.
* Fix mishandling of namespace nodes in `xpath()`
  (Michael Paquier)
  [§](https://postgr.es/c/4c777d6dd)
  [§](https://postgr.es/c/0d145be2c)

  This fix avoids an unexpected “could not copy node”
  error.
* Fix `jsonpath`'s `.decimal` method to
  not throw a hard error for incorrect precision or scale (Ewan Young)
  [§](https://postgr.es/c/84001a04d)
  [§](https://postgr.es/c/90789900b)

  Silent mode should suppress these errors, but failed to.
* Fix NULL-pointer crash when `IS JSON` or similar
  constructs have an argument that is of string category but lacks a
  cast to type `text` (Ayush Tiwari)
  [§](https://postgr.es/c/35d9a6263)

  There are no such data types in
  core PostgreSQL, but the problem is
  reachable with some extension types.
* Ensure that `SQL/JSON` `ON EMPTY / ON ERROR
  DEFAULT` values are coerced to the correct typmod (Ewan Young)
  [§](https://postgr.es/c/441e4c8d6)

  For example, the declared precision and scale of
  a `numeric` target column were not applied to the default
  value.
* Avoid machine-dependent behavior when dividing the smallest
  possible `money` value by -1 (Andrey Rachitskiy)
  [§](https://postgr.es/c/6298a41b4)
* Fix crash after out-of-memory failure partway through creation of a
  cache entry for a text search dictionary (Tom Lane)
  [§](https://postgr.es/c/81b1e7916)
* Fix memory-safety bugs in processing of incorrect ispell/hunspell
  dictionary files (Andrey Rachitskiy)
  [§](https://postgr.es/c/4689ea9ce)
* Prevent access to other sessions' temporary tables (Jim Jones,
  Daniil Davydov, Alexander Korotkov)
  [§](https://postgr.es/c/1b0dd0815)
  [§](https://postgr.es/c/3aaefe892)

  Some code paths failed to prevent this, leading to silently wrong
  (inconsistent) results.
* Prevent “no empty local buffer available” errors during
  temporary table access (Melanie Plageman)
  [§](https://postgr.es/c/ed8050370)

  Limit the number of local buffers that the read streaming mechanism
  is allowed to use. Previously, a large value
  of `effective_io_concurrency` could allow a single
  stream to use all the buffers, resulting in failure.
* Fix the order in which autovacuum processes databases
  (Rustam Khamidullin)
  [§](https://postgr.es/c/4cc49cb70)

  It was unintentionally processing databases from lowest to highest
  score, when it should be doing the reverse.
* Restore full use of shared buffer pool
  in `VACUUM`'s wraparound failsafe mode
  (Melanie Plageman)
  [§](https://postgr.es/c/585181e07)
  [§](https://postgr.es/c/7c25cdb1e)

  An ordinary `VACUUM` is limited to use just a few
  shared buffers, so as not to impinge too much on other processing.
  However, in failsafe mode we want to reclaim transaction IDs as
  quickly as possible, so that limit is supposed to be abandoned
  to allow vacuuming to proceed as fast as possible. This behavior
  was accidentally broken during refactoring in v18; restore it.
* Fix memory leak in parallel vacuum worker processes (Baji Shaik)
  [§](https://postgr.es/c/4154a1482)

  Progress reports from a parallel worker leaked about 1kB per report,
  with the waste accumulating for the life of the worker process.
* Honor query cancel and vacuum delay during GIN index posting-tree
  cleanup (Paul Kim, Alexander Korotkov)
  [§](https://postgr.es/c/7becb647d)

  The posting tree for a common value can be large, so that this
  missed check could allow vacuum to run for a long time before
  noticing an interrupt.
* Fix possible mis-decoding of index tuples during GiST and SP-GiST
  index-only scans (Peter Geoghegan)
  [§](https://postgr.es/c/959b7fa2c)

  This error could lead to emitting corrupted data from an index-only
  scan plan. The only affected core opclass is GiST's range_ops, and
  it could only fail if the range column were not the first index
  column.
* Ensure that the new last block of a bulk-extended table is added to
  its free space map promptly (Jingtang Zhang)
  [§](https://postgr.es/c/eabc9a9dd)

  An off-by-one error caused the last block of a multi-block table
  extension to not be marked as free in the map. This would
  eventually get corrected by vacuum, but meanwhile the space wouldn't
  be used.
* Avoid possible double-free or infinite error recovery loop in
  resource cleanup during transaction abort (Tom Lane)
  [§](https://postgr.es/c/ac6a58a70)
* When creating directories, tolerate concurrent creation of the same
  directory (Andrew Dunstan, Tom Lane)
  [§](https://postgr.es/c/aa80c34c8)
* Fix JIT-compiled tuple deconstruction code to account correctly for
  virtual generated columns (David Rowley)
  [§](https://postgr.es/c/e9692de1d)
* Prevent creation of dangling object dependencies by acquiring a
  shared lock on any object being depended on (Bertrand Drouvot)
  [§](https://postgr.es/c/c8cd3d697)
  [§](https://postgr.es/c/f9d5a52da)

  The shared lock will conflict with any attempt to drop the
  depended-on object, eliminating the race condition that formerly
  existed. For example, if one session drops a schema (that appears
  empty to it) concurrently with some other session creating a
  function in that schema, previously both transactions could commit,
  leaving an invalid function definition behind. Now, one transaction
  or the other will fail.
* Fix race condition in conflict detection
  for `SERIALIZABLE` isolation mode
  (Peter Geoghegan)
  [§](https://postgr.es/c/d560e730e)

  A conflict could be missed when examining an initially-empty btree
  index, allowing failure of serializability due to improperly
  allowing conflicting transactions to commit.
* Fix race condition in ProcSignalBarrier code (Masahiko Sawada)
  [§](https://postgr.es/c/1a9b1cc18)

  This error could result in processes getting stuck, typically after
  reporting “still waiting for backend with
  PID *`nnnn`* to accept
  ProcSignalBarrier”.
* Fix race conditions when a set of processes that belong to the same
  lock group exit at the same time (Vlad Lesin)
  [§](https://postgr.es/c/ae08eb168)
  [§](https://postgr.es/c/12c9b8b42)

  These errors could lead to PANIC aborts, with messages such
  as “latch already owned”. The issue does not normally
  arise in regular parallel query, since the leader won't exit before
  seeing its workers finish; but some extensions reach the problem.
* Fix WAL logging of operations that clear bits in tables' visibility
  maps (Melanie Plageman, Andres Freund)
  [§](https://postgr.es/c/d0fb1da21)
  [§](https://postgr.es/c/f581fa729)
  [§](https://postgr.es/c/4d7feebfb)

  Such VM changes were missed by the WAL summarizer, potentially
  leading to incorrect incremental backups. We also failed to log
  full-page images of such VM pages when needed, potentially allowing
  torn page writes to go uncorrected. This could lead to misbehavior
  later, such as wrong results from index-only scans.
* Prevent WAL summarizer process from getting stuck at a timeline
  switch (Robert Haas)
  [§](https://postgr.es/c/18f0de6b8)
  [§](https://postgr.es/c/1d299d6ab)
* Fix race with timeline selection in logical decoding during standby
  promotion (Bertrand Drouvot)
  [§](https://postgr.es/c/b4bd13850)
  [§](https://postgr.es/c/4bff3aa51)

  Logical decoding being performed on the standby could fail with
  a “requested WAL segment has already been removed”
  error. A repeat attempt would succeed, so there was no permanent
  problem but there was an availability hazard.
* Avoid exposing a WAL receiver's full connection string during timeline
  jumps (Chao Li)
  [§](https://postgr.es/c/b903d1792)

  The `pg_stat_wal_receiver` view should show a
  sanitized version of the connection string, without sensitive data.
  But it transiently showed the full string when we re-use an existing
  WAL receiver.
* Use run-time checks, not just Asserts, to verify the correct number
  of columns in tuples received during logical replication (Varik
  Matevosyan)
  [§](https://postgr.es/c/dc3db3a83)

  A malicious or buggy publisher could send inconsistent numbers of
  columns. While we could not find a scenario in which this would
  have serious ill effects, extra caution seems warranted.
* Clean up quoting of string parameters within constructed replication
  commands (Tom Lane)
  [§](https://postgr.es/c/abb582555)

  Various places that generate replication commands were not being
  adequately careful about quoting replication slot names and other
  parameters that need to be inserted into those commands. This could
  result in unexpected syntax errors in those commands. In principle,
  a crafted replication slot name could result in SQL injection; but
  such a scenario seems very unlikely to occur in practice, since
  replication operations can only be invoked by highly-privileged
  users and there is no reason for them to use a slot name coming from
  an untrustworthy source.
* Fix logical decoding of empty prepared transactions (Masahiko Sawada)
  [§](https://postgr.es/c/b563fc6bd)

  A prepared transaction that did not cause any decodable updates could
  result in sending `COMMIT/ROLLBACK PREPARED` to the
  output plugin with no preceding `PREPARE`. For the
  built-in subscriber this breaks replication, and other plugins will
  probably not like it either.
* Fix corruption of unlogged sequences after standby promotion
  (Fujii Masao)
  [§](https://postgr.es/c/627605713)

  Previously, if an unlogged sequence was created on the primary and
  replicated to a standby, accessing the sequence after promoting the
  standby could fail with “bad magic number in sequence”
  or related errors.
* Fix cascading standby reconnect failure after archive fallback
  (Marco Nenciarini)
  [§](https://postgr.es/c/331016322)

  A cascading standby could fail to reconnect to its upstream standby
  with “requested starting point ... is ahead of the WAL flush
  position” after falling back to archive recovery.
* Prevent accepting hot-standby connections before WAL replay has
  reached a consistent database state (Nikhil Sontakke)
  [§](https://postgr.es/c/311e66df9)
* Do not try to clear
  `pg_database`.`dathasloginevt`
  locally on a standby server (Ayush Tiwari)
  [§](https://postgr.es/c/97b5c5aaa)

  Event trigger cleanup tried to perform that action on standby
  servers as well as the primary. That can't work on a standby,
  and there's no need anyway since replay of the primary's database
  change will soon fix it.
* Avoid race condition while dropping obsolete replication slots
  (Xuneng Zhou)
  [§](https://postgr.es/c/08458bcae)

  An incorrect unlock and log message could occur if another session
  immediately re-used the dropped slot's shared-memory entry.
* Avoid race condition while dropping ephemeral replication slots
  (Zhijie Hou)
  [§](https://postgr.es/c/f833c9207)

  The slot-releasing code performed some additional updates to the
  replication slot's shared-memory entry after releasing the slot.
  This is unsafe since another session could immediately re-use the
  dropped slot's shared-memory entry. Skip those updates in the case
  of an ephemeral slot.
* Fix stale progress reports during logical replication table
  synchronization (Shinya Kato)
  [§](https://postgr.es/c/d9cd9b4d7)

  Previously, the `pg_stat_progress_copy` view
  in the subscriber would continue to show the
  initial `COPY` operation as active even after the
  data copy had finished. The stale entry remained visible until
  synchronization caught up with the publisher.
* Clear base backup progress on backup failure (Chao Li)
  [§](https://postgr.es/c/e7564ee8c)
  [§](https://postgr.es/c/e2ad214dd)

  Previously the `pg_stat_progress_basebackup`
  view would continue to show a stale progress entry after a failure,
  until the replication client
  disconnected. pg_basebackup normally
  disconnects immediately, but other clients might not.
* Fix possible PANIC due to concurrent drop of pgstats entries
  when `track_functions` is enabled (Sami Imseih,
  Michael Paquier)
  [§](https://postgr.es/c/5cc59834b)
  [§](https://postgr.es/c/8a4f389dd)
  [§](https://postgr.es/c/fe464e9e6)
* Clean up broken local pgstats entry after failing to obtain space for
  the corresponding shared hashtable entry (Niall Newman)
  [§](https://postgr.es/c/2fd8d45ec)

  Failure to do this led to a null-pointer dereference the next time
  the local entry was used.
* Avoid recording incorrect I/O operation statistics after a failed
  read or write (Bertrand Drouvot)
  [§](https://postgr.es/c/13f940b4b)
* In PL/Perl, avoid NULL pointer
  dereference crash when working with an
  invalid `PostgreSQL::InServer::ARRAY` object (Xing Guo)
  [§](https://postgr.es/c/e430ecc59)
* In PL/Python, properly check for errors
  when working with sequence and mapping objects (Richard Guo)
  [§](https://postgr.es/c/53482fcb9)

  Previously, a broken object or an unhandled exception could result
  in a NULL pointer dereference crash.
* In libpq, always drain all pending bytes
  from the SSL or GSS decryption buffer
  during `pqReadData()` (Jacob Champion)
  [§](https://postgr.es/c/2167302b7)
  [§](https://postgr.es/c/bb0a54518)
  [§](https://postgr.es/c/27761c015)
  [§](https://postgr.es/c/87c3a79ea)

  This avoids edge cases where libpq or its
  calling application waits for more data to arrive on the socket, but
  actually all the data has already arrived.
* Improve libpq's handling of out-of-memory
  conditions (Anthonin Bonnefoy)
  [§](https://postgr.es/c/6b46a5d1b)
* Fix libpq's trace facility to print
  new-style BackendKeyData and CancelRequest messages correctly
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/dd5eca055)
* Allow libpq to accept
  ParameterDescription messages exceeding 30000 bytes (Ning Sun)
  [§](https://postgr.es/c/b1ab4bc52)

  Previously, this message type was not among those
  that libpq's validity heuristics believed
  could be long. The limit resulted in failure for prepared queries
  having more than 7498 parameters, which is unlikely but supported.
* Fix null-pointer crash in ecpg compiler
  (Jehan-Guillaume de Rorthais)
  [§](https://postgr.es/c/917fdbc63)

  ecpg failed on
  a `DECLARE` section containing a union nested
  inside a struct.
* Reject multiple descriptor header items
  in ecpg's `GET/SET
  DESCRIPTOR` statements (Masashi Kamura)
  [§](https://postgr.es/c/081434b0f)

  Previously the grammar allowed this syntax, but broken C code was
  generated. Adjust the grammar and the documentation to allow only
  one header item.
* Fix issues with deferred errors in pipeline mode
  in psql (Michael Paquier)
  [§](https://postgr.es/c/1e9bc4074)

  psql could get stuck or suffer an
  assertion failure in some scenarios where the server reports an
  error in response to a Sync message, such as a deferred constraint
  violation.
* Make line widths match in psql's expanded
  aligned output format (Pavel Stehule)
  [§](https://postgr.es/c/07a6c262b)

  When the table's data rows are narrower than the record header lines,
  widen the data rows to match the headers, avoiding unsightly output.
* Enforce the intended upper limit
  for psql's special
  variable `WATCH_INTERVAL`
  (Sven Klemm, Daniel Gustafsson)
  [§](https://postgr.es/c/e0c641ebb)

  If a too-large value was given, psql
  reported an error but applied the setting anyway.
* Fix psql's privilege check for showing
  database size in `\l+` (Christoph Berg)
  [§](https://postgr.es/c/f2d6cf880)

  The underlying server function permits users who
  have `pg_read_all_stats` privileges to see the
  sizes of all databases, even if they lack `CONNECT`
  privilege. But psql was unaware of that
  provision and would not call the function unless the user
  has `CONNECT` privilege.
* Fix psql's tab completion
  for `\df` to consider procedures too
  (Erik Wienhold)
  [§](https://postgr.es/c/598af79b1)
* Fix thread-safety bug in pgbench
  (Fujii Masao)
  [§](https://postgr.es/c/98dd6c204)

  When pgbench runs with multiple threads
  and the `--verbose-errors` option, different threads
  could attempt to use the same buffer to construct error messages,
  leading to corrupted log output.
* In pg_combinebackup, prevent infinite
  loop if the source file is shorter than expected (Peter Eisentraut)
  [§](https://postgr.es/c/d36b72894)
* Fix cleanup of publisher-side objects after errors
  in pg_createsubscriber (Nisha Moond)
  [§](https://postgr.es/c/196b4b5ae)

  When pg_createsubscriber fails after
  creating logical replication objects, it should remove the
  publication and replication slot that it created on the publisher.
  Some error cases failed to do so.
* Use the source cluster's group-read file permissions
  for pg_recvlogical output files
  (Fujii Masao)
  [§](https://postgr.es/c/89b4b3ae3)

  pg_recvlogical was documented to behave
  this way, but it never actually enabled group-read.
* Fix inconsistent behavior of pg_restore
  with `--statistics`
  or `--statistics-only`
  (Chao Li, Michael Paquier)
  [§](https://postgr.es/c/42ffdedcf)
  [§](https://postgr.es/c/477efef08)

  When combined with other selective-restore options such
  as `--schema`, these options failed to restore the
  expected items, unlike pg_dump with
  similar options.
* Fix `vacuumdb --missing-stats-only` to ignore
  partitioned expression indexes (Baji Shaik)
  [§](https://postgr.es/c/7e085aabd)

  Previously, vacuumdb would always attempt
  to `ANALYZE` the partitioned table, accomplishing
  nothing since statistics are never created for partitioned indexes,
  only for their leaf indexes.
* In `contrib/amcheck`, fix failure to report
  corruption of a btree metapage's `allequalimage`
  flag (Chao Li)
  [§](https://postgr.es/c/12c32bbc8)
* In `contrib/amcheck`, fix query-lifespan memory
  leak while verifying a GIN index (Kirill Reshke)
  [§](https://postgr.es/c/1f8ab91c1)
* In `contrib/amcheck`, handle short-header varlena
  datums correctly (Andrey Borodin)
  [§](https://postgr.es/c/897e79486)

  This error could result in doing excess work while verifying a btree
  index, but seems not to have had any worse consequences.
* In `contrib/btree_gist`,
  fix `NaN` handling in the `float4`
  and `float8` opclasses (Bill Kim, Tom Lane)
  [§](https://postgr.es/c/1e1d07792)

  Comparisons, as well as the GiST penalty and distance functions, did
  not account for `NaN` and would give the wrong
  answer when handed one. It is recommended to
  reindex `btree_gist` indexes on float columns
  after installing this update, if there is any possibility that there
  are `NaN` entries in those columns.
* In `contrib/btree_gist`, fix sorting
  of `bit`/`varbit` entries during GiST index
  construction (Tom Lane)
  [§](https://postgr.es/c/558c4ea9a)

  Values of bit types were sorted as though they
  were `bytea`s, which did not cause any obvious failure
  but would result in an inefficient index, since the types'
  representations are different. It is recommended to
  reindex `btree_gist` indexes on bit columns
  after installing this update.
* In `contrib/btree_gist`, fix searches using a
  not-equal operator (Ayush Tiwari)
  [§](https://postgr.es/c/12c519207)

  For variable-length data types, the code for scanning non-leaf index
  pages applied the wrong comparison function, leading to wrong
  results and potentially crashes.
* In `contrib/dblink`
  and `contrib/postgres_fdw`, ensure that a user-mapping
  setting for `use_scram_passthrough` overrides one
  for a foreign server (Matheus Alcantara)
  [§](https://postgr.es/c/88d7748d2)
  [§](https://postgr.es/c/130396e6c)

  Previously the precedence went the other way, but that is
  inconsistent with the behavior of other foreign-table options.
* Reject setting `use_scram_passthrough`
  on `contrib/dblink` foreign-data wrappers
  (Matheus Alcantara)
  [§](https://postgr.es/c/cd777e27e)

  This option is only meaningful on foreign servers and user
  mappings, but dblink incorrectly allowed it at the FDW level as
  well (and then ignored it).
* Fix unguarded recursion and loops in
  `contrib/hstore_plperl`,
  `contrib/jsonb_plperl`, and
  `contrib/jsonb_plpython`
  (Aleksander Alekseev)
  [§](https://postgr.es/c/e3b7a43fa)
  [§](https://postgr.es/c/d65cf6f80)

  Prevent stack overflow when dealing with deeply
  nested `jsonb` values, and allow interruption of the infinite
  loop caused when attempting to dereference circular chains of Perl
  object references.
* Fix missed release of statistics catcache entry
  in `contrib/intarray` (Man Zeng)
  [§](https://postgr.es/c/e7544c518)

  This oversight led to warnings like “resource was not closed:
  cache pg_statistic”.
* In `contrib/ltree`, fix integer overflow in
  comparisons (Ayush Tiwari)
  [§](https://postgr.es/c/c3e36a9a5)

  `ltree` values containing more than about 14,653 labels
  resulted in wrong comparison answers due to overflow. If a btree
  index contains such values, it is probably corrupt and should be
  reindexed after installing this update.
* In `contrib/pgcrypto`, avoid double-free crash
  after encountering an error while using an OSSLCipher object
  (Yuelin Wang)
  [§](https://postgr.es/c/020426268)
* Fix out-of-bounds access
  in `contrib/pg_prewarm`'s autoprewarm worker
  (Matheus Alcantara)
  [§](https://postgr.es/c/3bf2cb225)

  The code tried to fetch a value from one past the end of an array,
  risking a segfault.
* Fix array overrun in `contrib/pg_surgery`'s
  `heap_force_kill` and
  `heap_force_freeze` functions (Michael Paquier)
  [§](https://postgr.es/c/2b09f8a91)

  Attempting to change a TID whose offset number equals
  MaxHeapTuplesPerPage wrote one byte past the end of the allocated
  array, potentially crashing the server.
* In `contrib/pg_surgery`, avoid infinite loop with
  TID arrays having more than 64K elements (Andrey Rachitskiy)
  [§](https://postgr.es/c/19f0391df)
* Avoid NULL-pointer dereference
  in `contrib/refint`'s
  `check_foreign_key()` (Ayush Tiwari)
  [§](https://postgr.es/c/ed0c4d5af)

  In the on-update-cascade case, a null value of a referenced column
  led to a crash. This is an oversight in the fix for CVE-2026-6637,
  but the code that was there before that wasn't really right either.
* Fix `contrib/seg` to print segments
  with `~` certainty indicators correctly
  (Ewan Young)
  [§](https://postgr.es/c/0004cab4d)

  Due to a typo, `seg_out()` did not print
  a `~` certainty indicator attached to a segment's
  upper boundary. Worse, if the lower boundary
  had `~` while the upper boundary had no indicator,
  the upper boundary was not printed at all, incorrectly converting
  the value into an open interval.
* Fix crash with namespace nodes in `contrib/xml2`'s
  `xpath_nodeset()` function (Andrey Chernyy,
  Michael Paquier)
  [§](https://postgr.es/c/91b57eade)
* Support building PostgreSQL with
  OpenSSL 4 (Daniel Gustafsson)
  [§](https://postgr.es/c/27cf3b5af)
* Update time zone data files to tzdata
  release 2026c (Tom Lane)
  [§](https://postgr.es/c/5f67124fa)

  Alberta (America/Edmonton) will be on year-round UTC-06
  (effectively, permanent DST) beginning in November 2026. This
  release assumes that their TZ abbreviation will
  be `CST` from that time forward. That seems likely
  to change, but it's unclear what new abbreviation will be used.

  Morocco (Africa/Casablanca) will move to permanent UTC+00,
  without daylight saving time transitions, on 2026-09-20.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-6.html)（英文原文，待翻譯）
