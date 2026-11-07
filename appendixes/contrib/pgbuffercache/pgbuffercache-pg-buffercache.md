# F.25.1. pg_buffercache 檢視表

<a id="PGBUFFERCACHE-PG-BUFFERCACHE"></a>

## F.25.1. `pg_buffercache` 檢視表 [#](#pgbuffercache-pg-buffercache) <a href="#pgbuffercache-pg-buffercache" id="pgbuffercache-pg-buffercache"></a>

此檢視表所提供欄位的定義如[表 F.14](#pgbuffercache-columns)所示。

<a id="PGBUFFERCACHE-COLUMNS"></a>

### 表 F.14. `pg_buffercache` 欄位 [#](#pgbuffercache-columns) <a href="#pgbuffercache-columns" id="pgbuffercache-columns"></a>

<table border="1" class="table" summary="pg_buffercache 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bufferid</code> <code class="type">integer</code>
</p>
<p>
       ID，範圍為 1..<code class="varname">shared_buffers</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfilenode</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../../internals/catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relfilenode</code>）
      </p>
<p>
       關聯的檔案節點（filenode）編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltablespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../../internals/catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       關聯的資料表空間 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reldatabase</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../../internals/catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       關聯的資料庫 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relforknumber</code> <code class="type">smallint</code>
</p>
<p>
       關聯內的分支（fork）編號；請參閱
       <code class="filename">common/relpath.h</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relblocknumber</code> <code class="type">bigint</code>
</p>
<p>
       關聯內的頁面編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">isdirty</code> <code class="type">boolean</code>
</p>
<p>
       頁面是否為髒頁？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usagecount</code> <code class="type">smallint</code>
</p>
<p>
       時鐘掃描（clock-sweep）存取計數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pinning_backends</code> <code class="type">integer</code>
</p>
<p>
       釘住此緩衝區的後端數量
      </p></td></tr></tbody></table>

<br>

共享快取中的每個緩衝區各有一個資料列。未使用的緩衝區除了 `bufferid` 以外，所有欄位皆顯示為 null。共享的系統目錄會顯示為屬於資料庫 0。

由於快取由所有資料庫共享，通常會有來自不屬於目前資料庫之關聯的頁面。這表示對某些資料列而言，`pg_class` 中可能沒有可與之連接的對應資料列，甚至可能產生不正確的連接。若你要與 `pg_class` 連接，最好將連接限制在 `reldatabase` 等於目前資料庫的 OID 或 0 的資料列。

由於複製此檢視表要顯示的緩衝區狀態資料時，不會取得緩衝區管理器的鎖定，存取 `pg_buffercache` 檢視表對正常緩衝區活動的影響較小，但它無法提供在所有緩衝區之間一致的結果集。不過，我們會確保每個緩衝區的資訊本身是一致的。

[返回 F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](../pgbuffercache.md#pgbuffercache)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
