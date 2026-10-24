<a id="LIBPQ-NOTIFY"></a>

## 32.9. 非同步通知 [#](#libpq-notify) <a href="#libpq-notify" id="libpq-notify"></a>

<a id="id-1.7.3.16.2"></a>

PostgreSQL 透過 `LISTEN` 與 `NOTIFY`
命令提供非同步通知。用戶端工作階段以 `LISTEN` 命令
登記其對特定通知頻道的關注（並且
可以用 `UNLISTEN` 命令停止監聽）。當任何
工作階段執行帶有該頻道名稱的 `NOTIFY` 命令時，
所有監聽該頻道的工作階段都會以非同步方式收到通知。
可以傳遞一個「承載（payload）」字串，向監聽者傳達額外資料。

libpq 應用程式將
`LISTEN`、`UNLISTEN`
與 `NOTIFY` 命令作為
一般 SQL 命令送出。之後可以呼叫
<a id="LIBPQ-PQNOTIFIES"></a>`PQnotifies`<a id="id-1.7.3.16.4.7"></a> 來偵測 `NOTIFY`
訊息是否到達。

函式 `PQnotifies` 會從伺服器傳來的
未處理通知訊息清單中傳回下一則通知。
若沒有待處理的通知，則傳回空指標。一旦
通知由 `PQnotifies` 傳回，即視為
已處理，並會從通知清單中移除。

```

PGnotify *PQnotifies(PGconn *conn);

typedef struct pgNotify
{
    char *relname;              /* notification channel name */
    int  be_pid;                /* process ID of notifying server process */
    char *extra;                /* notification payload string */
} PGnotify;
```

處理完 `PQnotifies` 傳回的
`PGnotify` 物件後，務必以
[`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 將其釋放。只需釋放
`PGnotify` 指標即可；
`relname` 與 `extra`
欄位並不代表各自獨立的記憶體配置。（這些欄位的名稱
是歷史沿革的結果；特別是，頻道名稱不必與
關聯名稱有任何關係。）

[範例 32.2](libpq-example.md#libpq-example-2) 提供了一個範例程式，示範
非同步通知的用法。

`PQnotifies` 實際上並不會從
伺服器讀取資料；它只會傳回先前已被另一個
libpq 函式吸收的訊息。在很早期的
libpq 版本中，確保及時收到
`NOTIFY` 訊息的唯一方法，是不斷送出命令（即使是
空命令），並在每次
[`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 之後檢查 `PQnotifies`。這種做法雖然仍然有效，但因為
浪費處理能力，已不建議使用。

在沒有實用的命令可執行時，檢查 `NOTIFY` 訊息的較佳方法是
呼叫 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput)，然後檢查
`PQnotifies`。你可以使用
`select()` 等待資料從
伺服器到達，如此除非有事要處理，否則不會耗用 CPU 資源。
（請參閱 [`PQsocket`](libpq-status.md#libpq-pqsocket) 以取得要搭配
`select()` 使用的檔案描述子編號。）請注意，
無論你是以
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery)/[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 送出命令，還是
只使用 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC)，這種方式都能正常運作。不過，你應該記得
在每次 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 或 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 之後檢查
`PQnotifies`，以確認在命令處理期間是否有通知傳入。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-notify.html)（原文版本：18.6；核對日期：2026-10-17）
