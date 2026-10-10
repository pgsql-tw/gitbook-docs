<a id="VIEW-PG-FILE-SETTINGS"></a>

## 53.8. `pg_file_settings` [#](#VIEW-PG-FILE-SETTINGS)

<a id="id-1.10.5.12.2"></a>

檢視表 `pg_file_settings` 提供伺服器設定檔內容的摘要。檔案中出現的每一筆「name = value」項目，都會在此檢視表中以一個資料列呈現，並附有註記說明該值是否能成功套用。對於與「name = value」項目無關的問題（例如檔案中的語法錯誤），可能會出現額外的資料列。

此檢視表有助於檢查設定檔中預計進行的變更是否可行，或用於診斷先前的失敗。請注意，此檢視表回報的是檔案的*目前*內容，而不是伺服器最後套用的內容。（要判斷後者，通常使用 [`pg_settings`](view-pg-settings.md) 檢視表就已足夠。）

預設情況下，只有超級使用者可以讀取 `pg_file_settings` 檢視表。

<a id="id-1.10.5.12.6"></a>

**表 53.8. `pg_file_settings` 欄位**

<table border="1" class="table" summary="表 53.8. pg_file_settings 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourcefile</code> <code class="type">text</code>
</p>
<p>
       設定檔的完整路徑名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourceline</code> <code class="type">int4</code>
</p>
<p>
       該項目在設定檔中出現的行號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqno</code> <code class="type">int4</code>
</p>
<p>
       各項目被處理的順序（1..<em class="replaceable"><code>n</code></em>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       設定參數名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setting</code> <code class="type">text</code>
</p>
<p>
       要指派給該參數的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">applied</code> <code class="type">bool</code>
</p>
<p>
       若該值可以成功套用，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">error</code> <code class="type">text</code>
</p>
<p>
       若不為 null，則為說明此項目為何無法套用的錯誤訊息
      </p></td></tr></tbody></table>

<br>

若設定檔包含語法錯誤或無效的參數名稱，伺服器將不會嘗試套用其中的任何設定，因此所有 `applied` 欄位都會顯示為 false。在這種情況下，會有一個或多個資料列的 `error` 欄位不為 null，用以指出問題所在。否則，個別設定會在可能的情況下被套用。若某個設定無法套用（例如值無效，或該設定在伺服器啟動後無法變更），其 `error` 欄位中會有相應的訊息。項目出現 `applied` = false 的另一種可能情況是：它被後面同一參數名稱的項目覆寫；這種情況不視為錯誤，因此 `error` 欄位中不會出現任何內容。

關於變更執行期參數之各種方式的更多資訊，請參閱[第 19.1 節](../../server-administration/runtime-config/config-setting.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-file-settings.html)（原文版本：18.6；核對日期：2026-10-09）
