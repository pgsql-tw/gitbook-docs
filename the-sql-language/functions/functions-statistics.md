## 9.31. Statistics Information Functions [#](#FUNCTIONS-STATISTICS)

[9.31.1. Inspecting MCV Lists](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

<a id="id-1.5.8.37.2"></a>

PostgreSQL provides a function to inspect complex
statistics defined using the `CREATE STATISTICS` command.

<a id="FUNCTIONS-STATISTICS-MCV"></a>

### 9.31.1. Inspecting MCV Lists [#](#FUNCTIONS-STATISTICS-MCV)

<a id="id-1.5.8.37.4.2"></a>

```

pg_mcv_list_items ( pg_mcv_list ) → setof record
```

`pg_mcv_list_items` returns a set of records describing
all items stored in a multi-column MCV list. It
returns the following columns:

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">index</code></td><td><code class="type">integer</code></td><td>index of the item in the <acronym class="acronym">MCV</acronym> list</td></tr><tr><td><code class="literal">values</code></td><td><code class="type">text[]</code></td><td>values stored in the MCV item</td></tr><tr><td><code class="literal">nulls</code></td><td><code class="type">boolean[]</code></td><td>flags identifying <code class="literal">NULL</code> values</td></tr><tr><td><code class="literal">frequency</code></td><td><code class="type">double precision</code></td><td>frequency of this <acronym class="acronym">MCV</acronym> item</td></tr><tr><td><code class="literal">base_frequency</code></td><td><code class="type">double precision</code></td><td>base frequency of this <acronym class="acronym">MCV</acronym> item</td></tr></tbody></table>

The `pg_mcv_list_items` function can be used like this:

```

SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';
```

Values of the `pg_mcv_list` type can be obtained only from the
`pg_statistic_ext_data`.`stxdmcv`
column.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-statistics.html)（英文原文，待翻譯）
