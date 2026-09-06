<a id="id-1.9.3.119.1"></a>

## DROP OPERATOR

DROP OPERATOR — remove an operator

## Synopsis

```

DROP OPERATOR [ IF EXISTS ] name ( { left_type | NONE } , right_type ) [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.119.5"></a>

## Description

`DROP OPERATOR` drops an existing operator from
the database system. To execute this command you must be the owner
of the operator.

<a id="id-1.9.3.119.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the operator does not exist. A notice is issued
    in this case.

*`name`*
:   The name (optionally schema-qualified) of an existing operator.

*`left_type`*
:   The data type of the operator's left operand; write
    `NONE` if the operator has no left operand.

*`right_type`*
:   The data type of the operator's right operand.

`CASCADE`
:   Automatically drop objects that depend on the operator (such as views
    using it), and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the operator if any objects depend on it. This
    is the default.

<a id="id-1.9.3.119.7"></a>

## Examples

Remove the power operator `a^b` for type `integer`:

```

DROP OPERATOR ^ (integer, integer);
```

Remove the bitwise-complement prefix operator
`~b` for type `bit`:

```

DROP OPERATOR ~ (none, bit);
```

Remove multiple operators in one command:

```

DROP OPERATOR ~ (none, bit), ^ (integer, integer);
```

<a id="id-1.9.3.119.8"></a>

## Compatibility

There is no `DROP OPERATOR` statement in the SQL standard.

<a id="id-1.9.3.119.9"></a>

## See Also

[CREATE OPERATOR](sql-createoperator.md), [ALTER OPERATOR](sql-alteroperator.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropoperator.html)（英文原文，待翻譯）
