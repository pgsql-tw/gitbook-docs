<a id="id-1.9.3.135.1"></a>

## DROP TABLESPACE

DROP TABLESPACE — remove a tablespace

## Synopsis

```

DROP TABLESPACE [ IF EXISTS ] name
```

<a id="id-1.9.3.135.5"></a>

## Description

`DROP TABLESPACE` removes a tablespace from the system.

A tablespace can only be dropped by its owner or a superuser.
The tablespace must be empty of all database objects before it can be
dropped. It is possible that objects in other databases might still reside
in the tablespace even if no objects in the current database are using
the tablespace. Also, if the tablespace is listed in the [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES) setting of any active session, the
`DROP` might fail due to temporary files residing in the
tablespace.

<a id="id-1.9.3.135.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the tablespace does not exist. A notice is issued
    in this case.

*`name`*
:   The name of a tablespace.

<a id="id-1.9.3.135.7"></a>

## Notes

`DROP TABLESPACE` cannot be executed inside a transaction block.

<a id="id-1.9.3.135.8"></a>

## Examples

To remove tablespace `mystuff` from the system:

```

DROP TABLESPACE mystuff;
```

<a id="id-1.9.3.135.9"></a>

## Compatibility

`DROP TABLESPACE` is a PostgreSQL
extension.

<a id="id-1.9.3.135.10"></a>

## See Also

[CREATE TABLESPACE](sql-createtablespace.md), [ALTER TABLESPACE](sql-altertablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptablespace.html)（英文原文，待翻譯）
