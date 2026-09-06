<a id="VIEW-PG-PREPARED-STATEMENTS"></a>

# 54.15. pg_prepared_statements

<a id="id-1.10.5.19.2"></a>

The `pg_prepared_statements` view displays all the prepared statements that are available in the current session. See [PREPARE](../../reference/sql-commands/prepare.md) for more information about prepared statements.

`pg_prepared_statements` contains one row for each prepared statement. Rows are added to the view when a new prepared statement is created and removed when a prepared statement is released (for example, via the [`DEALLOCATE`](../../reference/sql-commands/deallocate.md) command).

<a id="id-1.10.5.19.5"></a>

<strong>Table 54.15. <code class="structname">pg&#95;prepared&#95;statements</code> Columns</strong>

<table border="1" class="table" summary="pg_prepared_statements Columns">
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
<p>The identifier of the prepared statement</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">statement</code> <code class="type">text</code></p>
<p>The query string submitted by the client to create this prepared statement. For prepared statements created via SQL, this is the <code class="command">PREPARE</code> statement submitted by the client. For prepared statements created via the frontend/backend protocol, this is the text of the prepared statement itself.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">prepare_time</code> <code class="type">timestamptz</code></p>
<p>The time at which the prepared statement was created</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">parameter_types</code> <code class="type">regtype[]</code></p>
<p>The expected parameter types for the prepared statement in the form of an array of <code class="type">regtype</code>. The OID corresponding to an element of this array can be obtained by casting the <code class="type">regtype</code> value to <code class="type">oid</code>.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">from_sql</code> <code class="type">bool</code></p>
<p><code class="literal">true</code> if the prepared statement was created via the <code class="command">PREPARE</code> SQL command; <code class="literal">false</code> if the statement was prepared via the frontend/backend protocol</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">generic_plans</code> <code class="type">int8</code></p>
<p>Number of times generic plan was chosen</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">custom_plans</code> <code class="type">int8</code></p>
<p>Number of times custom plan was chosen</p>
</td>
</tr>
</tbody>
</table>



The `pg_prepared_statements` view is read-only.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/view-pg-prepared-statements.html)（英文原文，待翻譯）
