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

### 說明

CREATE INDEX 在指定關連的指定欄位上建構索引，該索引可以是資料表或具體化檢視表。索引主要用於增強資料庫效能（儘管不恰當的使用會導致效能降低）。

索引的主要欄位指定欄位名稱，或者作為括號中的表示式指定。如果索引方法支援多欄位索引，則可以指定多個欄位。

索引欄位可以是根據資料表的一個欄位或多個欄位的計算表示式。此功能可用於基於對基本資料的某些轉換來快速存取資料。例如，在 upper\(col\) 上計算的索引將允許子句 WHERE upper\(col\) = 'JIM' 使用索引。

PostgreSQL 提供索引方法 B-tree，hash，GiST，SP-GiST，GIN 和 BRIN。使用者也可以定義自己的索引方法，但這相當複雜。

WHERE子句存在時，將建立部分索引。部分索引是一個索引，它只包含資料表的一部分項目，通常是比索引的其餘部分更有用的索引部分。例如，如果您的資料表包含已開票和未開單的訂單，其中未開單的訂單佔據總資料表的一小部分，但這是一個經常使用的部分，您可以透過僅在該部分上建立索引來提高效能。另一個可能的應用是使用帶有 UNIQUE 的 WHERE 來強制資料表子集的唯一性。有關更多討論，請參閱[第 11.8 節](../../the-sql-language/index/partial-indexes.md)。

WHERE 子句中使用的表示式只能引用基礎資料表的欄位，但它可以使用所有欄位，而不僅僅是被索引的欄位。目前，WHERE 中也禁止使用子查詢和彙總資料表示式。相同的限制適用於作為表示式的索引欄位。

索引定義中使用的所有函數和運算符必須是「immutable」，也就是說，它們的結果必須僅依賴於它們的參數，而不是任何外部影響（例如另一個資料表的內容或目前時間）。此限制可確保明確定義索引的行為。要在索引表示式或 WHERE 子句中使用使用者定義的函數，請記住在建立函數時將該函數標記為 immutable。

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

### 注意

有關何時可以使用索引，何時不使用索引以及哪些特定情況可以使用索引的訊息，請參閱[第 11 章](../../the-sql-language/index/)。

目前，只有B-tree，GiST，GIN 和 BRIN 索引方法支持多欄位索引。預設情況下最多可以指定 32 個欄位。（編譯 PostgreSQL 時可以變更此限制。）只有 B-tree 目前支援唯一索引。

可以為索引的每個欄位指定運算子類。運算子類識別該欄位的索引要使用的運算子。例如，4 bytes 整數的 B-tree 索引將使用 int4\_ops 類；此運算子類包括 4 bytes 整數的比較函數。實際上，欄位資料型別的預設運算子類通常就足夠了。擁有運算子類的要點是，對於某些資料型別，可能存在多個有意義的排序。例如，我們可能希望按絕對值或複數資料型別的實部進行排序。我們可以透過為資料型別定義兩個運算子類，然後在建立索引時選擇適當的類。有關運算子類的更多訊息，請參閱[第 11.9 節](../../the-sql-language/index/operator-classes-and-operator-families.md)和[第 37.14 節](../../server-programming/extending-sql/interfacing-extensions-to-indexes.md)。

對於支援有序掃描的索引方法（目前只有 B-tree），可以指定選擇性子句 ASC，DESC，NULLS FIRST 和 NULLS LAST 來修改索引的排序順序。由於可以向前或向後掃描有序索引，因此建立單欄位 DESC 索引並不常用 - 排序順序已經可用於一般性索引。這些選項的值是可以建立多欄位索引，該索引搭配混合排序查詢所請求的排序順序，例如 SELECT ... ORDER BY x ASC, y DESC。如果您需要在依賴於索引以避免排序步驟的查詢中支援「nulls sort low」行為而不是預設的「nulls sort high」，那麼 NULLS 選項很有用。

對於大多數索引方法，建立索引的速度取決於 [maintenance\_work\_mem](../../server-administration/server-configuration/resource-consumption.md#19-4-1) 的設定。較大的值將減少索引建立所需的時間，只要您不要使其大於真正可用的記憶體大小，否則將驅使主機使用 SWAP。

使用 [DROP INDEX](drop-index.md) 移除索引。

PostgreSQL 的早期版本也有一個 R-tree 索引方法。此方法已被移除，因為它沒有 GiST 方法的顯著優勢。如果指定了 USING rtree，CREATE INDEX 會將其解釋為USING gist，以簡化舊資料庫到 GiST 的轉換。

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

