# CREATE SUBSCRIPTION

CREATE SUBSCRIPTION — 定義一個新的訂閱

### 語法

```
CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]
```

### 說明

CREATE SUBSCRIPTION 為目前資料庫加上一個新的訂閱。訂閱名稱必須與資料庫中任何現有訂閱的名稱相異。

訂閱表示與發佈者的複寫連線。因此，此指令不僅可以在本地中增加定義，還可以在發佈者上建立複寫插槽。

將在運行此指令的交易事務提交時啟動邏輯複寫工作程序以複寫新訂閱的資料。

若要建立一個 subscription，必須具有 pg\_create\_subscription 角色的授權，以及對目前資料庫的 CREATE 授權。

有關訂閱和邏輯複寫完整的訊息，請參閱[第 31.2 節](../../server-administration/logical-replication/subscription.md)和[第 31 章](../../server-administration/logical-replication/)。

### 參數

_`subscription_name`_

新訂閱的名稱。

`CONNECTION '`_`conninfo`_'

發佈者的連線字串。有關詳細訊息，請參閱[第 33.1.1 節](../../client-interfaces/libpq-c-library/database-connection-control-functions.md#33-1-1-connection-strings)。

`PUBLICATION`` `_`publication_name`_

要訂閱的發佈者的發佈名稱。

`WITH (`` `_`subscription_parameter`_ \[= _`value`_] \[, ... ] )

此子句指定訂閱的選用參數。支援以下參數：

`connect` (`boolean`) [#](https://www.postgresql.org/docs/current/sql-createsubscription.html#SQL-CREATESUBSCRIPTION-WITH-CONNECT)

指定 CREATE SUBSCRIPTION 是否應該連線到發佈者。將此設定為 false 會將enabled、create\_slot 和 copy\_data 的預設值更改為 false。

不允許將 connect 設定為 false，卻將 enabled、create\_slot 或 copy\_data 設定為 true。

由於此選項設定為 false 時未建立連線，所以資料表未訂閱，而在您啟用訂閱後，將不會複寫任何內容。若要啟動複製，必須手動立建複寫槽，啟用訂閱，然後更新訂閱。相關範例，請參閱 [31.2.3](../../server-administration/logical-replication/subscription.md#id-31.2.2.-examples)。

`create_slot` (`boolean`)

指定指令是否應在發佈者上建立複寫插槽。預設值為 true。

`enabled` (`boolean`)

指定訂閱是應該主動複寫，還是應該只是設定而不啟動。預設值為 true。

`slot_name` (`string`)

要使用的複寫插槽的名稱。預設行為是使用插槽名稱的訂閱。

當 slot\_name 設定為 NONE 時，將不會有與該訂閱關聯的複寫插槽。如果稍後手動建立複寫插槽，則可以使用此方法。此類訂閱還必須同時啟用並且將 create\_slot 設定為 false。

`binary` (`boolean`)&#x20;

Specifies whether the subscription will request the publisher to send the data in binary format (as opposed to text). The default is `false`. Any initial table synchronization copy (see `copy_data`) also uses the same format. Binary format can be faster than the text format, but it is less portable across machine architectures and PostgreSQL versions. Binary format is very data type specific; for example, it will not allow copying from a `smallint` column to an `integer` column, even though that would work fine in text format. Even when this option is enabled, only data types having binary send and receive functions will be transferred in binary. Note that the initial synchronization requires all data types to have binary send and receive functions, otherwise the synchronization will fail (see [CREATE TYPE](https://www.postgresql.org/docs/current/sql-createtype.html) for more about send/receive functions).

When doing cross-version replication, it could be that the publisher has a binary send function for some data type, but the subscriber lacks a binary receive function for that type. In such a case, data transfer will fail, and the `binary` option cannot be used.

If the publisher is a PostgreSQL version before 16, then any initial table synchronization will use text format even if `binary = true`.

`copy_data` (`boolean`)&#x20;

指定複寫開始後是否應複寫正在訂閱的發佈中的現有資料。預設值為 true。

If the publications contain `WHERE` clauses, it will affect what data is copied. Refer to the [Notes](https://www.postgresql.org/docs/current/sql-createsubscription.html#SQL-CREATESUBSCRIPTION-NOTES) for details.

See [Notes](https://www.postgresql.org/docs/current/sql-createsubscription.html#SQL-CREATESUBSCRIPTION-NOTES) for details of how `copy_data = true` can interact with the `origin` parameter.

`streaming` (`enum`)&#x20;

Specifies whether to enable streaming of in-progress transactions for this subscription. The default value is `off`, meaning all transactions are fully decoded on the publisher and only then sent to the subscriber as a whole.

If set to `on`, the incoming changes are written to temporary files and then applied only after the transaction is committed on the publisher and received by the subscriber.

If set to `parallel`, incoming changes are directly applied via one of the parallel apply workers, if available. If no parallel apply worker is free to handle streaming transactions then the changes are written to temporary files and applied after the transaction is committed. Note that if an error happens in a parallel apply worker, the finish LSN of the remote transaction might not be reported in the server log.

`synchronous_commit` (`enum`)

此參數的值將覆寫 [synchronous\_commit ](../../server-administration/server-configuration/write-ahead-log.md#19-5-1-settings)設定。預設值為 off。

使用 off 進行邏輯複寫是安全的：如果訂閱戶因缺少同步而遺失事務，則資料將從發佈者重新發送。

執行同步邏寫複製時，可能需要使用其他設定。邏輯複寫工作程序向發佈者報告寫入和更新的位置，使用同步複寫時，發佈者將等待實際更新。這意味著在將訂閱用於同步複寫時將訂閱戶的 synchronous\_commit 設定為 off 可能會增加發佈伺服器上 COMMIT 的延遲。在這種情況下，將 synchronous\_commit 設定為 local 或更高的值可能更有利。

`two_phase` (`boolean`)&#x20;

Specifies whether two-phase commit is enabled for this subscription. The default is `false`.

When two-phase commit is enabled, prepared transactions are sent to the subscriber at the time of `PREPARE TRANSACTION`, and are processed as two-phase transactions on the subscriber too. Otherwise, prepared transactions are sent to the subscriber only when committed, and are then processed immediately by the subscriber.

The implementation of two-phase commit requires that replication has successfully finished the initial table synchronization phase. So even when `two_phase` is enabled for a subscription, the internal two-phase state remains temporarily “pending” until the initialization phase completes. See column `subtwophasestate` of [`pg_subscription`](https://www.postgresql.org/docs/current/catalog-pg-subscription.html) to know the actual two-phase state.

`disable_on_error` (`boolean`)&#x20;

Specifies whether the subscription should be automatically disabled if any errors are detected by subscription workers during data replication from the publisher. The default is `false`.

`password_required` (`boolean`)&#x20;

Specifies whether connections to the publisher made as a result of this subscription must use password authentication. This setting is ignored when the subscription is owned by a superuser. The default is `true`. Only superusers can set this value to `false`.

`run_as_owner` (`boolean`)&#x20;

If true, all replication actions are performed as the subscription owner. If false, replication workers will perform actions on each table as the owner of that table. The latter configuration is generally much more secure; for details, see [Section 31.9](https://www.postgresql.org/docs/current/logical-replication-security.html). The default is `false`.

`origin` (`string`)&#x20;

Specifies whether the subscription will request the publisher to only send changes that don't have an origin or send changes regardless of origin. Setting `origin` to `none` means that the subscription will request the publisher to only send changes that don't have an origin. Setting `origin` to `any` means that the publisher sends changes regardless of their origin. The default is `any`.

See [Notes](https://www.postgresql.org/docs/current/sql-createsubscription.html#SQL-CREATESUBSCRIPTION-NOTES) for details of how `copy_data = true` can interact with the `origin` parameter.

When specifying a parameter of type `boolean`, the `=` _`value`_ part can be omitted, which is equivalent to specifying `TRUE`.

### 注意

有關如何在訂閱和發佈的服服之間配置存取控制的詳細訊息，請參閱[第 30.7 節](../../server-administration/logical-replication/security.md)。

建立複寫插槽時（預設行為），CREATE SUBSCRIPTION 不能在交易事務區塊內執行。

建立連線到同一資料庫叢集的訂閱（例如，在同一叢集中的資料庫之間進行複寫或在同一資料庫中進行複寫）只有在複寫插槽未作為同一指令的一部分建立時才會成功。否則，CREATE SUBSCRIPTION 呼叫將失敗。要使其順利運作，請單獨建立複寫插槽（使用函數 pg\_create\_logical\_replication\_slot，套件名稱為 pgoutput），並使用參數 create\_slot = false 建立訂閱。這是一個可能在將來的版本中解除的實作限制。

If any table in the publication has a `WHERE` clause, rows for which the _`expression`_ evaluates to false or null will not be published. If the subscription has several publications in which the same table has been published with different `WHERE` clauses, a row will be published if any of the expressions (referring to that publish operation) are satisfied. In the case of different `WHERE` clauses, if one of the publications has no `WHERE` clause (referring to that publish operation) or the publication is declared as [`FOR ALL TABLES`](https://www.postgresql.org/docs/current/sql-createpublication.html#SQL-CREATEPUBLICATION-FOR-ALL-TABLES) or [`FOR TABLES IN SCHEMA`](https://www.postgresql.org/docs/current/sql-createpublication.html#SQL-CREATEPUBLICATION-FOR-TABLES-IN-SCHEMA), rows are always published regardless of the definition of the other expressions. If the subscriber is a PostgreSQL version before 15, then any row filtering is ignored during the initial data synchronization phase. For this case, the user might want to consider deleting any initially copied data that would be incompatible with subsequent filtering. Because initial data synchronization does not take into account the publication [`publish`](https://www.postgresql.org/docs/current/sql-createpublication.html#SQL-CREATEPUBLICATION-WITH-PUBLISH) parameter when copying existing table data, some rows may be copied that would not be replicated using DML. See [Section 31.2.2](https://www.postgresql.org/docs/current/logical-replication-subscription.html#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES) for examples.

Subscriptions having several publications in which the same table has been published with different column lists are not supported.

We allow non-existent publications to be specified so that users can add those later. This means [`pg_subscription`](https://www.postgresql.org/docs/current/catalog-pg-subscription.html) can have non-existent publications.

When using a subscription parameter combination of `copy_data = true` and `origin = NONE`, the initial sync table data is copied directly from the publisher, meaning that knowledge of the true origin of that data is not possible. If the publisher also has subscriptions then the copied table data might have originated from further upstream. This scenario is detected and a WARNING is logged to the user, but the warning is only an indication of a potential problem; it is the user's responsibility to make the necessary checks to ensure the copied data origins are really as wanted or not.

To find which tables might potentially include non-local origins (due to other subscriptions created on the publisher) try this SQL query:

```
# substitute <pub-names> below with your publication name(s) to be queried
SELECT DISTINCT PT.schemaname, PT.tablename
FROM pg_publication_tables PT,
     pg_subscription_rel PS
     JOIN pg_class C ON (C.oid = PS.srrelid)
     JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE N.nspname = PT.schemaname AND
      C.relname = PT.tablename AND
      PT.pubname IN (<pub-names>);
```

### 範例

建立遠端伺服器的訂閱，將複寫 mypublication 和 insert\_only 資料表，並在提交時立即開始複寫：

```
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;
```

建立對於遠端伺服器的訂閱，將複寫 insert\_only 資料表，並且在稍後啟用之前不會開始複寫。

```
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);
```

### 相容性

CREATE SUBSCRIPTION 是 PostgreSQL 的延伸功能。

### 參閱

[ALTER SUBSCRIPTION](alter-subscription.md), [DROP SUBSCRIPTION](drop-subscription.md), [CREATE PUBLICATION](create-publication.md), [ALTER PUBLICATION](alter-publication.md)
