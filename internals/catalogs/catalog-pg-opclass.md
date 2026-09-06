## 52.33. `pg_opclass` [#](#CATALOG-PG-OPCLASS)

<a id="id-1.10.4.35.2"></a>

The catalog `pg_opclass` defines
index access method operator classes. Each operator class defines
semantics for index columns of a particular data type and a particular
index access method. An operator class essentially specifies that a
particular operator family is applicable to a particular indexable column
data type. The set of operators from the family that are actually usable
with the indexed column are whichever ones accept the column's data type
as their left-hand input.

Operator classes are described at length in [Section 36.16](../../server-programming/extend/xindex.md).

<a id="id-1.10.4.35.5"></a>

**Table 52.33. `pg_opclass` Columns**

<table border="1" class="table" summary="pg_opclass Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">opcmethod</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Index access method operator class is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcname</code> <code class="type">name</code>
</p>
<p>
       Name of this operator class
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Namespace of this operator class
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the operator class
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcfamily</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Operator family containing the operator class
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcintype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Data type that the operator class indexes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcdefault</code> <code class="type">bool</code>
</p>
<p>
       True if this operator class is the default for <code class="structfield">opcintype</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opckeytype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Type of data stored in index, or zero if same as <code class="structfield">opcintype</code>
</p></td></tr></tbody></table>

<br>

An operator class's `opcmethod` must match the
`opfmethod` of its containing operator family.
Also, there must be no more than one `pg_opclass`
row having `opcdefault` true for any given combination of
`opcmethod` and `opcintype`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-opclass.html)（英文原文，待翻譯）
