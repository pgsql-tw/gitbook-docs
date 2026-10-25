<a id="VIEW-PG-IDENT-FILE-MAPPINGS"></a>

## 53.11. `pg_ident_file_mappings` [#](#view-pg-ident-file-mappings) <a href="#view-pg-ident-file-mappings" id="view-pg-ident-file-mappings"></a>

<a id="id-1.10.5.15.2"></a>

檢視表 `pg_ident_file_mappings` 提供用戶端使用者名稱對應設定檔 [`pg_ident.conf`](../../server-administration/client-authentication/auth-username-maps.md) 內容的摘要。檔案中每一個非空白、非註解的行，都會在此檢視表中呈現為一筆資料列，並附有註記，指出該對應能否成功套用。

此檢視表有助於檢查對認證設定檔所規劃的變更是否可行，或診斷先前的失敗。請注意，此檢視表回報的是檔案*目前*的內容，而不是伺服器最後載入的內容。

預設情況下，只有超級使用者可讀取 `pg_ident_file_mappings` 檢視表。

<a id="id-1.10.5.15.6"></a>

**表 53.11. `pg_ident_file_mappings` 欄位**

<table border="1" class="table" summary="表 53.11. pg_ident_file_mappings 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">map_number</code> <code class="type">int4</code>
</p>
<p>
       若有效，則為此對應依優先順序的編號；否則為 <code class="literal">NULL</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">file_name</code> <code class="type">text</code>
</p>
<p>
       包含此對應之檔案的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">line_number</code> <code class="type">int4</code>
</p>
<p>
       此對應在 <code class="literal">file_name</code> 中的行號
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">map_name</code> <code class="type">text</code>
</p>
<p>
       對應名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sys_name</code> <code class="type">text</code>
</p>
<p>
       偵測到的用戶端使用者名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pg_username</code> <code class="type">text</code>
</p>
<p>
       所要求的 PostgreSQL 使用者名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">error</code> <code class="type">text</code>
</p>
<p>
       若不為 <code class="literal">NULL</code>，則為說明此行為何無法處理的錯誤訊息
      </p></td></tr></tbody></table>

<br>

通常，反映錯誤項目的資料列只會在 `line_number` 與 `error` 欄位中有值。

關於用戶端認證設定的更多資訊，請參閱[第 20 章](../../server-administration/client-authentication/README.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-ident-file-mappings.html)（原文版本：18.6；核對日期：2026-10-09）
