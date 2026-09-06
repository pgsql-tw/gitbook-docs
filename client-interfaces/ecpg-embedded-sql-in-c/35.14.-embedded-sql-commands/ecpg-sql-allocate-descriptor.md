<a id="ECPG-SQL-ALLOCATE-DESCRIPTOR"></a>

# ALLOCATE DESCRIPTOR

ALLOCATE DESCRIPTOR — allocate an SQL descriptor area

## Synopsis

```

ALLOCATE DESCRIPTOR name
```

<a id="id-1.7.5.20.3.3"></a>

## Description

`ALLOCATE DESCRIPTOR` allocates a new named SQL descriptor area, which can be used to exchange data between the PostgreSQL server and the host program.

Descriptor areas should be freed after use using the `DEALLOCATE DESCRIPTOR` command.

<a id="id-1.7.5.20.3.4"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

A name of SQL descriptor, case sensitive. This can be an SQL identifier or a host variable.

<a id="id-1.7.5.20.3.5"></a>

## Examples

```

EXEC SQL ALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.3.6"></a>

## Compatibility

`ALLOCATE DESCRIPTOR` is specified in the SQL standard.

<a id="id-1.7.5.20.3.7"></a>

## See Also

[DEALLOCATE DESCRIPTOR](ecpg-sql-deallocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md), [SET DESCRIPTOR](ecpg-sql-set-descriptor.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-allocate-descriptor.html)（英文原文，待翻譯）
