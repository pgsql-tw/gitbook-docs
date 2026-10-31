# CREATE SUBSCRIPTION 訂閱參數

[返回 CREATE SUBSCRIPTION](sql-createsubscription.md)

下列參數控制建立訂閱期間會發生的事：

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-CONNECT"></a>

## `connect` (`boolean`) [#](#sql-createsubscription-params-with-connect) <a href="#sql-createsubscription-params-with-connect" id="sql-createsubscription-params-with-connect"></a>

指定 `CREATE SUBSCRIPTION` 命令究竟是否應該連線到發佈者。預設為 `true`。將此參數設為 `false` 會強制將 `create_slot`、`enabled` 與 `copy_data` 的值設為 `false`。（你不能在將 `connect` 設為 `false` 的同時，將 `create_slot`、`enabled` 或 `copy_data` 設為 `true`。）

由於此選項為 `false` 時不會建立任何連線，因此不會訂閱任何資料表。要開始複寫，你必須手動建立複寫插槽、視需要啟用失效切換、啟用訂閱，並重新整理訂閱。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-CREATE-SLOT"></a>

## `create_slot` (`boolean`) [#](#sql-createsubscription-params-with-create-slot) <a href="#sql-createsubscription-params-with-create-slot" id="sql-createsubscription-params-with-create-slot"></a>

指定此命令是否應該在發佈者上建立複寫插槽。預設為 `true`。

若設為 `false`，你就必須負責以其他方式建立發佈者上的插槽。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-ENABLED"></a>

## `enabled` (`boolean`) [#](#sql-createsubscription-params-with-enabled) <a href="#sql-createsubscription-params-with-enabled" id="sql-createsubscription-params-with-enabled"></a>

指定訂閱應該主動進行複寫，或者只應該完成設定而尚不啟動。預設為 `true`。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME"></a>

## `slot_name` (`string`) [#](#sql-createsubscription-params-with-slot-name) <a href="#sql-createsubscription-params-with-slot-name" id="sql-createsubscription-params-with-slot-name"></a>

要使用的發佈者複寫插槽名稱。預設是使用訂閱的名稱作為插槽名稱。

將 `slot_name` 設為 `NONE` 表示不會有任何複寫插槽與此訂閱相關聯。這類訂閱也必須將 `enabled` 與 `create_slot` 都設為 `false`。當你之後將手動建立複寫插槽時，請使用此設定。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。

當 `slot_name` 設為有效的名稱且 `create_slot` 設為 `false` 時，所指名插槽的 `failover` 屬性值，可能與訂閱中所指定的對應 `failover` 參數不同。務必確保插槽屬性 `failover` 與訂閱的對應參數相符，反之亦然。否則，發佈者上的插槽行為可能與這些訂閱選項所述的不同：例如，即使訂閱的 `failover` 選項已停用，發佈者上的插槽仍可能被同步到備用伺服器；或者即使訂閱的 `failover` 選項已啟用，發佈者上的插槽也可能被停用同步。

下列參數控制訂閱建立之後的複寫行為：

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY"></a>

## `binary` (`boolean`) [#](#sql-createsubscription-params-with-binary) <a href="#sql-createsubscription-params-with-binary" id="sql-createsubscription-params-with-binary"></a>

指定訂閱是否要請求發佈者以二進位格式（而非文字格式）傳送資料。預設為 `false`。任何初始資料表同步複製（請參閱 `copy_data`）也會使用相同的格式。二進位格式可能比文字格式快，但在不同機器架構與 PostgreSQL 版本之間的可攜性較差。二進位格式與資料型別高度相關；例如，它不允許從 `smallint` 欄位複製到 `integer` 欄位，即使這在文字格式下可以正常運作。即使啟用此選項，也只有具備二進位傳送與接收函式的資料型別才會以二進位傳輸。請注意，初始同步要求所有資料型別都具備二進位傳送與接收函式，否則同步將會失敗（關於傳送／接收函式的更多資訊，請參閱 [CREATE TYPE](sql-createtype.md)）。

進行跨版本複寫時，可能會出現發佈者對某個資料型別具有二進位傳送函式，但訂閱者缺少該型別之二進位接收函式的情況。在這種情況下，資料傳輸將會失敗，且無法使用 `binary` 選項。

若發佈者是 PostgreSQL 16 之前的版本，則即使 `binary = true`，任何初始資料表同步都會使用文字格式。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA"></a>

## `copy_data` (`boolean`) [#](#sql-createsubscription-params-with-copy-data) <a href="#sql-createsubscription-params-with-copy-data" id="sql-createsubscription-params-with-copy-data"></a>

指定在複寫開始時，是否要複製所訂閱之發佈中既有的資料。預設為 `true`。

若發佈包含 `WHERE` 子句，將會影響要複製哪些資料。詳情請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。

關於 `copy_data = true` 可能如何與 `origin` 參數交互作用的細節，請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING"></a>

## `streaming` (`enum`) [#](#sql-createsubscription-params-with-streaming) <a href="#sql-createsubscription-params-with-streaming" id="sql-createsubscription-params-with-streaming"></a>

指定是否為此訂閱啟用進行中交易的串流。預設值為 `parallel`，表示傳入的變更會在有可用的平行套用工作程序時，直接透過其中一個平行套用工作程序套用。若沒有空閒的平行套用工作程序可以處理串流交易，變更會先寫入暫存檔，並在交易提交之後才套用。請注意，若平行套用工作程序中發生錯誤，遠端交易的結束 LSN 可能不會被回報到伺服器日誌中。

<a id="id-1.9.3.84.6.2.4.2.5.3.2.2"></a>

### 注意 [#](#sql-createsubscription-streaming-caution) <a href="#sql-createsubscription-streaming-caution" id="sql-createsubscription-streaming-caution"></a>

{% hint style="warning" %}
當發佈者與訂閱者的綱要不同時，存在發生死結的風險，不過這種情況很少見。套用工作程序具備自動重試這些交易的能力。
{% endhint %}

若設為 `on`，傳入的變更會先寫入暫存檔，並且只在交易於發佈者上提交且被訂閱者接收之後才套用。

若設為 `off`，所有交易都會先在發佈者上完整解碼，然後才整體傳送給訂閱者。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT"></a>

## `synchronous_commit` (`enum`) [#](#sql-createsubscription-params-with-synchronous-commit) <a href="#sql-createsubscription-params-with-synchronous-commit" id="sql-createsubscription-params-with-synchronous-commit"></a>

此參數的值會覆寫此訂閱之套用工作程序中的 [synchronous_commit](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) 設定。預設值為 `off`。

對邏輯複寫使用 `off` 是安全的：若訂閱者因為缺少同步而遺失交易，資料會由發佈者再次傳送。

進行同步邏輯複寫時，其他設定可能較為合適。邏輯複寫工作程序會向發佈者回報寫入與刷寫的位置，而使用同步複寫時，發佈者會等待實際的刷寫。這表示當訂閱用於同步複寫時，將訂閱者的 `synchronous_commit` 設為 `off` 可能會增加發佈者上 `COMMIT` 的延遲。在這種情境下，將 `synchronous_commit` 設為 `local` 或更高可能較有利。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE"></a>

## `two_phase` (`boolean`) [#](#sql-createsubscription-params-with-two-phase) <a href="#sql-createsubscription-params-with-two-phase" id="sql-createsubscription-params-with-two-phase"></a>

指定是否為此訂閱啟用兩階段提交。預設為 `false`。

啟用兩階段提交時，預備交易會在 `PREPARE TRANSACTION` 時傳送給訂閱者，並且在訂閱者上也以兩階段交易的方式處理。否則，預備交易只會在提交時才傳送給訂閱者，然後由訂閱者立即處理。

兩階段提交的實作要求複寫已成功完成初始資料表同步階段。因此，即使某個訂閱已啟用 `two_phase`，內部的兩階段狀態仍會暫時維持在「pending」，直到初始化階段完成為止。要得知實際的兩階段狀態，請參閱 [`pg_subscription`](../../internals/catalogs/catalog-pg-subscription.md) 的 `subtwophasestate` 欄位。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR"></a>

## `disable_on_error` (`boolean`) [#](#sql-createsubscription-params-with-disable-on-error) <a href="#sql-createsubscription-params-with-disable-on-error" id="sql-createsubscription-params-with-disable-on-error"></a>

指定在從發佈者複寫資料期間，若訂閱工作程序偵測到任何錯誤，是否應該自動停用該訂閱。預設為 `false`。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED"></a>

## `password_required` (`boolean`) [#](#sql-createsubscription-params-with-password-required) <a href="#sql-createsubscription-params-with-password-required" id="sql-createsubscription-params-with-password-required"></a>

若設為 `true`，因此訂閱而建立的發佈者連線必須使用密碼身分驗證，而且密碼必須作為連線字串的一部分來指定。當訂閱由超級使用者擁有時，此設定會被忽略。預設為 `true`。只有超級使用者可以將此值設為 `false`。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER"></a>

## `run_as_owner` (`boolean`) [#](#sql-createsubscription-params-with-run-as-owner) <a href="#sql-createsubscription-params-with-run-as-owner" id="sql-createsubscription-params-with-run-as-owner"></a>

若為 true，所有複寫動作都會以訂閱擁有者的身分執行。若為 false，複寫工作程序會以各資料表擁有者的身分，對該資料表執行動作。後一種設定通常安全得多；詳情請參閱[第 29.11 節](../../server-administration/logical-replication/logical-replication-security.md)。預設為 `false`。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN"></a>

## `origin` (`string`) [#](#sql-createsubscription-params-with-origin) <a href="#sql-createsubscription-params-with-origin" id="sql-createsubscription-params-with-origin"></a>

指定訂閱是要請求發佈者只傳送沒有來源（origin）的變更，還是不論來源都傳送變更。將 `origin` 設為 `none` 表示訂閱將請求發佈者只傳送沒有來源的變更。將 `origin` 設為 `any` 表示發佈者不論變更的來源為何都會傳送。預設為 `any`。

關於 `copy_data = true` 可能如何與 `origin` 參數交互作用的細節，請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。

<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER"></a>

## `failover` (`boolean`) [#](#sql-createsubscription-params-with-failover) <a href="#sql-createsubscription-params-with-failover" id="sql-createsubscription-params-with-failover"></a>

指定與此訂閱相關聯的複寫插槽是否啟用同步到備用伺服器，以便在失效切換之後，能從新的主要伺服器繼續進行邏輯複寫。預設為 `false`。

[返回 CREATE SUBSCRIPTION](sql-createsubscription.md)

---

本頁內容由父頁分出，沿用其原文版本與核對日期。

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createsubscription.html)（原文版本：18.6；核對日期：2026-10-04）
