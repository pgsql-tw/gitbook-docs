<a id="id-1.11.7.21.12.1"></a>

## dblink_open

dblink_open — opens a cursor in a remote database

## Synopsis

```

dblink_open(text cursorname, text sql [, bool fail_on_error]) returns text
dblink_open(text connname, text cursorname, text sql [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.12.5"></a>

## Description

`dblink_open()` opens a cursor in a remote database.
The cursor can subsequently be manipulated with
`dblink_fetch()` and `dblink_close()`.

<a id="id-1.11.7.21.12.6"></a>

## Arguments

*`connname`*
:   Name of the connection to use; omit this parameter to use the
    unnamed connection.

*`cursorname`*
:   The name to assign to this cursor.

*`sql`*
:   The `SELECT` statement that you wish to execute in the remote
    database, for example `select * from pg_class`.

*`fail_on_error`*
:   If true (the default when omitted) then an error thrown on the
    remote side of the connection causes an error to also be thrown
    locally. If false, the remote error is locally reported as a NOTICE,
    and the function's return value is set to `ERROR`.

<a id="id-1.11.7.21.12.7"></a>

## Return Value

Returns status, either `OK` or `ERROR`.

<a id="id-1.11.7.21.12.8"></a>

## Notes

Since a cursor can only persist within a transaction,
`dblink_open` starts an explicit transaction block
(`BEGIN`) on the remote side, if the remote side was
not already within a transaction. This transaction will be
closed again when the matching `dblink_close` is
executed. Note that if
you use `dblink_exec` to change data between
`dblink_open` and `dblink_close`,
and then an error occurs or you use `dblink_disconnect` before
`dblink_close`, your change *will be
lost* because the transaction will be aborted.

<a id="id-1.11.7.21.12.9"></a>

## Examples

```

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc');
 dblink_open
-------------
 OK
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-open.html)（英文原文，待翻譯）
