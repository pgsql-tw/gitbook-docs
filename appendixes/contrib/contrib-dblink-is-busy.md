<a id="id-1.11.7.21.18.1"></a>

## dblink_is_busy

dblink_is_busy — checks if connection is busy with an async query

## Synopsis

```

dblink_is_busy(text connname) returns int
```

<a id="id-1.11.7.21.18.5"></a>

## Description

`dblink_is_busy` tests whether an async query is in progress.

<a id="id-1.11.7.21.18.6"></a>

## Arguments

*`connname`*
:   Name of the connection to check.

<a id="id-1.11.7.21.18.7"></a>

## Return Value

Returns 1 if connection is busy, 0 if it is not busy.
If this function returns 0, it is guaranteed that
`dblink_get_result` will not block.

<a id="id-1.11.7.21.18.8"></a>

## Examples

```

SELECT dblink_is_busy('dtest1');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-is-busy.html)（英文原文，待翻譯）
