## 65.1. B-Tree Indexes [#](#BTREE)

[65.1.1. Introduction](btree.md#BTREE-INTRO)

[65.1.2. Behavior of B-Tree Operator Classes](btree.md#BTREE-BEHAVIOR)

[65.1.3. B-Tree Support Functions](btree.md#BTREE-SUPPORT-FUNCS)

[65.1.4. Implementation](btree.md#BTREE-IMPLEMENTATION)

<a id="id-1.10.17.2.2"></a><a id="BTREE-INTRO"></a>

### 65.1.1. Introduction [#](#BTREE-INTRO)

PostgreSQL includes an implementation of the
standard btree (multi-way balanced tree) index data
structure. Any data type that can be sorted into a well-defined linear
order can be indexed by a btree index. The only limitation is that an
index entry cannot exceed approximately one-third of a page (after TOAST
compression, if applicable).

Because each btree operator class imposes a sort order on its data type,
btree operator classes (or, really, operator families) have come to be
used as PostgreSQL's general representation
and understanding of sorting semantics. Therefore, they've acquired
some features that go beyond what would be needed just to support btree
indexes, and parts of the system that are quite distant from the
btree AM make use of them.

<a id="BTREE-BEHAVIOR"></a>

### 65.1.2. Behavior of B-Tree Operator Classes [#](#BTREE-BEHAVIOR)

As shown in [Table 36.3](../../server-programming/extend/xindex.md#XINDEX-BTREE-STRAT-TABLE), a btree operator
class must provide five comparison operators,
`<`,
`<=`,
`=`,
`>=` and
`>`.
One might expect that `<>` should also be part of
the operator class, but it is not, because it would almost never be
useful to use a `<>` WHERE clause in an index
search. (For some purposes, the planner treats `<>`
as associated with a btree operator class; but it finds that operator via
the `=` operator's negator link, rather than
from `pg_amop`.)

When several data types share near-identical sorting semantics, their
operator classes can be grouped into an operator family. Doing so is
advantageous because it allows the planner to make deductions about
cross-type comparisons. Each operator class within the family should
contain the single-type operators (and associated support functions)
for its input data type, while cross-type comparison operators and
support functions are “loose” in the family. It is
recommendable that a complete set of cross-type operators be included
in the family, thus ensuring that the planner can represent any
comparison conditions that it deduces from transitivity.

There are some basic assumptions that a btree operator family must
satisfy:

* An `=` operator must be an equivalence relation; that
  is, for all non-null values *`A`*,
  *`B`*, *`C`* of the
  data type:

  * *`A`* `=`
    *`A`* is true
    (*reflexive law*)
  * if *`A`* `=`
    *`B`*,
    then *`B`* `=`
    *`A`*
    (*symmetric law*)
  * if *`A`* `=`
    *`B`* and *`B`*
    `=` *`C`*,
    then *`A`* `=`
    *`C`*
    (*transitive law*)
* A `<` operator must be a strong ordering relation;
  that is, for all non-null values *`A`*,
  *`B`*, *`C`*:

  * *`A`* `<`
    *`A`* is false
    (*irreflexive law*)
  * if *`A`* `<`
    *`B`*
    and *`B`* `<`
    *`C`*,
    then *`A`* `<`
    *`C`*
    (*transitive law*)
* Furthermore, the ordering is total; that is, for all non-null
  values *`A`*, *`B`*:

  * exactly one of *`A`* `<`
    *`B`*, *`A`*
    `=` *`B`*, and
    *`B`* `<`
    *`A`* is true
    (*trichotomy law*)

  (The trichotomy law justifies the definition of the comparison support
  function, of course.)

The other three operators are defined in terms of `=`
and `<` in the obvious way, and must act consistently
with them.

For an operator family supporting multiple data types, the above laws must
hold when *`A`*, *`B`*,
*`C`* are taken from any data types in the family.
The transitive laws are the trickiest to ensure, as in cross-type
situations they represent statements that the behaviors of two or three
different operators are consistent.
As an example, it would not work to put `float8`
and `numeric` into the same operator family, at least not with
the current semantics that `numeric` values are converted
to `float8` for comparison to a `float8`. Because
of the limited accuracy of `float8`, this means there are
distinct `numeric` values that will compare equal to the
same `float8` value, and thus the transitive law would fail.

Another requirement for a multiple-data-type family is that any implicit
or binary-coercion casts that are defined between data types included in
the operator family must not change the associated sort ordering.

It should be fairly clear why a btree index requires these laws to hold
within a single data type: without them there is no ordering to arrange
the keys with. Also, index searches using a comparison key of a
different data type require comparisons to behave sanely across two
data types. The extensions to three or more data types within a family
are not strictly required by the btree index mechanism itself, but the
planner relies on them for optimization purposes.

<a id="BTREE-SUPPORT-FUNCS"></a>

### 65.1.3. B-Tree Support Functions [#](#BTREE-SUPPORT-FUNCS)

As shown in [Table 36.9](../../server-programming/extend/xindex.md#XINDEX-BTREE-SUPPORT-TABLE), btree defines
one required and five optional support functions. The six
user-defined methods are:

`order`
:   For each combination of data types that a btree operator family
    provides comparison operators for, it must provide a comparison
    support function, registered in
    `pg_amproc` with support function number 1
    and
    `amproclefttype`/`amprocrighttype`
    equal to the left and right data types for the comparison (i.e.,
    the same data types that the matching operators are registered
    with in `pg_amop`). The comparison
    function must take two non-null values
    *`A`* and *`B`* and
    return an `int32` value that is
    `<` `0`,
    `0`, or `>`
    `0` when *`A`*
    `<` *`B`*,
    *`A`* `=`
    *`B`*, or *`A`*
    `>` *`B`*,
    respectively. A null result is disallowed: all values of the
    data type must be comparable. See
    `src/backend/access/nbtree/nbtcompare.c` for
    examples.

    If the compared values are of a collatable data type, the
    appropriate collation OID will be passed to the comparison
    support function, using the standard
    `PG_GET_COLLATION()` mechanism.

`sortsupport`
:   Optionally, a btree operator family may provide *sort
    support* function(s), registered under support
    function number 2. These functions allow implementing
    comparisons for sorting purposes in a more efficient way than
    naively calling the comparison support function. The APIs
    involved in this are defined in
    `src/include/utils/sortsupport.h`.

`in_range`
:   <a id="id-1.10.17.2.5.3.3.2.1"></a><a id="id-1.10.17.2.5.3.3.2.2"></a>

    Optionally, a btree operator family may provide
    *in_range* support function(s), registered
    under support function number 3. These are not used during btree
    index operations; rather, they extend the semantics of the
    operator family so that it can support window clauses containing
    the `RANGE` *`offset`*
    `PRECEDING` and `RANGE`
    *`offset`* `FOLLOWING`
    frame bound types (see [Section 4.2.8](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)). Fundamentally, the extra
    information provided is how to add or subtract an
    *`offset`* value in a way that is
    compatible with the family's data ordering.

    An `in_range` function must have the signature

    ```

    in_range(val type1, base type1, offset type2, sub bool, less bool)
    returns bool
    ```

    *`val`* and
    *`base`* must be of the same type, which
    is one of the types supported by the operator family (i.e., a
    type for which it provides an ordering). However,
    *`offset`* could be of a different type,
    which might be one otherwise unsupported by the family. An
    example is that the built-in `time_ops` family
    provides an `in_range` function that has
    *`offset`* of type `interval`.
    A family can provide `in_range` functions for
    any of its supported types and one or more
    *`offset`* types. Each
    `in_range` function should be entered in
    `pg_amproc` with
    `amproclefttype` equal to
    `type1` and `amprocrighttype`
    equal to `type2`.

    The essential semantics of an `in_range`
    function depend on the two Boolean flag parameters. It should
    add or subtract *`base`* and
    *`offset`*, then compare
    *`val`* to the result, as follows:

    * if `!`*`sub`* and
      `!`*`less`*, return
      *`val`* `>=`
      (*`base`* `+`
      *`offset`*)
    * if `!`*`sub`* and
      *`less`*, return
      *`val`* `<=`
      (*`base`* `+`
      *`offset`*)
    * if *`sub`* and
      `!`*`less`*, return
      *`val`* `>=`
      (*`base`* `-`
      *`offset`*)
    * if *`sub`* and
      *`less`*, return
      *`val`* `<=`
      (*`base`* `-`
      *`offset`*)

    Before doing so, the function should check the sign of
    *`offset`*: if it is less than zero, raise
    error
    `ERRCODE_INVALID_PRECEDING_OR_FOLLOWING_SIZE`
    (22013) with error text like “invalid preceding or
    following size in window function”. (This is required by
    the SQL standard, although nonstandard operator families might
    perhaps choose to ignore this restriction, since there seems to
    be little semantic necessity for it.) This requirement is
    delegated to the `in_range` function so that
    the core code needn't understand what “less than
    zero” means for a particular data type.

    An additional expectation is that `in_range`
    functions should, if practical, avoid throwing an error if
    *`base`* `+`
    *`offset`* or
    *`base`* `-`
    *`offset`* would overflow. The correct
    comparison result can be determined even if that value would be
    out of the data type's range. Note that if the data type
    includes concepts such as “infinity” or
    “NaN”, extra care may be needed to ensure that
    `in_range`'s results agree with the normal
    sort order of the operator family.

    The results of the `in_range` function must be
    consistent with the sort ordering imposed by the operator family.
    To be precise, given any fixed values of
    *`offset`* and
    *`sub`*, then:

    * If `in_range` with
      *`less`* = true is true for some
      *`val1`* and
      *`base`*, it must be true for every
      *`val2`* `<=`
      *`val1`* with the same
      *`base`*.
    * If `in_range` with
      *`less`* = true is false for some
      *`val1`* and
      *`base`*, it must be false for every
      *`val2`* `>=`
      *`val1`* with the same
      *`base`*.
    * If `in_range` with
      *`less`* = true is true for some
      *`val`* and
      *`base1`*, it must be true for every
      *`base2`* `>=`
      *`base1`* with the same
      *`val`*.
    * If `in_range` with
      *`less`* = true is false for some
      *`val`* and
      *`base1`*, it must be false for every
      *`base2`* `<=`
      *`base1`* with the same
      *`val`*.

    Analogous statements with inverted conditions hold when
    *`less`* = false.

    If the type being ordered (`type1`) is collatable, the
    appropriate collation OID will be passed to the
    `in_range` function, using the standard
    PG_GET_COLLATION() mechanism.

    `in_range` functions need not handle NULL
    inputs, and typically will be marked strict.

`equalimage`
:   Optionally, a btree operator family may provide
    `equalimage` (“equality implies image
    equality”) support functions, registered under support
    function number 4. These functions allow the core code to
    determine when it is safe to apply the btree deduplication
    optimization. Currently, `equalimage`
    functions are only called when building or rebuilding an index.

    An `equalimage` function must have the
    signature

    ```

    equalimage(opcintype oid) returns bool
    ```

    The return value is static information about an operator class
    and collation. Returning `true` indicates that
    the `order` function for the operator class is
    guaranteed to only return `0` (“arguments
    are equal”) when its *`A`* and
    *`B`* arguments are also interchangeable
    without any loss of semantic information. Not registering an
    `equalimage` function or returning
    `false` indicates that this condition cannot be
    assumed to hold.

    The *`opcintype`* argument is the
    `pg_type.oid` of the
    data type that the operator class indexes. This is a convenience
    that allows reuse of the same underlying
    `equalimage` function across operator classes.
    If *`opcintype`* is a collatable data
    type, the appropriate collation OID will be passed to the
    `equalimage` function, using the standard
    `PG_GET_COLLATION()` mechanism.

    As far as the operator class is concerned, returning
    `true` indicates that deduplication is safe (or
    safe for the collation whose OID was passed to its
    `equalimage` function). However, the core
    code will only deem deduplication safe for an index when
    *every* indexed column uses an operator class
    that registers an `equalimage` function, and
    each function actually returns `true` when
    called.

    Image equality is *almost* the same condition
    as simple bitwise equality. There is one subtle difference: When
    indexing a varlena data type, the on-disk representation of two
    image equal datums may not be bitwise equal due to inconsistent
    application of TOAST compression on input.
    Formally, when an operator class's
    `equalimage` function returns
    `true`, it is safe to assume that the
    `datum_image_eq()` C function will always agree
    with the operator class's `order` function
    (provided that the same collation OID is passed to both the
    `equalimage` and `order`
    functions).

    The core code is fundamentally unable to deduce anything about
    the “equality implies image equality” status of an
    operator class within a multiple-data-type family based on
    details from other operator classes in the same family. Also, it
    is not sensible for an operator family to register a cross-type
    `equalimage` function, and attempting to do so
    will result in an error. This is because “equality implies
    image equality” status does not just depend on
    sorting/equality semantics, which are more or less defined at the
    operator family level. In general, the semantics that one
    particular data type implements must be considered separately.

    The convention followed by the operator classes included with the
    core PostgreSQL distribution is to
    register a stock, generic `equalimage`
    function. Most operator classes register
    `btequalimage()`, which indicates that
    deduplication is safe unconditionally. Operator classes for
    collatable data types such as `text` register
    `btvarstrequalimage()`, which indicates that
    deduplication is safe with deterministic collations. Best
    practice for third-party extensions is to register their own
    custom function to retain control.

`options`
:   Optionally, a B-tree operator family may provide
    `options` (“operator class specific
    options”) support functions, registered under support
    function number 5. These functions define a set of user-visible
    parameters that control operator class behavior.

    An `options` support function must have the
    signature

    ```

    options(relopts local_relopts *) returns void
    ```

    The function is passed a pointer to a `local_relopts`
    struct, which needs to be filled with a set of operator class
    specific options. The options can be accessed from other support
    functions using the `PG_HAS_OPCLASS_OPTIONS()` and
    `PG_GET_OPCLASS_OPTIONS()` macros.

    Currently, no B-Tree operator class has an `options`
    support function. B-tree doesn't allow flexible representation of keys
    like GiST, SP-GiST, GIN and BRIN do. So, `options`
    probably doesn't have much application in the current B-tree index
    access method. Nevertheless, this support function was added to B-tree
    for uniformity, and will probably find uses during further
    evolution of B-tree in PostgreSQL.

`skipsupport`
:   Optionally, a btree operator family may provide a *skip
    support* function, registered under support function number 6.
    These functions give the B-tree code a way to iterate through every
    possible value that can be represented by an operator class's underlying
    input type, in key space order. This is used by the core code when it
    applies the skip scan optimization. The APIs involved in this are
    defined in `src/include/utils/skipsupport.h`.

    Operator classes that do not provide a skip support function are still
    eligible to use skip scan. The core code can still use its fallback
    strategy, though that might be suboptimal for some discrete types. It
    usually doesn't make sense (and may not even be feasible) for operator
    classes on continuous types to provide a skip support function.

    It is not sensible for an operator family to register a cross-type
    `skipsupport` function, and attempting to do so will
    result in an error. This is because determining the next indexable value
    must happen by incrementing a value copied from an index tuple. The
    values generated must all be of the same underlying data type (the
    “skipped” index column's opclass input type).

<a id="BTREE-IMPLEMENTATION"></a>

### 65.1.4. Implementation [#](#BTREE-IMPLEMENTATION)

This section covers B-Tree index implementation details that may be
of use to advanced users. See
`src/backend/access/nbtree/README` in the source
distribution for a much more detailed, internals-focused description
of the B-Tree implementation.

<a id="BTREE-STRUCTURE"></a>

#### 65.1.4.1. B-Tree Structure [#](#BTREE-STRUCTURE)

PostgreSQL B-Tree indexes are
multi-level tree structures, where each level of the tree can be
used as a doubly-linked list of pages. A single metapage is stored
in a fixed position at the start of the first segment file of the
index. All other pages are either leaf pages or internal pages.
Leaf pages are the pages on the lowest level of the tree. All
other levels consist of internal pages. Each leaf page contains
tuples that point to table rows. Each internal page contains
tuples that point to the next level down in the tree. Typically,
over 99% of all pages are leaf pages. Both internal pages and leaf
pages use the standard page format described in [Section 66.6](../storage/storage-page-layout.md).

New leaf pages are added to a B-Tree index when an existing leaf
page cannot fit an incoming tuple. A *page
split* operation makes room for items that originally
belonged on the overflowing page by moving a portion of the items
to a new page. Page splits must also insert a new
*downlink* to the new page in the parent page,
which may cause the parent to split in turn. Page splits
“cascade upwards” in a recursive fashion. When the
root page finally cannot fit a new downlink, a *root page
split* operation takes place. This adds a new level to
the tree structure by creating a new root page that is one level
above the original root page.

<a id="BTREE-DELETION"></a>

#### 65.1.4.2. Bottom-up Index Deletion [#](#BTREE-DELETION)

B-Tree indexes are not directly aware that under MVCC, there might
be multiple extant versions of the same logical table row; to an
index, each tuple is an independent object that needs its own index
entry. “Version churn” tuples may sometimes
accumulate and adversely affect query latency and throughput. This
typically occurs with `UPDATE`-heavy workloads
where most individual updates cannot apply the
[HOT optimization.](../storage/storage-hot.md)
Changing the value of only
one column covered by one index during an `UPDATE`
*always* necessitates a new set of index tuples
— one for *each and every* index on the
table. Note in particular that this includes indexes that were not
“logically modified” by the `UPDATE`.
All indexes will need a successor physical index tuple that points
to the latest version in the table. Each new tuple within each
index will generally need to coexist with the original
“updated” tuple for a short period of time (typically
until shortly after the `UPDATE` transaction
commits).

B-Tree indexes incrementally delete version churn index tuples by
performing *bottom-up index deletion* passes.
Each deletion pass is triggered in reaction to an anticipated
“version churn page split”. This only happens with
indexes that are not logically modified by
`UPDATE` statements, where concentrated build up
of obsolete versions in particular pages would occur otherwise. A
page split will usually be avoided, though it's possible that
certain implementation-level heuristics will fail to identify and
delete even one garbage index tuple (in which case a page split or
deduplication pass resolves the issue of an incoming new tuple not
fitting on a leaf page). The worst-case number of versions that
any index scan must traverse (for any single logical row) is an
important contributor to overall system responsiveness and
throughput. A bottom-up index deletion pass targets suspected
garbage tuples in a single leaf page based on
*qualitative* distinctions involving logical
rows and versions. This contrasts with the “top-down”
index cleanup performed by autovacuum workers, which is triggered
when certain *quantitative* table-level
thresholds are exceeded (see [Section 24.1.6](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)).

### Note

Not all deletion operations that are performed within B-Tree
indexes are bottom-up deletion operations. There is a distinct
category of index tuple deletion: *simple index tuple
deletion*. This is a deferred maintenance operation
that deletes index tuples that are known to be safe to delete
(those whose item identifier's `LP_DEAD` bit is
already set). Like bottom-up index deletion, simple index
deletion takes place at the point that a page split is anticipated
as a way of avoiding the split.

Simple deletion is opportunistic in the sense that it can only
take place when recent index scans set the
`LP_DEAD` bits of affected items in passing.
Prior to PostgreSQL 14, the only
category of B-Tree deletion was simple deletion. The main
differences between it and bottom-up deletion are that only the
former is opportunistically driven by the activity of passing
index scans, while only the latter specifically targets version
churn from `UPDATE`s that do not logically modify
indexed columns.

Bottom-up index deletion performs the vast majority of all garbage
index tuple cleanup for particular indexes with certain workloads.
This is expected with any B-Tree index that is subject to
significant version churn from `UPDATE`s that
rarely or never logically modify the columns that the index covers.
The average and worst-case number of versions per logical row can
be kept low purely through targeted incremental deletion passes.
It's quite possible that the on-disk size of certain indexes will
never increase by even one single page/block despite
*constant* version churn from
`UPDATE`s. Even then, an exhaustive “clean
sweep” by a `VACUUM` operation (typically
run in an autovacuum worker process) will eventually be required as
a part of *collective* cleanup of the table and
each of its indexes.

Unlike `VACUUM`, bottom-up index deletion does not
provide any strong guarantees about how old the oldest garbage
index tuple may be. No index can be permitted to retain
“floating garbage” index tuples that became dead prior
to a conservative cutoff point shared by the table and all of its
indexes collectively. This fundamental table-level invariant makes
it safe to recycle table TIDs. This is how it
is possible for distinct logical rows to reuse the same table
TID over time (though this can never happen with
two logical rows whose lifetimes span the same
`VACUUM` cycle).

<a id="BTREE-DEDUPLICATION"></a>

#### 65.1.4.3. Deduplication [#](#BTREE-DEDUPLICATION)

A duplicate is a leaf page tuple (a tuple that points to a table
row) where *all* indexed key columns have values
that match corresponding column values from at least one other leaf
page tuple in the same index. Duplicate tuples are quite common in
practice. B-Tree indexes can use a special, space-efficient
representation for duplicates when an optional technique is
enabled: *deduplication*.

Deduplication works by periodically merging groups of duplicate
tuples together, forming a single *posting list* tuple for each
group. The column key value(s) only appear once in this
representation. This is followed by a sorted array of
TIDs that point to rows in the table. This
significantly reduces the storage size of indexes where each value
(or each distinct combination of column values) appears several
times on average. The latency of queries can be reduced
significantly. Overall query throughput may increase
significantly. The overhead of routine index vacuuming may also be
reduced significantly.

### Note

B-Tree deduplication is just as effective with
“duplicates” that contain a NULL value, even though
NULL values are never equal to each other according to the
`=` member of any B-Tree operator class. As far
as any part of the implementation that understands the on-disk
B-Tree structure is concerned, NULL is just another value from the
domain of indexed values.

The deduplication process occurs lazily, when a new item is
inserted that cannot fit on an existing leaf page, though only when
index tuple deletion could not free sufficient space for the new
item (typically deletion is briefly considered and then skipped
over). Unlike GIN posting list tuples, B-Tree posting list tuples
do not need to expand every time a new duplicate is inserted; they
are merely an alternative physical representation of the original
logical contents of the leaf page. This design prioritizes
consistent performance with mixed read-write workloads. Most
client applications will at least see a moderate performance
benefit from using deduplication. Deduplication is enabled by
default.

`CREATE INDEX` and `REINDEX`
apply deduplication to create posting list tuples, though the
strategy they use is slightly different. Each group of duplicate
ordinary tuples encountered in the sorted input taken from the
table is merged into a posting list tuple
*before* being added to the current pending leaf
page. Individual posting list tuples are packed with as many
TIDs as possible. Leaf pages are written out in
the usual way, without any separate deduplication pass. This
strategy is well-suited to `CREATE INDEX` and
`REINDEX` because they are once-off batch
operations.

Write-heavy workloads that don't benefit from deduplication due to
having few or no duplicate values in indexes will incur a small,
fixed performance penalty (unless deduplication is explicitly
disabled). The `deduplicate_items` storage
parameter can be used to disable deduplication within individual
indexes. There is never any performance penalty with read-only
workloads, since reading posting list tuples is at least as
efficient as reading the standard tuple representation. Disabling
deduplication isn't usually helpful.

It is sometimes possible for unique indexes (as well as unique
constraints) to use deduplication. This allows leaf pages to
temporarily “absorb” extra version churn duplicates.
Deduplication in unique indexes augments bottom-up index deletion,
especially in cases where a long-running transaction holds a
snapshot that blocks garbage collection. The goal is to buy time
for the bottom-up index deletion strategy to become effective
again. Delaying page splits until a single long-running
transaction naturally goes away can allow a bottom-up deletion pass
to succeed where an earlier deletion pass failed.

### Tip

A special heuristic is applied to determine whether a
deduplication pass in a unique index should take place. It can
often skip straight to splitting a leaf page, avoiding a
performance penalty from wasting cycles on unhelpful deduplication
passes. If you're concerned about the overhead of deduplication,
consider setting `deduplicate_items = off`
selectively. Leaving deduplication enabled in unique indexes has
little downside.

Deduplication cannot be used in all cases due to
implementation-level restrictions. Deduplication safety is
determined when `CREATE INDEX` or
`REINDEX` is run.

Note that deduplication is deemed unsafe and cannot be used in the
following cases involving semantically significant differences
among equal datums:

* `text`, `varchar`, and `char`
  cannot use deduplication when a
  *nondeterministic* collation is used. Case
  and accent differences must be preserved among equal datums.
* `numeric` cannot use deduplication. Numeric display
  scale must be preserved among equal datums.
* `jsonb` cannot use deduplication, since the
  `jsonb` B-Tree operator class uses
  `numeric` internally.
* `float4` and `float8` cannot use
  deduplication. These types have distinct representations for
  `-0` and `0`, which are
  nevertheless considered equal. This difference must be
  preserved.

There is one further implementation-level restriction that may be
lifted in a future version of
PostgreSQL:

* Container types (such as composite types, arrays, or range
  types) cannot use deduplication.

There is one further implementation-level restriction that applies
regardless of the operator class or collation used:

* `INCLUDE` indexes can never use deduplication.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/btree.html)（英文原文，待翻譯）
