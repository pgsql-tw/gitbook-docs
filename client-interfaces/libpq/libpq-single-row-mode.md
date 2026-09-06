## 32.6. Retrieving Query Results in Chunks [#](#LIBPQ-SINGLE-ROW-MODE)

<a id="id-1.7.3.13.2"></a><a id="id-1.7.3.13.3"></a>

Ordinarily, libpq collects an SQL command's
entire result and returns it to the application as a single
`PGresult`. This can be unworkable for commands
that return a large number of rows. For such cases, applications can use
[`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) and [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) in
*single-row mode* or *chunked
mode*. In these modes, result row(s) are returned to the
application as they are received from the server, one at a time for
single-row mode or in groups for chunked mode.

To enter one of these modes, call [`PQsetSingleRowMode`](libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE)
or [`PQsetChunkedRowsMode`](libpq-single-row-mode.md#LIBPQ-PQSETCHUNKEDROWSMODE)
immediately after a successful call of [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY)
(or a sibling function). This mode selection is effective only for the
currently executing query. Then call [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)
repeatedly, until it returns null, as documented in [Section 32.4](libpq-async.md). If the query returns any rows, they are returned
as one or more `PGresult` objects, which look like
normal query results except for having status code
`PGRES_SINGLE_TUPLE` for single-row mode or
`PGRES_TUPLES_CHUNK` for chunked mode, instead of
`PGRES_TUPLES_OK`. There is exactly one result row in
each `PGRES_SINGLE_TUPLE` object, while
a `PGRES_TUPLES_CHUNK` object contains at least one
row but not more than the specified number of rows per chunk.
After the last row, or immediately if
the query returns zero rows, a zero-row object with status
`PGRES_TUPLES_OK` is returned; this is the signal that no
more rows will arrive. (But note that it is still necessary to continue
calling [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) until it returns null.) All of
these `PGresult` objects will contain the same row
description data (column names, types, etc.) that an ordinary
`PGresult` object for the query would have.
Each object should be freed with [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) as usual.

When using pipeline mode, single-row or chunked mode needs to be
activated for each query in the pipeline before retrieving results for
that query with `PQgetResult`.
See [Section 32.5](libpq-pipeline-mode.md) for more information.

<a id="LIBPQ-PQSETSINGLEROWMODE"></a>

`PQsetSingleRowMode`<a id="id-1.7.3.13.7.1.1.1.2"></a> [#](#LIBPQ-PQSETSINGLEROWMODE)
:   Select single-row mode for the currently-executing query.

    ```

    int PQsetSingleRowMode(PGconn *conn);
    ```

    This function can only be called immediately after
    [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) or one of its sibling functions,
    before any other operation on the connection such as
    [`PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT) or
    [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT). If called at the correct time,
    the function activates single-row mode for the current query and
    returns 1. Otherwise the mode stays unchanged and the function
    returns 0. In any case, the mode reverts to normal after
    completion of the current query.
<a id="LIBPQ-PQSETCHUNKEDROWSMODE"></a>

`PQsetChunkedRowsMode`<a id="id-1.7.3.13.7.1.2.1.2"></a> [#](#LIBPQ-PQSETCHUNKEDROWSMODE)
:   Select chunked mode for the currently-executing query.

    ```

    int PQsetChunkedRowsMode(PGconn *conn, int chunkSize);
    ```

    This function is similar to
    [`PQsetSingleRowMode`](libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE), except that it
    specifies retrieval of up to *`chunkSize`* rows
    per `PGresult`, not necessarily just one row.
    This function can only be called immediately after
    [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) or one of its sibling functions,
    before any other operation on the connection such as
    [`PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT) or
    [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT). If called at the correct time,
    the function activates chunked mode for the current query and
    returns 1. Otherwise the mode stays unchanged and the function
    returns 0. In any case, the mode reverts to normal after
    completion of the current query.

### Caution

While processing a query, the server may return some rows and then
encounter an error, causing the query to be aborted. Ordinarily,
libpq discards any such rows and reports only the
error. But in single-row or chunked mode, some rows may have already
been returned to the application. Hence, the application will see some
`PGRES_SINGLE_TUPLE` or `PGRES_TUPLES_CHUNK`
`PGresult`
objects followed by a `PGRES_FATAL_ERROR` object. For
proper transactional behavior, the application must be designed to
discard or undo whatever has been done with the previously-processed
rows, if the query ultimately fails.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-single-row-mode.html)（英文原文，待翻譯）
