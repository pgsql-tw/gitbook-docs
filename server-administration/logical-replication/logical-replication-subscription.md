<a id="LOGICAL-REPLICATION-SUBSCRIPTION"></a>

## 29.2. 訂閱（Subscription） [#](#LOGICAL-REPLICATION-SUBSCRIPTION)

[29.2.1. 複寫插槽管理](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)

[29.2.2. 範例：設定邏輯複寫](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)

[29.2.3. 範例：延後建立複寫插槽](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

*訂閱（subscription）* 是邏輯
複寫的下游端。定義訂閱的節點稱為
*訂閱者（subscriber）*。一個訂閱定義了到
另一個資料庫的連線，以及它想要訂閱的一個或多個
發布（publication）集合。

訂閱者資料庫的行為與其他任何 PostgreSQL
執行個體相同，也可以透過定義自己的發布，
做為其他資料庫的發布者使用。

若有需要，一個訂閱者節點可以有多個訂閱。也
可以在同一組發布者—訂閱者之間定義多個訂閱，
但此時必須注意確保所訂閱的發布物件不會
重疊。

每個訂閱會透過一個複寫插槽接收變更（見
[第 26.2.6 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)）。對於既有資料表資料的初始資料
同步，可能還需要額外的複寫
插槽，這些插槽會在資料同步結束時被移除。

邏輯複寫訂閱可以做為同步複寫的待命端
（見 [第 26.2.8 節](../high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION)）。待命端
名稱預設為訂閱名稱。也可以在訂閱連線
資訊中以 `application_name` 指定其他
名稱。

若目前使用者是超級使用者，`pg_dump` 會傾印
訂閱。否則會寫出一則警告，並略過訂閱，因為
非超級使用者無法從 `pg_subscription` 系統目錄
讀取所有訂閱資訊。

訂閱是使用 [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) 新增，
可以隨時使用
[`ALTER SUBSCRIPTION`](../../reference/sql-commands/sql-altersubscription.md) 指令停止／繼續，
並使用 [`DROP SUBSCRIPTION`](../../reference/sql-commands/sql-dropsubscription.md) 移除。

當訂閱被移除並重新建立時，同步
資訊會遺失。這表示之後必須重新同步資料。

結構定義不會被複寫，被發布的資料表必須已
存在於訂閱者端。只有一般資料表可以做
為複寫的目標。舉例來說，你無法複寫到檢視表。

發布者與訂閱者之間的資料表比對，是以
完整限定的資料表名稱進行。不支援複寫到訂閱者端
名稱不同的資料表。

資料表的欄位也是以名稱比對。訂閱者端資料表中
欄位的順序不需要與發布者端相符。欄位的
資料型別也不需要相符，只要資料的文字
表示法可以轉換為目標型別即可。舉例來說，你可以從
`integer` 型別的欄位複寫到
`bigint` 型別的欄位。目標資料表也可以有
發布資料表未提供的額外欄位。任何這類
欄位都會依目標資料表定義中指定的預設值填入。
不過，以二進位格式進行的邏輯複寫限制較多。詳情請見
`CREATE SUBSCRIPTION` 的
[`binary`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY)
選項。

<a id="LOGICAL-REPLICATION-SUBSCRIPTION-SLOT"></a>

### 29.2.1. 複寫插槽管理 [#](#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)

如前所述，每個（作用中的）訂閱都會從遠端
（發布端）的複寫插槽接收變更。

額外的資料表同步插槽通常是暫時性的，是為了執行
初始資料表同步而在內部建立，一旦不再需要就會
自動移除。這些資料表同步插槽的名稱是自動產生的：
「`pg_%u_sync_%u_%llu`」
（參數依序為：訂閱的 *`oid`*、
資料表的 *`relid`*、系統識別碼 *`sysid`*）

一般來說，遠端複寫插槽會在使用
[`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) 建立訂閱時自動建立，
並在使用
[`DROP SUBSCRIPTION`](../../reference/sql-commands/sql-dropsubscription.md) 移除訂閱時自動
移除。不過，在某些情況下，個別操作
訂閱及其底層複寫插槽會很有用，甚至有其必要。
以下是幾種情境：

* 建立訂閱時，複寫插槽已經存在。在
  這種情況下，可以使用
  `create_slot = false` 選項來建立訂閱，
  以便與既有插槽建立關聯。
* 建立訂閱時，無法連上遠端主機，或其狀態不
  明確。在這種情況下，可以使用
  `connect = false` 選項來建立訂閱。此時完全
  不會聯絡遠端主機。這正是 pg_dump
  所使用的方式。此後必須手動建立遠端複寫
  插槽，訂閱才能被啟用。
* 移除訂閱時，應保留複寫插槽。當
  訂閱者資料庫要搬移到另一台主機、並打算在該處
  啟用時，這會很有用。在這種情況下，請先使用
  [`ALTER SUBSCRIPTION`](../../reference/sql-commands/sql-altersubscription.md)
  將插槽與訂閱解除關聯，再嘗試移除訂閱。
* 移除訂閱時，無法連上遠端主機。在
  這種情況下，請先使用 `ALTER SUBSCRIPTION`
  將插槽與訂閱解除關聯，再嘗試移除
  訂閱。若遠端資料庫執行個體已不復存在，則
  之後不需要進一步動作。但若遠端資料庫
  執行個體只是無法連線，就應該手動移除該
  複寫插槽（以及任何仍殘留的資料表同步插槽）；
  否則它們會持續保留 WAL，最終可能導致
  磁碟空間耗盡。此類情況應仔細
  調查。

<a id="LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES"></a>

### 29.2.2. 範例：設定邏輯複寫 [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)

在發布者端建立一些測試資料表。

```

/* pub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* pub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* pub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

在訂閱者端建立相同的資料表。

```

/* sub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* sub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* sub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

在發布者端為資料表插入資料。

```

/* pub # */ INSERT INTO t1 VALUES (1, 'one'), (2, 'two'), (3, 'three');
/* pub # */ INSERT INTO t2 VALUES (1, 'A'), (2, 'B'), (3, 'C');
/* pub # */ INSERT INTO t3 VALUES (1, 'i'), (2, 'ii'), (3, 'iii');
```

為這些資料表建立發布。發布 `pub2`
與 `pub3a` 停用了部分
[`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
操作。發布 `pub3b` 則有一個資料列篩選條件（見
[第 29.4 節](logical-replication-row-filter.md)）。

```

/* pub # */ CREATE PUBLICATION pub1 FOR TABLE t1;
/* pub # */ CREATE PUBLICATION pub2 FOR TABLE t2 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3a FOR TABLE t3 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3b FOR TABLE t3 WHERE (e > 5);
```

為這些發布建立訂閱。訂閱
`sub3` 同時訂閱 `pub3a` 與
`pub3b`。所有訂閱預設都會複製初始資料。

```

/* sub # */ CREATE SUBSCRIPTION sub1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub1'
/* sub - */ PUBLICATION pub1;
/* sub # */ CREATE SUBSCRIPTION sub2
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub2'
/* sub - */ PUBLICATION pub2;
/* sub # */ CREATE SUBSCRIPTION sub3
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub3'
/* sub - */ PUBLICATION pub3a, pub3b;
```

請注意，無論發布的 `publish` 操作為何，
初始資料表資料都會被複製。

```

/* sub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
(3 rows)

/* sub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)
```

此外，由於初始資料複製會忽略
`publish` 操作，而且發布 `pub3a`
沒有資料列篩選條件，這表示即使資料列不符合
發布 `pub3b` 的篩選條件，複製過去的資料表
`t3` 仍然會包含全部資料列。

```

/* sub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
(3 rows)
```

在發布者端為資料表插入更多資料。

```

/* pub # */ INSERT INTO t1 VALUES (4, 'four'), (5, 'five'), (6, 'six');
/* pub # */ INSERT INTO t2 VALUES (4, 'D'), (5, 'E'), (6, 'F');
/* pub # */ INSERT INTO t3 VALUES (4, 'iv'), (5, 'v'), (6, 'vi');
```

此時發布者端的資料如下：

```

/* pub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

/* pub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
 4 | D
 5 | E
 6 | F
(6 rows)

/* pub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
 4 | iv
 5 | v
 6 | vi
(6 rows)
```

請注意，在正常複寫過程中，會套用對應的
`publish` 操作。這表示發布
`pub2` 與 `pub3a` 不會複寫該
`INSERT`。此外，發布 `pub3b`
只會複寫符合 `pub3b` 篩選條件的資料。
此時訂閱者端的資料如下：

```

/* sub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

/* sub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)

/* sub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
 6 | vi
(4 rows)
```

<a id="LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT"></a>

### 29.2.3. 範例：延後建立複寫插槽 [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

在某些情況下（例如
[第 29.2.1 節](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)），若遠端
複寫插槽未被自動建立，使用者必須在訂閱能被
啟用之前手動建立該插槽。下列範例示範了建立
插槽並啟用訂閱的步驟。這些範例指定了標準的邏輯
解碼輸出外掛程式（`pgoutput`），
這也是內建邏輯複寫所使用的外掛程式。

首先，為這些範例建立一個發布以供使用。

```

/* pub # */ CREATE PUBLICATION pub1 FOR ALL TABLES;
```

範例 1：訂閱指定 `connect = false` 的情況

* 建立訂閱。

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (connect=false);
  WARNING:  subscription was created, but is not connected
  HINT:  To initiate replication, you must manually create the replication slot, enable the subscription, and refresh the subscription.
  ```
* 在發布者端手動建立插槽。由於在
  `CREATE SUBSCRIPTION` 時未指定名稱，要建立的
  插槽名稱會與訂閱名稱相同，例如 "sub1"。

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('sub1', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   sub1      | 0/19404D0
  (1 row)
  ```
* 在訂閱者端完成訂閱的啟用。完成之後，
  `pub1` 的資料表就會開始複寫。

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

範例 2：訂閱指定 `connect = false`，
但同時也指定了
[`slot_name`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME)
選項的情況。

* 建立訂閱。

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (connect=false, slot_name='myslot');
  WARNING:  subscription was created, but is not connected
  HINT:  To initiate replication, you must manually create the replication slot, enable the subscription, and refresh the subscription.
  ```
* 在發布者端手動建立插槽，並使用與
  `CREATE SUBSCRIPTION` 時所指定相同的名稱，例如 "myslot"。

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('myslot', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   myslot    | 0/19059A0
  (1 row)
  ```
* 在訂閱者端，剩餘的訂閱啟用步驟與之前相同。

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

範例 3：訂閱指定 `slot_name = NONE` 的情況

* 建立訂閱。當 `slot_name = NONE` 時，
  也需要一併指定 `enabled = false` 及
  `create_slot = false`。

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (slot_name=NONE, enabled=false, create_slot=false);
  ```
* 在發布者端使用任意名稱手動建立插槽，例如 "myslot"。

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('myslot', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   myslot    | 0/1905930
  (1 row)
  ```
* 在訂閱者端，將訂閱與剛才建立的插槽名稱
  建立關聯。

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 SET (slot_name='myslot');
  ```
* 剩餘的訂閱啟用步驟與之前相同。

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-subscription.html)（原文版本：18.6；核對日期：2026-09-26）
