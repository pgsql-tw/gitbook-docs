<a id="CATALOG-PG-OPFAMILY"></a>

# 53.35. pg_opfamily

<a id="id-1.10.4.37.2"></a>

The catalog `pg_opfamily` defines operator families. Each operator family is a collection of operators and associated support routines that implement the semantics specified for a particular index access method. Furthermore, the operators in a family are all “compatible”, in a way that is specified by the access method. The operator family concept allows cross-data-type operators to be used with indexes and to be reasoned about using knowledge of access method semantics.

Operator families are described at length in [Section 38.16](../../server-programming/extending-sql/interfacing-extensions-to-indexes.md).

<a id="id-1.10.4.37.5"></a>

<strong>Table 53.35. <code class="structname">pg&#95;opfamily</code> Columns</strong>

<table border="1" class="table" summary="pg_opfamily Columns">
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
<p class="column_definition"><code class="structfield">opfmethod</code> <code class="type">oid</code> (references <a class="link" href="pg_am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>)</p>
<p>Index access method operator family is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">opfname</code> <code class="type">name</code></p>
<p>Name of this operator family</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">opfnamespace</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>Namespace of this operator family</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">opfowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the operator family</p>
</td>
</tr>
</tbody>
</table>



The majority of the information defining an operator family is not in its `pg_opfamily` row, but in the associated rows in [`pg_amop`](pg_amop.md), [`pg_amproc`](pg_amproc.md), and [`pg_opclass`](pg_opclass.md).

---

原文：[PostgreSQL 15.19 Documentation](pg_opfamily.md)（英文原文，待翻譯）
