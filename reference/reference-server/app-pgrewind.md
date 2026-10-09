<a id="APP-PGREWIND"></a><a id="id-1.9.5.10.1"></a>

## pg_rewind

pg_rewind — 將 PostgreSQL 資料目錄與另一個從它分岔出去的資料目錄同步

## 語法

<a id="id-1.9.5.10.4.1"></a>

`pg_rewind` [*`option`*...] { `-D` | `--target-pgdata` } *`directory`* { `--source-pgdata=directory` | `--source-server=connstr` }

<a id="id-1.9.5.10.5"></a>

## 說明

pg_rewind 是一個工具，用於在叢集的時間軸分歧之後，將 PostgreSQL 叢集與同一叢集的另一份副本同步。典型的情境是在容錯移轉之後，讓舊的主要伺服器重新上線，成為跟隨新主要伺服器的待命伺服器。

倒轉（rewind）成功之後，目標資料目錄的狀態類似於來源資料目錄的基礎備份。與製作新的基礎備份或使用 rsync 之類的工具不同，pg_rewind 不需要比對或複製叢集中未變更的關聯區塊。只有現有關聯檔案中已變更的區塊會被複製；所有其他檔案，包括新的關聯檔案、設定檔與 WAL 區段，都會完整複製。因此，當資料庫很大、而叢集之間只有一小部分區塊不同時，倒轉操作會比其他做法快得多。

pg_rewind 會檢查來源叢集與目標叢集的時間軸歷史，以判定兩者分歧的時間點，並預期能在目標叢集的 `pg_wal` 目錄中找到一路回溯到分歧點的 WAL。分歧點可能位於目標時間軸、來源時間軸，或兩者的共同祖先上。在典型的容錯移轉情境中，目標叢集在分歧後不久就已關閉，這不是問題；但如果目標叢集在分歧後又執行了很長一段時間，它的舊 WAL 檔案可能已經不存在。在這種情況下，你可以手動將它們從 WAL 歸檔複製到 `pg_wal` 目錄，或是以 `-c` 選項執行 pg_rewind，自動從 WAL 歸檔取回它們。pg_rewind 的用途並不限於容錯移轉，例如，待命伺服器可以被提升、執行一些寫入交易，然後再倒轉回來重新成為待命伺服器。

執行 pg_rewind 之後，需要完成 WAL 重播，資料目錄才會處於一致的狀態。目標伺服器再次啟動時，會進入歸檔復原，並重播來源伺服器中從分歧點之前最後一個檢查點起所產生的所有 WAL。如果執行 pg_rewind 時，來源伺服器中已有部分 WAL 無法取得，因而無法由 pg_rewind 工作階段複製，則必須在目標伺服器啟動時讓這些 WAL 可供使用。做法是在目標資料目錄中建立 `recovery.signal` 檔案，並在 `postgresql.conf` 中設定適當的 [restore_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND)。

pg_rewind 要求目標伺服器在 `postgresql.conf` 中啟用 [wal_log_hints](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LOG-HINTS) 選項，或是在以 initdb 初始化叢集時啟用了資料檢查碼（這是預設值）。[full_page_writes](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES) 也必須設為 `on`，不過它預設就是啟用的。

<a id="id-1.9.5.10.5.7"></a>

### 警告：倒轉過程中的失敗

如果 pg_rewind 在處理過程中失敗，目標的資料資料夾很可能處於無法復原的狀態。在這種情況下，建議重新製作一份新的備份。

由於 pg_rewind 會從來源完整複製設定檔，因此在重新啟動目標伺服器之前，可能需要修正用於復原的設定，特別是當目標被重新引入為來源的待命伺服器時。如果你在倒轉操作完成後重新啟動伺服器，但沒有設定復原，目標可能會再次與主要伺服器分歧。

如果 pg_rewind 發現有它無法直接寫入的檔案，就會立即失敗。例如，當來源與目標伺服器對唯讀的 SSL 金鑰與憑證使用相同的檔案對應時，就可能發生這種情況。如果目標伺服器上存在這類檔案，建議在執行 pg_rewind 之前將它們移除。完成倒轉之後，其中一些檔案可能已從來源複製過來，在這種情況下，可能需要移除複製過來的資料，並還原倒轉前所使用的那組連結。

<a id="id-1.9.5.10.6"></a>

## 選項

pg_rewind 接受下列命令列引數：

`-D directory`<br>`--target-pgdata=directory`
:   此選項指定要與來源同步的目標資料目錄。在執行 pg_rewind 之前，目標伺服器必須已正常關閉

`--source-pgdata=directory`
:   指定要用來同步目標之來源伺服器的資料目錄檔案系統路徑。此選項要求來源伺服器已正常關閉。

`--source-server=connstr`
:   指定 libpq 連線字串，用於連線到要用來同步目標的來源 PostgreSQL 伺服器。此連線必須是一般（非複寫）連線，所使用的角色須具有足夠權限來執行 pg_rewind 在來源伺服器上使用的函式（詳情請參閱注意事項一節），或是超級使用者角色。此選項要求來源伺服器正在執行並接受連線。

`-R`<br>`--write-recovery-conf`
:   建立 `standby.signal`，並將連線設定附加到輸出目錄中的 `postgresql.auto.conf`。只有在連線字串或[環境變數](../../client-interfaces/libpq/libpq-envars.md)中明確指定了 dbname 時，才會記錄 dbname。使用此選項時，`--source-server` 為必要。

`-n`<br>`--dry-run`
:   執行所有動作，但實際上不修改目標目錄。

`-N`<br>`--no-sync`
:   預設情況下，`pg_rewind` 會等待所有檔案都安全寫入磁碟。此選項會讓 `pg_rewind` 不等待就返回，這樣比較快，但意味著之後的作業系統當機可能會使資料目錄損毀。一般而言，此選項適用於測試，但不應該用於正式環境的安裝。

`-P`<br>`--progress`
:   啟用進度回報。開啟後，從來源叢集複製資料時會提供大約的進度報告。

`-c`<br>`--restore-target-wal`
:   如果 WAL 檔案在 `pg_wal` 目錄中已無法取得，則使用目標叢集設定中定義的 `restore_command` 從 WAL 歸檔取回這些檔案。

`--config-file=filename`
:   對目標叢集使用指定的主要伺服器設定檔。當 pg_rewind 在內部使用 postgres 命令對此叢集進行倒轉操作時（以 `-c/--restore-target-wal` 選項取得 `restore_command` 時，以及強制完成當機復原時），這會影響 pg_rewind。

`--debug`
:   印出詳細的除錯輸出，這主要對正在除錯 pg_rewind 的開發者有用。

`--no-ensure-shutdown`
:   pg_rewind 要求目標伺服器在倒轉之前已正常關閉。預設情況下，如果目標伺服器沒有正常關閉，pg_rewind 會以單一使用者模式啟動目標伺服器，先完成當機復原，然後再停止它。傳入此選項後，pg_rewind 會略過這個步驟，並在伺服器未正常關閉時立即以錯誤結束。在這種情況下，使用者應該自行處理該狀況。

`--sync-method=method`
:   設為預設值 `fsync` 時，`pg_rewind` 會遞迴地開啟並同步資料目錄中的所有檔案。搜尋檔案時會跟隨 WAL 目錄與每個已設定之資料表空間的符號連結。

    在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含資料目錄、WAL 檔案與每個資料表空間的整個檔案系統。關於使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

    使用 `--no-sync` 時，此選項沒有作用。

`-V`<br>`--version`
:   顯示版本資訊後結束。

`-?`<br>`--help`
:   顯示說明後結束。

<a id="id-1.9.5.10.7"></a>

## 環境

使用 `--source-server` 選項時，pg_rewind 也會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.10.8"></a>

## 注意事項

以線上叢集作為來源執行 pg_rewind 時，可以使用具有足夠權限、能執行 pg_rewind 在來源叢集上所用函式的角色，來取代超級使用者。以下示範如何建立這樣的角色，這裡命名為 `rewind_user`：

```

CREATE USER rewind_user LOGIN;
GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO rewind_user;
```

<a id="id-1.9.5.10.8.3"></a>

### 運作方式

基本概念是將來源叢集中所有檔案系統層級的變更複製到目標叢集：

1. 掃描目標叢集的 WAL 日誌，從來源叢集的時間軸歷史自目標叢集分岔出去之時間點前的最後一個檢查點開始。對每一筆 WAL 紀錄，記下每個被變動過的資料區塊。這會產生一份清單，列出在來源叢集分岔之後，目標叢集中所有被變更過的資料區塊。如果部分 WAL 檔案已無法取得，請嘗試以 `-c` 選項重新執行 pg_rewind，以便在 WAL 歸檔中搜尋缺少的檔案。
2. 將所有這些已變更的區塊從來源叢集複製到目標叢集，方式可以是直接存取檔案系統（`--source-pgdata`）或透過 SQL（`--source-server`）。此時，關聯檔案的狀態，相當於來源與目標之 WAL 時間軸分歧點之前最後一個已完成檢查點當下的狀態，再加上分歧之後在目標上被變更過之區塊在來源上的目前狀態。
3. 將所有其他檔案，包括新的關聯檔案、WAL 區段、`pg_xact` 與設定檔，從來源叢集複製到目標叢集。與基礎備份類似，目錄 `pg_dynshmem/`、`pg_notify/`、`pg_replslot/`、`pg_serial/`、`pg_snapshots/`、`pg_stat_tmp/` 與 `pg_subtrans/` 的內容不會包含在從來源叢集複製的資料中。檔案 `backup_label`、`tablespace_map`、`pg_internal.init`、`postmaster.opts`、`postmaster.pid` 與 `.DS_Store`，以及任何以 `pgsql_tmp` 開頭的檔案或目錄，也都會被略過。
4. 建立 `backup_label` 檔案，以便從容錯移轉時建立的檢查點開始 WAL 重播，並在 `pg_control` 檔案中設定最小一致性 LSN；從執行中的來源倒轉時，此值定義為 `pg_current_wal_insert_lsn()` 的結果，從已停止的來源倒轉時，則為最後一個檢查點的 LSN。
5. 啟動目標時，PostgreSQL 會重播所有必要的 WAL，使資料目錄處於一致的狀態。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgrewind.html)（原文版本：18.6；核對日期：2026-10-05）
