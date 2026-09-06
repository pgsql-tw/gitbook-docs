<a id="id-1.11.7.21.9.1"></a>

## dblink_disconnect

dblink_disconnect — closes a persistent connection to a remote database

## Synopsis

```

dblink_disconnect() returns text
dblink_disconnect(text connname) returns text
```

<a id="id-1.11.7.21.9.5"></a>

## Description

`dblink_disconnect()` closes a connection previously opened
by `dblink_connect()`. The form with no arguments closes
an unnamed connection.

<a id="id-1.11.7.21.9.6"></a>

## Arguments

*`connname`*
:   The name of a named connection to be closed.

<a id="id-1.11.7.21.9.7"></a>

## Return Value

Returns status, which is always `OK` (since any error
causes the function to throw an error instead of returning).

<a id="id-1.11.7.21.9.8"></a>

## Examples

```

SELECT dblink_disconnect();
 dblink_disconnect
-------------------
 OK
(1 row)

SELECT dblink_disconnect('myconn');
 dblink_disconnect
-------------------
 OK
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-disconnect.html)（英文原文，待翻譯）
