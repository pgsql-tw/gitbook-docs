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

### 參數

`SESSION`

指定此指令對目前連線生效。（如果 SESSION 和 LOCAL 都沒有出現，這是預設行為。）

`LOCAL`

指定此指令僅對目前事務生效。在 COMMIT 或 ROLLBACK 之後，連線等級的設定會再次生效。在事務區塊之外發出此指令會發出警告，並且無效。

_`configuration_parameter`_

可設定的執行環境參數名稱。可用參數記錄在[第 19 章](../../server-administration/server-configuration/)及其以下小節。

_`value`_

參數的新值。可以將值指定為字串常數、識別字、數字或逗號分隔的值列表，以適應特定參數。可以使用 DEFAULT 來指定將參數重置為其預設值（即如果在目前會話中沒有執行 SET，它將具有的值）。

除了[第 19 章](../../server-administration/server-configuration/)中記錄的配置參數外，還有一些只能使用 SET 指令調整或具備的特殊語法：

`SCHEMA`

`SET SCHEMA 'value'` 是 `SET search_path TO value` 的別名。使用此語法只能指定一個綱要。

`NAMES`

`SET NAMES value` 是 `SET client_encoding TO value` 的別名。

`SEED`

設定隨機數産生器的內部種子（函數隨機）。允許值是介於 -1 和 1 之間的浮點數，然後乘以 2^31-1。

也可以透過呼叫 setseed 函數來設定種子：

```text
SELECT setseed(value);
```

`TIME ZONE`

SET TIME ZONE value 是 SET timezone TO value 的別名。語法 SET TIME ZONE 是允許時區規範的特殊語法。以下是有效值的範例：

`'PST8PDT'`

Berkeley, California 的時區。

`'Europe/Rome'`

義大利的時區。

`-7`

從 UTC 往西 7 小時的時區（相當於 PDT）。正值為 UTC 往東。

`INTERVAL '-08:00' HOUR TO MINUTE`

從 UTC 往西 8 小時的時區（相當於 PST）。

`LOCAL`  
`DEFAULT`

將時區設定為本地時區（即伺服器的時區預設值）。

以數字或間隔設定的時區設定在內部轉換為 POSIX 時區語法。例如，在 SET TIME ZONE -7 之後，SHOW TIME ZONE 將回報 &lt;-07&gt;+07。

有關時區的更多訊息，請參閱[第 8.5.3 節](../../the-sql-language/data-types/8.5.-ri-qi-shi-jian-xing-bie.md#8-5-3-time-zones)。

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

