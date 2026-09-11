<a id="APPLEVEL-CONSISTENCY"></a>

## 13.4. 應用程式層級的資料一致性檢查 [#](#APPLEVEL-CONSISTENCY)

[13.4.1. 以 Serializable 交易確保一致性](applevel-consistency.md#SERIALIZABLE-CONSISTENCY)

[13.4.2. 以明確的阻擋式鎖定確保一致性](applevel-consistency.md#NON-SERIALIZABLE-CONSISTENCY)

使用 Read Committed 交易來強制執行與資料完整性相關的商業規則是非常困難的，因為資料的視野會隨著每個陳述式而變動，而且如果發生寫入衝突，即使是單一陳述式也不一定會侷限在該陳述式的快照中。

雖然 Repeatable Read 交易在整個執行期間都有穩定的資料視野，但使用 MVCC 快照進行資料一致性檢查仍有一個微妙的問題，涉及所謂的*讀寫衝突*（read/write conflict）。如果一個交易寫入資料，而一個並行交易試圖讀取相同的資料（無論是在寫入之前或之後），它都看不到另一個交易所做的工作。於是無論哪一個先開始或哪一個先提交，讀取者看起來都像是先執行的。如果事情僅止於此，就沒有問題；但如果讀取者也寫入了被某個並行交易讀取的資料，現在就會有一個交易看起來是在前述兩個交易之前執行的。如果看起來最後執行的交易實際上最先提交，交易執行順序的圖中就很容易出現循環。當出現這種循環時，如果沒有一些協助，完整性檢查就無法正確運作。

如[第 13.2.3 節](transaction-iso.md#XACT-SERIALIZABLE)所述，Serializable 交易其實就是 Repeatable Read 交易，只是額外加上了對危險之讀寫衝突模式的非阻擋式監控。當偵測到可能在表面上的執行順序中造成循環的模式時，就會回復其中一個相關的交易，以打破循環。

<a id="SERIALIZABLE-CONSISTENCY"></a>

### 13.4.1. 以 Serializable 交易確保一致性 [#](#SERIALIZABLE-CONSISTENCY)

如果所有寫入以及所有需要一致資料視野的讀取都使用 Serializable 交易隔離等級，就不需要任何其他努力來確保一致性。在其他環境中為了確保一致性而使用可序列化交易的軟體，在 PostgreSQL 中應該在這方面「直接就能運作」。

使用這項技巧時，如果應用程式軟體透過一個會自動重試因序列化失敗而被回復之交易的框架，就能避免為應用程式設計師帶來不必要的負擔。將 `default_transaction_isolation` 設為 `serializable` 可能是個好主意。另外，透過在觸發程序中檢查交易隔離等級，採取一些措施確保不會使用其他的交易隔離等級（無論是不小心使用，還是為了規避完整性檢查），也是明智的做法。

效能方面的建議請參閱[第 13.2.3 節](transaction-iso.md#XACT-SERIALIZABLE)。

### 警告：Serializable 交易與資料複寫

這種使用 Serializable 交易的完整性保護，目前尚未延伸到熱備援模式（[第 26.4 節](../../server-administration/high-availability/hot-standby.md)）或邏輯複本。因此，使用熱備援或邏輯複寫的人，可能會想在主要伺服器上使用 Repeatable Read 與明確鎖定。

<a id="NON-SERIALIZABLE-CONSISTENCY"></a>

### 13.4.2. 以明確的阻擋式鎖定確保一致性 [#](#NON-SERIALIZABLE-CONSISTENCY)

當可能發生非可序列化的寫入時，要確保某筆資料列目前的有效性並保護它不受並行更新影響，就必須使用 `SELECT FOR UPDATE`、`SELECT FOR SHARE` 或適當的 `LOCK TABLE` 陳述式。（`SELECT FOR UPDATE` 與 `SELECT FOR SHARE` 只會鎖定回傳的資料列以防止並行更新，而 `LOCK TABLE` 則會鎖定整個資料表。）從其他環境將應用程式移植到 PostgreSQL 時，應考量這一點。

對於從其他環境轉換過來的人，另一件值得注意的事是，`SELECT FOR UPDATE` 並不能確保並行交易不會更新或刪除被選取的資料列。要在 PostgreSQL 中做到這一點，你必須實際更新該資料列，即使不需要改變任何值也一樣。`SELECT FOR UPDATE` 會*暫時阻擋*其他交易取得相同的鎖定，或執行會影響被鎖定資料列的 `UPDATE` 或 `DELETE`；但一旦持有該鎖定的交易提交或回復，被阻擋的交易就會繼續進行衝突的操作，除非在持有鎖定期間實際對該資料列執行了 `UPDATE`。

在非可序列化的 MVCC 下，全域有效性檢查需要額外的考量。例如，銀行應用程式可能會想檢查某個資料表中所有貸方的總和，是否等於另一個資料表中借方的總和，而兩個資料表都正在被頻繁地更新。在 Read Committed 模式下，比較兩個連續 `SELECT sum(...)` 指令的結果並不可靠，因為第二個查詢很可能會包含第一個查詢沒有計入之交易的結果。在單一的 repeatable read 交易中計算這兩個總和，只能準確呈現在該 repeatable read 交易開始之前已提交之交易的影響；但人們可能會合理地質疑，當答案送達時是否仍然有意義。如果 repeatable read 交易本身在嘗試進行一致性檢查之前就套用了一些變更，檢查的用處就更有爭議了，因為現在它包含了交易開始之後的部分（而非全部）變更。在這種情況下，謹慎的人可能會想鎖定檢查所需的所有資料表，以取得無可爭議的當下實況。`SHARE` 模式（或更高）的鎖定可以保證被鎖定的資料表中，除了目前交易的變更之外，沒有任何未提交的變更。

另外也請注意，如果依賴明確鎖定來防止並行變更，就應該使用 Read Committed 模式；或者在 Repeatable Read 模式下，小心地在執行查詢之前先取得鎖定。repeatable read 交易所取得的鎖定可以保證沒有其他修改該資料表的交易仍在執行中，但如果該交易所看到的快照早於取得鎖定的時間，它就可能早於資料表中某些現在已提交的變更。repeatable read 交易的快照實際上是在它第一個查詢或資料修改指令（`SELECT`、`INSERT`、`UPDATE`、`DELETE` 或 `MERGE`）開始時凍結的，因此可以在快照凍結之前明確地取得鎖定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/applevel-consistency.html)（原文版本：18.6；核對日期：2026-09-11）
