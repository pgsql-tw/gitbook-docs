<a id="PGTESTFSYNC"></a><a id="id-1.9.5.11.1"></a>

## pg_test_fsync

pg_test_fsync — 判定 PostgreSQL 最快的 `wal_sync_method`

## 語法

<a id="id-1.9.5.11.4.1"></a>

`pg_test_fsync` [*`option`*...]

<a id="id-1.9.5.11.5"></a>

## 說明

pg_test_fsync 的目的是讓你合理地了解，在你的特定系統上最快的 [wal_sync_method](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-SYNC-METHOD) 是哪一個，並在發現 I/O 問題時提供診斷資訊。不過，pg_test_fsync 所顯示的差異，在實際的資料庫吞吐量上可能不會造成任何顯著差異，特別是因為許多資料庫伺服器的速度並不受其預寫日誌所限制。pg_test_fsync 會針對每個 `wal_sync_method` 回報以微秒為單位的平均檔案同步操作時間，這也可以用來協助最佳化 [commit_delay](../../server-administration/runtime-config/runtime-config-wal.md#GUC-COMMIT-DELAY) 的值。

<a id="id-1.9.5.11.6"></a>

## 選項

pg_test_fsync 接受下列命令列選項：

`-f`<br>`--filename`
:   指定寫入測試資料的檔案名稱。此檔案應該位於 `pg_wal` 目錄目前所在或將要放置的同一個檔案系統中。（`pg_wal` 包含 WAL 檔案。）預設為目前目錄中的 `pg_test_fsync.out`。

`-s`<br>`--secs-per-test`
:   指定每項測試的秒數。每項測試的時間越長，測試的準確度越高，但執行所需的時間也越長。預設為 5 秒，可讓程式在 2 分鐘內完成。

`-V`<br>`--version`
:   印出 pg_test_fsync 版本後結束。

`-?`<br>`--help`
:   顯示 pg_test_fsync 命令列引數的說明後結束。

<a id="id-1.9.5.11.7"></a>

## 環境

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.11.8"></a>

## 另請參閱

[postgres](app-postgres.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtestfsync.html)（原文版本：18.6；核對日期：2026-10-05）
