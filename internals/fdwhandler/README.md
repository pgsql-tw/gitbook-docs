## Chapter 58. Writing a Foreign Data Wrapper

**Table of Contents**

[58.1. Foreign Data Wrapper Functions](fdw-functions.md)

[58.2. Foreign Data Wrapper Callback Routines](fdw-callbacks.md)
:   [58.2.1. FDW Routines for Scanning Foreign Tables](fdw-callbacks.md#FDW-CALLBACKS-SCAN)

    [58.2.2. FDW Routines for Scanning Foreign Joins](fdw-callbacks.md#FDW-CALLBACKS-JOIN-SCAN)

    [58.2.3. FDW Routines for Planning Post-Scan/Join Processing](fdw-callbacks.md#FDW-CALLBACKS-UPPER-PLANNING)

    [58.2.4. FDW Routines for Updating Foreign Tables](fdw-callbacks.md#FDW-CALLBACKS-UPDATE)

    [58.2.5. FDW Routines for `TRUNCATE`](fdw-callbacks.md#FDW-CALLBACKS-TRUNCATE)

    [58.2.6. FDW Routines for Row Locking](fdw-callbacks.md#FDW-CALLBACKS-ROW-LOCKING)

    [58.2.7. FDW Routines for `EXPLAIN`](fdw-callbacks.md#FDW-CALLBACKS-EXPLAIN)

    [58.2.8. FDW Routines for `ANALYZE`](fdw-callbacks.md#FDW-CALLBACKS-ANALYZE)

    [58.2.9. FDW Routines for `IMPORT FOREIGN SCHEMA`](fdw-callbacks.md#FDW-CALLBACKS-IMPORT)

    [58.2.10. FDW Routines for Parallel Execution](fdw-callbacks.md#FDW-CALLBACKS-PARALLEL)

    [58.2.11. FDW Routines for Asynchronous Execution](fdw-callbacks.md#FDW-CALLBACKS-ASYNC)

    [58.2.12. FDW Routines for Reparameterization of Paths](fdw-callbacks.md#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

[58.3. Foreign Data Wrapper Helper Functions](fdw-helpers.md)

[58.4. Foreign Data Wrapper Query Planning](fdw-planning.md)

[58.5. Row Locking in Foreign Data Wrappers](fdw-row-locking.md)

<a id="id-1.10.10.2"></a>

All operations on a foreign table are handled through its foreign data
wrapper, which consists of a set of functions that the core server
calls. The foreign data wrapper is responsible for fetching
data from the remote data source and returning it to the
PostgreSQL executor. If updating foreign
tables is to be supported, the wrapper must handle that, too.
This chapter outlines how to write a new foreign data wrapper.

The foreign data wrappers included in the standard distribution are good
references when trying to write your own. Look into the
`contrib` subdirectory of the source tree.
The [CREATE FOREIGN DATA WRAPPER](../../reference/sql-commands/sql-createforeigndatawrapper.md) reference page also has
some useful details.

### Note

The SQL standard specifies an interface for writing foreign data wrappers.
However, PostgreSQL does not implement that API, because the effort to
accommodate it into PostgreSQL would be large, and the standard API hasn't
gained wide adoption anyway.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdwhandler.html)（英文原文，待翻譯）
