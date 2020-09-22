# 13.2. 交易隔離

SQL 標準中定義了四個等級的交易隔離，其中最嚴格的隔離是「Serializable（序列化）」。序列化在標準的描述中，被定義為任意序列化交易的並行操作，都會保證產出與依照某種任意順序一個一個執行它們的效果相同。其他三個等級則是經由現象來定義的，即在不同的並行交易間的互動，這些現象在各個等集中必不能發生。標準中也注意到，基於 Serializable 的定義，這些現象都不可能發生在 Serializable 等級。（這並不難理解 -- 如果交易的影響必須與一個一個執行的結果一致，你怎麼會看到這些因為互動而產生的現象呢？）

在不同等級中被禁止的現象是：

`dirty read（髒讀）` 交易讀取的資料是由尚未提交的並行交易寫入的。

`nonrepeatable read（無法重複的讀取）` 交易重新讀取它之前讀過的資料，但是卻發現資料被其他交易修改（在最初讀取之後提交）了。

`phantom read（幻讀）` 交易重新執行查詢，得到滿足搜尋條件的資料集，但卻發現得到的資料集因為其他最近剛提交的交易而變更了。

`serialization anomaly（序列化異常）` 在成功提交一群交易後，結果與以所有可能的順序依序執行交易的結果都不一致。

SQL 標準以及 PostgreSQL 實作的交易隔離等級，可參閱 Table 13.1。

#### **Table 13.1. 交易隔離等級**

| 隔離等級 | Dirty Read | Nonrepeatable Read | Phantom Read | Serialization Anomaly |
| :--- | :--- | :--- | :--- | :--- |
| Read uncommitted | 允許，但 PG 中不會 | 可能 | 可能 | 可能 |
| Read committed | 不可能 | 可能 | 可能 | 可能 |
| Repeatable read | 不可能 | 不可能 | 允許，但 PG 中不會 | 可能 |
| Serializable | 不可能 | 不可能 | 不可能 | 不可能 |

在 PostgreSQL 當中，你可以要求上述四種交易隔離等級的任何一種，但在 PostgreSQL 內部實際上實作的只有三種隔離等級。舉例來說，PostgreSQL 的 Read Uncommitted 模式跟 Read Committed 的行為很相像，這是因為這是能夠把標準的隔離等級對應到 PostgreSQL 的 MVCC 架構的明智方法。

表格中也顯示了 PostgreSQL 的 Repeatable Read 的實作並不允許 phantom read。關於這點，在 SQL 標準中，更嚴格的行為是被容許的：標準中定義的四個隔離等級，只定義了哪些現象必須不會發生，而沒有定義哪些現象 _必須_ 發生。可用的隔離等級的行為，在接下來的小節中會詳細描述。

若要設定交易的隔離等級，可使用指令 [SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)。

{% hint style="info" %}
有些 PostgreSQL 的資料型態和函式具有特殊的交易行為的規則。具體來說，對序列（以及以 `serial` 宣告的計算器欄位）造成的變更將會立刻能夠被所有其他交易所看見，並且即使造成變更的交易取消了也不會被還原。請參考 [9.16 小節](https://github.com/pgsql-tw/gitbook-docs/tree/cf1d43f0131d46f75fce957eab384b4cc45e0168/tw/the-sql-language/functions-and-operators/9.16.-xu-lie-han-shi) 及 [8.1.4 小節](https://github.com/pgsql-tw/gitbook-docs/tree/cf1d43f0131d46f75fce957eab384b4cc45e0168/tw/the-sql-language/data-types/numeric-types/README.md#8-1-4-xu-lie-xing-serial-types)。
{% endhint %}

## 13.2.1. Read Committed 隔離等級

_Read Committed（提交讀）_ 是 PostgreSQL 預設的隔離等級。當交易使用這個隔離等級時，一個 `SELECT` 的查詢（沒有 `FOR UPDATE/SHARE` 的宣告）只會看見在查詢開始前已經被提交的資料；它不會看見尚未提交的資料或者是在查詢執行過程中被並行的交易提交的變更。實際上，`SELECT` 查詢是看見了在查詢開始執行的那一瞬間的資料庫快照。然而，`SELECT` 會看見在它自己的交易中比它先執行的更新，即使那些更新尚未被提交。同時需要注意的是，對於兩個成功的 `SELECT` 指令，如果其他交易在第一個 `SELECT` 開始後、第二個 `SELECT` 開始前提交變更，則即使這兩個 `SELECT` 在同一個交易中也可能會看見不同的資料，

`UPDATE`、`DELETE`、`SELECT FOR UPDATE`、和 `SELECT FOR SHARE` 在搜尋目標資料列的行為與 `SELECT` 一樣：它們只會找出在指令開始時已經被提交的目標資料列。然而，這些資料列在被找到的時候，有可能已經被其他並行交易更新（或者刪除、鎖定），在這個情況下，這個更新者會等待第一個更新的交易提交或者還原（如果那個交易還正在進行中）。如果第一個更新者還原了，那麼它的影響就無效了，第二個更新者會以原本找到的資料列做更新。而當第一個更新者提交了的狀況，若它把資料列刪除，則第二個更新者會忽略這個資料列，否則其他狀況下第二個更新者會嘗試在更新後的資料列上套用它要做的操作。此時指令中的搜尋條件（`WHERE` 宣告）會被重新評估，看看更新後的資料列是否依然符合搜尋條件，如果符合的話，第二個更新者就會對更新後的資料列套用它的操作。在 `SELECT FOR UPDATE` 和 `SELECT FOR SHARE` 的案例中，這代表會對更新後的資料列上鎖並回傳給客戶端。

包含 `ON CONFLICT DO UPDATE` 宣告的 `INSERT` 的行為也很相似。在 Read Committed 模式中，每個插入的資料列會被插入或者更新，除非有其他不相關的錯誤，否則會保證兩種結果的其中一種發生。如果衝突來自於其影響尚未能被 `INSERT` 所看見的其他交易，即使指令可能 _沒有_ 該資料列在慣例上可見的版本，`UPDATE` 宣告也將會影響那個資料列。

包含 `ON CONFLICT DO NOTHING` 宣告的 `INSERT` 在其他交易的影響尚未在 `INSERT` 的快照中可見的狀況，有可能不會執行插入。再次強調，這是只有在 Read Committed 模式的案例。

因為上述的規則，對更新的指令來說有可能會看見不一致的快照：它能夠看見其他並行的更新指令對它嘗試要更新的資料列的影響，但它不會看見這些其他指令對資料庫裡的其他資料列的影響。這個行為使得 Read Committed 模式並不適合牽涉到複雜的搜尋條件的指令；然而，它對於比較簡單的案例卻是剛剛好。例如，考慮以下更新銀行餘額的交易：

```text
BEGIN;
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
COMMIT;
```

如果兩個這樣的交易並行嘗試更新帳戶 12345 的餘額，我們顯然會希望第二個交易以帳戶資料列的更新後版本開始。因為每個指令都只會影響可預先決定的資料列，使得讓它看到更新後的資料列版本並不會造成任何有問題的不一致。

其他更複雜的使用狀況，在 Read Committed 模式中可以產生出並非期望的結果。例如考慮一個 `DELETE` 指令，要操作正好從它的限制條件中加入和移除的資料，像是假設 `website` 是一張有兩個資料列的表格，其中 `website.hits` 分別為 `9` 和 `10`：

```text
BEGIN;
UPDATE website SET hits = hits + 1;
-- run from another session:  DELETE FROM website WHERE hits = 10;
COMMIT;
```

即使在 `UPDATE` 之前與之後，都存在 `website.hits = 10` 的資料列，但 `DELETE` 指令不會產生任何影響。這是因為更新前值為 `9` 的資料列已經被忽略了，並且當 `UPDATE` 執行完成且 `DELETE` 取得鎖，新的資料列的值已經不是 `10` 而是 `11`，不再滿足限制條件了。

因為 Read Committed 模式在每個指令開始時會取得包含在那個瞬間已經提交的所有交易的快照，其後在同個交易中的指令無論如何都會看到並行交易提交的影響。上述的爭論點在於 _單一_ 指令是否看見資料庫完全一致的視野。

Read Committed 提供的部份交易隔離對很多應用程式來說已經足夠，並且這個模式很快且容易使用；然而，它沒辦法滿足所有的案例。對於做複雜查詢和更新的應用程式，可能會需要比 Read Committed 更嚴格的資料庫一致性視野。

## 13.2.2. Repeatable Read 隔離等級

_Repeatable Read（重複讀）_ 隔離等級只會看到在交易開始前已經被提交的資料；它永遠不會看見尚未提交的資料或者在交易期間被並行交易提交的變更。（然而，查詢會看見在它自己的交易中前面的更新所造成的影響，即使那些影響尚未被提交。）這是比 SQL 標準對這個隔離等級要求的還要更強的保證，並且能夠預防除了 serialization anomalies 以外所有在[表格 13.1](transaction-isolation.md#MVCC-ISOLEVEL-TABLE)描述的現象。如前所述，這是標準所允許的，因為標準只描述了每個隔離等級一定要提供的 _最小_ 保護。

這個等級跟 Read Committed 不同的地方在於 Repeatable Read 的交易看見的是在 _交易_ 的第一個非交易控制指令開始時的快照，而不是當前指令開始時的。因此，一個成功的 `SELECT` 指令在 _單一_ 交易之內都會看見相同的資料，例如它們不會看見在它們的交易開始以後其他交易所提交的變更。

使用這個等級的應用程式必須要準備好因為序列化失敗造成的交易重試。

`UPDATE`、`DELETE`、`SELECT FOR UPDATE`、和 `SELECT FOR SHARE` 指令的行為在搜尋目標資料列時與 `SELECT` 相同：它們將只會找在交易開始之前已經被提交的目標資料列。然而，這些目標資料列有可能在它被搜尋到時，已經被其他並行交易更新（或者刪除、上鎖），此時，Repeatable Read 的交易會等待第一個更新的交易提交或者還原（如果它正在進行中）。如果第一個更新者還原了，那麼它的影響就無效了，Repeatable Read 的交易就可以對原本找到的資料列做更新。但如果第一個更新者提交了（且確實更新或者刪除這個資料列，而非只是鎖定它而已），那麼 Repeatable Read 的交易將會還原並回應以下的訊息。

```text
ERROR:  could not serialize access due to concurrent update
```

這是因為 Repeatable Read 的交易無法更新或者鎖定在 Repeatable Read 的交易開始後被其他交易變更過的資料列。

當應用程式收到這個錯誤訊息，它應該要放棄現在的交易並且從頭開始重試整個交易。在第二次的期間，交易會看見之前提交的變更作為它對於資料庫的初始視野，因此在新的交易的更新中，不會有因為使用資料列的新版本為起始點而產生的邏輯衝突。

需注意的是，只有更新的交易可能需要重試；只有讀取的交易永遠不會發生序列化衝突。

Repeatable Read 模式提供了嚴格的保證，每個交易會看見完全穩定的資料庫視野。然而，這個視野並不需要跟並行交易的某些依序（一次一個）執行的結果總是維持一致。舉例來說，在這個等級中即使是一個只有讀取的交易，也可能只看見反應一個批次完成的控制紀錄的更新，但卻 _沒_ 看見邏輯上是批次的一部分的一個細節紀錄變更，因為它讀取到的是比較早的控制紀錄的版本。嘗試想要在這個隔離等級的交易下執行商業邏輯時，若沒有謹慎地使用明確的鎖去阻止並行交易的話，可能不會正確地運作。

## 注意

在 PostgreSQL 9.1 以前，一個採用 Serializable 交易隔離等級的要求，會提供跟這裡描述的完全一樣的行為。若想要保持過去的 Serializable 的行為，在現在應該要使用 Repeatable Read。

## 13.2.3. Serializable 隔離等級

_Serializable（序列化）_ 隔離等級提供了最嚴格的交易隔離。這個等級模擬了對所有提交的交易的一系列交易執行；如同交易們被一個接著一個地執行，連續地、而不是並行地。然而，如同 Repeatable Read，應用程式使用這個等級時必須要準備好因為序列化失敗而重試交易。事實上，這個隔離等級運作地完全與 Repeatable Read 相同，除了它會監視可能造成並行的序列化交易的執行結果跟一個一個執行這些交易產生些微不一致的症狀。這個監視行為並不會比 Repeatable Read 產生額外任何的阻塞（blocking），但監視的確會有一些額外的負擔，並且偵測到會造成 _serialization anomaly_ 的症狀將會觸發 _serialization failure_ 。

舉例來說，考慮有一個表格 `mytab`，一開始有：

```text
 class | value
-------+-------
     1 |    10
     1 |    20
     2 |   100
     2 |   200
```

假設有個序列化交易 A 要計算：

```text
SELECT SUM(value) FROM mytab WHERE class = 1;
```

然後將結果（30）作為 `value` 插入為 `class` `= 2` 的新資料列。同時序列化交易 B 並行地計算：

```text
SELECT SUM(value) FROM mytab WHERE class = 2;
```

並且得到結果 300，將它插入為 `class` `= 1` 的新資料列。接著兩個交易嘗試要提交。如果其中任何一個交易是以 Repeatable Read 隔離等級執行的，兩個交易都會被允許提交；但因為並沒有序列的執行順序與這個結果一致，使用 Serializable 的交易將會導致一個交易提交、另一個被還原並回覆這個訊息：

```text
ERROR:  could not serialize access due to read/write dependencies among transactions
```

This is because if A had executed before B, B would have computed the sum 330, not 300, and similarly the other order would have resulted in a different sum computed by A.

When relying on Serializable transactions to prevent anomalies, it is important that any data read from a permanent user table not be considered valid until the transaction which read it has successfully committed. This is true even for read-only transactions, except that data read within a _deferrable_ read-only transaction is known to be valid as soon as it is read, because such a transaction waits until it can acquire a snapshot guaranteed to be free from such problems before starting to read any data. In all other cases applications must not depend on results read during a transaction that later aborted; instead, they should retry the transaction until it succeeds.

To guarantee true serializability PostgreSQL uses _predicate locking_, which means that it keeps locks which allow it to determine when a write would have had an impact on the result of a previous read from a concurrent transaction, had it run first. In PostgreSQL these locks do not cause any blocking and therefore can _not_ play any part in causing a deadlock. They are used to identify and flag dependencies among concurrent Serializable transactions which in certain combinations can lead to serialization anomalies. In contrast, a Read Committed or Repeatable Read transaction which wants to ensure data consistency may need to take out a lock on an entire table, which could block other users attempting to use that table, or it may use `SELECT FOR UPDATE` or `SELECT FOR SHARE` which not only can block other transactions but cause disk access.

Predicate locks in PostgreSQL, like in most other database systems, are based on data actually accessed by a transaction. These will show up in the [`pg_locks`](https://www.postgresql.org/docs/10/static/view-pg-locks.html) system view with a `mode` of `SIReadLock`. The particular locks acquired during execution of a query will depend on the plan used by the query, and multiple finer-grained locks \(e.g., tuple locks\) may be combined into fewer coarser-grained locks \(e.g., page locks\) during the course of the transaction to prevent exhaustion of the memory used to track the locks. A `READ ONLY`transaction may be able to release its SIRead locks before completion, if it detects that no conflicts can still occur which could lead to a serialization anomaly. In fact, `READ ONLY`transactions will often be able to establish that fact at startup and avoid taking any predicate locks. If you explicitly request a `SERIALIZABLE READ ONLY DEFERRABLE` transaction, it will block until it can establish this fact. \(This is the _only_ case where Serializable transactions block but Repeatable Read transactions don't.\) On the other hand, SIRead locks often need to be kept past transaction commit, until overlapping read write transactions complete.

Consistent use of Serializable transactions can simplify development. The guarantee that any set of successfully committed concurrent Serializable transactions will have the same effect as if they were run one at a time means that if you can demonstrate that a single transaction, as written, will do the right thing when run by itself, you can have confidence that it will do the right thing in any mix of Serializable transactions, even without any information about what those other transactions might do, or it will not successfully commit. It is important that an environment which uses this technique have a generalized way of handling serialization failures \(which always return with a SQLSTATE value of '40001'\), because it will be very hard to predict exactly which transactions might contribute to the read/write dependencies and need to be rolled back to prevent serialization anomalies. The monitoring of read/write dependencies has a cost, as does the restart of transactions which are terminated with a serialization failure, but balanced against the cost and blocking involved in use of explicit locks and `SELECT FOR UPDATE` or `SELECT FOR SHARE`, Serializable transactions are the best performance choice for some environments.

While PostgreSQL's Serializable transaction isolation level only allows concurrent transactions to commit if it can prove there is a serial order of execution that would produce the same effect, it doesn't always prevent errors from being raised that would not occur in true serial execution. In particular, it is possible to see unique constraint violations caused by conflicts with overlapping Serializable transactions even after explicitly checking that the key isn't present before attempting to insert it. This can be avoided by making sure that _all_ Serializable transactions that insert potentially conflicting keys explicitly check if they can do so first. For example, imagine an application that asks the user for a new key and then checks that it doesn't exist already by trying to select it first, or generates a new key by selecting the maximum existing key and adding one. If some Serializable transactions insert new keys directly without following this protocol, unique constraints violations might be reported even in cases where they could not occur in a serial execution of the concurrent transactions.

For optimal performance when relying on Serializable transactions for concurrency control, these issues should be considered:

* Declare transactions as `READ ONLY` when possible.
* Control the number of active connections, using a connection pool if needed. This is always an important performance consideration, but it can be particularly important in a busy system using Serializable transactions.
* Don't put more into a single transaction than needed for integrity purposes.
* Don't leave connections dangling “idle in transaction” longer than necessary. The configuration parameter [idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) may be used to automatically disconnect lingering sessions.
* Eliminate explicit locks, `SELECT FOR UPDATE`, and `SELECT FOR SHARE` where no longer needed due to the protections automatically provided by Serializable transactions.
* When the system is forced to combine multiple page-level predicate locks into a single relation-level predicate lock because the predicate lock table is short of memory, an increase in the rate of serialization failures may occur. You can avoid this by increasing [max\_pred\_locks\_per\_transaction](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-TRANSACTION), [max\_pred\_locks\_per\_relation](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-RELATION), and/or [max\_pred\_locks\_per\_page](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-PAGE).
* A sequential scan will always necessitate a relation-level predicate lock. This can result in an increased rate of serialization failures. It may be helpful to encourage the use of index scans by reducing [random\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-RANDOM-PAGE-COST) and/or increasing [cpu\_tuple\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-CPU-TUPLE-COST). Be sure to weigh any decrease in transaction rollbacks and restarts against any overall change in query execution time.

