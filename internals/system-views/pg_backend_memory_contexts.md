<a id="VIEW-PG-BACKEND-MEMORY-CONTEXTS"></a>

# 54.4. pg_backend_memory_contexts

<a id="id-1.10.5.8.2"></a>

The view `pg_backend_memory_contexts` displays all the memory contexts of the server process attached to the current session.

`pg_backend_memory_contexts` contains one row for each memory context.

<a id="id-1.10.5.8.5"></a>

<strong>Table 54.4. <code class="structname">pg&#95;backend&#95;memory&#95;contexts</code> Columns</strong>

<table border="1" class="table" summary="pg_backend_memory_contexts Columns">
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
<p class="column_definition"><code class="structfield">name</code> <code class="type">text</code></p>
<p>Name of the memory context</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">ident</code> <code class="type">text</code></p>
<p>Identification information of the memory context. This field is truncated at 1024 bytes</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">parent</code> <code class="type">text</code></p>
<p>Name of the parent of this memory context</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">level</code> <code class="type">int4</code></p>
<p>Distance from TopMemoryContext in context tree</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">total_bytes</code> <code class="type">int8</code></p>
<p>Total bytes allocated for this memory context</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">total_nblocks</code> <code class="type">int8</code></p>
<p>Total number of blocks allocated for this memory context</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">free_bytes</code> <code class="type">int8</code></p>
<p>Free space in bytes</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">free_chunks</code> <code class="type">int8</code></p>
<p>Total number of free chunks</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">used_bytes</code> <code class="type">int8</code></p>
<p>Used space in bytes</p>
</td>
</tr>
</tbody>
</table>



By default, the `pg_backend_memory_contexts` view can be read only by superusers or roles with the privileges of the `pg_read_all_stats` role.

---

原文：[PostgreSQL 15.19 Documentation](pg_backend_memory_contexts.md)（英文原文，待翻譯）
