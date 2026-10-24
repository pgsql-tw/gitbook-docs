<a id="SQL-CREATESUBSCRIPTION"></a><a id="id-1.9.3.84.1"></a>

## CREATE SUBSCRIPTION

CREATE SUBSCRIPTION — 定義新的訂閱

<a id="id-1.9.3.84.4"></a>

## 語法

```

CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]
```

<a id="id-1.9.3.84.5"></a>

## 說明

`CREATE SUBSCRIPTION` 會新增一個邏輯複寫訂閱。建立訂閱的使用者會成為該訂閱的擁有者。訂閱名稱必須與目前資料庫中任何現有訂閱的名稱不同。

訂閱代表一條連到發佈者的複寫連線。因此，除了在本機系統目錄中新增定義之外，此命令通常還會在發佈者上建立一個複寫插槽。

除非訂閱一開始就是停用狀態，否則在執行此命令的交易提交時，會啟動一個邏輯複寫工作程序，為新的訂閱複寫資料。

要能建立訂閱，你必須具有 `pg_create_subscription` 角色的權限，以及目前資料庫上的 `CREATE` 權限。

關於訂閱以及邏輯複寫整體的更多資訊，請參閱[第 29.2 節](../../server-administration/logical-replication/logical-replication-subscription.md)與[第 29 章](../../server-administration/logical-replication/README.md)。

<a id="id-1.9.3.84.6"></a>

## 參數

<a id="SQL-CREATESUBSCRIPTION-PARAMS-NAME"></a>

*`subscription_name`* [#](#SQL-CREATESUBSCRIPTION-PARAMS-NAME)
:   新訂閱的名稱。
<a id="SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION"></a>

`CONNECTION 'conninfo'` [#](#SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION)
:   定義如何連線到發佈者資料庫的 libpq 連線字串。詳情請參閱[第 32.1.1 節](../../client-interfaces/libpq/libpq-connect.md#libpq-connstring)。
<a id="SQL-CREATESUBSCRIPTION-PARAMS-PUBLICATION"></a>

`PUBLICATION publication_name [, ...]` [#](#SQL-CREATESUBSCRIPTION-PARAMS-PUBLICATION)
:   發佈者上要訂閱的發佈名稱。
<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH"></a>

`WITH ( subscription_parameter [= value] [, ... ] )` [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH)
:   此子句指定訂閱的選用參數。

    下列參數控制建立訂閱期間會發生的事：

    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-CONNECT"></a>

    `connect` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-CONNECT)
    :   指定 `CREATE SUBSCRIPTION` 命令究竟是否應該連線到發佈者。預設為 `true`。將此參數設為 `false` 會強制將 `create_slot`、`enabled` 與 `copy_data` 的值設為 `false`。（你不能在將 `connect` 設為 `false` 的同時，將 `create_slot`、`enabled` 或 `copy_data` 設為 `true`。）

        由於此選項為 `false` 時不會建立任何連線，因此不會訂閱任何資料表。要開始複寫，你必須手動建立複寫插槽、視需要啟用失效切換、啟用訂閱，並重新整理訂閱。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-CREATE-SLOT"></a>

    `create_slot` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-CREATE-SLOT)
    :   指定此命令是否應該在發佈者上建立複寫插槽。預設為 `true`。

        若設為 `false`，你就必須負責以其他方式建立發佈者上的插槽。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-ENABLED"></a>

    `enabled` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ENABLED)
    :   指定訂閱應該主動進行複寫，或者只應該完成設定而尚不啟動。預設為 `true`。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME"></a>

    `slot_name` (`string`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME)
    :   要使用的發佈者複寫插槽名稱。預設是使用訂閱的名稱作為插槽名稱。

        將 `slot_name` 設為 `NONE` 表示不會有任何複寫插槽與此訂閱相關聯。這類訂閱也必須將 `enabled` 與 `create_slot` 都設為 `false`。當你之後將手動建立複寫插槽時，請使用此設定。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。

        當 `slot_name` 設為有效的名稱且 `create_slot` 設為 `false` 時，所指名插槽的 `failover` 屬性值，可能與訂閱中所指定的對應 `failover` 參數不同。務必確保插槽屬性 `failover` 與訂閱的對應參數相符，反之亦然。否則，發佈者上的插槽行為可能與這些訂閱選項所述的不同：例如，即使訂閱的 `failover` 選項已停用，發佈者上的插槽仍可能被同步到備用伺服器；或者即使訂閱的 `failover` 選項已啟用，發佈者上的插槽也可能被停用同步。

    下列參數控制訂閱建立之後的複寫行為：

    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY"></a>

    `binary` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY)
    :   指定訂閱是否要請求發佈者以二進位格式（而非文字格式）傳送資料。預設為 `false`。任何初始資料表同步複製（請參閱 `copy_data`）也會使用相同的格式。二進位格式可能比文字格式快，但在不同機器架構與 PostgreSQL 版本之間的可攜性較差。二進位格式與資料型別高度相關；例如，它不允許從 `smallint` 欄位複製到 `integer` 欄位，即使這在文字格式下可以正常運作。即使啟用此選項，也只有具備二進位傳送與接收函式的資料型別才會以二進位傳輸。請注意，初始同步要求所有資料型別都具備二進位傳送與接收函式，否則同步將會失敗（關於傳送／接收函式的更多資訊，請參閱 [CREATE TYPE](sql-createtype.md)）。

        進行跨版本複寫時，可能會出現發佈者對某個資料型別具有二進位傳送函式，但訂閱者缺少該型別之二進位接收函式的情況。在這種情況下，資料傳輸將會失敗，且無法使用 `binary` 選項。

        若發佈者是 PostgreSQL 16 之前的版本，則即使 `binary = true`，任何初始資料表同步都會使用文字格式。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA"></a>

    `copy_data` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA)
    :   指定在複寫開始時，是否要複製所訂閱之發佈中既有的資料。預設為 `true`。

        若發佈包含 `WHERE` 子句，將會影響要複製哪些資料。詳情請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。

        關於 `copy_data = true` 可能如何與 `origin` 參數交互作用的細節，請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING"></a>

    `streaming` (`enum`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING)
    :   指定是否為此訂閱啟用進行中交易的串流。預設值為 `parallel`，表示傳入的變更會在有可用的平行套用工作程序時，直接透過其中一個平行套用工作程序套用。若沒有空閒的平行套用工作程序可以處理串流交易，變更會先寫入暫存檔，並在交易提交之後才套用。請注意，若平行套用工作程序中發生錯誤，遠端交易的結束 LSN 可能不會被回報到伺服器日誌中。

        <a id="id-1.9.3.84.6.2.4.2.5.3.2.2"></a>

        ### 小心

        當發佈者與訂閱者的綱要不同時，存在發生死結的風險，不過這種情況很少見。套用工作程序具備自動重試這些交易的能力。

        若設為 `on`，傳入的變更會先寫入暫存檔，並且只在交易於發佈者上提交且被訂閱者接收之後才套用。

        若設為 `off`，所有交易都會先在發佈者上完整解碼，然後才整體傳送給訂閱者。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT"></a>

    `synchronous_commit` (`enum`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT)
    :   此參數的值會覆寫此訂閱之套用工作程序中的 [synchronous_commit](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) 設定。預設值為 `off`。

        對邏輯複寫使用 `off` 是安全的：若訂閱者因為缺少同步而遺失交易，資料會由發佈者再次傳送。

        進行同步邏輯複寫時，其他設定可能較為合適。邏輯複寫工作程序會向發佈者回報寫入與刷寫的位置，而使用同步複寫時，發佈者會等待實際的刷寫。這表示當訂閱用於同步複寫時，將訂閱者的 `synchronous_commit` 設為 `off` 可能會增加發佈者上 `COMMIT` 的延遲。在這種情境下，將 `synchronous_commit` 設為 `local` 或更高可能較有利。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE"></a>

    `two_phase` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
    :   指定是否為此訂閱啟用兩階段提交。預設為 `false`。

        啟用兩階段提交時，預備交易會在 `PREPARE TRANSACTION` 時傳送給訂閱者，並且在訂閱者上也以兩階段交易的方式處理。否則，預備交易只會在提交時才傳送給訂閱者，然後由訂閱者立即處理。

        兩階段提交的實作要求複寫已成功完成初始資料表同步階段。因此，即使某個訂閱已啟用 `two_phase`，內部的兩階段狀態仍會暫時維持在「pending」，直到初始化階段完成為止。要得知實際的兩階段狀態，請參閱 [`pg_subscription`](../../internals/catalogs/catalog-pg-subscription.md) 的 `subtwophasestate` 欄位。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR"></a>

    `disable_on_error` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR)
    :   指定在從發佈者複寫資料期間，若訂閱工作程序偵測到任何錯誤，是否應該自動停用該訂閱。預設為 `false`。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED"></a>

    `password_required` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED)
    :   若設為 `true`，因此訂閱而建立的發佈者連線必須使用密碼身分驗證，而且密碼必須作為連線字串的一部分來指定。當訂閱由超級使用者擁有時，此設定會被忽略。預設為 `true`。只有超級使用者可以將此值設為 `false`。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER"></a>

    `run_as_owner` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER)
    :   若為 true，所有複寫動作都會以訂閱擁有者的身分執行。若為 false，複寫工作程序會以各資料表擁有者的身分，對該資料表執行動作。後一種設定通常安全得多；詳情請參閱[第 29.11 節](../../server-administration/logical-replication/logical-replication-security.md)。預設為 `false`。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN"></a>

    `origin` (`string`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN)
    :   指定訂閱是要請求發佈者只傳送沒有來源（origin）的變更，還是不論來源都傳送變更。將 `origin` 設為 `none` 表示訂閱將請求發佈者只傳送沒有來源的變更。將 `origin` 設為 `any` 表示發佈者不論變更的來源為何都會傳送。預設為 `any`。

        關於 `copy_data = true` 可能如何與 `origin` 參數交互作用的細節，請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。
    <a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER"></a>

    `failover` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
    :   指定與此訂閱相關聯的複寫插槽是否啟用同步到備用伺服器，以便在失效切換之後，能從新的主要伺服器繼續進行邏輯複寫。預設為 `false`。

指定 `boolean` 型別的參數時，可以省略 `=` *`value`* 部分，這等同於指定 `TRUE`。

<a id="SQL-CREATESUBSCRIPTION-NOTES"></a>

## 注意事項

關於如何設定訂閱與發佈執行個體之間的存取控制，詳情請參閱[第 29.11 節](../../server-administration/logical-replication/logical-replication-security.md)。

建立複寫插槽時（預設行為），`CREATE SUBSCRIPTION` 不能在交易區塊內執行。

建立連線到同一個資料庫叢集的訂閱（例如，在同一叢集中的資料庫之間複寫，或在同一個資料庫內複寫），只有在複寫插槽不是作為同一個命令的一部分建立時才會成功。否則，`CREATE SUBSCRIPTION` 呼叫將會停滯。要讓這種做法可行，請另外建立複寫插槽（使用函式 `pg_create_logical_replication_slot`，外掛名稱為 `pgoutput`），並使用參數 `create_slot = false` 建立訂閱。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)。這是實作上的限制，未來的版本中可能會解除。

若發佈中的任何資料表具有 `WHERE` 子句，則 *`expression`* 求值結果為 `false` 或 `NULL` 的資料列將不會被發佈。若訂閱具有多個發佈，而同一個資料表在其中以不同的 `WHERE` 子句發佈，則只要任一運算式（針對該發佈操作）被滿足，資料列就會被發佈。在 `WHERE` 子句不同的情況下，若其中一個發佈沒有 `WHERE` 子句（針對該發佈操作），或該發佈被宣告為 [`FOR ALL TABLES`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 或 [`FOR TABLES IN SCHEMA`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)，則不論其他運算式的定義為何，資料列一律會被發佈。若訂閱者是 PostgreSQL 15 之前的版本，則在初始資料同步階段會忽略所有資料列過濾。在這種情況下，使用者可能會想考慮刪除任何與後續過濾不相容的初始複製資料。由於初始資料同步在複製既有資料表資料時，不會考慮發佈的 [`publish`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) 參數，因此可能會複製到一些使用 DML 時不會被複寫的資料列。範例請參閱[第 29.2.2 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)。

不支援具有多個發佈、且同一個資料表在其中以不同欄位清單發佈的訂閱。

我們允許指定不存在的發佈，以便使用者之後再加入它們。這表示 [`pg_subscription`](../../internals/catalogs/catalog-pg-subscription.md) 可能包含不存在的發佈。

使用 `copy_data = true` 與 `origin = NONE` 的訂閱參數組合時，初始同步的資料表資料是直接從發佈者複製的，這表示無法得知該資料的真正來源。若發佈者本身也有訂閱，則複製的資料表資料可能源自更上游。此情境會被偵測到，並向使用者記錄一則 WARNING，但該警告只是潛在問題的提示；確認所複製資料的來源是否確實符合預期，並進行必要的檢查，是使用者的責任。

要找出哪些資料表可能包含非本機來源（由於在發佈者上建立的其他訂閱），請嘗試以下 SQL 查詢：

```

# substitute <pub-names> below with your publication name(s) to be queried
SELECT DISTINCT PT.schemaname, PT.tablename
FROM pg_publication_tables PT
     JOIN pg_class C ON (C.relname = PT.tablename)
     JOIN pg_namespace N ON (N.nspname = PT.schemaname),
     pg_subscription_rel PS
WHERE C.relnamespace = N.oid AND
      (PS.srrelid = C.oid OR
      C.oid IN (SELECT relid FROM pg_partition_ancestors(PS.srrelid) UNION
                SELECT relid FROM pg_partition_tree(PS.srrelid))) AND
      PT.pubname IN (<pub-names>);
```

<a id="id-1.9.3.84.8"></a>

## 範例

建立一個連到遠端伺服器的訂閱，複寫發佈 `mypublication` 與 `insert_only` 中的資料表，並在提交時立即開始複寫：

```

CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;
```

建立一個連到遠端伺服器的訂閱，複寫 `insert_only` 發佈中的資料表，且在之後被啟用之前不開始複寫。

```

CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);
```

<a id="id-1.9.3.84.9"></a>

## 相容性

`CREATE SUBSCRIPTION` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.84.10"></a>

## 另請參閱

[ALTER SUBSCRIPTION](sql-altersubscription.md), [DROP SUBSCRIPTION](sql-dropsubscription.md), [CREATE PUBLICATION](sql-createpublication.md), [ALTER PUBLICATION](sql-alterpublication.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createsubscription.html)（原文版本：18.6；核對日期：2026-10-04）
