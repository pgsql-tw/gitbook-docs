<a id="id-1.9.3.174.1"></a>

## SET

SET — 變更一個執行期參數

## 語法

```

SET [ SESSION | LOCAL ] configuration_parameter { TO | = } { value | 'value' | DEFAULT }
SET [ SESSION | LOCAL ] TIME ZONE { value | 'value' | LOCAL | DEFAULT }
```

<a id="id-1.9.3.174.5"></a>

## 說明

`SET` 命令會變更執行期組態參數。[第 19 章](../../server-administration/runtime-config/README.md)
所列出的許多執行期參數，都可以用 `SET`
即時變更。
（有些參數只能由超級使用者，以及被授予對該參數
`SET` 權限的使用者變更。也有些參數
在伺服器或工作階段啟動之後就無法再變更。）
`SET` 只會影響目前工作階段所使用的值。

若在之後被中止的交易內發出 `SET`（或等效的
`SET SESSION`），當該交易被回復時，`SET`
命令的效果就會消失。一旦包住它的交易被提交，
其效果就會持續到工作階段結束為止，除非被另一個
`SET` 覆寫。

`SET LOCAL` 的效果只會持續到目前交易結束為止，無論該交易
是否提交。有一種特殊情況是在同一個交易內先執行 `SET`
再執行 `SET LOCAL`：在交易結束之前都會看到
`SET LOCAL` 所設的值，但之後（若該交易被提交）
`SET` 所設的值就會生效。

回復到早於該命令的儲存點，同樣會取消 `SET` 或
`SET LOCAL` 的效果。

若在函式內使用 `SET LOCAL`，而該函式對同一個變數
已具有 `SET` 選項（見
[CREATE FUNCTION](sql-createfunction.md)），
則 `SET LOCAL` 命令的效果會在函式結束時消失；
也就是說，無論如何都會還原成呼叫該函式時生效的值。這讓
`SET LOCAL` 可以用於在函式內動態或重複地變更參數，
同時仍可利用 `SET` 選項來儲存並還原呼叫端的值，
以享有其便利性。不過，一般的 `SET` 命令會覆寫
任何外層函式的 `SET` 選項；其效果會持續存在，
除非被回復。

### 注意

在 PostgreSQL 8.0 到 8.2 版中，
`SET LOCAL` 的效果會因釋放較早的儲存點，
或因 PL/pgSQL 例外處理區塊順利結束
而被取消。由於這種行為被認為不夠直覺，因此已被變更。

<a id="id-1.9.3.174.6"></a>

## 參數

`SESSION`
:   指定此命令對目前工作階段生效。
    （若 `SESSION` 與 `LOCAL`
    皆未出現，這就是預設值。）

`LOCAL`
:   指定此命令只對目前交易生效。在 `COMMIT` 或
    `ROLLBACK` 之後，工作階段層級的設定會再次生效。
    若在交易區塊之外執行此命令，會發出警告，
    且不會產生其他任何效果。

*`configuration_parameter`*
:   可設定之執行期參數的名稱。可用的參數記載於
    [第 19 章](../../server-administration/runtime-config/README.md)以及下文中。

*`value`*
:   參數的新值。依照個別參數的適用情況，值可以指定為
    字串常數、識別字、數字，或以逗號分隔的這些值清單。
    可以寫 `DEFAULT` 來指定將參數重設為其預設值
    （也就是說，若目前工作階段中未執行過 `SET`，
    該參數原本會有的值）。

除了[第 19 章](../../server-administration/runtime-config/README.md)所記載的組態參數之外，
還有少數幾個參數只能用 `SET` 命令調整，
或具有特殊語法：

`SCHEMA`
:   `SET SCHEMA 'value'` 是
    `SET search_path TO value` 的別名寫法。
    以此語法只能指定一個綱要。

`NAMES`
:   `SET NAMES 'value'` 是
    `SET client_encoding TO value` 的別名寫法。

`SEED`
:   設定亂數產生器（`random` 函式）所使用的內部種子值。
    允許的值為 -1 到 1（含）之間的浮點數。

    也可以透過呼叫函式
    `setseed` 來設定種子值：

    ```

    SELECT setseed(value);
    ```

`TIME ZONE`
:   `SET TIME ZONE 'value'` 是
    `SET timezone TO 'value'` 的別名寫法。
    `SET TIME ZONE` 語法允許為時區規格使用特殊語法。
    以下是有效值的範例：

    `'America/Los_Angeles'`
    :   加州柏克萊的時區。

    `'Europe/Rome'`
    :   義大利的時區。

    `-7`
    :   比 UTC 西邊 7 小時的時區（相當於
        PDT）。正值表示 UTC 以東。

    `INTERVAL '-08:00' HOUR TO MINUTE`
    :   比 UTC 西邊 8 小時的時區（相當於
        PST）。

    `LOCAL`<br>`DEFAULT`
    :   將時區設為你本地的時區（也就是伺服器
        `timezone` 的預設值）。

    以數字或區間形式指定的時區設定，內部會轉換為 POSIX
    時區語法。舉例來說，執行
    `SET TIME ZONE -7` 之後，`SHOW TIME ZONE` 會
    回報 `<-07>+07`。

    `SET` 不支援時區縮寫；關於時區的更多資訊，
    請參閱[8.5.3 節](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-TIMEZONES)。

<a id="id-1.9.3.174.7"></a>

## 注意事項

函式 `set_config` 提供相同的功能；請參閱
[9.28.1 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SET)。
此外，也可以透過 UPDATE
[`pg_settings`](../../internals/views/view-pg-settings.md)
系統檢視表，達到與 `SET` 相同的效果。

<a id="id-1.9.3.174.8"></a>

## 範例

設定綱要搜尋路徑：

```

SET search_path TO my_schema, public;
```

將日期的顯示樣式設為傳統的
POSTGRES 格式，並採用「日先於月」的輸入慣例：

```

SET datestyle TO postgres, dmy;
```

設定加州柏克萊的時區：

```

SET TIME ZONE 'America/Los_Angeles';
```

設定義大利的時區：

```

SET TIME ZONE 'Europe/Rome';
```

<a id="id-1.9.3.174.9"></a>

## 相容性

`SET TIME ZONE` 擴充了 SQL 標準所定義的語法。
標準只允許以數字表示的時區偏移量，而
PostgreSQL 則允許更有彈性的
時區指定方式。其餘所有 `SET`
功能都是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.174.10"></a>

## 另請參閱

[RESET](sql-reset.md)、[SHOW](sql-show.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-set.html)（原文版本：18.6；核對日期：2026-09-28）
