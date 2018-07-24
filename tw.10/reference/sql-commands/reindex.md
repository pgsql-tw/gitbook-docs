---
description: 版本：10
---

# REINDEX

REINDEX — 重建索引

### 語法

```text
REINDEX [ ( VERBOSE ) ] { INDEX | TABLE | SCHEMA | DATABASE | SYSTEM } name
```

### 說明

REINDEX 使用索引資料表中所儲存的資料重建索引，替換索引舊的版本。有幾種情況可以使用 REINDEX：

* 索引損壞，不再包含有效的資料。雖然理論上這種情況永遠不會發生，但實際上索引會因程式錯誤或硬體故障而損壞。REINDEX 提供了一種恢復的方法。
* 索引變得「臃腫」，即它包含許多空或幾乎空的頁面。在某些不常見的存取模式下，PostgreSQL 中 的 B-tree 索引會發生這種情況。REINDEX 提供了一種透過寫入無死頁的索引新版本來減少索引空間消耗的方法。有關更多訊息，請參閱[第 24.2 節](../../server-administration/routine-database-maintenance-tasks/routine-reindexing.md)。
* 您變更了索引的儲存參數（例如 fillfactor），並希望確保變更能完全生效。
* 使用 CONCURRENTLY 選項的索引建構失敗，留下「無效」的索引。 這些索引沒用，但使用 REINDEX 重建它們會很方便。請注意，REINDEX 將不執行同步建構。要在不干擾線上查詢的情況下建構索引，您應該刪除索引並重新發出 CREATE INDEX CONCURRENTLY 指令。

### Parameters

`INDEX`

Recreate the specified index.

`TABLE`

Recreate all indexes of the specified table. If the table has a secondary “TOAST” table, that is reindexed as well.

`SCHEMA`

Recreate all indexes of the specified schema. If a table of this schema has a secondary “TOAST” table, that is reindexed as well. Indexes on shared system catalogs are also processed. This form of `REINDEX` cannot be executed inside a transaction block.

`DATABASE`

Recreate all indexes within the current database. Indexes on shared system catalogs are also processed. This form of `REINDEX` cannot be executed inside a transaction block.

`SYSTEM`

Recreate all indexes on system catalogs within the current database. Indexes on shared system catalogs are included. Indexes on user tables are not processed. This form of `REINDEX` cannot be executed inside a transaction block.

_`name`_

The name of the specific index, table, or database to be reindexed. Index and table names can be schema-qualified. Presently, `REINDEX DATABASE` and `REINDEX SYSTEM` can only reindex the current database, so their parameter must match the current database's name.

`VERBOSE`

Prints a progress report as each index is reindexed.

### Notes

If you suspect corruption of an index on a user table, you can simply rebuild that index, or all indexes on the table, using `REINDEX INDEX` or `REINDEX TABLE`.

Things are more difficult if you need to recover from corruption of an index on a system table. In this case it's important for the system to not have used any of the suspect indexes itself. \(Indeed, in this sort of scenario you might find that server processes are crashing immediately at start-up, due to reliance on the corrupted indexes.\) To recover safely, the server must be started with the `-P` option, which prevents it from using indexes for system catalog lookups.

One way to do this is to shut down the server and start a single-user PostgreSQL server with the `-P` option included on its command line. Then, `REINDEX DATABASE`, `REINDEX SYSTEM`, `REINDEX TABLE`, or `REINDEX INDEX` can be issued, depending on how much you want to reconstruct. If in doubt, use `REINDEX SYSTEM` to select reconstruction of all system indexes in the database. Then quit the single-user server session and restart the regular server. See the [postgres](https://www.postgresql.org/docs/10/static/app-postgres.html) reference page for more information about how to interact with the single-user server interface.

Alternatively, a regular server session can be started with `-P` included in its command line options. The method for doing this varies across clients, but in all libpq-based clients, it is possible to set the `PGOPTIONS` environment variable to `-P` before starting the client. Note that while this method does not require locking out other clients, it might still be wise to prevent other users from connecting to the damaged database until repairs have been completed.

`REINDEX` is similar to a drop and recreate of the index in that the index contents are rebuilt from scratch. However, the locking considerations are rather different. `REINDEX` locks out writes but not reads of the index's parent table. It also takes an exclusive lock on the specific index being processed, which will block reads that attempt to use that index. In contrast, `DROP INDEX` momentarily takes an exclusive lock on the parent table, blocking both writes and reads. The subsequent `CREATE INDEX` locks out writes but not reads; since the index is not there, no read will attempt to use it, meaning that there will be no blocking but reads might be forced into expensive sequential scans.

Reindexing a single index or table requires being the owner of that index or table. Reindexing a database requires being the owner of the database \(note that the owner can therefore rebuild indexes of tables owned by other users\). Of course, superusers can always reindex anything.

### Examples

Rebuild a single index:

```text
REINDEX INDEX my_index;
```

Rebuild all the indexes on the table `my_table`:

```text
REINDEX TABLE my_table;
```

Rebuild all indexes in a particular database, without trusting the system indexes to be valid already:

```text
$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

### Compatibility

There is no `REINDEX` command in the SQL standard.

