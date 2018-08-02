---
description: 版本：10
---

# CREATE INDEX

CREATE INDEX — 定義一個新的索引

### 語法

```text
CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] name ] ON table_name [ USING method ]
    ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
    [ WITH ( storage_parameter = value [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    [ WHERE predicate ]
```

### Description

`CREATE INDEX` constructs an index on the specified column\(s\) of the specified relation, which can be a table or a materialized view. Indexes are primarily used to enhance database performance \(though inappropriate use can result in slower performance\).

The key field\(s\) for the index are specified as column names, or alternatively as expressions written in parentheses. Multiple fields can be specified if the index method supports multicolumn indexes.

An index field can be an expression computed from the values of one or more columns of the table row. This feature can be used to obtain fast access to data based on some transformation of the basic data. For example, an index computed on `upper(col)` would allow the clause `WHERE upper(col) = 'JIM'` to use an index.

PostgreSQL provides the index methods B-tree, hash, GiST, SP-GiST, GIN, and BRIN. Users can also define their own index methods, but that is fairly complicated.

When the `WHERE` clause is present, a _partial index_ is created. A partial index is an index that contains entries for only a portion of a table, usually a portion that is more useful for indexing than the rest of the table. For example, if you have a table that contains both billed and unbilled orders where the unbilled orders take up a small fraction of the total table and yet that is an often used section, you can improve performance by creating an index on just that portion. Another possible application is to use `WHERE` with `UNIQUE` to enforce uniqueness over a subset of a table. See [Section 11.8](https://www.postgresql.org/docs/10/static/indexes-partial.html) for more discussion.

The expression used in the `WHERE` clause can refer only to columns of the underlying table, but it can use all columns, not just the ones being indexed. Presently, subqueries and aggregate expressions are also forbidden in `WHERE`. The same restrictions apply to index fields that are expressions.

All functions and operators used in an index definition must be “immutable”, that is, their results must depend only on their arguments and never on any outside influence \(such as the contents of another table or the current time\). This restriction ensures that the behavior of the index is well-defined. To use a user-defined function in an index expression or `WHERE` clause, remember to mark the function immutable when you create it.

### Parameters

`UNIQUE`

Causes the system to check for duplicate values in the table when the index is created \(if data already exist\) and each time data is added. Attempts to insert or update data which would result in duplicate entries will generate an error.

`CONCURRENTLY`

When this option is used, PostgreSQL will build the index without taking any locks that prevent concurrent inserts, updates, or deletes on the table; whereas a standard index build locks out writes \(but not reads\) on the table until it's done. There are several caveats to be aware of when using this option — see [Building Indexes Concurrently](https://www.postgresql.org/docs/10/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY).

`IF NOT EXISTS`

Do not throw an error if a relation with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing index is anything like the one that would have been created. Index name is required when `IF NOT EXISTS` is specified.

_`name`_

The name of the index to be created. No schema name can be included here; the index is always created in the same schema as its parent table. If the name is omitted, PostgreSQL chooses a suitable name based on the parent table's name and the indexed column name\(s\).

_`table_name`_

The name \(possibly schema-qualified\) of the table to be indexed.

_`method`_

The name of the index method to be used. Choices are `btree`, `hash`, `gist`, `spgist`, `gin`, and `brin`. The default method is `btree`.

_`column_name`_

The name of a column of the table.

_`expression`_

An expression based on one or more columns of the table. The expression usually must be written with surrounding parentheses, as shown in the syntax. However, the parentheses can be omitted if the expression has the form of a function call.

_`collation`_

The name of the collation to use for the index. By default, the index uses the collation declared for the column to be indexed or the result collation of the expression to be indexed. Indexes with non-default collations can be useful for queries that involve expressions using non-default collations.

_`opclass`_

The name of an operator class. See below for details.

`ASC`

Specifies ascending sort order \(which is the default\).

`DESC`

Specifies descending sort order.

`NULLS FIRST`

Specifies that nulls sort before non-nulls. This is the default when `DESC` is specified.

`NULLS LAST`

Specifies that nulls sort after non-nulls. This is the default when `DESC` is not specified.

_`storage_parameter`_

The name of an index-method-specific storage parameter. See [Index Storage Parameters](https://www.postgresql.org/docs/10/static/sql-createindex.html#SQL-CREATEINDEX-STORAGE-PARAMETERS) for details.

_`tablespace_name`_

The tablespace in which to create the index. If not specified, [default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE) is consulted, or [temp\_tablespaces](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TEMP-TABLESPACES) for indexes on temporary tables.

_`predicate`_

The constraint expression for a partial index.

#### Index Storage Parameters

The optional `WITH` clause specifies _storage parameters_ for the index. Each index method has its own set of allowed storage parameters. The B-tree, hash, GiST and SP-GiST index methods all accept this parameter:

`fillfactor`

The fillfactor for an index is a percentage that determines how full the index method will try to pack index pages. For B-trees, leaf pages are filled to this percentage during initial index build, and also when extending the index at the right \(adding new largest key values\). If pages subsequently become completely full, they will be split, leading to gradual degradation in the index's efficiency. B-trees use a default fillfactor of 90, but any integer value from 10 to 100 can be selected. If the table is static then fillfactor 100 is best to minimize the index's physical size, but for heavily updated tables a smaller fillfactor is better to minimize the need for page splits. The other index methods use fillfactor in different but roughly analogous ways; the default fillfactor varies between methods.

GiST indexes additionally accept this parameter:

`buffering`

Determines whether the buffering build technique described in [Section 62.4.1](https://www.postgresql.org/docs/10/static/gist-implementation.html#GIST-BUFFERING-BUILD) is used to build the index. With `OFF` it is disabled, with `ON` it is enabled, and with `AUTO` it is initially disabled, but turned on on-the-fly once the index size reaches [effective\_cache\_size](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE). The default is `AUTO`.

GIN indexes accept different parameters:

`fastupdate`

This setting controls usage of the fast update technique described in [Section 64.4.1](https://www.postgresql.org/docs/10/static/gin-implementation.html#GIN-FAST-UPDATE). It is a Boolean parameter: `ON` enables fast update, `OFF` disables it. \(Alternative spellings of `ON` and `OFF` are allowed as described in [Section 19.1](https://www.postgresql.org/docs/10/static/config-setting.html).\) The default is `ON`.

#### Note

Turning `fastupdate` off via `ALTER INDEX` prevents future insertions from going into the list of pending index entries, but does not in itself flush previous entries. You might want to `VACUUM`the table or call `gin_clean_pending_list` function afterward to ensure the pending list is emptied.

`gin_pending_list_limit`

Custom [gin\_pending\_list\_limit](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-GIN-PENDING-LIST-LIMIT) parameter. This value is specified in kilobytes.

BRIN indexes accept different parameters:

`pages_per_range`

Defines the number of table blocks that make up one block range for each entry of a BRIN index \(see [Section 65.1](https://www.postgresql.org/docs/10/static/brin-intro.html) for more details\). The default is `128`.

`autosummarize`

Defines whether a summarization run is invoked for the previous page range whenever an insertion is detected on the next one.

#### Building Indexes Concurrently

Creating an index can interfere with regular operation of a database. Normally PostgreSQL locks the table to be indexed against writes and performs the entire index build with a single scan of the table. Other transactions can still read the table, but if they try to insert, update, or delete rows in the table they will block until the index build is finished. This could have a severe effect if the system is a live production database. Very large tables can take many hours to be indexed, and even for smaller tables, an index build can lock out writers for periods that are unacceptably long for a production system.

PostgreSQL supports building indexes without locking out writes. This method is invoked by specifying the `CONCURRENTLY` option of `CREATE INDEX`. When this option is used, PostgreSQL must perform two scans of the table, and in addition it must wait for all existing transactions that could potentially modify or use the index to terminate. Thus this method requires more total work than a standard index build and takes significantly longer to complete. However, since it allows normal operations to continue while the index is built, this method is useful for adding new indexes in a production environment. Of course, the extra CPU and I/O load imposed by the index creation might slow other operations.

In a concurrent index build, the index is actually entered into the system catalogs in one transaction, then two table scans occur in two more transactions. Before each table scan, the index build must wait for existing transactions that have modified the table to terminate. After the second scan, the index build must wait for any transactions that have a snapshot \(see [Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html)\) predating the second scan to terminate. Then finally the index can be marked ready for use, and the `CREATE INDEX` command terminates. Even then, however, the index may not be immediately usable for queries: in the worst case, it cannot be used as long as transactions exist that predate the start of the index build.

If a problem arises while scanning the table, such as a deadlock or a uniqueness violation in a unique index, the `CREATE INDEX` command will fail but leave behind an “invalid” index. This index will be ignored for querying purposes because it might be incomplete; however it will still consume update overhead. The psql `\d` command will report such an index as `INVALID`:

```text
postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Collation | Nullable | Default 
--------+---------+-----------+----------+---------
 col    | integer |           |          | 
Indexes:
    "idx" btree (col) INVALID
```

The recommended recovery method in such cases is to drop the index and try again to perform `CREATE INDEX CONCURRENTLY`. \(Another possibility is to rebuild the index with `REINDEX`. However, since `REINDEX` does not support concurrent builds, this option is unlikely to seem attractive.\)

Another caveat when building a unique index concurrently is that the uniqueness constraint is already being enforced against other transactions when the second table scan begins. This means that constraint violations could be reported in other queries prior to the index becoming available for use, or even in cases where the index build eventually fails. Also, if a failure does occur in the second scan, the “invalid” index continues to enforce its uniqueness constraint afterwards.

Concurrent builds of expression indexes and partial indexes are supported. Errors occurring in the evaluation of these expressions could cause behavior similar to that described above for unique constraint violations.

Regular index builds permit other regular index builds on the same table to occur in parallel, but only one concurrent index build can occur on a table at a time. In both cases, no other types of schema modification on the table are allowed meanwhile. Another difference is that a regular `CREATE INDEX` command can be performed within a transaction block, but `CREATE INDEX CONCURRENTLY` cannot.

### Notes

See [Chapter 11](https://www.postgresql.org/docs/10/static/indexes.html) for information about when indexes can be used, when they are not used, and in which particular situations they can be useful.

Currently, only the B-tree, GiST, GIN, and BRIN index methods support multicolumn indexes. Up to 32 fields can be specified by default. \(This limit can be altered when building PostgreSQL.\) Only B-tree currently supports unique indexes.

An _operator class_ can be specified for each column of an index. The operator class identifies the operators to be used by the index for that column. For example, a B-tree index on four-byte integers would use the `int4_ops` class; this operator class includes comparison functions for four-byte integers. In practice the default operator class for the column's data type is usually sufficient. The main point of having operator classes is that for some data types, there could be more than one meaningful ordering. For example, we might want to sort a complex-number data type either by absolute value or by real part. We could do this by defining two operator classes for the data type and then selecting the proper class when making an index. More information about operator classes is in [Section 11.9](https://www.postgresql.org/docs/10/static/indexes-opclass.html) and in [Section 37.14](https://www.postgresql.org/docs/10/static/xindex.html).

For index methods that support ordered scans \(currently, only B-tree\), the optional clauses `ASC`, `DESC`, `NULLS FIRST`, and/or `NULLS LAST` can be specified to modify the sort ordering of the index. Since an ordered index can be scanned either forward or backward, it is not normally useful to create a single-column `DESC` index — that sort ordering is already available with a regular index. The value of these options is that multicolumn indexes can be created that match the sort ordering requested by a mixed-ordering query, such as `SELECT ... ORDER BY x ASC, y DESC`. The `NULLS` options are useful if you need to support “nulls sort low” behavior, rather than the default “nulls sort high”, in queries that depend on indexes to avoid sorting steps.

For most index methods, the speed of creating an index is dependent on the setting of [maintenance\_work\_mem](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM). Larger values will reduce the time needed for index creation, so long as you don't make it larger than the amount of memory really available, which would drive the machine into swapping.

Use [DROP INDEX](https://www.postgresql.org/docs/10/static/sql-dropindex.html) to remove an index.

Prior releases of PostgreSQL also had an R-tree index method. This method has been removed because it had no significant advantages over the GiST method. If `USING rtree` is specified, `CREATE INDEX` will interpret it as `USING gist`, to simplify conversion of old databases to GiST.

### 範例

要在資料表中的欄位 title 上建立 B-tree 索引：

```text
CREATE UNIQUE INDEX title_idx ON films (title);
```

要在表示式 lower\(title\) 上建立索引，允許有效的不分大小寫搜尋：

```text
CREATE INDEX ON films ((lower(title)));
```

（在此範例中，我們選擇省略索引名稱，因此系統將選擇一個名稱，通常為 films\_lower\_idx。）

要使用非預設排序規則建立索引：

```text
CREATE INDEX title_idx_german ON films (title COLLATE "de_DE");
```

要建立具有空值的非預設排序順序索引：

```text
CREATE INDEX title_idx_nulls_low ON films (title NULLS FIRST);
```

要使用非預設 fill factor 建立索引：

```text
CREATE UNIQUE INDEX title_idx ON films (title) WITH (fillfactor = 70);
```

要建立停用快速更新的 GIN 索引：

```text
CREATE INDEX gin_idx ON documents_table USING GIN (locations) WITH (fastupdate = off);
```

要在資料表 film 中的欄位 code 上建立索引，並將索引放在資料表空間 indexspace 中：

```text
CREATE INDEX code_idx ON films (code) TABLESPACE indexspace;
```

要在 point 屬性上建立 GiST 索引，以便我們可以在轉換函數的結果上有效地使用 box 運算子：

```text
CREATE INDEX pointloc
    ON points USING gist (box(location,location));
SELECT * FROM points
    WHERE box(location,location) && '(0,0),(1,1)'::box;
```

要建立索引但不鎖定對資料表的寫入：

```text
CREATE INDEX CONCURRENTLY sales_quantity_index ON sales_table (quantity);
```

### 相容性

CREATE INDEX 是 PostgreSQL 延伸語法。SQL 標準中沒有索引的規定。

### 參閱

[ALTER INDEX](alter-index.md), [DROP INDEX](drop-index.md)

