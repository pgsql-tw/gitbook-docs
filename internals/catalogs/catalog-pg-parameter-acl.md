<a id="CATALOG-PG-PARAMETER-ACL"></a>

## 52.36. `pg_parameter_acl` [#](#CATALOG-PG-PARAMETER-ACL)

<a id="id-1.10.4.38.2"></a>

目錄 `pg_parameter_acl` 記錄已將權限授予一個或多個角色的設定參數。具有預設權限的參數不會建立項目。

與大多數系統目錄不同，`pg_parameter_acl` 由叢集中的所有資料庫共用：每個叢集只有一份 `pg_parameter_acl`，而不是每個資料庫各一份。

<a id="id-1.10.4.38.5"></a>

**表 52.36. `pg_parameter_acl` 欄位**

<table border="1" class="table" summary="表 52.36. pg_parameter_acl 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">parname</code> <code class="type">text</code>
</p>
<p>
       已授予權限之設定參數的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">paracl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-parameter-acl.html)（原文版本：18.6；核對日期：2026-10-17）
