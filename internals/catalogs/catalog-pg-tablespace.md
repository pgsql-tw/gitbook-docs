<a id="CATALOG-PG-TABLESPACE"></a>

## 52.56. `pg_tablespace` [#](#catalog-pg-tablespace) <a href="#catalog-pg-tablespace" id="catalog-pg-tablespace"></a>

<a id="id-1.10.4.58.2"></a>

目錄 `pg_tablespace` 儲存可用資料表空間的相關資訊。資料表可以放在特定的資料表空間中，以協助管理磁碟配置。

與大多數系統目錄不同，`pg_tablespace` 由叢集中的所有資料庫共用：每個叢集只有一份 `pg_tablespace`，而不是每個資料庫各一份。

<a id="id-1.10.4.58.5"></a>

**表 52.56. `pg_tablespace` 欄位**

<table border="1" class="table" summary="表 52.56. pg_tablespace 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">spcname</code> <code class="type">name</code>
</p>
<p>
       資料表空間名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       資料表空間的擁有者，通常是建立它的使用者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳情請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcoptions</code> <code class="type">text[]</code>
</p>
<p>
       資料表空間層級的選項，以<span class="quote">“<span class="quote">keyword=value</span>”</span>形式的字串表示
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-tablespace.html)（原文版本：18.6；核對日期：2026-10-17）
