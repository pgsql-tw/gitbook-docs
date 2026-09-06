## F.31. pgrowlocks — show a table's row locking information [#](#PGROWLOCKS)

[F.31.1. Overview](pgrowlocks.md#PGROWLOCKS-OVERVIEW)

[F.31.2. Sample Output](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)

[F.31.3. Author](pgrowlocks.md#PGROWLOCKS-AUTHOR)

<a id="id-1.11.7.41.2"></a>

The `pgrowlocks` module provides a function to show row
locking information for a specified table.

By default use is restricted to superusers, roles with privileges of the
`pg_stat_scan_tables` role, and users with
`SELECT` permissions on the table.

<a id="PGROWLOCKS-OVERVIEW"></a>

### F.31.1. Overview [#](#PGROWLOCKS-OVERVIEW)

<a id="id-1.11.7.41.5.2"></a>

```

pgrowlocks(text) returns setof record
```

The parameter is the name of a table. The result is a set of records,
with one row for each locked row within the table. The output columns
are shown in [Table F.21](pgrowlocks.md#PGROWLOCKS-COLUMNS).

<a id="PGROWLOCKS-COLUMNS"></a>

**Table F.21. `pgrowlocks` Output Columns**

<table border="1" class="table" summary="pgrowlocks Output Columns"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">locked_row</code></td><td><code class="type">tid</code></td><td>Tuple ID (TID) of locked row</td></tr><tr><td><code class="structfield">locker</code></td><td><code class="type">xid</code></td><td>Transaction ID of locker, or multixact ID if
      multitransaction;  see <a class="xref" href="../../internals/transactions/transaction-id.md">Section 67.1</a></td></tr><tr><td><code class="structfield">multi</code></td><td><code class="type">boolean</code></td><td>True if locker is a multitransaction</td></tr><tr><td><code class="structfield">xids</code></td><td><code class="type">xid[]</code></td><td>Transaction IDs of lockers (more than one if multitransaction)</td></tr><tr><td><code class="structfield">modes</code></td><td><code class="type">text[]</code></td><td>Lock mode of lockers (more than one if multitransaction),
       an array of <code class="literal">For Key Share</code>, <code class="literal">For Share</code>,
       <code class="literal">For No Key Update</code>, <code class="literal">No Key Update</code>,
       <code class="literal">For Update</code>, <code class="literal">Update</code>.</td></tr><tr><td><code class="structfield">pids</code></td><td><code class="type">integer[]</code></td><td>Process IDs of locking backends (more than one if multitransaction)</td></tr></tbody></table>

<br>

`pgrowlocks` takes `AccessShareLock` for the
target table and reads each row one by one to collect the row locking
information. This is not very speedy for a large table. Note that:

1. If an `ACCESS EXCLUSIVE` lock is taken on the table,
   `pgrowlocks` will be blocked.
2. `pgrowlocks` is not guaranteed to produce a
   self-consistent snapshot. It is possible that a new row lock is taken,
   or an old lock is freed, during its execution.

`pgrowlocks` does not show the contents of locked
rows. If you want to take a look at the row contents at the same time, you
could do something like this:

```

SELECT * FROM accounts AS a, pgrowlocks('accounts') AS p
  WHERE p.locked_row = a.ctid;
```

Be aware however that such a query will be very inefficient.

<a id="PGROWLOCKS-SAMPLE-OUTPUT"></a>

### F.31.2. Sample Output [#](#PGROWLOCKS-SAMPLE-OUTPUT)

```

=# SELECT * FROM pgrowlocks('t1');
 locked_row | locker | multi | xids  |     modes      |  pids
------------+--------+-------+-------+----------------+--------
 (0,1)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,2)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,3)      |    607 | f     | {607} | {"For Update"} | {3107}
 (0,4)      |    607 | f     | {607} | {"For Update"} | {3107}
(4 rows)
```

<a id="PGROWLOCKS-AUTHOR"></a>

### F.31.3. Author [#](#PGROWLOCKS-AUTHOR)

Tatsuo Ishii

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgrowlocks.html)（英文原文，待翻譯）
