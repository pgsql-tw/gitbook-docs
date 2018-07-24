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

### 參數

`INDEX`

重新建立指定的索引。

`TABLE`

重新建立指定資料表的所有索引。如果資料表具有額外的「TOAST」資料表，那麼也會重新編制索引。

`SCHEMA`

重新建立指定綱要的所有索引。如果此綱要的資料表具有額外的「TOAST」資料表，那麼也會重新編制索引。還會處理共享系統目錄上的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

`DATABASE`

重新建立目前資料庫中的所有索引。還會處理共享系統目錄上的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

`SYSTEM`

重新建立目前資料庫中系統目錄的所有索引。包含共享系統目錄的索引。但不處理使用者資料表的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

_`name`_

要重新編制索引的特定索引，資料表或資料庫的名稱。索引和資料表名稱可以是加上綱要名稱的。目前，REINDEX DATABASE 和 REINDEX SYSTEM 只能重新索引目前資料庫，因此它們的參數必須符合目前資料庫的名稱。

`VERBOSE`

在重新索引每個索引時輸出進度報告。

### Notes

If you suspect corruption of an index on a user table, you can simply rebuild that index, or all indexes on the table, using `REINDEX INDEX` or `REINDEX TABLE`.

Things are more difficult if you need to recover from corruption of an index on a system table. In this case it's important for the system to not have used any of the suspect indexes itself. \(Indeed, in this sort of scenario you might find that server processes are crashing immediately at start-up, due to reliance on the corrupted indexes.\) To recover safely, the server must be started with the `-P` option, which prevents it from using indexes for system catalog lookups.

One way to do this is to shut down the server and start a single-user PostgreSQL server with the `-P` option included on its command line. Then, `REINDEX DATABASE`, `REINDEX SYSTEM`, `REINDEX TABLE`, or `REINDEX INDEX` can be issued, depending on how much you want to reconstruct. If in doubt, use `REINDEX SYSTEM` to select reconstruction of all system indexes in the database. Then quit the single-user server session and restart the regular server. See the [postgres](https://www.postgresql.org/docs/10/static/app-postgres.html) reference page for more information about how to interact with the single-user server interface.

Alternatively, a regular server session can be started with `-P` included in its command line options. The method for doing this varies across clients, but in all libpq-based clients, it is possible to set the `PGOPTIONS` environment variable to `-P` before starting the client. Note that while this method does not require locking out other clients, it might still be wise to prevent other users from connecting to the damaged database until repairs have been completed.

`REINDEX` is similar to a drop and recreate of the index in that the index contents are rebuilt from scratch. However, the locking considerations are rather different. `REINDEX` locks out writes but not reads of the index's parent table. It also takes an exclusive lock on the specific index being processed, which will block reads that attempt to use that index. In contrast, `DROP INDEX` momentarily takes an exclusive lock on the parent table, blocking both writes and reads. The subsequent `CREATE INDEX` locks out writes but not reads; since the index is not there, no read will attempt to use it, meaning that there will be no blocking but reads might be forced into expensive sequential scans.

Reindexing a single index or table requires being the owner of that index or table. Reindexing a database requires being the owner of the database \(note that the owner can therefore rebuild indexes of tables owned by other users\). Of course, superusers can always reindex anything.

### 範例

重建單個索引：

```text
REINDEX INDEX my_index;
```

重建資料表 my\_table 上的所有索引：

```text
REINDEX TABLE my_table;
```

重建特定資料庫中的所有索引，而不必信任系統索引是否有效：

```text
$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

### 相容性

SQL 標準中沒有 REINDEX 指令。

