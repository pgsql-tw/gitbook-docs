<a id="PGROWLOCKS"></a>

## F.31. pgrowlocks — 顯示資料表的資料列鎖定資訊 [#](#pgrowlocks) <a href="#pgrowlocks" id="pgrowlocks"></a>

[F.31.1. 概觀](pgrowlocks.md#PGROWLOCKS-OVERVIEW)

[F.31.2. 輸出範例](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)

[F.31.3. 作者](pgrowlocks.md#PGROWLOCKS-AUTHOR)

<a id="id-1.11.7.41.2"></a>

`pgrowlocks` 模組提供一個函式，用來顯示指定資料表的資料列鎖定資訊。

預設情況下，只有超級使用者、具有 `pg_stat_scan_tables` 角色權限的角色，以及對該資料表具有 `SELECT` 權限的使用者可以使用。

<a id="PGROWLOCKS-OVERVIEW"></a>

### F.31.1. 概觀 [#](#PGROWLOCKS-OVERVIEW)

<a id="id-1.11.7.41.5.2"></a>

```

pgrowlocks(text) returns setof record
```

參數是資料表的名稱。結果是一組紀錄，資料表中每個被鎖定的資料列各對應一筆。輸出欄位如[表 F.21](pgrowlocks.md#PGROWLOCKS-COLUMNS) 所示。

<a id="PGROWLOCKS-COLUMNS"></a>

**表 F.21. `pgrowlocks` 輸出欄位**

<table border="1" class="table" summary="pgrowlocks 輸出欄位"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">locked_row</code></td><td><code class="type">tid</code></td><td>被鎖定資料列的元組 ID（TID）</td></tr><tr><td><code class="structfield">locker</code></td><td><code class="type">xid</code></td><td>鎖定者的交易 ID；若為多重交易（multitransaction），則為 multixact ID；請參閱<a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a></td></tr><tr><td><code class="structfield">multi</code></td><td><code class="type">boolean</code></td><td>若鎖定者為多重交易則為真</td></tr><tr><td><code class="structfield">xids</code></td><td><code class="type">xid[]</code></td><td>鎖定者的交易 ID（若為多重交易則超過一個）</td></tr><tr><td><code class="structfield">modes</code></td><td><code class="type">text[]</code></td><td>鎖定者的鎖定模式（若為多重交易則超過一個），為由 <code class="literal">For Key Share</code>、<code class="literal">For Share</code>、
       <code class="literal">For No Key Update</code>、<code class="literal">No Key Update</code>、
       <code class="literal">For Update</code>、<code class="literal">Update</code> 組成的陣列。</td></tr><tr><td><code class="structfield">pids</code></td><td><code class="type">integer[]</code></td><td>持有鎖定之後端的程序 ID（若為多重交易則超過一個）</td></tr></tbody></table>

<br>

`pgrowlocks` 會對目標資料表取得 `AccessShareLock`，並逐一讀取每個資料列以收集資料列鎖定資訊。對大型資料表而言，這並不是很快。請注意：

1. 若資料表上已取得 `ACCESS EXCLUSIVE` 鎖定，
   `pgrowlocks` 會被阻擋。
2. `pgrowlocks` 不保證產生自身一致的快照。在它執行期間，可能有新的資料列鎖定被取得，或有舊的鎖定被釋放。

`pgrowlocks` 不會顯示被鎖定資料列的內容。若你想同時查看資料列內容，可以這樣做：

```

SELECT * FROM accounts AS a, pgrowlocks('accounts') AS p
  WHERE p.locked_row = a.ctid;
```

不過請注意，這樣的查詢效率會非常差。

<a id="PGROWLOCKS-SAMPLE-OUTPUT"></a>

### F.31.2. 輸出範例 [#](#PGROWLOCKS-SAMPLE-OUTPUT)

```

=# SELECT * FROM pgrowlocks('t1');
 locked_row | locker | multi | xids  |     modes      |  pids
------------+--------+-------+-------+----------------+--------
 (0,1)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,2)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,3)      |    607 | f     | {607} | {"For Update"} | {3107}
 (0,4)      |    607 | f     | {607} | {"For Update"} | {3107}
(4 rows)
```

<a id="PGROWLOCKS-AUTHOR"></a>

### F.31.3. 作者 [#](#PGROWLOCKS-AUTHOR)

Tatsuo Ishii

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgrowlocks.html)（原文版本：18.6；核對日期：2026-10-23）
