<a id="EXPLICIT-LOCKING"></a>

## 13.3. 明確鎖定 [#](#EXPLICIT-LOCKING)

[13.3.1. 資料表層級鎖定](explicit-locking.md#LOCKING-TABLES)

[13.3.2. 資料列層級鎖定](explicit-locking.md#LOCKING-ROWS)

[13.3.3. 頁面層級鎖定](explicit-locking.md#LOCKING-PAGES)

[13.3.4. 死結](explicit-locking.md#LOCKING-DEADLOCKS)

[13.3.5. 諮詢鎖定](explicit-locking.md#ADVISORY-LOCKS)

<a id="id-1.5.12.6.2"></a>

PostgreSQL 提供了多種鎖定模式，用來控制對資料表中資料的並行存取。在 MVCC 無法提供所需行為的情況下，這些模式可用於由應用程式控制的鎖定。此外，大多數 PostgreSQL 命令會自動取得適當模式的鎖定，以確保在命令執行期間，被參照的資料表不會被刪除或以不相容的方式修改。（例如，`TRUNCATE` 無法安全地與同一資料表上的其他操作並行執行，因此它會在該資料表上取得 `ACCESS EXCLUSIVE` 鎖定來強制做到這一點。）

要檢視資料庫伺服器中目前尚未釋放的鎖定清單，請使用 [`pg_locks`](../../internals/views/view-pg-locks.md) 系統視圖。關於監控鎖定管理子系統狀態的更多資訊，請參閱[第 27 章](../../server-administration/monitoring/README.md)。

<a id="LOCKING-TABLES"></a>

### 13.3.1. 資料表層級鎖定 [#](#LOCKING-TABLES)

<a id="id-1.5.12.6.5.2"></a>

下列清單列出可用的鎖定模式，以及 PostgreSQL 自動使用它們的情境。你也可以使用 [LOCK](../../reference/sql-commands/sql-lock.md) 命令明確取得這些鎖定中的任何一種。請記住，這些鎖定模式全都是資料表層級的鎖定，即使名稱中含有「row」一詞也一樣；鎖定模式的名稱是沿襲歷史而來的。在某種程度上，這些名稱反映了每種鎖定模式的典型用途——但它們的語意全都相同。一種鎖定模式與另一種之間唯一真正的差別，在於各自會與哪些鎖定模式衝突（請參閱[表 13.2](explicit-locking.md#TABLE-LOCK-COMPATIBILITY)）。兩個交易不能同時在同一個資料表上持有互相衝突之模式的鎖定。（不過，交易永遠不會與自己衝突。例如，它可以先取得 `ACCESS EXCLUSIVE` 鎖定，之後再在同一個資料表上取得 `ACCESS SHARE` 鎖定。）不會衝突的鎖定模式可以由許多交易同時持有。特別要注意的是，有些鎖定模式會與自己衝突（例如，`ACCESS EXCLUSIVE` 鎖定同一時間只能由一個交易持有），而其他鎖定模式則不會與自己衝突（例如，`ACCESS SHARE` 鎖定可以由多個交易持有）。

**資料表層級鎖定模式**

`ACCESS SHARE` (`AccessShareLock`)
:   只與 `ACCESS EXCLUSIVE` 鎖定模式衝突。

    `SELECT` 命令會在被參照的資料表上取得這種模式的鎖定。一般而言，任何只*讀取*資料表而不修改它的查詢，都會取得這種鎖定模式。

`ROW SHARE` (`RowShareLock`)
:   與 `EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。

    `SELECT` 命令會在所有指定了 `FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 選項之一的資料表上，取得這種模式的鎖定（此外，對於任何其他未指定明確 `FOR ...` 鎖定選項而被參照的資料表，則會取得 `ACCESS SHARE` 鎖定）。

`ROW EXCLUSIVE` (`RowExclusiveLock`)
:   與 `SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。

    `UPDATE`、`DELETE`、`INSERT` 與 `MERGE` 命令會在目標資料表上取得這種鎖定模式（此外，對任何其他被參照的資料表則會取得 `ACCESS SHARE` 鎖定）。一般而言，任何會*修改資料表中資料*的命令，都會取得這種鎖定模式。

`SHARE UPDATE EXCLUSIVE` (`ShareUpdateExclusiveLock`)
:   與 `SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的綱要變更與 `VACUUM` 執行。

    由 `VACUUM`（不含 `FULL`）、`ANALYZE`、`CREATE INDEX CONCURRENTLY`、`CREATE STATISTICS`、`COMMENT ON`、`REINDEX CONCURRENTLY`，以及某些 [`ALTER INDEX`](../../reference/sql-commands/sql-alterindex.md) 與 [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 的變化形式取得（完整細節請參閱這些命令的說明文件）。

`SHARE` (`ShareLock`)
:   與 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的資料變更。

    由 `CREATE INDEX`（不含 `CONCURRENTLY`）取得。

`SHARE ROW EXCLUSIVE` (`ShareRowExclusiveLock`)
:   與 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的資料變更，而且它會與自己互斥，因此同一時間只能有一個工作階段持有它。

    由 `CREATE TRIGGER` 以及某些形式的 [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 取得。

`EXCLUSIVE` (`ExclusiveLock`)
:   與 `ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式只允許並行的 `ACCESS SHARE` 鎖定，也就是說，在交易持有這種鎖定模式時，只有對該資料表的讀取可以同時進行。

    由 `REFRESH MATERIALIZED VIEW CONCURRENTLY` 取得。

`ACCESS EXCLUSIVE` (`AccessExclusiveLock`)
:   與所有模式的鎖定衝突（`ACCESS SHARE`、`ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE`）。這種模式保證持有者是唯一以任何方式存取該資料表的交易。

    由 `DROP TABLE`、`TRUNCATE`、`REINDEX`、`CLUSTER`、`VACUUM FULL` 以及 `REFRESH MATERIALIZED VIEW`（不含 `CONCURRENTLY`）命令取得。許多形式的 `ALTER INDEX` 與 `ALTER TABLE` 也會取得這個層級的鎖定。對於沒有明確指定模式的 `LOCK TABLE` 陳述式，這也是預設的鎖定模式。

### 提示

只有 `ACCESS EXCLUSIVE` 鎖定會阻擋 `SELECT`（不含 `FOR UPDATE/SHARE`）陳述式。

鎖定一旦取得，通常會一直持有到交易結束。但如果鎖定是在建立交易儲存點之後才取得的，那麼在回復到該交易儲存點時，這個鎖定會立即被釋放。這與 `ROLLBACK` 會取消自交易儲存點以來所有命令之效果的原則一致。在 PL/pgSQL 例外處理區塊中取得的鎖定也是如此：因錯誤而跳出該區塊時，會釋放在其中取得的鎖定。

<a id="TABLE-LOCK-COMPATIBILITY"></a>

**表 13.2. 互相衝突的鎖定模式**

<table border="1" class="table" summary="Conflicting Lock Modes"><colgroup><col/><col class="lockst"/><col/><col/><col/><col/><col/><col/><col class="lockend"/></colgroup><thead><tr><th rowspan="2">要求的鎖定模式</th><th align="center" colspan="8">既有的鎖定模式</th></tr><tr><th><code class="literal">ACCESS SHARE</code></th><th><code class="literal">ROW SHARE</code></th><th><code class="literal">ROW EXCL.</code></th><th><code class="literal">SHARE UPDATE EXCL.</code></th><th><code class="literal">SHARE</code></th><th><code class="literal">SHARE ROW EXCL.</code></th><th><code class="literal">EXCL.</code></th><th><code class="literal">ACCESS EXCL.</code></th></tr></thead><tbody><tr><td><code class="literal">ACCESS SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td></tr><tr><td><code class="literal">ROW SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">ROW EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE UPDATE EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE ROW EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">EXCL.</code></td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">ACCESS EXCL.</code></td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr></tbody></table>

<br>

<a id="LOCKING-ROWS"></a>

### 13.3.2. 資料列層級鎖定 [#](#LOCKING-ROWS)

除了資料表層級的鎖定之外，還有資料列層級的鎖定；下面列出這些鎖定，以及 PostgreSQL 自動使用它們的情境。完整的資料列層級鎖定衝突表請參閱[表 13.3](explicit-locking.md#ROW-LOCK-COMPATIBILITY)。請注意，一個交易可以在同一筆資料列上持有互相衝突的鎖定，即使是在不同的子交易中也可以；但除此之外，兩個交易永遠不能在同一筆資料列上持有互相衝突的鎖定。資料列層級的鎖定不會影響資料查詢；它們只會阻擋對同一筆資料列的*寫入者與鎖定者*。資料列層級的鎖定就像資料表層級的鎖定一樣，會在交易結束時或回復交易儲存點時被釋放。

**資料列層級鎖定模式**

`FOR UPDATE`
:   `FOR UPDATE` 會使 `SELECT` 陳述式取得的資料列，如同要進行更新一般被鎖定。這可以防止它們在目前交易結束之前被其他交易鎖定、修改或刪除。也就是說，其他嘗試對這些資料列執行 `UPDATE`、`DELETE`、`SELECT FOR UPDATE`、`SELECT FOR NO KEY UPDATE`、`SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE` 的交易，都會被阻擋直到目前交易結束為止；反過來說，`SELECT FOR UPDATE` 會等待已經在同一筆資料列上執行過上述任何命令的並行交易，然後鎖定並回傳更新後的資料列（如果該資料列已被刪除，則不回傳任何資料列）。不過，在 `REPEATABLE READ` 或 `SERIALIZABLE` 交易中，如果要鎖定的資料列在交易開始之後已經被變更，就會引發錯誤。進一步的討論請參閱[第 13.4 節](applevel-consistency.md)。

    任何對資料列的 `DELETE`，以及修改某些欄位值的 `UPDATE`，也會取得 `FOR UPDATE` 鎖定模式。目前，`UPDATE` 情況所考量的欄位集合，是那些具有可用於外鍵之唯一索引的欄位（因此不考慮部分索引與運算式索引），但這在未來可能會改變。

`FOR NO KEY UPDATE`
:   行為與 `FOR UPDATE` 類似，只是所取得的鎖定較弱：這種鎖定不會阻擋嘗試在相同資料列上取得鎖定的 `SELECT FOR KEY SHARE` 命令。任何沒有取得 `FOR UPDATE` 鎖定的 `UPDATE`，也會取得這種鎖定模式。

`FOR SHARE`
:   行為與 `FOR NO KEY UPDATE` 類似，只是它在每一筆取得的資料列上取得的是共享鎖定，而不是排他鎖定。共享鎖定會阻擋其他交易對這些資料列執行 `UPDATE`、`DELETE`、`SELECT FOR UPDATE` 或 `SELECT FOR NO KEY UPDATE`，但不會阻止它們執行 `SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE`。

`FOR KEY SHARE`
:   行為與 `FOR SHARE` 類似，只是鎖定較弱：會阻擋 `SELECT FOR UPDATE`，但不會阻擋 `SELECT FOR NO KEY UPDATE`。鍵共享鎖定會阻擋其他交易執行 `DELETE` 或任何會變更鍵值的 `UPDATE`，但不會阻擋其他的 `UPDATE`，也不會阻止 `SELECT FOR NO KEY UPDATE`、`SELECT FOR SHARE` 或 `SELECT FOR KEY SHARE`。

PostgreSQL 不會在記憶體中記住任何關於已修改資料列的資訊，因此一次可鎖定的資料列數量沒有上限。不過，鎖定一筆資料列可能會造成磁碟寫入；例如，`SELECT FOR UPDATE` 會修改選取的資料列以將它們標記為已鎖定，因此會導致磁碟寫入。

<a id="ROW-LOCK-COMPATIBILITY"></a>

**表 13.3. 互相衝突的資料列層級鎖定**

<table border="1" class="table" summary="Conflicting Row-Level Locks"><colgroup><col class="col1"/><col class="lockst"/><col class="col3"/><col class="col4"/><col class="lockend"/></colgroup><thead><tr><th rowspan="2">要求的鎖定模式</th><th colspan="4">目前的鎖定模式</th></tr><tr><th>FOR KEY SHARE</th><th>FOR SHARE</th><th>FOR NO KEY UPDATE</th><th>FOR UPDATE</th></tr></thead><tbody><tr><td>FOR KEY SHARE</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td></tr><tr><td>FOR SHARE</td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td></tr><tr><td>FOR NO KEY UPDATE</td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td>FOR UPDATE</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr></tbody></table>

<br>

<a id="LOCKING-PAGES"></a>

### 13.3.3. 頁面層級鎖定 [#](#LOCKING-PAGES)

除了資料表與資料列鎖定之外，還會使用頁面層級的共享／排他鎖定，來控制對共享緩衝池中資料表頁面的讀寫存取。這些鎖定會在擷取或更新資料列之後立即釋放。應用程式開發人員通常不需要關心頁面層級的鎖定，這裡提到它們只是為了完整起見。

<a id="LOCKING-DEADLOCKS"></a>

### 13.3.4. 死結 [#](#LOCKING-DEADLOCKS)

<a id="id-1.5.12.6.8.2"></a>

使用明確鎖定可能會增加發生*死結*（deadlock）的可能性，也就是兩個（或更多）交易各自持有對方想要的鎖定。例如，如果交易 1 在資料表 A 上取得排他鎖定，接著嘗試在資料表 B 上取得排他鎖定，而交易 2 已經對資料表 B 取得排他鎖定，現在又想在資料表 A 上取得排他鎖定，那麼兩者都無法繼續進行。PostgreSQL 會自動偵測死結的情況，並藉由中止其中一個相關交易來解決它，讓其他交易得以完成。（確切會中止哪一個交易很難預測，也不應依賴它。）

請注意，死結也可能因資料列層級的鎖定而發生（因此，即使沒有使用明確鎖定，也可能發生死結）。考慮兩個並行交易修改同一個資料表的情況。第一個交易執行：

```

UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 11111;
```

這會在具有指定帳號的資料列上取得資料列層級的鎖定。接著，第二個交易執行：

```

UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 22222;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 11111;
```

第一個 `UPDATE` 陳述式成功在指定的資料列上取得資料列層級的鎖定，因此成功更新了該資料列。不過，第二個 `UPDATE` 陳述式發現它嘗試更新的資料列已經被鎖定，所以它會等待取得該鎖定的交易完成。現在，交易二在繼續執行之前，要等待交易一完成。接著，交易一執行：

```

UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 22222;
```

交易一嘗試在指定的資料列上取得資料列層級的鎖定，但它無法取得：交易二已經持有這樣的鎖定。所以它會等待交易二完成。因此，交易一被交易二阻擋，而交易二又被交易一阻擋：這就是死結的情況。PostgreSQL 會偵測到這種情況，並中止其中一個交易。

防範死結最好的方法，通常是確保所有使用某個資料庫的應用程式，都以一致的順序取得多個物件上的鎖定，從而避免死結。在上面的範例中，如果兩個交易都以相同的順序更新資料列，就不會發生死結。你也應該確保，在交易中對某個物件取得的第一個鎖定，是該物件將會需要的最嚴格模式。如果無法事先確認這一點，那麼可以藉由重試因死結而中止的交易，即時處理死結。

只要沒有偵測到死結的情況，要求資料表層級或資料列層級鎖定的交易，就會無限期地等待互相衝突的鎖定被釋放。這表示讓應用程式長時間保持交易開啟（例如，在等待使用者輸入時）是個壞主意。

<a id="ADVISORY-LOCKS"></a>

### 13.3.5. 諮詢鎖定 [#](#ADVISORY-LOCKS)

<a id="id-1.5.12.6.9.2"></a><a id="id-1.5.12.6.9.3"></a>

PostgreSQL 提供了一種建立具有應用程式定義之意義的鎖定的方法。這些鎖定稱為*諮詢鎖定*（advisory lock），因為系統不會強制使用它們——正確使用它們是應用程式的責任。對於不太適合 MVCC 模型的鎖定策略，諮詢鎖定可能很有用。例如，諮詢鎖定的一個常見用途，是模擬所謂「平面檔案」（flat file）資料管理系統中典型的悲觀鎖定策略。雖然儲存在資料表中的旗標也能達到相同的目的，但諮詢鎖定比較快、可以避免資料表膨脹，而且會在工作階段結束時由伺服器自動清除。

在 PostgreSQL 中取得諮詢鎖定有兩種方式：在工作階段層級，或在交易層級。在工作階段層級取得的諮詢鎖定，會一直持有到被明確釋放或工作階段結束為止。與標準的鎖定要求不同，工作階段層級的諮詢鎖定要求不遵循交易語意：在後來被回復的交易中取得的鎖定，在回復之後仍會被持有；同樣地，即使呼叫的交易後來失敗，解除鎖定仍然有效。一個鎖定可以被其擁有的程序多次取得；每一次完成的鎖定要求，都必須有一個對應的解除鎖定要求，鎖定才會真正被釋放。另一方面，交易層級的鎖定要求，行為則比較像一般的鎖定要求：它們會在交易結束時自動釋放，而且沒有明確的解除鎖定操作。對於短期使用諮詢鎖定而言，這種行為通常比工作階段層級的行為更方便。對於同一個諮詢鎖定識別碼，工作階段層級與交易層級的鎖定要求會以預期的方式互相阻擋。如果某個工作階段已經持有某個諮詢鎖定，那麼它對該鎖定的額外要求一定會成功，即使有其他工作階段正在等待該鎖定也一樣；無論既有的鎖定持有與新的要求是在工作階段層級還是交易層級，這一點都成立。

就像 PostgreSQL 中所有的鎖定一樣，任何工作階段目前持有的諮詢鎖定完整清單，都可以在 [`pg_locks`](../../internals/views/view-pg-locks.md) 系統視圖中找到。

諮詢鎖定與一般鎖定都儲存在一個共享記憶體池中，其大小由組態變數 [max_locks_per_transaction](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-LOCKS-PER-TRANSACTION) 與 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 決定。必須小心不要耗盡這塊記憶體，否則伺服器將完全無法授予任何鎖定。這對伺服器可授予的諮詢鎖定數量設下了上限，視伺服器的設定而定，通常在數萬到數十萬之間。

在某些使用諮詢鎖定方法的情況下，特別是在涉及明確排序與 `LIMIT` 子句的查詢中，由於 SQL 運算式的評估順序，必須小心控制所取得的鎖定。例如：

```

SELECT pg_advisory_lock(id) FROM foo WHERE id = 12345; -- ok
SELECT pg_advisory_lock(id) FROM foo WHERE id > 12345 LIMIT 100; -- danger!
SELECT pg_advisory_lock(q.id) FROM
(
  SELECT id FROM foo WHERE id > 12345 LIMIT 100
) q; -- ok
```

在上面的查詢中，第二種形式很危險，因為無法保證 `LIMIT` 會在鎖定函式執行之前套用。這可能導致取得一些應用程式沒有預期到的鎖定，因此也就無法釋放它們（直到結束工作階段為止）。從應用程式的角度來看，這樣的鎖定會是懸置的，儘管仍然可以在 `pg_locks` 中看到。

用來操作諮詢鎖定的函式，說明於[第 9.28.10 節](../functions/functions-admin.md#FUNCTIONS-ADVISORY-LOCKS)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/explicit-locking.html)（原文版本：18.6；核對日期：2026-09-11）
