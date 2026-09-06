<a id="id-1.9.3.48.1"></a>

## CALL

CALL — invoke a procedure

## Synopsis

```

CALL name ( [ argument ] [, ...] )
```

<a id="id-1.9.3.48.5"></a>

## Description

`CALL` executes a procedure.

If the procedure has any output parameters, then a result row will be
returned, containing the values of those parameters.

<a id="id-1.9.3.48.6"></a>

## Parameters

*`name`*
:   The name (optionally schema-qualified) of the procedure.

*`argument`*
:   An argument expression for the procedure call.

    Arguments can include parameter names, using the syntax
    `name => value`.
    This works the same as in ordinary function calls; see
    [Section 4.3](../../the-sql-language/sql-syntax/sql-syntax-calling-funcs.md) for details.

    Arguments must be supplied for all procedure parameters that lack
    defaults, including `OUT` parameters. However,
    arguments matching `OUT` parameters are not evaluated,
    so it's customary to just write `NULL` for them.
    (Writing something else for an `OUT` parameter
    might cause compatibility problems with
    future PostgreSQL versions.)

<a id="id-1.9.3.48.7"></a>

## Notes

The user must have `EXECUTE` privilege on the procedure in
order to be allowed to invoke it.

To call a function (not a procedure), use `SELECT` instead.

If `CALL` is executed in a transaction block, then the
called procedure cannot execute transaction control statements.
Transaction control statements are only allowed if `CALL`
is executed in its own transaction.

PL/pgSQL handles output parameters
in `CALL` commands differently;
see [Section 41.6.3](../../server-programming/plpgsql/plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE).

<a id="id-1.9.3.48.8"></a>

## Examples

```

CALL do_db_maintenance();
```

<a id="id-1.9.3.48.9"></a>

## Compatibility

`CALL` conforms to the SQL standard,
except for the handling of output parameters. The standard
says that users should write variables to receive the values
of output parameters.

<a id="id-1.9.3.48.10"></a>

## See Also

[CREATE PROCEDURE](sql-createprocedure.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-call.html)（英文原文，待翻譯）
