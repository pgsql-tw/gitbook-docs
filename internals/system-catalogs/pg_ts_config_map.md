<a id="CATALOG-PG-TS-CONFIG-MAP"></a>

# 53.60. pg_ts_config_map

<a id="id-1.10.4.62.2"></a>

The `pg_ts_config_map` catalog contains entries showing which text search dictionaries should be consulted, and in what order, for each output token type of each text search configuration's parser.

PostgreSQL's text search features are described at length in [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md).

<a id="id-1.10.4.62.5"></a>

<strong>Table 53.60. <code class="structname">pg&#95;ts&#95;config&#95;map</code> Columns</strong>

<table border="1" class="table" summary="pg_ts_config_map Columns">
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
<p class="column_definition"><code class="structfield">mapcfg</code> <code class="type">oid</code> (references <a class="link" href="pg_ts_config.md"><code class="structname">pg_ts_config</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the <a class="link" href="pg_ts_config.md"><code class="structname">pg_ts_config</code></a> entry owning this map entry</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">maptokentype</code> <code class="type">int4</code></p>
<p>A token type emitted by the configuration's parser</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">mapseqno</code> <code class="type">int4</code></p>
<p>Order in which to consult this entry (lower <code class="structfield">mapseqno</code>s first)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">mapdict</code> <code class="type">oid</code> (references <a class="link" href="pg_ts_dict.md"><code class="structname">pg_ts_dict</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the text search dictionary to consult</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_ts_config_map.md)（英文原文，待翻譯）
