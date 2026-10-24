<a id="LIBPQ-OAUTH"></a>

## 32.20. OAuth 支援 [#](#libpq-oauth) <a href="#libpq-oauth" id="libpq-oauth"></a>

[32.20.1. 認證資料（authdata）掛鉤](libpq-oauth.md#libpq-oauth-authdata-hooks)

[32.20.2. 除錯與開發者設定](libpq-oauth.md#libpq-oauth-debugging)

libpq 以選用模組的形式，實作了對 OAuth v2 裝置授權（Device Authorization）用戶端流程的支援，
該流程記載於
[RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)。
關於如何啟用以裝置授權作為內建流程的支援，請參閱[安裝說明文件](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)。

啟用支援並安裝選用模組後，若伺服器在認證期間
[要求持有者權杖（bearer token）](../../server-administration/client-authentication/auth-oauth.md)，
libpq 預設會使用內建流程。即使執行
用戶端應用程式的系統沒有可用的網頁瀏覽器，例如
透過 SSH 執行用戶端時，也可以使用此流程。

預設情況下，內建流程會印出一個要造訪的 URL，以及要在該處輸入的使用者代碼：

```

$ psql 'dbname=postgres oauth_issuer=https://example.com oauth_client_id=...'
Visit https://example.com/device and enter the code: ABCD-EFGH
```

（此提示可以
[自訂](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE)。）
接著，使用者會登入其 OAuth 提供者，提供者會詢問是否
允許 libpq 與伺服器代表使用者執行操作。在繼續之前，
仔細檢查所顯示的 URL 與權限，確認它們符合預期，
永遠是個好主意。不應該將權限授予
不受信任的第三方。

用戶端應用程式可以實作自己的流程，以自訂互動方式
以及與應用程式的整合。關於如何將自訂流程加入 libpq，
詳細資訊請參閱[第 32.20.1 節](libpq-oauth.md#libpq-oauth-authdata-hooks)。

OAuth 用戶端流程若要可用，連線字串至少必須
包含 [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) 與
[oauth_client_id](libpq-connect.md#LIBPQ-CONNECT-OAUTH-CLIENT-ID)。（這些設定
由你組織的 OAuth 提供者決定。）內建流程
另外還要求 OAuth 授權伺服器發佈裝置
授權端點。

### 注意

內建的裝置授權流程目前不支援 Windows。
仍然可以實作自訂的用戶端流程。

<a id="LIBPQ-OAUTH-AUTHDATA-HOOKS"></a>

### 32.20.1. 認證資料（authdata）掛鉤 [#](#libpq-oauth-authdata-hooks) <a href="#libpq-oauth-authdata-hooks" id="libpq-oauth-authdata-hooks"></a>

用戶端可以使用下列掛鉤 API 修改或取代
OAuth 流程的行為：

<a id="LIBPQ-PQSETAUTHDATAHOOK"></a>

`PQsetAuthDataHook`<a id="id-1.7.3.27.8.2.1.1.1.2"></a> [#](#LIBPQ-PQSETAUTHDATAHOOK)
:   設定 `PGauthDataHook`，覆寫
    libpq 對其 OAuth 用戶端流程中
    一個或多個面向的處理。

    ```

    void PQsetAuthDataHook(PQauthDataHook_type hook);
    ```

    若 *`hook`* 為 `NULL`，將
    重新安裝預設的處理函式。否則，應用程式會傳入
    一個指向回呼函式的指標，其簽章為：

    ```

    int hook_fn(PGauthData type, PGconn *conn, void *data);
    ```

    libpq 會在需要應用程式採取動作時
    呼叫它。*`type`* 描述
    所提出的請求，*`conn`* 是
    正在進行認證的連線控制代碼，*`data`*
    則指向該請求特有的中繼資料。此指標的內容
    由 *`type`* 決定；支援的清單請參閱
    [第 32.20.1.1 節](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES)。

    掛鉤可以串接在一起，以實現協同及／或備援（fallback）
    行為。一般而言，掛鉤實作應該檢查傳入的
    *`type`*（以及可能的請求中繼資料
    及／或所使用之特定 *`conn`*
    的設定），以決定是否處理某一項特定的認證資料（authdata）。
    若不處理，則應該委派給鏈中的前一個掛鉤
    （可透過 `PQgetAuthDataHook` 取得）。

    傳回大於零的整數表示成功。
    傳回負整數表示發生錯誤狀況，並放棄
    此次連線嘗試。（零值保留給預設
    實作使用。）
<a id="LIBPQ-PQGETAUTHDATAHOOK"></a>

`PQgetAuthDataHook`<a id="id-1.7.3.27.8.2.1.2.1.2"></a> [#](#LIBPQ-PQGETAUTHDATAHOOK)
:   取得 `PGauthDataHook` 目前的值。

    ```

    PQauthDataHook_type PQgetAuthDataHook(void);
    ```

    在初始化時（第一次呼叫
    `PQsetAuthDataHook` 之前），此函式會傳回
    `PQdefaultAuthDataHook`。

<a id="LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES"></a>

#### 32.20.1.1. 掛鉤類型 [#](#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES)

已定義下列 `PGauthData` 類型及其對應的
*`data`* 結構：

<a id="LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE"></a>

`PQAUTHDATA_PROMPT_OAUTH_DEVICE` <a id="id-1.7.3.27.8.3.2.3.1.1.2"></a> [#](#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE)
:   在內建裝置授權用戶端流程中取代預設的使用者提示。
    *`data`* 指向
    一個 `PGpromptOAuthDevice` 實例：

    ```

    typedef struct _PGpromptOAuthDevice
    {
        const char *verification_uri;   /* verification URI to visit */
        const char *user_code;          /* user code to enter */
        const char *verification_uri_complete;  /* optional combination of URI and
                                                 * code, or NULL */
        int         expires_in;         /* seconds until user code expires */
    } PGpromptOAuthDevice;
    ```

    [可以包含](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)
    在 libpq 中的 OAuth 裝置授權流程，
    要求終端使用者以瀏覽器造訪某個 URL，然後輸入一組代碼，
    以允許 libpq 代表他們連線到伺服器。
    預設提示只是將
    `verification_uri` 與 `user_code`
    印到標準錯誤輸出。替代實作可以使用任何偏好的方式
    顯示此資訊，例如透過 GUI。

    此回呼函式只會在內建裝置
    授權流程中被呼叫。若應用程式安裝了
    [自訂 OAuth
    流程](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN)，或 libpq 建置時
    未支援內建流程，就不會使用此認證資料類型。

    若提供了非 NULL 的 `verification_uri_complete`，
    可以選擇性地將它用於非文字形式的驗證（例如
    顯示 QR code）。在這種情況下，仍然應該
    向終端使用者顯示 URL 與使用者代碼，因為該代碼
    會在提供者端以人工方式確認，而 URL 讓使用者即使
    無法使用非文字方法時也能繼續。詳細資訊
    請參閱
    [RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628#section-3.3.1) 的第 3.3.1 節。
<a id="LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN"></a>

`PQAUTHDATA_OAUTH_BEARER_TOKEN` <a id="id-1.7.3.27.8.3.2.3.2.1.2"></a> [#](#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN)
:   加入流程的自訂實作；若已[安裝](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)內建流程，
    則會取代內建流程。
    掛鉤應該在不阻塞即可取得權杖時，直接傳回目前
    使用者／核發者／範圍組合的持有者權杖（Bearer token）；
    否則就設定一個非同步回呼函式來取得權杖。

    *`data`* 指向一個
    `PGoauthBearerRequest` 實例，應由
    實作填入內容：

    ```

    typedef struct PGoauthBearerRequest
    {
        /* Hook inputs (constant across all calls) */
        const char *openid_configuration; /* OIDC discovery URL */
        const char *scope;                /* required scope(s), or NULL */

        /* Hook outputs */

        /*
         * Callback implementing a custom asynchronous OAuth flow. The signature is
         * platform-dependent: PQ_SOCKTYPE is SOCKET on Windows, and int everywhere
         * else.
         */
        PostgresPollingStatusType (*async) (PGconn *conn,
                                            struct PGoauthBearerRequest *request,
                                            PQ_SOCKTYPE *altsock);

        /* Callback to clean up custom allocations. */
        void        (*cleanup) (PGconn *conn, struct PGoauthBearerRequest *request);

        char       *token;   /* acquired Bearer token */
        void       *user;    /* hook-defined allocated data */
    } PGoauthBearerRequest;
    ```

    libpq 會提供兩項資訊給
    掛鉤：
    *`openid_configuration`* 包含一份
    OAuth 發現文件的 URL，該文件描述授權伺服器
    所支援的流程；*`scope`* 則包含
    存取伺服器所需的 OAuth 範圍（scope）清單，
    以空白分隔（可能為空）。兩者之一或兩者都可能為
    `NULL`，表示無法探查到該資訊。
    （在此情況下，實作或許能使用其他
    預先設定的知識確立需求，也可能
    選擇失敗。）

    掛鉤的最終輸出是 *`token`*，它
    必須指向可用於此連線的有效持有者權杖。（此
    權杖應該由
    [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) 核發，並具備所請求的
    範圍，否則連線將被伺服器的驗證器
    模組拒絕。）配置的權杖字串必須在
    libpq 完成連線之前保持有效；掛鉤
    應該設定一個 *`cleanup`* 回呼函式，在
    libpq 不再需要該字串時被呼叫。

    若實作無法在初次呼叫掛鉤時立即產生
    *`token`*，
    則應該設定 *`async`* 回呼函式，以處理
    與授權伺服器之間的非阻塞通訊。
    [<a id="id-1.7.3.27.8.3.2.3.2.2.5.3"></a>[16]](#ftn.id-1.7.3.27.8.3.2.3.2.2.5.3)
    此回呼函式會在掛鉤返回後立即被呼叫，以開始流程。
    當回呼函式無法在不阻塞的情況下繼續進行時，
    應該先將
    `*altsock` 設為在可以再次進行時會被標示為
    可讀取／可寫入的檔案描述子，然後傳回
    `PGRES_POLLING_READING` 或
    `PGRES_POLLING_WRITING`。（此描述子
    接著會透過
    `PQsocket()` 提供給最上層的輪詢迴圈。）流程完成時，
    在設定 *`token`* 之後傳回 `PGRES_POLLING_OK`；
    或傳回 `PGRES_POLLING_FAILED` 表示失敗。

    實作可能會想要在多次呼叫 *`async`* 與
    *`cleanup`* 回呼函式之間，儲存額外的資料以供
    記錄管理。
    *`user`* 指標即為此用途而提供；
    libpq 不會碰觸其內容，
    應用程式可以依自己的方便使用。（請記得在權杖
    清理時釋放所有配置的記憶體。）

<a id="LIBPQ-OAUTH-DEBUGGING"></a>

### 32.20.2. 除錯與開發者設定 [#](#libpq-oauth-debugging) <a href="#libpq-oauth-debugging" id="libpq-oauth-debugging"></a>

可以透過設定環境變數 `PGOAUTHDEBUG=UNSAFE` 啟用
「危險的除錯模式」。此功能僅為了方便
本機開發與測試而提供。它會做幾件
你不會希望正式環境系統做的事：

* 允許在與 OAuth 提供者交換資料時使用未加密的 HTTP
* 允許使用 `PGOAUTHCAFILE` 環境變數
  完全取代系統信任的 CA 清單
* 在 OAuth 流程期間，將 HTTP 流量（其中包含數個關鍵祕密）
  印到標準錯誤輸出
* 允許使用零秒的重試間隔，這可能導致
  用戶端陷入忙碌迴圈（busy-loop），無謂地耗用 CPU

### 警告

不要將 OAuth 流程流量的輸出分享給第三方。
其中包含可用來攻擊你的用戶端與伺服器的祕密。

<br>

---

<a id="ftn.id-1.7.3.27.8.3.2.3.2.2.5.3"></a>

[[16]](#id-1.7.3.27.8.3.2.3.2.2.5.3) 
在 `PQAUTHDATA_OAUTH_BEARER_TOKEN` 掛鉤回呼函式中
執行阻塞操作，會干擾
`PQconnectPoll` 等非阻塞連線 API，並使並行的連線
無法繼續進行。只會使用
同步連線基本函式的應用程式，例如
`PQconnectdb`，可以在掛鉤中同步取得權杖，
而不必實作
*`async`* 回呼函式，但它們必然
會被限制為一次只能有一個連線。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-oauth.html)（原文版本：18.6；核對日期：2026-10-17）
