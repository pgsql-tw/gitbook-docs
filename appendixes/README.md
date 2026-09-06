# Part VIII. Appendixes

**Table of Contents**

[A. PostgreSQL Error Codes](errcodes-appendix/README.md)

[B. Date/Time Support](datetime-appendix/README.md)
:   [B.1. Date/Time Input Interpretation](datetime-appendix/datetime-input-rules.md)

    [B.2. Handling of Invalid or Ambiguous Timestamps](datetime-appendix/datetime-invalid-input.md)

    [B.3. Date/Time Key Words](datetime-appendix/datetime-keywords.md)

    [B.4. Date/Time Configuration Files](datetime-appendix/datetime-config-files.md)

    [B.5. POSIX Time Zone Specifications](datetime-appendix/datetime-posix-timezone-specs.md)

    [B.6. History of Units](datetime-appendix/datetime-units-history.md)

    [B.7. Julian Dates](datetime-appendix/datetime-julian-dates.md)

[C. SQL Key Words](sql-keywords-appendix/README.md)

[D. SQL Conformance](features/README.md)
:   [D.1. Supported Features](features/features-sql-standard.md)

    [D.2. Unsupported Features](features/unsupported-features-sql-standard.md)

    [D.3. XML Limits and Conformance to SQL/XML](features/xml-limits-conformance.md)

[E. Release Notes](release/README.md)
:   [E.1. Release 18.6](release/release-18-6.md)

    [E.2. Release 18.4](release/release-18-4.md)

    [E.3. Release 18.3](release/release-18-3.md)

    [E.4. Release 18.2](release/release-18-2.md)

    [E.5. Release 18.1](release/release-18-1.md)

    [E.6. Release 18](release/release-18.md)

    [E.7. Prior Releases](release/release-prior.md)

[F. Additional Supplied Modules and Extensions](contrib/README.md)
:   [F.1. amcheck — tools to verify table and index consistency](contrib/amcheck.md)

    [F.2. auth_delay — pause on authentication failure](contrib/auth-delay.md)

    [F.3. auto_explain — log execution plans of slow queries](contrib/auto-explain.md)

    [F.4. basebackup_to_shell — example "shell" pg_basebackup module](contrib/basebackup-to-shell.md)

    [F.5. basic_archive — an example WAL archive module](contrib/basic-archive.md)

    [F.6. bloom — bloom filter index access method](contrib/bloom.md)

    [F.7. btree_gin — GIN operator classes with B-tree behavior](contrib/btree-gin.md)

    [F.8. btree_gist — GiST operator classes with B-tree behavior](contrib/btree-gist.md)

    [F.9. citext — a case-insensitive character string type](contrib/citext.md)

    [F.10. cube — a multi-dimensional cube data type](contrib/cube.md)

    [F.11. dblink — connect to other PostgreSQL databases](contrib/dblink.md)

    [F.12. dict_int — example full-text search dictionary for integers](contrib/dict-int.md)

    [F.13. dict_xsyn — example synonym full-text search dictionary](contrib/dict-xsyn.md)

    [F.14. earthdistance — calculate great-circle distances](contrib/earthdistance.md)

    [F.15. file_fdw — access data files in the server's file system](contrib/file-fdw.md)

    [F.16. fuzzystrmatch — determine string similarities and distance](contrib/fuzzystrmatch.md)

    [F.17. hstore — hstore key/value datatype](contrib/hstore.md)

    [F.18. intagg — integer aggregator and enumerator](contrib/intagg.md)

    [F.19. intarray — manipulate arrays of integers](contrib/intarray.md)

    [F.20. isn — data types for international standard numbers (ISBN, EAN, UPC, etc.)](contrib/isn.md)

    [F.21. lo — manage large objects](contrib/lo.md)

    [F.22. ltree — hierarchical tree-like data type](contrib/ltree.md)

    [F.23. pageinspect — low-level inspection of database pages](contrib/pageinspect.md)

    [F.24. passwordcheck — verify password strength](contrib/passwordcheck.md)

    [F.25. pg_buffercache — inspect PostgreSQL buffer cache state](contrib/pgbuffercache.md)

    [F.26. pgcrypto — cryptographic functions](contrib/pgcrypto.md)

    [F.27. pg_freespacemap — examine the free space map](contrib/pgfreespacemap.md)

    [F.28. pg_logicalinspect — logical decoding components inspection](contrib/pglogicalinspect.md)

    [F.29. pg_overexplain — allow EXPLAIN to dump even more details](contrib/pgoverexplain.md)

    [F.30. pg_prewarm — preload relation data into buffer caches](contrib/pgprewarm.md)

    [F.31. pgrowlocks — show a table's row locking information](contrib/pgrowlocks.md)

    [F.32. pg_stat_statements — track statistics of SQL planning and execution](contrib/pgstatstatements.md)

    [F.33. pgstattuple — obtain tuple-level statistics](contrib/pgstattuple.md)

    [F.34. pg_surgery — perform low-level surgery on relation data](contrib/pgsurgery.md)

    [F.35. pg_trgm — support for similarity of text using trigram matching](contrib/pgtrgm.md)

    [F.36. pg_visibility — visibility map information and utilities](contrib/pgvisibility.md)

    [F.37. pg_walinspect — low-level WAL inspection](contrib/pgwalinspect.md)

    [F.38. postgres_fdw — access data stored in external PostgreSQL servers](contrib/postgres-fdw.md)

    [F.39. seg — a datatype for line segments or floating point intervals](contrib/seg.md)

    [F.40. sepgsql — SELinux-, label-based mandatory access control (MAC) security module](contrib/sepgsql.md)

    [F.41. spi — Server Programming Interface features/examples](contrib/contrib-spi.md)

    [F.42. sslinfo — obtain client SSL information](contrib/sslinfo.md)

    [F.43. tablefunc — functions that return tables (`crosstab` and others)](contrib/tablefunc.md)

    [F.44. tcn — a trigger function to notify listeners of changes to table content](contrib/tcn.md)

    [F.45. test_decoding — SQL-based test/example module for WAL logical decoding](contrib/test-decoding.md)

    [F.46. tsm_system_rows — the `SYSTEM_ROWS` sampling method for `TABLESAMPLE`](contrib/tsm-system-rows.md)

    [F.47. tsm_system_time — the `SYSTEM_TIME` sampling method for `TABLESAMPLE`](contrib/tsm-system-time.md)

    [F.48. unaccent — a text search dictionary which removes diacritics](contrib/unaccent.md)

    [F.49. uuid-ossp — a UUID generator](contrib/uuid-ossp.md)

    [F.50. xml2 — XPath querying and XSLT functionality](contrib/xml2.md)

[G. Additional Supplied Programs](contrib-prog/README.md)
:   [G.1. Client Applications](contrib-prog/contrib-prog-client.md)

    [G.2. Server Applications](contrib-prog/contrib-prog-server.md)

[H. External Projects](external-projects/README.md)
:   [H.1. Client Interfaces](external-projects/external-interfaces.md)

    [H.2. Administration Tools](external-projects/external-admin-tools.md)

    [H.3. Procedural Languages](external-projects/external-pl.md)

    [H.4. Extensions](external-projects/external-extensions.md)

[I. The Source Code Repository](sourcerepo/README.md)
:   [I.1. Getting the Source via Git](sourcerepo/git.md)

[J. Documentation](docguide/README.md)
:   [J.1. DocBook](docguide/docguide-docbook.md)

    [J.2. Tool Sets](docguide/docguide-toolsets.md)

    [J.3. Building the Documentation with Make](docguide/docguide-build.md)

    [J.4. Building the Documentation with Meson](docguide/docguide-build-meson.md)

    [J.5. Documentation Authoring](docguide/docguide-authoring.md)

    [J.6. Style Guide](docguide/docguide-style.md)

[K. PostgreSQL Limits](limits/README.md)

[L. Acronyms](acronyms/README.md)

[M. Glossary](glossary/README.md)

[N. Color Support](color/README.md)
:   [N.1. When Color is Used](color/color-when.md)

    [N.2. Configuring the Colors](color/color-which.md)

[O. Obsolete or Renamed Features](appendix-obsolete/README.md)
:   [O.1. `recovery.conf` file merged into `postgresql.conf`](appendix-obsolete/recovery-config.md)

    [O.2. Default Roles Renamed to Predefined Roles](appendix-obsolete/default-roles.md)

    [O.3. `pg_xlogdump` renamed to `pg_waldump`](appendix-obsolete/pgxlogdump.md)

    [O.4. `pg_resetxlog` renamed to `pg_resetwal`](appendix-obsolete/app-pgresetxlog.md)

    [O.5. `pg_receivexlog` renamed to `pg_receivewal`](appendix-obsolete/app-pgreceivexlog.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/appendixes.html)（英文原文，待翻譯）
