# ALTER RULE

ALTER RULE — change the definition of a rule

### Synopsis

```text
ALTER RULE name ON table_name RENAME TO new_name
```

### Description

`ALTER RULE` changes properties of an existing rule. Currently, the only available action is to change the rule's name.

To use `ALTER RULE`, you must own the table or view that the rule applies to.

### Parameters

_`name`_

The name of an existing rule to alter._`table_name`_

The name \(optionally schema-qualified\) of the table or view that the rule applies to._`new_name`_

The new name for the rule.

### Examples

To rename an existing rule:

```text
ALTER RULE notify_all ON emp RENAME TO notify_me;
```

### Compatibility

`ALTER RULE` is a PostgreSQL language extension, as is the entire query rewrite system.

### See Also

[CREATE RULE](https://www.postgresql.org/docs/10/static/sql-createrule.html), [DROP RULE](https://www.postgresql.org/docs/10/static/sql-droprule.html)

