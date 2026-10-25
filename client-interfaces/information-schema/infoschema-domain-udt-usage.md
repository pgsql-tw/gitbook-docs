<a id="INFOSCHEMA-DOMAIN-UDT-USAGE"></a>
## 35.22. `domain_udt_usage` [#](#infoschema-domain-udt-usage) <a href="#infoschema-domain-udt-usage" id="infoschema-domain-udt-usage"></a>

檢視表 `domain_udt_usage` 列出以目前已啟用角色所擁有之資料型別為基礎的所有網域。請注意，在 PostgreSQL 中，內建資料型別的行為如同使用者定義型別，因此它們也包含在此處。

<a id="id-1.7.6.26.3"></a>

**表 35.20. `domain_udt_usage` 欄位**

<table border="1" class="table" summary="domain_udt_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該網域之資料型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該網域之資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該網域之資料型別的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       網域名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-domain-udt-usage.html)（原文版本：18.6；核對日期：2026-10-18）
