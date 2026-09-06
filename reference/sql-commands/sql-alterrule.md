<a id="id-1.9.3.28.1"></a>

## ALTER RULE

ALTER RULE — change the definition of a rule

## Synopsis

```

ALTER RULE name ON table_name RENAME TO new_name
```

<a id="id-1.9.3.28.5"></a>

## Description

`ALTER RULE` changes properties of an existing
rule. Currently, the only available action is to change the rule's name.

To use `ALTER RULE`, you must own the table or view that
the rule applies to.

<a id="id-1.9.3.28.6"></a>

## Parameters

*`name`*
:   The name of an existing rule to alter.

*`table_name`*
:   The name (optionally schema-qualified) of the table or view that the
    rule applies to.

*`new_name`*
:   The new name for the rule.

<a id="id-1.9.3.28.7"></a>

## Examples

To rename an existing rule:

```

ALTER RULE notify_all ON emp RENAME TO notify_me;
```

<a id="id-1.9.3.28.8"></a>

## Compatibility

`ALTER RULE` is a
PostgreSQL language extension, as is the
entire query rewrite system.

<a id="id-1.9.3.28.9"></a>

## See Also

[CREATE RULE](sql-createrule.md), [DROP RULE](sql-droprule.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterrule.html)（英文原文，待翻譯）
