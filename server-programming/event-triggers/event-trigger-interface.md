<a id="EVENT-TRIGGER-INTERFACE"></a>
## 38.2. 以 C 撰寫事件觸發程序函式 [#](#EVENT-TRIGGER-INTERFACE)

<a id="id-1.8.5.6.2"></a>

本節說明事件觸發程序函式介面的底層細節。只有在以 C 撰寫事件觸發程序函式時，才需要這些資訊。如果你使用的是較高階的語言，這些細節就會由該語言替你處理。在大多數情況下，你應該考慮先使用程序語言，而不是直接以 C 撰寫事件觸發程序。每種程序語言各自的文件，都說明了如何以該語言撰寫事件觸發程序。

事件觸發程序函式必須使用「第一版」函式管理器介面。

當函式被事件觸發程序管理器呼叫時，不會傳入任何一般引數，而是會傳入一個指向 `EventTriggerData` 結構的「上下文」指標。C 函式可以透過執行以下巨集，來檢查自己是否是被事件觸發程序管理器呼叫的：

```

CALLED_AS_EVENT_TRIGGER(fcinfo)
```

這個巨集會展開為：

```

((fcinfo)->context != NULL && IsA((fcinfo)->context, EventTriggerData))
```

如果這個結果為真，那麼就可以安全地把 `fcinfo->context` 轉型為 `EventTriggerData *` 型別，並使用它所指向的 `EventTriggerData` 結構。函式*不可*變更 `EventTriggerData` 結構，或它所指向的任何資料。

`struct EventTriggerData` 定義於 `commands/event_trigger.h` 中：

```

typedef struct EventTriggerData
{
    NodeTag     type;
    const char *event;      /* event name */
    Node       *parsetree;  /* parse tree */
    CommandTag  tag;        /* command tag */
} EventTriggerData;
```

其中各成員的定義如下：

`type`
:   永遠是 `T_EventTriggerData`。

`event`
:   描述呼叫該函式所對應的事件，可以是 `"login"`、`"ddl_command_start"`、`"ddl_command_end"`、`"sql_drop"`、`"table_rewrite"` 其中之一。這些事件的意義請參閱[第 38.1 節](event-trigger-definition.md)。

`parsetree`
:   指向該命令剖析樹的指標。詳情請查閱 PostgreSQL 原始碼。剖析樹的結構可能隨時變更，恕不另行通知。

`tag`
:   與執行該事件觸發程序之事件相關聯的命令標籤，例如 `"CREATE FUNCTION"`。

事件觸發程序函式必須回傳一個 `NULL` 指標（*不是* SQL 空值，也就是說，不要把 *`isNull`* 設為 true）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-trigger-interface.html)（原文版本：18.6；核對日期：2026-09-15）
