---
description: 版本：10
---

# ALTER FUNCTION

ALTER FUNCTION — 變更一個函數的定義

### 語法

```text
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    DEPENDS ON EXTENSION extension_name

where action is one of:

    CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    IMMUTABLE | STABLE | VOLATILE | [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

### 說明

`ALTER FUNCTION` 變更一個函數的定義。

您必須是函數擁有者才能使用 ALTER FUNCTION 功能。要變更函數的綱要，您還必須具有新綱要的 CREATE 權限。要變更擁有者，您還必須是新擁有角色的直接或間接成員，並且該角色必須對該函數的綱要具有 CREATE 權限。（這些限制強制改變擁有者不會做任何透過刪除和重新建立函數都無法做到的事情，但是超級用戶可以改變任何函數的所有權。）

### Parameters

_`name`_

The name \(optionally schema-qualified\) of an existing function. If no argument list is specified, the name must be unique in its schema.

_`argmode`_

The mode of an argument: `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`. Note that `ALTER FUNCTION` does not actually pay any attention to `OUT` arguments, since only the input arguments are needed to determine the function's identity. So it is sufficient to list the `IN`, `INOUT`, and `VARIADIC` arguments.

_`argname`_

The name of an argument. Note that `ALTER FUNCTION` does not actually pay any attention to argument names, since only the argument data types are needed to determine the function's identity.

_`argtype`_

The data type\(s\) of the function's arguments \(optionally schema-qualified\), if any.

_`new_name`_

The new name of the function.

_`new_owner`_

The new owner of the function. Note that if the function is marked `SECURITY DEFINER`, it will subsequently execute as the new owner.

_`new_schema`_

The new schema for the function.

_`extension_name`_

The name of the extension that the function is to depend on.

`CALLED ON NULL INPUT`  
`RETURNS NULL ON NULL INPUT`  
`STRICT`

`CALLED ON NULL INPUT` changes the function so that it will be invoked when some or all of its arguments are null. `RETURNS NULL ON NULL INPUT` or `STRICT` changes the function so that it is not invoked if any of its arguments are null; instead, a null result is assumed automatically. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for more information.

`IMMUTABLE`  
`STABLE`  
`VOLATILE`

Change the volatility of the function to the specified setting. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for details.

`[ EXTERNAL ] SECURITY INVOKER`  
`[ EXTERNAL ] SECURITY DEFINER`

Change whether the function is a security definer or not. The key word `EXTERNAL` is ignored for SQL conformance. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for more information about this capability.

`PARALLEL`

Change whether the function is deemed safe for parallelism. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for details.

`LEAKPROOF`

Change whether the function is considered leakproof or not. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for more information about this capability.

`COST` _`execution_cost`_

Change the estimated execution cost of the function. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for more information.

`ROWS` _`result_rows`_

Change the estimated number of rows returned by a set-returning function. See [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) for more information.

_`configuration_parameter`_  
_`value`_

Add or change the assignment to be made to a configuration parameter when the function is called. If _`value`_ is `DEFAULT` or, equivalently, `RESET` is used, the function-local setting is removed, so that the function executes with the value present in its environment. Use `RESET ALL` to clear all function-local settings. `SET FROM CURRENT` saves the value of the parameter that is current when `ALTER FUNCTION` is executed as the value to be applied when the function is entered.

See [SET](https://www.postgresql.org/docs/10/static/sql-set.html) and [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html) for more information about allowed parameter names and values.

`RESTRICT`

Ignored for conformance with the SQL standard.

### 範例

要將 integer 型別的函數 sqrt 重新命名為 square\_root：

```text
ALTER FUNCTION sqrt(integer) RENAME TO square_root;
```

要將整數型別函數 sqrt 的擁有者變更為 joe，請執行以下操作：

```text
ALTER FUNCTION sqrt(integer) OWNER TO joe;
```

要將整數型別函數 sqrt 的綱要變更為 maths，請執行以下操作：

```text
ALTER FUNCTION sqrt(integer) SET SCHEMA maths;
```

要將 integer 型別的函數標記為相依於延伸套件 mathlib：

```text
ALTER FUNCTION sqrt(integer) DEPENDS ON EXTENSION mathlib;
```

自動以該函數調整搜尋路徑：

```text
ALTER FUNCTION check_password(text) SET search_path = admin, pg_temp;
```

要停用某個函數的 search\_path 自動設定，請執行以下操作：

```text
ALTER FUNCTION check_password(text) RESET search_path;
```

該函數現在將執行其呼叫者使用的任何搜尋路徑。

### 相容性

此語法與 SQL 標準中的 ALTER FUNCTION 語法部分相容。標準可以允許修改一個函數的更多屬性，但不能提供重新命名函數、使函數成為 security definer、將配置參數值附加到函數或變更函數的擁有者、綱要或易變性的設定。標準還需要 RESTRICT 關鍵字，這在 PostgreSQL 中是選用的。

### 參閱

[CREATE FUNCTION](create-function.md), [DROP FUNCTION](drop-function.md)

