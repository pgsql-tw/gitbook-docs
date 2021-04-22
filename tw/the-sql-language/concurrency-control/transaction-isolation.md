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

這是因為如果 A 在 B 之前執行的話，B 的 SUM 函數就會得到 330 的總和而不是 300。然而若是將執行順序反過來的話，A 的 SUM 函數也會有總合數值不同的類似問題。

當我們藉由序列化交易來預防 _serialization anomaly_ 的時候，在一個正在進行讀取的交易成功提交之前，任何從持久性使用者資料表所讀取的資料都不該被視為合法的。即使是唯讀的交易也是如此，除非是在讀取時直接視作合法資料的 _deferrable_ 的交易，因為他會一直等到能取得一個確保不被這類問題影響的 snapshot 後才會開始讀取資料。在所有其他的應用情境中，都不應該依賴於稍後被中斷的交易所讀取的資料；取而代之的是．他們應該持續重試整個交易直到成功。

在 PostgreSQL 中可以使用 _predicate locking_ 確保正確的序列化，當一個交易優先執行時，他將會持有一把特別的鎖，用來決定一個寫入操作何時會對先前其他併發交易中的讀取操作產生影響。這種鎖在 PostgreSQL 中並不會導致任何阻塞或是死鎖的情況，他們主要是用來判斷與標記在進行序列化併發交易時，會導致 serialization anomalies 的特定組合。相對而言，一個 Read Committed 或 Repeatable Read 隔離等級的交易，就可能需要取得一整個資料表的鎖才能確保其資料一致性。然而這可能會阻塞其他想存取那張資料表的使用者，或是在使用 `SELECT FOR UPDATE` 或 `SELECT FOR SHARE` 的指令時阻塞其他交易進行且造成額外的硬碟資料存取。

就像其他大多數的資料庫系統一樣，PostgreSQL 的 predicate locks 是基於一筆交易所實際訪問的資料的。這將會在 [`pg_locks`](https://www.postgresql.org/docs/10/static/view-pg-locks.html) 系統介面中的 `SIReadLock` 模式下呈現。在一次查詢中所需要的鎖會取決於它採用的執行計畫，同時為了避免追蹤各個鎖的狀態而導致記憶體用罄，他將會傾向於把多個細粒度的鎖（比如 tuple locks） 組合成更粗粒度的鎖（比如 page locks）。而在一筆唯讀的交易中，如果它檢測到已經沒有會導致 serialization anomaly 的衝突時，它可以提前釋放所持有的 SIRead 鎖，而且實際上唯讀的交易往往可以在開始時就這麼做來避免持有任何 predicate locks。但如果你特別請求一筆 `SERIALIZABLE READ ONLY DEFERRABLE` 的交易的話，他仍會持續阻塞直到能確認這種情況為止。（這也是唯一一個 Serializable 交易會阻塞，但 Repeatable Read 交易卻不會的狀況。）從另一方面來說，SIRead 鎖通常需要持有直到交易提交之後，直到所有存取資料相互重疊的讀寫交易都完成為止。

一致使用序列化交易可以簡化開發。對於任何成功提交的併發交易的集合，都會有和逐個執行相同的效果，這個保證意味著如果你能證明一筆交易在獨自執行時是正確的，那麼你便可以相信他在任何混雜的序列化交易中也能運作良好，即使你不知道其他交易做了什麼或是使否成功提交也絲毫不影響。對於一個使用這類型技術的環境而言，有一個通用的方法來處理序列化失敗是非常重要的（他通常會返回一個 '40001' 的 SQLSTATE），因為很難去準確的預測哪些交易可能會對相關的資料進行讀寫並進行回滾來預防 serialization anomalies。對於相關資料的讀寫進行監控，以及重啟因為序列化失敗而受影響的交易都需要付出成本，但相對於顯式鎖導致的阻塞以及 `SELECT FOR UPDATE` 或 `SELECT FOR SHARE` 指令來得更平衡些，序列化交易確實是某些環境中追求效能的最佳解。

在 PostgresSQL 的 Serializable transaction 的隔離等級中，併發的交易只有在能夠證明有一個可產生同樣結果的序列化執行順序時，才會被允許提交，但他仍無法完全避免實際序列化執行時所引發的錯誤。更準確的來說，即使再插入鍵值之前已經明確檢查確認過他並不存在，仍然可能因為序列化交易存取資料的重疊問題，而導致違反數值唯一限制的衝突。這可以透過在插入可能引發衝突的鍵值之前檢查所有的序列化交易來避免。舉例而言，想像有一個應用程式它向使用者索取一個新的鍵值，並預先透過在資料表中選取他來檢查確保他尚未存在，或是直接選擇現有的最大鍵值加上 1 來生成一個新的鍵值。如果有些序列化交易沒有遵循這個協議反而直接插入鍵值的話，可能會回報違反了唯一數值的限制，即使他在一連串序列化執行的併發交易中不可能發生也一樣。

若要仰賴序列化交易的併發控制來追求效能最佳化的話，你需要考慮到這些議題：

* 盡可能將交易宣告為 `READ ONLY` 的
* 妥善控制使用中的連線數，並在必要時刻使用連線池。這總是會是一個重要的效能考量，尤其是在使用序列化交易的工作量繁重的系統中。
* 別在單一筆交易中安排不必要的事務，以實現簡潔的目的
* 別讓連線陷入過久的閒置狀態。[idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) 這個設定參數可以用來自動斷開閒置的會話。
* 當有了序列化交易所帶來的隔離與保護後，移除掉不必要的顯式鎖、`SELECT FOR UPDATE`, 和 `SELECT FOR SHARE` 指令。
* 當 predicate lock 的資料表因為記憶體不足，而被迫把多個 page-level predicate locks 合併成單一個relation-level predicate lock 時，序列化失敗率可能會因此上升。你可以透過提高 [max\_pred\_locks\_per\_transaction](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-TRANSACTION), [max\_pred\_locks\_per\_relation](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-RELATION), 且/或 [max\_pred\_locks\_per\_page](https://www.postgresql.org/docs/10/static/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-PAGE) 來避免。
* 線性掃描始終都需要一個 relation-level predicate lock，這可能導致序列化失敗率的上升。透過減少 [random\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-RANDOM-PAGE-COST) 且/或增加 [cpu\_tuple\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-CPU-TUPLE-COST) 來鼓勵使用索引掃描可能會有所幫助。記得要在減少交易回滾及重試次數與執行查詢的整題時間變化之間做好權衡。
