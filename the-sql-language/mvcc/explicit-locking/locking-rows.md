# 13.3.2. 資料列層級鎖定

<a id="LOCKING-ROWS"></a>

## 13.3.2. 資料列層級鎖定 [#](#locking-rows) <a href="#locking-rows" id="locking-rows"></a>

除了資料表層級的鎖定之外，還有資料列層級的鎖定；下面列出這些鎖定，以及 PostgreSQL 自動使用它們的情境。完整的資料列層級鎖定衝突表請參閱[表 13.3](#row-lock-compatibility)。請注意，一個交易可以在同一筆資料列上持有互相衝突的鎖定，即使是在不同的子交易中也可以；但除此之外，兩個交易永遠不能在同一筆資料列上持有互相衝突的鎖定。資料列層級的鎖定不會影響資料查詢；它們只會阻擋對同一筆資料列的*寫入者與鎖定者*。資料列層級的鎖定就像資料表層級的鎖定一樣，會在交易結束時或回復交易儲存點時被釋放。

**資料列層級鎖定模式**

`FOR UPDATE`

`FOR UPDATE` 會使 `SELECT` 陳述式取得的資料列，如同要進行更新一般被鎖定。這可以防止它們在目前交易結束之前被其他交易鎖定、修改或刪除。也就是說，其他嘗試對這些資料列執行 `UPDATE`、`DELETE`、`SELECT FOR UPDATE`、`SELECT FOR NO KEY UPDATE`、`SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE` 的交易，都會被阻擋直到目前交易結束為止；反過來說，`SELECT FOR UPDATE` 會等待已經在同一筆資料列上執行過上述任何命令的並行交易，然後鎖定並回傳更新後的資料列（如果該資料列已被刪除，則不回傳任何資料列）。不過，在 `REPEATABLE READ` 或 `SERIALIZABLE` 交易中，如果要鎖定的資料列在交易開始之後已經被變更，就會引發錯誤。進一步的討論請參閱[第 13.4 節](../applevel-consistency.md)。

任何對資料列的 `DELETE`，以及修改某些欄位值的 `UPDATE`，也會取得 `FOR UPDATE` 鎖定模式。目前，`UPDATE` 情況所考量的欄位集合，是那些具有可用於外鍵之唯一索引的欄位（因此不考慮部分索引與運算式索引），但這在未來可能會改變。

`FOR NO KEY UPDATE`
:   行為與 `FOR UPDATE` 類似，只是所取得的鎖定較弱：這種鎖定不會阻擋嘗試在相同資料列上取得鎖定的 `SELECT FOR KEY SHARE` 命令。任何沒有取得 `FOR UPDATE` 鎖定的 `UPDATE`，也會取得這種鎖定模式。

`FOR SHARE`
:   行為與 `FOR NO KEY UPDATE` 類似，只是它在每一筆取得的資料列上取得的是共享鎖定，而不是排他鎖定。共享鎖定會阻擋其他交易對這些資料列執行 `UPDATE`、`DELETE`、`SELECT FOR UPDATE` 或 `SELECT FOR NO KEY UPDATE`，但不會阻止它們執行 `SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE`。

`FOR KEY SHARE`
:   行為與 `FOR SHARE` 類似，只是鎖定較弱：會阻擋 `SELECT FOR UPDATE`，但不會阻擋 `SELECT FOR NO KEY UPDATE`。鍵共享鎖定會阻擋其他交易執行 `DELETE` 或任何會變更鍵值的 `UPDATE`，但不會阻擋其他的 `UPDATE`，也不會阻止 `SELECT FOR NO KEY UPDATE`、`SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE`。

PostgreSQL 不會在記憶體中記住任何關於已修改資料列的資訊，因此一次可鎖定的資料列數量沒有上限。不過，鎖定一筆資料列可能會造成磁碟寫入；例如，`SELECT FOR UPDATE` 會修改選取的資料列以將它們標記為已鎖定，因此會導致磁碟寫入。

<a id="ROW-LOCK-COMPATIBILITY"></a>

### 表 13.3. 互相衝突的資料列層級鎖定 [#](#row-lock-compatibility) <a href="#row-lock-compatibility" id="row-lock-compatibility"></a>

<table border="1" class="table" summary="Conflicting Row-Level Locks"><colgroup><col class="col1"/><col class="lockst"/><col class="col3"/><col class="col4"/><col class="lockend"/></colgroup><thead><tr><th rowspan="2">要求的鎖定模式</th><th colspan="4">目前的鎖定模式</th></tr><tr><th>FOR KEY SHARE</th><th>FOR SHARE</th><th>FOR NO KEY UPDATE</th><th>FOR UPDATE</th></tr></thead><tbody><tr><td>FOR KEY SHARE</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td></tr><tr><td>FOR SHARE</td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td></tr><tr><td>FOR NO KEY UPDATE</td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td>FOR UPDATE</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr></tbody></table>

<br>

[返回 13.3. 明確鎖定](../explicit-locking.md#explicit-locking)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/explicit-locking.html)（原文版本：18.6；核對日期：2026-09-11）
