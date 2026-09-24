<a id="MONITORING-PS"></a>

## 27.1. 標準 Unix 工具 [#](#MONITORING-PS)

<a id="id-1.6.14.6.2"></a>

在大多數 Unix 平台上，PostgreSQL 會修改
`ps` 所回報的命令標題，讓你能輕易識別
個別的伺服器程序。以下是一則顯示範例：

```

$ ps auxww | grep ^postgres
postgres  15551  0.0  0.1  57536  7132 pts/0    S    18:02   0:00 postgres -i
postgres  15554  0.0  0.0  57536  1184 ?        Ss   18:02   0:00 postgres: background writer
postgres  15555  0.0  0.0  57536   916 ?        Ss   18:02   0:00 postgres: checkpointer
postgres  15556  0.0  0.0  57536   916 ?        Ss   18:02   0:00 postgres: walwriter
postgres  15557  0.0  0.0  58504  2244 ?        Ss   18:02   0:00 postgres: autovacuum launcher
postgres  15582  0.0  0.0  58772  3080 ?        Ss   18:04   0:00 postgres: joe runbug 127.0.0.1 idle
postgres  15606  0.0  0.0  58772  3052 ?        Ss   18:07   0:00 postgres: tgl regression [local] SELECT waiting
postgres  15610  0.0  0.0  58772  3056 ?        Ss   18:07   0:00 postgres: tgl regression [local] idle in transaction
```

（`ps` 的適當呼叫方式因平台而異，
顯示的細節內容也是如此。此範例取自一套
較新的 Linux 系統。）此處所列出的第一個程序，
是主要伺服器程序。其所顯示的命令引數，
與啟動時所使用的引數相同。接下來的四個程序，
是由主要程序自動啟動的背景工作程序。
（若你已將系統設定為不執行自動 vacuum，
則不會出現「autovacuum launcher」程序。）
其餘的每一個程序，
都是負責處理一個用戶端連線的伺服器程序。
每個這類程序，都會以下列格式，
設定其命令列顯示內容：

```

postgres: user database host activity
```

使用者、資料庫，以及（用戶端）主機這幾個項目，
在該用戶端連線的存續期間都會保持不變，
但活動指示器則會改變。此活動可以是 `idle`
（即等待用戶端命令）、`idle in transaction`
（在 `BEGIN` 區塊內等待用戶端），
或是像 `SELECT` 這樣的命令類型名稱。
此外，若該伺服器程序目前正在等待
其他工作階段持有的鎖定，就會附加 `waiting`。
在上方的範例中，我們可以推論出，
程序 15606 正在等待程序 15610
完成其交易，藉此釋放某個鎖定。
（程序 15610 必定是造成阻塞的一方，
因為並沒有其他作用中的工作階段。在較複雜的情況下，
就需要查看
[`pg_locks`](../../internals/views/view-pg-locks.md)
系統檢視表，才能判斷究竟是誰阻塞了誰。）

若已設定 [cluster_name](../runtime-config/runtime-config-logging.md#GUC-CLUSTER-NAME)，
叢集名稱也會顯示在 `ps` 輸出中：

```

$ psql -c 'SHOW cluster_name'
 cluster_name
--------------
 server1
(1 row)

$ ps aux|grep server1
postgres   27093  0.0  0.0  30096  2752 ?        Ss   11:34   0:00 postgres: server1: background writer
...
```

若你已關閉 [update_process_title](../runtime-config/runtime-config-logging.md#GUC-UPDATE-PROCESS-TITLE)，
則活動指示器就不會被更新；
程序標題只會在新程序啟動時設定一次。
在某些平台上，這能節省可測量得出的每一命令額外負擔；
在其他平台上則影響甚微。

### 提示

Solaris 需要特殊處理方式。你必須使用
`/usr/ucb/ps`，而不是
`/bin/ps`。你還必須使用兩個
`w` 旗標，而不能只用一個。此外，
你最初呼叫 `postgres` 命令時，
其 `ps` 狀態顯示內容，
必須比每個伺服器程序所提供的內容更短。
若你未能完成以上三項要求，每個伺服器程序的
`ps` 輸出，就會是最初的 `postgres`
命令列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-ps.html)（原文版本：18.6；核對日期：2026-09-24）
