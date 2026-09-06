## 14.5. Non-Durable Settings [#](#NON-DURABILITY)

<a id="id-1.5.13.8.2"></a>

Durability is a database feature that guarantees the recording of
committed transactions even if the server crashes or loses
power. However, durability adds significant database overhead,
so if your site does not require such a guarantee,
PostgreSQL can be configured to run
much faster. The following are configuration changes you can make
to improve performance in such cases. Except as noted below, durability
is still guaranteed in case of a crash of the database software;
only an abrupt operating system crash creates a risk of data loss
or corruption when these settings are used.

* Place the database cluster's data directory in a memory-backed
  file system (i.e., RAM disk). This eliminates all
  database disk I/O, but limits data storage to the amount of
  available memory (and perhaps swap).
* Turn off [fsync](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FSYNC); there is no need to flush
  data to disk.
* Turn off [synchronous_commit](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT); there might be no
  need to force WAL writes to disk on every
  commit. This setting does risk transaction loss (though not data
  corruption) in case of a crash of the *database*.
* Turn off [full_page_writes](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES); there is no need
  to guard against partial page writes.
* Increase [max_wal_size](../../server-administration/runtime-config/runtime-config-wal.md#GUC-MAX-WAL-SIZE) and [checkpoint_timeout](../../server-administration/runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-TIMEOUT); this reduces the frequency
  of checkpoints, but increases the storage requirements of
  `/pg_wal`.
* Create [unlogged
  tables](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-UNLOGGED) to avoid WAL writes, though it
  makes the tables non-crash-safe.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/non-durability.html)（英文原文，待翻譯）
