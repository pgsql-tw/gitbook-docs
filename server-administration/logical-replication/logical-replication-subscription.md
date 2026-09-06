## 29.2. Subscription [#](#LOGICAL-REPLICATION-SUBSCRIPTION)

[29.2.1. Replication Slot Management](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)

[29.2.2. Examples: Set Up Logical Replication](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)

[29.2.3. Examples: Deferred Replication Slot Creation](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

A *subscription* is the downstream side of logical
replication. The node where a subscription is defined is referred to as
the *subscriber*. A subscription defines the connection
to another database and the set of publications (one or more) to which it
wants to subscribe.

The subscriber database behaves in the same way as any other PostgreSQL
instance and can be used as a publisher for other databases by defining its
own publications.

A subscriber node may have multiple subscriptions if desired. It is
possible to define multiple subscriptions between a single
publisher-subscriber pair, in which case care must be taken to ensure
that the subscribed publication objects don't overlap.

Each subscription will receive changes via one replication slot (see
[Section 26.2.6](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)). Additional replication
slots may be required for the initial data synchronization of
pre-existing table data and those will be dropped at the end of data
synchronization.

A logical replication subscription can be a standby for synchronous
replication (see [Section 26.2.8](../high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION)). The standby
name is by default the subscription name. An alternative name can be
specified as `application_name` in the connection
information of the subscription.

Subscriptions are dumped by `pg_dump` if the current user
is a superuser. Otherwise a warning is written and subscriptions are
skipped, because non-superusers cannot read all subscription information
from the `pg_subscription` catalog.

The subscription is added using [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) and
can be stopped/resumed at any time using the
[`ALTER SUBSCRIPTION`](../../reference/sql-commands/sql-altersubscription.md) command and removed using
[`DROP SUBSCRIPTION`](../../reference/sql-commands/sql-dropsubscription.md).

When a subscription is dropped and recreated, the synchronization
information is lost. This means that the data has to be resynchronized
afterwards.

The schema definitions are not replicated, and the published tables must
exist on the subscriber. Only regular tables may be
the target of replication. For example, you can't replicate to a view.

The tables are matched between the publisher and the subscriber using the
fully qualified table name. Replication to differently-named tables on the
subscriber is not supported.

Columns of a table are also matched by name. The order of columns in the
subscriber table does not need to match that of the publisher. The data
types of the columns do not need to match, as long as the text
representation of the data can be converted to the target type. For
example, you can replicate from a column of type `integer` to a
column of type `bigint`. The target table can also have
additional columns not provided by the published table. Any such columns
will be filled with the default value as specified in the definition of the
target table. However, logical replication in binary format is more
restrictive. See the
[`binary`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY)
option of `CREATE SUBSCRIPTION` for details.

<a id="LOGICAL-REPLICATION-SUBSCRIPTION-SLOT"></a>

### 29.2.1. Replication Slot Management [#](#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)

As mentioned earlier, each (active) subscription receives changes from a
replication slot on the remote (publishing) side.

Additional table synchronization slots are normally transient, created
internally to perform initial table synchronization and dropped
automatically when they are no longer needed. These table synchronization
slots have generated names: “`pg_%u_sync_%u_%llu`”
(parameters: Subscription *`oid`*,
Table *`relid`*, system identifier *`sysid`*)

Normally, the remote replication slot is created automatically when the
subscription is created using [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) and it
is dropped automatically when the subscription is dropped using
[`DROP SUBSCRIPTION`](../../reference/sql-commands/sql-dropsubscription.md).
In some situations, however, it can
be useful or necessary to manipulate the subscription and the underlying
replication slot separately. Here are some scenarios:

* When creating a subscription, the replication slot already exists. In
  that case, the subscription can be created using
  the `create_slot = false` option to associate with the
  existing slot.
* When creating a subscription, the remote host is not reachable or in an
  unclear state. In that case, the subscription can be created using
  the `connect = false` option. The remote host will then not
  be contacted at all. This is what pg_dump
  uses. The remote replication slot will then have to be created
  manually before the subscription can be activated.
* When dropping a subscription, the replication slot should be kept.
  This could be useful when the subscriber database is being moved to a
  different host and will be activated from there. In that case,
  disassociate the slot from the subscription using
  [`ALTER SUBSCRIPTION`](../../reference/sql-commands/sql-altersubscription.md)
  before attempting to drop the subscription.
* When dropping a subscription, the remote host is not reachable. In
  that case, disassociate the slot from the subscription
  using `ALTER SUBSCRIPTION` before attempting to drop
  the subscription. If the remote database instance no longer exists, no
  further action is then necessary. If, however, the remote database
  instance is just unreachable, the replication slot (and any still
  remaining table synchronization slots) should then be
  dropped manually; otherwise it/they would continue to reserve WAL and might
  eventually cause the disk to fill up. Such cases should be carefully
  investigated.

<a id="LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES"></a>

### 29.2.2. Examples: Set Up Logical Replication [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)

Create some test tables on the publisher.

```

/* pub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* pub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* pub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

Create the same tables on the subscriber.

```

/* sub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* sub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* sub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

Insert data to the tables at the publisher side.

```

/* pub # */ INSERT INTO t1 VALUES (1, 'one'), (2, 'two'), (3, 'three');
/* pub # */ INSERT INTO t2 VALUES (1, 'A'), (2, 'B'), (3, 'C');
/* pub # */ INSERT INTO t3 VALUES (1, 'i'), (2, 'ii'), (3, 'iii');
```

Create publications for the tables. The publications `pub2`
and `pub3a` disallow some
[`publish`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
operations. The publication `pub3b` has a row filter (see
[Section 29.4](logical-replication-row-filter.md)).

```

/* pub # */ CREATE PUBLICATION pub1 FOR TABLE t1;
/* pub # */ CREATE PUBLICATION pub2 FOR TABLE t2 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3a FOR TABLE t3 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3b FOR TABLE t3 WHERE (e > 5);
```

Create subscriptions for the publications. The subscription
`sub3` subscribes to both `pub3a` and
`pub3b`. All subscriptions will copy initial data by default.

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

Observe that initial table data is copied, regardless of the
`publish` operation of the publication.

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

Furthermore, because the initial data copy ignores the `publish`
operation, and because publication `pub3a` has no row filter,
it means the copied table `t3` contains all rows even when
they do not match the row filter of publication `pub3b`.

```

/* sub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
(3 rows)
```

Insert more data to the tables at the publisher side.

```

/* pub # */ INSERT INTO t1 VALUES (4, 'four'), (5, 'five'), (6, 'six');
/* pub # */ INSERT INTO t2 VALUES (4, 'D'), (5, 'E'), (6, 'F');
/* pub # */ INSERT INTO t3 VALUES (4, 'iv'), (5, 'v'), (6, 'vi');
```

Now the publisher side data looks like:

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

Observe that during normal replication the appropriate
`publish` operations are used. This means publications
`pub2` and `pub3a` will not replicate the
`INSERT`. Also, publication `pub3b` will
only replicate data that matches the row filter of `pub3b`.
Now the subscriber side data looks like:

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

### 29.2.3. Examples: Deferred Replication Slot Creation [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

There are some cases (e.g.
[Section 29.2.1](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)) where, if the
remote replication slot was not created automatically, the user must create
it manually before the subscription can be activated. The steps to create
the slot and activate the subscription are shown in the following examples.
These examples specify the standard logical decoding output plugin
(`pgoutput`), which is what the built-in logical
replication uses.

First, create a publication for the examples to use.

```

/* pub # */ CREATE PUBLICATION pub1 FOR ALL TABLES;
```

Example 1: Where the subscription says `connect = false`

* Create the subscription.

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (connect=false);
  WARNING:  subscription was created, but is not connected
  HINT:  To initiate replication, you must manually create the replication slot, enable the subscription, and refresh the subscription.
  ```
* On the publisher, manually create a slot. Because the name was not
  specified during `CREATE SUBSCRIPTION`, the name of the
  slot to create is same as the subscription name, e.g. "sub1".

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('sub1', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   sub1      | 0/19404D0
  (1 row)
  ```
* On the subscriber, complete the activation of the subscription. After
  this the tables of `pub1` will start replicating.

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

Example 2: Where the subscription says `connect = false`,
but also specifies the
[`slot_name`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME)
option.

* Create the subscription.

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (connect=false, slot_name='myslot');
  WARNING:  subscription was created, but is not connected
  HINT:  To initiate replication, you must manually create the replication slot, enable the subscription, and refresh the subscription.
  ```
* On the publisher, manually create a slot using the same name that was
  specified during `CREATE SUBSCRIPTION`, e.g. "myslot".

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('myslot', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   myslot    | 0/19059A0
  (1 row)
  ```
* On the subscriber, the remaining subscription activation steps are the
  same as before.

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

Example 3: Where the subscription specifies `slot_name = NONE`

* Create the subscription. When `slot_name = NONE` then
  `enabled = false`, and
  `create_slot = false` are also needed.

  ```

  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (slot_name=NONE, enabled=false, create_slot=false);
  ```
* On the publisher, manually create a slot using any name, e.g. "myslot".

  ```

  /* pub # */ SELECT * FROM pg_create_logical_replication_slot('myslot', 'pgoutput');
   slot_name |    lsn
  -----------+-----------
   myslot    | 0/1905930
  (1 row)
  ```
* On the subscriber, associate the subscription with the slot name just
  created.

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 SET (slot_name='myslot');
  ```
* The remaining subscription activation steps are same as before.

  ```

  /* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
  /* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
  ```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-subscription.html)（英文原文，待翻譯）
