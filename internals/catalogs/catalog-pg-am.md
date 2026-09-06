## 52.3. `pg_am` [#](#CATALOG-PG-AM)

<a id="id-1.10.4.5.2"></a>

The catalog `pg_am` stores information about
relation access methods. There is one row for each access method supported
by the system.
Currently, only tables and indexes have access methods. The requirements for table
and index access methods are discussed in detail in [Chapter 62](../tableam/README.md) and
[Chapter 63](../indexam/README.md) respectively.

<a id="id-1.10.4.5.4"></a>

**Table 52.3. `pg_am` Columns**

<table border="1" class="table" summary="pg_am Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amname</code> <code class="type">name</code>
</p>
<p>
       Name of the access method
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amhandler</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of a handler function that is responsible for supplying information
       about the access method
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amtype</code> <code class="type">char</code>
</p>
<p>
<code class="literal">t</code> = table (including materialized views),
       <code class="literal">i</code> = index.
      </p></td></tr></tbody></table>

<br>

### Note

Before PostgreSQL 9.6, `pg_am`
contained many additional columns representing properties of index access
methods. That data is now only directly visible at the C code level.
However, `pg_index_column_has_property()` and related
functions have been added to allow SQL queries to inspect index access
method properties; see [Table 9.76](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-am.html)（英文原文，待翻譯）
