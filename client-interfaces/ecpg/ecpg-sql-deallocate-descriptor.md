## DEALLOCATE DESCRIPTOR

DEALLOCATE DESCRIPTOR — deallocate an SQL descriptor area

## Synopsis

```

DEALLOCATE DESCRIPTOR name
```

<a id="id-1.7.5.20.5.3"></a>

## Description

`DEALLOCATE DESCRIPTOR` deallocates a named SQL
descriptor area.

<a id="id-1.7.5.20.5.4"></a>

## Parameters

<a id="ECPG-SQL-DEALLOCATE-DESCRIPTOR-NAME"></a>

*`name`* [#](#ECPG-SQL-DEALLOCATE-DESCRIPTOR-NAME)
:   The name of the descriptor which is going to be deallocated.
    It is case sensitive. This can be an SQL identifier or a host
    variable.

<a id="id-1.7.5.20.5.5"></a>

## Examples

```

EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.5.6"></a>

## Compatibility

`DEALLOCATE DESCRIPTOR` is specified in the SQL
standard.

<a id="id-1.7.5.20.5.7"></a>

## See Also

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md), [SET DESCRIPTOR](ecpg-sql-set-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-deallocate-descriptor.html)（英文原文，待翻譯）
