<a id="APP-PGCHECKSUMS"></a><a id="id-1.9.5.5.1"></a>

## pg_checksums

pg_checksums — 在 PostgreSQL 資料庫叢集中啟用、停用或檢查資料校驗和

## 語法

<a id="id-1.9.5.5.4.1"></a>

`pg_checksums` [*`option`*...] [[ `-D` | `--pgdata` ]*`datadir`*]

<a id="R1-APP-PGCHECKSUMS-1"></a>

## 說明

pg_checksums 會檢查、啟用或停用 PostgreSQL 叢集中的資料校驗和。執行 pg_checksums 之前，伺服器必須已正常（clean）關閉。驗證校驗和時，若沒有校驗和錯誤，結束狀態為零；若偵測到至少一個校驗和失敗，結束狀態則為非零。啟用或停用校驗和時，若操作失敗，結束狀態為非零。

驗證校驗和時，會掃描叢集中的每一個檔案。啟用校驗和時，每個校驗和有變更的關聯檔案區塊都會被就地改寫。停用校驗和只會更新檔案 `pg_control`。

<a id="id-1.9.5.5.6"></a>

## 選項

可用的命令列選項如下：

`-D directory`<br>`--pgdata=directory`
:   指定資料庫叢集的儲存目錄。

`-c`<br>`--check`
:   檢查校驗和。若未指定其他模式，這是預設模式。

`-d`<br>`--disable`
:   停用校驗和。

`-e`<br>`--enable`
:   啟用校驗和。

`-f filenode`<br>`--filenode=filenode`
:   只驗證 filenode 為 *`filenode`* 之關聯中的校驗和。

`-N`<br>`--no-sync`
:   預設情況下，`pg_checksums` 會等待所有檔案都安全地寫入磁碟。此選項會讓 `pg_checksums` 不等待就返回，這樣比較快，但也表示之後若作業系統當機，可能會使更新過的資料目錄損毀。一般而言，此選項適用於測試，但不應該用於正式環境的安裝。使用 `--check` 時，此選項沒有作用。

`-P`<br>`--progress`
:   啟用進度回報。開啟此選項後，會在檢查或啟用校驗和時提供進度報告。

`--sync-method=method`

設定為預設值 `fsync` 時，`pg_checksums` 會遞迴地開啟並同步資料目錄中的所有檔案。搜尋檔案時，會跟隨 WAL 目錄與每個已設定資料表空間的符號連結。

在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含資料目錄、WAL 檔案與每個資料表空間的整個檔案系統。使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

使用 `--no-sync` 時，此選項沒有作用。

`-v`<br>`--verbose`
:   啟用詳細輸出。列出所有已檢查的檔案。

`-V`<br>`--version`
:   印出 pg_checksums 的版本後結束。

`-?`<br>`--help`
:   顯示 pg_checksums 命令列引數的說明後結束。

<a id="id-1.9.5.5.7"></a>

## 環境

`PGDATA`
:   指定資料庫叢集的儲存目錄；可以用 `-D` 選項覆寫。

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.5.8"></a>

## 注意事項

在大型叢集中啟用校驗和可能會花費很長的時間。在此操作期間，不得啟動該叢集或其他會寫入資料目錄的程式，否則可能會發生資料遺失。

在使用會直接複製關聯檔案區塊之工具（例如 [pg_rewind](app-pgrewind.md)）的複寫架構中，若啟用或停用校驗和的操作未在所有節點上一致地進行，可能會導致以錯誤校驗和形式呈現的頁面損毀。因此，在複寫架構中啟用或停用校驗和時，建議先停止所有叢集，再一致地切換所有叢集。銷毀所有待命伺服器、在主要伺服器上執行該操作，最後從頭重新建立待命伺服器，這種做法也是安全的。

若 pg_checksums 在啟用或停用校驗和時被中止或終止，叢集的資料校驗和設定會維持不變，而且可以重新執行 pg_checksums 來進行相同的操作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgchecksums.html)（原文版本：18.6；核對日期：2026-10-05）
