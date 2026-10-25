<a id="LIBPQ-NOTICE-PROCESSING"></a>

## 32.13. 通知訊息處理 [#](#libpq-notice-processing) <a href="#libpq-notice-processing" id="libpq-notice-processing"></a>

<a id="id-1.7.3.20.2"></a>

伺服器產生的通知訊息與警告訊息不會由查詢執行函式
傳回，因為它們並不代表查詢失敗。
這些訊息會改為傳遞給通知訊息處理函式，處理函式返回後，
執行會正常繼續。預設的通知訊息處理函式會將訊息印到
`stderr`，但應用程式可以提供
自己的處理函式來覆寫此行為。

由於歷史因素，通知訊息處理分為兩個層級，分別稱為
通知訊息接收器（notice receiver）與通知訊息處理器（notice processor）。預設行為是由通知訊息接收器
格式化通知訊息，並將一個字串傳給通知訊息處理器
輸出。不過，選擇提供自己的通知訊息接收器的
應用程式，通常會忽略通知訊息處理器這一層，
直接在通知訊息接收器中完成所有工作。

函式 <a id="LIBPQ-PQSETNOTICERECEIVER"></a>`PQsetNoticeReceiver`
<a id="id-1.7.3.20.5.2"></a>
<a id="id-1.7.3.20.5.3"></a> 會設定或
查看連線物件目前的通知訊息接收器。
同樣地，<a id="LIBPQ-PQSETNOTICEPROCESSOR"></a>`PQsetNoticeProcessor`
<a id="id-1.7.3.20.5.5"></a>
<a id="id-1.7.3.20.5.6"></a> 會設定或
查看目前的通知訊息處理器。

```

typedef void (*PQnoticeReceiver) (void *arg, const PGresult *res);

PQnoticeReceiver
PQsetNoticeReceiver(PGconn *conn,
                    PQnoticeReceiver proc,
                    void *arg);

typedef void (*PQnoticeProcessor) (void *arg, const char *message);

PQnoticeProcessor
PQsetNoticeProcessor(PGconn *conn,
                     PQnoticeProcessor proc,
                     void *arg);
```

這兩個函式都會傳回先前的通知訊息接收器或
處理器函式指標，並設定新的值。若你提供
空函式指標，則不會執行任何動作，但仍會傳回目前的指標。

當從伺服器收到通知訊息或警告訊息，或由
libpq 內部產生此類訊息時，會呼叫通知訊息
接收器函式。傳給它的訊息採用
`PGRES_NONFATAL_ERROR` 的
`PGresult` 形式。（這讓接收器可以
使用 [`PQresultErrorField`](libpq-exec-main.md#libpq-pqresulterrorfield) 擷取個別欄位，或使用 [`PQresultErrorMessage`](libpq-exec-main.md#libpq-pqresulterrormessage)
或 [`PQresultVerboseErrorMessage`](libpq-exec-main.md#libpq-pqresultverboseerrormessage) 取得
完整的預先格式化訊息。）傳給 `PQsetNoticeReceiver` 的同一個
void 指標也會一併傳入。（如有需要，此指標可用來存取
應用程式特有的狀態。）

預設的通知訊息接收器只是擷取訊息（使用
[`PQresultErrorMessage`](libpq-exec-main.md#libpq-pqresulterrormessage)），並將其傳給通知訊息
處理器。

通知訊息處理器負責處理以文字形式提供的通知訊息或警告
訊息。傳給它的是訊息的字串文字
（包含結尾的換行字元），以及一個 void 指標，該指標與
傳給 `PQsetNoticeProcessor` 的相同。（如有需要，此指標
可用來存取應用程式特有的狀態。）

預設的通知訊息處理器很簡單，就是：

```

static void
defaultNoticeProcessor(void *arg, const char *message)
{
    fprintf(stderr, "%s", message);
}
```

一旦設定了通知訊息接收器或處理器，你應該預期
只要 `PGconn` 物件或由它建立的
`PGresult` 物件仍然存在，該函式就可能
被呼叫。在建立 `PGresult` 時，
`PGconn` 目前的通知訊息處理指標會複製
到 `PGresult` 中，以供
[`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 之類的函式可能使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-notice-processing.html)（原文版本：18.6；核對日期：2026-10-17）
