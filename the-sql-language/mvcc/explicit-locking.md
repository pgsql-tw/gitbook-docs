<a id="EXPLICIT-LOCKING"></a>

## 13.3. 明確鎖定 [#](#explicit-locking) <a href="#explicit-locking" id="explicit-locking"></a>

[13.3.1. 資料表層級鎖定](explicit-locking/locking-tables.md#locking-tables)

[13.3.2. 資料列層級鎖定](explicit-locking/locking-rows.md#locking-rows)

[13.3.3. 頁面層級鎖定](explicit-locking.md#locking-pages)

[13.3.4. 死結](explicit-locking.md#locking-deadlocks)

[13.3.5. 諮詢鎖定](explicit-locking.md#advisory-locks)

<a id="id-1.5.12.6.2"></a>

PostgreSQL 提供了多種鎖定模式，用來控制對資料表中資料的並行存取。在 MVCC 無法提供所需行為的情況下，這些模式可用於由應用程式控制的鎖定。此外，大多數 PostgreSQL 命令會自動取得適當模式的鎖定，以確保在命令執行期間，被參照的資料表不會被刪除或以不相容的方式修改。（例如，`TRUNCATE` 無法安全地與同一資料表上的其他操作並行執行，因此它會在該資料表上取得 `ACCESS EXCLUSIVE` 鎖定來強制做到這一點。）

要檢視資料庫伺服器中目前尚未釋放的鎖定清單，請使用 [`pg_locks`](../../internals/views/view-pg-locks.md) 系統視圖。關於監控鎖定管理子系統狀態的更多資訊，請參閱[第 27 章](../../server-administration/monitoring/README.md)。

### 13.3.1. 資料表層級鎖定 [#](#locking-tables) <a href="#locking-tables" id="locking-tables"></a>

完整內容請見 [13.3.1. 資料表層級鎖定](explicit-locking/locking-tables.md#locking-tables)。

### 13.3.2. 資料列層級鎖定 [#](#locking-rows) <a href="#locking-rows" id="locking-rows"></a>

完整內容請見 [13.3.2. 資料列層級鎖定](explicit-locking/locking-rows.md#locking-rows)。

<a id="LOCKING-PAGES"></a>

### 13.3.3. 頁面層級鎖定 [#](#locking-pages) <a href="#locking-pages" id="locking-pages"></a>

除了資料表與資料列鎖定之外，還會使用頁面層級的共享／排他鎖定，來控制對共享緩衝池中資料表頁面的讀寫存取。這些鎖定會在擷取或更新資料列之後立即釋放。應用程式開發人員通常不需要關心頁面層級的鎖定，這裡提到它們只是為了完整起見。

<a id="LOCKING-DEADLOCKS"></a>

### 13.3.4. 死結 [#](#locking-deadlocks) <a href="#locking-deadlocks" id="locking-deadlocks"></a>

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

### 13.3.5. 諮詢鎖定 [#](#advisory-locks) <a href="#advisory-locks" id="advisory-locks"></a>

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

用來操作諮詢鎖定的函式，說明於[第 9.28.10 節](../functions/functions-admin/functions-advisory-locks.md#functions-advisory-locks)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/explicit-locking.html)（原文版本：18.6；核對日期：2026-09-11）
