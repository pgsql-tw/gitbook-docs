<a id="LOGICAL-REPLICATION-CONFIG"></a>

## 29.12. 組態設定 [#](#LOGICAL-REPLICATION-CONFIG)

[29.12.1. 發布端](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-PUBLISHER)

[29.12.2. 訂閱端](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER)

邏輯複寫需要設定數個組態選項。這些選項僅與複寫的其中一側有關。

<a id="LOGICAL-REPLICATION-CONFIG-PUBLISHER"></a>

### 29.12.1. 發布端 [#](#LOGICAL-REPLICATION-CONFIG-PUBLISHER)

[`wal_level`](../runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL) 必須
設為 `logical`。

[`max_replication_slots`](../runtime-config/runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS)
必須設為至少等於預期會連線的訂閱數量，
再加上一些供資料表同步使用的預留量。

邏輯複寫插槽也會受到
[`idle_replication_slot_timeout`](../runtime-config/runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT)
的影響。

[`max_wal_senders`](../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)
應至少設為與
`max_replication_slots` 相同，
再加上同時連線的實體複寫端數量。

邏輯複寫的 walsender 也會受到
[`wal_sender_timeout`](../runtime-config/runtime-config-replication.md#GUC-WAL-SENDER-TIMEOUT)
的影響。

<a id="LOGICAL-REPLICATION-CONFIG-SUBSCRIBER"></a>

### 29.12.2. 訂閱端 [#](#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER)

[`max_active_replication_origins`](../runtime-config/runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS)
必須至少設為將加入至該訂閱端的訂閱數量，
再加上一些供資料表同步使用的預留量。

[`max_logical_replication_workers`](../runtime-config/runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS)
必須至少設為訂閱數量（供 leader apply
工作程序使用），再加上一些供資料表同步工作程序與
平行套用工作程序使用的預留量。

[`max_worker_processes`](../runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)
可能需要調整，以容納複寫工作程序，至少需為
([`max_logical_replication_workers`](../runtime-config/runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS)
+ `1`)。請注意，部分擴充套件與平行查詢
也會從 `max_worker_processes` 取用工作程序插槽。

[`max_sync_workers_per_subscription`](../runtime-config/runtime-config-replication.md#GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION)
用於控制訂閱初始化期間、或新增資料表時，
初始資料複製的平行處理程度。

[`max_parallel_apply_workers_per_subscription`](../runtime-config/runtime-config-replication.md#GUC-MAX-PARALLEL-APPLY-WORKERS-PER-SUBSCRIPTION)
用於控制在訂閱參數
`streaming = parallel` 下，
串流傳輸進行中交易的平行處理程度。

邏輯複寫工作程序也會受到
[`wal_receiver_timeout`](../runtime-config/runtime-config-replication.md#GUC-WAL-RECEIVER-TIMEOUT)、
[`wal_receiver_status_interval`](../runtime-config/runtime-config-replication.md#GUC-WAL-RECEIVER-STATUS-INTERVAL) 以及
[`wal_retrieve_retry_interval`](../runtime-config/runtime-config-replication.md#GUC-WAL-RETRIEVE-RETRY-INTERVAL)
的影響。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-config.html)（原文版本：18.6；核對日期：2026-09-24）
