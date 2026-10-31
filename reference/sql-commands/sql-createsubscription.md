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
:   定義如何連線到發佈者資料庫的 libpq 連線字串。詳情請參閱[第 32.1.1 節](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。
<a id="SQL-CREATESUBSCRIPTION-PARAMS-PUBLICATION"></a>

`PUBLICATION publication_name [, ...]` [#](#SQL-CREATESUBSCRIPTION-PARAMS-PUBLICATION)
:   發佈者上要訂閱的發佈名稱。
<a id="SQL-CREATESUBSCRIPTION-PARAMS-WITH"></a>

`WITH ( subscription_parameter [= value] [, ... ] )` [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH)

此子句指定訂閱的選用參數。

[訂閱參數與其警示說明](sql-createsubscription-parameters.md)

指定 `boolean` 型別的參數時，可以省略 `=` *`value`* 部分，這等同於指定 `TRUE`。

<a id="SQL-CREATESUBSCRIPTION-NOTES"></a>

## 注意事項

關於如何設定訂閱與發佈執行個體之間的存取控制，詳情請參閱[第 29.11 節](../../server-administration/logical-replication/logical-replication-security.md)。

建立複寫插槽時（預設行為），`CREATE SUBSCRIPTION` 不能在交易區塊內執行。

建立連線到同一個資料庫叢集的訂閱（例如，在同一叢集中的資料庫之間複寫，或在同一個資料庫內複寫），只有在複寫插槽不是作為同一個命令的一部分建立時才會成功。否則，`CREATE SUBSCRIPTION` 呼叫將會停滯。要讓這種做法可行，請另外建立複寫插槽（使用函式 `pg_create_logical_replication_slot`，外掛名稱為 `pgoutput`），並使用參數 `create_slot = false` 建立訂閱。範例請參閱[第 29.2.3 節](../../server-administration/logical-replication/logical-replication-subscription.md#logical-replication-subscription-examples-deferred-slot)。這是實作上的限制，未來的版本中可能會解除。

若發佈中的任何資料表具有 `WHERE` 子句，則 *`expression`* 求值結果為 `false` 或 `NULL` 的資料列將不會被發佈。若訂閱具有多個發佈，而同一個資料表在其中以不同的 `WHERE` 子句發佈，則只要任一運算式（針對該發佈操作）被滿足，資料列就會被發佈。在 `WHERE` 子句不同的情況下，若其中一個發佈沒有 `WHERE` 子句（針對該發佈操作），或該發佈被宣告為 [`FOR ALL TABLES`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 或 [`FOR TABLES IN SCHEMA`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)，則不論其他運算式的定義為何，資料列一律會被發佈。若訂閱者是 PostgreSQL 15 之前的版本，則在初始資料同步階段會忽略所有資料列過濾。在這種情況下，使用者可能會想考慮刪除任何與後續過濾不相容的初始複製資料。由於初始資料同步在複製既有資料表資料時，不會考慮發佈的 [`publish`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) 參數，因此可能會複製到一些使用 DML 時不會被複寫的資料列。範例請參閱[第 29.2.2 節](../../server-administration/logical-replication/logical-replication-subscription.md#logical-replication-subscription-examples)。

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
