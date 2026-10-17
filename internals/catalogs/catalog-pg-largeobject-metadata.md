<a id="CATALOG-PG-LARGEOBJECT-METADATA"></a>

## 52.31. `pg_largeobject_metadata` [#](#CATALOG-PG-LARGEOBJECT-METADATA)

<a id="id-1.10.4.33.2"></a>

目錄 `pg_largeobject_metadata` 存放與大型物件相關聯的中繼資料。大型物件的實際資料存放在 [`pg_largeobject`](catalog-pg-largeobject.md) 中。

<a id="id-1.10.4.33.4"></a>

**表 52.31. `pg_largeobject_metadata` 欄位**

<table border="1" class="table" summary="表 52.31. pg_largeobject_metadata 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">lomowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       大型物件的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lomacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-largeobject-metadata.html)（原文版本：18.6；核對日期：2026-10-17）
