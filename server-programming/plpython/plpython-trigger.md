<a id="PLPYTHON-TRIGGER"></a>

## 44.5. 觸發程序函式 [#](#PLPYTHON-TRIGGER)

<a id="id-1.8.11.13.2"></a>

當某個函式被用作觸發程序時，字典 `TD` 會包含與觸發程序相關的值：

`TD["event"]`
:   以字串形式包含事件：`INSERT`、`UPDATE`、`DELETE` 或 `TRUNCATE`。

`TD["when"]`
:   包含 `BEFORE`、`AFTER` 或 `INSTEAD OF` 其中之一。

`TD["level"]`
:   包含 `ROW` 或 `STATEMENT`。

`TD["new"]`<br>`TD["old"]`
:   對於資料列層級的觸發程序，依觸發事件而定，這兩個欄位中會有一個或兩個包含對應的觸發資料列。

`TD["name"]`
:   包含觸發程序的名稱。

`TD["table_name"]`
:   包含觸發程序所發生之資料表的名稱。

`TD["table_schema"]`
:   包含觸發程序所發生之資料表的綱要。

`TD["relid"]`
:   包含觸發程序所發生之資料表的 OID。

`TD["args"]`
:   如果 `CREATE TRIGGER` 指令中含有引數，可以在 `TD["args"][0]` 到 `TD["args"][n-1]` 取得它們。

如果 `TD["when"]` 是 `BEFORE` 或 `INSTEAD OF`，而且 `TD["level"]` 是 `ROW`，你可以從 Python 函式回傳 `None` 或 `"OK"` 表示該資料列未被修改，回傳 `"SKIP"` 以中止該事件；或者，若 `TD["event"]` 是 `INSERT` 或 `UPDATE`，你可以回傳 `"MODIFY"` 表示你已修改了新的資料列。除此之外的情況，回傳值都會被忽略。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-trigger.html)（原文版本：18.6；核對日期：2026-09-13）
