<a id="PGWALINSPECT"></a>

# F.37. pg_walinspect

[F.37.1. General Functions](#id-1.11.7.46.8)

[F.37.2. Author](#id-1.11.7.46.9)

<a id="id-1.11.7.46.2"></a>

The `pg_walinspect` module provides SQL functions that allow you to inspect the contents of write-ahead log of a running PostgreSQL database cluster at a low level, which is useful for debugging, analytical, reporting or educational purposes. It is similar to [pg_waldump](../../reference/server-applications/pg_waldump.md), but accessible through SQL rather than a separate utility.

All the functions of this module will provide the WAL information using the current server's timeline ID.

All the functions of this module will try to find the first valid WAL record that is at or after the given <em class="replaceable"><code>in&#95;lsn</code></em> or <em class="replaceable"><code>start&#95;lsn</code></em> and will emit error if no such record is available. Similarly, the <em class="replaceable"><code>end&#95;lsn</code></em> must be available, and if it falls in the middle of a record, the entire record must be available.

## Note

Some functions, such as <code class="function"><a class="link" href="https://www.postgresql.org/docs/15/functions-admin.html#PG-LOGICAL-EMIT-MESSAGE">pg&#95;logical&#95;emit&#95;message</a></code>, return the LSN <em>after</em> the record just inserted. Therefore, if you pass that LSN as <em class="replaceable"><code>in&#95;lsn</code></em> or <em class="replaceable"><code>start&#95;lsn</code></em> to one of these functions, it will return the <em>next</em> record.

By default, use of these functions is restricted to superusers and members of the `pg_read_server_files` role. Access may be granted by superusers to others using `GRANT`.

<a id="id-1.11.7.46.8"></a>

## F.37.1. General Functions

`pg_get_wal_record_info(in_lsn pg_lsn) returns record`

Gets WAL record information of a given LSN. If the given LSN isn't at the start of a WAL record, it gives the information of the next available valid WAL record; or an error if no such record is found. For example, usage of the function is as follows:

```

postgres=# SELECT * FROM pg_get_wal_record_info('0/1E826E98');
-[ RECORD 1 ]----+----------------------------------------------------
start_lsn        | 0/1E826F20
end_lsn          | 0/1E826F60
prev_lsn         | 0/1E826C80
xid              | 0
resource_manager | Heap2
record_type      | PRUNE
record_length    | 58
main_data_length | 8
fpi_length       | 0
description      | snapshotConflictHorizon 33748 nredirected 0 ndead 2
block_ref        | blkref #0: rel 1663/5/60221 fork main blk 2
```

`pg_get_wal_records_info(start_lsn pg_lsn, end_lsn pg_lsn) returns setof record`

Gets information of all the valid WAL records between <em class="replaceable"><code>start&#95;lsn</code></em> and <em class="replaceable"><code>end&#95;lsn</code></em>. Returns one row per WAL record. If <em class="replaceable"><code>start&#95;lsn</code></em> or <em class="replaceable"><code>end&#95;lsn</code></em> are not yet available, the function will raise an error. For example:

```

postgres=# SELECT * FROM pg_get_wal_records_info('0/1E913618', '0/1E913740') LIMIT 1;
-[ RECORD 1 ]----+--------------------------------------------------------------
start_lsn        | 0/1E913618
end_lsn          | 0/1E913650
prev_lsn         | 0/1E9135A0
xid              | 0
resource_manager | Standby
record_type      | RUNNING_XACTS
record_length    | 50
main_data_length | 24
fpi_length       | 0
description      | nextXid 33775 latestCompletedXid 33774 oldestRunningXid 33775
block_ref        |
```

`pg_get_wal_records_info_till_end_of_wal(start_lsn pg_lsn) returns setof record`

This function is the same as `pg_get_wal_records_info()`, except that it gets information of all the valid WAL records from <em class="replaceable"><code>start&#95;lsn</code></em> till the end of WAL.

`pg_get_wal_stats(start_lsn pg_lsn, end_lsn pg_lsn, per_record boolean DEFAULT false) returns setof record`

Gets statistics of all the valid WAL records between <em class="replaceable"><code>start&#95;lsn</code></em> and <em class="replaceable"><code>end&#95;lsn</code></em>. By default, it returns one row per <em class="replaceable"><code>resource&#95;manager</code></em> type. When <em class="replaceable"><code>per&#95;record</code></em> is set to `true`, it returns one row per <em class="replaceable"><code>record&#95;type</code></em>. If <em class="replaceable"><code>start&#95;lsn</code></em> or <em class="replaceable"><code>end&#95;lsn</code></em> are not yet available, the function will raise an error. For example:

```

postgres=# SELECT * FROM pg_get_wal_stats('0/1E847D00', '0/1E84F500')
           WHERE count > 0 AND
                 "resource_manager/record_type" = 'Transaction'
           LIMIT 1;
-[ RECORD 1 ]----------------+-------------------
resource_manager/record_type | Transaction
count                        | 2
count_percentage             | 8
record_size                  | 875
record_size_percentage       | 41.23468426013195
fpi_size                     | 0
fpi_size_percentage          | 0
combined_size                | 875
combined_size_percentage     | 2.8634072910530795
```

`pg_get_wal_stats_till_end_of_wal(start_lsn pg_lsn, per_record boolean DEFAULT false) returns setof record`

This function is the same as `pg_get_wal_stats()`, except that it gets statistics of all the valid WAL records from <em class="replaceable"><code>start&#95;lsn</code></em> till end of WAL.

<a id="id-1.11.7.46.9"></a>

## F.37.2. Author

Bharath Rupireddy <code class="email">&lt;<a class="email" href="mailto:bharath.rupireddyforpostgres@gmail.com">bharath.rupireddyforpostgres@gmail.com</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/pgwalinspect.html)（英文原文，待翻譯）
