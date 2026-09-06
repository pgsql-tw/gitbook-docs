<a id="CATALOG-PG-DESCRIPTION"></a>

# 53.19. pg_description

<a id="id-1.10.4.21.2"></a>

The catalog `pg_description` stores optional descriptions (comments) for each database object. Descriptions can be manipulated with the [`COMMENT`](../../reference/sql-commands/comment.md) command and viewed with psql's `\d` commands. Descriptions of many built-in system objects are provided in the initial contents of `pg_description`.

See also [`pg_shdescription`](pg_shdescription.md), which performs a similar function for descriptions involving objects that are shared across a database cluster.

<a id="id-1.10.4.21.5"></a>

<strong>Table 53.19. <code class="structname">pg&#95;description</code> Columns</strong>

<table border="1" class="table" summary="pg_description Columns">
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
<p class="column_definition"><code class="structfield">objoid</code> <code class="type">oid</code> (references any OID column)</p>
<p>The OID of the object this description pertains to</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">classoid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the system catalog this object appears in</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">objsubid</code> <code class="type">int4</code></p>
<p>For a comment on a table column, this is the column number (the <code class="structfield">objoid</code> and <code class="structfield">classoid</code> refer to the table itself). For all other object types, this column is zero.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">description</code> <code class="type">text</code></p>
<p>Arbitrary text that serves as the description of this object</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-description.html)（英文原文，待翻譯）
