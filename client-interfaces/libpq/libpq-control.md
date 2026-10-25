<a id="LIBPQ-CONTROL"></a>

## 32.11. 控制函式 [#](#libpq-control) <a href="#libpq-control" id="libpq-control"></a>

這些函式控制 libpq 行為的各種細節。

<a id="LIBPQ-PQCLIENTENCODING"></a>

### `PQclientEncoding`<a id="id-1.7.3.18.3.1.1.2"></a> [#](#libpq-pqclientencoding) <a href="#libpq-pqclientencoding" id="libpq-pqclientencoding"></a>

傳回用戶端編碼。

```

    int PQclientEncoding(const PGconn *conn);
```

請注意，它傳回的是編碼 ID，而不是像 `EUC_JP` 這樣的符號字串。若不成功，則傳回 -1。要將編碼 ID 轉換為編碼名稱，你可以使用：

```

    char *pg_encoding_to_char(int encoding_id);
```

<a id="LIBPQ-PQSETCLIENTENCODING"></a>

### `PQsetClientEncoding`<a id="id-1.7.3.18.3.2.1.2"></a> [#](#libpq-pqsetclientencoding) <a href="#libpq-pqsetclientencoding" id="libpq-pqsetclientencoding"></a>

設定用戶端編碼。

```

    int PQsetClientEncoding(PGconn *conn, const char *encoding);
```

*`conn`* 是連往伺服器的連線，*`encoding`* 是你想使用的編碼。若函式成功設定編碼，則傳回 0，否則傳回 -1。此連線目前的編碼可以使用 [`PQclientEncoding`](libpq-control.md#libpq-pqclientencoding) 來確定。

<a id="LIBPQ-PQSETERRORVERBOSITY"></a>

### `PQsetErrorVerbosity`<a id="id-1.7.3.18.3.3.1.2"></a> [#](#libpq-pqseterrorverbosity) <a href="#libpq-pqseterrorverbosity" id="libpq-pqseterrorverbosity"></a>

決定 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 與 [`PQresultErrorMessage`](libpq-exec-main.md#libpq-pqresulterrormessage) 所傳回訊息的詳細程度。

```

    typedef enum
    {
        PQERRORS_TERSE,
        PQERRORS_DEFAULT,
        PQERRORS_VERBOSE,
        PQERRORS_SQLSTATE
    } PGVerbosity;

    PGVerbosity PQsetErrorVerbosity(PGconn *conn, PGVerbosity verbosity);
```

[`PQsetErrorVerbosity`](libpq-control.md#libpq-pqseterrorverbosity) 會設定詳細程度模式，並傳回該連線先前的設定。在 *TERSE* 模式下，傳回的訊息只包含嚴重性、主要文字與位置；這通常可以容納在單一行中。*DEFAULT* 模式產生的訊息包含上述內容，再加上任何詳細資訊（detail）、提示（hint）或上下文（context）欄位（這些可能跨越多行）。*VERBOSE* 模式包含所有可用的欄位。*SQLSTATE* 模式只包含錯誤嚴重性與 `SQLSTATE` 錯誤代碼（如果有的話；若沒有，輸出就和 *TERSE* 模式相同）。

變更詳細程度設定不會影響已經存在的 `PGresult` 物件中可取得的訊息，只會影響之後建立的物件。（但如果你想以不同的詳細程度印出先前的錯誤，請參閱 [`PQresultVerboseErrorMessage`](libpq-exec-main.md#libpq-pqresultverboseerrormessage)。）

<a id="LIBPQ-PQSETERRORCONTEXTVISIBILITY"></a>

### `PQsetErrorContextVisibility`<a id="id-1.7.3.18.3.4.1.2"></a> [#](#libpq-pqseterrorcontextvisibility) <a href="#libpq-pqseterrorcontextvisibility" id="libpq-pqseterrorcontextvisibility"></a>

決定 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 與 [`PQresultErrorMessage`](libpq-exec-main.md#libpq-pqresulterrormessage) 所傳回訊息中 `CONTEXT` 欄位的處理方式。

```

    typedef enum
    {
        PQSHOW_CONTEXT_NEVER,
        PQSHOW_CONTEXT_ERRORS,
        PQSHOW_CONTEXT_ALWAYS
    } PGContextVisibility;

    PGContextVisibility PQsetErrorContextVisibility(PGconn *conn, PGContextVisibility show_context);
```

[`PQsetErrorContextVisibility`](libpq-control.md#libpq-pqseterrorcontextvisibility) 會設定上下文（context）顯示模式，並傳回該連線先前的設定。此模式控制訊息中是否包含 `CONTEXT` 欄位。*NEVER* 模式永遠不包含 `CONTEXT`，而 *ALWAYS* 模式則只要有就一律包含。在 *ERRORS* 模式（預設值）下，`CONTEXT` 欄位只包含在錯誤訊息中，不包含在通知訊息與警告中。（不過，若詳細程度設定為 *TERSE* 或 *SQLSTATE*，則不論上下文顯示模式為何，都會省略 `CONTEXT` 欄位。）

變更此模式不會影響已經存在的 `PGresult` 物件中可取得的訊息，只會影響之後建立的物件。（但如果你想以不同的顯示模式印出先前的錯誤，請參閱 [`PQresultVerboseErrorMessage`](libpq-exec-main.md#libpq-pqresultverboseerrormessage)。）

<a id="LIBPQ-PQTRACE"></a>

### `PQtrace`<a id="id-1.7.3.18.3.5.1.2"></a> [#](#libpq-pqtrace) <a href="#libpq-pqtrace" id="libpq-pqtrace"></a>

啟用用戶端／伺服器通訊的追蹤，輸出到除錯用的檔案串流。

```

    void PQtrace(PGconn *conn, FILE *stream);
```

每一行依序包含：選擇性的時間戳記、方向指示（`F` 表示從用戶端送往伺服器的訊息，`B` 表示從伺服器送往用戶端的訊息）、訊息長度、訊息類型，以及訊息內容。非訊息內容的欄位（時間戳記、方向、長度與訊息類型）以定位字元（tab）分隔。訊息內容以空格分隔。協定字串以雙引號括住，而作為資料值的字串則以單引號括住。無法列印的字元會以十六進位跳脫序列印出。各訊息類型的進一步細節可在[第 54.7 節](../../internals/protocol/protocol-message-formats.md)中找到。

#### 注意

在 Windows 上，如果 libpq 函式庫與應用程式是以不同的旗標編譯，呼叫此函式會使應用程式當掉，因為 `FILE` 指標的內部表示方式不同。具體而言，函式庫與所有使用該函式庫的應用程式，其多執行緒／單執行緒、發行／除錯（release/debug） 以及靜態／動態旗標都應該相同。

<a id="LIBPQ-PQSETTRACEFLAGS"></a>

### `PQsetTraceFlags`<a id="id-1.7.3.18.3.6.1.2"></a> [#](#libpq-pqsettraceflags) <a href="#libpq-pqsettraceflags" id="libpq-pqsettraceflags"></a>

控制用戶端／伺服器通訊的追蹤行為。

```

    void PQsetTraceFlags(PGconn *conn, int flags);
```

`flags` 包含描述追蹤運作模式的旗標位元。若 `flags` 包含 `PQTRACE_SUPPRESS_TIMESTAMPS`，則印出每則訊息時不會包含時間戳記。若 `flags` 包含 `PQTRACE_REGRESS_MODE`，則印出每則訊息時會遮蔽某些欄位（例如物件 OID），讓輸出更便於在測試框架中使用。此函式必須在呼叫 `PQtrace` 之後呼叫。

<a id="LIBPQ-PQUNTRACE"></a>

### `PQuntrace`<a id="id-1.7.3.18.3.7.1.2"></a> [#](#libpq-pquntrace) <a href="#libpq-pquntrace" id="libpq-pquntrace"></a>

停用由 [`PQtrace`](libpq-control.md#libpq-pqtrace) 啟動的追蹤。

```

    void PQuntrace(PGconn *conn);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-control.html)（原文版本：18.6；核對日期：2026-10-18）
