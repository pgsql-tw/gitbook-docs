## 第 46 章 背景工作程序

<a id="id-1.8.13.2"></a>

PostgreSQL 可以擴充，以在獨立的程序中執行使用者提供的程式碼。
這類程序由 `postgres` 啟動、停止並監控，
使其生命週期能夠與伺服器的狀態緊密連結。
這些程序會附著於 PostgreSQL 的
共享記憶體區域，並可選擇在內部連線至資料庫；它們也可以像由一般用戶端連線的伺服器
程序一樣，依序執行多筆交易。此外，透過連結至 libpq，它們也可以連線至
伺服器，並表現得如同一般的用戶端應用程式一樣。

<a id="id-1.8.13.3"></a>

### 警告

使用背景工作程序存在相當大的穩健性與安全性風險，因為它們是以
`C` 語言撰寫，對資料擁有不受限制的存取權。希望啟用
包含背景工作程序之模組的管理員，應格外謹慎。只應允許經過仔細審核的模組
執行背景工作程序。

背景工作程序可以在 PostgreSQL 啟動時，
藉由將模組名稱列於 `shared_preload_libraries` 中來進行初始化。希望執行背景工作
程序的模組，可以透過在其 `_PG_init()` 函式中呼叫
`RegisterBackgroundWorker(BackgroundWorker
*worker)`
來註冊該程序。
背景工作程序也可以在系統啟動並執行之後，
藉由呼叫
`RegisterDynamicBackgroundWorker(BackgroundWorker
*worker, BackgroundWorkerHandle
**handle)` 來啟動。與只能從
postmaster 程序內部呼叫的
`RegisterBackgroundWorker` 不同，
`RegisterDynamicBackgroundWorker` 必須從
一般的後端或另一個背景工作程序中呼叫。

`BackgroundWorker` 結構的定義如下：

```

typedef void (*bgworker_main_type)(Datum main_arg);
typedef struct BackgroundWorker
{
    char        bgw_name[BGW_MAXLEN];
    char        bgw_type[BGW_MAXLEN];
    int         bgw_flags;
    BgWorkerStartTime bgw_start_time;
    int         bgw_restart_time;       /* in seconds, or BGW_NEVER_RESTART */
    char        bgw_library_name[MAXPGPATH];
    char        bgw_function_name[BGW_MAXLEN];
    Datum       bgw_main_arg;
    char        bgw_extra[BGW_EXTRALEN];
    pid_t       bgw_notify_pid;
} BackgroundWorker;
```

`bgw_name` 與 `bgw_type` 是
用於日誌訊息、程序清單及類似情境中的字串。
`bgw_type` 對於同一類型的所有背景工作
程序而言，應該都相同，如此才能在程序清單中，將這類工作程序分組列出。
另一方面，`bgw_name`
則可以包含該特定程序的額外資訊。
（通常，`bgw_name` 的字串會以某種方式包含其類型，
但這並非嚴格要求。）

`bgw_flags` 是一個以位元或（bitwise-or）方式組合的位元遮罩，用以指出
該模組所需要的能力。可能的值有：

`BGWORKER_SHMEM_ACCESS`
:   <a id="id-1.8.13.8.2.1.2.1.1"></a>
    請求共享記憶體存取權。此旗標為必要項目。

`BGWORKER_BACKEND_DATABASE_CONNECTION`
:   <a id="id-1.8.13.8.2.2.2.1.1"></a>
    請求建立資料庫連線的能力，之後便可透過該連線執行交易與
    查詢。使用 `BGWORKER_BACKEND_DATABASE_CONNECTION`
    連線至資料庫的背景工作程序，也必須以
    `BGWORKER_SHMEM_ACCESS` 附著共享記憶體，否則
    工作程序啟動將會失敗。

`bgw_start_time` 是 `postgres`
應該啟動該程序時所處的伺服器狀態；其值可以是
`BgWorkerStart_PostmasterStart`（在
`postgres` 本身完成自身初始化後立即啟動；提出此請求的程序不得連線至資料庫）、
`BgWorkerStart_ConsistentState`（在熱備援伺服器達到一致狀態後立即啟動，
使程序得以連線至資料庫並執行唯讀查詢），以及
`BgWorkerStart_RecoveryFinished`（在系統進入正常讀寫狀態後立即啟動）。請注意，在非熱備援伺服器上，最後兩個值是等效的。另請注意，此設定僅指出
程序何時應被啟動；當系統進入另一個狀態時，它們並不會停止。

`bgw_restart_time` 是指若該程序當機，
`postgres` 在重新啟動該程序之前應等待的
秒數間隔。其值可以是任何正數，
或是 `BGW_NEVER_RESTART`，表示在該程序當機時
不要重新啟動。

`bgw_library_name` 是應在其中尋找該背景工作程序
初始進入點的程式庫名稱。
該命名的程式庫將由工作程序動態載入，並以
`bgw_function_name` 識別要呼叫的
函式。若呼叫的是核心程式碼中的函式，此欄位必須
設為 `"postgres"`。

`bgw_function_name` 是用作新背景工作程序
初始進入點的函式名稱。若
此函式位於動態載入的程式庫中，則必須標記為
`PGDLLEXPORT`（且不得為 `static`）。

`bgw_main_arg` 是傳給背景工作程序主函式的
`Datum` 引數。此主函式應接受
單一 `Datum` 型別的引數，並傳回 `void`。
`bgw_main_arg` 將作為該引數傳入。
此外，全域變數 `MyBgworkerEntry`
會指向註冊時所傳入之 `BackgroundWorker` 結構的
複本；該工作程序或許會發現檢視此結構相當有幫助。

在 Windows 上（以及任何其他有定義 `EXEC_BACKEND`
的地方），或是在動態背景工作程序中，以參照方式傳遞
`Datum` 並不安全，只能以傳值方式傳遞。若需要引數，
最安全的做法是傳遞一個 int32 或其他小型值，並將其作為索引，
用來存取共享記憶體中配置的陣列。若傳遞的是像 `cstring`
或 `text` 這樣的值，該指標在新的背景工作程序中將不會有效。

`bgw_extra` 可以包含要傳給背景工作程序的
額外資料。與 `bgw_main_arg` 不同，這項資料
不會作為引數傳給工作程序的主函式，但可以如上所述，
透過 `MyBgworkerEntry` 加以存取。

`bgw_notify_pid` 是 postmaster 應在該程序啟動或結束時，
向其傳送 `SIGUSR1` 的 PostgreSQL
後端程序 PID。對於在 postmaster 啟動時註冊的工作程序，或是註冊該工作程序的後端
不希望等待工作程序啟動的情況，此值應為 0。否則，
應將其初始化為 `MyProcPid`。

一旦開始執行，該程序便可以透過呼叫
`BackgroundWorkerInitializeConnection(char *dbname, char *username, uint32 flags)` 或
`BackgroundWorkerInitializeConnectionByOid(Oid dboid, Oid useroid, uint32 flags)`
來連線至資料庫。
這讓該程序得以使用
`SPI` 介面執行交易與查詢。若 `dbname` 為 NULL 或
`dboid` 為 `InvalidOid`，該工作階段將不會連線至任何特定
資料庫，但仍可存取共享的系統目錄表（shared catalogs）。
若 `username` 為 NULL 或 `useroid` 為
`InvalidOid`，該程序將以 `initdb`
期間所建立的超級使用者身分執行。若在 `flags` 中指定
`BGWORKER_BYPASS_ALLOWCONN`，便可繞過
不允許使用者連線之資料庫的連線限制。
若在 `flags` 中指定
`BGWORKER_BYPASS_ROLELOGINCHECK`，便可繞過用於
連線至資料庫之角色的登入檢查。
一個背景工作程序只能呼叫這兩個函式中的其中一個，且只能呼叫一次。無法
切換資料庫。

當控制權到達背景工作程序的主函式時，訊號一開始會被
封鎖，且必須由該函式自行解除封鎖；這是為了
讓該程序在必要時，能夠自訂其訊號處理常式。
可以透過呼叫 `BackgroundWorkerUnblockSignals` 在新的程序中解除封鎖訊號，
並透過呼叫 `BackgroundWorkerBlockSignals` 加以封鎖。

若某個背景工作程序的 `bgw_restart_time`
設定為 `BGW_NEVER_RESTART`，或是它以結束碼 0
結束，或是被 `TerminateBackgroundWorker` 終止，
postmaster 便會在其結束時自動將其取消註冊。
否則，它將在透過
`bgw_restart_time` 所設定的時間間隔之後重新啟動，
或是在 postmaster 因後端失敗而重新初始化叢集時立即重新啟動。只需要暫時
暫停執行的後端，應使用可中斷的睡眠，
而不是直接結束；這可以透過呼叫
`WaitLatch()` 來達成。呼叫該函式時，請務必確認已設定
`WL_POSTMASTER_DEATH` 旗標，並在
`postgres` 本身已終止的緊急情況下，檢查其傳回碼以立即結束。

當背景工作程序是透過
`RegisterDynamicBackgroundWorker` 函式註冊時，
執行該註冊的後端便可以取得
該工作程序狀態的相關資訊。希望這麼做的後端，應
將一個 `BackgroundWorkerHandle *` 的位址，作為第二個
引數傳給 `RegisterDynamicBackgroundWorker`。若
該工作程序成功註冊，此指標將被初始化為一個不透明的
控制代碼，之後可將其傳給
`GetBackgroundWorkerPid(BackgroundWorkerHandle *, pid_t *)` 或
`TerminateBackgroundWorker(BackgroundWorkerHandle *)`。
`GetBackgroundWorkerPid` 可用來輪詢該
工作程序的狀態：傳回值 `BGWH_NOT_YET_STARTED` 表示
該工作程序尚未被 postmaster 啟動；
`BGWH_STOPPED` 表示它已被啟動但
已不再執行；而 `BGWH_STARTED` 則表示它目前
正在執行。在最後這種情況下，PID 也會透過
第二個引數傳回。
`TerminateBackgroundWorker` 會使 postmaster 在該工作程序正在執行時，向其傳送
`SIGTERM`，並在其不再執行時將其取消註冊。

在某些情況下，註冊了背景工作程序的程序，可能會希望
等待該工作程序啟動。這可以透過將
`bgw_notify_pid` 初始化為 `MyProcPid`，
接著將註冊時取得的
`BackgroundWorkerHandle *` 傳給
`WaitForBackgroundWorkerStartup(BackgroundWorkerHandle
*handle, pid_t *)` 函式來達成。
此函式將會阻塞，直到 postmaster 已嘗試啟動該
背景工作程序，或直到 postmaster 結束為止。若該背景工作程序
正在執行，傳回值將為 `BGWH_STARTED`，並且
PID 將被寫入所提供的位址。否則，傳回
值將為 `BGWH_STOPPED` 或
`BGWH_POSTMASTER_DIED`。

程序也可以等待背景工作程序關閉，方式是使用
`WaitForBackgroundWorkerShutdown(BackgroundWorkerHandle
*handle)` 函式，並傳入
註冊時所取得的 `BackgroundWorkerHandle *`。此
函式將會阻塞，直到該背景工作程序結束，或 postmaster 結束為止。
當背景工作程序結束時，傳回值為
`BGWH_STOPPED`；若 postmaster 結束，則會傳回
`BGWH_POSTMASTER_DIED`。

背景工作程序可以傳送非同步通知訊息，方式可以是
透過 SPI 使用 `NOTIFY` 命令，
或直接透過 `Async_Notify()`。這類通知
將在交易提交時傳送。
背景工作程序不應使用 `LISTEN` 命令
註冊以接收非同步通知，因為並沒有讓工作程序消費此類通知的基礎架構。

`src/test/modules/worker_spi` 模組
包含一個可運作的範例，
示範了一些實用的技巧。

已註冊背景工作程序的最大數量，受
[max_worker_processes](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 限制。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bgworker.html)（原文版本：18.6；核對日期：2026-09-24）
