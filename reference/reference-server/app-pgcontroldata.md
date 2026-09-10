<a id="id-1.9.5.6.1"></a>

## pg_controldata

pg_controldata — 顯示 PostgreSQL 資料庫叢集的控制資訊

## 語法

<a id="id-1.9.5.6.4.1"></a>

`pg_controldata` [*`option`*] [[ `-D` | `--pgdata` ]*`datadir`*]

<a id="R1-APP-PGCONTROLDATA-1"></a>

## 說明

`pg_controldata` 會印出 `initdb` 初始化的資訊，例如目錄版本。它也會顯示預先寫入日誌與檢查點處理的資訊。這些資訊涵蓋整個叢集，並非特定資料庫的資訊。

此工具需要資料目錄的讀取權限，因此只有初始化叢集的使用者能執行。你可以在命令列指定資料目錄，或使用環境變數 `PGDATA`。此工具支援 `-V` 與 `--version` 選項，會印出 pg_controldata 版本後結束；也支援 `-?` 與 `--help` 選項，會輸出支援的引數。

<a id="id-1.9.5.6.6"></a>

## 環境

`PGDATA`
:   預設資料目錄位置。

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgcontroldata.html)（原文版本：18.6；核對日期：2026-09-10）
