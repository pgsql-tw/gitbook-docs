<a id="APP-PGCOMBINEBACKUP"></a><a id="id-1.9.4.12.1"></a>

## pg_combinebackup

pg_combinebackup — 從增量備份及其相依的備份重建完整備份

<a id="id-1.9.4.12.4"></a>

## 語法

<a id="id-1.9.4.12.4.1"></a>

`pg_combinebackup` [*`option`*...] [*`backup_directory`*...]

<a id="id-1.9.4.12.5"></a>

## 說明

pg_combinebackup 用來從一個[增量備份](../../server-administration/backup/continuous-archiving.md#backup-incremental-backup)及其所相依的較早備份，重建出一份合成的完整備份。

請在命令列上依照由舊到新的順序指定所有需要的備份。也就是說，第一個備份目錄應該是完整備份的路徑，最後一個則應該是你想要還原的最終增量備份的路徑。重建後的備份會寫入 `-o` 選項所指定的輸出目錄。

pg_combinebackup 會嘗試驗證你所指定的備份是否構成合法的備份鏈，足以從中重建出正確的完整備份。不過，它的設計並不是要幫你追蹤哪些備份相依於哪些其他備份。如果你移除了增量備份所依賴的一個或多個先前備份，你將無法還原該增量備份。此外，pg_combinebackup 只會嘗試驗證這些備份彼此之間的關係是否正確，而不會驗證每一個個別備份是否完好；若要驗證這一點，請使用 [pg_verifybackup](app-pgverifybackup.md)。

由於 pg_combinebackup 的輸出是一份合成的完整備份，它可以作為之後呼叫 pg_combinebackup 時的輸入。此時會在命令列上指定該合成的完整備份，以取代重建它時所用的備份鏈。

<a id="id-1.9.4.12.6"></a>

## 選項

`-d`<br>`--debug`
:   在 `stderr` 上印出大量的除錯日誌輸出。

`-k`<br>`--link`

使用硬連結，而不是將檔案複製到合成的備份中。重建合成備份的速度可能會比較快（不需複製檔案），也會使用較少的磁碟空間，但使用輸出目錄時必須小心，因為對該目錄的任何修改（例如啟動伺服器）也可能影響輸入目錄。同樣地，對輸入目錄的變更（例如在完整備份上啟動伺服器）也可能影響輸出目錄。因此，此選項最適合在輸入目錄只是副本、且會在 pg_combinebackup 完成後移除的情況下使用。

此選項要求輸入備份與輸出目錄位於同一個檔案系統中。

若沒有可用的備份清單（manifest），或備份清單中不包含正確類型的檢查碼，仍會建立硬連結，但也會逐區塊讀取檔案以計算檢查碼。

`-n`<br>`--dry-run`
:   `-n`/`--dry-run` 選項會指示 `pg_combinebackup` 推算出將會執行哪些動作，而不實際建立目標目錄或任何輸出檔案。此選項與 `--debug` 一起使用時特別有用。

`-N`<br>`--no-sync`
:   預設情況下，`pg_combinebackup` 會等待所有檔案都安全寫入磁碟。此選項會讓 `pg_combinebackup` 不等待就返回，這樣比較快，但意味著之後的作業系統當機可能會使輸出的備份損毀。一般而言，此選項適用於測試，但不應該在建立正式環境的安裝時使用。

`-o outputdir`<br>`--output=outputdir`
:   指定合成的完整備份應寫入的輸出目錄。目前此引數為必要。

`-T olddir=newdir`<br>`--tablespace-mapping=olddir=newdir`
:   在備份期間，將位於目錄 *`olddir`* 的資料表空間重新放置到 *`newdir`*。*`olddir`* 是該資料表空間在命令列上所指定之最終備份中的絕對路徑，而 *`newdir`* 是重建後的備份中該資料表空間要使用的絕對路徑。若任一路徑需要包含等號（`=`），請在等號前加上反斜線。此選項可以為多個資料表空間指定多次。

`--clone`

使用有效率的檔案複製（clone，在某些系統上也稱為「reflinks」），而不是將檔案複製（copy）到新的資料目錄。這可以讓資料檔案的複製幾乎在瞬間完成。

若沒有可用的備份清單，或備份清單中不包含正確類型的檢查碼，會使用檔案複製（clone）來複製檔案，但也會逐區塊讀取檔案以計算檢查碼。

只有部分作業系統與檔案系統支援檔案複製（clone）。如果選擇了此選項但系統不支援，pg_combinebackup 的執行將會發生錯誤。目前，支援的環境有 Linux（核心 4.5 或更新版本）上的 Btrfs 與 XFS（在建立時啟用 reflink 支援的檔案系統上），以及 macOS 上的 APFS。

`--copy`
:   執行一般的檔案複製。這是預設行為。（另請參閱 `--copy-file-range`、`--clone` 與 `-k`/`--link`。）

`--copy-file-range`

使用 `copy_file_range` 系統呼叫進行有效率的複製。在某些檔案系統上，這會產生與 `--clone` 類似的結果，共用實體磁碟區塊；而在其他檔案系統上，它可能仍會複製區塊，但會透過最佳化的路徑來進行。目前，Linux 與 FreeBSD 支援此選項。

若沒有可用的備份清單，或備份清單中不包含正確類型的檢查碼，會使用 `copy_file_range` 來複製檔案，但也會逐區塊讀取檔案以計算檢查碼。

`--manifest-checksums=algorithm`
:   與 [pg_basebackup](app-pgbasebackup.md) 一樣，pg_combinebackup 會在輸出目錄中寫入備份清單。此選項指定應該套用於備份清單所含之每個檔案的檢查碼演算法。目前可用的演算法有 `NONE`、`CRC32C`、`SHA224`、`SHA256`、`SHA384` 與 `SHA512`。預設為 `CRC32C`。

`--no-manifest`
:   停用備份清單的產生。若未指定此選項，重建後備份的備份清單會寫入輸出目錄。

`--sync-method=method`

設為預設值 `fsync` 時，`pg_combinebackup` 會遞迴地開啟並同步備份目錄中的所有檔案。使用 plain 格式時，搜尋檔案會跟隨 WAL 目錄與每個已設定之資料表空間的符號連結。

在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含備份目錄的整個檔案系統。使用 plain 格式時，`pg_combinebackup` 也會同步包含 WAL 檔案與每個資料表空間的檔案系統。關於使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

使用 `--no-sync` 時，此選項沒有作用。

`-V`<br>`--version`
:   印出 pg_combinebackup 的版本後結束。

`-?`<br>`--help`
:   顯示 pg_combinebackup 命令列引數的說明後結束。

<a id="APP-PGCOMBINEBACKUP-LIMITATIONS"></a>

## 限制

`pg_combinebackup` 在寫入輸出目錄時，不會重新計算頁面檢查碼。因此，如果用於重建的任何備份是在停用檢查碼時取得的，而最終備份是在啟用檢查碼時取得的，產生的目錄可能會包含檢查碼無效的頁面。

為了避免此問題，建議在使用 [pg_checksums](../reference-server/app-pgchecksums.md) 變更叢集的檢查碼狀態之後，取得一份新的完整備份。否則，你可以對 `pg_combinebackup` 所產生的目錄先停用檢查碼，再視需要重新啟用檢查碼，以修正此問題。

<a id="id-1.9.4.12.8"></a>

## 環境

此工具程式與大多數其他 PostgreSQL 工具程式一樣，會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.12.9"></a>

## 另請參閱

[pg_basebackup](app-pgbasebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgcombinebackup.html)（原文版本：18.6；核對日期：2026-10-09）
