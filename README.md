# PostgreSQL 18.6 Documentation

### The PostgreSQL Global Development Group

Copyright © 1996–2026 The PostgreSQL Global Development Group

[Legal Notice](https://www.postgresql.org/docs/18/legalnotice.html)

---

**Table of Contents**

[Preface](preface/README.md)
:   [1. What Is PostgreSQL?](preface/intro-whatis.md)

    [2. A Brief History of PostgreSQL](preface/history.md)

    [3. Conventions](preface/notation.md)

    [4. Further Information](preface/resources.md)

    [5. Bug Reporting Guidelines](preface/bug-reporting.md)

[I. Tutorial](tutorial/README.md)
:   [1. Getting Started](tutorial/tutorial-start/README.md)

    [2. The SQL Language](tutorial/tutorial-sql/README.md)

    [3. Advanced Features](tutorial/tutorial-advanced/README.md)

[II. The SQL Language](the-sql-language/README.md)
:   [4. SQL Syntax](the-sql-language/sql-syntax/README.md)

    [5. Data Definition](the-sql-language/ddl/README.md)

    [6. Data Manipulation](the-sql-language/dml/README.md)

    [7. Queries](the-sql-language/queries/README.md)

    [8. Data Types](the-sql-language/datatype/README.md)

    [9. Functions and Operators](the-sql-language/functions/README.md)

    [10. Type Conversion](the-sql-language/typeconv/README.md)

    [11. Indexes](the-sql-language/indexes/README.md)

    [12. Full Text Search](the-sql-language/textsearch/README.md)

    [13. Concurrency Control](the-sql-language/mvcc/README.md)

    [14. Performance Tips](the-sql-language/performance-tips/README.md)

    [15. Parallel Query](the-sql-language/parallel-query/README.md)

[III. Server Administration](server-administration/README.md)
:   [16. Installation from Binaries](server-administration/install-binaries/README.md)

    [17. Installation from Source Code](server-administration/installation/README.md)

    [18. Server Setup and Operation](server-administration/runtime/README.md)

    [19. Server Configuration](server-administration/runtime-config/README.md)

    [20. Client Authentication](server-administration/client-authentication/README.md)

    [21. Database Roles](server-administration/user-manag/README.md)

    [22. Managing Databases](server-administration/managing-databases/README.md)

    [23. Localization](server-administration/charset/README.md)

    [24. Routine Database Maintenance Tasks](server-administration/maintenance/README.md)

    [25. Backup and Restore](server-administration/backup/README.md)

    [26. High Availability, Load Balancing, and Replication](server-administration/high-availability/README.md)

    [27. Monitoring Database Activity](server-administration/monitoring/README.md)

    [28. Reliability and the Write-Ahead Log](server-administration/wal/README.md)

    [29. Logical Replication](server-administration/logical-replication/README.md)

    [30. Just-in-Time Compilation (JIT)](server-administration/jit/README.md)

    [31. Regression Tests](server-administration/regress/README.md)

[IV. Client Interfaces](client-interfaces/README.md)
:   [32. libpq — C Library](client-interfaces/libpq/README.md)

    [33. Large Objects](client-interfaces/largeobjects/README.md)

    [34. ECPG — Embedded SQL in C](client-interfaces/ecpg/README.md)

    [35. The Information Schema](client-interfaces/information-schema/README.md)

[V. Server Programming](server-programming/README.md)
:   [36. Extending SQL](server-programming/extend/README.md)

    [37. Triggers](server-programming/triggers/README.md)

    [38. Event Triggers](server-programming/event-triggers/README.md)

    [39. The Rule System](server-programming/rules/README.md)

    [40. Procedural Languages](server-programming/xplang/README.md)

    [41. PL/pgSQL — SQL Procedural Language](server-programming/plpgsql/README.md)

    [42. PL/Tcl — Tcl Procedural Language](server-programming/pltcl/README.md)

    [43. PL/Perl — Perl Procedural Language](server-programming/plperl/README.md)

    [44. PL/Python — Python Procedural Language](server-programming/plpython/README.md)

    [45. Server Programming Interface](server-programming/spi/README.md)

    [46. Background Worker Processes](server-programming/bgworker/README.md)

    [47. Logical Decoding](server-programming/logicaldecoding/README.md)

    [48. Replication Progress Tracking](server-programming/replication-origins/README.md)

    [49. Archive Modules](server-programming/archive-modules/README.md)

    [50. OAuth Validator Modules](server-programming/oauth-validators/README.md)

[VI. Reference](reference/README.md)
:   [I. SQL Commands](reference/sql-commands/README.md)

    [II. PostgreSQL Client Applications](reference/reference-client/README.md)

    [III. PostgreSQL Server Applications](reference/reference-server/README.md)

[VII. Internals](internals/README.md)
:   [51. Overview of PostgreSQL Internals](internals/overview/README.md)

    [52. System Catalogs](internals/catalogs/README.md)

    [53. System Views](internals/views/README.md)

    [54. Frontend/Backend Protocol](internals/protocol/README.md)

    [55. PostgreSQL Coding Conventions](internals/source/README.md)

    [56. Native Language Support](internals/nls/README.md)

    [57. Writing a Procedural Language Handler](internals/plhandler/README.md)

    [58. Writing a Foreign Data Wrapper](internals/fdwhandler/README.md)

    [59. Writing a Table Sampling Method](internals/tablesample-method/README.md)

    [60. Writing a Custom Scan Provider](internals/custom-scan/README.md)

    [61. Genetic Query Optimizer](internals/geqo/README.md)

    [62. Table Access Method Interface Definition](internals/tableam/README.md)

    [63. Index Access Method Interface Definition](internals/indexam/README.md)

    [64. Write Ahead Logging for Extensions](internals/wal-for-extensions/README.md)

    [65. Built-in Index Access Methods](internals/indextypes/README.md)

    [66. Database Physical Storage](internals/storage/README.md)

    [67. Transaction Processing](internals/transactions/README.md)

    [68. System Catalog Declarations and Initial Contents](internals/bki/README.md)

    [69. How the Planner Uses Statistics](internals/planner-stats-details/README.md)

    [70. Backup Manifest Format](internals/backup-manifest-format/README.md)

[VIII. Appendixes](appendixes/README.md)
:   [A. PostgreSQL Error Codes](appendixes/errcodes-appendix/README.md)

    [B. Date/Time Support](appendixes/datetime-appendix/README.md)

    [C. SQL Key Words](appendixes/sql-keywords-appendix/README.md)

    [D. SQL Conformance](appendixes/features/README.md)

    [E. Release Notes](appendixes/release/README.md)

    [F. Additional Supplied Modules and Extensions](appendixes/contrib/README.md)

    [G. Additional Supplied Programs](appendixes/contrib-prog/README.md)

    [H. External Projects](appendixes/external-projects/README.md)

    [I. The Source Code Repository](appendixes/sourcerepo/README.md)

    [J. Documentation](appendixes/docguide/README.md)

    [K. PostgreSQL Limits](appendixes/limits/README.md)

    [L. Acronyms](appendixes/acronyms/README.md)

    [M. Glossary](appendixes/glossary/README.md)

    [N. Color Support](appendixes/color/README.md)

    [O. Obsolete or Renamed Features](appendixes/appendix-obsolete/README.md)

[Bibliography](bibliography.md)

[Index](https://www.postgresql.org/docs/18/bookindex.html)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/index.html)（英文原文，待翻譯）
