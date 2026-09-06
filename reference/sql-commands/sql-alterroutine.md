<a id="id-1.9.3.27.1"></a>

## ALTER ROUTINE

ALTER ROUTINE — change the definition of a routine

## Synopsis

```

ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    IMMUTABLE | STABLE | VOLATILE
    [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

<a id="id-1.9.3.27.5"></a>

## Description

`ALTER ROUTINE` changes the definition of a routine, which
can be an aggregate function, a normal function, or a procedure. See
under [ALTER AGGREGATE](sql-alteraggregate.md), [ALTER FUNCTION](sql-alterfunction.md),
and [ALTER PROCEDURE](sql-alterprocedure.md) for the description of the
parameters, more examples, and further details.

<a id="id-1.9.3.27.6"></a>

## Examples

To rename the routine `foo` for type
`integer` to `foobar`:

```

ALTER ROUTINE foo(integer) RENAME TO foobar;
```

This command will work independent of whether `foo` is an
aggregate, function, or procedure.

<a id="id-1.9.3.27.7"></a>

## Compatibility

This statement is partially compatible with the `ALTER
ROUTINE` statement in the SQL standard. See
under [ALTER FUNCTION](sql-alterfunction.md)
and [ALTER PROCEDURE](sql-alterprocedure.md) for more details. Allowing
routine names to refer to aggregate functions is
a PostgreSQL extension.

<a id="id-1.9.3.27.8"></a>

## See Also

[ALTER AGGREGATE](sql-alteraggregate.md), [ALTER FUNCTION](sql-alterfunction.md), [ALTER PROCEDURE](sql-alterprocedure.md), [DROP ROUTINE](sql-droproutine.md)

Note that there is no `CREATE ROUTINE` command.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterroutine.html)（英文原文，待翻譯）
