<a id="LOGICAL-REPLICATION-FAILOVER"></a>

## 29.3. 邏輯複寫失效切換 [#](#LOGICAL-REPLICATION-FAILOVER)
為了讓訂閱端節點即使在發布端節點失效時，仍能持續從發布端複寫資料，
發布端節點必須對應有一個實體待命伺服器。透過在建立訂閱時指定
`failover = true`，可以將主要伺服器上、對應各訂閱的邏輯插槽
同步到待命伺服器。詳情請參閱
[第 47.2.3 節](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)。
啟用
[`failover`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
參數，可確保待命伺服器被提升之後，這些訂閱能夠順利轉換；
它們可以繼續訂閱新主要伺服器上的發布。

由於插槽同步邏輯是以非同步方式進行複製，因此在失效切換（failover）
發生之前，必須先確認複寫插槽已同步到待命伺服器。為確保失效切換順利成功，
待命伺服器的進度必須領先訂閱端。這可以透過設定
[`synchronized_standby_slots`](../runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS)
來達成。

若要確認待命伺服器針對某特定訂閱端，是否確實已準備好進行失效切換，
請依照以下步驟，驗證該訂閱端所需的所有邏輯複寫插槽，是否都已同步到
待命伺服器：

1. 在訂閱端節點上，使用以下 SQL 識別哪些複寫插槽，應該同步到我們打算
   提升的待命伺服器。這個查詢會傳回與已啟用 failover 的訂閱相關聯的
   複寫插槽。

   ```

   /* sub # */ SELECT
                  array_agg(quote_literal(s.subslotname)) AS slots
              FROM  pg_subscription s
              WHERE s.subfailover AND
                    s.subslotname IS NOT NULL;
    slots
   -------
    {'sub1','sub2','sub3'}
   (1 row)
   ```
2. 在訂閱端節點上，使用以下 SQL 識別哪些資料表同步插槽，應該同步到
   我們打算提升的待命伺服器。這個查詢需要在包含已啟用 failover 訂閱的
   每個資料庫上執行。請注意，只有在資料表複製已完成時
   （見[第 52.55 節](../../internals/catalogs/catalog-pg-subscription-rel.md)），
   資料表同步插槽才需要同步到待命伺服器。在其他情境中，我們不需要確保
   資料表同步插槽已同步，因為在那些情境下，它們最終會在新主要伺服器上
   被移除或重新建立。

   ```

   /* sub # */ SELECT
                  array_agg(quote_literal(slot_name)) AS slots
              FROM
              (
                  SELECT CONCAT('pg_', srsubid, '_sync_', srrelid, '_', ctl.system_identifier) AS slot_name
                  FROM pg_control_system() ctl, pg_subscription_rel r, pg_subscription s
                  WHERE r.srsubstate = 'f' AND s.oid = r.srsubid AND s.subfailover
              );
    slots
   -------
    {'pg_16394_sync_16385_7394666715149055164'}
   (1 row)
   ```
3. 檢查上面識別出的邏輯複寫插槽，是否存在於待命伺服器上，且已準備好
   進行失效切換。

   ```

   /* standby # */ SELECT slot_name, (synced AND NOT temporary AND invalidation_reason IS NULL) AS failover_ready
                  FROM pg_replication_slots
                  WHERE slot_name IN
                      ('sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164');
     slot_name                                 | failover_ready
   --------------------------------------------+----------------
     sub1                                      | t
     sub2                                      | t
     sub3                                      | t
     pg_16394_sync_16385_7394666715149055164   | t
   (4 rows)
   ```

如果上述所有插槽都存在於待命伺服器上，且上述 SQL 查詢的結果
（`failover_ready`）為 true，那麼現有的訂閱就可以繼續訂閱新主要伺服器
上的發布。

上述程序中的前兩個步驟，是針對 PostgreSQL 訂閱端而設計的。建議在失效
切換後、將由指定待命伺服器服務的每一個訂閱端節點上，都執行這些步驟，
以取得完整的複寫插槽清單；接著即可在步驟 3 中驗證此清單，以確認是否
已準備好進行失效切換。至於非 PostgreSQL 訂閱端，
則可以使用自己的方法，來識別其各自訂閱所使用的複寫插槽。

在某些情況下，例如進行計畫性的失效切換時，必須確認所有訂閱端——
不論是 PostgreSQL 或非 PostgreSQL——在失效切換到指定待命伺服器之後，
都能夠繼續複寫。在這種情況下，可以改用以下 SQL，來取代執行上述前兩個
步驟，以識別主要伺服器上有哪些複寫插槽，需要同步到打算提升的待命伺服器。
這個查詢會傳回與所有已啟用 failover 訂閱相關聯的複寫插槽。

```

/* primary # */ SELECT array_agg(quote_literal(r.slot_name)) AS slots
               FROM pg_replication_slots r
               WHERE r.failover AND NOT r.temporary;
 slots
-------
 {'sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164'}
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-failover.html)（原文版本：18.6；核對日期：2026-09-25）
