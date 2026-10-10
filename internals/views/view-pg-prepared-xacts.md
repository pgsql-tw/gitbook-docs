<a id="VIEW-PG-PREPARED-XACTS"></a>

## 53.17. `pg_prepared_xacts` [#](#VIEW-PG-PREPARED-XACTS)

<a id="id-1.10.5.21.2"></a>

檢視表 `pg_prepared_xacts` 顯示目前已為兩階段提交而準備之交易的相關資訊（詳情請參閱 [PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md)）。

`pg_prepared_xacts` 中每個已準備交易各有一筆資料列。當交易被提交或回復時，對應的項目就會被移除。

<a id="id-1.10.5.21.5"></a>

**表 53.17. `pg_prepared_xacts` 欄位**

<table border="1" class="table" summary="表 53.17. pg_prepared_xacts 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">transaction</code> <code class="type">xid</code>
</p>
<p>
       已準備交易的數值交易識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">gid</code> <code class="type">text</code>
</p>
<p>
       指派給此交易的全域交易識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prepared</code> <code class="type">timestamptz</code>
</p>
<p>
       此交易為提交而準備完成的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">owner</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       執行此交易之使用者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">datname</code>）
      </p>
<p>
       執行此交易之資料庫的名稱
      </p></td></tr></tbody></table>

<br>

存取 `pg_prepared_xacts` 檢視表時，內部交易管理器的資料結構會被短暫鎖定，並製作一份副本供此檢視表顯示。這能確保此檢視表產生一致的結果集，同時不會阻擋一般操作超過必要的時間。儘管如此，若頻繁存取此檢視表，仍可能對資料庫效能造成一些影響。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-prepared-xacts.html)（原文版本：18.6；核對日期：2026-10-10）
