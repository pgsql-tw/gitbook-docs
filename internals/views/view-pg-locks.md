## 53.13. `pg_locks` [#](#VIEW-PG-LOCKS)

<a id="id-1.10.5.17.2"></a>

The view `pg_locks` provides access to
information about the locks held by active processes within the
database server. See [Chapter 13](../../the-sql-language/mvcc/README.md) for more discussion
of locking.

`pg_locks` contains one row per active lockable
object, requested lock mode, and relevant process. Thus, the same
lockable object might
appear many times, if multiple processes are holding or waiting
for locks on it. However, an object that currently has no locks on it
will not appear at all.

There are several distinct types of lockable objects:
whole relations (e.g., tables), individual pages of relations,
individual tuples of relations,
transaction IDs (both virtual and permanent IDs),
and general database objects (identified by class OID and object OID,
in the same way as in [`pg_description`](../catalogs/catalog-pg-description.md) or
[`pg_depend`](../catalogs/catalog-pg-depend.md)). Also, the right to extend a
relation is represented as a separate lockable object, as is the right to
update `pg_database`.`datfrozenxid`.
Also, “advisory” locks can be taken on numbers that have
user-defined meanings.

<a id="id-1.10.5.17.6"></a>

**Table 53.13. `pg_locks` Columns**

<table border="1" class="table" summary="pg_locks Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">locktype</code> <code class="type">text</code>
</p>
<p>
       Type of the lockable object:
       <code class="literal">relation</code>,
       <code class="literal">extend</code>,
       <code class="literal">frozenid</code>,
       <code class="literal">page</code>,
       <code class="literal">tuple</code>,
       <code class="literal">transactionid</code>,
       <code class="literal">virtualxid</code>,
       <code class="literal">spectoken</code>,
       <code class="literal">object</code>,
       <code class="literal">userlock</code>,
       <code class="literal">advisory</code>, or
       <code class="literal">applytransaction</code>.
       (See also <a class="xref" href="../../server-administration/monitoring/monitoring-stats.md#WAIT-EVENT-LOCK-TABLE">Table 27.11</a>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the database in which the lock target exists, or
       zero if the target is a shared object, or
       null if the target is a transaction ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relation</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the relation targeted by the lock, or null if the target is not
       a relation or part of a relation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">page</code> <code class="type">int4</code>
</p>
<p>
       Page number targeted by the lock within the relation,
       or null if the target is not a relation page or tuple
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuple</code> <code class="type">int2</code>
</p>
<p>
       Tuple number targeted by the lock within the page,
       or null if the target is not a tuple
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">virtualxid</code> <code class="type">text</code>
</p>
<p>
       Virtual ID of the transaction targeted by the lock,
       or null if the target is not a virtual transaction ID;  see
       <a class="xref" href="../transactions/README.md">Chapter 67</a>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">transactionid</code> <code class="type">xid</code>
</p>
<p>
       ID of the transaction targeted by the lock, or null if the target
       is not a transaction ID;  <a class="xref" href="../transactions/README.md">Chapter 67</a>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the system catalog containing the lock target, or null if the
       target is not a general database object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objid</code> <code class="type">oid</code>
       (references any OID column)
      </p>
<p>
       OID of the lock target within its system catalog, or null if the
       target is not a general database object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int2</code>
</p>
<p>
       Column number targeted by the lock (the
       <code class="structfield">classid</code> and <code class="structfield">objid</code> refer to the
       table itself),
       or zero if the target is some other general database object,
       or null if the target is not a general database object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">virtualtransaction</code> <code class="type">text</code>
</p>
<p>
       Virtual ID of the transaction that is holding or awaiting this lock
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">int4</code>
</p>
<p>
       Process ID of the server process holding or awaiting this
       lock, or null if the lock is held by a prepared transaction
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mode</code> <code class="type">text</code>
</p>
<p>
       Name of the lock mode held or desired by this process (see <a class="xref" href="../../the-sql-language/mvcc/explicit-locking.md#LOCKING-TABLES">Section 13.3.1</a> and <a class="xref" href="../../the-sql-language/mvcc/transaction-iso.md#XACT-SERIALIZABLE">Section 13.2.3</a>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">granted</code> <code class="type">bool</code>
</p>
<p>
       True if lock is held, false if lock is awaited
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fastpath</code> <code class="type">bool</code>
</p>
<p>
       True if lock was taken via fast path, false if taken via main
       lock table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">waitstart</code> <code class="type">timestamptz</code>
</p>
<p>
       Time when the server process started waiting for this lock,
       or null if the lock is held.
       Note that this can be null for a very short period of time after
       the wait started even though <code class="structfield">granted</code>
       is <code class="literal">false</code>.
      </p></td></tr></tbody></table>

<br>

`granted` is true in a row representing a lock
held by the indicated process. False indicates that this process is
currently waiting to acquire this lock, which implies that at least one
other process is holding or waiting for a conflicting lock mode on the same
lockable object. The waiting process will sleep until the other lock is
released (or a deadlock situation is detected). A single process can be
waiting to acquire at most one lock at a time.

Throughout running a transaction, a server process holds an exclusive lock
on the transaction's virtual transaction ID. If a permanent ID is assigned
to the transaction (which normally happens only if the transaction changes
the state of the database), it also holds an exclusive lock on the
transaction's permanent transaction ID until it ends. When a process finds
it necessary to wait specifically for another transaction to end, it does
so by attempting to acquire share lock on the other transaction's ID
(either virtual or permanent ID depending on the situation). That will
succeed only when the other transaction terminates and releases its locks.

Although tuples are a lockable type of object,
information about row-level locks is stored on disk, not in memory,
and therefore row-level locks normally do not appear in this view.
If a process is waiting for a
row-level lock, it will usually appear in the view as waiting for the
permanent transaction ID of the current holder of that row lock.

A speculative insertion lock consists of a transaction ID and a speculative
insertion token. The speculative insertion token is displayed in the
`objid` column.

Advisory locks can be acquired on keys consisting of either a single
`bigint` value or two integer values.
A `bigint` key is displayed with its
high-order half in the `classid` column, its low-order half
in the `objid` column, and `objsubid` equal
to 1. The original `bigint` value can be reassembled with the
expression `(classid::bigint << 32) |
objid::bigint`. Integer keys are displayed with the
first key in the
`classid` column, the second key in the `objid`
column, and `objsubid` equal to 2. The actual meaning of
the keys is up to the user. Advisory locks are local to each database,
so the `database` column is meaningful for an advisory lock.

Apply transaction locks are used in parallel mode to apply the transaction
in logical replication. The remote transaction ID is displayed in the
`transactionid` column. The `objsubid`
displays the lock subtype which is 0 for the lock used to synchronize the
set of changes, and 1 for the lock used to wait for the transaction to
finish to ensure commit order.

`pg_locks` provides a global view of all locks
in the database cluster, not only those relevant to the current database.
Although its `relation` column can be joined
against [`pg_class`](../catalogs/catalog-pg-class.md).`oid` to identify locked
relations, this will only work correctly for relations in the current
database (those for which the `database` column
is either the current database's OID or zero).

The `pid` column can be joined to the
`pid` column of the
[`pg_stat_activity`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
view to get more
information on the session holding or awaiting each lock,
for example

```

SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
    ON pl.pid = psa.pid;
```

Also, if you are using prepared transactions, the
`virtualtransaction` column can be joined to the
`transaction` column of the [`pg_prepared_xacts`](view-pg-prepared-xacts.md)
view to get more information on prepared transactions that hold locks.
(A prepared transaction can never be waiting for a lock,
but it continues to hold the locks it acquired while running.)
For example:

```

SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
    ON pl.virtualtransaction = '-1/' || ppx.transaction;
```

While it is possible to obtain information about which processes block
which other processes by joining `pg_locks` against
itself, this is very difficult to get right in detail. Such a query would
have to encode knowledge about which lock modes conflict with which
others. Worse, the `pg_locks` view does not expose
information about which processes are ahead of which others in lock wait
queues, nor information about which processes are parallel workers running
on behalf of which other client sessions. It is better to use
the `pg_blocking_pids()` function
(see [Table 9.71](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)) to identify which
process(es) a waiting process is blocked behind.

The `pg_locks` view displays data from both the
regular lock manager and the predicate lock manager, which are
separate systems; in addition, the regular lock manager subdivides its
locks into regular and *fast-path* locks.
This data is not guaranteed to be entirely consistent.
When the view is queried,
data on fast-path locks (with `fastpath` = `true`)
is gathered from each backend one at a time, without freezing the state of
the entire lock manager, so it is possible for locks to be taken or
released while information is gathered. Note, however, that these locks are
known not to conflict with any other lock currently in place. After
all backends have been queried for fast-path locks, the remainder of the
regular lock manager is locked as a unit, and a consistent snapshot of all
remaining locks is collected as an atomic action. After unlocking the
regular lock manager, the predicate lock manager is similarly locked and all
predicate locks are collected as an atomic action. Thus, with the exception
of fast-path locks, each lock manager will deliver a consistent set of
results, but as we do not lock both lock managers simultaneously, it is
possible for locks to be taken or released after we interrogate the regular
lock manager and before we interrogate the predicate lock manager.

Locking the regular and/or predicate lock manager could have some
impact on database performance if this view is very frequently accessed.
The locks are held only for the minimum amount of time necessary to
obtain data from the lock managers, but this does not completely eliminate
the possibility of a performance impact.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-locks.html)（英文原文，待翻譯）
