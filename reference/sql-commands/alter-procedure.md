<a id="SQL-ALTERPROCEDURE"></a><a id="id-1.9.3.24.1"></a>

# ALTER PROCEDURE

ALTER PROCEDURE — change the definition of a procedure

## Synopsis

```

ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

<a id="id-1.9.3.24.5"></a>

## Description

`ALTER PROCEDURE` changes the definition of a procedure.

You must own the procedure to use `ALTER PROCEDURE`. To change a procedure's schema, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the procedure's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the procedure. However, a superuser can alter ownership of any procedure anyway.)

<a id="id-1.9.3.24.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing procedure. If no argument list is specified, the name must be unique in its schema.

<em class="replaceable"><code>argmode</code></em>

The mode of an argument: `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`.

<em class="replaceable"><code>argname</code></em>

The name of an argument. Note that `ALTER PROCEDURE` does not actually pay any attention to argument names, since only the argument data types are used to determine the procedure's identity.

<em class="replaceable"><code>argtype</code></em>

The data type(s) of the procedure's arguments (optionally schema-qualified), if any. See [DROP PROCEDURE](drop-procedure.md) for the details of how the procedure is looked up using the argument data type(s).

<em class="replaceable"><code>new&#95;name</code></em>

The new name of the procedure.

<em class="replaceable"><code>new&#95;owner</code></em>

The new owner of the procedure. Note that if the procedure is marked `SECURITY DEFINER`, it will subsequently execute as the new owner.

<em class="replaceable"><code>new&#95;schema</code></em>

The new schema for the procedure.

<em class="replaceable"><code>extension&#95;name</code></em>

This form marks the procedure as dependent on the extension, or no longer dependent on the extension if `NO` is specified. A procedure that's marked as dependent on an extension is dropped when the extension is dropped, even if cascade is not specified. A procedure can depend upon multiple extensions, and will be dropped when any one of those extensions is dropped.

<code class="literal">&#91; <span class="optional">EXTERNAL</span> &#93; SECURITY INVOKER</code><br><code class="literal">&#91; <span class="optional">EXTERNAL</span> &#93; SECURITY DEFINER</code>

Change whether the procedure is a security definer or not. The key word `EXTERNAL` is ignored for SQL conformance. See [CREATE PROCEDURE](create-procedure.md) for more information about this capability.

<em class="replaceable"><code>configuration&#95;parameter</code></em><br><em class="replaceable"><code>value</code></em>

Add or change the assignment to be made to a configuration parameter when the procedure is called. If <em class="replaceable"><code>value</code></em> is `DEFAULT` or, equivalently, `RESET` is used, the procedure-local setting is removed, so that the procedure executes with the value present in its environment. Use `RESET ALL` to clear all procedure-local settings. `SET FROM CURRENT` saves the value of the parameter that is current when `ALTER PROCEDURE` is executed as the value to be applied when the procedure is entered.

See [SET](set.md) and [Chapter 20](../../server-administration/server-configuration/README.md) for more information about allowed parameter names and values.

`RESTRICT`

Ignored for conformance with the SQL standard.

<a id="id-1.9.3.24.7"></a>

## Examples

To rename the procedure `insert_data` with two arguments of type `integer` to `insert_record`:

```

ALTER PROCEDURE insert_data(integer, integer) RENAME TO insert_record;
```

To change the owner of the procedure `insert_data` with two arguments of type `integer` to `joe`:

```

ALTER PROCEDURE insert_data(integer, integer) OWNER TO joe;
```

To change the schema of the procedure `insert_data` with two arguments of type `integer` to `accounting`:

```

ALTER PROCEDURE insert_data(integer, integer) SET SCHEMA accounting;
```

To mark the procedure `insert_data(integer, integer)` as being dependent on the extension `myext`:

```

ALTER PROCEDURE insert_data(integer, integer) DEPENDS ON EXTENSION myext;
```

To adjust the search path that is automatically set for a procedure:

```

ALTER PROCEDURE check_password(text) SET search_path = admin, pg_temp;
```

To disable automatic setting of `search_path` for a procedure:

```

ALTER PROCEDURE check_password(text) RESET search_path;
```

The procedure will now execute with whatever search path is used by its caller.

<a id="id-1.9.3.24.8"></a>

## Compatibility

This statement is partially compatible with the `ALTER PROCEDURE` statement in the SQL standard. The standard allows more properties of a procedure to be modified, but does not provide the ability to rename a procedure, make a procedure a security definer, attach configuration parameter values to a procedure, or change the owner, schema, or volatility of a procedure. The standard also requires the `RESTRICT` key word, which is optional in PostgreSQL.

<a id="id-1.9.3.24.9"></a>

## See Also

[CREATE PROCEDURE](create-procedure.md), [DROP PROCEDURE](drop-procedure.md), [ALTER FUNCTION](alter-function.md), [ALTER ROUTINE](alter-routine.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-alterprocedure.html)（英文原文，待翻譯）
