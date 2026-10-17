<a id="CATALOG-PG-NAMESPACE"></a>

## 52.32. `pg_namespace` [#](#CATALOG-PG-NAMESPACE)

<a id="id-1.10.4.34.2"></a>

目錄 `pg_namespace` 存放命名空間。命名空間是 SQL 綱要底層的結構：每個命名空間都可以擁有各自獨立的一組關聯、型別等，而不會發生名稱衝突。

<a id="id-1.10.4.34.4"></a>

**表 52.32. `pg_namespace` 欄位**

<table border="1" class="table" summary="表 52.32. pg_namespace 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">nspname</code> <code class="type">name</code>
</p>
<p>
       命名空間的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nspowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       命名空間的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nspacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-namespace.html)（原文版本：18.6；核對日期：2026-10-17）
