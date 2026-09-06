## F.33. pgstattuple — obtain tuple-level statistics [#](#PGSTATTUPLE)

[F.33.1. Functions](pgstattuple.md#PGSTATTUPLE-FUNCS)

[F.33.2. Authors](pgstattuple.md#PGSTATTUPLE-AUTHORS)

<a id="id-1.11.7.43.2"></a>

The `pgstattuple` module provides various functions to
obtain tuple-level statistics.

Because these functions return detailed page-level information, access is
restricted by default. By default, only the
role `pg_stat_scan_tables` has `EXECUTE`
privilege. Superusers of course bypass this restriction. After the
extension has been installed, users may issue `GRANT`
commands to change the privileges on the functions to allow others to
execute them. However, it might be preferable to add those users to
the `pg_stat_scan_tables` role instead.

<a id="PGSTATTUPLE-FUNCS"></a>

### F.33.1. Functions [#](#PGSTATTUPLE-FUNCS)

<a id="id-1.11.7.43.5.2.1.1.1"></a> `pgstattuple(regclass) returns record`
:   `pgstattuple` returns a relation's physical length,
    percentage of “dead” tuples, and other info. This may help users
    to determine whether vacuum is necessary or not. The argument is the
    target relation's name (optionally schema-qualified) or OID.
    For example:

    ```

    test=> SELECT * FROM pgstattuple('pg_catalog.pg_proc');
    -[ RECORD 1 ]------+-------
    table_len          | 458752
    tuple_count        | 1470
    tuple_len          | 438896
    tuple_percent      | 95.67
    dead_tuple_count   | 11
    dead_tuple_len     | 3157
    dead_tuple_percent | 0.69
    free_space         | 8932
    free_percent       | 1.95
    ```

    The output columns are described in [Table F.24](pgstattuple.md#PGSTATTUPLE-COLUMNS).

    <a id="PGSTATTUPLE-COLUMNS"></a>

    **Table F.24. `pgstattuple` Output Columns**

    <table border="1" class="table" summary="pgstattuple Output Columns"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">table_len</code></td><td><code class="type">bigint</code></td><td>Physical relation length in bytes</td></tr><tr><td><code class="structfield">tuple_count</code></td><td><code class="type">bigint</code></td><td>Number of live tuples</td></tr><tr><td><code class="structfield">tuple_len</code></td><td><code class="type">bigint</code></td><td>Total length of live tuples in bytes</td></tr><tr><td><code class="structfield">tuple_percent</code></td><td><code class="type">float8</code></td><td>Percentage of live tuples</td></tr><tr><td><code class="structfield">dead_tuple_count</code></td><td><code class="type">bigint</code></td><td>Number of dead tuples</td></tr><tr><td><code class="structfield">dead_tuple_len</code></td><td><code class="type">bigint</code></td><td>Total length of dead tuples in bytes</td></tr><tr><td><code class="structfield">dead_tuple_percent</code></td><td><code class="type">float8</code></td><td>Percentage of dead tuples</td></tr><tr><td><code class="structfield">free_space</code></td><td><code class="type">bigint</code></td><td>Total free space in bytes</td></tr><tr><td><code class="structfield">free_percent</code></td><td><code class="type">float8</code></td><td>Percentage of free space</td></tr></tbody></table>

    <br>

    ### Note

    The `table_len` will always be greater than the sum
    of the `tuple_len`, `dead_tuple_len`
    and `free_space`. The difference is accounted for by
    fixed page overhead, the per-page table of pointers to tuples, and
    padding to ensure that tuples are correctly aligned.

    `pgstattuple` acquires only a read lock on the
    relation. So the results do not reflect an instantaneous snapshot;
    concurrent updates will affect them.

    `pgstattuple` judges a tuple is “dead” if
    `HeapTupleSatisfiesDirty` returns false.

`pgstattuple(text) returns record`
:   This is the same as `pgstattuple(regclass)`, except
    that the target relation is specified as TEXT. This function is kept
    because of backward-compatibility so far, and will be deprecated in
    some future release.

<a id="id-1.11.7.43.5.2.3.1.1"></a> `pgstatindex(regclass) returns record`
:   `pgstatindex` returns a record showing information
    about a B-tree index. For example:

    ```

    test=> SELECT * FROM pgstatindex('pg_cast_oid_index');
    -[ RECORD 1 ]------+------
    version            | 2
    tree_level         | 0
    index_size         | 16384
    root_block_no      | 1
    internal_pages     | 0
    leaf_pages         | 1
    empty_pages        | 0
    deleted_pages      | 0
    avg_leaf_density   | 54.27
    leaf_fragmentation | 0
    ```

    The output columns are:

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>B-tree version number</td></tr><tr><td><code class="structfield">tree_level</code></td><td><code class="type">integer</code></td><td>Tree level of the root page</td></tr><tr><td><code class="structfield">index_size</code></td><td><code class="type">bigint</code></td><td>Total index size in bytes</td></tr><tr><td><code class="structfield">root_block_no</code></td><td><code class="type">bigint</code></td><td>Location of root page (zero if none)</td></tr><tr><td><code class="structfield">internal_pages</code></td><td><code class="type">bigint</code></td><td>Number of <span class="quote">“<span class="quote">internal</span>”</span> (upper-level) pages</td></tr><tr><td><code class="structfield">leaf_pages</code></td><td><code class="type">bigint</code></td><td>Number of leaf pages</td></tr><tr><td><code class="structfield">empty_pages</code></td><td><code class="type">bigint</code></td><td>Number of empty pages</td></tr><tr><td><code class="structfield">deleted_pages</code></td><td><code class="type">bigint</code></td><td>Number of deleted pages</td></tr><tr><td><code class="structfield">avg_leaf_density</code></td><td><code class="type">float8</code></td><td>Average density of leaf pages</td></tr><tr><td><code class="structfield">leaf_fragmentation</code></td><td><code class="type">float8</code></td><td>Leaf page fragmentation</td></tr></tbody></table>

    The reported `index_size` will normally correspond to one more
    page than is accounted for by `internal_pages + leaf_pages +
    empty_pages + deleted_pages`, because it also includes the
    index's metapage.

    As with `pgstattuple`, the results are accumulated
    page-by-page, and should not be expected to represent an
    instantaneous snapshot of the whole index.

`pgstatindex(text) returns record`
:   This is the same as `pgstatindex(regclass)`, except
    that the target index is specified as TEXT. This function is kept
    because of backward-compatibility so far, and will be deprecated in
    some future release.

<a id="id-1.11.7.43.5.2.5.1.1"></a> `pgstatginindex(regclass) returns record`
:   `pgstatginindex` returns a record showing information
    about a GIN index. For example:

    ```

    test=> SELECT * FROM pgstatginindex('test_gin_index');
    -[ RECORD 1 ]--+--
    version        | 1
    pending_pages  | 0
    pending_tuples | 0
    ```

    The output columns are:

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>GIN version number</td></tr><tr><td><code class="structfield">pending_pages</code></td><td><code class="type">integer</code></td><td>Number of pages in the pending list</td></tr><tr><td><code class="structfield">pending_tuples</code></td><td><code class="type">bigint</code></td><td>Number of tuples in the pending list</td></tr></tbody></table>

<a id="id-1.11.7.43.5.2.6.1.1"></a> `pgstathashindex(regclass) returns record`
:   `pgstathashindex` returns a record showing information
    about a HASH index. For example:

    ```

    test=> select * from pgstathashindex('con_hash_index');
    -[ RECORD 1 ]--+-----------------
    version        | 4
    bucket_pages   | 33081
    overflow_pages | 0
    bitmap_pages   | 1
    unused_pages   | 32455
    live_items     | 10204006
    dead_items     | 0
    free_percent   | 61.8005949100872
    ```

    The output columns are:

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>HASH version number</td></tr><tr><td><code class="structfield">bucket_pages</code></td><td><code class="type">bigint</code></td><td>Number of bucket pages</td></tr><tr><td><code class="structfield">overflow_pages</code></td><td><code class="type">bigint</code></td><td>Number of overflow pages</td></tr><tr><td><code class="structfield">bitmap_pages</code></td><td><code class="type">bigint</code></td><td>Number of bitmap pages</td></tr><tr><td><code class="structfield">unused_pages</code></td><td><code class="type">bigint</code></td><td>Number of unused pages</td></tr><tr><td><code class="structfield">live_items</code></td><td><code class="type">bigint</code></td><td>Number of live tuples</td></tr><tr><td><code class="structfield">dead_tuples</code></td><td><code class="type">bigint</code></td><td>Number of dead tuples</td></tr><tr><td><code class="structfield">free_percent</code></td><td><code class="type">float</code></td><td>Percentage of free space</td></tr></tbody></table>

<a id="id-1.11.7.43.5.2.7.1.1"></a> `pg_relpages(regclass) returns bigint`
:   `pg_relpages` returns the number of pages in the
    relation.

`pg_relpages(text) returns bigint`
:   This is the same as `pg_relpages(regclass)`, except
    that the target relation is specified as TEXT. This function is kept
    because of backward-compatibility so far, and will be deprecated in
    some future release.

<a id="id-1.11.7.43.5.2.9.1.1"></a> `pgstattuple_approx(regclass) returns record`
:   `pgstattuple_approx` is a faster alternative to
    `pgstattuple` that returns approximate results.
    The argument is the target relation's name or OID.
    For example:

    ```

    test=> SELECT * FROM pgstattuple_approx('pg_catalog.pg_proc'::regclass);
    -[ RECORD 1 ]--------+-------
    table_len            | 573440
    scanned_percent      | 2
    approx_tuple_count   | 2740
    approx_tuple_len     | 561210
    approx_tuple_percent | 97.87
    dead_tuple_count     | 0
    dead_tuple_len       | 0
    dead_tuple_percent   | 0
    approx_free_space    | 11996
    approx_free_percent  | 2.09
    ```

    The output columns are described in [Table F.25](pgstattuple.md#PGSTATAPPROX-COLUMNS).

    Whereas `pgstattuple` always performs a
    full-table scan and returns an exact count of live and dead tuples
    (and their sizes) and free space, `pgstattuple_approx`
    tries to avoid the full-table scan and returns exact dead tuple
    statistics along with an approximation of the number and
    size of live tuples and free space.

    It does this by skipping pages that have only visible tuples
    according to the visibility map (if a page has the corresponding VM
    bit set, then it is assumed to contain no dead tuples). For such
    pages, it derives the free space value from the free space map, and
    assumes that the rest of the space on the page is taken up by live
    tuples.

    For pages that cannot be skipped, it scans each tuple, recording its
    presence and size in the appropriate counters, and adding up the
    free space on the page. At the end, it estimates the total number of
    live tuples based on the number of pages and tuples scanned (in the
    same way that VACUUM estimates pg_class.reltuples).

    <a id="PGSTATAPPROX-COLUMNS"></a>

    **Table F.25. `pgstattuple_approx` Output Columns**

    <table border="1" class="table" summary="pgstattuple_approx Output Columns"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">table_len</code></td><td><code class="type">bigint</code></td><td>Physical relation length in bytes (exact)</td></tr><tr><td><code class="structfield">scanned_percent</code></td><td><code class="type">float8</code></td><td>Percentage of table scanned</td></tr><tr><td><code class="structfield">approx_tuple_count</code></td><td><code class="type">bigint</code></td><td>Number of live tuples (estimated)</td></tr><tr><td><code class="structfield">approx_tuple_len</code></td><td><code class="type">bigint</code></td><td>Total length of live tuples in bytes (estimated)</td></tr><tr><td><code class="structfield">approx_tuple_percent</code></td><td><code class="type">float8</code></td><td>Percentage of live tuples</td></tr><tr><td><code class="structfield">dead_tuple_count</code></td><td><code class="type">bigint</code></td><td>Number of dead tuples (exact)</td></tr><tr><td><code class="structfield">dead_tuple_len</code></td><td><code class="type">bigint</code></td><td>Total length of dead tuples in bytes (exact)</td></tr><tr><td><code class="structfield">dead_tuple_percent</code></td><td><code class="type">float8</code></td><td>Percentage of dead tuples</td></tr><tr><td><code class="structfield">approx_free_space</code></td><td><code class="type">bigint</code></td><td>Total free space in bytes (estimated)</td></tr><tr><td><code class="structfield">approx_free_percent</code></td><td><code class="type">float8</code></td><td>Percentage of free space</td></tr></tbody></table>

    <br>

    In the above output, the free space figures may not match the
    `pgstattuple` output exactly, because the free
    space map gives us an exact figure, but is not guaranteed to be
    accurate to the byte.

<a id="PGSTATTUPLE-AUTHORS"></a>

### F.33.2. Authors [#](#PGSTATTUPLE-AUTHORS)

Tatsuo Ishii, Satoshi Nagayasu and Abhijit Menon-Sen

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstattuple.html)（英文原文，待翻譯）
