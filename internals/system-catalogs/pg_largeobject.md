<a id="CATALOG-PG-LARGEOBJECT"></a>

# 53.30. pg_largeobject

<a id="id-1.10.4.32.2"></a>

The catalog `pg_largeobject` holds the data making up “large objects”. A large object is identified by an OID assigned when it is created. Each large object is broken into segments or “pages” small enough to be conveniently stored as rows in `pg_largeobject`. The amount of data per page is defined to be `LOBLKSIZE` (which is currently `BLCKSZ/4`, or typically 2 kB).

Prior to PostgreSQL 9.0, there was no permission structure associated with large objects. As a result, `pg_largeobject` was publicly readable and could be used to obtain the OIDs (and contents) of all large objects in the system. This is no longer the case; use [`pg_largeobject_metadata`](pg_largeobject_metadata.md) to obtain a list of large object OIDs.

<a id="id-1.10.4.32.5"></a>

<strong>Table 53.30. <code class="structname">pg&#95;largeobject</code> Columns</strong>

<table border="1" class="table" summary="pg_largeobject Columns">
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
<p class="column_definition"><code class="structfield">loid</code> <code class="type">oid</code> (references <a class="link" href="pg_largeobject_metadata.md"><code class="structname">pg_largeobject_metadata</code></a>.<code class="structfield">oid</code>)</p>
<p>Identifier of the large object that includes this page</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pageno</code> <code class="type">int4</code></p>
<p>Page number of this page within its large object (counting from zero)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">data</code> <code class="type">bytea</code></p>
<p>Actual data stored in the large object. This will never be more than <code class="symbol">LOBLKSIZE</code> bytes and might be less.</p>
</td>
</tr>
</tbody>
</table>



Each row of `pg_largeobject` holds data for one page of a large object, beginning at byte offset (`pageno * LOBLKSIZE`) within the object. The implementation allows sparse storage: pages might be missing, and might be shorter than `LOBLKSIZE` bytes even if they are not the last page of the object. Missing regions within a large object read as zeroes.

---

原文：[PostgreSQL 15.19 Documentation](pg_largeobject.md)（英文原文，待翻譯）
