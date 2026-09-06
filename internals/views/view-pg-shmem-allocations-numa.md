## 53.28. `pg_shmem_allocations_numa` [#](#VIEW-PG-SHMEM-ALLOCATIONS-NUMA)

<a id="id-1.10.5.32.2"></a>

The `pg_shmem_allocations_numa` shows how shared
memory allocations in the server's main shared memory segment are distributed
across NUMA nodes. This includes both memory allocated by
PostgreSQL itself and memory allocated
by extensions using the mechanisms detailed in
[Section 36.10.11](../../server-programming/extend/xfunc-c.md#XFUNC-SHARED-ADDIN). This view will output multiple rows
for each of the shared memory segments provided that they are spread across
multiple NUMA nodes. This view should not be queried by monitoring systems
as it is very slow and may end up allocating shared memory in case it was not
used earlier.
Current limitation for this view is that won't show anonymous shared memory
allocations.

Note that this view does not include memory allocated using the dynamic
shared memory infrastructure.

### Warning

When determining the NUMA node, the view touches
all memory pages for the shared memory segment. This will force
allocation of the shared memory, if it wasn't allocated already,
and the memory may get allocated in a single NUMA
node (depending on system configuration).

<a id="id-1.10.5.32.6"></a>

**Table 53.28. `pg_shmem_allocations_numa` Columns**

<table border="1" class="table" summary="pg_shmem_allocations_numa Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       The name of the shared memory allocation.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numa_node</code> <code class="type">int4</code>
</p>
<p>
      ID of <acronym class="acronym">NUMA</acronym> node
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">size</code> <code class="type">int8</code>
</p>
<p>
       Size of the allocation on this particular NUMA memory node in bytes
      </p></td></tr></tbody></table>

<br>

By default, the `pg_shmem_allocations_numa` view can be
read only by superusers or roles with privileges of the
`pg_read_all_stats` role.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shmem-allocations-numa.html)（英文原文，待翻譯）
