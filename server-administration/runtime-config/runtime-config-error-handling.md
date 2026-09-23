<a id="RUNTIME-CONFIG-ERROR-HANDLING"></a>

## 19.14. 錯誤處理 [#](#RUNTIME-CONFIG-ERROR-HANDLING)

<a id="GUC-EXIT-ON-ERROR"></a>

`exit_on_error`（`boolean`） <a id="id-1.6.6.17.2.1.1.3"></a> [#](#GUC-EXIT-ON-ERROR)
:   若設為 on，任何錯誤，都會終止目前的工作階段。
    依預設，此值設為 off，因此只有 FATAL 等級的錯誤，
    才會終止工作階段。
<a id="GUC-RESTART-AFTER-CRASH"></a>

`restart_after_crash`（`boolean`） <a id="id-1.6.6.17.2.2.1.3"></a> [#](#GUC-RESTART-AFTER-CRASH)
:   當設為 on（此為預設值）時，PostgreSQL
    會在後端當機之後，自動重新初始化。將此值保持設為 on，
    通常是將資料庫可用性最大化的最佳方式。不過，
    在某些情況下，例如當 PostgreSQL
    是由叢集軟體（clusterware）呼叫時，
    停用自動重新啟動或許會有幫助，
    如此一來，叢集軟體就能取得控制權，
    並採取其認為適當的任何動作。

    此參數只能在 `postgresql.conf` 檔案中，
    或於伺服器命令列上設定。
<a id="GUC-DATA-SYNC-RETRY"></a>

`data_sync_retry`（`boolean`） <a id="id-1.6.6.17.2.3.1.3"></a> [#](#GUC-DATA-SYNC-RETRY)
:   當設為 off（此為預設值）時，若無法將已修改的資料檔案，
    排清至檔案系統，PostgreSQL 會引發一個
    PANIC 等級的錯誤。這會導致資料庫伺服器當機。
    此參數只能在伺服器啟動時設定。

    在某些作業系統上，寫回（write-back）失敗之後，
    核心分頁快取中資料的狀態，是未知的。在某些情況下，
    該資料可能已經完全遺失，導致重試並不安全；
    第二次嘗試，可能會被回報為成功，但實際上資料已經遺失。
    在這種情況下，唯一能避免資料遺失的方式，
    就是在任何失敗被回報之後，從 WAL 復原，
    最好是在調查失敗的根本原因、並更換任何故障硬體之後，
    再進行復原。

    若設為 on，PostgreSQL 則會改為回報一個錯誤，
    但仍繼續執行，讓資料排清操作，
    能在稍後的某次檢查點中重試。只有在調查過
    作業系統在寫回失敗時對緩衝資料的處理方式之後，
    才應將此值設為 on。
<a id="GUC-RECOVERY-INIT-SYNC-METHOD"></a>

`recovery_init_sync_method`（`enum`） <a id="id-1.6.6.17.2.4.1.3"></a> [#](#GUC-RECOVERY-INIT-SYNC-METHOD)
:   當設為 `fsync`（此為預設值）時，
    PostgreSQL 會在當機復原開始之前，
    遞迴地開啟並同步資料目錄中的所有檔案。
    搜尋檔案時，會沿著 WAL 目錄與每個已設定資料表空間的
    符號連結進行（但不會沿著任何其他符號連結）。
    這麼做的目的，是確保在重播變更之前，
    所有 WAL 與資料檔案，都已耐久地儲存於磁碟上。
    每當啟動一個未正常關閉的資料庫叢集時
    （包括以 pg_basebackup 建立的複本），都會套用此設定。

    在 Linux 上，也可以改用 `syncfs`，
    要求作業系統同步包含資料目錄、WAL 檔案
    與各個資料表空間的檔案系統（但不包括其他任何
    可能透過符號連結存取到的檔案系統）。
    由於它不需要逐一開啟每個檔案，這可能會比
    `fsync` 設定快上許多。另一方面，
    若某個檔案系統，同時被其他會修改大量檔案的應用程式共用，
    此設定可能反而較慢，因為那些檔案也會被寫入磁碟。
    此外，在 5.8 之前的 Linux 版本上，
    寫入資料至磁碟時所發生的 I/O 錯誤，
    可能不會回報給 PostgreSQL，
    相關的錯誤訊息，可能只會出現在核心日誌中。

    此參數只能在 `postgresql.conf` 檔案中，
    或於伺服器命令列上設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-error-handling.html)（原文版本：18.6；核對日期：2026-09-22）
