<a id="LOGICAL-REPLICATION-CONFLICTS"></a>

## 29.7. 衝突 [#](#LOGICAL-REPLICATION-CONFLICTS)

邏輯複寫的行為與一般 DML 操作類似：即使資料在訂閱端本機已被變更，
資料仍然會被更新。若接收到的資料違反任何限制條件，複寫就會停止。
這種情況稱為*衝突（conflict）*。在複寫 `UPDATE` 或
`DELETE` 操作時，資料缺失同樣會被視為
*衝突*，但不會導致錯誤，這類操作只會被單純地略過。

在下列*衝突*情境中，會觸發額外的日誌記錄，並收集衝突統計資訊
（顯示於
[`pg_stat_subscription_stats`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS) 檢視表中）：

<a id="CONFLICT-INSERT-EXISTS"></a>

`insert_exists` [#](#CONFLICT-INSERT-EXISTS)
:   插入的資料列違反了 `NOT DEFERRABLE`
    唯一值限制條件。請注意，若要記錄衝突鍵值的來源與提交
    時間戳記細節，訂閱端必須啟用
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)。
    在這種情況下，會持續回報錯誤，直到該衝突被手動解決為止。
<a id="CONFLICT-UPDATE-ORIGIN-DIFFERS"></a>

`update_origin_differs` [#](#CONFLICT-UPDATE-ORIGIN-DIFFERS)
:   更新了先前由其他來源修改過的資料列。請注意，只有在
    訂閱端啟用
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    時，才能偵測到這種衝突。目前，無論本機資料列的來源為何，
    更新一律都會被套用。
<a id="CONFLICT-UPDATE-EXISTS"></a>

`update_exists` [#](#CONFLICT-UPDATE-EXISTS)
:   資料列更新後的值違反了 `NOT DEFERRABLE`
    唯一值限制條件。請注意，若要記錄衝突鍵值的來源與提交
    時間戳記細節，訂閱端必須啟用
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)。
    在這種情況下，會持續回報錯誤，直到該衝突被手動解決為止。另請注意，
    在更新分割表時，若更新後的資料列值符合另一個分割區的
    限制條件，導致該資料列被插入到新的分割區中，而新資料列若違反
    `NOT DEFERRABLE` 唯一值限制條件，就可能出現
    `insert_exists` 衝突。
<a id="CONFLICT-UPDATE-MISSING"></a>

`update_missing` [#](#CONFLICT-UPDATE-MISSING)
:   找不到要更新的資料列。在這種情況下，更新會被直接略過。
<a id="CONFLICT-DELETE-ORIGIN-DIFFERS"></a>

`delete_origin_differs` [#](#CONFLICT-DELETE-ORIGIN-DIFFERS)
:   刪除了先前由其他來源修改過的資料列。請注意，只有在
    訂閱端啟用
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    時，才能偵測到這種衝突。目前，無論本機資料列的來源為何，
    刪除一律都會被套用。
<a id="CONFLICT-DELETE-MISSING"></a>

`delete_missing` [#](#CONFLICT-DELETE-MISSING)
:   找不到要刪除的資料列。在這種情況下，刪除會被直接略過。
<a id="CONFLICT-MULTIPLE-UNIQUE-CONFLICTS"></a>

`multiple_unique_conflicts` [#](#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS)
:   插入或更新資料列違反了多個
    `NOT DEFERRABLE` 唯一值限制條件。請注意，為了記錄
    各個衝突鍵值的來源與提交時間戳記細節，請確保訂閱端已啟用
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)。
    在這種情況下，會持續回報錯誤，直到
    該衝突被手動解決為止。

請注意，還有其他的衝突情境，例如排他（exclusion）限制條件
違反。目前，我們並未在日誌中為這些情境提供額外的細節。

邏輯複寫衝突的日誌格式如下：

```

LOG:  conflict detected on relation "schemaname.tablename": conflict=conflict_type
DETAIL:  detailed_explanation.
{detail_values [; ... ]}.

where detail_values is one of:

    Key (column_name [, ...])=(column_value [, ...])
    existing local row [(column_name [, ...])=](column_value [, ...])
    remote row [(column_name [, ...])=](column_value [, ...])
    replica identity {(column_name [, ...])=(column_value [, ...]) | full [(column_name [, ...])=](column_value [, ...])}
```

日誌提供了以下資訊：

`LOG`
:   * *`schemaname`*.*`tablename`*
      標示出發生衝突所涉及的本機關聯（relation）。
    * *`conflict_type`* 是發生的衝突類型
      （例如 `insert_exists`、`update_exists`）。

`DETAIL`
:   * *`detailed_explanation`* 包含
      修改該既有本機資料列的交易的來源、交易 ID 與提交時間戳記
      （若有的話）。
    * `Key` 區段包含違反唯一值限制條件的本機
      資料列鍵值，適用於
      `insert_exists`、`update_exists` 或
      `multiple_unique_conflicts` 衝突。
    * `existing local row` 區段包含本機
      資料列，適用於以下情況：其來源與遠端資料列不同，適用於
      `update_origin_differs` 或 `delete_origin_differs`
      衝突；或者其鍵值與遠端資料列衝突，適用於
      `insert_exists`、`update_exists` 或
      `multiple_unique_conflicts` 衝突。
    * `remote row` 區段包含造成衝突的遠端
      插入或更新操作所帶來的新資料列。請注意，
      對於更新操作，若新資料列的欄位值未變更且已被 toast，
      則該欄位值會顯示為 null。
    * `replica identity` 區段包含用來搜尋
      待更新或待刪除之既有本機資料列時所使用的複本識別
      （replica identity）鍵值。若本機關聯標記為
      [`REPLICA IDENTITY FULL`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL)，
      這裡可能會包含完整的資料列值。
    * *`column_name`* 是欄位名稱。
      對於 `existing local row`、`remote row`
      與 `replica identity full` 的情況，只有在使用者
      沒有權限存取資料表所有欄位時，才會記錄欄位名稱。若有記錄欄位名稱，
      它們出現的順序會與對應的欄位值相同。
    * *`column_value`* 是欄位值。
      過大的欄位值會被截斷為 64 個位元組。
    * 請注意，在 `multiple_unique_conflicts` 衝突的情況下，
      會產生多行 *`detailed_explanation`*
      與 *`detail_values`*，
      分別詳述與各個不同唯一值限制條件相關的衝突資訊。

邏輯複寫操作是以擁有該訂閱的角色（role）之權限來執行。若目標
資料表發生權限失敗，會導致複寫衝突；若目標資料表已啟用
[資料列層級安全性（row-level security）](../../the-sql-language/ddl/ddl-rowsecurity.md)，
且訂閱擁有者受其規範，也同樣會導致複寫衝突，無論該政策
原本是否會拒絕正在複寫的 `INSERT`、
`UPDATE`、`DELETE` 或
`TRUNCATE` 操作皆然。此項針對資料列層級安全性的限制，
未來版本的 PostgreSQL 有可能會解除。

產生錯誤的衝突會使複寫停止；必須由使用者手動解決該衝突。
關於該衝突的詳細資訊，可以在訂閱端的伺服器日誌中找到。

解決方式可以是變更訂閱端上的資料或權限，使其不再與傳入的變更
發生衝突，也可以是略過與既有資料發生衝突的該筆交易。當衝突
產生錯誤時，複寫不會繼續進行，邏輯複寫工作程序會在訂閱端的
伺服器日誌中發出下列類型的訊息：

```

ERROR:  conflict detected on relation "public.test": conflict=insert_exists
DETAIL:  Key already exists in unique index "t_pkey", which was modified locally in transaction 740 at 2024-06-26 10:47:04.727375+08.
Key (c)=(1); existing local row (1, 'local'); remote row (1, 'remote').
CONTEXT:  processing remote data for replication origin "pg_16395" during "INSERT" for replication target relation "public.test" in transaction 725 finished at 0/14C0378
```

違反限制條件之變更所屬交易的 LSN，以及複寫來源名稱，都可以從伺服器日誌中
找到（在上例中為 LSN 0/14C0378 與複寫來源
`pg_16395`）。你可以使用
[`ALTER SUBSCRIPTION ... SKIP`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP)
搭配結束 LSN（finish LSN）
（即 LSN 0/14C0378）來略過造成衝突的交易。結束 LSN 可以是該交易
在發布端上提交或準備妥當（prepared）時所對應的 LSN。此外，
也可以透過呼叫
[`pg_replication_origin_advance()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE)
函式來略過該交易。在使用這個函式之前，需要先透過
[`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)
暫時停用該訂閱，或者該訂閱也可以搭配使用
[`disable_on_error`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR)
選項。接著，你就可以使用 *`node_name`*（即
`pg_16395`）與結束 LSN 的下一個 LSN（即 0/14C0379），
來呼叫 `pg_replication_origin_advance()`
函式。各個來源目前的位置，可以在
[`pg_replication_origin_status`](../../internals/views/view-pg-replication-origin-status.md)
系統檢視表中查看。請注意，略過整筆交易時，也會一併略過該交易中
原本不會違反任何限制條件的變更。這很容易讓訂閱端資料變得不一致。
關於衝突資料列的其他細節，例如其來源與提交時間戳記，
可以在日誌的 `DETAIL` 行中看到。但請注意，
只有在訂閱端啟用
[`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
時，才能取得這項資訊。使用者可以利用這項資訊，來決定要保留
本機的變更，還是採用遠端的變更。舉例來說，上述日誌中的
`DETAIL` 行顯示，既有的資料列是在本機被修改的。
使用者可以手動選擇讓遠端變更生效。

當
[`streaming`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING)
模式為 `parallel` 時，失敗交易的結束 LSN 可能不會被
記錄下來。在這種情況下，可能需要將串流模式改為
`on` 或 `off`，並重新觸發相同的
衝突，讓該失敗交易的結束 LSN 得以寫入伺服器日誌中。關於結束 LSN
的用法，請參見 [`ALTER SUBSCRIPTION ...
SKIP`](../../reference/sql-commands/sql-altersubscription.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-conflicts.html)（原文版本：18.6；核對日期：2026-09-25）
