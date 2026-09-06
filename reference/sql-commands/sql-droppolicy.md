<a id="id-1.9.3.123.1"></a>

## DROP POLICY

DROP POLICY — remove a row-level security policy from a table

## Synopsis

```

DROP POLICY [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.123.5"></a>

## Description

`DROP POLICY` removes the specified policy from the table.
Note that if the last policy is removed for a table and the table still has
row-level security enabled via `ALTER TABLE`, then the
default-deny policy will be used. `ALTER TABLE ... DISABLE ROW
LEVEL SECURITY` can be used to disable row-level security for a
table, whether policies for the table exist or not.

<a id="id-1.9.3.123.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the policy does not exist. A notice is issued
    in this case.

*`name`*
:   The name of the policy to drop.

*`table_name`*
:   The name (optionally schema-qualified) of the table that
    the policy is on.

`CASCADE`<br>`RESTRICT`
:   These key words do not have any effect, since there are no
    dependencies on policies.

<a id="id-1.9.3.123.7"></a>

## Examples

To drop the policy called `p1` on the table named
`my_table`:

```

DROP POLICY p1 ON my_table;
```

<a id="id-1.9.3.123.8"></a>

## Compatibility

`DROP POLICY` is a PostgreSQL extension.

<a id="id-1.9.3.123.9"></a>

## See Also

[CREATE POLICY](sql-createpolicy.md), [ALTER POLICY](sql-alterpolicy.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droppolicy.html)（英文原文，待翻譯）
