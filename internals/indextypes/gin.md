## 65.4. GIN Indexes [#](#GIN)

[65.4.1. Introduction](gin.md#GIN-INTRO)

[65.4.2. Built-in Operator Classes](gin.md#GIN-BUILTIN-OPCLASSES)

[65.4.3. Extensibility](gin.md#GIN-EXTENSIBILITY)

[65.4.4. Implementation](gin.md#GIN-IMPLEMENTATION)

[65.4.5. GIN Tips and Tricks](gin.md#GIN-TIPS)

[65.4.6. Limitations](gin.md#GIN-LIMIT)

[65.4.7. Examples](gin.md#GIN-EXAMPLES)

<a id="id-1.10.17.5.2"></a><a id="GIN-INTRO"></a>

### 65.4.1. Introduction [#](#GIN-INTRO)

GIN stands for Generalized Inverted Index.
GIN is designed for handling cases where the items
to be indexed are composite values, and the queries to be handled by
the index need to search for element values that appear within
the composite items. For example, the items could be documents,
and the queries could be searches for documents containing specific words.

We use the word *item* to refer to a composite value that
is to be indexed, and the word *key* to refer to an element
value. GIN always stores and searches for keys,
not item values per se.

A GIN index stores a set of (key, posting list) pairs,
where a *posting list* is a set of row IDs in which the key
occurs. The same row ID can appear in multiple posting lists, since
an item can contain more than one key. Each key value is stored only
once, so a GIN index is very compact for cases
where the same key appears many times.

GIN is generalized in the sense that the
GIN access method code does not need to know the
specific operations that it accelerates.
Instead, it uses custom strategies defined for particular data types.
The strategy defines how keys are extracted from indexed items and
query conditions, and how to determine whether a row that contains
some of the key values in a query actually satisfies the query.

One advantage of GIN is that it allows the development
of custom data types with the appropriate access methods, by
an expert in the domain of the data type, rather than a database expert.
This is much the same advantage as using GiST.

The GIN
implementation in PostgreSQL is primarily
maintained by Teodor Sigaev and Oleg Bartunov. There is more
information about GIN on their
[website](http://www.sai.msu.su/~megera/wiki/Gin).

<a id="GIN-BUILTIN-OPCLASSES"></a>

### 65.4.2. Built-in Operator Classes [#](#GIN-BUILTIN-OPCLASSES)

The core PostgreSQL distribution
includes the GIN operator classes shown in
[Table 65.3](gin.md#GIN-BUILTIN-OPCLASSES-TABLE).
(Some of the optional modules described in [Appendix F](../../appendixes/contrib/README.md)
provide additional GIN operator classes.)

<a id="GIN-BUILTIN-OPCLASSES-TABLE"></a>

**Table 65.3. Built-in GIN Operator Classes**

<table border="1" class="table" summary="Built-in GIN Operator Classes"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Indexable Operators</th></tr></thead><tbody><tr><td rowspan="4" valign="middle"><code class="literal">array_ops</code></td><td><code class="literal">&amp;&amp; (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">@&gt; (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">&lt;@ (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">= (anyarray,anyarray)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">jsonb_ops</code></td><td><code class="literal">@&gt; (jsonb,jsonb)</code></td></tr><tr><td><code class="literal">@? (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">@@ (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">? (jsonb,text)</code></td></tr><tr><td><code class="literal">?| (jsonb,text[])</code></td></tr><tr><td><code class="literal">?&amp; (jsonb,text[])</code></td></tr><tr><td rowspan="3" valign="middle"><code class="literal">jsonb_path_ops</code></td><td><code class="literal">@&gt; (jsonb,jsonb)</code></td></tr><tr><td><code class="literal">@? (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">@@ (jsonb,jsonpath)</code></td></tr><tr><td valign="middle"><code class="literal">tsvector_ops</code></td><td><code class="literal">@@ (tsvector,tsquery)</code></td></tr></tbody></table>

<br>

Of the two operator classes for type `jsonb`, `jsonb_ops`
is the default. `jsonb_path_ops` supports fewer operators but
offers better performance for those operators.
See [Section 8.14.4](../../the-sql-language/datatype/datatype-json.md#JSON-INDEXING) for details.

<a id="GIN-EXTENSIBILITY"></a>

### 65.4.3. Extensibility [#](#GIN-EXTENSIBILITY)

The GIN interface has a high level of abstraction,
requiring the access method implementer only to implement the semantics of
the data type being accessed. The GIN layer itself
takes care of concurrency, logging and searching the tree structure.

All it takes to get a GIN access method working is to
implement a few user-defined methods, which define the behavior of
keys in the tree and the relationships between keys, indexed items,
and indexable queries. In short, GIN combines
extensibility with generality, code reuse, and a clean interface.

There are two methods that an operator class for
GIN must provide:

`Datum *extractValue(Datum itemValue, int32 *nkeys, bool **nullFlags)`
:   Returns a palloc'd array of keys given an item to be indexed. The
    number of returned keys must be stored into `*nkeys`.
    If any of the keys can be null, also palloc an array of
    `*nkeys` `bool` fields, store its address at
    `*nullFlags`, and set these null flags as needed.
    `*nullFlags` can be left `NULL` (its initial value)
    if all keys are non-null.
    The return value can be `NULL` if the item contains no keys.

`Datum *extractQuery(Datum query, int32 *nkeys, StrategyNumber n, bool **pmatch, Pointer **extra_data, bool **nullFlags, int32 *searchMode)`
:   Returns a palloc'd array of keys given a value to be queried; that is,
    `query` is the value on the right-hand side of an
    indexable operator whose left-hand side is the indexed column.
    `n` is the strategy number of the operator within the
    operator class (see [Section 36.16.2](../../server-programming/extend/xindex.md#XINDEX-STRATEGIES)).
    Often, `extractQuery` will need
    to consult `n` to determine the data type of
    `query` and the method it should use to extract key values.
    The number of returned keys must be stored into `*nkeys`.
    If any of the keys can be null, also palloc an array of
    `*nkeys` `bool` fields, store its address at
    `*nullFlags`, and set these null flags as needed.
    `*nullFlags` can be left `NULL` (its initial value)
    if all keys are non-null.
    The return value can be `NULL` if the `query` contains no keys.

    `searchMode` is an output argument that allows
    `extractQuery` to specify details about how the search
    will be done.
    If `*searchMode` is set to
    `GIN_SEARCH_MODE_DEFAULT` (which is the value it is
    initialized to before call), only items that match at least one of
    the returned keys are considered candidate matches.
    If `*searchMode` is set to
    `GIN_SEARCH_MODE_INCLUDE_EMPTY`, then in addition to items
    containing at least one matching key, items that contain no keys at
    all are considered candidate matches. (This mode is useful for
    implementing is-subset-of operators, for example.)
    If `*searchMode` is set to `GIN_SEARCH_MODE_ALL`,
    then all non-null items in the index are considered candidate
    matches, whether they match any of the returned keys or not. (This
    mode is much slower than the other two choices, since it requires
    scanning essentially the entire index, but it may be necessary to
    implement corner cases correctly. An operator that needs this mode
    in most cases is probably not a good candidate for a GIN operator
    class.)
    The symbols to use for setting this mode are defined in
    `access/gin.h`.

    `pmatch` is an output argument for use when partial match
    is supported. To use it, `extractQuery` must allocate
    an array of `*nkeys` `bool`s and store its address at
    `*pmatch`. Each element of the array should be set to true
    if the corresponding key requires partial match, false if not.
    If `*pmatch` is set to `NULL` then GIN assumes partial match
    is not required. The variable is initialized to `NULL` before call,
    so this argument can simply be ignored by operator classes that do
    not support partial match.

    `extra_data` is an output argument that allows
    `extractQuery` to pass additional data to the
    `consistent` and `comparePartial` methods.
    To use it, `extractQuery` must allocate
    an array of `*nkeys` pointers and store its address at
    `*extra_data`, then store whatever it wants to into the
    individual pointers. The variable is initialized to `NULL` before
    call, so this argument can simply be ignored by operator classes that
    do not require extra data. If `*extra_data` is set, the
    whole array is passed to the `consistent` method, and
    the appropriate element to the `comparePartial` method.

An operator class must also provide a function to check if an indexed item
matches the query. It comes in two flavors, a Boolean `consistent`
function, and a ternary `triConsistent` function.
`triConsistent` covers the functionality of both, so providing
`triConsistent` alone is sufficient. However, if the Boolean
variant is significantly cheaper to calculate, it can be advantageous to
provide both. If only the Boolean variant is provided, some optimizations
that depend on refuting index items before fetching all the keys are
disabled.

`bool consistent(bool check[], StrategyNumber n, Datum query, int32 nkeys, Pointer extra_data[], bool *recheck, Datum queryKeys[], bool nullFlags[])`
:   Returns true if an indexed item satisfies the query operator with
    strategy number `n` (or might satisfy it, if the recheck
    indication is returned). This function does not have direct access
    to the indexed item's value, since GIN does not
    store items explicitly. Rather, what is available is knowledge
    about which key values extracted from the query appear in a given
    indexed item. The `check` array has length
    `nkeys`, which is the same as the number of keys previously
    returned by `extractQuery` for this `query` datum.
    Each element of the
    `check` array is true if the indexed item contains the
    corresponding query key, i.e., if (check[i] == true) the i-th key of the
    `extractQuery` result array is present in the indexed item.
    The original `query` datum is
    passed in case the `consistent` method needs to consult it,
    and so are the `queryKeys[]` and `nullFlags[]`
    arrays previously returned by `extractQuery`.
    `extra_data` is the extra-data array returned by
    `extractQuery`, or `NULL` if none.

    When `extractQuery` returns a null key in
    `queryKeys[]`, the corresponding `check[]` element
    is true if the indexed item contains a null key; that is, the
    semantics of `check[]` are like `IS NOT DISTINCT
    FROM`. The `consistent` function can examine the
    corresponding `nullFlags[]` element if it needs to tell
    the difference between a regular value match and a null match.

    On success, `*recheck` should be set to true if the heap
    tuple needs to be rechecked against the query operator, or false if
    the index test is exact. That is, a false return value guarantees
    that the heap tuple does not match the query; a true return value with
    `*recheck` set to false guarantees that the heap tuple does
    match the query; and a true return value with
    `*recheck` set to true means that the heap tuple might match
    the query, so it needs to be fetched and rechecked by evaluating the
    query operator directly against the originally indexed item.

`GinTernaryValue triConsistent(GinTernaryValue check[], StrategyNumber n, Datum query, int32 nkeys, Pointer extra_data[], Datum queryKeys[], bool nullFlags[])`
:   `triConsistent` is similar to `consistent`,
    but instead of Booleans in the `check` vector, there are
    three possible values for each
    key: `GIN_TRUE`, `GIN_FALSE` and
    `GIN_MAYBE`. `GIN_FALSE` and `GIN_TRUE`
    have the same meaning as regular Boolean values, while
    `GIN_MAYBE` means that the presence of that key is not known.
    When `GIN_MAYBE` values are present, the function should only
    return `GIN_TRUE` if the item certainly matches whether or
    not the index item contains the corresponding query keys. Likewise, the
    function must return `GIN_FALSE` only if the item certainly
    does not match, whether or not it contains the `GIN_MAYBE`
    keys. If the result depends on the `GIN_MAYBE` entries, i.e.,
    the match cannot be confirmed or refuted based on the known query keys,
    the function must return `GIN_MAYBE`.

    When there are no `GIN_MAYBE` values in the `check`
    vector, a `GIN_MAYBE` return value is the equivalent of
    setting the `recheck` flag in the
    Boolean `consistent` function.

In addition, GIN must have a way to sort the key values stored in the index.
The operator class can define the sort ordering by specifying a comparison
method:

`int compare(Datum a, Datum b)`
:   Compares two keys (not indexed items!) and returns an integer less than
    zero, zero, or greater than zero, indicating whether the first key is
    less than, equal to, or greater than the second. Null keys are never
    passed to this function.

Alternatively, if the operator class does not provide a `compare`
method, GIN will look up the default btree operator class for the index
key data type, and use its comparison function. It is recommended to
specify the comparison function in a GIN operator class that is meant for
just one data type, as looking up the btree operator class costs a few
cycles. However, polymorphic GIN operator classes (such
as `array_ops`) typically cannot specify a single comparison
function.

An operator class for GIN can optionally supply the
following methods:

`int comparePartial(Datum partial_key, Datum key, StrategyNumber n, Pointer extra_data)`
:   Compare a partial-match query key to an index key. Returns an integer
    whose sign indicates the result: less than zero means the index key
    does not match the query, but the index scan should continue; zero
    means that the index key does match the query; greater than zero
    indicates that the index scan should stop because no more matches
    are possible. The strategy number `n` of the operator
    that generated the partial match query is provided, in case its
    semantics are needed to determine when to end the scan. Also,
    `extra_data` is the corresponding element of the extra-data
    array made by `extractQuery`, or `NULL` if none.
    Null keys are never passed to this function.

`void options(local_relopts *relopts)`
:   Defines a set of user-visible parameters that control operator class
    behavior.

    The `options` function is passed a pointer to a
    `local_relopts` struct, which needs to be
    filled with a set of operator class specific options. The options
    can be accessed from other support functions using the
    `PG_HAS_OPCLASS_OPTIONS()` and
    `PG_GET_OPCLASS_OPTIONS()` macros.

    Since both key extraction of indexed values and representation of the
    key in GIN are flexible, they may depend on
    user-specified parameters.

To support “partial match” queries, an operator class must
provide the `comparePartial` method, and its
`extractQuery` method must set the `pmatch`
parameter when a partial-match query is encountered. See
[Section 65.4.4.2](gin.md#GIN-PARTIAL-MATCH) for details.

The actual data types of the various `Datum` values mentioned
above vary depending on the operator class. The item values passed to
`extractValue` are always of the operator class's input type, and
all key values must be of the class's `STORAGE` type. The type of
the `query` argument passed to `extractQuery`,
`consistent` and `triConsistent` is whatever is the
right-hand input type of the class member operator identified by the
strategy number. This need not be the same as the indexed type, so long as
key values of the correct type can be extracted from it. However, it is
recommended that the SQL declarations of these three support functions use
the opclass's indexed data type for the `query` argument, even
though the actual type might be something else depending on the operator.

<a id="GIN-IMPLEMENTATION"></a>

### 65.4.4. Implementation [#](#GIN-IMPLEMENTATION)

Internally, a GIN index contains a B-tree index
constructed over keys, where each key is an element of one or more indexed
items (a member of an array, for example) and where each tuple in a leaf
page contains either a pointer to a B-tree of heap pointers (a
“posting tree”), or a simple list of heap pointers (a “posting
list”) when the list is small enough to fit into a single index tuple along
with the key value. [Figure 65.1](gin.md#GIN-INTERNALS-FIGURE) illustrates
these components of a GIN index.

As of PostgreSQL 9.1, null key values can be
included in the index. Also, placeholder nulls are included in the index
for indexed items that are null or contain no keys according to
`extractValue`. This allows searches that should find empty
items to do so.

Multicolumn GIN indexes are implemented by building
a single B-tree over composite values (column number, key value). The
key values for different columns can be of different types.

<a id="GIN-INTERNALS-FIGURE"></a>

**Figure 65.1. GIN Internals**

<br><a id="GIN-FAST-UPDATE"></a>

#### 65.4.4.1. GIN Fast Update Technique [#](#GIN-FAST-UPDATE)

Updating a GIN index tends to be slow because of the
intrinsic nature of inverted indexes: inserting or updating one heap row
can cause many inserts into the index (one for each key extracted
from the indexed item).
GIN is capable of postponing much of this work by inserting
new tuples into a temporary, unsorted list of pending entries.
When the table is vacuumed or autoanalyzed, or when
`gin_clean_pending_list` function is called, or if the
pending list becomes larger than
[gin_pending_list_limit](../../server-administration/runtime-config/runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT), the entries are moved to the
main GIN data structure using the same bulk insert
techniques used during initial index creation. This greatly improves
GIN index update speed, even counting the additional
vacuum overhead. Moreover the overhead work can be done by a background
process instead of in foreground query processing.

The main disadvantage of this approach is that searches must scan the list
of pending entries in addition to searching the regular index, and so
a large list of pending entries will slow searches significantly.
Another disadvantage is that, while most updates are fast, an update
that causes the pending list to become “too large” will incur an
immediate cleanup cycle and thus be much slower than other updates.
Proper use of autovacuum can minimize both of these problems.

If consistent response time is more important than update speed,
use of pending entries can be disabled by turning off the
`fastupdate` storage parameter for a
GIN index. See [CREATE INDEX](../../reference/sql-commands/sql-createindex.md)
for details.

<a id="GIN-PARTIAL-MATCH"></a>

#### 65.4.4.2. Partial Match Algorithm [#](#GIN-PARTIAL-MATCH)

GIN can support “partial match” queries, in which the query
does not determine an exact match for one or more keys, but the possible
matches fall within a reasonably narrow range of key values (within the
key sorting order determined by the `compare` support method).
The `extractQuery` method, instead of returning a key value
to be matched exactly, returns a key value that is the lower bound of
the range to be searched, and sets the `pmatch` flag true.
The key range is then scanned using the `comparePartial`
method. `comparePartial` must return zero for a matching
index key, less than zero for a non-match that is still within the range
to be searched, or greater than zero if the index key is past the range
that could match.

<a id="GIN-TIPS"></a>

### 65.4.5. GIN Tips and Tricks [#](#GIN-TIPS)

Create vs. insert
:   Insertion into a GIN index can be slow
    due to the likelihood of many keys being inserted for each item.
    So, for bulk insertions into a table it is advisable to drop the GIN
    index and recreate it after finishing bulk insertion.

    When `fastupdate` is enabled for GIN
    (see [Section 65.4.4.1](gin.md#GIN-FAST-UPDATE) for details), the penalty is
    less than when it is not. But for very large updates it may still be
    best to drop and recreate the index.

[maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM)
:   Build time for a GIN index is very sensitive to
    the `maintenance_work_mem` setting; it doesn't pay to
    skimp on work memory during index creation.

[gin_pending_list_limit](../../server-administration/runtime-config/runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT)
:   During a series of insertions into an existing GIN
    index that has `fastupdate` enabled, the system will clean up
    the pending-entry list whenever the list grows larger than
    `gin_pending_list_limit`. To avoid fluctuations in observed
    response time, it's desirable to have pending-list cleanup occur in the
    background (i.e., via autovacuum). Foreground cleanup operations
    can be avoided by increasing `gin_pending_list_limit`
    or making autovacuum more aggressive.
    However, enlarging the threshold of the cleanup operation means that
    if a foreground cleanup does occur, it will take even longer.

    `gin_pending_list_limit` can be overridden for individual
    GIN indexes by changing storage parameters, which allows each
    GIN index to have its own cleanup threshold.
    For example, it's possible to increase the threshold only for the GIN
    index which can be updated heavily, and decrease it otherwise.

[gin_fuzzy_search_limit](../../server-administration/runtime-config/runtime-config-client.md#GUC-GIN-FUZZY-SEARCH-LIMIT)
:   The primary goal of developing GIN indexes was
    to create support for highly scalable full-text search in
    PostgreSQL, and there are often situations when
    a full-text search returns a very large set of results. Moreover, this
    often happens when the query contains very frequent words, so that the
    large result set is not even useful. Since reading many
    tuples from the disk and sorting them could take a lot of time, this is
    unacceptable for production. (Note that the index search itself is very
    fast.)

    To facilitate controlled execution of such queries,
    GIN has a configurable soft upper limit on the
    number of rows returned: the
    `gin_fuzzy_search_limit` configuration parameter.
    It is set to 0 (meaning no limit) by default.
    If a non-zero limit is set, then the returned set is a subset of
    the whole result set, chosen at random.

    “Soft” means that the actual number of returned results
    could differ somewhat from the specified limit, depending on the query
    and the quality of the system's random number generator.

    From experience, values in the thousands (e.g., 5000 — 20000)
    work well.

<a id="GIN-LIMIT"></a>

### 65.4.6. Limitations [#](#GIN-LIMIT)

GIN assumes that indexable operators are strict. This
means that `extractValue` will not be called at all on a null
item value (instead, a placeholder index entry is created automatically),
and `extractQuery` will not be called on a null query
value either (instead, the query is presumed to be unsatisfiable). Note
however that null key values contained within a non-null composite item
or query value are supported.

<a id="GIN-EXAMPLES"></a>

### 65.4.7. Examples [#](#GIN-EXAMPLES)

The core PostgreSQL distribution
includes the GIN operator classes previously shown in
[Table 65.3](gin.md#GIN-BUILTIN-OPCLASSES-TABLE).
The following `contrib` modules also contain
GIN operator classes:

`btree_gin`
:   B-tree equivalent functionality for several data types

`hstore`
:   Module for storing (key, value) pairs

`intarray`
:   Enhanced support for `int[]`

`pg_trgm`
:   Text similarity using trigram matching

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gin.html)（英文原文，待翻譯）
