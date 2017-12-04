# F. 延伸支援模組[^1]

**Table of Contents**

[F.1. adminpack](https://www.postgresql.org/docs/10/static/adminpack.html)

[F.2. amcheck](https://www.postgresql.org/docs/10/static/amcheck.html)

[F.2.1. Functions](https://www.postgresql.org/docs/10/static/amcheck.html#idm46428636945584)

[F.2.2. Using`amcheck`effectively](https://www.postgresql.org/docs/10/static/amcheck.html#idm46428636915840)

[F.2.3. Repairing corruption](https://www.postgresql.org/docs/10/static/amcheck.html#idm46428636896240)

[F.3. auth\_delay](https://www.postgresql.org/docs/10/static/auth-delay.html)

[F.3.1. Configuration Parameters](https://www.postgresql.org/docs/10/static/auth-delay.html#idm46428636883824)

[F.3.2. Author](https://www.postgresql.org/docs/10/static/auth-delay.html#idm46428636878784)

[F.4. auto\_explain](https://www.postgresql.org/docs/10/static/auto-explain.html)

[F.4.1. Configuration Parameters](https://www.postgresql.org/docs/10/static/auto-explain.html#idm46428636869424)

[F.4.2. Example](https://www.postgresql.org/docs/10/static/auto-explain.html#idm46428636821600)

[F.4.3. Author](https://www.postgresql.org/docs/10/static/auto-explain.html#idm46428636818320)

[F.5. bloom](https://www.postgresql.org/docs/10/static/bloom.html)

[F.5.1. Parameters](https://www.postgresql.org/docs/10/static/bloom.html#idm46428636811264)

[F.5.2. Examples](https://www.postgresql.org/docs/10/static/bloom.html#idm46428636803232)

[F.5.3. Operator Class Interface](https://www.postgresql.org/docs/10/static/bloom.html#idm46428636787584)

[F.5.4. Limitations](https://www.postgresql.org/docs/10/static/bloom.html#idm46428636785552)

[F.5.5. Authors](https://www.postgresql.org/docs/10/static/bloom.html#idm46428636782016)

[F.6. btree\_gin](https://www.postgresql.org/docs/10/static/btree-gin.html)

[F.6.1. Example Usage](https://www.postgresql.org/docs/10/static/btree-gin.html#idm46428636764912)

[F.6.2. Authors](https://www.postgresql.org/docs/10/static/btree-gin.html#idm46428636763696)

[F.7. btree\_gist](https://www.postgresql.org/docs/10/static/btree-gist.html)

[F.7.1. Example Usage](https://www.postgresql.org/docs/10/static/btree-gist.html#idm46428636736160)

[F.7.2. Authors](https://www.postgresql.org/docs/10/static/btree-gist.html#idm46428636730672)

[F.8. chkpass](https://www.postgresql.org/docs/10/static/chkpass.html)

[F.8.1. Author](https://www.postgresql.org/docs/10/static/chkpass.html#idm46428636718224)

[F.9. citext](https://www.postgresql.org/docs/10/static/citext.html)

[F.9.1. Rationale](https://www.postgresql.org/docs/10/static/citext.html#idm46428636712000)

[F.9.2. How to Use It](https://www.postgresql.org/docs/10/static/citext.html#idm46428636699936)

[F.9.3. String Comparison Behavior](https://www.postgresql.org/docs/10/static/citext.html#idm46428636695440)

[F.9.4. Limitations](https://www.postgresql.org/docs/10/static/citext.html#idm46428636672480)

[F.9.5. Author](https://www.postgresql.org/docs/10/static/citext.html#idm46428636655120)

[F.10. cube](https://www.postgresql.org/docs/10/static/cube.html)

[F.10.1. Syntax](https://www.postgresql.org/docs/10/static/cube.html#idm46428636650256)

[F.10.2. Precision](https://www.postgresql.org/docs/10/static/cube.html#idm46428636622592)

[F.10.3. Usage](https://www.postgresql.org/docs/10/static/cube.html#idm46428636621744)

[F.10.4. Defaults](https://www.postgresql.org/docs/10/static/cube.html#idm46428636528880)

[F.10.5. Notes](https://www.postgresql.org/docs/10/static/cube.html#idm46428636524208)

[F.10.6. Credits](https://www.postgresql.org/docs/10/static/cube.html#idm46428636521616)

[F.11. dblink](https://www.postgresql.org/docs/10/static/dblink.html)

[dblink\_connect](https://www.postgresql.org/docs/10/static/contrib-dblink-connect.html)

— opens a persistent connection to a remote database

[dblink\_connect\_u](https://www.postgresql.org/docs/10/static/contrib-dblink-connect-u.html)

— opens a persistent connection to a remote database, insecurely

[dblink\_disconnect](https://www.postgresql.org/docs/10/static/contrib-dblink-disconnect.html)

— closes a persistent connection to a remote database

[dblink](https://www.postgresql.org/docs/10/static/contrib-dblink-function.html)

— executes a query in a remote database

[dblink\_exec](https://www.postgresql.org/docs/10/static/contrib-dblink-exec.html)

— executes a command in a remote database

[dblink\_open](https://www.postgresql.org/docs/10/static/contrib-dblink-open.html)

— opens a cursor in a remote database

[dblink\_fetch](https://www.postgresql.org/docs/10/static/contrib-dblink-fetch.html)

— returns rows from an open cursor in a remote database

[dblink\_close](https://www.postgresql.org/docs/10/static/contrib-dblink-close.html)

— closes a cursor in a remote database

[dblink\_get\_connections](https://www.postgresql.org/docs/10/static/contrib-dblink-get-connections.html)

— returns the names of all open named dblink connections

[dblink\_error\_message](https://www.postgresql.org/docs/10/static/contrib-dblink-error-message.html)

— gets last error message on the named connection

[dblink\_send\_query](https://www.postgresql.org/docs/10/static/contrib-dblink-send-query.html)

— sends an async query to a remote database

[dblink\_is\_busy](https://www.postgresql.org/docs/10/static/contrib-dblink-is-busy.html)

— checks if connection is busy with an async query

[dblink\_get\_notify](https://www.postgresql.org/docs/10/static/contrib-dblink-get-notify.html)

— retrieve async notifications on a connection

[dblink\_get\_result](https://www.postgresql.org/docs/10/static/contrib-dblink-get-result.html)

— gets an async query result

[dblink\_cancel\_query](https://www.postgresql.org/docs/10/static/contrib-dblink-cancel-query.html)

— cancels any active query on the named connection

[dblink\_get\_pkey](https://www.postgresql.org/docs/10/static/contrib-dblink-get-pkey.html)

— returns the positions and field names of a relation's primary key fields

[dblink\_build\_sql\_insert](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-insert.html)

— builds an INSERT statement using a local tuple, replacing the primary key field values with alternative supplied values

[dblink\_build\_sql\_delete](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-delete.html)

— builds a DELETE statement using supplied values for primary key field values

[dblink\_build\_sql\_update](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-update.html)

— builds an UPDATE statement using a local tuple, replacing the primary key field values with alternative supplied values

[F.12. dict\_int](https://www.postgresql.org/docs/10/static/dict-int.html)

[F.12.1. Configuration](https://www.postgresql.org/docs/10/static/dict-int.html#idm46428636189392)

[F.12.2. Usage](https://www.postgresql.org/docs/10/static/dict-int.html#idm46428636182272)

[F.13. dict\_xsyn](https://www.postgresql.org/docs/10/static/dict-xsyn.html)

[F.13.1. Configuration](https://www.postgresql.org/docs/10/static/dict-xsyn.html#idm46428636172400)

[F.13.2. Usage](https://www.postgresql.org/docs/10/static/dict-xsyn.html#idm46428636153728)

[F.14. earthdistance](https://www.postgresql.org/docs/10/static/earthdistance.html)

[F.14.1. Cube-based Earth Distances](https://www.postgresql.org/docs/10/static/earthdistance.html#idm46428636139088)

[F.14.2. Point-based Earth Distances](https://www.postgresql.org/docs/10/static/earthdistance.html#idm46428636109744)

[F.15. file\_fdw](https://www.postgresql.org/docs/10/static/file-fdw.html)

[F.16. fuzzystrmatch](https://www.postgresql.org/docs/10/static/fuzzystrmatch.html)

[F.16.1. Soundex](https://www.postgresql.org/docs/10/static/fuzzystrmatch.html#idm46428636034112)

[F.16.2. Levenshtein](https://www.postgresql.org/docs/10/static/fuzzystrmatch.html#idm46428636025488)

[F.16.3. Metaphone](https://www.postgresql.org/docs/10/static/fuzzystrmatch.html#idm46428636014320)

[F.16.4. Double Metaphone](https://www.postgresql.org/docs/10/static/fuzzystrmatch.html#idm46428636009088)

[F.17. hstore](https://www.postgresql.org/docs/10/static/hstore.html)

[F.17.1.`hstore`External Representation](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635999696)

[F.17.2.`hstore`Operators and Functions](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635983504)

[F.17.3. Indexes](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635827552)

[F.17.4. Examples](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635815424)

[F.17.5. Statistics](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635806832)

[F.17.6. Compatibility](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635802096)

[F.17.7. Transforms](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635796800)

[F.17.8. Authors](https://www.postgresql.org/docs/10/static/hstore.html#idm46428635790128)

[F.18. intagg](https://www.postgresql.org/docs/10/static/intagg.html)

[F.18.1. Functions](https://www.postgresql.org/docs/10/static/intagg.html#idm46428635783152)

[F.18.2. Sample Uses](https://www.postgresql.org/docs/10/static/intagg.html#idm46428635776400)

[F.19. intarray](https://www.postgresql.org/docs/10/static/intarray.html)

[F.19.1.`intarray`Functions and Operators](https://www.postgresql.org/docs/10/static/intarray.html#idm46428635760336)

[F.19.2. Index Support](https://www.postgresql.org/docs/10/static/intarray.html#idm46428635672544)

[F.19.3. Example](https://www.postgresql.org/docs/10/static/intarray.html#idm46428635664800)

[F.19.4. Benchmark](https://www.postgresql.org/docs/10/static/intarray.html#idm46428635662800)

[F.19.5. Authors](https://www.postgresql.org/docs/10/static/intarray.html#idm46428635658064)

[F.20. isn](https://www.postgresql.org/docs/10/static/isn.html)

[F.20.1. Data Types](https://www.postgresql.org/docs/10/static/isn.html#idm46428635651808)

[F.20.2. Casts](https://www.postgresql.org/docs/10/static/isn.html#idm46428635630608)

[F.20.3. Functions and Operators](https://www.postgresql.org/docs/10/static/isn.html#idm46428635623584)

[F.20.4. Examples](https://www.postgresql.org/docs/10/static/isn.html#idm46428635602080)

[F.20.5. Bibliography](https://www.postgresql.org/docs/10/static/isn.html#idm46428635598896)

[F.20.6. Author](https://www.postgresql.org/docs/10/static/isn.html#idm46428635591152)

[F.21. lo](https://www.postgresql.org/docs/10/static/lo.html)

[F.21.1. Rationale](https://www.postgresql.org/docs/10/static/lo.html#idm46428635584992)

[F.21.2. How to Use It](https://www.postgresql.org/docs/10/static/lo.html#idm46428635577008)

[F.21.3. Limitations](https://www.postgresql.org/docs/10/static/lo.html#idm46428635572400)

[F.21.4. Author](https://www.postgresql.org/docs/10/static/lo.html#idm46428635565472)

[F.22. ltree](https://www.postgresql.org/docs/10/static/ltree.html)

[F.22.1. Definitions](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635561264)

[F.22.2. Operators and Functions](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635503696)

[F.22.3. Indexes](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635365248)

[F.22.4. Example](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635345248)

[F.22.5. Transforms](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635331296)

[F.22.6. Authors](https://www.postgresql.org/docs/10/static/ltree.html#idm46428635326608)

[F.23. pageinspect](https://www.postgresql.org/docs/10/static/pageinspect.html)

[F.23.1. General Functions](https://www.postgresql.org/docs/10/static/pageinspect.html#idm46428635320864)

[F.23.2. B-tree Functions](https://www.postgresql.org/docs/10/static/pageinspect.html#idm46428635269984)

[F.23.3. BRIN Functions](https://www.postgresql.org/docs/10/static/pageinspect.html#idm46428635246304)

[F.23.4. GIN Functions](https://www.postgresql.org/docs/10/static/pageinspect.html#idm46428635225552)

[F.23.5. Hash Functions](https://www.postgresql.org/docs/10/static/pageinspect.html#idm46428635210400)

[F.24. passwordcheck](https://www.postgresql.org/docs/10/static/passwordcheck.html)

[F.25. pg\_buffercache](https://www.postgresql.org/docs/10/static/pgbuffercache.html)

[F.25.1. The`pg_buffercache`View](https://www.postgresql.org/docs/10/static/pgbuffercache.html#idm46428635163904)

[F.25.2. Sample Output](https://www.postgresql.org/docs/10/static/pgbuffercache.html#idm46428635139888)

[F.25.3. Authors](https://www.postgresql.org/docs/10/static/pgbuffercache.html#idm46428635138000)

[F.26. pgcrypto](https://www.postgresql.org/docs/10/static/pgcrypto.html)

[F.26.1. General Hashing Functions](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428635130224)

[F.26.2. Password Hashing Functions](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428635111328)

[F.26.3. PGP Encryption Functions](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428635025696)

[F.26.4. Raw Encryption Functions](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428634927392)

[F.26.5. Random-Data Functions](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428634902160)

[F.26.6. Notes](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428634897728)

[F.26.7. Author](https://www.postgresql.org/docs/10/static/pgcrypto.html#idm46428634857840)

[F.27. pg\_freespacemap](https://www.postgresql.org/docs/10/static/pgfreespacemap.html)

[F.27.1. Functions](https://www.postgresql.org/docs/10/static/pgfreespacemap.html#idm46428634840160)

[F.27.2. Sample Output](https://www.postgresql.org/docs/10/static/pgfreespacemap.html#idm46428634831680)

[F.27.3. Author](https://www.postgresql.org/docs/10/static/pgfreespacemap.html#idm46428634829744)

[F.28. pg\_prewarm](https://www.postgresql.org/docs/10/static/pgprewarm.html)

[F.28.1. Functions](https://www.postgresql.org/docs/10/static/pgprewarm.html#idm46428634824080)

[F.28.2. Author](https://www.postgresql.org/docs/10/static/pgprewarm.html#idm46428634816224)

[F.29. pgrowlocks](https://www.postgresql.org/docs/10/static/pgrowlocks.html)

[F.29.1. Overview](https://www.postgresql.org/docs/10/static/pgrowlocks.html#idm46428634806736)

[F.29.2. Sample Output](https://www.postgresql.org/docs/10/static/pgrowlocks.html#idm46428634782064)

[F.29.3. Author](https://www.postgresql.org/docs/10/static/pgrowlocks.html#idm46428634780656)

[F.30. pg\_stat\_statements](https://www.postgresql.org/docs/10/static/pgstatstatements.html)

[F.30.1. The`pg_stat_statements`View](https://www.postgresql.org/docs/10/static/pgstatstatements.html#idm46428634770256)

[F.30.2. Functions](https://www.postgresql.org/docs/10/static/pgstatstatements.html#idm46428634701552)

[F.30.3. Configuration Parameters](https://www.postgresql.org/docs/10/static/pgstatstatements.html#idm46428634688944)

[F.30.4. Sample Output](https://www.postgresql.org/docs/10/static/pgstatstatements.html#idm46428634666272)

[F.30.5. Authors](https://www.postgresql.org/docs/10/static/pgstatstatements.html#idm46428634663728)

[F.31. pgstattuple](https://www.postgresql.org/docs/10/static/pgstattuple.html)

[F.31.1. Functions](https://www.postgresql.org/docs/10/static/pgstattuple.html#idm46428634656048)

[F.31.2. Authors](https://www.postgresql.org/docs/10/static/pgstattuple.html#idm46428634542784)

[F.32. pg\_trgm](https://www.postgresql.org/docs/10/static/pgtrgm.html)

[F.32.1. Trigram \(or Trigraph\) Concepts](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634538704)

[F.32.2. Functions and Operators](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634524336)

[F.32.3. GUC Parameters](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634479328)

[F.32.4. Index Support](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634469168)

[F.32.5. Text Search Integration](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634444576)

[F.32.6. References](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634436816)

[F.32.7. Authors](https://www.postgresql.org/docs/10/static/pgtrgm.html#idm46428634434672)

[F.33. pg\_visibility](https://www.postgresql.org/docs/10/static/pgvisibility.html)

[F.33.1. Functions](https://www.postgresql.org/docs/10/static/pgvisibility.html#idm46428634423952)

[F.33.2. Author](https://www.postgresql.org/docs/10/static/pgvisibility.html#idm46428634407392)

[F.34. postgres\_fdw](https://www.postgresql.org/docs/10/static/postgres-fdw.html)

[F.34.1. FDW Options of postgres\_fdw](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634379088)

[F.34.2. Connection Management](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634305472)

[F.34.3. Transaction Management](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634303728)

[F.34.4. Remote Query Optimization](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634296048)

[F.34.5. Remote Query Execution Environment](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634279792)

[F.34.6. Cross-Version Compatibility](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634262256)

[F.34.7. Examples](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634255488)

[F.34.8. Author](https://www.postgresql.org/docs/10/static/postgres-fdw.html#idm46428634241488)

[F.35. seg](https://www.postgresql.org/docs/10/static/seg.html)

[F.35.1. Rationale](https://www.postgresql.org/docs/10/static/seg.html#idm46428634237024)

[F.35.2. Syntax](https://www.postgresql.org/docs/10/static/seg.html#idm46428634232000)

[F.35.3. Precision](https://www.postgresql.org/docs/10/static/seg.html#idm46428634184688)

[F.35.4. Usage](https://www.postgresql.org/docs/10/static/seg.html#idm46428634182800)

[F.35.5. Notes](https://www.postgresql.org/docs/10/static/seg.html#idm46428634159696)

[F.35.6. Credits](https://www.postgresql.org/docs/10/static/seg.html#idm46428634154512)

[F.36. sepgsql](https://www.postgresql.org/docs/10/static/sepgsql.html)

[F.36.1. Overview](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-OVERVIEW)

[F.36.2. Installation](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-INSTALLATION)

[F.36.3. Regression Tests](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-REGRESSION)

[F.36.4. GUC Parameters](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-PARAMETERS)

[F.36.5. Features](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-FEATURES)

[F.36.6. Sepgsql Functions](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-FUNCTIONS)

[F.36.7. Limitations](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-LIMITATIONS)

[F.36.8. External Resources](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-RESOURCES)

[F.36.9. Author](https://www.postgresql.org/docs/10/static/sepgsql.html#SEPGSQL-AUTHOR)

[F.37. spi](https://www.postgresql.org/docs/10/static/contrib-spi.html)

[F.37.1. refint — Functions for Implementing Referential Integrity](https://www.postgresql.org/docs/10/static/contrib-spi.html#idm46428633972496)

[F.37.2. timetravel — Functions for Implementing Time Travel](https://www.postgresql.org/docs/10/static/contrib-spi.html#idm46428633962528)

[F.37.3. autoinc — Functions for Autoincrementing Fields](https://www.postgresql.org/docs/10/static/contrib-spi.html#idm46428633944272)

[F.37.4. insert\_username — Functions for Tracking Who Changed a Table](https://www.postgresql.org/docs/10/static/contrib-spi.html#idm46428633938352)

[F.37.5. moddatetime — Functions for Tracking Last Modification Time](https://www.postgresql.org/docs/10/static/contrib-spi.html#idm46428633933920)

[F.38. sslinfo](https://www.postgresql.org/docs/10/static/sslinfo.html)

[F.38.1. Functions Provided](https://www.postgresql.org/docs/10/static/sslinfo.html#idm46428633923744)

[F.38.2. Author](https://www.postgresql.org/docs/10/static/sslinfo.html#idm46428633891344)

[F.39. tablefunc](https://www.postgresql.org/docs/10/static/tablefunc.html)

[F.39.1. Functions Provided](https://www.postgresql.org/docs/10/static/tablefunc.html#idm46428633885408)

[F.39.2. Author](https://www.postgresql.org/docs/10/static/tablefunc.html#idm46428633724304)

[F.40. tcn](https://www.postgresql.org/docs/10/static/tcn.html)

[F.41. test\_decoding](https://www.postgresql.org/docs/10/static/test-decoding.html)

[F.42. tsm\_system\_rows](https://www.postgresql.org/docs/10/static/tsm-system-rows.html)

[F.42.1. Examples](https://www.postgresql.org/docs/10/static/tsm-system-rows.html#idm46428633697472)

[F.43. tsm\_system\_time](https://www.postgresql.org/docs/10/static/tsm-system-time.html)

[F.43.1. Examples](https://www.postgresql.org/docs/10/static/tsm-system-time.html#idm46428633683136)

[F.44. unaccent](https://www.postgresql.org/docs/10/static/unaccent.html)

[F.44.1. Configuration](https://www.postgresql.org/docs/10/static/unaccent.html#idm46428633673184)

[F.44.2. Usage](https://www.postgresql.org/docs/10/static/unaccent.html#idm46428633664672)

[F.44.3. Functions](https://www.postgresql.org/docs/10/static/unaccent.html#idm46428633648256)

[F.45. uuid-ossp](https://www.postgresql.org/docs/10/static/uuid-ossp.html)

[F.45.1.`uuid-ossp`Functions](https://www.postgresql.org/docs/10/static/uuid-ossp.html#idm46428633635312)

[F.45.2. Building`uuid-ossp`](https://www.postgresql.org/docs/10/static/uuid-ossp.html#idm46428633607040)

[F.45.3. Author](https://www.postgresql.org/docs/10/static/uuid-ossp.html#idm46428633594848)

[F.46. xml2](https://www.postgresql.org/docs/10/static/xml2.html)

[F.46.1. Deprecation Notice](https://www.postgresql.org/docs/10/static/xml2.html#idm46428633590480)

[F.46.2. Description of Functions](https://www.postgresql.org/docs/10/static/xml2.html#idm46428633587984)

[F.46.3.`xpath_table`](https://www.postgresql.org/docs/10/static/xml2.html#idm46428633554064)

[F.46.4. XSLT Functions](https://www.postgresql.org/docs/10/static/xml2.html#idm46428633516816)

[F.46.5. Author](https://www.postgresql.org/docs/10/static/xml2.html#idm46428633510848)

This appendix and the next one contain information regarding the modules that can be found in the`contrib`directory of thePostgreSQLdistribution. These include porting tools, analysis utilities, and plug-in features that are not part of the core PostgreSQL system, mainly because they address a limited audience or are too experimental to be part of the main source tree. This does not preclude their usefulness.

This appendix covers extensions and other server plug-in modules found in`contrib`.[Appendix G](https://www.postgresql.org/docs/10/static/contrib-prog.html)covers utility programs.

When building from the source distribution, these components are not built automatically, unless you build the "world" target \(see[Step 2](https://www.postgresql.org/docs/10/static/install-procedure.html#BUILD)\). You can build and install all of them by running:

```
make
make install
```

in the`contrib`directory of a configured source tree; or to build and install just one selected module, do the same in that module's subdirectory. Many of the modules have regression tests, which can be executed by running:

```
make check
```

before installation or

```
make installcheck
```

once you have aPostgreSQLserver running.

If you are using a pre-packaged version ofPostgreSQL, these modules are typically made available as a separate subpackage, such as`postgresql-contrib`.

Many modules supply new user-defined functions, operators, or types. To make use of one of these modules, after you have installed the code you need to register the new SQL objects in the database system. InPostgreSQL9.1 and later, this is done by executing a[CREATE EXTENSION](https://www.postgresql.org/docs/10/static/sql-createextension.html)command. In a fresh database, you can simply do

```
CREATE EXTENSION 
module_name
;

```

This command must be run by a database superuser. This registers the new SQL objects in the current database only, so you need to run this command in each database that you want the module's facilities to be available in. Alternatively, run it in database`template1`so that the extension will be copied into subsequently-created databases by default.

Many modules allow you to install their objects in a schema of your choice. To do that, add`SCHEMA`_`schema_name`_to the`CREATE EXTENSION`command. By default, the objects will be placed in your current creation target schema, typically`public`.

If your database was brought forward by dump and reload from a pre-9.1 version ofPostgreSQL, and you had been using the pre-9.1 version of the module in it, you should instead do

```
CREATE EXTENSION 
module_name
 FROM unpackaged;

```

This will update the pre-9.1 objects of the module into a proper_extension_object. Future updates to the module will be managed by[ALTER EXTENSION](https://www.postgresql.org/docs/10/static/sql-alterextension.html). For more information about extension updates, see[Section 37.15](https://www.postgresql.org/docs/10/static/extend-extensions.html).

Note, however, that some of these modules are not“extensions”in this sense, but are loaded into the server in some other way, for instance by way of[shared\_preload\_libraries](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES). See the documentation of each module for details.

---



[^1]:  [PostgreSQL: Documentation: 10: Appendix F. Additional Supplied Modules](https://www.postgresql.org/docs/10/static/contrib.html)

