<a id="EVENT-TRIGGER-EXAMPLE"></a>
## 38.3. 完整的事件觸發程序範例 [#](#EVENT-TRIGGER-EXAMPLE)

以下是一個以 C 撰寫的非常簡單的事件觸發程序函式範例。（以程序語言撰寫的觸發程序範例，可以在各程序語言各自的文件中找到。）

函式 `noddl` 每次被呼叫時都會拋出一個例外。這個事件觸發程序的定義，把該函式與 `ddl_command_start` 事件關聯起來。其效果就是所有 DDL 命令（除了[第 38.1 節](event-trigger-definition.md)中提到的例外情況）都會被阻止執行。

以下是該觸發程序函式的原始碼：

```

#include "postgres.h"

#include "commands/event_trigger.h"
#include "fmgr.h"

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(noddl);

Datum
noddl(PG_FUNCTION_ARGS)
{
    EventTriggerData *trigdata;

    if (!CALLED_AS_EVENT_TRIGGER(fcinfo))  /* internal error */
        elog(ERROR, "not fired by event trigger manager");

    trigdata = (EventTriggerData *) fcinfo->context;

    ereport(ERROR,
            (errcode(ERRCODE_INSUFFICIENT_PRIVILEGE),
             errmsg("command \"%s\" denied",
                    GetCommandTagName(trigdata->tag))));

    PG_RETURN_NULL();
}
```

編譯完原始碼之後（見[第 36.10.5 節](../extend/xfunc-c.md#DFUNC)），宣告函式與觸發程序：

```

CREATE FUNCTION noddl() RETURNS event_trigger
    AS 'noddl' LANGUAGE C;

CREATE EVENT TRIGGER noddl ON ddl_command_start
    EXECUTE FUNCTION noddl();
```

現在你可以測試這個觸發程序的運作：

```

=# \dy
                     List of event triggers
 Name  |       Event       | Owner | Enabled | Function | Tags
-------+-------------------+-------+---------+----------+------
 noddl | ddl_command_start | dim   | enabled | noddl    |
(1 row)

=# CREATE TABLE foo(id serial);
ERROR:  command "CREATE TABLE" denied
```

在這種情況下，如果你需要能夠執行某些 DDL 命令，就必須刪除該事件觸發程序，或是將它停用。你也可以只在某個交易期間停用該觸發程序，這樣會比較方便：

```

BEGIN;
ALTER EVENT TRIGGER noddl DISABLE;
CREATE TABLE foo (id serial);
ALTER EVENT TRIGGER noddl ENABLE;
COMMIT;
```

（回想一下，事件觸發程序本身的 DDL 命令，並不會受到事件觸發程序的影響。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-trigger-example.html)（原文版本：18.6；核對日期：2026-09-15）
