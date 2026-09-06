<a id="id-1.9.3.128.1"></a>

## DROP RULE

DROP RULE — remove a rewrite rule

## Synopsis

```

DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.128.5"></a>

## Description

`DROP RULE` drops a rewrite rule.

<a id="id-1.9.3.128.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the rule does not exist. A notice is issued
    in this case.

*`name`*
:   The name of the rule to drop.

*`table_name`*
:   The name (optionally schema-qualified) of the table or view that
    the rule applies to.

`CASCADE`
:   Automatically drop objects that depend on the rule,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the rule if any objects depend on it. This is
    the default.

<a id="id-1.9.3.128.7"></a>

## Examples

To drop the rewrite rule `newrule`:

```

DROP RULE newrule ON mytable;
```

<a id="id-1.9.3.128.8"></a>

## Compatibility

`DROP RULE` is a
PostgreSQL language extension, as is the
entire query rewrite system.

<a id="id-1.9.3.128.9"></a>

## See Also

[CREATE RULE](sql-createrule.md), [ALTER RULE](sql-alterrule.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droprule.html)（英文原文，待翻譯）
