<a id="id-1.11.7.21.19.1"></a>

## dblink_get_notify

dblink_get_notify — retrieve async notifications on a connection

## Synopsis

```

dblink_get_notify() returns setof (notify_name text, be_pid int, extra text)
dblink_get_notify(text connname) returns setof (notify_name text, be_pid int, extra text)
```

<a id="id-1.11.7.21.19.5"></a>

## Description

`dblink_get_notify` retrieves notifications on either
the unnamed connection, or on a named connection if specified.
To receive notifications via dblink, `LISTEN` must
first be issued, using `dblink_exec`.
For details see [LISTEN](../../reference/sql-commands/sql-listen.md) and [NOTIFY](../../reference/sql-commands/sql-notify.md).

<a id="id-1.11.7.21.19.6"></a>

## Arguments

*`connname`*
:   The name of a named connection to get notifications on.

<a id="id-1.11.7.21.19.7"></a>

## Return Value

Returns `setof (notify_name text, be_pid int, extra text)`, or an empty set if none.

<a id="id-1.11.7.21.19.8"></a>

## Examples

```

SELECT dblink_exec('LISTEN virtual');
 dblink_exec
-------------
 LISTEN
(1 row)

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
(0 rows)

NOTIFY virtual;
NOTIFY

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
 virtual     |   1229 |
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-notify.html)（英文原文，待翻譯）
