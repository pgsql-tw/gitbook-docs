<a id="id-1.11.7.21.14.1"></a>

## dblink_close

dblink_close — closes a cursor in a remote database

## Synopsis

```

dblink_close(text cursorname [, bool fail_on_error]) returns text
dblink_close(text connname, text cursorname [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.14.5"></a>

## Description

`dblink_close` closes a cursor previously opened with
`dblink_open`.

<a id="id-1.11.7.21.14.6"></a>

## Arguments

*`connname`*
:   Name of the connection to use; omit this parameter to use the
    unnamed connection.

*`cursorname`*
:   The name of the cursor to close.

*`fail_on_error`*
:   If true (the default when omitted) then an error thrown on the
    remote side of the connection causes an error to also be thrown
    locally. If false, the remote error is locally reported as a NOTICE,
    and the function's return value is set to `ERROR`.

<a id="id-1.11.7.21.14.7"></a>

## Return Value

Returns status, either `OK` or `ERROR`.

<a id="id-1.11.7.21.14.8"></a>

## Notes

If `dblink_open` started an explicit transaction block,
and this is the last remaining open cursor in this connection,
`dblink_close` will issue the matching `COMMIT`.

<a id="id-1.11.7.21.14.9"></a>

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

SELECT dblink_close('foo');
 dblink_close
--------------
 OK
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-close.html)（英文原文，待翻譯）
