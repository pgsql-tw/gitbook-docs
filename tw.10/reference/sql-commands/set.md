---
description: 版本：10
---

# SET

SET — 變更執行環境參數

### 語法

```text
SET [ SESSION | LOCAL ] configuration_parameter { TO | = } { value | 'value' | DEFAULT }
SET [ SESSION | LOCAL ] TIME ZONE { timezone | LOCAL | DEFAULT }
```

### Description

The `SET` command changes run-time configuration parameters. Many of the run-time parameters listed in [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html) can be changed on-the-fly with `SET`. \(But some require superuser privileges to change, and others cannot be changed after server or session start.\) `SET` only affects the value used by the current session.

If `SET` \(or equivalently `SET SESSION`\) is issued within a transaction that is later aborted, the effects of the `SET` command disappear when the transaction is rolled back. Once the surrounding transaction is committed, the effects will persist until the end of the session, unless overridden by another `SET`.

The effects of `SET LOCAL` last only till the end of the current transaction, whether committed or not. A special case is `SET` followed by `SET LOCAL` within a single transaction: the `SET LOCAL` value will be seen until the end of the transaction, but afterwards \(if the transaction is committed\) the `SET` value will take effect.

The effects of `SET` or `SET LOCAL` are also canceled by rolling back to a savepoint that is earlier than the command.

If `SET LOCAL` is used within a function that has a `SET` option for the same variable \(see [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html)\), the effects of the `SET LOCAL` command disappear at function exit; that is, the value in effect when the function was called is restored anyway. This allows `SET LOCAL` to be used for dynamic or repeated changes of a parameter within a function, while still having the convenience of using the `SET` option to save and restore the caller's value. However, a regular `SET` command overrides any surrounding function's `SET` option; its effects will persist unless rolled back.

#### Note

In PostgreSQL versions 8.0 through 8.2, the effects of a `SET LOCAL` would be canceled by releasing an earlier savepoint, or by successful exit from a PL/pgSQL exception block. This behavior has been changed because it was deemed unintuitive.

### Parameters

`SESSION`

Specifies that the command takes effect for the current session. \(This is the default if neither `SESSION` nor `LOCAL` appears.\)`LOCAL`

Specifies that the command takes effect for only the current transaction. After `COMMIT` or `ROLLBACK`, the session-level setting takes effect again. Issuing this outside of a transaction block emits a warning and otherwise has no effect.

_`configuration_parameter`_

Name of a settable run-time parameter. Available parameters are documented in [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html) and below._`value`_

New value of parameter. Values can be specified as string constants, identifiers, numbers, or comma-separated lists of these, as appropriate for the particular parameter. `DEFAULT` can be written to specify resetting the parameter to its default value \(that is, whatever value it would have had if no `SET` had been executed in the current session\).

Besides the configuration parameters documented in [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html), there are a few that can only be adjusted using the `SET` command or that have a special syntax:

`SCHEMA`

`SET SCHEMA '`_`value`_' is an alias for `SET search_path TO` _`value`_. Only one schema can be specified using this syntax.

`NAMES`

`SET NAMES` _`value`_ is an alias for `SET client_encoding TO` _`value`_.

`SEED`

Sets the internal seed for the random number generator \(the function `random`\). Allowed values are floating-point numbers between -1 and 1, which are then multiplied by 231-1.

The seed can also be set by invoking the function `setseed`:

```text
SELECT setseed(value);
```

`TIME ZONE`

`SET TIME ZONE` _`value`_ is an alias for `SET timezone TO` _`value`_. The syntax `SET TIME ZONE` allows special syntax for the time zone specification. Here are examples of valid values:

`'PST8PDT'`

The time zone for Berkeley, California.

`'Europe/Rome'`

The time zone for Italy.`-7`

The time zone 7 hours west from UTC \(equivalent to PDT\). Positive values are east from UTC.

`INTERVAL '-08:00' HOUR TO MINUTE`

The time zone 8 hours west from UTC \(equivalent to PST\).

`LOCAL`  
`DEFAULT`

Set the time zone to your local time zone \(that is, the server's default value of `timezone`\).

Timezone settings given as numbers or intervals are internally translated to POSIX timezone syntax. For example, after `SET TIME ZONE -7`, `SHOW TIME ZONE` would report `<-07>+07`.

See [Section 8.5.3](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-TIMEZONES) for more information about time zones.

### 注意

函數 set\_config 提供了等效的功能；詳見 [9.26 節](../../the-sql-language/functions-and-operators/9.26.-xi-tong-guan-li-han-shi.md)。此外，也可以更新 [pg\_settings](../../internals/system-catalogs/pg_settings.md) 系統檢視表以執行 SET 的等效操作。

### 範例

設定綱要（schema）搜尋路徑：

```text
SET search_path TO my_schema, public;
```

使用「日期置於月份前面」的輸入方式，將日期樣式設定為傳統 POSTGRES：

```text
SET datestyle TO postgres, dmy;
```

設定為 Berkeley, California 的時區：

```text
SET TIME ZONE 'PST8PDT';
```

設定為義大利的時區：

```text
SET TIME ZONE 'Europe/Rome';
```

### 相容性

SET TIME ZONE 延伸了 SQL 標準所定義的語法。原標準僅允許數字時區語法，而 PostgreSQL 允許更靈活的時區規範。所有其他 SET 功能都是 PostgreSQL 的延伸功能。

### 參閱

[RESET](reset.md), [SHOW](show.md)

