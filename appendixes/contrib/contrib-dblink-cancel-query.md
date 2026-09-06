<a id="id-1.11.7.21.21.1"></a>

## dblink_cancel_query

dblink_cancel_query — cancels any active query on the named connection

## Synopsis

```

dblink_cancel_query(text connname) returns text
```

<a id="id-1.11.7.21.21.5"></a>

## Description

`dblink_cancel_query` attempts to cancel any query that
is in progress on the named connection. Note that this is not
certain to succeed (since, for example, the remote query might
already have finished). A cancel request simply improves the
odds that the query will fail soon. You must still complete the
normal query protocol, for example by calling
`dblink_get_result`.

<a id="id-1.11.7.21.21.6"></a>

## Arguments

*`connname`*
:   Name of the connection to use.

<a id="id-1.11.7.21.21.7"></a>

## Return Value

Returns `OK` if the cancel request has been sent, or
the text of an error message on failure.

<a id="id-1.11.7.21.21.8"></a>

## Examples

```

SELECT dblink_cancel_query('dtest1');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-cancel-query.html)（英文原文，待翻譯）
