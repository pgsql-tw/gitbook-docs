## 53.27. `pg_shmem_allocations` [#](#VIEW-PG-SHMEM-ALLOCATIONS)

<a id="id-1.10.5.31.2"></a>

The `pg_shmem_allocations` view shows allocations
made from the server's main shared memory segment. This includes both
memory allocated by PostgreSQL itself and memory
allocated by extensions using the mechanisms detailed in
[Section 36.10.11](../../server-programming/extend/xfunc-c.md#XFUNC-SHARED-ADDIN).

Note that this view does not include memory allocated using the dynamic
shared memory infrastructure.

<a id="id-1.10.5.31.5"></a>

**Table 53.27. `pg_shmem_allocations` Columns**

<table border="1" class="table" summary="pg_shmem_allocations Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       The name of the shared memory allocation. NULL for unused memory
       and <code class="literal">&lt;anonymous&gt;</code> for anonymous
       allocations.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">off</code> <code class="type">int8</code>
</p>
<p>
       The offset at which the allocation starts. NULL for anonymous
       allocations, since details related to them are not known.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">size</code> <code class="type">int8</code>
</p>
<p>
       Size of the allocation in bytes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">allocated_size</code> <code class="type">int8</code>
</p>
<p>
       Size of the allocation in bytes including padding. For anonymous
       allocations, no information about padding is available, so the
       <code class="literal">size</code> and <code class="literal">allocated_size</code> columns
       will always be equal. Padding is not meaningful for free memory, so
       the columns will be equal in that case also.
      </p></td></tr></tbody></table>

<br>

Anonymous allocations are allocations that have been made
with `ShmemAlloc()` directly, rather than via
`ShmemInitStruct()` or
`ShmemInitHash()`.

By default, the `pg_shmem_allocations` view can be
read only by superusers or roles with privileges of the
`pg_read_all_stats` role.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shmem-allocations.html)（英文原文，待翻譯）
