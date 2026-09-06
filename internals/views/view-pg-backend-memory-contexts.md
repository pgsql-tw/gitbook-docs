## 53.5. `pg_backend_memory_contexts` [#](#VIEW-PG-BACKEND-MEMORY-CONTEXTS)

<a id="id-1.10.5.9.2"></a>

The view `pg_backend_memory_contexts` displays all
the memory contexts of the server process attached to the current session.

`pg_backend_memory_contexts` contains one row
for each memory context.

<a id="id-1.10.5.9.5"></a>

**Table 53.5. `pg_backend_memory_contexts` Columns**

<table border="1" class="table" summary="pg_backend_memory_contexts Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       Name of the memory context
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ident</code> <code class="type">text</code>
</p>
<p>
       Identification information of the memory context. This field is truncated at 1024 bytes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       Type of the memory context
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">level</code> <code class="type">int4</code>
</p>
<p>
       The 1-based level of the context in the memory context hierarchy. The
       level of a context also shows the position of that context in the
       <code class="structfield">path</code> column.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">path</code> <code class="type">int4[]</code>
</p>
<p>
       Array of transient numerical identifiers to describe the memory
       context hierarchy. The first element is for
       <code class="literal">TopMemoryContext</code>, subsequent elements contain
       intermediate parents and the final element contains the identifier for
       the current context.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_bytes</code> <code class="type">int8</code>
</p>
<p>
       Total bytes allocated for this memory context
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_nblocks</code> <code class="type">int8</code>
</p>
<p>
       Total number of blocks allocated for this memory context
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">free_bytes</code> <code class="type">int8</code>
</p>
<p>
       Free space in bytes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">free_chunks</code> <code class="type">int8</code>
</p>
<p>
       Total number of free chunks
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">used_bytes</code> <code class="type">int8</code>
</p>
<p>
       Used space in bytes
      </p></td></tr></tbody></table>

<br>

By default, the `pg_backend_memory_contexts` view can be
read only by superusers or roles with the privileges of the
`pg_read_all_stats` role.

Since memory contexts are created and destroyed during the running of a
query, the identifiers stored in the `path` column
can be unstable between multiple invocations of the view in the same query.
The example below demonstrates an effective usage of this column and
calculates the total number of bytes used by
`CacheMemoryContext` and all of its children:

```

WITH memory_contexts AS (
    SELECT * FROM pg_backend_memory_contexts
)
SELECT sum(c1.total_bytes)
FROM memory_contexts c1, memory_contexts c2
WHERE c2.name = 'CacheMemoryContext'
AND c1.path[c2.level] = c2.path[c2.level];
```

The [Common Table Expression](../../the-sql-language/queries/queries-with.md) is used
to ensure the context IDs in the `path` column
match between both evaluations of the view.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-backend-memory-contexts.html)（英文原文，待翻譯）
