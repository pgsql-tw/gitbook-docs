# 14.5. 風險性彈性設定

Durability (耐用性)是一種資料庫特性，即使伺服器當機或斷電，也可以保證保存好已提交的交易事務。但是，耐用性會增加大量的資料庫成本。因此，如果您的服務不需要這樣的保證，則可以將 PostgreSQL 設定可以執行得更快。以下是在這種情況下可以進行以提高效能的配置調整。除非另有說明，否則在資料庫軟體當機的情況下仍然可以保證持久性；使用這些設定時，只有突然的作業系統停止才會造成資料遺失或損壞的風險。

* 將資料庫叢集的資料目錄放置在記憶體中的檔案系統（即 RAM 磁碟）中。這樣可以完全消除所有資料庫磁碟的 I/O，但將資料儲存限制為可用記憶體大小（可能會包含 SWAP 空間）。
* 關閉 [fsync](../../server-administration/server-configuration/write-ahead-log.md#fsync-boolean)；毌須主動將資料更新到磁碟。
* 關閉 [sync\_commit](../../server-administration/server-configuration/write-ahead-log.md#synchronous\_commit-enum)；可以不用在每次交易提交時都強制將 WAL 寫到磁碟。如果資料庫服務當掉，此設定會產生交易結果消失（但不會破壞資料）的風險。
* 關閉 [full\_page\_writes](../../server-administration/server-configuration/write-ahead-log.md#full\_page\_writes-boolean); 沒有必要防止部分頁面寫入。
* 增加 [max\_wal\_size](../../server-administration/server-configuration/write-ahead-log.md#max\_wal\_size-integer) 和 [checkpoint\_timeout](../../server-administration/server-configuration/write-ahead-log.md#checkpoint\_timeout-integer); 這減少了檢查點的頻率，但是增加了 /pg\_wal 的儲存需求。
* 建立 [unlogged table](../../reference/sql-commands/create-table.md) 以避免 WAL 寫入，儘管這會使資料表是 non-crash-safe。
