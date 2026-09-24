<a id="RUNTIME-CONFIG-PRESET"></a>

## 19.15. 預設選項 [#](#RUNTIME-CONFIG-PRESET)

以下這些「參數」皆為唯讀。
因此，這些參數已從範例
`postgresql.conf` 檔案中排除。這些選項回報
PostgreSQL 行為的各種面向，
可能會是某些應用程式，特別是管理前端所感興趣的資訊。
其中大部分是在編譯或安裝
PostgreSQL 時就已決定。

<a id="GUC-BLOCK-SIZE"></a>

`block_size` (`integer`) <a id="id-1.6.6.18.3.1.1.3"></a> [#](#GUC-BLOCK-SIZE)
:   回報磁碟區塊的大小。此值由建置伺服器時
    `BLCKSZ` 的值決定。預設值
    為 8192 位元組。某些組態變數（例如
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)）的意義
    會受到 `block_size` 影響。詳情請參閱[19.4 節](runtime-config-resource.md)。
<a id="GUC-DATA-CHECKSUMS"></a>

`data_checksums` (`boolean`) <a id="id-1.6.6.18.3.2.1.3"></a> [#](#GUC-DATA-CHECKSUMS)
:   回報此叢集是否已啟用資料檢查碼。
    詳情請參閱 [`-k`](../../reference/reference-server/app-initdb.md#APP-INITDB-DATA-CHECKSUMS)。
<a id="GUC-DATA-DIRECTORY-MODE"></a>

`data_directory_mode` (`integer`) <a id="id-1.6.6.18.3.3.1.3"></a> [#](#GUC-DATA-DIRECTORY-MODE)
:   在 Unix 系統上，此參數回報伺服器啟動時
    資料目錄（由 [data_directory](runtime-config-file-locations.md#GUC-DATA-DIRECTORY) 定義）
    所具有的權限。
    （在 Microsoft Windows 上，此參數永遠顯示為
    `0700`。）詳情請參閱
    [initdb 的
    `-g` 選項](../../reference/reference-server/app-initdb.md#APP-INITDB-ALLOW-GROUP-ACCESS)。
<a id="GUC-DEBUG-ASSERTIONS"></a>

`debug_assertions` (`boolean`) <a id="id-1.6.6.18.3.4.1.3"></a> [#](#GUC-DEBUG-ASSERTIONS)
:   回報 PostgreSQL 建置時是否
    啟用了斷言（assertion）。若在建置
    PostgreSQL 時定義了 `USE_ASSERT_CHECKING`
    巨集（例如透過
    `configure` 選項
    `--enable-cassert` 達成），則會是這種情況。
    預設情況下，PostgreSQL 是在不含
    斷言的狀態下建置的。
<a id="GUC-HUGE-PAGES-STATUS"></a>

`huge_pages_status` (`enum`) <a id="id-1.6.6.18.3.5.1.3"></a> [#](#GUC-HUGE-PAGES-STATUS)
:   回報目前實例中巨型分頁（huge page）的狀態：
    `on`、`off`，或
    `unknown`（若以
    `postgres -C` 顯示）。
    此參數可用於判斷在 `huge_pages=try` 之下
    巨型分頁的配置是否成功。
    詳情請參閱 [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES)。
<a id="GUC-INTEGER-DATETIMES"></a>

`integer_datetimes` (`boolean`) <a id="id-1.6.6.18.3.6.1.3"></a> [#](#GUC-INTEGER-DATETIMES)
:   回報 PostgreSQL 建置時是否支援
    64 位元整數的日期與時間。自 PostgreSQL 10 起，
    此值永遠為 `on`。
<a id="GUC-IN-HOT-STANDBY"></a>

`in_hot_standby` (`boolean`) <a id="id-1.6.6.18.3.7.1.3"></a> [#](#GUC-IN-HOT-STANDBY)
:   回報伺服器目前是否處於 hot standby 模式。當
    此值為 `on` 時，所有交易都會被強制設為
    唯讀。在單一工作階段內，只有當伺服器被
    提升（promote）為 primary 時，此值才能改變。詳情請參閱
    [26.4 節](../high-availability/hot-standby.md)。
<a id="GUC-MAX-FUNCTION-ARGS"></a>

`max_function_args` (`integer`) <a id="id-1.6.6.18.3.8.1.3"></a> [#](#GUC-MAX-FUNCTION-ARGS)
:   回報函式引數的最大數量。此值由建置伺服器時
    `FUNC_MAX_ARGS` 的值決定。預設值為 100 個引數。
<a id="GUC-MAX-IDENTIFIER-LENGTH"></a>

`max_identifier_length` (`integer`) <a id="id-1.6.6.18.3.9.1.3"></a> [#](#GUC-MAX-IDENTIFIER-LENGTH)
:   回報識別字的最大長度。此值由建置伺服器時
    `NAMEDATALEN` 的值減一決定。`NAMEDATALEN`
    的預設值為
    64；因此預設的
    `max_identifier_length` 為 63 位元組，
    在使用多位元組編碼時，字元數可能少於 63 個。
<a id="GUC-MAX-INDEX-KEYS"></a>

`max_index_keys` (`integer`) <a id="id-1.6.6.18.3.10.1.3"></a> [#](#GUC-MAX-INDEX-KEYS)
:   回報索引鍵值的最大數量。此值由建置伺服器時
    `INDEX_MAX_KEYS` 的值決定。預設值為 32 個鍵值。
<a id="GUC-NUM-OS-SEMAPHORES"></a>

`num_os_semaphores` (`integer`) <a id="id-1.6.6.18.3.11.1.3"></a> [#](#GUC-NUM-OS-SEMAPHORES)
:   根據所設定允許連線數
    （[max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)）、允許的 autovacuum 工作
    程序數（[autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)）、允許的 WAL
    傳送程序數（[max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）、允許的
    背景程序數（[max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)）等，
    回報伺服器所需的號誌（semaphore）數量。
<a id="GUC-SEGMENT-SIZE"></a>

`segment_size` (`integer`) <a id="id-1.6.6.18.3.12.1.3"></a> [#](#GUC-SEGMENT-SIZE)
:   回報一個檔案區段（segment）內可以儲存的區塊（頁面）數量。
    此值由建置伺服器時 `RELSEG_SIZE` 的值決定。
    區段檔案的最大位元組大小等於
    `segment_size` 乘以
    `block_size`；預設值為 1GB。
<a id="GUC-SERVER-ENCODING"></a>

`server_encoding` (`string`) <a id="id-1.6.6.18.3.13.1.3"></a> <a id="id-1.6.6.18.3.13.1.4"></a> [#](#GUC-SERVER-ENCODING)
:   回報資料庫編碼（字元集）。
    此值在建立資料庫時決定。通常，
    用戶端只需要關心 [client_encoding](runtime-config-client.md#GUC-CLIENT-ENCODING) 的值。
<a id="GUC-SERVER-VERSION"></a>

`server_version` (`string`) <a id="id-1.6.6.18.3.14.1.3"></a> [#](#GUC-SERVER-VERSION)
:   回報伺服器的版本號碼。此值由建置伺服器時
    `PG_VERSION` 的值決定。
<a id="GUC-SERVER-VERSION-NUM"></a>

`server_version_num` (`integer`) <a id="id-1.6.6.18.3.15.1.3"></a> [#](#GUC-SERVER-VERSION-NUM)
:   以整數形式回報伺服器的版本號碼。此值由建置伺服器時
    `PG_VERSION_NUM` 的值決定。
<a id="GUC-SHARED-MEMORY-SIZE"></a>

`shared_memory_size` (`integer`) <a id="id-1.6.6.18.3.16.1.3"></a> [#](#GUC-SHARED-MEMORY-SIZE)
:   回報主要共享記憶體區域的大小，並無條件進位到
    最接近的百萬位元組（MB）。
<a id="GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES"></a>

`shared_memory_size_in_huge_pages` (`integer`) <a id="id-1.6.6.18.3.17.1.3"></a> [#](#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES)
:   根據所指定的 [huge_page_size](runtime-config-resource.md#GUC-HUGE-PAGE-SIZE)，
    回報主要共享記憶體區域所需的巨型分頁數量。
    若不支援巨型分頁，此值會是 `-1`。

    此設定僅在 Linux 上受支援。在
    其他平台上，此值永遠為 `-1`。有關在 Linux 上使用
    巨型分頁的更多細節，請參閱
    [18.4.5 節](../runtime/kernel-resources.md#LINUX-HUGE-PAGES)。
<a id="GUC-SSL-LIBRARY"></a>

`ssl_library` (`string`) <a id="id-1.6.6.18.3.18.1.3"></a> [#](#GUC-SSL-LIBRARY)
:   回報建置此 PostgreSQL 伺服器時所使用的 SSL
    程式庫名稱（即使目前此實例並未設定或使用
    SSL），例如
    `OpenSSL`，若無則為空字串。
<a id="GUC-WAL-BLOCK-SIZE"></a>

`wal_block_size` (`integer`) <a id="id-1.6.6.18.3.19.1.3"></a> [#](#GUC-WAL-BLOCK-SIZE)
:   回報 WAL 磁碟區塊的大小。此值由建置伺服器時
    `XLOG_BLCKSZ` 的值決定。預設值
    為 8192 位元組。
<a id="GUC-WAL-SEGMENT-SIZE"></a>

`wal_segment_size` (`integer`) <a id="id-1.6.6.18.3.20.1.3"></a> [#](#GUC-WAL-SEGMENT-SIZE)
:   回報預寫日誌（write ahead log）區段的大小。預設值為
    16MB。詳情請參閱[28.5 節](../wal/wal-configuration.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-preset.html)（原文版本：18.6；核對日期：2026-09-24）
