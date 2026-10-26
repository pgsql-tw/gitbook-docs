<a id="VIEW-PG-LOCKS"></a>

## 53.13. `pg_locks` [#](#view-pg-locks) <a href="#view-pg-locks" id="view-pg-locks"></a>

<a id="id-1.10.5.17.2"></a>

檢視表 `pg_locks` 提供資料庫伺服器內各個活動中程序所持有之鎖定的相關資訊。關於鎖定的更多討論，請參閱[第 13 章](../../the-sql-language/mvcc/README.md)。

`pg_locks` 中，每個「活動中的可鎖定物件、所請求的鎖定模式與相關程序」的組合各占一筆資料列。因此，如果有多個程序在同一個可鎖定物件上持有或等待鎖定，該物件可能會出現許多次。不過，目前沒有任何鎖定的物件完全不會出現。

可鎖定物件分為數種不同的類型：整個關聯（例如資料表）、關聯中的個別頁面、關聯中的個別 tuple、交易 ID（包括虛擬 ID 與永久 ID），以及一般資料庫物件（以類別 OID 與物件 OID 識別，方式與 [`pg_description`](../catalogs/catalog-pg-description.md) 或 [`pg_depend`](../catalogs/catalog-pg-depend.md) 相同）。此外，擴充關聯的權利也以一個獨立的可鎖定物件表示，更新 `pg_database`.`datfrozenxid` 的權利也是如此。另外，也可以對具有使用者自訂意義的數字取得「諮詢」鎖定。

<a id="id-1.10.5.17.6"></a>

**表 53.13. `pg_locks` 欄位**

<table border="1" class="table" summary="表 53.13. pg_locks 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">locktype</code> <code class="type">text</code>
</p>
<p>
       可鎖定物件的類型：
       <code class="literal">relation</code>、
       <code class="literal">extend</code>、
       <code class="literal">frozenid</code>、
       <code class="literal">page</code>、
       <code class="literal">tuple</code>、
       <code class="literal">transactionid</code>、
       <code class="literal">virtualxid</code>、
       <code class="literal">spectoken</code>、
       <code class="literal">object</code>、
       <code class="literal">userlock</code>、
       <code class="literal">advisory</code> 或
       <code class="literal">applytransaction</code>。
       （另請參閱<a class="xref" href="../../server-administration/monitoring/monitoring-stats.md#WAIT-EVENT-LOCK-TABLE">表 27.11</a>。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       鎖定目標所在之資料庫的 OID；若目標是共享物件則為零；若目標是交易 ID 則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relation</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       鎖定所針對之關聯的 OID；若目標不是關聯，也不是關聯的一部分，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">page</code> <code class="type">int4</code>
</p>
<p>
       鎖定所針對之頁面在該關聯內的頁碼；若目標不是關聯頁面，也不是 tuple，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuple</code> <code class="type">int2</code>
</p>
<p>
       鎖定所針對之 tuple 在該頁面內的編號；若目標不是 tuple，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">virtualxid</code> <code class="type">text</code>
</p>
<p>
       鎖定所針對之交易的虛擬 ID；若目標不是虛擬交易 ID，則為 null；請參閱
       <a class="xref" href="../transactions/README.md">第 67 章</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">transactionid</code> <code class="type">xid</code>
</p>
<p>
       鎖定所針對之交易的 ID；若目標不是交易 ID，則為 null；<a class="xref" href="../transactions/README.md">第 67 章</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含鎖定目標之系統目錄的 OID；若目標不是一般資料庫物件，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       鎖定目標在其系統目錄中的 OID；若目標不是一般資料庫物件，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int2</code>
</p>
<p>
       鎖定所針對的欄位編號（此時
       <code class="structfield">classid</code> 與 <code class="structfield">objid</code> 指的是該資料表本身）；
       若目標是其他一般資料庫物件，則為零；
       若目標不是一般資料庫物件，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">virtualtransaction</code> <code class="type">text</code>
</p>
<p>
       持有或正在等待此鎖定之交易的虛擬 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">int4</code>
</p>
<p>
       持有或正在等待此鎖定之伺服器程序的程序 ID；若此鎖定由預備交易持有，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mode</code> <code class="type">text</code>
</p>
<p>
       此程序所持有或想要取得之鎖定模式的名稱（請參閱<a class="xref" href="../../the-sql-language/mvcc/explicit-locking.md#locking-tables">第 13.3.1 節</a>與<a class="xref" href="../../the-sql-language/mvcc/transaction-iso.md#xact-serializable">第 13.2.3 節</a>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">granted</code> <code class="type">bool</code>
</p>
<p>
       若已持有鎖定則為 true，若正在等待鎖定則為 false
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fastpath</code> <code class="type">bool</code>
</p>
<p>
       若鎖定是透過快速路徑（fast path）取得則為 true，若是透過主鎖定表取得則為 false
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">waitstart</code> <code class="type">timestamptz</code>
</p>
<p>
       伺服器程序開始等待此鎖定的時間；若已持有該鎖定則為 null。
       請注意，即使 <code class="structfield">granted</code>
       為 <code class="literal">false</code>，在等待開始後的極短時間內，此值仍可能為 null。
      </p></td></tr></tbody></table>

<br>

在代表指定程序所持有之鎖定的資料列中，`granted` 為 true。false 表示此程序目前正在等待取得此鎖定，這意味著至少有一個其他程序正在同一個可鎖定物件上持有或等待一個相衝突的鎖定模式。等待中的程序會休眠，直到另一個鎖定被釋放（或偵測到死結狀況）為止。單一程序一次最多只能等待取得一個鎖定。

在交易執行的整個期間，伺服器程序都會在該交易的虛擬交易 ID 上持有排他鎖定。如果有永久 ID 指派給該交易（通常只有在交易變更資料庫狀態時才會發生），它也會在該交易的永久交易 ID 上持有排他鎖定，直到交易結束為止。當某個程序認為有必要特地等待另一個交易結束時，它的做法是嘗試在另一個交易的 ID（依情況為虛擬 ID 或永久 ID）上取得共享鎖定。這只有在另一個交易終止並釋放其鎖定時才會成功。

雖然 tuple 是一種可鎖定的物件類型，但資料列層級鎖定的資訊是儲存在磁碟上，而不是記憶體中，因此資料列層級鎖定通常不會出現在此檢視表中。如果某個程序正在等待資料列層級鎖定，它在檢視表中通常會顯示為正在等待該資料列鎖定目前持有者的永久交易 ID。

推測性插入（speculative insertion）鎖定由一個交易 ID 與一個推測性插入權杖組成。推測性插入權杖顯示在 `objid` 欄位中。

諮詢鎖定可以在由單一 `bigint` 值或兩個整數值所組成的鍵上取得。`bigint` 鍵的顯示方式是：高位半部在 `classid` 欄位中，低位半部在 `objid` 欄位中，且 `objsubid` 等於 1。原始的 `bigint` 值可以用運算式 `(classid::bigint << 32) |
objid::bigint` 重新組合。整數鍵的顯示方式是：第一個鍵在 `classid` 欄位中，第二個鍵在 `objid` 欄位中，且 `objsubid` 等於 2。這些鍵的實際意義由使用者決定。諮詢鎖定是各資料庫各自獨立的，因此對諮詢鎖定而言，`database` 欄位是有意義的。

套用交易（apply transaction）鎖定用於在邏輯複寫中以平行模式套用交易。遠端交易 ID 顯示在 `transactionid` 欄位中。`objsubid` 顯示鎖定的子類型：用於同步變更集合的鎖定為 0，用於等待交易完成以確保提交順序的鎖定為 1。

`pg_locks` 提供整個資料庫叢集中所有鎖定的全域檢視，而不只是與目前資料庫相關的鎖定。雖然可以將它的 `relation` 欄位與 [`pg_class`](../catalogs/catalog-pg-class.md).`oid` 連接，以識別被鎖定的關聯，但這只對目前資料庫中的關聯（也就是 `database` 欄位為目前資料庫的 OID 或零的那些關聯）才能正確運作。

可以將 `pid` 欄位與 [`pg_stat_activity`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW) 檢視表的 `pid` 欄位連接，以取得持有或等待各個鎖定之工作階段的更多資訊，例如

```

SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
    ON pl.pid = psa.pid;
```

此外，如果你使用預備交易，可以將 `virtualtransaction` 欄位與 [`pg_prepared_xacts`](view-pg-prepared-xacts.md) 檢視表的 `transaction` 欄位連接，以取得持有鎖定之預備交易的更多資訊。（預備交易永遠不可能正在等待鎖定，但它會繼續持有在執行期間所取得的鎖定。）例如：

```

SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
    ON pl.virtualtransaction = '-1/' || ppx.transaction;
```

雖然可以將 `pg_locks` 與自身連接，來取得哪些程序阻擋了哪些其他程序的資訊，但要在細節上做到完全正確非常困難。這樣的查詢必須編寫「哪些鎖定模式與哪些其他鎖定模式相衝突」的知識。更糟的是，`pg_locks` 檢視表並不會揭露在鎖定等待佇列中哪些程序排在哪些其他程序之前的資訊，也不會揭露哪些程序是代表哪些其他用戶端工作階段執行的平行工作程序。比較好的做法是使用 `pg_blocking_pids()` 函式（請參閱[表 9.71](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)），來識別等待中的程序被哪個（或哪些）程序所阻擋。

`pg_locks` 檢視表會顯示來自一般鎖定管理器與謂詞鎖管理器的資料，兩者是各自獨立的系統；此外，一般鎖定管理器又將其鎖定細分為一般鎖定與*快速路徑（fast-path）*鎖定。這些資料並不保證完全一致。查詢此檢視表時，快速路徑鎖定（`fastpath` = `true`）的資料是逐一從各個後端收集而來，過程中不會凍結整個鎖定管理器的狀態，因此在收集資訊的期間，可能有鎖定被取得或釋放。不過請注意，已知這些鎖定不會與目前存在的任何其他鎖定相衝突。在向所有後端查詢過快速路徑鎖定之後，一般鎖定管理器的其餘部分會作為一個整體被鎖定，並以一個不可分割的動作，收集所有剩餘鎖定的一致快照。在解除一般鎖定管理器的鎖定之後，謂詞鎖管理器也會以同樣的方式被鎖定，並以一個不可分割的動作收集所有謂詞鎖。因此，除了快速路徑鎖定之外，每個鎖定管理器都會提供一組一致的結果；但由於我們不會同時鎖定兩個鎖定管理器，因此在我們查詢一般鎖定管理器之後、查詢謂詞鎖管理器之前，仍有可能有鎖定被取得或釋放。

如果此檢視表被非常頻繁地存取，鎖定一般鎖定管理器及／或謂詞鎖管理器可能會對資料庫效能產生一些影響。這些鎖定只會持有從鎖定管理器取得資料所需的最短時間，但這並不能完全消除影響效能的可能性。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-locks.html)（原文版本：18.6；核對日期：2026-10-10）
