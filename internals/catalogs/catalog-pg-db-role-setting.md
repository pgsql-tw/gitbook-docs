<a id="CATALOG-PG-DB-ROLE-SETTING"></a>

## 52.16. `pg_db_role_setting` [#](#CATALOG-PG-DB-ROLE-SETTING)

<a id="id-1.10.4.18.2"></a>

系統目錄 `pg_db_role_setting` 記錄針對每一種角色與資料庫組合所設定的執行階段設定變數預設值。

與大多數系統目錄不同，`pg_db_role_setting` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_db_role_setting`，而不是每個資料庫各一份。

<a id="id-1.10.4.18.5"></a>

**表 52.16. `pg_db_role_setting` 欄位**

<table border="1" class="table" summary="表 52.16. pg_db_role_setting 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setdatabase</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此設定所適用之資料庫的 OID；若不限定特定資料庫則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setrole</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此設定所適用之角色的 OID；若不限定特定角色則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setconfig</code> <code class="type">text[]</code>
</p>
<p>
       執行階段設定變數的預設值
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-db-role-setting.html)（原文版本：18.6；核對日期：2026-10-17）
