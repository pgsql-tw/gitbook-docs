# DROP SUBSCRIPTION

DROP SUBSCRIPTION — 移除訂閱

### 語法

```text
DROP SUBSCRIPTION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

### 說明

DROP SUBSCRIPTION 從資料庫叢集中移除訂閱。

訂閱只能由超級使用者移除。

如果訂閱與複寫插槽關連，則不能在交易事務內執行 DROP SUBSCRIPTION。 （您可以使用 ALTER SUBSCRIPTION 來取消插槽的設定。）

### 參數

_`name`_

要移除的訂閱名稱。

`CASCADE`  
`RESTRICT`

這些關鍵詞沒有任何作用，因為訂閱沒有相依關係。

### 注意

在移除與遠端主機上的複寫插槽關連的訂閱（正常狀態）時，DROP SUBSCRIPTION 將連線到遠端主機，並嘗試將復寫插槽移除作為其操作的一部分。這是必要的，以便釋放為遠端主機上的訂閱所分配的資源。如果失敗，無論是因為遠端主機不可連線，還是因為遠端複寫插槽不能被移除或不存在，DROP SUBSCRIPTION 命令都將失敗。要在這種情況下繼續，請透過執行 ALTER SUBSCRIPTION ... SET（slot\_name = NONE）來解除訂閱與複寫插槽的關連。 之後，DROP SUBSCRIPTION 將不再嘗試對遠端主機執行任何操作。請注意，如果遠程複寫插槽仍然存在，則應該手動移除它；否則它將繼續保留 WAL 並最終可能導致磁碟空間不足。另見[第 31.2.1 節](../../server-administration/logical-replication/subscription.md)。

如果訂閱與複寫插槽相關連，則 DROP SUBSCRIPTION 不能在交易事務內執行。

### 範例

移除訂閱：

```text
DROP SUBSCRIPTION mysub;
```

### 相容性

DROP SUBSCRIPTION 是 PostgreSQL 的延伸功能。

### 參閱

[CREATE SUBSCRIPTION](create-subscription.md), [ALTER SUBSCRIPTION](alter-subscription.md)

