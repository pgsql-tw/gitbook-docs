# DROP RULE

DROP RULE — remove a rewrite rule

### Synopsis

```text
DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

### Description

`DROP RULE` drops a rewrite rule.

### Parameters

`IF EXISTS`

Do not throw an error if the rule does not exist. A notice is issued in this case.

_`name`_

The name of the rule to drop.

_`table_name`_

The name \(optionally schema-qualified\) of the table or view that the rule applies to.

`CASCADE`

Automatically drop objects that depend on the rule, and in turn all objects that depend on those objects \(see [Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the rule if any objects depend on it. This is the default.

### Examples

To drop the rewrite rule `newrule`:

```text
DROP RULE newrule ON mytable;
```

### Compatibility

`DROP RULE` is a PostgreSQL language extension, as is the entire query rewrite system.

### See Also

[CREATE RULE](https://www.postgresql.org/docs/10/static/sql-createrule.html), [ALTER RULE](https://www.postgresql.org/docs/10/static/sql-alterrule.html)

