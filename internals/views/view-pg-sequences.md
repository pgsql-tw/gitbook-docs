## 53.24. `pg_sequences` [#](#VIEW-PG-SEQUENCES)

<a id="id-1.10.5.28.2"></a>

The view `pg_sequences` provides access to
useful information about each sequence in the database.

<a id="id-1.10.5.28.4"></a>

**Table 53.24. `pg_sequences` Columns**

<table border="1" class="table" summary="pg_sequences Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequencename</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequenceowner</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of sequence's owner
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">regtype</code>
       (references <a class="link" href="../catalogs/catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Data type of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">start_value</code> <code class="type">int8</code>
</p>
<p>
       Start value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_value</code> <code class="type">int8</code>
</p>
<p>
       Minimum value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_value</code> <code class="type">int8</code>
</p>
<p>
       Maximum value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">increment_by</code> <code class="type">int8</code>
</p>
<p>
       Increment value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cycle</code> <code class="type">bool</code>
</p>
<p>
       Whether the sequence cycles
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cache_size</code> <code class="type">int8</code>
</p>
<p>
       Cache size of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_value</code> <code class="type">int8</code>
</p>
<p>
       The last sequence value written to disk.  If caching is used,
       this value can be greater than the last value handed out from the
       sequence.
      </p></td></tr></tbody></table>

<br>

The `last_value` column will read as null if any of
the following are true:

* The sequence has not been read from yet.
* The current user does not have `USAGE` or
  `SELECT` privilege on the sequence.
* The sequence is unlogged and the server is a standby.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-sequences.html)（英文原文，待翻譯）
