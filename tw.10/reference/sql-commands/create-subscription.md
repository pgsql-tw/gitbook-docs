---
description: 版本：10
---

# CREATE SUBSCRIPTION

CREATE SUBSCRIPTION — 定義一個新的訂閱

### 語法

```text
CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]
```

### 說明

CREATE SUBSCRIPTION 為目前資料庫加上一個新的訂閱。訂閱名稱必須與資料庫中任何現有訂閱的名稱相異。

訂閱表示與發佈者的複寫連線。因此，此指令不僅可以在本地中增加定義，還可以在發佈者上建立複寫插槽。

將在運行此指令的交易事務提交時啟動邏輯複寫工作程序以複寫新訂閱的資料。

有關訂閱和邏輯複寫完整的訊息，請參閱[第 31.2 節](../../server-administration/31.-luo-ji-fu-xie-logical-replication/31.2.-ding-yue-subscription.md)和[第 31 章](../../server-administration/31.-luo-ji-fu-xie-logical-replication/)。

### Parameters

_`subscription_name`_

The name of the new subscription.

`CONNECTION '`_`conninfo`_'

The connection string to the publisher. For details see [Section 33.1.1](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNSTRING).

`PUBLICATION` _`publication_name`_

Names of the publications on the publisher to subscribe to.

`WITH (` _`subscription_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional parameters for a subscription. The following parameters are supported:

`copy_data` \(`boolean`\)

Specifies whether the existing data in the publications that are being subscribed to should be copied once the replication starts. The default is `true`.

`create_slot` \(`boolean`\)

Specifies whether the command should create the replication slot on the publisher. The default is `true`.

`enabled` \(`boolean`\)

Specifies whether the subscription should be actively replicating, or whether it should be just setup but not started yet. The default is `true`.

`slot_name` \(`string`\)

Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name.

When `slot_name` is set to `NONE`, there will be no replication slot associated with the subscription. This can be used if the replication slot will be created later manually. Such subscriptions must also have both `enabled` and `create_slot` set to `false`.

`synchronous_commit` \(`enum`\)

The value of this parameter overrides the [synchronous\_commit](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) setting. The default value is `off`.

It is safe to use `off` for logical replication: If the subscriber loses transactions because of missing synchronization, the data will be resent from the publisher.

A different setting might be appropriate when doing synchronous logical replication. The logical replication workers report the positions of writes and flushes to the publisher, and when using synchronous replication, the publisher will wait for the actual flush. This means that setting `synchronous_commit` for the subscriber to `off` when the subscription is used for synchronous replication might increase the latency for `COMMIT` on the publisher. In this scenario, it can be advantageous to set `synchronous_commit` to `local` or higher.

`connect` \(`boolean`\)

Specifies whether the `CREATE SUBSCRIPTION` should connect to the publisher at all. Setting this to `false` will change default values of `enabled`, `create_slot` and `copy_data` to `false`.

It is not allowed to combine `connect` set to `false` and `enabled`, `create_slot`, or `copy_data` set to `true`.

Since no connection is made when this option is set to `false`, the tables are not subscribed, and so after you enable the subscription nothing will be replicated. It is required to run `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` in order for tables to be subscribed.

### 注意

有關如何在訂閱和發佈的服服之間配置存取控制的詳細訊息，請參閱[第 31.7 節](../../server-administration/31.-luo-ji-fu-xie-logical-replication/31.7.-an-quan-xing.md)。

建立複寫插槽時（預設行為），CREATE SUBSCRIPTION 不能在交易事務區塊內執行。

建立連線到同一資料庫叢集的訂閱（例如，在同一叢集中的資料庫之間進行複寫或在同一資料庫中進行複寫）只有在複寫插槽未作為同一指令的一部分建立時才會成功。否則，CREATE SUBSCRIPTION 呼叫將失敗。要使其順利運作，請單獨建立複寫插槽（使用函數 pg\_create\_logical\_replication\_slot，套件名稱為 pgoutput），並使用參數 create\_slot = false 建立訂閱。這是一個可能在將來的版本中解除的實作限制。

### 範例

建立遠端伺服器的訂閱，將複寫 mypublication 和 insert\_only 資料表，並在提交時立即開始複寫：

```text
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;
```

建立對於遠端伺服器的訂閱，將複寫 insert\_only 資料表，並且在稍後啟用之前不會開始複寫。

```text
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);
```

### 相容性

CREATE SUBSCRIPTION 是 PostgreSQL 的延伸功能。

### 參閱

[ALTER SUBSCRIPTION](alter-subscription.md), [DROP SUBSCRIPTION](drop-subscription.md), [CREATE PUBLICATION](create-publication.md), [ALTER PUBLICATION](alter-publication.md)

