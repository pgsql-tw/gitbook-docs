<a id="id-1.9.3.117.1"></a>

## DROP LANGUAGE

DROP LANGUAGE — remove a procedural language

## Synopsis

```

DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.117.5"></a>

## Description

`DROP LANGUAGE` removes the definition of a
previously registered procedural language. You must be a superuser
or the owner of the language to use `DROP LANGUAGE`.

### Note

As of PostgreSQL 9.1, most procedural
languages have been made into “extensions”, and should
therefore be removed with [`DROP EXTENSION`](sql-dropextension.md)
not `DROP LANGUAGE`.

<a id="id-1.9.3.117.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the language does not exist. A notice is issued
    in this case.

*`name`*
:   The name of an existing procedural language.

`CASCADE`
:   Automatically drop objects that depend on the language (such as
    functions in the language),
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the language if any objects depend on it. This
    is the default.

<a id="id-1.9.3.117.7"></a>

## Examples

This command removes the procedural language
`plsample`:

```

DROP LANGUAGE plsample;
```

<a id="id-1.9.3.117.8"></a>

## Compatibility

There is no `DROP LANGUAGE` statement in the SQL
standard.

<a id="id-1.9.3.117.9"></a>

## See Also

[ALTER LANGUAGE](sql-alterlanguage.md), [CREATE LANGUAGE](sql-createlanguage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droplanguage.html)（英文原文，待翻譯）
