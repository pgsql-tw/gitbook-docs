# 29.2. Write-Ahead Logging（WAL）

預寫日誌記錄（WAL）是確保資料完整性的標準方法。在大多數（可能不是全部）有關交易處理的書中可以找到詳細的說明。簡而言之，WAL的中心概念是，只有在記錄了這些變更後，即在描述變更的日誌記錄已更新到永久儲存的時候，才必須寫入對資料檔案（資料表和索引所在的位置）的變更。如果遵循此流程，則不需要在每次事務提交時都將資料完全更新到磁碟，因為我們知道在系統崩潰的情況下，我們將能夠使用日誌來恢復資料庫：尚未套用的所有變更則可以從日誌記錄重新執行到資料頁面。 （這是 roll-forward recovery，也稱為 REDO。）

#### Tip

Because WAL restores database file contents after a crash, journaled file systems are not necessary for reliable storage of the data files or WAL files. In fact, journaling overhead can reduce performance, especially if journaling causes file system _data_ to be flushed to disk. Fortunately, data flushing during journaling can often be disabled with a file system mount option, e.g. `data=writeback` on a Linux ext3 file system. Journaled file systems do improve boot speed after a crash.

Using WAL results in a significantly reduced number of disk writes, because only the log file needs to be flushed to disk to guarantee that a transaction is committed, rather than every data file changed by the transaction. The log file is written sequentially, and so the cost of syncing the log is much less than the cost of flushing the data pages. This is especially true for servers handling many small transactions touching different parts of the data store. Furthermore, when the server is processing many small concurrent transactions, one `fsync` of the log file may suffice to commit many transactions.

WAL also makes it possible to support on-line backup and point-in-time recovery, as described in [Section 25.3](https://www.postgresql.org/docs/12/continuous-archiving.html). By archiving the WAL data we can support reverting to any time instant covered by the available WAL data: we simply install a prior physical backup of the database, and replay the WAL log just as far as the desired time. What's more, the physical backup doesn't have to be an instantaneous snapshot of the database state — if it is made over some period of time, then replaying the WAL log for that period will fix any internal inconsistencies.

