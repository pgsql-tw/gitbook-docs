<a id="LOGICAL-REPLICATION-COL-LISTS"></a>

## 29.5. 欄位清單 [#](#logical-replication-col-lists) <a href="#logical-replication-col-lists" id="logical-replication-col-lists"></a>

[29.5.1. 範例](logical-replication-col-lists.md#logical-replication-col-list-examples)

每個發佈都可以選擇性地指定每個資料表的哪些欄位要
複寫到訂閱者。訂閱者端的資料表至少必須
具有所有已發佈的欄位。如果未指定欄位清單，
則會複寫發佈者上的所有欄位。
語法的詳細資訊請參閱 [CREATE PUBLICATION](../../reference/sql-commands/sql-createpublication.md)。

欄位的選擇可以基於行為或效能上的理由。
不過，不要依賴這項功能來確保安全性：惡意的訂閱者
能夠取得未特別發佈之欄位中的資料。
如果有安全性方面的考量，可以在發佈者端
施加保護措施。

如果未指定欄位清單，之後加入資料表的任何欄位都會
自動被複寫。這表示具有列出所有欄位的欄位清單，
與完全沒有欄位清單並不相同。

欄位清單只能包含單純的欄位參照。清單中欄位的
順序不會被保留。

產生欄位也可以在欄位清單中指定。這使得
產生欄位可以被發佈，不論發佈參數
[`publish_generated_columns`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) 的設定為何。詳細資訊請參閱
[第 29.6 節](logical-replication-gencols.md)。

當發佈同時也發佈
[`FOR TABLES IN SCHEMA`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)
時，不支援指定欄位清單。

對於分割資料表，由發佈參數
[`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT)
決定使用哪一個欄位清單。如果 `publish_via_partition_root`
為 `true`，則使用根分割資料表的欄位清單。
否則，如果 `publish_via_partition_root` 為
`false`（預設值），則使用每個分割區各自的欄位清單。

如果發佈會發佈 `UPDATE` 或
`DELETE` 操作，則任何欄位清單都必須包含該
資料表的複寫識別欄位（請參閱
[`REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)）。
如果發佈只發佈 `INSERT` 操作，則
欄位清單可以省略複寫識別欄位。

欄位清單對 `TRUNCATE` 命令沒有作用。

在初始資料同步期間，只會複製已發佈的欄位。
不過，如果訂閱者是 15 之前的版本，則
在初始資料同步期間會複製資料表中的所有欄位，
並忽略任何欄位清單。如果訂閱者是 18 之前的版本，
則即使發佈者中定義了產生欄位，初始資料表同步也不會複製
這些產生欄位。

<a id="LOGICAL-REPLICATION-COL-LIST-COMBINING"></a>

### 警告：合併來自多個發佈的欄位清單

目前不支援由多個發佈組成、且同一個資料表
在這些發佈中以不同欄位清單發佈的訂閱。
[CREATE SUBSCRIPTION](../../reference/sql-commands/sql-createsubscription.md) 不允許
建立這樣的訂閱，但在訂閱建立之後，
仍然可能因為在發佈端加入或修改欄位清單
而陷入這種情況。

這表示變更已被訂閱之發佈中資料表的欄位清單，
可能導致訂閱者端擲出
錯誤。

如果訂閱受到此問題影響，恢復
複寫的唯一方法是調整發佈端的其中一個欄位清單，
使它們全部一致；然後重新建立訂閱，
或使用 [`ALTER SUBSCRIPTION ... DROP PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION)
移除其中一個造成問題的發佈，再將它重新加入。

<a id="LOGICAL-REPLICATION-COL-LIST-EXAMPLES"></a>

### 29.5.1. 範例 [#](#logical-replication-col-list-examples) <a href="#logical-replication-col-list-examples" id="logical-replication-col-list-examples"></a>

建立下列範例中要使用的資料表 `t1`。

```

/* pub # */ CREATE TABLE t1(id int, a text, b text, c text, d text, e text, PRIMARY KEY(id));
```

建立發佈 `p1`。為資料表 `t1` 定義欄位清單，
以減少將被複寫的欄位數量。請注意，欄位清單中
欄位名稱的順序並不重要。

```

/* pub # */ CREATE PUBLICATION p1 FOR TABLE t1 (id, b, a, d);
```

可以使用 `psql` 顯示每個發佈的欄位清單（如果有定義的話）。

```

/* pub # */ \dRp+
                                         Publication p1
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1" (id, a, b, d)
```

可以使用 `psql` 顯示每個資料表的欄位清單（如果有定義的話）。

```

/* pub # */ \d t1
                 Table "public.t1"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 id     | integer |           | not null |
 a      | text    |           |          |
 b      | text    |           |          |
 c      | text    |           |          |
 d      | text    |           |          |
 e      | text    |           |          |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (id)
Publications:
    "p1" (id, a, b, d)
```

在訂閱者節點上建立資料表 `t1`，現在它
只需要發佈者資料表 `t1` 中欄位的一個子集，
同時建立訂閱
`s1`，訂閱發佈
`p1`。

```

/* sub # */ CREATE TABLE t1(id int, b text, a text, d text, PRIMARY KEY(id));
/* sub # */ CREATE SUBSCRIPTION s1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s1'
/* sub - */ PUBLICATION p1;
```

在發佈者節點上，將一些資料列插入資料表 `t1`。

```

/* pub # */ INSERT INTO t1 VALUES(1, 'a-1', 'b-1', 'c-1', 'd-1', 'e-1');
/* pub # */ INSERT INTO t1 VALUES(2, 'a-2', 'b-2', 'c-2', 'd-2', 'e-2');
/* pub # */ INSERT INTO t1 VALUES(3, 'a-3', 'b-3', 'c-3', 'd-3', 'e-3');
/* pub # */ SELECT * FROM t1 ORDER BY id;
 id |  a  |  b  |  c  |  d  |  e
----+-----+-----+-----+-----+-----
  1 | a-1 | b-1 | c-1 | d-1 | e-1
  2 | a-2 | b-2 | c-2 | d-2 | e-2
  3 | a-3 | b-3 | c-3 | d-3 | e-3
(3 rows)
```

只有發佈 `p1` 欄位清單中的資料會被
複寫。

```

/* sub # */ SELECT * FROM t1 ORDER BY id;
 id |  b  |  a  |  d
----+-----+-----+-----
  1 | b-1 | a-1 | d-1
  2 | b-2 | a-2 | d-2
  3 | b-3 | a-3 | d-3
(3 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-col-lists.html)（原文版本：18.6；核對日期：2026-10-10）
