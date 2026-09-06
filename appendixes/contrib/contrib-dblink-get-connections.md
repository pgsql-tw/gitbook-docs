<a id="id-1.11.7.21.15.1"></a>

## dblink_get_connections

dblink_get_connections — returns the names of all open named dblink connections

## Synopsis

```

dblink_get_connections() returns text[]
```

<a id="id-1.11.7.21.15.5"></a>

## Description

`dblink_get_connections` returns an array of the names
of all open named `dblink` connections.

<a id="id-1.11.7.21.15.6"></a>

## Return Value

Returns a text array of connection names, or NULL if none.

<a id="id-1.11.7.21.15.7"></a>

## Examples

```

SELECT dblink_get_connections();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-connections.html)（英文原文，待翻譯）
