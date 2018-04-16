# 11.2. 索引型別

PostgreSQLprovides several index types: B-tree, Hash, GiST, SP-GiST, GIN and BRIN. Each index type uses a different algorithm that is best suited to different types of queries. By default, the`CREATE INDEX`command creates B-tree indexes, which fit the most common situations.

B-trees can handle equality and range queries on data that can be sorted into some ordering. In particular, thePostgreSQLquery planner will consider using a B-tree index whenever an indexed column is involved in a comparison using one of these operators:

| `<` |
| :--- |
| `<=` |
| `=` |
| `>=` |
| `>` |

Constructs equivalent to combinations of these operators, such as`BETWEEN`and`IN`, can also be implemented with a B-tree index search. Also, an`IS NULL`or`IS NOT NULL`condition on an index column can be used with a B-tree index.

The optimizer can also use a B-tree index for queries involving the pattern matching operators`LIKE`and`~`\_if\_the pattern is a constant and is anchored to the beginning of the string — for example,`col LIKE 'foo%'`or`col ~ '^foo'`, but not`col LIKE '%bar'`. However, if your database does not use the C locale you will need to create the index with a special operator class to support indexing of pattern-matching queries; see[Section 11.9](https://www.postgresql.org/docs/10/static/indexes-opclass.html)below. It is also possible to use B-tree indexes for`ILIKE`and`~*`, but only if the pattern starts with non-alphabetic characters, i.e., characters that are not affected by upper/lower case conversion.

B-tree indexes can also be used to retrieve data in sorted order. This is not always faster than a simple scan and sort, but it is often helpful.

Hash indexes can only handle simple equality comparisons. The query planner will consider using a hash index whenever an indexed column is involved in a comparison using the`=`operator. The following command is used to create a hash index:

```text
CREATE INDEX 
name
 ON 
table
 USING HASH (
column
);
```

GiST indexes are not a single kind of index, but rather an infrastructure within which many different indexing strategies can be implemented. Accordingly, the particular operators with which a GiST index can be used vary depending on the indexing strategy \(the_operator class_\). As an example, the standard distribution ofPostgreSQLincludes GiST operator classes for several two-dimensional geometric data types, which support indexed queries using these operators:

| `<<` |  |
| :--- |
| `&<` |  |
| `&>` |  |
| `>>` |  |
| \`&lt;&lt; | \` |
| \`&&lt; | \` |
| \` | &&gt;\` |
| \` | &gt;&gt;\` |
| `@>` |  |
| `<@` |  |
| `~=` |  |
| `&&` |  |

\(See[Section 9.11](https://www.postgresql.org/docs/10/static/functions-geometry.html)for the meaning of these operators.\) The GiST operator classes included in the standard distribution are documented in[Table 62.1](https://www.postgresql.org/docs/10/static/gist-builtin-opclasses.html#gist-builtin-opclasses-table). Many other GiST operator classes are available in the`contrib`collection or as separate projects. For more information see[Chapter 62](https://www.postgresql.org/docs/10/static/gist.html).

GiST indexes are also capable of optimizing“nearest-neighbor”searches, such as

```text
SELECT * FROM places ORDER BY location 
<
-
>
 point '(101,456)' LIMIT 10;
```

which finds the ten places closest to a given target point. The ability to do this is again dependent on the particular operator class being used. In[Table 62.1](https://www.postgresql.org/docs/10/static/gist-builtin-opclasses.html#gist-builtin-opclasses-table), operators that can be used in this way are listed in the column“Ordering Operators”.

SP-GiST indexes, like GiST indexes, offer an infrastructure that supports various kinds of searches. SP-GiST permits implementation of a wide range of different non-balanced disk-based data structures, such as quadtrees, k-d trees, and radix trees \(tries\). As an example, the standard distribution ofPostgreSQLincludes SP-GiST operator classes for two-dimensional points, which support indexed queries using these operators:

| `<<` |
| :--- |
| `>>` |
| `~=` |
| `<@` |
| `<^` |
| `>^` |

\(See[Section 9.11](https://www.postgresql.org/docs/10/static/functions-geometry.html)for the meaning of these operators.\) The SP-GiST operator classes included in the standard distribution are documented in[Table 63.1](https://www.postgresql.org/docs/10/static/spgist-builtin-opclasses.html#spgist-builtin-opclasses-table). For more information see[Chapter 63](https://www.postgresql.org/docs/10/static/spgist.html).

GIN indexes are“inverted indexes”which are appropriate for data values that contain multiple component values, such as arrays. An inverted index contains a separate entry for each component value, and can efficiently handle queries that test for the presence of specific component values.

Like GiST and SP-GiST, GIN can support many different user-defined indexing strategies, and the particular operators with which a GIN index can be used vary depending on the indexing strategy. As an example, the standard distribution ofPostgreSQLincludes a GIN operator class for arrays, which supports indexed queries using these operators:

| `<@` |
| :--- |
| `@>` |
| `=` |
| `&&` |

\(See[Section 9.18](https://www.postgresql.org/docs/10/static/functions-array.html)for the meaning of these operators.\) The GIN operator classes included in the standard distribution are documented in[Table 64.1](https://www.postgresql.org/docs/10/static/gin-builtin-opclasses.html#gin-builtin-opclasses-table). Many other GIN operator classes are available in the`contrib`collection or as separate projects. For more information see[Chapter 64](https://www.postgresql.org/docs/10/static/gin.html).

BRIN indexes \(a shorthand for Block Range INdexes\) store summaries about the values stored in consecutive physical block ranges of a table. Like GiST, SP-GiST and GIN, BRIN can support many different indexing strategies, and the particular operators with which a BRIN index can be used vary depending on the indexing strategy. For data types that have a linear sort order, the indexed data corresponds to the minimum and maximum values of the values in the column for each block range. This supports indexed queries using these operators:

| `<` |
| :--- |
| `<=` |
| `=` |
| `>=` |
| `>` |

The BRIN operator classes included in the standard distribution are documented in[Table 65.1](https://www.postgresql.org/docs/10/static/brin-builtin-opclasses.html#brin-builtin-opclasses-table). For more information see[Chapter 65](https://www.postgresql.org/docs/10/static/brin.html).

