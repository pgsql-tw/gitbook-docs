## 52.26. `pg_index` [#](#CATALOG-PG-INDEX)

<a id="id-1.10.4.28.2"></a>

The catalog `pg_index` contains part of the information
about indexes. The rest is mostly in
[`pg_class`](catalog-pg-class.md).

<a id="id-1.10.4.28.4"></a>

**Table 52.26. `pg_index` Columns**

<table border="1" class="table" summary="pg_index Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> entry for this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> entry for the table this index is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnatts</code> <code class="type">int2</code>
</p>
<p>
       The total number of columns in the index (duplicates
       <code class="literal">pg_class.relnatts</code>); this number includes both key and included attributes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnkeyatts</code> <code class="type">int2</code>
</p>
<p>
       The number of <em class="firstterm">key columns</em> in the index,
       not counting any <em class="firstterm">included columns</em>, which are
       merely stored and do not participate in the index semantics
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisunique</code> <code class="type">bool</code>
</p>
<p>
       If true, this is a unique index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnullsnotdistinct</code> <code class="type">bool</code>
</p>
<p>
       This value is only used for unique indexes.  If false, this unique
       index will consider null values distinct (so the index can contain
       multiple null values in a column, the default PostgreSQL behavior).  If
       it is true, it will consider null values to be equal (so the index can
       only contain one null value in a column).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisprimary</code> <code class="type">bool</code>
</p>
<p>
       If true, this index represents the primary key of the table
       (<code class="structfield">indisunique</code> should always be true when this is true)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisexclusion</code> <code class="type">bool</code>
</p>
<p>
       If true, this index supports an exclusion constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indimmediate</code> <code class="type">bool</code>
</p>
<p>
       If true, the uniqueness check is enforced immediately on
       insertion
       (irrelevant if <code class="structfield">indisunique</code> is not true)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisclustered</code> <code class="type">bool</code>
</p>
<p>
       If true, the table was last clustered on this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisvalid</code> <code class="type">bool</code>
</p>
<p>
       If true, the index is currently valid for queries.  False means the
       index is possibly incomplete: it must still be modified by
       <a class="link" href="../../reference/sql-commands/sql-insert.md"><code class="command">INSERT</code></a>/<a class="link" href="../../reference/sql-commands/sql-update.md"><code class="command">UPDATE</code></a> operations, but it cannot safely
       be used for queries. If it is unique, the uniqueness property is not
       guaranteed true either.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indcheckxmin</code> <code class="type">bool</code>
</p>
<p>
       If true, queries must not use the index until the <code class="structfield">xmin</code>
       of this <code class="structname">pg_index</code> row is below their <code class="symbol">TransactionXmin</code>
       event horizon, because the table may contain broken <a class="link" href="../storage/storage-hot.md">HOT chains</a> with
       incompatible rows that they can see
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisready</code> <code class="type">bool</code>
</p>
<p>
       If true, the index is currently ready for inserts.  False means the
       index must be ignored by <a class="link" href="../../reference/sql-commands/sql-insert.md"><code class="command">INSERT</code></a>/<a class="link" href="../../reference/sql-commands/sql-update.md"><code class="command">UPDATE</code></a>
       operations.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indislive</code> <code class="type">bool</code>
</p>
<p>
       If false, the index is in process of being dropped, and should be
       ignored for all purposes (including HOT-safety decisions)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisreplident</code> <code class="type">bool</code>
</p>
<p>
       If true this index has been chosen as <span class="quote">“<span class="quote">replica identity</span>”</span>
       using <a class="link" href="../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY"><code class="command">ALTER TABLE ...
       REPLICA IDENTITY USING INDEX ...</code></a>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indkey</code> <code class="type">int2vector</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       This is an array of <code class="structfield">indnatts</code> values that
       indicate which table columns this index indexes.  For example, a value
       of <code class="literal">1 3</code> would mean that the first and the third table
       columns make up the index entries.  Key columns come before non-key
       (included) columns.  A zero in this array indicates that the
       corresponding index attribute is an expression over the table columns,
       rather than a simple column reference.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indcollation</code> <code class="type">oidvector</code>
       (references <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       For each column in the index key
       (<code class="structfield">indnkeyatts</code> values), this contains the OID
       of the collation to use for the index, or zero if the column is not of
       a collatable data type.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indclass</code> <code class="type">oidvector</code>
       (references <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       For each column in the index key
       (<code class="structfield">indnkeyatts</code> values), this contains the OID
       of the operator class to use.  See
       <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a> for details.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indoption</code> <code class="type">int2vector</code>
</p>
<p>
       This is an array of <code class="structfield">indnkeyatts</code> values that
       store per-column flag bits.  The meaning of the bits is defined by
       the index's access method.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexprs</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression trees (in <code class="function">nodeToString()</code>
       representation) for index attributes that are not simple column
       references.  This is a list with one element for each zero
       entry in <code class="structfield">indkey</code>.  Null if all index attributes
       are simple references.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indpred</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression tree (in <code class="function">nodeToString()</code>
       representation) for partial index predicate.  Null if not a
       partial index.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-index.html)（英文原文，待翻譯）
