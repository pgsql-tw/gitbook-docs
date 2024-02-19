# 30.4. Asynchronous Commit

Asyncgronous commit 是可以讓事務更快完成的選項，但如果資料庫崩潰，最後未完成的事務可能會遺失。在許多應用中，這是一個可以接受的折衷方案。

如上一節所述，事務提交通常是同步的：伺服器在將成功的指示回傳給用戶端之前，等待事務的 WAL 記錄寫入到永久儲存。因此，即使在此之後立即發生伺服器崩潰的情況下，也可以保證用戶端將保留回報為已提交的事務。但是，對於短交易，此延遲時間是總交易時間的主要組成部分。選擇非同步提交模式意味著在邏輯上完成事務後，伺服器將在產生的 WAL 記錄實際進入磁碟之前回傳成功。這可以大大提高短交易事務的處理量。

非同步提交會帶來資料遺失的風險。在向用戶端提交事務完成報告與真正提交事務的時間之間存在很短的時間窗口（也就是說，如果伺服器崩潰，可以保證不會遺失）。因此，如果用戶端將根據將記住交易的假設來採取額外的操作，則不應使用非同步提交。例如，銀行肯定不會在記錄 ATM 現金分配的交易中使用非同步提交。但是在許多情況下，例如事件日誌記錄，不需要這種強大的保證。

The risk that is taken by using asynchronous commit is of data loss, not data corruption. If the database should crash, it will recover by replaying WAL up to the last record that was flushed. The database will therefore be restored to a self-consistent state, but any transactions that were not yet flushed to disk will not be reflected in that state. The net effect is therefore loss of the last few transactions. Because the transactions are replayed in commit order, no inconsistency can be introduced — for example, if transaction B made changes relying on the effects of a previous transaction A, it is not possible for A's effects to be lost while B's effects are preserved.

The user can select the commit mode of each transaction, so that it is possible to have both synchronous and asynchronous commit transactions running concurrently. This allows flexible trade-offs between performance and certainty of transaction durability. The commit mode is controlled by the user-settable parameter [synchronous\_commit](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT), which can be changed in any of the ways that a configuration parameter can be set. The mode used for any one transaction depends on the value of `synchronous_commit` when transaction commit begins.

Certain utility commands, for instance `DROP TABLE`, are forced to commit synchronously regardless of the setting of `synchronous_commit`. This is to ensure consistency between the server's file system and the logical state of the database. The commands supporting two-phase commit, such as `PREPARE TRANSACTION`, are also always synchronous.

If the database crashes during the risk window between an asynchronous commit and the writing of the transaction's WAL records, then changes made during that transaction _will_ be lost. The duration of the risk window is limited because a background process (the “WAL writer”) flushes unwritten WAL records to disk every [wal\_writer\_delay](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-WAL-WRITER-DELAY) milliseconds. The actual maximum duration of the risk window is three times `wal_writer_delay` because the WAL writer is designed to favor writing whole pages at a time during busy periods.

#### Caution

An immediate-mode shutdown is equivalent to a server crash, and will therefore cause loss of any unflushed asynchronous commits.

Asynchronous commit provides behavior different from setting [fsync](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-FSYNC) = off. `fsync` is a server-wide setting that will alter the behavior of all transactions. It disables all logic within PostgreSQL that attempts to synchronize writes to different portions of the database, and therefore a system crash (that is, a hardware or operating system crash, not a failure of PostgreSQL itself) could result in arbitrarily bad corruption of the database state. In many scenarios, asynchronous commit provides most of the performance improvement that could be obtained by turning off `fsync`, but without the risk of data corruption.

[commit\_delay](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-COMMIT-DELAY) also sounds very similar to asynchronous commit, but it is actually a synchronous commit method (in fact, `commit_delay` is ignored during an asynchronous commit). `commit_delay` causes a delay just before a transaction flushes WAL to disk, in the hope that a single flush executed by one such transaction can also serve other transactions committing at about the same time. The setting can be thought of as a way of increasing the time window in which transactions can join a group about to participate in a single flush, to amortize the cost of the flush among multiple transactions.
