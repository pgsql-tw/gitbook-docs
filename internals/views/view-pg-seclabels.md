<a id="VIEW-PG-SECLABELS"></a>

## 53.23. `pg_seclabels` [#](#view-pg-seclabels) <a href="#view-pg-seclabels" id="view-pg-seclabels"></a>

<a id="id-1.10.5.27.2"></a>

檢視表 `pg_seclabels` 提供關於安全標籤的資訊。它是 [`pg_seclabel`](../catalogs/catalog-pg-seclabel.md) 系統目錄較容易查詢的版本。

<a id="id-1.10.5.27.4"></a>

**表 53.23. `pg_seclabels` 欄位**

<table border="1" class="table" summary="表 53.23. pg_seclabels 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       此安全標籤所屬之物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此物件所在之系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位上的安全標籤，這是欄位編號（<code class="structfield">objoid</code> 與 <code class="structfield">classoid</code> 參照資料表本身）。對於其他所有物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objtype</code> <code class="type">text</code>
</p>
<p>
       此標籤所套用之物件的類型，以文字表示。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此物件之命名空間的 OID（若適用）；否則為 NULL。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objname</code> <code class="type">text</code>
</p>
<p>
       此標籤所套用之物件的名稱，以文字表示。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provider</code> <code class="type">text</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-seclabel.md"><code class="structname">pg_seclabel</code></a>.<code class="structfield">provider</code>）
      </p>
<p>
       與此標籤關聯的標籤提供者。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">label</code> <code class="type">text</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-seclabel.md"><code class="structname">pg_seclabel</code></a>.<code class="structfield">label</code>）
      </p>
<p>
       套用於此物件的安全標籤。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-seclabels.html)（原文版本：18.6；核對日期：2026-10-10）
