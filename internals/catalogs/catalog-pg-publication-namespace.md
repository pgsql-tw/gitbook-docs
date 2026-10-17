<a id="CATALOG-PG-PUBLICATION-NAMESPACE"></a>

## 52.41. `pg_publication_namespace` [#](#CATALOG-PG-PUBLICATION-NAMESPACE)

<a id="id-1.10.4.43.2"></a>

目錄 `pg_publication_namespace` 記錄資料庫中綱要與發佈之間的對應關係。這是多對多的對應。

<a id="id-1.10.4.43.4"></a>

**表 52.41. `pg_publication_namespace` 欄位**

<table border="1" class="table" summary="表 52.41. pg_publication_namespace 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pnpubid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       所參照的發佈
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pnnspid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       所參照的綱要
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-publication-namespace.html)（原文版本：18.6；核對日期：2026-10-17）
