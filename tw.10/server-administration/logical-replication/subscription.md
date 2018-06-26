---
description: 版本：10
---

# 31.2. 訂閱（Subscription）

訂閱是邏輯複寫的下游。訂閱的節點被稱為訂閱者。訂閱定義了與另一個資料庫以及它想要訂閱的一組或多組發佈（一個或多個）的連線。

訂閱資料庫的行為與任何其他 PostgreSQL 服務的行為相同，也可以透過定義自己的發佈來成為其他資料庫的發佈者。

如果需要，用戶節點可能有多個訂閱。在單個（發佈者 - 訂閱者）配對之間定義多個訂閱允許的，在這種情況下必須小心以確保訂閱的發佈對象不重疊。

每個訂閱都將透過一個複寫插槽（replication slot）接收變更（請參閱[第 26.2.6 節](../high-availability-load-balancing-and-replication/26.2.-log-shipping-standby-servers.md#26-2-6-replication-slots)）。額外的臨時複寫插槽可能需要用於預先存在的資料表資料才能開始初始化資料同步。

邏輯複寫訂閱可以是同步複寫的備用資料庫（請參閱[第 26.2.8 節](../high-availability-load-balancing-and-replication/26.2.-log-shipping-standby-servers.md#26-2-8-synchronous-replication)）。備用名稱預設為訂閱名稱。可以在訂閱的連線訊息中將另一個名稱以 application\_name 指定。

如果目前使用者是超級使用者，則 pg\_dump 會匯出訂閱的內容。否則會提示警告訊息並跳過訂閱內容，因為非超級使用者無法讀取 pg\_subscription 目錄中的訂閱訊息。

訂閱是使用 CREATE SUBSCRIPTION 加入的，可以隨時使用 ALTER SUBSCRIPTION 指令停止或恢復，並使用 DROP SUBSCRIPTION 移除訂閱。

When a subscription is dropped and recreated, the synchronization information is lost. This means that the data has to be resynchronized afterwards.

The schema definitions are not replicated, and the published tables must exist on the subscriber. Only regular tables may be the target of replication. For example, you can't replicate to a view.

The tables are matched between the publisher and the subscriber using the fully qualified table name. Replication to differently-named tables on the subscriber is not supported.

Columns of a table are also matched by name. A different order of columns in the target table is allowed, but the column types have to match. The target table can have additional columns not provided by the published table. Those will be filled with their default values.

#### 31.2.1. Replication Slot Management

As mentioned earlier, each \(active\) subscription receives changes from a replication slot on the remote \(publishing\) side. Normally, the remote replication slot is created automatically when the subscription is created using `CREATE SUBSCRIPTION` and it is dropped automatically when the subscription is dropped using `DROP SUBSCRIPTION`. In some situations, however, it can be useful or necessary to manipulate the subscription and the underlying replication slot separately. Here are some scenarios:

* When creating a subscription, the replication slot already exists. In that case, the subscription can be created using the `create_slot = false` option to associate with the existing slot.
* When creating a subscription, the remote host is not reachable or in an unclear state. In that case, the subscription can be created using the `connect = false` option. The remote host will then not be contacted at all. This is what pg\_dump uses. The remote replication slot will then have to be created manually before the subscription can be activated.
* When dropping a subscription, the replication slot should be kept. This could be useful when the subscriber database is being moved to a different host and will be activated from there. In that case, disassociate the slot from the subscription using `ALTER SUBSCRIPTION` before attempting to drop the subscription.
* When dropping a subscription, the remote host is not reachable. In that case, disassociate the slot from the subscription using `ALTER SUBSCRIPTION` before attempting to drop the subscription. If the remote database instance no longer exists, no further action is then necessary. If, however, the remote database instance is just unreachable, the replication slot should then be dropped manually; otherwise it would continue to reserve WAL and might eventually cause the disk to fill up. Such cases should be carefully investigated.

