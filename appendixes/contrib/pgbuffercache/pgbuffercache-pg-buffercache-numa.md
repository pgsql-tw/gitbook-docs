# F.25.2. pg_buffercache_numa 檢視表

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-NUMA"></a>

## F.25.2. `pg_buffercache_numa` 檢視表 [#](#pgbuffercache-pg-buffercache-numa) <a href="#pgbuffercache-pg-buffercache-numa" id="pgbuffercache-pg-buffercache-numa"></a>

此檢視表所提供欄位的定義如[表 F.15](#pgbuffercache-numa-columns)所示。

<a id="PGBUFFERCACHE-NUMA-COLUMNS"></a>

### 表 F.15. `pg_buffercache_numa` 欄位 [#](#pgbuffercache-numa-columns) <a href="#pgbuffercache-numa-columns" id="pgbuffercache-numa-columns"></a>

<table border="1" class="table" summary="pg_buffercache_numa 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">os_page_num</code> <code class="type">bigint</code>
</p>
<p>
       此緩衝區所在的作業系統記憶體頁面編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numa_node</code> <code class="type">int</code>
</p>
<p>
       <acronym class="acronym">NUMA</acronym> 節點的 ID
      </p></td></tr></tbody></table>

<br>

由於查詢每個頁面的 NUMA 節點 ID 需要先將記憶體頁面調入（page in），此函式第一次執行時可能需要相當可觀的時間。在所有情況下（無論是否為第一次執行），擷取此資訊的成本都很高，因此不建議高頻率查詢此檢視表。

### 警告

在判定 NUMA 節點時，此檢視表會存取（touch）共享記憶體區段的所有記憶體頁面。若共享記憶體尚未配置，這會強制配置它，而且記憶體可能會被配置在單一 NUMA 節點上（取決於系統設定）。

[返回 F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](../pgbuffercache.md#pgbuffercache)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
