## 42.7. PL/Tcl 中的事件觸發器函式 [#](#PLTCL-EVENT-TRIGGER)

<a id="id-1.8.9.11.2"></a>

事件觸發器函式可以用 PL/Tcl 撰寫。PostgreSQL 要求作為事件觸發器呼叫的函式，必須宣告為不帶引數且回傳型別為 `event_trigger` 的函式。

觸發器管理器的資訊會透過下列變數傳入函式主體：

`$TG_event`
:   引發此觸發器的事件名稱。

`$TG_tag`
:   引發此觸發器的命令標籤。

觸發器函式的回傳值會被忽略。

以下是一個簡單的事件觸發器函式範例，每次執行受支援的命令時，都會發出一則 `NOTICE` 訊息：

```

CREATE OR REPLACE FUNCTION tclsnitch() RETURNS event_trigger AS $$
  elog NOTICE "tclsnitch: $TG_event $TG_tag"
$$ LANGUAGE pltcl;

CREATE EVENT TRIGGER tcl_a_snitch ON ddl_command_start EXECUTE FUNCTION tclsnitch();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-event-trigger.html)（原文版本：18.6；核對日期：2026-09-07）
