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

### 參數

_`subscription_name`_

新訂閱的名稱。

`CONNECTION '`_`conninfo`_'

發佈者的連線字串。有關詳細訊息，請參閱[第 33.1.1 節](../../client-interfaces/libpq-c-library/database-connection-control-functions.md#33-1-1-connection-strings)。

`PUBLICATION` _`publication_name`_

要訂閱的發佈者的發佈名稱。

`WITH (` _`subscription_parameter`_ \[= _`value`_\] \[, ... \] \)

此子句指定訂閱的選用參數。支援以下參數：

`copy_data` \(`boolean`\)

指定複寫開始後是否應複寫正在訂閱的發佈中的現有資料。預設值為 true。

`create_slot` \(`boolean`\)

指定指令是否應在發佈者上建立複寫插槽。預設值為 true。

`enabled` \(`boolean`\)

指定訂閱是應該主動複寫，還是應該只是設定而不啟動。預設值為 true。

`slot_name` \(`string`\)

要使用的複寫插槽的名稱。預設行為是使用插槽名稱的訂閱。

當 slot\_name 設定為 NONE 時，將不會有與該訂閱關聯的複寫插槽。如果稍後手動建立複寫插槽，則可以使用此方法。此類訂閱還必須同時啟用並且將 create\_slot 設定為 false。

`synchronous_commit` \(`enum`\)

此參數的值將覆寫 [synchronous\_commit ](../../server-administration/server-configuration/write-ahead-log.md#19-5-1-settings)設定。預設值為 off。

使用 off 進行邏輯複寫是安全的：如果訂閱戶因缺少同步而遺失事務，則資料將從發佈者重新發送。

執行同步邏寫複製時，可能需要使用其他設定。邏輯複寫工作程序向發佈者報告寫入和更新的位置，使用同步複寫時，發佈者將等待實際更新。這意味著在將訂閱用於同步複寫時將訂閱戶的 synchronous\_commit 設定為 off 可能會增加發佈伺服器上 COMMIT 的延遲。在這種情況下，將 synchronous\_commit 設定為 local 或更高的值可能更有利。

`connect` \(`boolean`\)

指定 CREATE SUBSCRIPTION 是否應該連線到發佈者。將此設定為 false 會將enabled、create\_slot 和 copy\_data 的預設值更改為 false。

不允許將 connect 設定為 false，卻將 enabled、create\_slot 或 copy\_data 設定為 true。

由於此選項設定為 false 時未建立連線，所以資料表未訂閱，而在您啟用訂閱後，將不會複寫任何內容。需要執行 ALTER SUBSCRIPTION ... REFRESH PUBLICATION 才能訂閱資料表。

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

