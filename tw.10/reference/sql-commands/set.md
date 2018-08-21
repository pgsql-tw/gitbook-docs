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

### 說明

SET 指令變更執行環境的配置參數。[第 19 章](../../server-administration/server-configuration/)中列出的許多執行環境參數都可以使用 SET 動態變更。（但有些需要超級使用者權限才能變更，有些參數則是伺服器或連線啟動後無法變更。）SET 僅影響目前連線所使用的值。

如果在稍後中止的事務中發出 SET（或等效的 SET SESSION），則在回溯事務時 SET 指令的效果也會消失。一旦提交了相關的事務，則效果將持續到連線結束，除非被另一個 SET 覆寫。

SET LOCAL 的效果僅持續到目前事務結束，無論是否已提交。一個特殊情況是在單個事務中 SET 後跟 SET LOCAL：SET LOCAL 值將一直顯示直到事務結束，但在事務之後（如果事務已提交）SET 值將生效。

透過回溯到早於指令的 savepoint，也會取消 SET 或 SET LOCAL 的效果。

如果在具有相同變數的 SET 選項函數中使用 SET LOCAL（參閱 [CREATE FUNCTION](create-function.md)），則 SET LOCAL 指令的效果在函數結束時消失；也就是說，無論如何都會恢復呼叫函數時生效的值。這允許 SET LOCAL 用於函數內參數的動態或重複變更，同時仍然可以方便地使用 SET 選項來保存和恢復呼叫者的值。但是，一般 SET 指令會覆寫任何相關函數的 SET 選項；除非回溯，否則其效果將持續存在。

**注意**  
在 PostgreSQL 版本 8.0 到 8.2 中，SET LOCAL 的效果將透過釋放較早的 savepoint 或成功退出 PL/pgSQL 例外處理來取消。此行為已被調整，因為它被認為是不直觀的。

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

