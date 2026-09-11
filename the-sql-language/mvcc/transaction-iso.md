<a id="TRANSACTION-ISO"></a>

## 13.2. 交易隔離 [#](#TRANSACTION-ISO)

[13.2.1. Read Committed 隔離等級](transaction-iso.md#XACT-READ-COMMITTED)

[13.2.2. Repeatable Read 隔離等級](transaction-iso.md#XACT-REPEATABLE-READ)

[13.2.3. Serializable 隔離等級](transaction-iso.md#XACT-SERIALIZABLE)

<a id="id-1.5.12.5.2"></a>

SQL 標準定義了四種交易隔離等級。最嚴格的是 Serializable，標準以一段文字來定義它：一組 Serializable 交易的任何並行執行，都保證會產生與依某種順序逐一執行它們相同的效果。其他三個等級則是以「現象」來定義，這些現象源自並行交易之間的交互作用，而且在各個等級中都不得發生。標準也指出，由於 Serializable 的定義方式，這些現象在該等級中都不可能發生。（這一點並不令人意外——如果交易的效果必須與逐一執行時一致，你怎麼可能看到由交互作用造成的任何現象？）

在各個等級中被禁止的現象如下：

dirty read（髒讀） <a id="id-1.5.12.5.4.1.1.1.1"></a>
:   某個交易讀取到另一個尚未提交的並行交易所寫入的資料。

nonrepeatable read（不可重複讀） <a id="id-1.5.12.5.4.1.2.1.1"></a>
:   某個交易重新讀取先前讀過的資料，卻發現該資料已被另一個交易（在第一次讀取之後提交的交易）修改。

phantom read（幻讀） <a id="id-1.5.12.5.4.1.3.1.1"></a>
:   某個交易重新執行一個回傳符合某搜尋條件之資料列集合的查詢，卻發現由於另一個最近提交的交易，符合該條件的資料列集合已經改變。

serialization anomaly（序列化異常） <a id="id-1.5.12.5.4.1.4.1.1"></a>
:   成功提交一組交易的結果，與逐一執行這些交易的所有可能順序都不一致。

<a id="id-1.5.12.5.5.1"></a>
SQL 標準與 PostgreSQL 所實作的交易隔離等級，說明於[表 13.1](transaction-iso.md#MVCC-ISOLEVEL-TABLE)。

<a id="MVCC-ISOLEVEL-TABLE"></a>

**表 13.1. 交易隔離等級**

<table border="1" class="table" summary="Transaction Isolation Levels"><colgroup><col/><col/><col/><col/><col/></colgroup><thead><tr><th>
         隔離等級
        </th><th>
         髒讀
        </th><th>
         不可重複讀
        </th><th>
         幻讀
        </th><th>
         序列化異常
        </th></tr></thead><tbody><tr><td>
         Read uncommitted
        </td><td>
         允許，但 PG 中不會發生
        </td><td>
         可能
        </td><td>
         可能
        </td><td>
         可能
        </td></tr><tr><td>
         Read committed
        </td><td>
         不可能
        </td><td>
         可能
        </td><td>
         可能
        </td><td>
         可能
        </td></tr><tr><td>
         Repeatable read
        </td><td>
         不可能
        </td><td>
         不可能
        </td><td>
         允許，但 PG 中不會發生
        </td><td>
         可能
        </td></tr><tr><td>
         Serializable
        </td><td>
         不可能
        </td><td>
         不可能
        </td><td>
         不可能
        </td><td>
         不可能
        </td></tr></tbody></table>

<br>

在 PostgreSQL 中，你可以要求四種標準交易隔離等級中的任何一種，但內部只實作了三種不同的隔離等級，也就是說，PostgreSQL 的 Read Uncommitted 模式的行為與 Read Committed 相同。這是因為，這是將標準隔離等級對應到 PostgreSQL 多版本並行控制架構的唯一合理方式。

此表也顯示，PostgreSQL 的 Repeatable Read 實作不允許幻讀。這在 SQL 標準下是可以接受的，因為標準規定的是在特定隔離等級下*不得*發生哪些異常；提供更高的保證是可以接受的。各個可用隔離等級的行為，會在後續小節中詳細說明。

要設定交易的隔離等級，請使用 [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) 命令。

### 重要

有些 PostgreSQL 資料型別與函式在交易行為上有特殊的規則。特別是，對序列（因此也包括以 `serial` 宣告之欄位的計數器）所做的變更，會立即對所有其他交易可見，而且即使做出變更的交易中止，也不會被回復。請參閱[第 9.17 節](../functions/functions-sequence.md)與[第 8.1.4 節](../datatype/datatype-numeric.md#DATATYPE-SERIAL)。

<a id="XACT-READ-COMMITTED"></a>

### 13.2.1. Read Committed 隔離等級 [#](#XACT-READ-COMMITTED)

<a id="id-1.5.12.5.11.2"></a><a id="id-1.5.12.5.11.3"></a>

*Read Committed* 是 PostgreSQL 的預設隔離等級。當交易使用這個隔離等級時，`SELECT` 查詢（不含 `FOR UPDATE/SHARE` 子句）只會看到在查詢開始之前已提交的資料；它永遠不會看到未提交的資料，也不會看到並行交易在查詢執行期間所提交的變更。實際上，`SELECT` 查詢看到的是資料庫在查詢開始執行那一刻的快照。不過，`SELECT` 確實會看到在它自己的交易中先前執行之更新的效果，即使這些更新尚未提交。另外也請注意，即使兩個相繼的 `SELECT` 命令位於同一個交易中，如果其他交易在第一個 `SELECT` 開始之後、第二個 `SELECT` 開始之前提交了變更，這兩個命令也可能看到不同的資料。

`UPDATE`、`DELETE`、`SELECT FOR UPDATE` 與 `SELECT FOR SHARE` 命令在搜尋目標資料列方面的行為與 `SELECT` 相同：它們只會找到在命令開始時已提交的目標資料列。不過，在找到這樣的目標資料列時，它可能已經被另一個並行交易更新（或刪除、鎖定）。在這種情況下，打算進行更新的一方會等待第一個進行更新的交易提交或回復（如果它仍在進行中）。如果第一個更新者回復，它的效果就會被抵銷，第二個更新者便可以繼續更新原先找到的資料列。如果第一個更新者提交，那麼若第一個更新者刪除了該資料列，第二個更新者就會略過它；否則第二個更新者會嘗試將它的操作套用到該資料列更新後的版本上。命令的搜尋條件（`WHERE` 子句）會被重新評估，以確認該資料列更新後的版本是否仍符合搜尋條件。若是如此，第二個更新者便會使用該資料列更新後的版本繼續進行它的操作。對於 `SELECT FOR UPDATE` 與 `SELECT FOR SHARE` 而言，這表示被鎖定並回傳給用戶端的，是該資料列更新後的版本。

帶有 `ON CONFLICT DO UPDATE` 子句的 `INSERT` 行為類似。在 Read Committed 模式下，每一筆打算插入的資料列不是被插入就是被更新。除非發生不相關的錯誤，否則保證會是這兩種結果之一。如果衝突來自另一個其效果尚未對該 `INSERT` 可見的交易，`UPDATE` 子句仍會影響那一筆資料列，即使該資料列可能*沒有*任何版本以一般方式對該命令可見。

帶有 `ON CONFLICT DO NOTHING` 子句的 `INSERT`，可能會因為另一個交易的結果（其效果對該 `INSERT` 的快照不可見）而不插入某筆資料列。同樣地，這只會發生在 Read Committed 模式下。

`MERGE` 讓使用者可以指定 `INSERT`、`UPDATE` 與 `DELETE` 子命令的各種組合。同時帶有 `INSERT` 與 `UPDATE` 子命令的 `MERGE` 命令，看起來類似帶有 `ON CONFLICT DO UPDATE` 子句的 `INSERT`，但它並不保證 `INSERT` 或 `UPDATE` 其中之一一定會發生。如果 `MERGE` 嘗試執行 `UPDATE` 或 `DELETE`，而該資料列被並行更新，但對於目前的目標與目前的來源 tuple，聯結條件仍然成立，那麼 `MERGE` 的行為會與 `UPDATE` 或 `DELETE` 命令相同，對該資料列更新後的版本執行其動作。不過，由於 `MERGE` 可以指定多個動作，而且這些動作可以是有條件的，因此會從第一個動作開始，針對該資料列更新後的版本重新評估每個動作的條件，即使原本相符的動作出現在動作清單的較後面也一樣。另一方面，如果該資料列被並行更新，使得聯結條件不再成立，那麼 `MERGE` 接下來會評估命令的 `NOT MATCHED BY SOURCE` 與 `NOT MATCHED [BY TARGET]` 動作，並分別執行每一種中第一個成功的動作。如果該資料列被並行刪除，那麼 `MERGE` 會評估命令的 `NOT MATCHED [BY TARGET]` 動作，並執行第一個成功的動作。如果 `MERGE` 嘗試執行 `INSERT`，而存在唯一索引且有重複的資料列被並行插入，就會引發唯一性違反錯誤；`MERGE` 不會藉由重新開始評估 `MATCHED` 條件來嘗試避免這類錯誤。

由於上述規則，進行更新的命令有可能看到不一致的快照：它可以看到並行更新命令對它試圖更新之相同資料列的效果，卻看不到那些命令對資料庫中其他資料列的效果。這種行為使得 Read Committed 模式不適合涉及複雜搜尋條件的命令；不過，對於較簡單的情況，它恰到好處。例如，考慮從一個帳戶轉帳 $100 到另一個帳戶：

```

BEGIN;
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
COMMIT;
```

如果另一個交易同時嘗試變更帳戶 7534 的餘額，我們顯然希望第二個陳述式從該帳戶資料列更新後的版本開始處理。由於每個命令只影響一筆預先決定的資料列，讓它看到該資料列更新後的版本並不會造成任何麻煩的不一致。

更複雜的用法在 Read Committed 模式下可能產生不理想的結果。例如，考慮一個 `DELETE` 命令，它所操作的資料正被另一個命令同時加入與移出其限制條件的範圍；例如，假設 `website` 是一個有兩筆資料列的資料表，其 `website.hits` 分別等於 `9` 與 `10`：

```

BEGIN;
UPDATE website SET hits = hits + 1;
-- run from another session:  DELETE FROM website WHERE hits = 10;
COMMIT;
```

即使在 `UPDATE` 之前與之後都存在 `website.hits = 10` 的資料列，這個 `DELETE` 也不會有任何效果。這是因為更新前的資料列值 `9` 會被略過，而當 `UPDATE` 完成、`DELETE` 取得鎖定時，新的資料列值已不再是 `10` 而是 `11`，不再符合條件。

由於 Read Committed 模式會以一個新的快照開始每個命令，而該快照包含到那一刻為止已提交的所有交易，因此同一個交易中的後續命令無論如何都會看到已提交之並行交易的效果。上面討論的重點在於，*單一*命令是否能看到資料庫絕對一致的視圖。

Read Committed 模式所提供的部分交易隔離，對許多應用程式來說已經足夠，而且這個模式使用起來既快速又簡單；不過，它並不適用於所有情況。執行複雜查詢與更新的應用程式，可能需要比 Read Committed 模式所提供的更嚴格一致的資料庫視圖。

<a id="XACT-REPEATABLE-READ"></a>

### 13.2.2. Repeatable Read 隔離等級 [#](#XACT-REPEATABLE-READ)

<a id="id-1.5.12.5.12.2"></a><a id="id-1.5.12.5.12.3"></a>

*Repeatable Read* 隔離等級只會看到在交易開始之前已提交的資料；它永遠不會看到未提交的資料，也不會看到並行交易在該交易執行期間所提交的變更。（不過，每個查詢確實會看到在它自己的交易中先前執行之更新的效果，即使這些更新尚未提交。）這是比 SQL 標準對這個隔離等級所要求的更強的保證，而且可以防止[表 13.1](transaction-iso.md#MVCC-ISOLEVEL-TABLE) 中所描述的所有現象，唯獨序列化異常除外。如前所述，這是標準明確允許的，因為標準只描述了每個隔離等級必須提供的*最低*保護。

這個等級與 Read Committed 的不同之處在於，Repeatable Read 交易中的查詢所看到的快照，是*交易*中第一個非交易控制陳述式開始時的快照，而不是交易中目前這個陳述式開始時的快照。因此，*單一*交易中相繼的 `SELECT` 命令會看到相同的資料，也就是說，它們不會看到其他交易在自己的交易開始之後所提交的變更。

使用這個等級的應用程式，必須準備好因序列化失敗而重試交易。

`UPDATE`、`DELETE`、`MERGE`、`SELECT FOR UPDATE` 與 `SELECT FOR SHARE` 命令在搜尋目標資料列方面的行為與 `SELECT` 相同：它們只會找到在交易開始時已提交的目標資料列。不過，在找到這樣的目標資料列時，它可能已經被另一個並行交易更新（或刪除、鎖定）。在這種情況下，Repeatable Read 交易會等待第一個進行更新的交易提交或回復（如果它仍在進行中）。如果第一個更新者回復，它的效果就會被抵銷，Repeatable Read 交易便可以繼續更新原先找到的資料列。但如果第一個更新者提交（而且確實更新或刪除了該資料列，而不只是鎖定它），那麼 Repeatable Read 交易就會被回復，並出現下列訊息

```

ERROR:  could not serialize access due to concurrent update
```

因為 Repeatable Read 交易無法修改或鎖定在它開始之後被其他交易變更過的資料列。

當應用程式收到這個錯誤訊息時，應該中止目前的交易，並從頭重試整個交易。第二次執行時，交易會將先前已提交的變更視為其初始資料庫視圖的一部分，因此使用該資料列的新版本作為新交易之更新的起點，並不會有邏輯上的衝突。

請注意，只有進行更新的交易可能需要重試；唯讀交易永遠不會發生序列化衝突。

Repeatable Read 模式提供了嚴格的保證，確保每個交易都看到完全穩定的資料庫視圖。不過，這個視圖不一定總是與同一等級之並行交易的某種序列（逐一）執行一致。例如，即使是這個等級的唯讀交易，也可能看到一筆控制記錄已被更新為顯示某個批次已經完成，卻*沒有*看到邏輯上屬於該批次的某一筆明細記錄，因為它讀取的是控制記錄較早的版本。在這個隔離等級下執行的交易，若不謹慎地使用明確鎖定來阻擋會衝突的交易，想要藉此強制執行商業規則，通常無法正確運作。

Repeatable Read 隔離等級是以一種在學術資料庫文獻及其他一些資料庫產品中稱為*快照隔離*（Snapshot Isolation）的技術來實作的。與使用會降低並行性之傳統鎖定技術的系統相比，可能會觀察到行為與效能上的差異。有些其他系統甚至可能將 Repeatable Read 與快照隔離提供為行為不同的兩種隔離等級。區分這兩種技術的允許現象，直到 SQL 標準制定之後才由資料庫研究人員正式定義，這超出了本手冊的範圍。完整的探討請參閱 [[berenson95]](../../bibliography.md#BERENSON95)。

### 注意

在 PostgreSQL 9.1 版之前，要求 Serializable 交易隔離等級所提供的行為，與這裡所描述的完全相同。若要保留舊有的 Serializable 行為，現在應該改為要求 Repeatable Read。

<a id="XACT-SERIALIZABLE"></a>

### 13.2.3. Serializable 隔離等級 [#](#XACT-SERIALIZABLE)

<a id="id-1.5.12.5.13.2"></a><a id="id-1.5.12.5.13.3"></a><a id="id-1.5.12.5.13.4"></a><a id="id-1.5.12.5.13.5"></a>

*Serializable* 隔離等級提供最嚴格的交易隔離。這個等級會為所有已提交的交易模擬序列式的交易執行，就好像交易是一個接一個依序執行，而不是並行執行。不過，就像 Repeatable Read 等級一樣，使用這個等級的應用程式必須準備好因序列化失敗而重試交易。事實上，這個隔離等級的運作方式與 Repeatable Read 完全相同，只是它還會監控某些情況，這些情況可能使一組並行的 Serializable 交易的執行，表現得與這些交易所有可能的序列（逐一）執行都不一致。這項監控除了 Repeatable Read 中既有的阻擋之外，不會再引入任何阻擋，但監控本身會有一些額外負擔，而且一旦偵測到可能造成*序列化異常*的情況，就會觸發*序列化失敗*。

舉例來說，考慮一個資料表 `mytab`，最初內容如下：

```

 class | value
-------+-------
     1 |    10
     1 |    20
     2 |   100
     2 |   200
```

假設 Serializable 交易 A 計算：

```

SELECT SUM(value) FROM mytab WHERE class = 1;
```

然後將結果（30）作為 `value` 插入到一筆 `class` `= 2` 的新資料列中。同時，Serializable 交易 B 計算：

```

SELECT SUM(value) FROM mytab WHERE class = 2;
```

並得到結果 300，將它插入到一筆 `class` `= 1` 的新資料列中。接著兩個交易都嘗試提交。如果其中任一交易是在 Repeatable Read 隔離等級下執行，兩者都會被允許提交；但由於沒有任何與此結果一致的序列執行順序，使用 Serializable 交易時，只會允許其中一個交易提交，並以下列訊息回復另一個交易：

```

ERROR:  could not serialize access due to read/write dependencies among transactions
```

這是因為如果 A 在 B 之前執行，B 計算出來的總和會是 330 而不是 300；同樣地，另一種順序也會使 A 計算出不同的總和。

依賴 Serializable 交易來防止異常時，重要的是，從永久使用者資料表讀取的任何資料，在讀取它的交易成功提交之前，都不應被視為有效。即使是唯讀交易也是如此，唯一的例外是在*可延遲*（deferrable）唯讀交易中讀取的資料，它們一經讀取即可確定有效，因為這類交易在開始讀取任何資料之前，會等到能夠取得保證不會有這類問題的快照為止。在所有其他情況下，應用程式都不得依賴在後來中止之交易中讀取到的結果；而是應該重試該交易，直到成功為止。

為了保證真正的可序列化，PostgreSQL 使用*述詞鎖定*（predicate locking），也就是說，它會保留一些鎖定，用來判斷某次寫入如果先執行，是否會影響並行交易先前讀取的結果。在 PostgreSQL 中，這些鎖定不會造成任何阻擋，因此*不可能*在造成死結中扮演任何角色。它們用來識別並標記並行 Serializable 交易之間的相依關係，這些相依關係在某些組合下可能導致序列化異常。相較之下，想要確保資料一致性的 Read Committed 或 Repeatable Read 交易，可能需要鎖定整個資料表，這可能會阻擋其他嘗試使用該資料表的使用者；或者它可能使用 `SELECT FOR UPDATE` 或 `SELECT FOR SHARE`，這不僅可能阻擋其他交易，還會造成磁碟存取。

PostgreSQL 中的述詞鎖定，就像大多數其他資料庫系統一樣，是以交易實際存取的資料為基礎。這些鎖定會出現在 [`pg_locks`](../../internals/views/view-pg-locks.md) 系統視圖中，其 `mode` 為 `SIReadLock`。執行查詢期間所取得的具體鎖定，取決於查詢所使用的計畫；而且在交易進行過程中，多個較細粒度的鎖定（例如 tuple 鎖定）可能會被合併成較少的較粗粒度鎖定（例如頁面鎖定），以避免耗盡用來追蹤鎖定的記憶體。`READ ONLY` 交易如果偵測到已不可能再發生會導致序列化異常的衝突，就可能在完成之前釋放它的 SIRead 鎖定。事實上，`READ ONLY` 交易通常能在啟動時就確立這一點，從而完全不取得任何述詞鎖定。如果你明確要求 `SERIALIZABLE READ ONLY DEFERRABLE` 交易，它會阻擋直到能夠確立這一點為止。（這是 Serializable 交易會阻擋而 Repeatable Read 交易不會阻擋的*唯一*情況。）另一方面，SIRead 鎖定通常需要保留到交易提交之後，直到與它重疊的讀寫交易完成為止。

一致地使用 Serializable 交易可以簡化開發。由於保證任何一組成功提交的並行 Serializable 交易，其效果都與逐一執行它們相同，這表示只要你能證明某個照原樣撰寫的單一交易在單獨執行時會做正確的事，你就可以確信它在任何 Serializable 交易的組合中也會做正確的事——即使完全不知道其他那些交易可能做些什麼——否則它就不會成功提交。重要的是，使用這種技術的環境要有一套處理序列化失敗（一律以 SQLSTATE 值 '40001' 回傳）的通用方法，因為要準確預測哪些交易可能促成讀寫相依關係、並需要被回復以防止序列化異常，會非常困難。監控讀寫相依關係有其成本，重新啟動因序列化失敗而終止的交易也有成本；但與使用明確鎖定以及 `SELECT FOR UPDATE` 或 `SELECT FOR SHARE` 所涉及的成本與阻擋相比，對某些環境而言，Serializable 交易是效能上最好的選擇。

雖然 PostgreSQL 的 Serializable 交易隔離等級，只有在能證明存在某種會產生相同效果的序列執行順序時，才允許並行交易提交，但它不一定總能防止引發在真正的序列執行中不會發生的錯誤。特別是，即使在嘗試插入某個鍵之前已明確檢查過該鍵不存在，仍有可能因為與重疊的 Serializable 交易發生衝突而看到唯一限制條件違反。要避免這種情況，可以確保*所有*插入可能衝突之鍵的 Serializable 交易，都先明確檢查自己是否可以這麼做。例如，設想一個應用程式會向使用者要求一個新的鍵，然後先嘗試選取它以檢查它是否已經存在；或者藉由選取現有的最大鍵並加一來產生新的鍵。如果有些 Serializable 交易不遵循這套規則而直接插入新的鍵，那麼即使在並行交易的序列執行中不可能發生的情況下，也可能回報唯一限制條件違反。

依賴 Serializable 交易進行並行控制時，為了獲得最佳效能，應考慮下列事項：

* 盡可能將交易宣告為 `READ ONLY`。
* 控制作用中連線的數量，必要時使用連線池。這一向是重要的效能考量，但在使用 Serializable 交易的忙碌系統中可能格外重要。
* 不要在單一交易中放入超過維持完整性所需的內容。
* 不要讓連線處於「idle in transaction」（交易中閒置）狀態超過必要的時間。組態參數 [idle_in_transaction_session_timeout](../../server-administration/runtime-config/runtime-config-client.md#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) 可用來自動中斷逗留不去的工作階段。
* 由於 Serializable 交易會自動提供保護，因此請移除不再需要的明確鎖定、`SELECT FOR UPDATE` 與 `SELECT FOR SHARE`。
* 當述詞鎖定表的記憶體不足，系統被迫將多個頁面層級的述詞鎖定合併為單一關聯層級的述詞鎖定時，序列化失敗的發生率可能會上升。你可以藉由增加 [max_pred_locks_per_transaction](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-TRANSACTION)、[max_pred_locks_per_relation](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-RELATION) 和／或 [max_pred_locks_per_page](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-PAGE) 來避免這種情況。
* 循序掃描一定需要關聯層級的述詞鎖定。這可能導致序列化失敗的發生率上升。藉由降低 [random_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-RANDOM-PAGE-COST) 和／或提高 [cpu_tuple_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-TUPLE-COST) 來鼓勵使用索引掃描，可能會有所幫助。請務必權衡交易回復與重新啟動的減少，以及查詢執行時間的整體變化。

Serializable 隔離等級是以一種在學術資料庫文獻中稱為可序列化快照隔離（Serializable Snapshot Isolation）的技術來實作的，它以快照隔離為基礎，再加上對序列化異常的檢查。與使用傳統鎖定技術的其他系統相比，可能會觀察到一些行為與效能上的差異。詳細資訊請參閱 [[ports12]](../../bibliography.md#PORTS12)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/transaction-iso.html)（原文版本：18.6；核對日期：2026-09-11）
