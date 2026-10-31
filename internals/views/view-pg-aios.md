<a id="VIEW-PG-AIOS"></a>

## 53.2. `pg_aios` [#](#view-pg-aios) <a href="#view-pg-aios" id="view-pg-aios"></a>

<a id="id-1.10.5.6.2"></a>

檢視表 `pg_aios` 列出目前使用中的所有[非同步 I/O](../../appendixes/glossary/README.md#glossary-aio) 控制代碼。I/O 控制代碼用來參照一個正在準備、正在執行或正在完成中的 I/O 操作。`pg_aios` 中，每個 I/O 控制代碼各占一筆資料列。

此檢視表主要對 PostgreSQL 的開發者有用，但在調校 PostgreSQL 時也可能有幫助。

<a id="id-1.10.5.6.5"></a>

**表 53.2. `pg_aios` 欄位**

<table border="1" class="table" summary="表 53.2. pg_aios 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">int4</code>
</p>
<p>
       發出此 I/O 之伺服器程序的程序 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">io_id</code> <code class="type">int4</code>
</p>
<p>
       I/O 控制代碼的識別碼。I/O 完成後（或控制代碼在 I/O 開始之前就被釋放時），控制代碼會被重複使用。重複使用時，
       <a class="link" href="view-pg-aios.md#VIEW-PG-AIOS-IO-GENERATION">
<code class="structname">pg_aios</code>.<code class="structfield">io_generation</code>
</a>
       會遞增。
      </p></td></tr><tr><td class="catalog_table_entry" id="VIEW-PG-AIOS-IO-GENERATION"><p class="column_definition">
<code class="structfield">io_generation</code> <code class="type">int8</code>
</p>
<p>
       I/O 控制代碼的世代。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state</code> <code class="type">text</code>
</p>
<p>
       I/O 控制代碼的狀態：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">HANDED_OUT</code>：已被程式碼參照，但尚未使用
         </p></li><li class="listitem"><p>
<code class="literal">DEFINED</code>：已知執行所需的資訊
         </p></li><li class="listitem"><p>
<code class="literal">STAGED</code>：已準備好執行
         </p></li><li class="listitem"><p>
<code class="literal">SUBMITTED</code>：已送出執行
         </p></li><li class="listitem"><p>
<code class="literal">COMPLETED_IO</code>：已完成，但結果尚未處理
         </p></li><li class="listitem"><p>
<code class="literal">COMPLETED_SHARED</code>：共享的完成處理已完成
         </p></li><li class="listitem"><p>
<code class="literal">COMPLETED_LOCAL</code>：後端本地的完成處理已完成
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">operation</code> <code class="type">text</code>
</p>
<p>
       使用此 I/O 控制代碼執行的操作：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">invalid</code>：尚未得知
         </p></li><li class="listitem"><p>
<code class="literal">readv</code>：向量化讀取
         </p></li><li class="listitem"><p>
<code class="literal">writev</code>：向量化寫入
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">off</code> <code class="type">int8</code>
</p>
<p>
       I/O 操作的位移量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">length</code> <code class="type">int8</code>
</p>
<p>
       I/O 操作的長度。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">target</code> <code class="type">text</code>
</p>
<p>
       此 I/O 所針對的物件種類：
       </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">smgr</code>：對關聯進行的 I/O
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">handle_data_len</code> <code class="type">int2</code>
</p>
<p>
       與此 I/O 操作相關聯的資料長度。對於寫入或讀取
       <a class="xref" href="../../server-administration/runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS">shared_buffers</a> 與 <a class="xref" href="../../server-administration/runtime-config/runtime-config-resource.md#GUC-TEMP-BUFFERS">temp_buffers</a> 的 I/O，此值表示該 I/O 所操作的緩衝區數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">raw_result</code> <code class="type">int4</code>
</p>
<p>
       I/O 操作的低階結果；若操作尚未完成則為 NULL。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result</code> <code class="type">text</code>
</p>
<p>
       I/O 操作的高階結果：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">UNKNOWN</code> 表示尚未得知操作的結果。
         </p></li><li class="listitem"><p>
<code class="literal">OK</code> 表示 I/O 已成功完成。
         </p></li><li class="listitem"><p>
<code class="literal">PARTIAL</code> 表示 I/O 已無錯誤地完成，但並未處理所有資料。呼叫端通常需要重試，並以另一個 I/O 執行剩餘的工作。
         </p></li><li class="listitem"><p>
<code class="literal">WARNING</code> 表示 I/O 已無錯誤地完成，但執行該 IO 時觸發了警告。例如在啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-developer.md#GUC-ZERO-DAMAGED-PAGES">zero_damaged_pages</a> 的情況下遇到損毀的緩衝區時。
         </p></li><li class="listitem"><p>
<code class="literal">ERROR</code> 表示 I/O 因錯誤而失敗。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">target_desc</code> <code class="type">text</code>
</p>
<p>
       此 I/O 操作所針對對象的描述。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">f_sync</code> <code class="type">bool</code>
</p>
<p>
       表示此 I/O 是否以同步方式執行的旗標。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">f_localmem</code> <code class="type">bool</code>
</p>
<p>
       表示此 I/O 是否參照程序本地記憶體的旗標。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">f_buffered</code> <code class="type">bool</code>
</p>
<p>
       表示此 I/O 是否為經過緩衝的 I/O 的旗標。
      </p></td></tr></tbody></table>

<br>

`pg_aios` 檢視表是唯讀的。

預設情況下，只有超級使用者或具有 `pg_read_all_stats` 角色權限的角色可以讀取 `pg_aios` 檢視表。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-aios.html)（原文版本：18.6；核對日期：2026-10-12）
