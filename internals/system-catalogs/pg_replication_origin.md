<a id="CATALOG-PG-REPLICATION-ORIGIN"></a>

# 53.44. pg_replication_origin

<a id="id-1.10.4.46.2"></a>

The `pg_replication_origin` catalog contains all replication origins created. For more on replication origins see [Chapter 50](../../server-programming/replication-progress-tracking.md).

Unlike most system catalogs, `pg_replication_origin` is shared across all databases of a cluster: there is only one copy of `pg_replication_origin` per cluster, not one per database.

<a id="id-1.10.4.46.5"></a>

<strong>Table 53.44. <code class="structname">pg&#95;replication&#95;origin</code> Columns</strong>

<table border="1" class="table" summary="pg_replication_origin Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">Column Type</p>
<p>Description</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">roident</code> <code class="type">oid</code></p>
<p>A unique, cluster-wide identifier for the replication origin. Should never leave the system.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">roname</code> <code class="type">text</code></p>
<p>The external, user defined, name of a replication origin.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-replication-origin.html)（英文原文，待翻譯）
