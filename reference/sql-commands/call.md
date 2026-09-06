<a id="SQL-CALL"></a><a id="id-1.9.3.48.1"></a>

# CALL

CALL — invoke a procedure

## Synopsis

```

CALL name ( [ argument ] [, ...] )
```

<a id="id-1.9.3.48.5"></a>

## Description

`CALL` executes a procedure.

If the procedure has any output parameters, then a result row will be returned, containing the values of those parameters.

<a id="id-1.9.3.48.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of the procedure.

<em class="replaceable"><code>argument</code></em>

An argument expression for the procedure call.

Arguments can include parameter names, using the syntax <code class="literal"><em class="replaceable"><code>name</code></em> =&gt; <em class="replaceable"><code>value</code></em></code>. This works the same as in ordinary function calls; see [Section 4.3](../../the-sql-language/sql-syntax/4.3.-han-shu-hu-jiao.md) for details.

Arguments must be supplied for all procedure parameters that lack defaults, including `OUT` parameters. However, arguments matching `OUT` parameters are not evaluated, so it's customary to just write `NULL` for them. (Writing something else for an `OUT` parameter might cause compatibility problems with future PostgreSQL versions.)

<a id="id-1.9.3.48.7"></a>

## Notes

The user must have `EXECUTE` privilege on the procedure in order to be allowed to invoke it.

To call a function (not a procedure), use `SELECT` instead.

If `CALL` is executed in a transaction block, then the called procedure cannot execute transaction control statements. Transaction control statements are only allowed if `CALL` is executed in its own transaction.

PL/pgSQL handles output parameters in `CALL` commands differently; see [Section 43.6.3](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-CALLING-PROCEDURE).

<a id="id-1.9.3.48.8"></a>

## Examples

```

CALL do_db_maintenance();
```

<a id="id-1.9.3.48.9"></a>

## Compatibility

`CALL` conforms to the SQL standard, except for the handling of output parameters. The standard says that users should write variables to receive the values of output parameters.

<a id="id-1.9.3.48.10"></a>

## See Also

[CREATE PROCEDURE](create-procedure.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-call.html)（英文原文，待翻譯）
