## DESCRIBE

DESCRIBE — obtain information about a prepared statement or result set

## Synopsis

```

DESCRIBE [ OUTPUT ] prepared_name USING [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO sqlda_name
```

<a id="id-1.7.5.20.8.3"></a>

## Description

`DESCRIBE` retrieves metadata information about
the result columns contained in a prepared statement, without
actually fetching a row.

<a id="id-1.7.5.20.8.4"></a>

## Parameters

<a id="ECPG-SQL-DESCRIBE-PREPARED-NAME"></a>

*`prepared_name`* [#](#ECPG-SQL-DESCRIBE-PREPARED-NAME)
:   The name of a prepared statement. This can be an SQL
    identifier or a host variable.
<a id="ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME)
:   A descriptor name. It is case sensitive. It can be an SQL
    identifier or a host variable.
<a id="ECPG-SQL-DESCRIBE-SQLDA-NAME"></a>

*`sqlda_name`* [#](#ECPG-SQL-DESCRIBE-SQLDA-NAME)
:   The name of an SQLDA variable.

<a id="id-1.7.5.20.8.5"></a>

## Examples

```

EXEC SQL ALLOCATE DESCRIPTOR mydesc;
EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :charvar = NAME;
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.8.6"></a>

## Compatibility

`DESCRIBE` is specified in the SQL standard.

<a id="id-1.7.5.20.8.7"></a>

## See Also

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-describe.html)（英文原文，待翻譯）
