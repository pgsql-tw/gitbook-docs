# 13.5. 特別注意

有一些 DDL 命令，目前只有 [TRUNCATE](../../reference/sql-commands/truncate.md) 和 [ALTER TABLE](../../reference/sql-commands/alter-table.md) 的資料表重寫語法，並不是 MVCC 安全的。這意味著在清除或重寫提交之後，如果使用在提交 DDL 指令之前的快照，會使該資料表對於平行處理中的事務將顯示為空。對於在 DDL 指令開始之前沒有存取相關資料表的事務來說，這會是一個問題 - 任何已經這樣做的事務都將至少保存一個 ACCESS SHARE 資料表鎖，這會在該事務完成之前阻擋 DDL 指令。因此，這些指令不會使目標資料表的連續查詢中導致資料表內容的明顯不一致，但它們可能會導致目標資料表的內容與資料庫中的其他資料表之間出現可見的不一致。

尚未將對 Serializable 事務隔離等級的支援增加到 Hot Standby 複製目標（如[第 26.5 節](../../server-administration/high-availability-load-balancing-and-replication/26.5.-hot-standby.md)中所述）。熱備份模式目前支援的最嚴格的隔離等級是 Repeatable Read。在主服務器上的 Serializable 事務中執行所有永久性資料庫寫操作時，將確保所有備用服務器最終能達到一致狀態，在備用服務器上執行的可重複讀事務處理有時會看到與任何串行執行的事務不一致的暫時狀態。
