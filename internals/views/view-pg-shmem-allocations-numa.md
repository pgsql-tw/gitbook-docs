<a id="VIEW-PG-SHMEM-ALLOCATIONS-NUMA"></a>

## 53.28. `pg_shmem_allocations_numa` [#](#view-pg-shmem-allocations-numa) <a href="#view-pg-shmem-allocations-numa" id="view-pg-shmem-allocations-numa"></a>

<a id="id-1.10.5.32.2"></a>

`pg_shmem_allocations_numa` 顯示伺服器主要共享記憶體區段中的共享記憶體配置如何分布於各 NUMA 節點。這同時包含 PostgreSQL 本身配置的記憶體，以及擴充功能透過[第 36.10.11 節](../../server-programming/extend/xfunc-c.md#XFUNC-SHARED-ADDIN)所述機制配置的記憶體。只要共享記憶體區段分布於多個 NUMA 節點，此檢視表就會為每個這樣的區段輸出多個資料列。監控系統不應查詢此檢視表，因為它非常緩慢，而且若共享記憶體先前未被使用，查詢最後可能會配置這些共享記憶體。此檢視表目前的限制是不會顯示匿名共享記憶體配置。

請注意，此檢視表不包含使用動態共享記憶體基礎設施所配置的記憶體。

<a id="id-1.10.5.32.5"></a>

### 警告

在判定 NUMA 節點時，此檢視表會存取（touch）共享記憶體區段的所有記憶體分頁。若共享記憶體尚未配置，這會強制配置它，而且這些記憶體可能會被配置在單一 NUMA 節點上（取決於系統設定）。

<a id="id-1.10.5.32.6"></a>

**表 53.28. `pg_shmem_allocations_numa` 欄位**

<table border="1" class="table" summary="表 53.28. pg_shmem_allocations_numa 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       共享記憶體配置的名稱。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numa_node</code> <code class="type">int4</code>
</p>
<p>
      <acronym class="acronym">NUMA</acronym> 節點的 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">size</code> <code class="type">int8</code>
</p>
<p>
       此配置在這個特定 NUMA 記憶體節點上的大小，以位元組為單位
      </p></td></tr></tbody></table>

<br>

預設情況下，只有超級使用者或具有 `pg_read_all_stats` 角色權限的角色可以讀取 `pg_shmem_allocations_numa` 檢視表。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shmem-allocations-numa.html)（原文版本：18.6；核對日期：2026-10-09）
