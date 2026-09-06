## Appendix F. Additional Supplied Modules and Extensions

**Table of Contents**

[F.1. amcheck — tools to verify table and index consistency](amcheck.md)
:   [F.1.1. Functions](amcheck.md#AMCHECK-FUNCTIONS)

    [F.1.2. Optional *`heapallindexed`* Verification](amcheck.md#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)

    [F.1.3. Using `amcheck` Effectively](amcheck.md#AMCHECK-USING-AMCHECK-EFFECTIVELY)

    [F.1.4. Repairing Corruption](amcheck.md#AMCHECK-REPAIRING-CORRUPTION)

[F.2. auth_delay — pause on authentication failure](auth-delay.md)
:   [F.2.1. Configuration Parameters](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)

    [F.2.2. Author](auth-delay.md#AUTH-DELAY-AUTHOR)

[F.3. auto_explain — log execution plans of slow queries](auto-explain.md)
:   [F.3.1. Configuration Parameters](auto-explain.md#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)

    [F.3.2. Example](auto-explain.md#AUTO-EXPLAIN-EXAMPLE)

    [F.3.3. Author](auto-explain.md#AUTO-EXPLAIN-AUTHOR)

[F.4. basebackup_to_shell — example "shell" pg_basebackup module](basebackup-to-shell.md)
:   [F.4.1. Configuration Parameters](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)

    [F.4.2. Author](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-AUTHOR)

[F.5. basic_archive — an example WAL archive module](basic-archive.md)
:   [F.5.1. Configuration Parameters](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

    [F.5.2. Notes](basic-archive.md#BASIC-ARCHIVE-NOTES)

    [F.5.3. Author](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

[F.6. bloom — bloom filter index access method](bloom.md)
:   [F.6.1. Parameters](bloom.md#BLOOM-PARAMETERS)

    [F.6.2. Examples](bloom.md#BLOOM-EXAMPLES)

    [F.6.3. Operator Class Interface](bloom.md#BLOOM-OPERATOR-CLASS-INTERFACE)

    [F.6.4. Limitations](bloom.md#BLOOM-LIMITATIONS)

    [F.6.5. Authors](bloom.md#BLOOM-AUTHORS)

[F.7. btree_gin — GIN operator classes with B-tree behavior](btree-gin.md)
:   [F.7.1. Example Usage](btree-gin.md#BTREE-GIN-EXAMPLE-USAGE)

    [F.7.2. Authors](btree-gin.md#BTREE-GIN-AUTHORS)

[F.8. btree_gist — GiST operator classes with B-tree behavior](btree-gist.md)
:   [F.8.1. Example Usage](btree-gist.md#BTREE-GIST-EXAMPLE-USAGE)

    [F.8.2. Authors](btree-gist.md#BTREE-GIST-AUTHORS)

[F.9. citext — a case-insensitive character string type](citext.md)
:   [F.9.1. Rationale](citext.md#CITEXT-RATIONALE)

    [F.9.2. How to Use It](citext.md#CITEXT-HOW-TO-USE-IT)

    [F.9.3. String Comparison Behavior](citext.md#CITEXT-STRING-COMPARISON-BEHAVIOR)

    [F.9.4. Limitations](citext.md#CITEXT-LIMITATIONS)

    [F.9.5. Author](citext.md#CITEXT-AUTHOR)

[F.10. cube — a multi-dimensional cube data type](cube.md)
:   [F.10.1. Syntax](cube.md#CUBE-SYNTAX)

    [F.10.2. Precision](cube.md#CUBE-PRECISION)

    [F.10.3. Usage](cube.md#CUBE-USAGE)

    [F.10.4. Defaults](cube.md#CUBE-DEFAULTS)

    [F.10.5. Notes](cube.md#CUBE-NOTES)

    [F.10.6. Credits](cube.md#CUBE-CREDITS)

[F.11. dblink — connect to other PostgreSQL databases](dblink.md)
:   [dblink_connect](contrib-dblink-connect.md) — opens a persistent connection to a remote database

    [dblink_connect_u](contrib-dblink-connect-u.md) — opens a persistent connection to a remote database, insecurely

    [dblink_disconnect](contrib-dblink-disconnect.md) — closes a persistent connection to a remote database

    [dblink](contrib-dblink-function.md) — executes a query in a remote database

    [dblink_exec](contrib-dblink-exec.md) — executes a command in a remote database

    [dblink_open](contrib-dblink-open.md) — opens a cursor in a remote database

    [dblink_fetch](contrib-dblink-fetch.md) — returns rows from an open cursor in a remote database

    [dblink_close](contrib-dblink-close.md) — closes a cursor in a remote database

    [dblink_get_connections](contrib-dblink-get-connections.md) — returns the names of all open named dblink connections

    [dblink_error_message](contrib-dblink-error-message.md) — gets last error message on the named connection

    [dblink_send_query](contrib-dblink-send-query.md) — sends an async query to a remote database

    [dblink_is_busy](contrib-dblink-is-busy.md) — checks if connection is busy with an async query

    [dblink_get_notify](contrib-dblink-get-notify.md) — retrieve async notifications on a connection

    [dblink_get_result](contrib-dblink-get-result.md) — gets an async query result

    [dblink_cancel_query](contrib-dblink-cancel-query.md) — cancels any active query on the named connection

    [dblink_get_pkey](contrib-dblink-get-pkey.md) — returns the positions and field names of a relation's primary key fields

    [dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — builds an INSERT statement using a local tuple, replacing the primary key field values with alternative supplied values

    [dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — builds a DELETE statement using supplied values for primary key field values

    [dblink_build_sql_update](contrib-dblink-build-sql-update.md) — builds an UPDATE statement using a local tuple, replacing the primary key field values with alternative supplied values

[F.12. dict_int — example full-text search dictionary for integers](dict-int.md)
:   [F.12.1. Configuration](dict-int.md#DICT-INT-CONFIG)

    [F.12.2. Usage](dict-int.md#DICT-INT-USAGE)

[F.13. dict_xsyn — example synonym full-text search dictionary](dict-xsyn.md)
:   [F.13.1. Configuration](dict-xsyn.md#DICT-XSYN-CONFIG)

    [F.13.2. Usage](dict-xsyn.md#DICT-XSYN-USAGE)

[F.14. earthdistance — calculate great-circle distances](earthdistance.md)
:   [F.14.1. Cube-Based Earth Distances](earthdistance.md#EARTHDISTANCE-CUBE-BASED)

    [F.14.2. Point-Based Earth Distances](earthdistance.md#EARTHDISTANCE-POINT-BASED)

[F.15. file_fdw — access data files in the server's file system](file-fdw.md)

[F.16. fuzzystrmatch — determine string similarities and distance](fuzzystrmatch.md)
:   [F.16.1. Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-SOUNDEX)

    [F.16.2. Daitch-Mokotoff Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-DAITCH-MOKOTOFF)

    [F.16.3. Levenshtein](fuzzystrmatch.md#FUZZYSTRMATCH-LEVENSHTEIN)

    [F.16.4. Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-METAPHONE)

    [F.16.5. Double Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-DOUBLE-METAPHONE)

[F.17. hstore — hstore key/value datatype](hstore.md)
:   [F.17.1. `hstore` External Representation](hstore.md#HSTORE-EXTERNAL-REP)

    [F.17.2. `hstore` Operators and Functions](hstore.md#HSTORE-OPS-FUNCS)

    [F.17.3. Indexes](hstore.md#HSTORE-INDEXES)

    [F.17.4. Examples](hstore.md#HSTORE-EXAMPLES)

    [F.17.5. Statistics](hstore.md#HSTORE-STATISTICS)

    [F.17.6. Compatibility](hstore.md#HSTORE-COMPATIBILITY)

    [F.17.7. Transforms](hstore.md#HSTORE-TRANSFORMS)

    [F.17.8. Authors](hstore.md#HSTORE-AUTHORS)

[F.18. intagg — integer aggregator and enumerator](intagg.md)
:   [F.18.1. Functions](intagg.md#INTAGG-FUNCTIONS)

    [F.18.2. Sample Uses](intagg.md#INTAGG-SAMPLES)

[F.19. intarray — manipulate arrays of integers](intarray.md)
:   [F.19.1. `intarray` Functions and Operators](intarray.md#INTARRAY-FUNCS-OPS)

    [F.19.2. Index Support](intarray.md#INTARRAY-INDEX)

    [F.19.3. Example](intarray.md#INTARRAY-EXAMPLE)

    [F.19.4. Benchmark](intarray.md#INTARRAY-BENCHMARK)

    [F.19.5. Authors](intarray.md#INTARRAY-AUTHORS)

[F.20. isn — data types for international standard numbers (ISBN, EAN, UPC, etc.)](isn.md)
:   [F.20.1. Data Types](isn.md#ISN-DATA-TYPES)

    [F.20.2. Casts](isn.md#ISN-CASTS)

    [F.20.3. Functions and Operators](isn.md#ISN-FUNCS-OPS)

    [F.20.4. Configuration Parameters](isn.md#ISN-CONFIGURATION-PARAMETERS)

    [F.20.5. Examples](isn.md#ISN-EXAMPLES)

    [F.20.6. Bibliography](isn.md#ISN-BIBLIOGRAPHY)

    [F.20.7. Author](isn.md#ISN-AUTHOR)

[F.21. lo — manage large objects](lo.md)
:   [F.21.1. Rationale](lo.md#LO-RATIONALE)

    [F.21.2. How to Use It](lo.md#LO-HOW-TO-USE)

    [F.21.3. Limitations](lo.md#LO-LIMITATIONS)

    [F.21.4. Author](lo.md#LO-AUTHOR)

[F.22. ltree — hierarchical tree-like data type](ltree.md)
:   [F.22.1. Definitions](ltree.md#LTREE-DEFINITIONS)

    [F.22.2. Operators and Functions](ltree.md#LTREE-OPS-FUNCS)

    [F.22.3. Indexes](ltree.md#LTREE-INDEXES)

    [F.22.4. Example](ltree.md#LTREE-EXAMPLE)

    [F.22.5. Transforms](ltree.md#LTREE-TRANSFORMS)

    [F.22.6. Authors](ltree.md#LTREE-AUTHORS)

[F.23. pageinspect — low-level inspection of database pages](pageinspect.md)
:   [F.23.1. General Functions](pageinspect.md#PAGEINSPECT-GENERAL-FUNCS)

    [F.23.2. Heap Functions](pageinspect.md#PAGEINSPECT-HEAP-FUNCS)

    [F.23.3. B-Tree Functions](pageinspect.md#PAGEINSPECT-B-TREE-FUNCS)

    [F.23.4. BRIN Functions](pageinspect.md#PAGEINSPECT-BRIN-FUNCS)

    [F.23.5. GIN Functions](pageinspect.md#PAGEINSPECT-GIN-FUNCS)

    [F.23.6. GiST Functions](pageinspect.md#PAGEINSPECT-GIST-FUNCS)

    [F.23.7. Hash Functions](pageinspect.md#PAGEINSPECT-HASH-FUNCS)

[F.24. passwordcheck — verify password strength](passwordcheck.md)
:   [F.24.1. Configuration Parameters](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

[F.25. pg_buffercache — inspect PostgreSQL buffer cache state](pgbuffercache.md)
:   [F.25.1. The `pg_buffercache` View](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE)

    [F.25.2. The `pg_buffercache_numa` View](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)

    [F.25.3. The `pg_buffercache_summary()` Function](pgbuffercache.md#PGBUFFERCACHE-SUMMARY)

    [F.25.4. The `pg_buffercache_usage_counts()` Function](pgbuffercache.md#PGBUFFERCACHE-USAGE-COUNTS)

    [F.25.5. The `pg_buffercache_evict()` Function](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)

    [F.25.6. The `pg_buffercache_evict_relation()` Function](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)

    [F.25.7. The `pg_buffercache_evict_all()` Function](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)

    [F.25.8. Sample Output](pgbuffercache.md#PGBUFFERCACHE-SAMPLE-OUTPUT)

    [F.25.9. Authors](pgbuffercache.md#PGBUFFERCACHE-AUTHORS)

[F.26. pgcrypto — cryptographic functions](pgcrypto.md)
:   [F.26.1. General Hashing Functions](pgcrypto.md#PGCRYPTO-GENERAL-HASHING-FUNCS)

    [F.26.2. Password Hashing Functions](pgcrypto.md#PGCRYPTO-PASSWORD-HASHING-FUNCS)

    [F.26.3. PGP Encryption Functions](pgcrypto.md#PGCRYPTO-PGP-ENC-FUNCS)

    [F.26.4. Raw Encryption Functions](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS)

    [F.26.5. Random-Data Functions](pgcrypto.md#PGCRYPTO-RANDOM-DATA-FUNCS)

    [F.26.6. OpenSSL Support Functions](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)

    [F.26.7. Configuration Parameters](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS)

    [F.26.8. Notes](pgcrypto.md#PGCRYPTO-NOTES)

    [F.26.9. Author](pgcrypto.md#PGCRYPTO-AUTHOR)

[F.27. pg_freespacemap — examine the free space map](pgfreespacemap.md)
:   [F.27.1. Functions](pgfreespacemap.md#PGFREESPACEMAP-FUNCS)

    [F.27.2. Sample Output](pgfreespacemap.md#PGFREESPACEMAP-SAMPLE-OUTPUT)

    [F.27.3. Author](pgfreespacemap.md#PGFREESPACEMAP-AUTHOR)

[F.28. pg_logicalinspect — logical decoding components inspection](pglogicalinspect.md)
:   [F.28.1. Functions](pglogicalinspect.md#PGLOGICALINSPECT-FUNCS)

    [F.28.2. Author](pglogicalinspect.md#PGLOGICALINSPECT-AUTHOR)

[F.29. pg_overexplain — allow EXPLAIN to dump even more details](pgoverexplain.md)
:   [F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)

    [F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)

    [F.29.3. Author](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

[F.30. pg_prewarm — preload relation data into buffer caches](pgprewarm.md)
:   [F.30.1. Functions](pgprewarm.md#PGPREWARM-FUNCS)

    [F.30.2. Configuration Parameters](pgprewarm.md#PGPREWARM-CONFIG-PARAMS)

    [F.30.3. Author](pgprewarm.md#PGPREWARM-AUTHOR)

[F.31. pgrowlocks — show a table's row locking information](pgrowlocks.md)
:   [F.31.1. Overview](pgrowlocks.md#PGROWLOCKS-OVERVIEW)

    [F.31.2. Sample Output](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)

    [F.31.3. Author](pgrowlocks.md#PGROWLOCKS-AUTHOR)

[F.32. pg_stat_statements — track statistics of SQL planning and execution](pgstatstatements.md)
:   [F.32.1. The `pg_stat_statements` View](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

    [F.32.2. The `pg_stat_statements_info` View](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

    [F.32.3. Functions](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)

    [F.32.4. Configuration Parameters](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)

    [F.32.5. Sample Output](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

    [F.32.6. Authors](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

[F.33. pgstattuple — obtain tuple-level statistics](pgstattuple.md)
:   [F.33.1. Functions](pgstattuple.md#PGSTATTUPLE-FUNCS)

    [F.33.2. Authors](pgstattuple.md#PGSTATTUPLE-AUTHORS)

[F.34. pg_surgery — perform low-level surgery on relation data](pgsurgery.md)
:   [F.34.1. Functions](pgsurgery.md#PGSURGERY-FUNCS)

    [F.34.2. Authors](pgsurgery.md#PGSURGERY-AUTHORS)

[F.35. pg_trgm — support for similarity of text using trigram matching](pgtrgm.md)
:   [F.35.1. Trigram (or Trigraph) Concepts](pgtrgm.md#PGTRGM-CONCEPTS)

    [F.35.2. Functions and Operators](pgtrgm.md#PGTRGM-FUNCS-OPS)

    [F.35.3. GUC Parameters](pgtrgm.md#PGTRGM-GUC)

    [F.35.4. Index Support](pgtrgm.md#PGTRGM-INDEX)

    [F.35.5. Text Search Integration](pgtrgm.md#PGTRGM-TEXT-SEARCH)

    [F.35.6. References](pgtrgm.md#PGTRGM-REFERENCES)

    [F.35.7. Authors](pgtrgm.md#PGTRGM-AUTHORS)

[F.36. pg_visibility — visibility map information and utilities](pgvisibility.md)
:   [F.36.1. Functions](pgvisibility.md#PGVISIBILITY-FUNCS)

    [F.36.2. Author](pgvisibility.md#PGVISIBILITY-AUTHOR)

[F.37. pg_walinspect — low-level WAL inspection](pgwalinspect.md)
:   [F.37.1. General Functions](pgwalinspect.md#PGWALINSPECT-FUNCS)

    [F.37.2. Author](pgwalinspect.md#PGWALINSPECT-AUTHOR)

[F.38. postgres_fdw — access data stored in external PostgreSQL servers](postgres-fdw.md)
:   [F.38.1. FDW Options of postgres_fdw](postgres-fdw.md#POSTGRES-FDW-OPTIONS)

    [F.38.2. Functions](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)

    [F.38.3. Connection Management](postgres-fdw.md#POSTGRES-FDW-CONNECTION-MANAGEMENT)

    [F.38.4. Transaction Management](postgres-fdw.md#POSTGRES-FDW-TRANSACTION-MANAGEMENT)

    [F.38.5. Remote Query Optimization](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)

    [F.38.6. Remote Query Execution Environment](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)

    [F.38.7. Cross-Version Compatibility](postgres-fdw.md#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)

    [F.38.8. Wait Events](postgres-fdw.md#POSTGRES-FDW-WAIT-EVENTS)

    [F.38.9. Configuration Parameters](postgres-fdw.md#POSTGRES-FDW-CONFIGURATION-PARAMETERS)

    [F.38.10. Examples](postgres-fdw.md#POSTGRES-FDW-EXAMPLES)

    [F.38.11. Author](postgres-fdw.md#POSTGRES-FDW-AUTHOR)

[F.39. seg — a datatype for line segments or floating point intervals](seg.md)
:   [F.39.1. Rationale](seg.md#SEG-RATIONALE)

    [F.39.2. Syntax](seg.md#SEG-SYNTAX)

    [F.39.3. Precision](seg.md#SEG-PRECISION)

    [F.39.4. Usage](seg.md#SEG-USAGE)

    [F.39.5. Notes](seg.md#SEG-NOTES)

    [F.39.6. Credits](seg.md#SEG-CREDITS)

[F.40. sepgsql — SELinux-, label-based mandatory access control (MAC) security module](sepgsql.md)
:   [F.40.1. Overview](sepgsql.md#SEPGSQL-OVERVIEW)

    [F.40.2. Installation](sepgsql.md#SEPGSQL-INSTALLATION)

    [F.40.3. Regression Tests](sepgsql.md#SEPGSQL-REGRESSION)

    [F.40.4. GUC Parameters](sepgsql.md#SEPGSQL-PARAMETERS)

    [F.40.5. Features](sepgsql.md#SEPGSQL-FEATURES)

    [F.40.6. Sepgsql Functions](sepgsql.md#SEPGSQL-FUNCTIONS)

    [F.40.7. Limitations](sepgsql.md#SEPGSQL-LIMITATIONS)

    [F.40.8. External Resources](sepgsql.md#SEPGSQL-RESOURCES)

    [F.40.9. Author](sepgsql.md#SEPGSQL-AUTHOR)

[F.41. spi — Server Programming Interface features/examples](contrib-spi.md)
:   [F.41.1. refint — Functions for Implementing Referential Integrity](contrib-spi.md#CONTRIB-SPI-REFINT)

    [F.41.2. autoinc — Functions for Autoincrementing Fields](contrib-spi.md#CONTRIB-SPI-AUTOINC)

    [F.41.3. insert_username — Functions for Tracking Who Changed a Table](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)

    [F.41.4. moddatetime — Functions for Tracking Last Modification Time](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

[F.42. sslinfo — obtain client SSL information](sslinfo.md)
:   [F.42.1. Functions Provided](sslinfo.md#SSLINFO-FUNCTIONS)

    [F.42.2. Author](sslinfo.md#SSLINFO-AUTHOR)

[F.43. tablefunc — functions that return tables (`crosstab` and others)](tablefunc.md)
:   [F.43.1. Functions Provided](tablefunc.md#TABLEFUNC-FUNCTIONS-SECT)

    [F.43.2. Author](tablefunc.md#TABLEFUNC-AUTHOR)

[F.44. tcn — a trigger function to notify listeners of changes to table content](tcn.md)

[F.45. test_decoding — SQL-based test/example module for WAL logical decoding](test-decoding.md)

[F.46. tsm_system_rows — the `SYSTEM_ROWS` sampling method for `TABLESAMPLE`](tsm-system-rows.md)
:   [F.46.1. Examples](tsm-system-rows.md#TSM-SYSTEM-ROWS-EXAMPLES)

[F.47. tsm_system_time — the `SYSTEM_TIME` sampling method for `TABLESAMPLE`](tsm-system-time.md)
:   [F.47.1. Examples](tsm-system-time.md#TSM-SYSTEM-TIME-EXAMPLES)

[F.48. unaccent — a text search dictionary which removes diacritics](unaccent.md)
:   [F.48.1. Configuration](unaccent.md#UNACCENT-CONFIGURATION)

    [F.48.2. Usage](unaccent.md#UNACCENT-USAGE)

    [F.48.3. Functions](unaccent.md#UNACCENT-FUNCTIONS)

[F.49. uuid-ossp — a UUID generator](uuid-ossp.md)
:   [F.49.1. `uuid-ossp` Functions](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)

    [F.49.2. Building `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)

    [F.49.3. Author](uuid-ossp.md#UUID-OSSP-AUTHOR)

[F.50. xml2 — XPath querying and XSLT functionality](xml2.md)
:   [F.50.1. Deprecation Notice](xml2.md#XML2-DEPRECATION)

    [F.50.2. Description of Functions](xml2.md#XML2-FUNCTIONS)

    [F.50.3. `xpath_table`](xml2.md#XML2-XPATH-TABLE)

    [F.50.4. XSLT Functions](xml2.md#XML2-XSLT)

    [F.50.5. Author](xml2.md#XML2-AUTHOR)

This appendix and the next one contain information on the
optional components
found in the `contrib` directory of the
PostgreSQL distribution.
These include porting tools, analysis utilities,
and plug-in features that are not part of the core PostgreSQL system.
They are separate mainly
because they address a limited audience or are too experimental
to be part of the main source tree. This does not preclude their
usefulness.

This appendix covers extensions and other server plug-in module
libraries found in
`contrib`. [Appendix G](../contrib-prog/README.md) covers utility
programs.

When building from the source distribution, these optional
components are not built
automatically, unless you build the "world" target
(see [Step 2](../../server-administration/installation/install-make.md#BUILD)).
You can build and install all of them by running:

```

make
make install
```

in the `contrib` directory of a configured source tree;
or to build and install
just one selected module, do the same in that module's subdirectory.
Many of the modules have regression tests, which can be executed by
running:

```

make check
```

before installation or

```

make installcheck
```

once you have a PostgreSQL server running.

If you are using a pre-packaged version of PostgreSQL,
these components are typically made available as a separate subpackage,
such as `postgresql-contrib`.

Many components supply new user-defined functions, operators, or types,
packaged as *extensions*.
To make use of one of these extensions, after you have installed the code
you need to register the new SQL objects in the database system.
This is done by executing
a [CREATE EXTENSION](../../reference/sql-commands/sql-createextension.md) command. In a fresh database,
you can simply do

```

CREATE EXTENSION extension_name;
```

This command registers the new SQL objects in the current database only,
so you need to run it in every database in which you want
the extension's facilities to be available. Alternatively, run it in
database `template1` so that the extension will be copied into
subsequently-created databases by default.

For all extensions, the `CREATE EXTENSION` command must be
run by a database superuser, unless the extension is
considered “trusted”. Trusted extensions can be run by any
user who has `CREATE` privilege on the current
database. Extensions that are trusted are identified as such in the
sections that follow. Generally, trusted extensions are ones that cannot
provide access to outside-the-database functionality.

<a id="CONTRIB-TRUSTED-EXTENSIONS"></a>

The following extensions are trusted in a default installation:

<table border="0" class="simplelist" summary="Simple list"><tr><td><a class="xref" href="btree-gin.md">btree_gin</a></td><td><a class="xref" href="fuzzystrmatch.md">fuzzystrmatch</a></td><td><a class="xref" href="ltree.md">ltree</a></td><td><a class="xref" href="tcn.md">tcn</a></td></tr><tr><td><a class="xref" href="btree-gist.md">btree_gist</a></td><td><a class="xref" href="hstore.md">hstore</a></td><td><a class="xref" href="pgcrypto.md">pgcrypto</a></td><td><a class="xref" href="tsm-system-rows.md">tsm_system_rows</a></td></tr><tr><td><a class="xref" href="citext.md">citext</a></td><td><a class="xref" href="intarray.md">intarray</a></td><td><a class="xref" href="pgtrgm.md">pg_trgm</a></td><td><a class="xref" href="tsm-system-time.md">tsm_system_time</a></td></tr><tr><td><a class="xref" href="cube.md">cube</a></td><td><a class="xref" href="isn.md">isn</a></td><td><a class="xref" href="seg.md">seg</a></td><td><a class="xref" href="unaccent.md">unaccent</a></td></tr><tr><td><a class="xref" href="dict-int.md">dict_int</a></td><td><a class="xref" href="lo.md">lo</a></td><td><a class="xref" href="tablefunc.md">tablefunc</a></td><td><a class="xref" href="uuid-ossp.md">uuid-ossp</a></td></tr></table>

Many extensions allow you to install their objects in a schema of your
choice. To do that, add `SCHEMA
schema_name` to the `CREATE EXTENSION`
command. By default, the objects will be placed in your current creation
target schema, which in turn defaults to `public`.

Note, however, that some of these components are not “extensions”
in this sense, but are loaded into the server in some other way, for instance
by way of
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES). See the documentation of each
component for details.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib.html)（英文原文，待翻譯）
