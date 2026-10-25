<a id="VIEW-PG-HBA-FILE-RULES"></a>

## 53.10. `pg_hba_file_rules` [#](#view-pg-hba-file-rules) <a href="#view-pg-hba-file-rules" id="view-pg-hba-file-rules"></a>

<a id="id-1.10.5.14.2"></a>

檢視表 `pg_hba_file_rules` 提供用戶端認證設定檔 [`pg_hba.conf`](../../server-administration/client-authentication/auth-pg-hba-conf.md) 內容的摘要。檔案中每一個非空白、非註解的行，都會在此檢視表中以一個資料列呈現，並附有註記說明該規則是否能成功套用。

此檢視表可以協助檢查認證設定檔中預計進行的變更是否可行，或用於診斷先前的失敗。請注意，此檢視表回報的是檔案的*目前*內容，而不是伺服器最後載入的內容。

預設情況下，只有超級使用者可以讀取 `pg_hba_file_rules` 檢視表。

<a id="id-1.10.5.14.6"></a>

**表 53.10. `pg_hba_file_rules` 欄位**

<table border="1" class="table" summary="表 53.10. pg_hba_file_rules 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rule_number</code> <code class="type">int4</code>
</p>
<p>
       若此規則有效，則為此規則的編號，否則為 <code class="literal">NULL</code>。它表示在認證期間，直到找到相符的規則為止，各規則被檢查的順序。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">file_name</code> <code class="type">text</code>
</p>
<p>
       包含此規則的檔案名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">line_number</code> <code class="type">int4</code>
</p>
<p>
       此規則在 <code class="literal">file_name</code> 中的行號
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       連線類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">text[]</code>
</p>
<p>
       此規則所適用的資料庫名稱清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_name</code> <code class="type">text[]</code>
</p>
<p>
       此規則所適用的使用者與群組名稱清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">address</code> <code class="type">text</code>
</p>
<p>
       主機名稱或 IP 位址，或是 <code class="literal">all</code>、<code class="literal">samehost</code>、<code class="literal">samenet</code> 其中之一；若為本機連線則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">netmask</code> <code class="type">text</code>
</p>
<p>
       IP 位址遮罩；若不適用則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">auth_method</code> <code class="type">text</code>
</p>
<p>
       認證方法
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">options</code> <code class="type">text[]</code>
</p>
<p>
       為認證方法指定的選項（若有）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">error</code> <code class="type">text</code>
</p>
<p>
       若不為 null，則為說明此行為何無法處理的錯誤訊息
      </p></td></tr></tbody></table>

<br>

通常，反映錯誤項目的資料列只會在 `line_number` 與 `error` 欄位中有值。

關於用戶端認證設定的更多資訊，請參閱[第 20 章](../../server-administration/client-authentication/README.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-hba-file-rules.html)（原文版本：18.6；核對日期：2026-10-09）
