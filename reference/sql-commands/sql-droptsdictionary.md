<a id="id-1.9.3.137.1"></a>

## DROP TEXT SEARCH DICTIONARY

DROP TEXT SEARCH DICTIONARY — remove a text search dictionary

## Synopsis

```

DROP TEXT SEARCH DICTIONARY [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.137.5"></a>

## Description

`DROP TEXT SEARCH DICTIONARY` drops an existing text
search dictionary. To execute this command you must be the owner of the
dictionary.

<a id="id-1.9.3.137.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the text search dictionary does not exist.
    A notice is issued in this case.

*`name`*
:   The name (optionally schema-qualified) of an existing text search
    dictionary.

`CASCADE`
:   Automatically drop objects that depend on the text search dictionary,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the text search dictionary if any objects depend on it.
    This is the default.

<a id="id-1.9.3.137.7"></a>

## Examples

Remove the text search dictionary `english`:

```

DROP TEXT SEARCH DICTIONARY english;
```

This command will not succeed if there are any existing text search
configurations that use the dictionary. Add `CASCADE` to
drop such configurations along with the dictionary.

<a id="id-1.9.3.137.8"></a>

## Compatibility

There is no `DROP TEXT SEARCH DICTIONARY` statement in the
SQL standard.

<a id="id-1.9.3.137.9"></a>

## See Also

[ALTER TEXT SEARCH DICTIONARY](sql-altertsdictionary.md), [CREATE TEXT SEARCH DICTIONARY](sql-createtsdictionary.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptsdictionary.html)（英文原文，待翻譯）
