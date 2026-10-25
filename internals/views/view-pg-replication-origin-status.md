<a id="VIEW-PG-REPLICATION-ORIGIN-STATUS"></a>

## 53.19. `pg_replication_origin_status` [#](#view-pg-replication-origin-status) <a href="#view-pg-replication-origin-status" id="view-pg-replication-origin-status"></a>

<a id="id-1.10.5.23.2"></a>

檢視表 `pg_replication_origin_status` 包含特定來源的重播已推進到何處的資訊。關於複寫來源的更多資訊，請參閱[第 48 章](../../server-programming/replication-origins/README.md)。

<a id="id-1.10.5.23.4"></a>

**表 53.19. `pg_replication_origin_status` 欄位**

<table border="1" class="table" summary="表 53.19. pg_replication_origin_status 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_id</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-replication-origin.md"><code class="structname">pg_replication_origin</code></a>.<code class="structfield">roident</code>）
      </p>
<p>
       內部節點識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_id</code> <code class="type">text</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-replication-origin.md"><code class="structname">pg_replication_origin</code></a>.<code class="structfield">roname</code>）
      </p>
<p>
       外部節點識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">remote_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       來源節點上資料已複寫到的 LSN 位置。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       <code class="literal">remote_lsn</code> 被複寫時，本節點所在的 LSN。使用非同步提交時，用來在將資料持久寫入磁碟之前排清提交紀錄。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-replication-origin-status.html)（原文版本：18.6；核對日期：2026-10-10）
