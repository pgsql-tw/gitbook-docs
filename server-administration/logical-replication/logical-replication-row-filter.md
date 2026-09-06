## 29.4. Row Filters [#](#LOGICAL-REPLICATION-ROW-FILTER)

[29.4.1. Row Filter Rules](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RULES)

[29.4.2. Expression Restrictions](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)

[29.4.3. UPDATE Transformations](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)

[29.4.4. Partitioned Tables](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)

[29.4.5. Initial Data Synchronization](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)

[29.4.6. Combining Multiple Row Filters](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)

[29.4.7. Examples](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

By default, all data from all published tables will be replicated to the
appropriate subscribers. The replicated data can be reduced by using a
*row filter*. A user might choose to use row filters
for behavioral, security or performance reasons. If a published table sets a
row filter, a row is replicated only if its data satisfies the row filter
expression. This allows a set of tables to be partially replicated. The row
filter is defined per table. Use a `WHERE` clause after the
table name for each published table that requires data to be filtered out.
The `WHERE` clause must be enclosed by parentheses. See
[CREATE PUBLICATION](../../reference/sql-commands/sql-createpublication.md) for details.

<a id="LOGICAL-REPLICATION-ROW-FILTER-RULES"></a>

### 29.4.1. Row Filter Rules [#](#LOGICAL-REPLICATION-ROW-FILTER-RULES)

Row filters are applied *before* publishing the changes.
If the row filter evaluates to `false` or `NULL`
then the row is not replicated. The `WHERE` clause expression
is evaluated with the same role used for the replication connection (i.e.
the role specified in the
[`CONNECTION`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION)
clause of the [CREATE SUBSCRIPTION](../../reference/sql-commands/sql-createsubscription.md)). Row filters have
no effect for `TRUNCATE` command.

<a id="LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS"></a>

### 29.4.2. Expression Restrictions [#](#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)

The `WHERE` clause allows only simple expressions. It
cannot contain user-defined functions, operators, types, and collations,
system column references or non-immutable built-in functions.

If a publication publishes `UPDATE` or
`DELETE` operations, the row filter `WHERE`
clause must contain only columns that are covered by the replica identity
(see [`REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)). If a publication
publishes only `INSERT` operations, the row filter
`WHERE` clause can use any column.

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS"></a>

### 29.4.3. UPDATE Transformations [#](#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)

Whenever an `UPDATE` is processed, the row filter
expression is evaluated for both the old and new row (i.e. using the data
before and after the update). If both evaluations are `true`,
it replicates the `UPDATE` change. If both evaluations are
`false`, it doesn't replicate the change. If only one of
the old/new rows matches the row filter expression, the `UPDATE`
is transformed to `INSERT` or `DELETE`, to
avoid any data inconsistency. The row on the subscriber should reflect what
is defined by the row filter expression on the publisher.

If the old row satisfies the row filter expression (it was sent to the
subscriber) but the new row doesn't, then, from a data consistency
perspective the old row should be removed from the subscriber.
So the `UPDATE` is transformed into a `DELETE`.

If the old row doesn't satisfy the row filter expression (it wasn't sent
to the subscriber) but the new row does, then, from a data consistency
perspective the new row should be added to the subscriber.
So the `UPDATE` is transformed into an `INSERT`.

[Table 29.1](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY)
summarizes the applied transformations.

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY"></a>

**Table 29.1. `UPDATE` Transformation Summary**

<table border="1" class="table" summary="UPDATE Transformation Summary"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Old row</th><th>New row</th><th>Transformation</th></tr></thead><tbody><tr><td>no match</td><td>no match</td><td>don't replicate</td></tr><tr><td>no match</td><td>match</td><td><code class="literal">INSERT</code></td></tr><tr><td>match</td><td>no match</td><td><code class="literal">DELETE</code></td></tr><tr><td>match</td><td>match</td><td><code class="literal">UPDATE</code></td></tr></tbody></table>

<br>

<a id="LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE"></a>

### 29.4.4. Partitioned Tables [#](#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)

If the publication contains a partitioned table, the publication parameter
[`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT)
determines which row filter is used. If `publish_via_partition_root`
is `true`, the *root partitioned table's*
row filter is used. Otherwise, if `publish_via_partition_root`
is `false` (default), each *partition's*
row filter is used.

<a id="LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC"></a>

### 29.4.5. Initial Data Synchronization [#](#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)

If the subscription requires copying pre-existing table data
and a publication contains `WHERE` clauses, only data that
satisfies the row filter expressions is copied to the subscriber.

If the subscription has several publications in which a table has been
published with different `WHERE` clauses, rows that satisfy
*any* of the expressions will be copied. See
[Section 29.4.6](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING) for details.

### Warning

Because initial data synchronization does not take into account the
[`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
parameter when copying existing table data, some rows may be copied that
would not be replicated using DML. Refer to
[Section 29.9.1](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT), and see
[Section 29.2.2](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES) for examples.

### Note

If the subscriber is in a release prior to 15, copying pre-existing data
doesn't use row filters even if they are defined in the publication.
This is because old releases can only copy the entire table data.

<a id="LOGICAL-REPLICATION-ROW-FILTER-COMBINING"></a>

### 29.4.6. Combining Multiple Row Filters [#](#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)

If the subscription has several publications in which the same table has
been published with different row filters (for the same
[`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
operation), those expressions get ORed together, so that rows satisfying
*any* of the expressions will be replicated. This means all
the other row filters for the same table become redundant if:

* One of the publications has no row filter.
* One of the publications was created using
  [`FOR ALL TABLES`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES).
  This clause does not allow row filters.
* One of the publications was created using
  [`FOR TABLES IN SCHEMA`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)
  and the table belongs to the referred schema. This clause does not allow
  row filters.

<a id="LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES"></a>

### 29.4.7. Examples [#](#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

Create some tables to be used in the following examples.

```

/* pub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* pub # */ CREATE TABLE t2(d int, e int, f int, PRIMARY KEY(d));
/* pub # */ CREATE TABLE t3(g int, h int, i int, PRIMARY KEY(g));
```

Create some publications. Publication `p1` has one table
(`t1`) and that table has a row filter. Publication
`p2` has two tables. Table `t1` has no row
filter, and table `t2` has a row filter. Publication
`p3` has two tables, and both of them have a row filter.

```

/* pub # */ CREATE PUBLICATION p1 FOR TABLE t1 WHERE (a > 5 AND c = 'NSW');
/* pub # */ CREATE PUBLICATION p2 FOR TABLE t1, t2 WHERE (e = 99);
/* pub # */ CREATE PUBLICATION p3 FOR TABLE t2 WHERE (d = 10), t3 WHERE (g = 10);
```

`psql` can be used to show the row filter expressions (if
defined) for each publication.

```

/* pub # */ \dRp+
                                         Publication p1
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1" WHERE ((a > 5) AND (c = 'NSW'::text))

                                         Publication p2
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1"
    "public.t2" WHERE (e = 99)

                                         Publication p3
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t2" WHERE (d = 10)
    "public.t3" WHERE (g = 10)
```

`psql` can be used to show the row filter expressions (if
defined) for each table. See that table `t1` is a member
of two publications, but has a row filter only in `p1`.
See that table `t2` is a member of two publications, and
has a different row filter in each of them.

```

/* pub # */ \d t1
                 Table "public.t1"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 a      | integer |           | not null |
 b      | integer |           |          |
 c      | text    |           | not null |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (a, c)
Publications:
    "p1" WHERE ((a > 5) AND (c = 'NSW'::text))
    "p2"

/* pub # */ \d t2
                 Table "public.t2"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 d      | integer |           | not null |
 e      | integer |           |          |
 f      | integer |           |          |
Indexes:
    "t2_pkey" PRIMARY KEY, btree (d)
Publications:
    "p2" WHERE (e = 99)
    "p3" WHERE (d = 10)

/* pub # */ \d t3
                 Table "public.t3"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 g      | integer |           | not null |
 h      | integer |           |          |
 i      | integer |           |          |
Indexes:
    "t3_pkey" PRIMARY KEY, btree (g)
Publications:
    "p3" WHERE (g = 10)
```

On the subscriber node, create a table `t1` with the same
definition as the one on the publisher, and also create the subscription
`s1` that subscribes to the publication `p1`.

```

/* sub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* sub # */ CREATE SUBSCRIPTION s1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s1'
/* sub - */ PUBLICATION p1;
```

Insert some rows. Only the rows satisfying the `t1 WHERE`
clause of publication `p1` are replicated.

```

/* pub # */ INSERT INTO t1 VALUES (2, 102, 'NSW');
/* pub # */ INSERT INTO t1 VALUES (3, 103, 'QLD');
/* pub # */ INSERT INTO t1 VALUES (4, 104, 'VIC');
/* pub # */ INSERT INTO t1 VALUES (5, 105, 'ACT');
/* pub # */ INSERT INTO t1 VALUES (6, 106, 'NSW');
/* pub # */ INSERT INTO t1 VALUES (7, 107, 'NT');
/* pub # */ INSERT INTO t1 VALUES (8, 108, 'QLD');
/* pub # */ INSERT INTO t1 VALUES (9, 109, 'NSW');

/* pub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 2 | 102 | NSW
 3 | 103 | QLD
 4 | 104 | VIC
 5 | 105 | ACT
 6 | 106 | NSW
 7 | 107 | NT
 8 | 108 | QLD
 9 | 109 | NSW
(8 rows)
```

```

/* sub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 6 | 106 | NSW
 9 | 109 | NSW
(2 rows)
```

Update some data, where the old and new row values both
satisfy the `t1 WHERE` clause of publication
`p1`. The `UPDATE` replicates
the change as normal.

```

/* pub # */ UPDATE t1 SET b = 999 WHERE a = 6;

/* pub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 2 | 102 | NSW
 3 | 103 | QLD
 4 | 104 | VIC
 5 | 105 | ACT
 7 | 107 | NT
 8 | 108 | QLD
 9 | 109 | NSW
 6 | 999 | NSW
(8 rows)
```

```

/* sub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 9 | 109 | NSW
 6 | 999 | NSW
(2 rows)
```

Update some data, where the old row values did not satisfy
the `t1 WHERE` clause of publication `p1`,
but the new row values do satisfy it. The `UPDATE` is
transformed into an `INSERT` and the change is replicated.
See the new row on the subscriber.

```

/* pub # */ UPDATE t1 SET a = 555 WHERE a = 2;

/* pub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   3 | 103 | QLD
   4 | 104 | VIC
   5 | 105 | ACT
   7 | 107 | NT
   8 | 108 | QLD
   9 | 109 | NSW
   6 | 999 | NSW
 555 | 102 | NSW
(8 rows)
```

```

/* sub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   9 | 109 | NSW
   6 | 999 | NSW
 555 | 102 | NSW
(3 rows)
```

Update some data, where the old row values satisfied
the `t1 WHERE` clause of publication `p1`,
but the new row values do not satisfy it. The `UPDATE` is
transformed into a `DELETE` and the change is replicated.
See that the row is removed from the subscriber.

```

/* pub # */ UPDATE t1 SET c = 'VIC' WHERE a = 9;

/* pub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   3 | 103 | QLD
   4 | 104 | VIC
   5 | 105 | ACT
   7 | 107 | NT
   8 | 108 | QLD
   6 | 999 | NSW
 555 | 102 | NSW
   9 | 109 | VIC
(8 rows)
```

```

/* sub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   6 | 999 | NSW
 555 | 102 | NSW
(2 rows)
```

The following examples show how the publication parameter
[`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT)
determines whether the row filter of the parent or child table will be used
in the case of partitioned tables.

Create a partitioned table on the publisher.

```

/* pub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* pub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

Create the same tables on the subscriber.

```

/* sub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* sub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

Create a publication `p4`, and then subscribe to it. The
publication parameter `publish_via_partition_root` is set
as true. There are row filters defined on both the partitioned table
(`parent`), and on the partition (`child`).

```

/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent WHERE (a < 5), child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=true);
```

```

/* sub # */ CREATE SUBSCRIPTION s4
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s4'
/* sub - */ PUBLICATION p4;
```

Insert some values directly into the `parent` and
`child` tables. They replicate using the row filter of
`parent` (because `publish_via_partition_root`
is true).

```

/* pub # */ INSERT INTO parent VALUES (2), (4), (6);
/* pub # */ INSERT INTO child VALUES (3), (5), (7);

/* pub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
 5
 6
 7
(6 rows)
```

```

/* sub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
(3 rows)
```

Repeat the same test, but with a different value for `publish_via_partition_root`.
The publication parameter `publish_via_partition_root` is
set as false. A row filter is defined on the partition (`child`).

```

/* pub # */ DROP PUBLICATION p4;
/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent, child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=false);
```

```

/* sub # */ ALTER SUBSCRIPTION s4 REFRESH PUBLICATION;
```

Do the inserts on the publisher same as before. They replicate using the
row filter of `child` (because
`publish_via_partition_root` is false).

```

/* pub # */ TRUNCATE parent;
/* pub # */ INSERT INTO parent VALUES (2), (4), (6);
/* pub # */ INSERT INTO child VALUES (3), (5), (7);

/* pub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
 5
 6
 7
(6 rows)
```

```

/* sub # */ SELECT * FROM child ORDER BY a;
 a
---
 5
 6
 7
(3 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-row-filter.html)（英文原文，待翻譯）
