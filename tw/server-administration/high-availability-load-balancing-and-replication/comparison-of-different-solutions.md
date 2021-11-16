# 26.1. 比較不同的解決方案

#### Shared Disk Failover

共享磁碟的故障轉移透過僅使用一份資料庫檔案來避免同步程序的花費。它使用由多個伺服器共享的同一個磁碟陣列。如果主要資料庫伺服器發生故障，備用伺服器就可以掛載並啟動資料庫，就好像它正在從資料庫崩潰後恢復一樣。這樣可以進行快速的故障轉移而不會遺失資料。

共享硬體的功能在網路儲存設備中很常見。儘管必須注意檔案系統具有完整的 POSIX 行為，但也可以使用網路檔案系統（請參閱 [18.2.2.1 節](../server-setup-and-operation/creating-a-database-cluster.md#18-2-2-1-nfs)）。此方法的一個重要限制是，如果共享磁碟陣列發生故障或損壞，則主要伺服器和備用伺服器都將無法運作。另一個問題是，在主要伺服器運行時，備用伺服器永遠都不應存取共享的資料庫檔案。

#### File System (Block Device) Replication

共享硬碟功能的另一種版本是檔案系統複製，其中對檔案系統的所有變更都將鏡像同步到另一台主機上的檔案系統。唯一的限制是必須確保備用伺服器具有檔案系統一致副本的方式進行鏡像-特別是，寫入備用資料庫的順序必須與主要伺服器上的順序相同。DRBD 是針對 Linux 常用檔案系統複製的解決方案。

#### Write-Ahead Log Shipping

透過讀取預寫日誌（WAL）記錄串流，可以使熱備用伺服器保持最新狀態。如果主要伺服器發生故障，則備用資料庫幾乎將包含主要伺服器的所有資料，並且可以迅速成為新的主要資料庫伺服器。這可以是同步或非同步的，不過只能以整個資料庫伺服器為單位來實行。

備用伺服器可以使用基於檔案的日誌傳送（[第 26.2 節](log-shipping-standby-servers.md)）或串流式複寫（請參閱[第 26.2.5 節](log-shipping-standby-servers.md#26-2-5-streaming-replication)）或兩者的結合來實現。有關熱備用伺服器的說明，請參閱[第 26.5 節](26.5.-hot-standby.md)。

#### Logical Replication

邏輯複寫讓資料庫伺服器可以將資料修改的過程發送到另一台伺服器。 PostgreSQL 的邏輯複寫會從 WAL 產生邏輯資料修改串流。邏輯複寫允許複寫單個資料表中的資料變更。邏輯複寫不需要將特定的伺服器指定為主要伺服器或備用伺服器，而是允許資料沿多個方向流動。有關邏輯複寫的更多資訊，請參閱第 30 章。透過邏輯解譯介面（第 48 章），第三方延伸套件也有機會提供類似的功能。

#### Trigger-Based Master-Standby Replication

A master-standby replication setup sends all data modification queries to the master server. The master server asynchronously sends data changes to the standby server. The standby can answer read-only queries while the master server is running. The standby server is ideal for data warehouse queries.

Slony-I is an example of this type of replication, with per-table granularity, and support for multiple standby servers. Because it updates the standby server asynchronously (in batches), there is possible data loss during fail over.

#### SQL-Based Replication Middleware

With SQL-based replication middleware, a program intercepts every SQL query and sends it to one or all servers. Each server operates independently. Read-write queries must be sent to all servers, so that every server receives any changes. But read-only queries can be sent to just one server, allowing the read workload to be distributed among them.

If queries are simply broadcast unmodified, functions like `random()`, `CURRENT_TIMESTAMP`, and sequences can have different values on different servers. This is because each server operates independently, and because SQL queries are broadcast (and not actual modified rows). If this is unacceptable, either the middleware or the application must query such values from a single server and then use those values in write queries. Another option is to use this replication option with a traditional master-standby setup, i.e., data modification queries are sent only to the master and are propagated to the standby servers via master-standby replication, not by the replication middleware. Care must also be taken that all transactions either commit or abort on all servers, perhaps using two-phase commit ([PREPARE TRANSACTION](https://www.postgresql.org/docs/13/sql-prepare-transaction.html) and [COMMIT PREPARED](https://www.postgresql.org/docs/13/sql-commit-prepared.html)). Pgpool-II and Continuent Tungsten are examples of this type of replication.

#### Asynchronous Multimaster Replication

對於不定期連線或通訊網路速度較慢的伺服器（例如筆記型電腦或遠端伺服器），保持伺服器之間的資料一致性是一個挑戰。使用 Asynchronous Multimaster Replication，每個伺服器獨立工作，並定期與其他伺服器溝通以識別衝突的交易事務。可以透過使用者或訂定規則來解決衝突。Bucardo 是這種複寫方式的一個範例。

#### Synchronous Multimaster Replication

在 Synchronous Multimaster Replication 中，每個伺服器都可以接受寫入請求，並且在每個事務提交之前，已修改的資料將從原始伺服器傳輸到所有其他伺服器之中。繁重的寫入活動可能導致過多的鎖定和提交延遲，從而導致效能下降。讀取請求可以發送到任何一個伺服器。有一些實作方案使用共享磁碟來減少通訊成本。同步多重主要伺服器複寫最適合大多數為讀取工作的負載情況，儘管它的最大優點是任何伺服器都可以接受寫入請求-毋須在主要伺服器和備用伺服器之間區分工作負載，並且因為資料變更是由一台伺服器發送到另一台伺服器的，像 random() 這樣的不確定結果的函數也沒有問題。

PostgreSQL 並不提供這種複寫機制，儘管可以使用 PostgreSQL 兩階段提交（PREPARE TRANSACTION 和 COMMIT PREPARED）在應用程式或中間層服務中實作這種複寫方式。

[Table 26.1](comparison-of-different-solutions.md#table-26-1-high-availability-load-balancing-and-replication-feature-matrix) 總結了上面各種解決方案的功能。

#### **Table 26.1. High Availability, Load Balancing, and Replication Feature Matrix**

| Feature                             | Shared Disk | File System Repl. | Write-Ahead Log Shipping | Logical Repl.                     | Trigger-Based Repl. | SQL Repl. Middle-ware | Async. MM Repl. | Sync. MM Repl.           |
| ----------------------------------- | ----------- | ----------------- | ------------------------ | --------------------------------- | ------------------- | --------------------- | --------------- | ------------------------ |
| Popular examples                    | NAS         | DRBD              | built-in streaming repl. | built-in logical repl., pglogical | Londiste, Slony     | pgpool-II             | Bucardo         |                          |
| Comm. method                        | shared disk | disk blocks       | WAL                      | logical decoding                  | table rows          | SQL                   | table rows      | table rows and row locks |
| No special hardware required        |             | •                 | •                        | •                                 | •                   | •                     | •               | •                        |
| Allows multiple master servers      |             |                   |                          | •                                 |                     | •                     | •               | •                        |
| No master server overhead           | •           |                   | •                        | •                                 |                     | •                     |                 |                          |
| No waiting for multiple servers     | •           |                   | with sync off            | with sync off                     | •                   |                       | •               |                          |
| Master failure will never lose data | •           | •                 | with sync on             | with sync on                      |                     | •                     |                 | •                        |
| Replicas accept read-only queries   |             |                   | with hot standby         | •                                 | •                   | •                     | •               | •                        |
| Per-table granularity               |             |                   |                          | •                                 | •                   |                       | •               | •                        |
| No conflict resolution necessary    | •           | •                 | •                        |                                   | •                   | •                     |                 | •                        |

There are a few solutions that do not fit into the above categories:

#### Data Partitioning

Data partitioning splits tables into data sets. Each set can be modified by only one server. For example, data can be partitioned by offices, e.g., London and Paris, with a server in each office. If queries combining London and Paris data are necessary, an application can query both servers, or master/standby replication can be used to keep a read-only copy of the other office's data on each server.

#### Multiple-Server Parallel Query Execution

Many of the above solutions allow multiple servers to handle multiple queries, but none allow a single query to use multiple servers to complete faster. This solution allows multiple servers to work concurrently on a single query. It is usually accomplished by splitting the data among servers and having each server execute its part of the query and return results to a central server where they are combined and returned to the user. This can be implemented using the PL/Proxy tool set.

It should also be noted that because PostgreSQL is open source and easily extended, a number of companies have taken PostgreSQL and created commercial closed-source solutions with unique failover, replication, and load balancing capabilities. These are not discussed here.
