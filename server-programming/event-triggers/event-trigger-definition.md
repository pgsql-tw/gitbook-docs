<a id="EVENT-TRIGGER-DEFINITION"></a>
## 38.1. 事件觸發程序行為概觀 [#](#EVENT-TRIGGER-DEFINITION)

[38.1.1. login](event-trigger-definition.md#EVENT-TRIGGER-LOGIN)

[38.1.2. ddl_command_start](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)

[38.1.3. ddl_command_end](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)

[38.1.4. sql_drop](event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)

[38.1.5. table_rewrite](event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)

[38.1.6. 中止交易中的事件觸發程序](event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

[38.1.7. 建立事件觸發程序](event-trigger-definition.md#EVENT-TRIGGER-CREATING)

當事件觸發程序所關聯的事件，在其所定義的資料庫中發生時，該事件觸發程序便會被觸發。目前支援的事件有
`login`、
`ddl_command_start`、
`ddl_command_end`、
`table_rewrite`
以及 `sql_drop`。
未來版本可能會加入對其他事件的支援。

<a id="EVENT-TRIGGER-LOGIN"></a>

### 38.1.1. login [#](#EVENT-TRIGGER-LOGIN)

`login` 事件會在已通過驗證的使用者登入系統時發生。此事件的觸發程序若有任何錯誤，都可能導致無法成功登入系統。這類錯誤可透過在連線字串或組態檔中，將 [event_triggers](../../server-administration/runtime-config/runtime-config-client.md#GUC-EVENT-TRIGGERS) 設為 `false` 來加以規避。或者，您也可以將系統以單使用者模式重新啟動（因為事件觸發程序在此模式下會被停用）。關於使用單使用者模式的詳情，請參閱 [postgres](../../reference/reference-server/app-postgres.md) 參考頁面。
`login` 事件也會在待命伺服器上觸發。為避免伺服器變得無法存取，這類觸發程序在待命伺服器上執行時，必須避免對資料庫寫入任何內容。此外，建議避免在 `login` 事件觸發程序中執行長時間執行的查詢。請注意，舉例來說，在 psql 中取消連線，並不會取消正在進行中的 `login` 觸發程序。

關於如何使用 `login` 事件觸發程序的範例，請見[38.5 節](event-trigger-database-login-example.md)。

<a id="EVENT-TRIGGER-DDL_COMMAND_START"></a>

### 38.1.2. ddl_command_start [#](#EVENT-TRIGGER-DDL_COMMAND_START)

`ddl_command_start` 事件會在執行 DDL 命令之前緊接著發生。在此語境下，DDL 命令是指：

* `CREATE`
* `ALTER`
* `DROP`
* `COMMENT`
* `GRANT`
* `IMPORT FOREIGN SCHEMA`
* `REINDEX`
* `REFRESH MATERIALIZED VIEW`
* `REVOKE`
* `SECURITY LABEL`

`ddl_command_start` 也會在執行 `SELECT INTO`
命令之前緊接著發生，因為這與 `CREATE TABLE AS`
是等效的。

例外情況是，對於以共用物件為目標的 DDL 命令，此事件不會發生：

* 資料庫
* 角色（角色定義與角色成員關係）
* 資料表空間
* 參數權限
* `ALTER SYSTEM`

對於以事件觸發程序本身為目標的命令，此事件也不會發生。

在事件觸發程序被觸發之前，並不會檢查受影響的物件是否存在。

<a id="EVENT-TRIGGER-DDL_COMMAND_END"></a>

### 38.1.3. ddl_command_end [#](#EVENT-TRIGGER-DDL_COMMAND_END)

`ddl_command_end` 事件會在執行與
`ddl_command_start` 相同的一組命令之後緊接著發生。若要取得所發生 DDL
操作的更多細節，可在 `ddl_command_end` 事件觸發程序程式碼中，使用傳回集合函式
`pg_event_trigger_ddl_commands()`（見[9.30 節](../../the-sql-language/functions/functions-event-triggers.md)）。請注意，此觸發程序是在相關動作已經發生之後（但交易尚未提交之前）才觸發，因此讀取系統目錄時，會看到已經變更後的內容。

<a id="EVENT-TRIGGER-SQL_DROP"></a>

### 38.1.4. sql_drop [#](#EVENT-TRIGGER-SQL_DROP)

`sql_drop` 事件會在任何刪除資料庫物件的操作，其
`ddl_command_end` 事件觸發程序執行之前緊接著發生。請注意，除了明顯的
`DROP` 命令之外，某些 `ALTER`
命令也可能觸發 `sql_drop` 事件。

若要列出已被刪除的物件，可在 `sql_drop`
事件觸發程序程式碼中，使用傳回集合函式
`pg_event_trigger_dropped_objects()`（見[9.30 節](../../the-sql-language/functions/functions-event-triggers.md)）。請注意，此觸發程序是在物件已從系統目錄中刪除之後才會執行，因此屆時已無法再查詢這些物件。

<a id="EVENT-TRIGGER-TABLE_REWRITE"></a>

### 38.1.5. table_rewrite [#](#EVENT-TRIGGER-TABLE_REWRITE)

`table_rewrite` 事件會在資料表因
`ALTER TABLE` 與 `ALTER TYPE`
命令的某些動作而被重寫之前緊接著發生。雖然還有其他控制陳述式可用來重寫資料表，例如
`CLUSTER` 與 `VACUUM`，但
`table_rewrite` 事件並不會被這些命令觸發。
若要找出被重寫資料表的 OID，可使用函式
`pg_event_trigger_table_rewrite_oid()`；若要得知重寫的原因，可使用函式
`pg_event_trigger_table_rewrite_reason()`（見[9.30 節](../../the-sql-language/functions/functions-event-triggers.md)）。

<a id="EVENT-TRIGGER-ABORTED-TRANSACTIONS"></a>

### 38.1.6. 中止交易中的事件觸發程序 [#](#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

事件觸發程序（如同其他函式）無法在已中止的交易中執行。因此，若某個 DDL 命令因錯誤而失敗，任何相關聯的
`ddl_command_end` 觸發程序都不會被執行。反之，若某個
`ddl_command_start` 觸發程序因錯誤而失敗，則不會再觸發後續的任何事件觸發程序，也不會嘗試執行該命令本身。同樣地，若某個
`ddl_command_end` 觸發程序因錯誤而失敗，該 DDL 陳述式所造成的效果將會被回復，就如同在任何其他導致所在交易中止的情況下一樣。

<a id="EVENT-TRIGGER-CREATING"></a>

### 38.1.7. 建立事件觸發程序 [#](#EVENT-TRIGGER-CREATING)

事件觸發程序是使用 [CREATE EVENT TRIGGER](../../reference/sql-commands/sql-createeventtrigger.md) 命令建立的。若要建立事件觸發程序，您必須先建立一個傳回型別為特殊型別
`event_trigger` 的函式。此函式不需要（也不可以）傳回值；此傳回型別僅作為一種訊號，表示該函式將以事件觸發程序的形式被呼叫。

若針對特定事件定義了一個以上的事件觸發程序，它們將依觸發程序名稱的字母順序依序觸發。

觸發程序定義也可以指定 `WHEN`
條件，例如讓 `ddl_command_start`
觸發程序只在使用者想要攔截的特定命令上觸發。這類觸發程序常見的用途，是用來限制使用者可執行的 DDL 操作範圍。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-trigger-definition.html)（原文版本：18.6；核對日期：2026-09-15）
