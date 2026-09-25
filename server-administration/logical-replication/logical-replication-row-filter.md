<a id="LOGICAL-REPLICATION-ROW-FILTER"></a>

## 29.4. 資料列篩選器 [#](#LOGICAL-REPLICATION-ROW-FILTER)

[29.4.1. 資料列篩選規則](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RULES)

[29.4.2. 運算式限制](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)

[29.4.3. UPDATE 轉換](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)

[29.4.4. 分區表](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)

[29.4.5. 初始資料同步](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)

[29.4.6. 合併多個資料列篩選](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)

[29.4.7. 範例](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

依預設，所有已發布資料表的資料都會複寫到對應的訂閱者。透過使用*資料列篩選器*，可以減少被複寫的資料量。使用者可能基於行為、安全性或效能上的考量而選擇使用資料列篩選器。若已發布的資料表設定了資料列篩選器，則只有資料滿足篩選運算式的資料列才會被複寫。這使得一組資料表可以只被部分複寫。資料列篩選器是以資料表為單位個別定義的。針對每個需要篩選掉部分資料的已發布資料表，在資料表名稱之後使用 `WHERE` 子句。`WHERE` 子句必須以括號括住。詳情請見 [CREATE PUBLICATION](../../reference/sql-commands/sql-createpublication.md)。

<a id="LOGICAL-REPLICATION-ROW-FILTER-RULES"></a>

### 29.4.1. 資料列篩選規則 [#](#LOGICAL-REPLICATION-ROW-FILTER-RULES)

資料列篩選器是在發布異動之*前*套用的。若篩選運算式的結果為 `false` 或 `NULL`，則該資料列不會被複寫。`WHERE` 子句運算式是以複寫連線所使用的同一角色來求值（也就是 [CREATE SUBSCRIPTION](../../reference/sql-commands/sql-createsubscription.md) 的 [`CONNECTION`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION) 子句中指定的角色）。資料列篩選器對 `TRUNCATE` 指令沒有作用。

<a id="LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS"></a>

### 29.4.2. 運算式限制 [#](#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)

`WHERE` 子句只允許使用簡單的運算式，不能包含使用者自訂函式、運算子、型別與定序、系統欄位參照，或非不可變（non-immutable）的內建函式。

若發布項目發布了 `UPDATE` 或 `DELETE` 操作，則資料列篩選器的 `WHERE` 子句只能包含屬於複寫識別（replica identity，見 [`REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)）所涵蓋的欄位。若發布項目只發布 `INSERT` 操作，則資料列篩選器的 `WHERE` 子句可以使用任何欄位。

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS"></a>

### 29.4.3. UPDATE 轉換 [#](#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)

每當處理一筆 `UPDATE` 時，會分別以更新前與更新後的資料列（即舊資料與新資料）來求值資料列篩選運算式。若兩者求值結果皆為 `true`，則複寫該筆 `UPDATE` 異動。若兩者求值結果皆為 `false`，則不複寫該筆異動。若只有其中一筆（舊資料或新資料）符合資料列篩選運算式，則該筆 `UPDATE` 會被轉換為 `INSERT` 或 `DELETE`，以避免資料不一致。訂閱者上的資料列應反映發布者上資料列篩選運算式所定義的結果。

若舊資料列滿足篩選運算式（因此已送至訂閱者），但新資料列不滿足，則從資料一致性的角度來看，應將該舊資料列從訂閱者移除。因此該 `UPDATE` 會被轉換為 `DELETE`。

若舊資料列不滿足篩選運算式（因此未送至訂閱者），但新資料列滿足，則從資料一致性的角度來看，應將該新資料列加入訂閱者。因此該 `UPDATE` 會被轉換為 `INSERT`。

[表 29.1](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY) 彙整了套用的轉換規則。

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY"></a>

**表 29.1. `UPDATE` 轉換彙整**

<table border="1" class="table" summary="UPDATE 轉換摘要"><colgroup><col/><col/><col/></colgroup><thead><tr><th>舊資料列</th><th>新資料列</th><th>轉換方式</th></tr></thead><tbody><tr><td>不符合</td><td>不符合</td><td>不複寫</td></tr><tr><td>不符合</td><td>符合</td><td><code class="literal">INSERT</code></td></tr><tr><td>符合</td><td>不符合</td><td><code class="literal">DELETE</code></td></tr><tr><td>符合</td><td>符合</td><td><code class="literal">UPDATE</code></td></tr></tbody></table>

<br>

<a id="LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE"></a>

### 29.4.4. 分區表 [#](#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)

若發布項目包含分區表，則發布參數 [`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) 決定要使用哪一個資料列篩選器。若 `publish_via_partition_root` 為 `true`，則使用*根分區表*的資料列篩選器。否則，若 `publish_via_partition_root` 為 `false`（預設值），則使用各*分區*自己的資料列篩選器。

<a id="LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC"></a>

### 29.4.5. 初始資料同步 [#](#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)

若訂閱需要複製既有資料表的資料，且發布項目含有 `WHERE` 子句，則只有滿足資料列篩選運算式的資料才會被複製到訂閱者。

若訂閱訂閱了多個發布項目，而同一個資料表在其中以不同的 `WHERE` 子句被發布，則滿足*任一*運算式的資料列都會被複製。詳情請見 [第 29.4.6 節](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)。

### 警告

由於初始資料同步在複製既有資料表的資料時，並不會考量 [`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) 參數，因此可能會複製到一些原本不會透過 DML 複寫的資料列。請參閱 [第 29.9.1 節](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)，範例請見 [第 29.2.2 節](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)。

### 注意

若訂閱者是版本 15 之前的舊版本，即使發布項目中定義了資料列篩選器，複製既有資料時也不會使用資料列篩選器。這是因為舊版本只能複製整個資料表的資料。

<a id="LOGICAL-REPLICATION-ROW-FILTER-COMBINING"></a>

### 29.4.6. 合併多個資料列篩選 [#](#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)

若訂閱訂閱了多個發布項目，而同一個資料表在這些發布項目中（針對同一種 [`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) 操作）以不同的資料列篩選器被發布，這些運算式會以 OR 邏輯組合，因此滿足*任一*運算式的資料列都會被複寫。這代表在下列情況下，同一資料表的其他資料列篩選器都會變得多餘：

* 其中一個發布項目沒有資料列篩選器。
* 其中一個發布項目是使用 [`FOR ALL TABLES`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 建立的。此子句不允許使用資料列篩選器。
* 其中一個發布項目是使用 [`FOR TABLES IN SCHEMA`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA) 建立的，且該資料表屬於所指的綱要（schema）。此子句不允許使用資料列篩選器。

<a id="LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES"></a>

### 29.4.7. 範例 [#](#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

建立一些資料表，供以下範例使用。

```

/* pub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* pub # */ CREATE TABLE t2(d int, e int, f int, PRIMARY KEY(d));
/* pub # */ CREATE TABLE t3(g int, h int, i int, PRIMARY KEY(g));
```

建立一些發布項目。發布項目 `p1` 有一個資料表（`t1`），且該資料表有資料列篩選器。發布項目 `p2` 有兩個資料表：資料表 `t1` 沒有資料列篩選器，資料表 `t2` 有資料列篩選器。發布項目 `p3` 有兩個資料表，且兩者都有資料列篩選器。

```

/* pub # */ CREATE PUBLICATION p1 FOR TABLE t1 WHERE (a > 5 AND c = 'NSW');
/* pub # */ CREATE PUBLICATION p2 FOR TABLE t1, t2 WHERE (e = 99);
/* pub # */ CREATE PUBLICATION p3 FOR TABLE t2 WHERE (d = 10), t3 WHERE (g = 10);
```

可以使用 `psql` 顯示各發布項目的資料列篩選運算式（若有定義的話）。

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

可以使用 `psql` 顯示各資料表的資料列篩選運算式（若有定義的話）。可以看到資料表 `t1` 屬於兩個發布項目的成員，但只有在 `p1` 中才有資料列篩選器。可以看到資料表 `t2` 屬於兩個發布項目的成員，且在每個發布項目中都有不同的資料列篩選器。

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

在訂閱者節點上，建立一個與發布者上定義相同的資料表 `t1`，並建立訂閱 `s1` 來訂閱發布項目 `p1`。

```

/* sub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* sub # */ CREATE SUBSCRIPTION s1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s1'
/* sub - */ PUBLICATION p1;
```

插入一些資料列。只有滿足發布項目 `p1` 中 `t1 WHERE` 子句的資料列會被複寫。

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

更新一些資料，其中舊資料列與新資料列的值都滿足發布項目 `p1` 中的 `t1 WHERE` 子句。此 `UPDATE` 會正常複寫該項異動。

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

更新一些資料，其中舊資料列的值不滿足發布項目 `p1` 中的 `t1 WHERE` 子句，但新資料列的值滿足。此 `UPDATE` 會被轉換為 `INSERT`，並複寫該項異動。請留意訂閱者上出現的新資料列。

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

更新一些資料，其中舊資料列的值滿足發布項目 `p1` 中的 `t1 WHERE` 子句，但新資料列的值不滿足。此 `UPDATE` 會被轉換為 `DELETE`，並複寫該項異動。請留意該資料列已從訂閱者中移除。

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

以下範例說明發布參數 [`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) 在分區表的情況下，如何決定要使用父資料表還是子資料表的資料列篩選器。

在發布者上建立一個分區表。

```

/* pub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* pub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

在訂閱者上建立相同的資料表。

```

/* sub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* sub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

建立發布項目 `p4`，然後訂閱它。發布參數 `publish_via_partition_root` 設為 true。在分區表（`parent`）與分區（`child`）上都定義了資料列篩選器。

```

/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent WHERE (a < 5), child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=true);
```

```

/* sub # */ CREATE SUBSCRIPTION s4
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s4'
/* sub - */ PUBLICATION p4;
```

直接將值插入 `parent` 與 `child` 資料表。它們會使用 `parent` 的資料列篩選器來複寫（因為 `publish_via_partition_root` 為 true）。

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

重複相同的測試，但改變 `publish_via_partition_root` 的值。發布參數 `publish_via_partition_root` 設為 false。資料列篩選器定義在分區（`child`）上。

```

/* pub # */ DROP PUBLICATION p4;
/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent, child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=false);
```

```

/* sub # */ ALTER SUBSCRIPTION s4 REFRESH PUBLICATION;
```

在發布者上執行與先前相同的插入操作。它們會使用 `child` 的資料列篩選器來複寫（因為 `publish_via_partition_root` 為 false）。

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-row-filter.html)（原文版本：18.6；核對日期：2026-09-25）
