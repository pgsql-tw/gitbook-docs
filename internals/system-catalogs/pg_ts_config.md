<a id="CATALOG-PG-TS-CONFIG"></a>

# 53.59. pg_ts_config

<a id="id-1.10.4.61.2"></a>

The `pg_ts_config` catalog contains entries representing text search configurations. A configuration specifies a particular text search parser and a list of dictionaries to use for each of the parser's output token types. The parser is shown in the `pg_ts_config` entry, but the token-to-dictionary mapping is defined by subsidiary entries in [`pg_ts_config_map`](pg_ts_config_map.md).

PostgreSQL's text search features are described at length in [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md).

<a id="id-1.10.4.61.5"></a>

<strong>Table 53.59. <code class="structname">pg&#95;ts&#95;config</code> Columns</strong>

<table border="1" class="table" summary="pg_ts_config Columns">
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
<p class="column_definition"><code class="structfield">oid</code> <code class="type">oid</code></p>
<p>Row identifier</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">cfgname</code> <code class="type">name</code></p>
<p>Text search configuration name</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">cfgnamespace</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the namespace that contains this configuration</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">cfgowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the configuration</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">cfgparser</code> <code class="type">oid</code> (references <a class="link" href="pg_ts_parser.md"><code class="structname">pg_ts_parser</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the text search parser for this configuration</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_ts_config.md)（英文原文，待翻譯）
