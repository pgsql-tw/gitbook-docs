# CREATE FUNCTION

CREATE FUNCTION — 定義一個新函數

## Synopsis

```text
CREATE [ OR REPLACE ] FUNCTION
  name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_namecolumn_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | IMMUTABLE | STABLE | VOLATILE | [ NOT ] LEAKPROOF
    | CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    | [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
  } ...
    [ WITH ( attribute [, ...] ) ]
```

## 說明

`CREATE FUNCTION 用來定義一個新函數。CREATE OR REPLACE FUNCTION 將建立一個新的函數，或是更換現有的函數定義。為了能夠定義一個函數，使用者必須具有該程式語言的 USAGE 權限。`

如果包含 schema，則該函數將在指定的 schema 中建立。否則它會在目前的 schema中建立。新函數的名稱不得與相同 schema 中具有相同輸入參數型別的任何現有函數相同。但是，不同參數型別的函數可以共享一個名稱（稱為多載 overloading）。

要更換現有函數的目前定義，請使用 CREATE OR REPLACE FUNCTION。以這種方式改變函數的名稱或參數型別是不可行的（如果你嘗試做了，實際上你會建立一個新的、不同的函數）。另外，CREATE OR REPLACE FUNCTION 不會讓你改變現有函數的回傳型別。為此，你必須刪除並重新建立該函數。（使用 OUT 參數時，這意味著你不能更改任何 OUT 參數的型別，除非移除該函數。）

當使用 CREATE OR REPLACE FUNCTION 替換現有函數時，該函數的所有權和權限都不會改變。所有其他的函數屬性都被分配了指令中指定或隱含的值。你必須擁有取代它的功能（這包括成為自己角色群組的成員）。

如果你刪除然後重新建立一個函數，那麼新函數與舊的函數不是同一個實體；你必須刪除引用舊功能的現有規則、view、觸發器等。使用 CREATE OR REPLACE FUNCTION 來更改函數定義而不會破壞引用該函數的物件。此外，ALTER FUNCTION 可用於更改現有函數的大部分輔助屬性。

建立函數的使用者會成為該函數的所有者。

為了能夠建立一個函數，你必須對參數型別和回傳型別具有 USAGE 權限。

## 參數

`name`

要建立的函數名稱（可以加上 schema）。

`argmode`

參數的模式：IN、OUT、INOUT 或 VARIADIC。如果省略的話，則預設為 IN。只有 OUT 參數可以接著 VARIADIC 之後。此外，OUT 和 INOUT 參數不能與 RETURNS TABLE 表示法一起使用。

`argname`

參數的名稱。在某些語言（包括 SQL 和 PL/pgSQL）可讓你在函數中使用該名稱。對於其他語言而言，就函數本身而言，輸入參數的名稱只是額外的文件；但可以在呼叫函數時使用輸入參數名稱，以提高可讀性（請參閱[第 4.3 節](../../sql/syntax/calling-funcs.md)）。在任何情況下，輸出參數的名稱都很重要，因為它會在結果的欄位型別中定義了欄位名稱。 （如果你省略輸出參數的名稱，系統將自行選擇一個預設的欄位名稱。）

`argtype`

如果有的話，函數參數的資料型別（可加上 schema）。參數型別可以是基本型別、複合型別或 domain 型別，也可以引用資料表欄位的型別。

根據實作語言的不同，它也可能被指定為「偽型別」，例如 cstring。偽型別表示實際參數型別或者是不完整指定的，或者是在普通 SQL 資料型別集合之外的型別。

透過寫成 table\_name.column\_name %TYPE來引用欄位的型別。使用此功能有時可以幫助建立獨立於資料表定義的修改功能。

`default_expr`

如果未指定參數，則將用作預設值的表示式。該表示式必須是參數的參數型別的強制性。 只有輸入（包括 INOUT）參數可以有一個預設值。具有預設值的參數之後的所有輸入參數也必須具有預設值。

`rettype`

The return data type \(optionally schema-qualified\). The return type can be a base, composite, or domain type, or can reference the type of a table column. Depending on the implementation language it might also be allowed to specify“pseudo-types”such as`cstring`. If the function is not supposed to return a value, specify`void`as the return type.

When there are`OUT`or`INOUT`parameters, the`RETURNS`clause can be omitted. If present, it must agree with the result type implied by the output parameters:`RECORD`if there are multiple output parameters, or the same type as the single output parameter.

The`SETOF`modifier indicates that the function will return a set of items, rather than a single item.

The type of a column is referenced by writing`table_name`.`column_name`%TYPE.

`column_name`

The name of an output column in the`RETURNS TABLE`syntax. This is effectively another way of declaring a named`OUT`parameter, except that`RETURNS TABLE`also implies`RETURNS SETOF`.

`column_type`

The data type of an output column in the`RETURNS TABLE`syntax.

`lang_name`

The name of the language that the function is implemented in. It can be`sql`,`c`,`internal`, or the name of a user-defined procedural language, e.g.`plpgsql`. Enclosing the name in single quotes is deprecated and requires matching case.

`TRANSFORM { FOR TYPEtype_name`} \[, ... \] }

Lists which transforms a call to the function should apply. Transforms convert between SQL types and language-specific data types; see[CREATE TRANSFORM](https://www.postgresql.org/docs/10/static/sql-createtransform.html). Procedural language implementations usually have hardcoded knowledge of the built-in types, so those don't need to be listed here. If a procedural language implementation does not know how to handle a type and no transform is supplied, it will fall back to a default behavior for converting data types, but this depends on the implementation.

`WINDOW`

`WINDOW`indicates that the function is a\_window function\_rather than a plain function. This is currently only useful for functions written in C. The`WINDOW`attribute cannot be changed when replacing an existing function definition.

`IMMUTABLE`

`STABLE`

`VOLATILE`

These attributes inform the query optimizer about the behavior of the function. At most one choice can be specified. If none of these appear,`VOLATILE`is the default assumption.

`IMMUTABLE`indicates that the function cannot modify the database and always returns the same result when given the same argument values; that is, it does not do database lookups or otherwise use information not directly present in its argument list. If this option is given, any call of the function with all-constant arguments can be immediately replaced with the function value.

`STABLE`indicates that the function cannot modify the database, and that within a single table scan it will consistently return the same result for the same argument values, but that its result could change across SQL statements. This is the appropriate selection for functions whose results depend on database lookups, parameter variables \(such as the current time zone\), etc. \(It is inappropriate for`AFTER`triggers that wish to query rows modified by the current command.\) Also note that the`current_timestamp`family of functions qualify as stable, since their values do not change within a transaction.

`VOLATILE`indicates that the function value can change even within a single table scan, so no optimizations can be made. Relatively few database functions are volatile in this sense; some examples are`random()`,`currval()`,`timeofday()`. But note that any function that has side-effects must be classified volatile, even if its result is quite predictable, to prevent calls from being optimized away; an example is`setval()`.

For additional details see[Section 37.6](https://www.postgresql.org/docs/10/static/xfunc-volatility.html).

`LEAKPROOF`

`LEAKPROOF`indicates that the function has no side effects. It reveals no information about its arguments other than by its return value. For example, a function which throws an error message for some argument values but not others, or which includes the argument values in any error message, is not leakproof. This affects how the system executes queries against views created with the`security_barrier`option or tables with row level security enabled. The system will enforce conditions from security policies and security barrier views before any user-supplied conditions from the query itself that contain non-leakproof functions, in order to prevent the inadvertent exposure of data. Functions and operators marked as leakproof are assumed to be trustworthy, and may be executed before conditions from security policies and security barrier views. In addition, functions which do not take arguments or which are not passed any arguments from the security barrier view or table do not have to be marked as leakproof to be executed before security conditions. See[CREATE VIEW](https://www.postgresql.org/docs/10/static/sql-createview.html)and[Section 40.5](https://www.postgresql.org/docs/10/static/rules-privileges.html). This option can only be set by the superuser.

`CALLED ON NULL INPUT`

`RETURNS NULL ON NULL INPUT`

`STRICT`

`CALLED ON NULL INPUT`\(the default\) indicates that the function will be called normally when some of its arguments are null. It is then the function author's responsibility to check for null values if necessary and respond appropriately.

`RETURNS NULL ON NULL INPUT`or`STRICT`indicates that the function always returns null whenever any of its arguments are null. If this parameter is specified, the function is not executed when there are null arguments; instead a null result is assumed automatically.

`[EXTERNAL] SECURITY INVOKER  
[EXTERNAL] SECURITY DEFINER`

`SECURITY INVOKER`indicates that the function is to be executed with the privileges of the user that calls it. That is the default.`SECURITY DEFINER`specifies that the function is to be executed with the privileges of the user that owns it.

The key word`EXTERNAL`is allowed for SQL conformance, but it is optional since, unlike in SQL, this feature applies to all functions not only external ones.

`PARALLEL`

`PARALLEL UNSAFE`indicates that the function can't be executed in parallel mode and the presence of such a function in an SQL statement forces a serial execution plan. This is the default.`PARALLEL RESTRICTED`indicates that the function can be executed in parallel mode, but the execution is restricted to parallel group leader.`PARALLEL SAFE`indicates that the function is safe to run in parallel mode without restriction.

Functions should be labeled parallel unsafe if they modify any database state, or if they make changes to the transaction such as using sub-transactions, or if they access sequences or attempt to make persistent changes to settings \(e.g.`setval`\). They should be labeled as parallel restricted if they access temporary tables, client connection state, cursors, prepared statements, or miscellaneous backend-local state which the system cannot synchronize in parallel mode \(e.g.`setseed`cannot be executed other than by the group leader because a change made by another process would not be reflected in the leader\). In general, if a function is labeled as being safe when it is restricted or unsafe, or if it is labeled as being restricted when it is in fact unsafe, it may throw errors or produce wrong answers when used in a parallel query. C-language functions could in theory exhibit totally undefined behavior if mislabeled, since there is no way for the system to protect itself against arbitrary C code, but in most likely cases the result will be no worse than for any other function. If in doubt, functions should be labeled as`UNSAFE`, which is the default.

`execution_cost`

A positive number giving the estimated execution cost for the function, in units of[cpu\_operator\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-CPU-OPERATOR-COST). If the function returns a set, this is the cost per returned row. If the cost is not specified, 1 unit is assumed for C-language and internal functions, and 100 units for functions in all other languages. Larger values cause the planner to try to avoid evaluating the function more often than necessary.

`result_rows`

A positive number giving the estimated number of rows that the planner should expect the function to return. This is only allowed when the function is declared to return a set. The default assumption is 1000 rows.

`configuration_parameter`

`value`

The`SET`clause causes the specified configuration parameter to be set to the specified value when the function is entered, and then restored to its prior value when the function exits.`SET FROM CURRENT`saves the value of the parameter that is current when`CREATE FUNCTION`is executed as the value to be applied when the function is entered.

If a`SET`clause is attached to a function, then the effects of a`SET LOCAL`command executed inside the function for the same variable are restricted to the function: the configuration parameter's prior value is still restored at function exit. However, an ordinary`SET`command \(without`LOCAL`\) overrides the`SET`clause, much as it would do for a previous`SET LOCAL`command: the effects of such a command will persist after function exit, unless the current transaction is rolled back.

See[SET](https://www.postgresql.org/docs/10/static/sql-set.html)and[Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html)for more information about allowed parameter names and values.

`definition`

A string constant defining the function; the meaning depends on the language. It can be an internal function name, the path to an object file, an SQL command, or text in a procedural language.

It is often helpful to use dollar quoting \(see[Section 4.1.2.4](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING)\) to write the function definition string, rather than the normal single quote syntax. Without dollar quoting, any single quotes or backslashes in the function definition must be escaped by doubling them.

`obj_file`,`link_symbol`

This form of the`AS`clause is used for dynamically loadable C language functions when the function name in the C language source code is not the same as the name of the SQL function. The string`obj_file`_\_is the name of the shared library file containing the compiled C function, and is interpreted as for the_[_LOAD_](https://www.postgresql.org/docs/10/static/sql-load.html)_command. The string_`link_symbol`\_is the function's link symbol, that is, the name of the function in the C language source code. If the link symbol is omitted, it is assumed to be the same as the name of the SQL function being defined.

When repeated`CREATE FUNCTION`calls refer to the same object file, the file is only loaded once per session. To unload and reload the file \(perhaps during development\), start a new session.

`attribute`

The historical way to specify optional pieces of information about the function. The following attributes can appear here:

`isStrict`

Equivalent to`STRICT`or`RETURNS NULL ON NULL INPUT`.

`isCachable`

`isCachable`is an obsolete equivalent of`IMMUTABLE`; it's still accepted for backwards-compatibility reasons.

Attribute names are not case-sensitive.

Refer to[Section 37.3](https://www.postgresql.org/docs/10/static/xfunc.html)for further information on writing functions.

## Overloading

PostgreSQLallows function_overloading_; that is, the same name can be used for several different functions so long as they have distinct input argument types. However, the C names of all functions must be different, so you must give overloaded C functions different C names \(for example, use the argument types as part of the C names\).

Two functions are considered the same if they have the same names and\_input\_argument types, ignoring any`OUT`parameters. Thus for example these declarations conflict:

```text
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, out text) ...
```

Functions that have different argument type lists will not be considered to conflict at creation time, but if defaults are provided they might conflict in use. For example, consider

```text
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, int default 42) ...
```

A call`foo(10)`will fail due to the ambiguity about which function should be called.

## Notes

The fullSQLtype syntax is allowed for declaring a function's arguments and return value. However, parenthesized type modifiers \(e.g., the precision field for type`numeric`\) are discarded by`CREATE FUNCTION`. Thus for example`CREATE FUNCTION foo (varchar(10)) ...`is exactly the same as`CREATE FUNCTION foo (varchar) ...`.

When replacing an existing function with`CREATE OR REPLACE FUNCTION`, there are restrictions on changing parameter names. You cannot change the name already assigned to any input parameter \(although you can add names to parameters that had none before\). If there is more than one output parameter, you cannot change the names of the output parameters, because that would change the column names of the anonymous composite type that describes the function's result. These restrictions are made to ensure that existing calls of the function do not stop working when it is replaced.

If a function is declared`STRICT`with a`VARIADIC`argument, the strictness check tests that the variadic array\_as a whole\_is non-null. The function will still be called if the array has null elements.

## Examples

Here are some trivial examples to help you get started. For more information and examples, see[Section 37.3](https://www.postgresql.org/docs/10/static/xfunc.html).

```text
CREATE FUNCTION add(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
```

Increment an integer, making use of an argument name, inPL/pgSQL:

```text
CREATE OR REPLACE FUNCTION increment(i integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
```

Return a record containing multiple output parameters:

```text
CREATE FUNCTION dup(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

You can do the same thing more verbosely with an explicitly named composite type:

```text
CREATE TYPE dup_result AS (f1 int, f2 text);

CREATE FUNCTION dup(int) RETURNS dup_result
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

Another way to return multiple columns is to use a`TABLE`function:

```text
CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

However, a`TABLE`function is different from the preceding examples, because it actually returns a\_set\_of records, not just one record.

## Writing`SECURITY DEFINER`Functions Safely

Because a`SECURITY DEFINER`function is executed with the privileges of the user that owns it, care is needed to ensure that the function cannot be misused. For security,[search\_path](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SEARCH-PATH)should be set to exclude any schemas writable by untrusted users. This prevents malicious users from creating objects \(e.g., tables, functions, and operators\) that mask objects intended to be used by the function. Particularly important in this regard is the temporary-table schema, which is searched first by default, and is normally writable by anyone. A secure arrangement can be obtained by forcing the temporary schema to be searched last. To do this, write`pg_temp`as the last entry in`search_path`. This function illustrates safe usage:

```text
CREATE FUNCTION check_password(uname TEXT, pass TEXT)
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
BEGIN
        SELECT  (pwd = $2) INTO passed
        FROM    pwds
        WHERE   username = $1;

        RETURN passed;
END;
$$  LANGUAGE plpgsql
    SECURITY DEFINER
    -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
    SET search_path = admin, pg_temp;
```

This function's intention is to access a table`admin.pwds`. But without the`SET`clause, or with a`SET`clause mentioning only`admin`, the function could be subverted by creating a temporary table named`pwds`.

BeforePostgreSQLversion 8.3, the`SET`clause was not available, and so older functions may contain rather complicated logic to save, set, and restore`search_path`. The`SET`clause is far easier to use for this purpose.

Another point to keep in mind is that by default, execute privilege is granted to`PUBLIC`for newly created functions \(see[GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html)for more information\). Frequently you will wish to restrict use of a security definer function to only some users. To do that, you must revoke the default`PUBLIC`privileges and then grant execute privilege selectively. To avoid having a window where the new function is accessible to all, create it and set the privileges within a single transaction. For example:

```text
BEGIN;
CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER;
REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins;
COMMIT;
```

## Compatibility

A`CREATE FUNCTION`command is defined in SQL:1999 and later. ThePostgreSQLversion is similar but not fully compatible. The attributes are not portable, neither are the different available languages.

For compatibility with some other database systems,`argmode`_\_can be written either before or after_`argname`\_. But only the first way is standard-compliant.

For parameter defaults, the SQL standard specifies only the syntax with the`DEFAULT`key word. The syntax with`=`is used in T-SQL and Firebird.

## See Also

[ALTER FUNCTION](https://www.postgresql.org/docs/10/static/sql-alterfunction.html), [DROP FUNCTION](https://www.postgresql.org/docs/10/static/sql-dropfunction.html), [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html), [LOAD](https://www.postgresql.org/docs/10/static/sql-load.html), [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html)

