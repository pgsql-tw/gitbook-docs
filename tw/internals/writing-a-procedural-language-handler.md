# 55. 撰寫程序語言的處理程序

使用目前編譯語言的「version 1」介面以外的語言撰寫的函數（包括使用者定義的程序語言函數和用 SQL 撰寫的函數）在被呼叫時，都將透過特定語言的呼叫處理程序函數。呼叫處理程序有責任以有意義的方式執行功能，例如透過解譯程式原始碼。本章概述如何撰寫新程序語言的呼叫處理程序。

程序語言的呼叫處理程序是「一般」函數，必須使用「version 1」介面以編譯語言（例如 C）撰寫，並在 PostgreSQL 中註冊為不帶任何參數且回傳 language\_handler 型別。這種特殊的偽型別將函數標識為呼叫處理程序，並防止在 SQL 指令中直接呼叫該函數。有關 C 語言呼叫約定和動態載入的更多詳細訊，請參閱[第 37.10 節](../server-programming/extending-sql/c-language-functions.md)。

呼叫處理程序的呼叫方式與其他任何函數相同：它會接收到一個指向 FunctionCallInfoBaseData 結構的指標，該結構包含參數值和有關被呼叫函數的資訊，並且期待回傳 Datum 結果（也可能設定 FunctionCallInfoBaseData 結構中 isnull 的欄位，如果該函數希望回傳 SQL NULL 的結果）。呼叫處理程序和普通被呼叫函數之間的區別在於 FunctionCallInfoBaseData 結構的 flinfo-&gt;fn\_oid 欄位會包含要呼叫實際函數的 OID，而不包含呼叫處理程序本身的 OID。呼叫處理程序必須使用此欄位來決定所要執行的功能。同樣地，傳遞的參數列表是根據目標函數而不是呼叫處理程序的宣告設定。

呼叫處理程序要從 pg\_proc 系統目錄中取得函數的項目，並分析被呼叫函數的參數和回傳型別。該函數的 CREATE FUNCTION 命令的 AS 子句可以在 pg\_proc 行的 prosrc 欄位中看到。這通常是程序語言的原始碼，但是從理論上說，它也可能是其他內容，例如檔案的路徑名稱，或告訴呼叫處理程序詳細操作的其他任何內容。

通常，每個 SQL 語句會多次呼叫同一函數。 呼叫處理程序可以透過使用 flinfo-&gt;fn\_extra 欄位來避免重複查詢有關被呼叫函數的資訊。最初將為 NULL，但可以由呼叫處理程序設定為指向有關被呼叫函數的資訊。在後續的呼叫中，如果 flinfo-&gt;fn\_extra 已經為非 NULL，則可以使用它，並且跳過資訊查詢步驟。呼叫處理程序必須確保使 flinfo-&gt;fn\_extra 指向至少可以保存到目前查詢結束的快取，因為 FmgrInfo 資料結構可以保留那麼長時間。一種方法是在 flinfo-&gt;fn\_mcxt 指定的快取內容中分配額外的資料。此類資料通常與 FmgrInfo 本身俱有相同的壽命。但是處理程序還可以選擇使用壽命更長的快取，以便它可以跨查詢快取函數定義資訊。

當將程序語言函數作為事件觸發器呼叫時，不會以通常的方式傳遞任何參數，但是 FunctionCallInfoBaseData 的 context 欄位指向 TriggerData 結構，而不是像在普通函數呼叫中那樣為 NULL。語言處理程序應提供程序語言函數的機制，以取得所觸發資訊。

This is a template for a procedural-language handler written in C:

```text
#include "postgres.h"
#include "executor/spi.h"
#include "commands/trigger.h"
#include "fmgr.h"
#include "access/heapam.h"
#include "utils/syscache.h"
#include "catalog/pg_proc.h"
#include "catalog/pg_type.h"

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(plsample_call_handler);

Datum
plsample_call_handler(PG_FUNCTION_ARGS)
{
    Datum          retval;

    if (CALLED_AS_TRIGGER(fcinfo))
    {
        /*
         * Called as a trigger function
         */
        TriggerData    *trigdata = (TriggerData *) fcinfo->context;

        retval = ...
    }
    else
    {
        /*
         * Called as a function
         */

        retval = ...
    }

    return retval;
}
```

Only a few thousand lines of code have to be added instead of the dots to complete the call handler.

After having compiled the handler function into a loadable module \(see [Section 37.10.5](https://www.postgresql.org/docs/12/xfunc-c.html#DFUNC)\), the following commands then register the sample procedural language:

```text
CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS 'filename'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

Although providing a call handler is sufficient to create a minimal procedural language, there are two other functions that can optionally be provided to make the language more convenient to use. These are a _validator_ and an _inline handler_. A validator can be provided to allow language-specific checking to be done during [CREATE FUNCTION](https://www.postgresql.org/docs/12/sql-createfunction.html). An inline handler can be provided to allow the language to support anonymous code blocks executed via the [DO](https://www.postgresql.org/docs/12/sql-do.html) command.

If a validator is provided by a procedural language, it must be declared as a function taking a single parameter of type `oid`. The validator's result is ignored, so it is customarily declared to return `void`. The validator will be called at the end of a `CREATE FUNCTION` command that has created or updated a function written in the procedural language. The passed-in OID is the OID of the function's `pg_proc` row. The validator must fetch this row in the usual way, and do whatever checking is appropriate. First, call `CheckFunctionValidatorAccess()` to diagnose explicit calls to the validator that the user could not achieve through `CREATE FUNCTION`. Typical checks then include verifying that the function's argument and result types are supported by the language, and that the function's body is syntactically correct in the language. If the validator finds the function to be okay, it should just return. If it finds an error, it should report that via the normal `ereport()` error reporting mechanism. Throwing an error will force a transaction rollback and thus prevent the incorrect function definition from being committed.

Validator functions should typically honor the [check\_function\_bodies](https://www.postgresql.org/docs/12/runtime-config-client.html#GUC-CHECK-FUNCTION-BODIES) parameter: if it is turned off then any expensive or context-sensitive checking should be skipped. If the language provides for code execution at compilation time, the validator must suppress checks that would induce such execution. In particular, this parameter is turned off by pg\_dump so that it can load procedural language functions without worrying about side effects or dependencies of the function bodies on other database objects. \(Because of this requirement, the call handler should avoid assuming that the validator has fully checked the function. The point of having a validator is not to let the call handler omit checks, but to notify the user immediately if there are obvious errors in a `CREATE FUNCTION` command.\) While the choice of exactly what to check is mostly left to the discretion of the validator function, note that the core `CREATE FUNCTION` code only executes `SET` clauses attached to a function when `check_function_bodies` is on. Therefore, checks whose results might be affected by GUC parameters definitely should be skipped when `check_function_bodies` is off, to avoid false failures when reloading a dump.

If an inline handler is provided by a procedural language, it must be declared as a function taking a single parameter of type `internal`. The inline handler's result is ignored, so it is customarily declared to return `void`. The inline handler will be called when a `DO` statement is executed specifying the procedural language. The parameter actually passed is a pointer to an `InlineCodeBlock` struct, which contains information about the `DO` statement's parameters, in particular the text of the anonymous code block to be executed. The inline handler should execute this code and return.

It's recommended that you wrap all these function declarations, as well as the `CREATE LANGUAGE` command itself, into an _extension_ so that a simple `CREATE EXTENSION` command is sufficient to install the language. See [Section 37.17](https://www.postgresql.org/docs/12/extend-extensions.html) for information about writing extensions.

The procedural languages included in the standard distribution are good references when trying to write your own language handler. Look into the `src/pl` subdirectory of the source tree. The [CREATE LANGUAGE](https://www.postgresql.org/docs/12/sql-createlanguage.html) reference page also has some useful details.

