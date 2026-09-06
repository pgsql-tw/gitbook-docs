## 53.19. `pg_replication_origin_status` [#](#VIEW-PG-REPLICATION-ORIGIN-STATUS)

<a id="id-1.10.5.23.2"></a>

The `pg_replication_origin_status` view
contains information about how far replay for a certain origin has
progressed. For more on replication origins
see [Chapter 48](../../server-programming/replication-origins/README.md).

<a id="id-1.10.5.23.4"></a>

**Table 53.19. `pg_replication_origin_status` Columns**

<table border="1" class="table" summary="pg_replication_origin_status Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_id</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-replication-origin.md"><code class="structname">pg_replication_origin</code></a>.<code class="structfield">roident</code>)
      </p>
<p>
       internal node identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_id</code> <code class="type">text</code>
       (references <a class="link" href="../catalogs/catalog-pg-replication-origin.md"><code class="structname">pg_replication_origin</code></a>.<code class="structfield">roname</code>)
      </p>
<p>
       external node identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">remote_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       The origin node's LSN up to which data has been replicated.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       This node's LSN at which <code class="literal">remote_lsn</code> has
       been replicated. Used to flush commit records before persisting
       data to disk when using asynchronous commits.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-replication-origin-status.html)（英文原文，待翻譯）
