# 14.5. 彈性設定[^1]

Durability is a database feature that guarantees the recording of committed transactions even if the server crashes or loses power. However, durability adds significant database overhead, so if your site does not require such a guarantee,PostgreSQLcan be configured to run much faster. The following are configuration changes you can make to improve performance in such cases. Except as noted below, durability is still guaranteed in case of a crash of the database software; only abrupt operating system stoppage creates a risk of data loss or corruption when these settings are used.

* Place the database cluster's data directory in a memory-backed file system \(i.e.RAMdisk\). This eliminates all database disk I/O, but limits data storage to the amount of available memory \(and perhaps swap\).

* Turn off[fsync](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#guc-fsync); there is no need to flush data to disk.

* Turn off[synchronous\_commit](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#guc-synchronous-commit); there might be no need to forceWALwrites to disk on every commit. This setting does risk transaction loss \(though not data corruption\) in case of a crash of the_database_.

* Turn off[full\_page\_writes](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#guc-full-page-writes); there is no need to guard against partial page writes.

* Increase[max\_wal\_size](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#guc-max-wal-size)and[checkpoint\_timeout](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#guc-checkpoint-timeout); this reduces the frequency of checkpoints, but increases the storage requirements of`/pg_wal`.

* Create[unlogged tables](https://www.postgresql.org/docs/10/static/sql-createtable.html#sql-createtable-unlogged)to avoidWALwrites, though it makes the tables non-crash-safe.

---



[^1]:  [PostgreSQL: Documentation: 10: 14.5. Non-Durable Settings](https://www.postgresql.org/docs/10/static/non-durability.html)

