<a id="NON-DURABILITY"></a>

## 14.5. 非持久性設定 [#](#NON-DURABILITY)

<a id="id-1.5.13.8.2"></a>

持久性（durability）是一項資料庫功能，它保證即使伺服器當機或斷電，已提交的交易仍會被記錄下來。不過，持久性會為資料庫帶來相當大的額外負擔，因此如果你的網站不需要這樣的保證，可以將 PostgreSQL 設定為執行得更快。以下是在這類情況下，可以用來提升效能的組態變更。除了下面特別註明的情況之外，在資料庫軟體當機時仍然能保證持久性；使用這些設定時，只有作業系統突然當機才會造成資料遺失或損毀的風險。

* 將資料庫叢集的資料目錄放在以記憶體為基礎的檔案系統（也就是 RAM 磁碟）中。這可以免除所有資料庫的磁碟 I/O，但資料儲存量會被限制在可用記憶體（或許再加上置換空間）的大小之內。
* 關閉 [fsync](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FSYNC)；不需要將資料排清（flush）到磁碟。
* 關閉 [synchronous_commit](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT)；可能不需要在每次提交時都強制將 WAL 寫入磁碟。這項設定在*資料庫*當機時確實有遺失交易的風險（但不會造成資料損毀）。
* 關閉 [full_page_writes](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES)；不需要防範部分頁面寫入。
* 增加 [max_wal_size](../../server-administration/runtime-config/runtime-config-wal.md#GUC-MAX-WAL-SIZE) 與 [checkpoint_timeout](../../server-administration/runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-TIMEOUT)；這會降低檢查點的頻率，但會增加 `/pg_wal` 的儲存空間需求。
* 建立[無日誌資料表](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-UNLOGGED)（unlogged table）以避免寫入 WAL，但這會使這些資料表在當機時不安全。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/non-durability.html)（原文版本：18.6；核對日期：2026-09-11）
