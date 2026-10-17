<a id="VIEW-PG-AVAILABLE-EXTENSIONS"></a>

## 53.3. `pg_available_extensions` [#](#VIEW-PG-AVAILABLE-EXTENSIONS)

<a id="id-1.10.5.7.2"></a>

檢視表 `pg_available_extensions` 列出可供安裝的擴充功能。另請參閱
[`pg_extension`](../catalogs/catalog-pg-extension.md)
系統目錄，它顯示目前已安裝的擴充功能。

<a id="id-1.10.5.7.4"></a>

**表 53.3. `pg_available_extensions` 欄位**

<table border="1" class="table" summary="表 53.3. pg_available_extensions 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">name</code>
</p>
<p>
       擴充功能名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_version</code> <code class="type">text</code>
</p>
<p>
       預設版本的名稱；若未指定則為 <code class="literal">NULL</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">installed_version</code> <code class="type">text</code>
</p>
<p>
       目前已安裝的擴充功能版本；若未安裝則為 <code class="literal">NULL</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comment</code> <code class="type">text</code>
</p>
<p>
       來自擴充功能控制檔的註解字串
      </p></td></tr></tbody></table>

<br>

`pg_available_extensions` 檢視表是唯讀的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-available-extensions.html)（原文版本：18.6；核對日期：2026-10-12）
