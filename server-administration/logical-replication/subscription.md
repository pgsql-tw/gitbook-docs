# 31.2. 訂閱（Subscription）

訂閱是邏輯複寫的下游。訂閱的節點被稱為訂閱者。訂閱定義了與另一個資料庫以及它想要訂閱的一組或多組發佈（一個或多個）的連線。

訂閱資料庫的行為與任何其他 PostgreSQL 服務的行為相同，也可以透過定義自己的發佈來成為其他資料庫的發佈者。

如果需要，用戶節點可能有多個訂閱。在單個（發佈者 - 訂閱者）配對之間定義多個訂閱允許的，在這種情況下必須小心以確保訂閱的發佈對象不重疊。

每個訂閱都將透過一個複寫插槽（replication slot）接收變更（請參閱[第 27.2.6 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-6-replication-slots)）。額外的臨時複寫插槽可能需要用於預先存在的資料表資料才能開始初始化資料同步。

邏輯複寫訂閱可以是同步複寫的備用資料庫（請參閱[第 27.2.8 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-8-synchronous-replication)）。備用名稱預設為訂閱名稱。可以在訂閱的連線訊息中將另一個名稱以 application\_name 指定。

如果目前使用者是超級使用者，則 pg\_dump 會匯出訂閱的內容。否則會提示警告訊息並跳過訂閱內容，因為非超級使用者無法讀取 pg\_subscription 目錄中的訂閱訊息。

訂閱是使用 [CREATE SUBSCRIPTION](../../reference/sql-commands/create-subscription.md) 加入的，可以隨時使用 [ALTER SUBSCRIPTION](../../reference/sql-commands/alter-subscription.md) 指令停止或恢復，並使用 [DROP SUBSCRIPTION](../../reference/sql-commands/drop-subscription.md) 移除訂閱。

當訂閱被移除並重新建立時，將會失去同步訊息。這意味著資料必須在事後重新同步。

資料庫結構的定義不會被複寫，並且已發佈的資料表必須存在於訂閱的伺服器上。只有一般的資料表可以是複寫的標的。例如，您不能複寫到檢視表（view）。

這些資料表使用完全限定的資料表名稱，在發佈者和訂閱者之間進行匹配。不支援複寫到訂閱戶上不同名稱的資料表。

資料表的欄位也按照名稱對應，目標資料表中具有不同的欄位順序是允許的。欄位型別不需要完全相同，只要資料可以被轉換為目標類型即可。例如，你可以將型別為 integer 的欄位複寫至型別為 bigint 的欄位之中。目標資料表可以具有未由發佈資料表所提供的附加欄位。那些欄位將以它們的預設值填入。

## 31.2.1. 複寫插槽管理

如前所述，每個執行中的訂閱都會從遠端（發佈）端的複寫插槽接收變更。

Additional table synchronization slots are normally transient, created internally to perform initial table synchronization and dropped automatically when they are no longer needed. These table synchronization slots have generated names: “`pg_%u_sync_%u_%llu`” (parameters: Subscription _`oid`_, Table _`relid`_, system identifier _`sysid`_)

通常，使用 CREATE SUBSCRIPTION 建立訂閱時會自動建立遠端的複寫插槽，使用 DROP SUBSCRIPTION 移除訂閱時會自動移除該插槽。但是，在某些情況下，分別管理訂閱和底層複寫插槽可能很有用甚至是必要的。 以下是一些情況：

* 建立訂閱時，複寫插槽已經存在。在這種情況下，可以使用 create\_slot = false 選項來與現有插槽關連以建立訂閱。
* 建立訂閱時，遠端主機無法存取或處於不明狀態。在這種情況下，可以使用 connect = false 選項建立訂閱。遠端主機將不會被聯繫。這是 pg\_dump 所使用的。然後必須在訂閱啓動之前手動建立遠端的複寫插槽。
* 在移除訂閱時，應該保留複寫插槽。當使用者資料庫被移動到不同的主機並且從那裡被啓動時，這可能會有用。在這種情況下，在嘗試移除訂閱之前，請使用 ALTER SUBSCRIPTION 從插入位置解除關連。
* 在移除訂閱時，遠端主機無法存取。在這種情況下，在嘗試移除訂閱之前，請使用 ALTER SUBSCRIPTION 從插入位置解除關連。如果遠端資料庫服務不再存在，則不需要進一步的操作。但是，如果遠端資料庫服務不可存取，則應手動移除複寫插槽；否則它會繼續保留 WAL，最終可能會導致磁碟空間不足。應該仔細檢查這種情況。

## 31.2.2. Examples

Create some test tables on the publisher.

```
test_pub=# CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
CREATE TABLE
test_pub=# CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
CREATE TABLE
test_pub=# CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
CREATE TABLE
```

Create the same tables on the subscriber.

```
test_sub=# CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
CREATE TABLE
test_sub=# CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
CREATE TABLE
test_sub=# CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
CREATE TABLE
```

Insert data to the tables at the publisher side.

```
test_pub=# INSERT INTO t1 VALUES (1, 'one'), (2, 'two'), (3, 'three');
INSERT 0 3
test_pub=# INSERT INTO t2 VALUES (1, 'A'), (2, 'B'), (3, 'C');
INSERT 0 3
test_pub=# INSERT INTO t3 VALUES (1, 'i'), (2, 'ii'), (3, 'iii');
INSERT 0 3
```

Create publications for the tables. The publications `pub2` and `pub3a` disallow some `publish` operations. The publication `pub3b` has a row filter (see [Section 31.3](https://www.postgresql.org/docs/current/logical-replication-row-filter.html)).

```
test_pub=# CREATE PUBLICATION pub1 FOR TABLE t1;
CREATE PUBLICATION
test_pub=# CREATE PUBLICATION pub2 FOR TABLE t2 WITH (publish = 'truncate');
CREATE PUBLICATION
test_pub=# CREATE PUBLICATION pub3a FOR TABLE t3 WITH (publish = 'truncate');
CREATE PUBLICATION
test_pub=# CREATE PUBLICATION pub3b FOR TABLE t3 WHERE (e > 5);
CREATE PUBLICATION
```

Create subscriptions for the publications. The subscription `sub3` subscribes to both `pub3a` and `pub3b`. All subscriptions will copy initial data by default.

```
test_sub=# CREATE SUBSCRIPTION sub1
test_sub-# CONNECTION 'host=localhost dbname=test_pub application_name=sub1'
test_sub-# PUBLICATION pub1;
CREATE SUBSCRIPTION
test_sub=# CREATE SUBSCRIPTION sub2
test_sub-# CONNECTION 'host=localhost dbname=test_pub application_name=sub2'
test_sub-# PUBLICATION pub2;
CREATE SUBSCRIPTION
test_sub=# CREATE SUBSCRIPTION sub3
test_sub-# CONNECTION 'host=localhost dbname=test_pub application_name=sub3'
test_sub-# PUBLICATION pub3a, pub3b;
CREATE SUBSCRIPTION
```

Observe that initial table data is copied, regardless of the `publish` operation of the publication.

```
test_sub=# SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
(3 rows)

test_sub=# SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)
```

Furthermore, because the initial data copy ignores the `publish` operation, and because publication `pub3a` has no row filter, it means the copied table `t3` contains all rows even when they do not match the row filter of publication `pub3b`.

```
test_sub=# SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
(3 rows)
```

Insert more data to the tables at the publisher side.

```
test_pub=# INSERT INTO t1 VALUES (4, 'four'), (5, 'five'), (6, 'six');
INSERT 0 3
test_pub=# INSERT INTO t2 VALUES (4, 'D'), (5, 'E'), (6, 'F');
INSERT 0 3
test_pub=# INSERT INTO t3 VALUES (4, 'iv'), (5, 'v'), (6, 'vi');
INSERT 0 3
```

Now the publisher side data looks like:

```
test_pub=# SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

test_pub=# SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
 4 | D
 5 | E
 6 | F
(6 rows)

test_pub=# SELECT * FROM t3;
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

Observe that during normal replication the appropriate `publish` operations are used. This means publications `pub2` and `pub3a` will not replicate the `INSERT`. Also, publication `pub3b` will only replicate data that matches the row filter of `pub3b`. Now the subscriber side data looks like:

```
test_sub=# SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

test_sub=# SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)

test_sub=# SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
 6 | vi
(4 rows)
```
