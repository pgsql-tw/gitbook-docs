<a id="SQL-DROPSUBSCRIPTION"></a><a id="id-1.9.3.133.1"></a>

## DROP SUBSCRIPTION

DROP SUBSCRIPTION — 移除訂閱

<a id="id-1.9.3.133.4"></a>

## 語法

```

DROP SUBSCRIPTION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.133.5"></a>

## 說明

`DROP SUBSCRIPTION` 會從資料庫叢集中移除訂閱。

要執行此命令，使用者必須是該訂閱的擁有者。

若訂閱與某個複寫插槽相關聯，則 `DROP SUBSCRIPTION` 不能在交易區塊內執行。（您可以使用 [`ALTER SUBSCRIPTION`](sql-altersubscription.md) 取消設定該複寫插槽。）

<a id="id-1.9.3.133.6"></a>

## 參數

`IF EXISTS`
:   訂閱不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之訂閱的名稱。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有任何作用，因為沒有任何物件相依於訂閱。

<a id="id-1.9.3.133.7"></a>

## 注意事項

移除與遠端主機上某個複寫插槽相關聯的訂閱時（這是正常狀態），`DROP SUBSCRIPTION` 會連線到遠端主機，並在其操作過程中嘗試移除該複寫插槽（以及任何剩餘的資料表同步插槽）。這是必要的，如此才能釋放在遠端主機上為該訂閱配置的資源。若此動作失敗，不論是因為無法連線到遠端主機，或是因為遠端複寫插槽無法移除、不存在或從未存在，`DROP SUBSCRIPTION` 命令都會失敗。要在這種情況下繼續進行，請先執行 [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE) 停用該訂閱，然後執行 [`ALTER SUBSCRIPTION ... SET (slot_name = NONE)`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SET) 將它與複寫插槽解除關聯。之後，`DROP SUBSCRIPTION` 就不會嘗試移除訂閱本身的複寫插槽。若仍有部分資料表同步尚未完成，它仍可能連線到發佈端以移除內部建立的資料表同步插槽；若無法連線到發佈端，則必須手動移除這些槽（以及主要的槽，若它仍存在）。否則，這個（些）槽會持續保留 WAL，最終可能導致磁碟空間被填滿。另請參閱[第 29.2.1 節](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)。

若訂閱與某個複寫插槽相關聯，則 `DROP
SUBSCRIPTION` 不能在交易區塊內執行。

<a id="id-1.9.3.133.8"></a>

## 範例

移除訂閱：

```

DROP SUBSCRIPTION mysub;
```

<a id="id-1.9.3.133.9"></a>

## 相容性

`DROP SUBSCRIPTION` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.133.10"></a>

## 另請參閱

[CREATE SUBSCRIPTION](sql-createsubscription.md), [ALTER SUBSCRIPTION](sql-altersubscription.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropsubscription.html)（原文版本：18.6；核對日期：2026-10-03）
