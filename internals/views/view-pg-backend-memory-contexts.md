<a id="VIEW-PG-BACKEND-MEMORY-CONTEXTS"></a>

## 53.5. `pg_backend_memory_contexts` [#](#VIEW-PG-BACKEND-MEMORY-CONTEXTS)

<a id="id-1.10.5.9.2"></a>

檢視表 `pg_backend_memory_contexts` 顯示目前工作階段所連接之伺服器程序的所有記憶體上下文。

`pg_backend_memory_contexts` 中，每個記憶體上下文各占一筆資料列。

<a id="id-1.10.5.9.5"></a>

**表 53.5. `pg_backend_memory_contexts` 欄位**

<table border="1" class="table" summary="表 53.5. pg_backend_memory_contexts 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       記憶體上下文的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ident</code> <code class="type">text</code>
</p>
<p>
       記憶體上下文的識別資訊。此欄位會截斷在 1024 位元組
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       記憶體上下文的類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">level</code> <code class="type">int4</code>
</p>
<p>
       此上下文在記憶體上下文階層中的層級（從 1 起算）。上下文的層級也代表該上下文在
       <code class="structfield">path</code> 欄位中的位置。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">path</code> <code class="type">int4[]</code>
</p>
<p>
       由暫時性數字識別碼組成的陣列，用以描述記憶體上下文階層。第一個元素對應
       <code class="literal">TopMemoryContext</code>，後續元素包含中間層的父上下文，最後一個元素則包含目前上下文的識別碼。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_bytes</code> <code class="type">int8</code>
</p>
<p>
       為此記憶體上下文配置的總位元組數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_nblocks</code> <code class="type">int8</code>
</p>
<p>
       為此記憶體上下文配置的區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">free_bytes</code> <code class="type">int8</code>
</p>
<p>
       可用空間（位元組）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">free_chunks</code> <code class="type">int8</code>
</p>
<p>
       可用區塊片段（chunk）的總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">used_bytes</code> <code class="type">int8</code>
</p>
<p>
       已使用空間（位元組）
      </p></td></tr></tbody></table>

<br>

預設情況下，只有超級使用者或具有 `pg_read_all_stats` 角色權限的角色可以讀取 `pg_backend_memory_contexts` 檢視表。

由於記憶體上下文會在查詢執行期間建立與銷毀，因此在同一個查詢中多次叫用此檢視表時，`path` 欄位中儲存的識別碼可能不一致。下面的範例示範如何有效使用此欄位，計算 `CacheMemoryContext` 及其所有子上下文所使用的總位元組數：

```

WITH memory_contexts AS (
    SELECT * FROM pg_backend_memory_contexts
)
SELECT sum(c1.total_bytes)
FROM memory_contexts c1, memory_contexts c2
WHERE c2.name = 'CacheMemoryContext'
AND c1.path[c2.level] = c2.path[c2.level];
```

此處使用[通用資料表運算式](../../the-sql-language/queries/queries-with.md)，以確保 `path` 欄位中的上下文 ID 在兩次評估此檢視表時一致。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-backend-memory-contexts.html)（原文版本：18.6；核對日期：2026-10-12）
