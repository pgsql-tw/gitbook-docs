<a id="VIEW-PG-AVAILABLE-EXTENSION-VERSIONS"></a>

## 53.4. `pg_available_extension_versions` [#](#VIEW-PG-AVAILABLE-EXTENSION-VERSIONS)

<a id="id-1.10.5.8.2"></a>

檢視表 `pg_available_extension_versions` 列出可供安裝的各個擴充功能特定版本。另請參閱 [`pg_extension`](../catalogs/catalog-pg-extension.md)
系統目錄，它顯示目前已安裝的擴充功能。

<a id="id-1.10.5.8.4"></a>

**表 53.4. `pg_available_extension_versions` 欄位**

<table border="1" class="table" summary="表 53.4. pg_available_extension_versions 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">version</code> <code class="type">text</code>
</p>
<p>
       版本名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">installed</code> <code class="type">bool</code>
</p>
<p>
       若此擴充功能的這個版本目前已安裝，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">superuser</code> <code class="type">bool</code>
</p>
<p>
       若只允許超級使用者安裝此擴充功能，則為 true
       （但請參閱 <code class="structfield">trusted</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trusted</code> <code class="type">bool</code>
</p>
<p>
       若具有適當權限的非超級使用者可以安裝此擴充功能，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relocatable</code> <code class="type">bool</code>
</p>
<p>
       若擴充功能可以重新定位到另一個綱要，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema</code> <code class="type">name</code>
</p>
<p>
       擴充功能必須安裝到的綱要名稱；若為部分或完全可重新定位，則為 <code class="literal">NULL</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">requires</code> <code class="type">name[]</code>
</p>
<p>
       先決擴充功能的名稱；若沒有則為 <code class="literal">NULL</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comment</code> <code class="type">text</code>
</p>
<p>
       來自擴充功能控制檔的註解字串
      </p></td></tr></tbody></table>

<br>

`pg_available_extension_versions` 檢視表是唯讀的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-available-extension-versions.html)（原文版本：18.6；核對日期：2026-10-12）
