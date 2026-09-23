<a id="RUNTIME-CONFIG-FILE-LOCATIONS"></a>

## 19.2. 檔案位置 [#](#RUNTIME-CONFIG-FILE-LOCATIONS)

除了前面已提過的 `postgresql.conf` 檔案之外，
PostgreSQL 還會使用另外兩個需要手動編輯的組態檔，
用於控制用戶端驗證（其用法，於
[第 20 章](../client-authentication/README.md)討論）。
依預設，這三個組態檔，都儲存在資料庫叢集的資料目錄中。
本節所描述的參數，可讓您將這些組態檔，
放置在其他位置。（這麼做能簡化管理工作；特別是當
組態檔各自獨立存放時，通常更容易確保它們都已妥善備份。）

<a id="GUC-DATA-DIRECTORY"></a>

`data_directory`（`string`） <a id="id-1.6.6.5.3.1.1.3"></a> [#](#GUC-DATA-DIRECTORY)
:   指定用於資料儲存的目錄。
    此參數只能在伺服器啟動時設定。
<a id="GUC-CONFIG-FILE"></a>

`config_file`（`string`） <a id="id-1.6.6.5.3.2.1.3"></a> [#](#GUC-CONFIG-FILE)
:   指定伺服器的主要組態檔
    （慣例上命名為 `postgresql.conf`）。
    此參數只能在 `postgres` 命令列上設定。
<a id="GUC-HBA-FILE"></a>

`hba_file`（`string`） <a id="id-1.6.6.5.3.3.1.3"></a> [#](#GUC-HBA-FILE)
:   指定基於主機的驗證（host-based authentication）組態檔
    （慣例上命名為 `pg_hba.conf`）。
    此參數只能在伺服器啟動時設定。
<a id="GUC-IDENT-FILE"></a>

`ident_file`（`string`） <a id="id-1.6.6.5.3.4.1.3"></a> [#](#GUC-IDENT-FILE)
:   指定使用者名稱對應的組態檔
    （慣例上命名為 `pg_ident.conf`）。
    此參數只能在伺服器啟動時設定。
    另請參閱[20.2 節](../client-authentication/auth-username-maps.md)。
<a id="GUC-EXTERNAL-PID-FILE"></a>

`external_pid_file`（`string`） <a id="id-1.6.6.5.3.5.1.3"></a> [#](#GUC-EXTERNAL-PID-FILE)
:   指定伺服器應建立的額外處理程序識別碼（PID）檔案名稱，
    供伺服器管理程式使用。
    此參數只能在伺服器啟動時設定。

在預設安裝中，以上參數皆未明確設定。而是透過
`-D` 命令列選項，或 `PGDATA`
環境變數，指定資料目錄，所有組態檔，
都會在該資料目錄中被找到。

若您希望將組態檔，存放在資料目錄以外的地方，
`postgres` 的 `-D` 命令列選項，
或 `PGDATA` 環境變數，
就必須指向包含這些組態檔的目錄，
並且必須在 `postgresql.conf`
（或命令列上）設定 `data_directory`
參數，以標示資料目錄的實際位置。請注意，
`data_directory` 會覆寫 `-D`
與 `PGDATA` 對資料目錄位置的指定，
但不會覆寫它們對組態檔位置的指定。

若您願意，也可以使用參數
`config_file`、`hba_file`
及／或 `ident_file`，個別指定組態檔的
名稱與位置。`config_file` 只能在
`postgres` 命令列上指定，但其他兩者，
則可以在主要組態檔中設定。若這三個參數
加上 `data_directory`，都已明確設定，
就不需要指定 `-D` 或 `PGDATA`。

在設定這些參數時，相對路徑，
會相對於啟動 `postgres` 時所在的目錄來解讀。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-file-locations.html)（原文版本：18.6；核對日期：2026-09-22）
