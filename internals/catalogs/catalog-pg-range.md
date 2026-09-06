## 52.43. `pg_range` [#](#CATALOG-PG-RANGE)

<a id="id-1.10.4.45.2"></a>

The catalog `pg_range` stores information about
range types. This is in addition to the types' entries in
[`pg_type`](catalog-pg-type.md).

<a id="id-1.10.4.45.4"></a>

**Table 52.43. `pg_range` Columns**

<table border="1" class="table" summary="pg_range Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngtypid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the range type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubtype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the element type (subtype) of this range type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngmultitypid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the multirange type for this range type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngcollation</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the collation used for range comparisons, or zero if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubopc</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the subtype's operator class used for range comparisons
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngcanonical</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the function to convert a range value into canonical form,
       or zero if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubdiff</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the function to return the difference between two element
       values as <code class="type">double precision</code>, or zero if none
      </p></td></tr></tbody></table>

<br>

`rngsubopc` (plus `rngcollation`, if the
element type is collatable) determines the sort ordering used by the range
type. `rngcanonical` is used when the element type is
discrete. `rngsubdiff` is optional but should be supplied to
improve performance of GiST indexes on the range type.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-range.html)（英文原文，待翻譯）
