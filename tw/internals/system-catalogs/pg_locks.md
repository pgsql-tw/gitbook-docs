# 51.73. pg\_locks

The view `pg_locks` provides access to information about the locks held by active processes within the database server. See [Chapter 13](https://www.postgresql.org/docs/13/mvcc.html) for more discussion of locking.

`pg_locks` contains one row per active lockable object, requested lock mode, and relevant process. Thus, the same lockable object might appear many times, if multiple processes are holding or waiting for locks on it. However, an object that currently has no locks on it will not appear at all.

There are several distinct types of lockable objects: whole relations \(e.g., tables\), individual pages of relations, individual tuples of relations, transaction IDs \(both virtual and permanent IDs\), and general database objects \(identified by class OID and object OID, in the same way as in `pg_description` or `pg_depend`\). Also, the right to extend a relation is represented as a separate lockable object, as is the right to update `pg_database`.`datfrozenxid`. Also, “advisory” locks can be taken on numbers that have user-defined meanings.

#### **Table 51.74. `pg_locks` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>locktype</code>  <code>text</code>
        </p>
        <p>Type of the lockable object: <code>relation</code>, <code>extend</code>, <code>frozenid</code>, <code>page</code>, <code>tuple</code>, <code>transactionid</code>, <code>virtualxid</code>, <code>spectoken</code>, <code>object</code>, <code>userlock</code>,
          or <code>advisory</code>. (See also <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-LOCK-TABLE">Table 27.11</a>.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>database</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-database.html"><code>pg_database</code></a>.<code>oid</code>)</p>
        <p>OID of the database in which the lock target exists, or zero if the target
          is a shared object, or null if the target is a transaction ID</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relation</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>OID of the relation targeted by the lock, or null if the target is not
          a relation or part of a relation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>page</code>  <code>int4</code>
        </p>
        <p>Page number targeted by the lock within the relation, or null if the target
          is not a relation page or tuple</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tuple</code>  <code>int2</code>
        </p>
        <p>Tuple number targeted by the lock within the page, or null if the target
          is not a tuple</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>virtualxid</code>  <code>text</code>
        </p>
        <p>Virtual ID of the transaction targeted by the lock, or null if the target
          is not a virtual transaction ID</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>transactionid</code>  <code>xid</code>
        </p>
        <p>ID of the transaction targeted by the lock, or null if the target is not
          a transaction ID</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>classid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>OID of the system catalog containing the lock target, or null if the target
          is not a general database object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>objid</code>  <code>oid</code> (references any OID column)</p>
        <p>OID of the lock target within its system catalog, or null if the target
          is not a general database object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>objsubid</code>  <code>int2</code>
        </p>
        <p>Column number targeted by the lock (the <code>classid</code> and <code>objid</code> refer
          to the table itself), or zero if the target is some other general database
          object, or null if the target is not a general database object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>virtualtransaction</code>  <code>text</code>
        </p>
        <p>Virtual ID of the transaction that is holding or awaiting this lock</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>int4</code>
        </p>
        <p>Process ID of the server process holding or awaiting this lock, or null
          if the lock is held by a prepared transaction</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>mode</code>  <code>text</code>
        </p>
        <p>Name of the lock mode held or desired by this process (see <a href="https://www.postgresql.org/docs/13/explicit-locking.html#LOCKING-TABLES">Section 13.3.1</a> and
          <a
          href="https://www.postgresql.org/docs/13/transaction-iso.html#XACT-SERIALIZABLE">Section 13.2.3</a>)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>granted</code>  <code>bool</code>
        </p>
        <p>True if lock is held, false if lock is awaited</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>fastpath</code>  <code>bool</code>
        </p>
        <p>True if lock was taken via fast path, false if taken via main lock table</p>
      </td>
    </tr>
  </tbody>
</table>

`granted` is true in a row representing a lock held by the indicated process. False indicates that this process is currently waiting to acquire this lock, which implies that at least one other process is holding or waiting for a conflicting lock mode on the same lockable object. The waiting process will sleep until the other lock is released \(or a deadlock situation is detected\). A single process can be waiting to acquire at most one lock at a time.

Throughout running a transaction, a server process holds an exclusive lock on the transaction's virtual transaction ID. If a permanent ID is assigned to the transaction \(which normally happens only if the transaction changes the state of the database\), it also holds an exclusive lock on the transaction's permanent transaction ID until it ends. When a process finds it necessary to wait specifically for another transaction to end, it does so by attempting to acquire share lock on the other transaction's ID \(either virtual or permanent ID depending on the situation\). That will succeed only when the other transaction terminates and releases its locks.

Although tuples are a lockable type of object, information about row-level locks is stored on disk, not in memory, and therefore row-level locks normally do not appear in this view. If a process is waiting for a row-level lock, it will usually appear in the view as waiting for the permanent transaction ID of the current holder of that row lock.

Advisory locks can be acquired on keys consisting of either a single `bigint` value or two integer values. A `bigint` key is displayed with its high-order half in the `classid` column, its low-order half in the `objid` column, and `objsubid` equal to 1. The original `bigint` value can be reassembled with the expression `(classid::bigint << 32) | objid::bigint`. Integer keys are displayed with the first key in the `classid` column, the second key in the `objid` column, and `objsubid` equal to 2. The actual meaning of the keys is up to the user. Advisory locks are local to each database, so the `database` column is meaningful for an advisory lock.

`pg_locks` provides a global view of all locks in the database cluster, not only those relevant to the current database. Although its `relation` column can be joined against `pg_class`.`oid` to identify locked relations, this will only work correctly for relations in the current database \(those for which the `database` column is either the current database's OID or zero\).

The `pid` column can be joined to the `pid` column of the [`pg_stat_activity`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW) view to get more information on the session holding or awaiting each lock, for example

```text
SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
    ON pl.pid = psa.pid;
```

Also, if you are using prepared transactions, the `virtualtransaction` column can be joined to the `transaction` column of the [`pg_prepared_xacts`](https://www.postgresql.org/docs/13/view-pg-prepared-xacts.html) view to get more information on prepared transactions that hold locks. \(A prepared transaction can never be waiting for a lock, but it continues to hold the locks it acquired while running.\) For example:

```text
SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
    ON pl.virtualtransaction = '-1/' || ppx.transaction;
```

While it is possible to obtain information about which processes block which other processes by joining `pg_locks` against itself, this is very difficult to get right in detail. Such a query would have to encode knowledge about which lock modes conflict with which others. Worse, the `pg_locks` view does not expose information about which processes are ahead of which others in lock wait queues, nor information about which processes are parallel workers running on behalf of which other client sessions. It is better to use the `pg_blocking_pids()` function \(see [Table 9.63](https://www.postgresql.org/docs/13/functions-info.html#FUNCTIONS-INFO-SESSION-TABLE)\) to identify which process\(es\) a waiting process is blocked behind.

The `pg_locks` view displays data from both the regular lock manager and the predicate lock manager, which are separate systems; in addition, the regular lock manager subdivides its locks into regular and _fast-path_ locks. This data is not guaranteed to be entirely consistent. When the view is queried, data on fast-path locks \(with `fastpath` = `true`\) is gathered from each backend one at a time, without freezing the state of the entire lock manager, so it is possible for locks to be taken or released while information is gathered. Note, however, that these locks are known not to conflict with any other lock currently in place. After all backends have been queried for fast-path locks, the remainder of the regular lock manager is locked as a unit, and a consistent snapshot of all remaining locks is collected as an atomic action. After unlocking the regular lock manager, the predicate lock manager is similarly locked and all predicate locks are collected as an atomic action. Thus, with the exception of fast-path locks, each lock manager will deliver a consistent set of results, but as we do not lock both lock managers simultaneously, it is possible for locks to be taken or released after we interrogate the regular lock manager and before we interrogate the predicate lock manager.

Locking the regular and/or predicate lock manager could have some impact on database performance if this view is very frequently accessed. The locks are held only for the minimum amount of time necessary to obtain data from the lock managers, but this does not completely eliminate the possibility of a performance impact.  


