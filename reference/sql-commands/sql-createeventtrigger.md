<a id="SQL-CREATEEVENTTRIGGER"></a><a id="id-1.9.3.63.1"></a>

## CREATE EVENT TRIGGER

CREATE EVENT TRIGGER — 定義新的事件觸發程序

<a id="id-1.9.3.63.4"></a>

## 語法

```

CREATE EVENT TRIGGER name
    ON event
    [ WHEN filter_variable IN (filter_value [, ... ]) [ AND ... ] ]
    EXECUTE { FUNCTION | PROCEDURE } function_name()
```

<a id="id-1.9.3.63.5"></a>

## 說明

`CREATE EVENT TRIGGER` 會建立新的事件觸發程序。每當指定的事件發生，且與該觸發程序相關聯的 `WHEN` 條件（若有的話）獲得滿足時，就會執行觸發程序函式。關於事件觸發程序的一般介紹，請參閱[第 38 章](../../server-programming/event-triggers/README.md)。建立事件觸發程序的使用者會成為其擁有者。

<a id="id-1.9.3.63.6"></a>

## 參數

*`name`*
:   要賦予新觸發程序的名稱。此名稱在資料庫內必須是唯一的。

*`event`*
:   觸發呼叫指定函式之事件的名稱。關於事件名稱的更多資訊，請參閱[第 38.1 節](../../server-programming/event-triggers/event-trigger-definition.md)。

*`filter_variable`*
:   用來篩選事件之變數的名稱。這讓你可以將觸發程序的觸發限制在它所支援之情況的一個子集。目前唯一支援的
    *`filter_variable`*
    是 `TAG`。

*`filter_value`*
:   相關聯之 *`filter_variable`* 的值清單，觸發程序應該針對這些值觸發。對 `TAG` 而言，這表示命令標籤的清單（例如 `'DROP FUNCTION'`）。

*`function_name`*

使用者提供的函式，宣告為不接受任何引數，並傳回 `event_trigger` 型別。

在 `CREATE EVENT TRIGGER` 的語法中，關鍵字 `FUNCTION` 與 `PROCEDURE` 是等價的，但所參照的函式無論如何都必須是函式，而不是程序。此處使用關鍵字 `PROCEDURE` 是歷史因素，且已不建議使用。

<a id="SQL-CREATEEVENTTRIGGER-NOTES"></a>

## 注意事項

只有超級使用者可以建立事件觸發程序。

事件觸發程序在單一使用者模式中會停用（請參閱 [postgres](../reference-server/app-postgres.md)），在 [event_triggers](../../server-administration/runtime-config/runtime-config-client.md#GUC-EVENT-TRIGGERS) 設為 `false` 時也會停用。若某個有錯誤的事件觸發程序使資料庫嚴重失常，甚至讓你無法移除該觸發程序，請將 [event_triggers](../../server-administration/runtime-config/runtime-config-client.md#GUC-EVENT-TRIGGERS) 設為 `false` 以暫時停用事件觸發程序後重新啟動，或以單一使用者模式重新啟動，就能夠移除它。

<a id="SQL-CREATEEVENTTRIGGER-EXAMPLES"></a>

## 範例

禁止執行任何 [DDL](../../the-sql-language/ddl/README.md) 命令：

```

CREATE OR REPLACE FUNCTION abort_any_command()
  RETURNS event_trigger
 LANGUAGE plpgsql
  AS $$
BEGIN
  RAISE EXCEPTION 'command % is disabled', tg_tag;
END;
$$;

CREATE EVENT TRIGGER abort_ddl ON ddl_command_start
   EXECUTE FUNCTION abort_any_command();
```

<a id="SQL-CREATEEVENTTRIGGER-COMPATIBILITY"></a>

## 相容性

SQL 標準中沒有 `CREATE EVENT TRIGGER` 陳述式。

<a id="id-1.9.3.63.10"></a>

## 另請參閱

[ALTER EVENT TRIGGER](sql-altereventtrigger.md), [DROP EVENT TRIGGER](sql-dropeventtrigger.md), [CREATE FUNCTION](sql-createfunction.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createeventtrigger.html)（原文版本：18.6；核對日期：2026-10-04）
