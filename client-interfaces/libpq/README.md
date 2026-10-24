<a id="LIBPQ"></a>

## 第 32 章 libpq — C 函式庫

**目錄**

[32.1. 資料庫連線控制函式](libpq-connect.md)
:   [32.1.1. 連線字串](libpq-connect.md#libpq-connstring)

    [32.1.2. 參數關鍵字](libpq-connect.md#libpq-paramkeywords)

[32.2. 連線狀態函式](libpq-status.md)

[32.3. 命令執行函式](libpq-exec.md)
:   [32.3.1. 主要函式](libpq-exec.md#libpq-exec-main)

    [32.3.2. 取得查詢結果資訊](libpq-exec.md#libpq-exec-select-info)

    [32.3.3. 取得其他結果資訊](libpq-exec.md#libpq-exec-nonselect)

    [32.3.4. 跳脫要放入 SQL 命令中的字串](libpq-exec.md#libpq-exec-escape-string)

[32.4. 非同步命令處理](libpq-async.md)

[32.5. 管線模式](libpq-pipeline-mode.md)
:   [32.5.1. 使用管線模式](libpq-pipeline-mode.md#libpq-pipeline-using)

    [32.5.2. 與管線模式相關的函式](libpq-pipeline-mode.md#libpq-pipeline-functions)

    [32.5.3. 何時使用管線模式](libpq-pipeline-mode.md#libpq-pipeline-tips)

[32.6. 分塊取得查詢結果](libpq-single-row-mode.md)

[32.7. 取消進行中的查詢](libpq-cancel.md)
:   [32.7.1. 傳送取消請求的函式](libpq-cancel.md#libpq-cancel-functions)

    [32.7.2. 已過時的傳送取消請求函式](libpq-cancel.md#libpq-cancel-deprecated)

[32.8. 快速路徑介面](libpq-fastpath.md)

[32.9. 非同步通知](libpq-notify.md)

[32.10. 與 `COPY` 命令相關的函式](libpq-copy.md)
:   [32.10.1. 傳送 `COPY` 資料的函式](libpq-copy.md#libpq-copy-send)

    [32.10.2. 接收 `COPY` 資料的函式](libpq-copy.md#libpq-copy-receive)

    [32.10.3. 已過時的 `COPY` 函式](libpq-copy.md#libpq-copy-deprecated)

[32.11. 控制函式](libpq-control.md)

[32.12. 其他函式](libpq-misc.md)

[32.13. 通知訊息處理](libpq-notice-processing.md)

[32.14. 事件系統](libpq-events.md)
:   [32.14.1. 事件類型](libpq-events.md#libpq-events-types)

    [32.14.2. 事件回呼程序](libpq-events.md#libpq-events-proc)

    [32.14.3. 事件支援函式](libpq-events.md#libpq-events-funcs)

    [32.14.4. 事件範例](libpq-events.md#libpq-events-example)

[32.15. 環境變數](libpq-envars.md)

[32.16. 密碼檔](libpq-pgpass.md)

[32.17. 連線服務檔](libpq-pgservice.md)

[32.18. 以 LDAP 查詢連線參數](libpq-ldap.md)

[32.19. SSL 支援](libpq-ssl.md)
:   [32.19.1. 用戶端驗證伺服器憑證](libpq-ssl.md#libq-ssl-certificates)

    [32.19.2. 用戶端憑證](libpq-ssl.md#libpq-ssl-clientcert)

    [32.19.3. 不同模式所提供的保護](libpq-ssl.md#libpq-ssl-protection)

    [32.19.4. SSL 用戶端檔案用途](libpq-ssl.md#libpq-ssl-fileusage)

    [32.19.5. SSL 函式庫初始化](libpq-ssl.md#libpq-ssl-initialize)

[32.20. OAuth 支援](libpq-oauth.md)
:   [32.20.1. 認證資料（authdata）掛鉤](libpq-oauth.md#libpq-oauth-authdata-hooks)

    [32.20.2. 除錯與開發者設定](libpq-oauth.md#libpq-oauth-debugging)

[32.21. 多執行緒程式中的行為](libpq-threading.md)

[32.22. 建置 libpq 程式](libpq-build.md)

[32.23. 範例程式](libpq-example.md)

<a id="id-1.7.3.2"></a><a id="id-1.7.3.3"></a>

libpq 是 PostgreSQL 的 C
應用程式設計介面。
libpq 是一組函式庫函式，讓
用戶端程式能將查詢傳給 PostgreSQL
後端伺服器，並接收這些查詢的結果。

libpq 也是其他數個
PostgreSQL 應用程式介面的底層引擎，包括
為 C++、Perl、Python、Tcl 與 ECPG 所撰寫的介面。
因此，若你使用這些套件之一，libpq 行為的某些面向
對你而言會很重要。特別是，
[第 32.15 節](libpq-envars.md)、
[第 32.16 節](libpq-pgpass.md)與
[第 32.19 節](libpq-ssl.md)
說明了任何使用 libpq 之應用程式的使用者
都看得到的行為。

本章結尾收錄了一些簡短的程式（[第 32.23 節](libpq-example.md)），示範
如何撰寫使用 libpq 的程式。在原始碼發行版的
`src/test/examples` 目錄中，也有數個
完整的 libpq 應用程式範例。

使用 libpq 的用戶端程式必須
引入標頭檔
`libpq-fe.h`<a id="id-1.7.3.7.3"></a>，
並且必須與 libpq 函式庫連結。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq.html)（原文版本：18.6；核對日期：2026-10-18）
