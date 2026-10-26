<a id="VIEW-PG-SHMEM-ALLOCATIONS"></a>

## 53.27. `pg_shmem_allocations` [#](#view-pg-shmem-allocations) <a href="#view-pg-shmem-allocations" id="view-pg-shmem-allocations"></a>

<a id="id-1.10.5.31.2"></a>

檢視表 `pg_shmem_allocations` 顯示從伺服器主要共享記憶體區段所進行的配置。這包含 PostgreSQL 本身所配置的記憶體，以及擴充功能使用[第 36.10.11 節](../../server-programming/extend/xfunc-c.md#xfunc-shared-addin)所詳述之機制配置的記憶體。

請注意，此檢視表不包含使用動態共享記憶體基礎架構所配置的記憶體。

<a id="id-1.10.5.31.5"></a>

**表 53.27. `pg_shmem_allocations` 欄位**

<table border="1" class="table" summary="表 53.27. pg_shmem_allocations 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       共享記憶體配置的名稱。未使用的記憶體為 NULL，匿名配置則為 <code class="literal">&lt;anonymous&gt;</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">off</code> <code class="type">int8</code>
</p>
<p>
       配置起始處的位移量。匿名配置則為 NULL，因為與其相關的細節是未知的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">size</code> <code class="type">int8</code>
</p>
<p>
       配置的大小（以位元組為單位）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">allocated_size</code> <code class="type">int8</code>
</p>
<p>
       配置的大小（以位元組為單位，含填補）。對於匿名配置，沒有關於填補的資訊可用，因此 <code class="literal">size</code> 與 <code class="literal">allocated_size</code> 欄位一律相等。填補對閒置記憶體沒有意義，因此在該情況下這兩個欄位也會相等。
      </p></td></tr></tbody></table>

<br>

匿名配置是指直接以 `ShmemAlloc()` 進行的配置，而不是透過 `ShmemInitStruct()` 或 `ShmemInitHash()` 進行的配置。

預設情況下，只有超級使用者或具有 `pg_read_all_stats` 角色權限的角色可讀取 `pg_shmem_allocations` 檢視表。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shmem-allocations.html)（原文版本：18.6；核對日期：2026-10-09）
