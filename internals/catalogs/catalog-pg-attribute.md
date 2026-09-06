## 52.7. `pg_attribute` [#](#CATALOG-PG-ATTRIBUTE)

<a id="id-1.10.4.9.2"></a>

The catalog `pg_attribute` stores information about
table columns. There will be exactly one
`pg_attribute` row for every column in every
table in the database. (There will also be attribute entries for
indexes, and indeed all objects that have
[`pg_class`](catalog-pg-class.md)
entries.)

The term attribute is equivalent to column and is used for
historical reasons.

<a id="id-1.10.4.9.5"></a>

**Table 52.7. `pg_attribute` Columns**

<table border="1" class="table" summary="pg_attribute Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table this column belongs to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attname</code> <code class="type">name</code>
</p>
<p>
       The column name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atttypid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The data type of this column (zero for a dropped column)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attlen</code> <code class="type">int2</code>
</p>
<p>
       A copy of <code class="literal">pg_type.typlen</code> of this column's
       type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnum</code> <code class="type">int2</code>
</p>
<p>
       The number of the column.  Ordinary columns are numbered from 1
       up.  System columns, such as <code class="structfield">ctid</code>,
       have (arbitrary) negative numbers.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atttypmod</code> <code class="type">int4</code>
</p>
<p>
<code class="structfield">atttypmod</code> records type-specific data
       supplied at table creation time (for example, the maximum
       length of a <code class="type">varchar</code> column).  It is passed to
       type-specific input functions and length coercion functions.
       The value will generally be -1 for types that do not need <code class="structfield">atttypmod</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attndims</code> <code class="type">int2</code>
</p>
<p>
       Number of dimensions, if the column is an array type; otherwise 0.
       (Presently, the number of dimensions of an array is not enforced,
       so any nonzero value effectively means <span class="quote">“<span class="quote">it's an array</span>”</span>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attbyval</code> <code class="type">bool</code>
</p>
<p>
       A copy of <code class="literal">pg_type.typbyval</code> of this column's type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attalign</code> <code class="type">char</code>
</p>
<p>
       A copy of <code class="literal">pg_type.typalign</code> of this column's type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attstorage</code> <code class="type">char</code>
</p>
<p>
       Normally a copy of <code class="literal">pg_type.typstorage</code> of this
       column's type.  For TOAST-able data types, this can be altered
       after column creation to control storage policy.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attcompression</code> <code class="type">char</code>
</p>
<p>
       The current compression method of the column.  Typically this is
       <code class="literal">'\0'</code> to specify use of the current default setting
       (see <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION">default_toast_compression</a>).  Otherwise,
       <code class="literal">'p'</code> selects pglz compression, while
       <code class="literal">'l'</code> selects <span class="productname">LZ4</span>
       compression.  However, this field is ignored
       whenever <code class="structfield">attstorage</code> does not allow
       compression.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnotnull</code> <code class="type">bool</code>
</p>
<p>
       This column has a (possibly invalid) not-null constraint.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atthasdef</code> <code class="type">bool</code>
</p>
<p>
       This column has a default expression or generation expression, in which
       case there will be a corresponding entry in the
       <a class="link" href="catalog-pg-attrdef.md"><code class="structname">pg_attrdef</code></a> catalog that actually defines the
       expression.  (Check <code class="structfield">attgenerated</code> to
       determine whether this is a default or a generation expression.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atthasmissing</code> <code class="type">bool</code>
</p>
<p>
       This column has a value which is used where the column is entirely
       missing from the row, as happens when a column is added with a
       non-volatile <code class="literal">DEFAULT</code> value after the row is created.
       The actual value used is stored in the
       <code class="structfield">attmissingval</code> column.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attidentity</code> <code class="type">char</code>
</p>
<p>
       If a zero byte (<code class="literal">''</code>), then not an identity column.
       Otherwise, <code class="literal">a</code> = generated
       always, <code class="literal">d</code> = generated by default.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attgenerated</code> <code class="type">char</code>
</p>
<p>
       If a zero byte (<code class="literal">''</code>), then not a generated column.
       Otherwise, <code class="literal">s</code> = stored, <code class="literal">v</code> =
       virtual.  A stored generated column is physically stored like a normal
       column.  A virtual generated column is physically stored as a null
       value, with the actual value being computed at run time.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attisdropped</code> <code class="type">bool</code>
</p>
<p>
       This column has been dropped and is no longer valid.  A dropped
       column is still physically present in the table, but is
       ignored by the parser and so cannot be accessed via SQL.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attislocal</code> <code class="type">bool</code>
</p>
<p>
       This column is defined locally in the relation.  Note that a column can
       be locally defined and inherited simultaneously.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attinhcount</code> <code class="type">int2</code>
</p>
<p>
       The number of direct ancestors this column has.  A column with a
       nonzero number of ancestors cannot be dropped nor renamed.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attcollation</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The defined collation of the column, or zero if the column is
       not of a collatable data type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attstattarget</code> <code class="type">int2</code>
</p>
<p>
<code class="structfield">attstattarget</code> controls the level of detail
       of statistics accumulated for this column by
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>.
       A zero value indicates that no statistics should be collected.
       A null value says to use the system default statistics target.
       The exact meaning of positive values is data type-dependent.
       For scalar data types, <code class="structfield">attstattarget</code>
       is both the target number of <span class="quote">“<span class="quote">most common values</span>”</span>
       to collect, and the target number of histogram bins to create.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Column-level access privileges, if any have been granted specifically
       on this column
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attoptions</code> <code class="type">text[]</code>
</p>
<p>
       Attribute-level options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attfdwoptions</code> <code class="type">text[]</code>
</p>
<p>
       Attribute-level foreign data wrapper options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attmissingval</code> <code class="type">anyarray</code>
</p>
<p>
       This column has a one element array containing the value used when the
       column is entirely missing from the row, as happens when the column is
       added with a non-volatile <code class="literal">DEFAULT</code> value after the
       row is created.  The value is only used when
       <code class="structfield">atthasmissing</code> is true.  If there is no value
       the column is null.
      </p></td></tr></tbody></table>

<br>

In a dropped column's `pg_attribute` entry,
`atttypid` is reset to zero, but
`attlen` and the other fields copied from
[`pg_type`](catalog-pg-type.md) are still valid. This arrangement is needed
to cope with the situation where the dropped column's data type was
later dropped, and so there is no `pg_type` row anymore.
`attlen` and the other fields can be used
to interpret the contents of a row of the table.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-attribute.html)（英文原文，待翻譯）
