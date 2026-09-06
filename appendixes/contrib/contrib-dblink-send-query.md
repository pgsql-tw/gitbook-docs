<a id="id-1.11.7.21.17.1"></a>

## dblink_send_query

dblink_send_query — sends an async query to a remote database

## Synopsis

```

dblink_send_query(text connname, text sql) returns int
```

<a id="id-1.11.7.21.17.5"></a>

## Description

`dblink_send_query` sends a query to be executed
asynchronously, that is, without immediately waiting for the result.
There must not be an async query already in progress on the
connection.

After successfully dispatching an async query, completion status
can be checked with `dblink_is_busy`, and the results
are ultimately collected with `dblink_get_result`.
It is also possible to attempt to cancel an active async query
using `dblink_cancel_query`.

<a id="id-1.11.7.21.17.6"></a>

## Arguments

*`connname`*
:   Name of the connection to use.

*`sql`*
:   The SQL statement that you wish to execute in the remote database,
    for example `select * from pg_class`.

<a id="id-1.11.7.21.17.7"></a>

## Return Value

Returns 1 if the query was successfully dispatched, 0 otherwise.

<a id="id-1.11.7.21.17.8"></a>

## Examples

```

SELECT dblink_send_query('dtest1', 'SELECT * FROM foo WHERE f1 < 3');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-send-query.html)（英文原文，待翻譯）
