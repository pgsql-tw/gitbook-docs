<a id="id-1.9.3.17.1"></a>

## ALTER LANGUAGE

ALTER LANGUAGE — change the definition of a procedural language

## Synopsis

```

ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.17.5"></a>

## Description

`ALTER LANGUAGE` changes the definition of a
procedural language. The only functionality is to rename the language or
assign a new owner. You must be superuser or owner of the language to
use `ALTER LANGUAGE`.

<a id="id-1.9.3.17.6"></a>

## Parameters

*`name`*
:   Name of a language

*`new_name`*
:   The new name of the language

*`new_owner`*
:   The new owner of the language

<a id="id-1.9.3.17.7"></a>

## Compatibility

There is no `ALTER LANGUAGE` statement in the SQL
standard.

<a id="id-1.9.3.17.8"></a>

## See Also

[CREATE LANGUAGE](sql-createlanguage.md), [DROP LANGUAGE](sql-droplanguage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterlanguage.html)（英文原文，待翻譯）
