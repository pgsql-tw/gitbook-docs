# ALTER SUBSCRIPTION

ALTER SUBSCRIPTION — change the definition of a subscription

### 語法

```text
ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( set_publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name
```

### 說明

ALTER SUBSCRIPTION 可以變更 [CREATE SUBSCRIPTION](create-subscription.md) 中大部分可指定的訂閱屬性。

您必須是該訂閱的擁有者才能使用 ALTER SUBSCRIPTION。要變更擁有者，您必須是新角色的直接或間接成員，而新所有者必須是超級使用者。（目前，訂閱擁有者都必須是超級使用者，因此擁有者檢查將在實作中繞過，但未來這個部份有可能會發生變化。）

### 參數

_`name`_

屬性將被變更的訂閱名稱。

`CONNECTION '`_`conninfo`_'

此子句變更最初由 [CREATE SUBSCRIPTION](create-subscription.md) 設定的連線參數。請到該指令查看更多訊息。

`SET PUBLICATION` _`publication_name`_

變更訂閱發佈的列表。有關更多訊息，請參閱 [CREATE SUBSCRIPTION](create-subscription.md)。預設情況下，這個指令就如同 REFRESH PUBLICATION 一樣。

set\_publication\_option 為此操作指定了其他選項。支援的選項有：

`refresh` \(`boolean`\)

如果為 false，此指令將不會嘗試更新資料表訊息。REFRESH PUBLICATION 就應該要分開執行。預設值是 true。

此外，可能需要指定更新選項，如 REFRESH PUBLICATION 中所述。

`REFRESH PUBLICATION`

從發佈者取得缺少的資料表訊息。這將開始複寫自從上次呼叫 REFRESH PUBLICATION 或自從 CREATE SUBSCRIPTION 以來已加到訂閱發佈中的資料表。

refresh\_option 指定更新操作的附加選項。支援的選項有：

`copy_data` \(`boolean`\)

指定在複寫開始之後是否應複寫正在訂閱的發佈中的現有資料。預設值是 true。

`ENABLE`

啟用先前停用的訂閱，在交易事務結束時啟動邏輯複寫程序。

`DISABLE`

停用正在運行的訂閱，在交易事務結束時停止邏輯複寫的工作。

`SET (` _`subscription_parameter`_ \[= _`value`_\] \[, ... \] \)

此子句變更最初由 [CREATE SUBSCRIPTION](create-subscription.md) 設定的參數。查看該指令取得更多訊息。允許的選項是 slot\_name 和 synchronous\_commit

_`new_owner`_

訂閱的新擁有者的使用者名稱。

_`new_name`_

訂閱的新名稱。

### 範例

將訂閱的發佈對象變更為 insert\_only：

```text
ALTER SUBSCRIPTION mysub SET PUBLICATION insert_only;
```

停用（停止）訂閱：

```text
ALTER SUBSCRIPTION mysub DISABLE;
```

### 相容性

ALTER SUBSCRIPTION 是 PostgreSQL 的延伸功能。

### 參閱

[CREATE SUBSCRIPTION](create-subscription.md), [DROP SUBSCRIPTION](drop-subscription.md), [CREATE PUBLICATION](create-publication.md), [ALTER PUBLICATION](alter-publication.md)

