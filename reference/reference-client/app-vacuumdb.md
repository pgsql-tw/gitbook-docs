<a id="APP-VACUUMDB"></a><a id="id-1.9.4.23.1"></a>

## vacuumdb

vacuumdb — 對 PostgreSQL 資料庫進行垃圾回收與分析

<a id="id-1.9.4.23.4"></a>

## 語法

<a id="id-1.9.4.23.4.1"></a>

`vacuumdb` [*`connection-option`*...] [*`option`*...]
[
`-t` | `--table`
*`table`*
[( *`column`* [,...] )]
]
... [
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.23.4.2"></a>

`vacuumdb` [*`connection-option`*...] [*`option`*...]
[
`-n` | `--schema`
*`schema`*
]
... [
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.23.4.3"></a>

`vacuumdb` [*`connection-option`*...] [*`option`*...]
[
`-N` | `--exclude-schema`
*`schema`*
]
... [
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.23.5"></a>

## 說明

vacuumdb 是用來清理 PostgreSQL 資料庫的工具程式。vacuumdb 也會產生 PostgreSQL 查詢最佳化器所使用的內部統計資訊。

vacuumdb 是 SQL 命令 [`VACUUM`](../sql-commands/sql-vacuum.md) 的包裝程式。透過此工具程式對資料庫進行清理（vacuum）與分析，和透過其他存取伺服器的方法進行，實際上沒有任何差別。

<a id="id-1.9.4.23.6"></a>

## 選項

vacuumdb 接受下列命令列引數：

`-a`<br>`--all`
:   清理所有資料庫。

`--buffer-usage-limit size`
:   指定此次呼叫 vacuumdb 所用的緩衝區存取策略（[*[Buffer Access Strategy](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)）環狀緩衝區大小。此大小用來計算此策略中會被重複使用的共享緩衝區數量。請參閱 [VACUUM](../sql-commands/sql-vacuum.md)。

`[-d] dbname`<br>`[--dbname=]dbname`
:   在未使用 `-a`/`--all` 時，指定要清理或分析的資料庫名稱。若未指定，則從環境變數 `PGDATABASE` 讀取資料庫名稱。若該變數也未設定，則使用連線時指定的使用者名稱。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何相衝突的命令列選項。

`--disable-page-skipping`
:   停用依據可見性對應表（visibility map）內容略過頁面的功能。

`-e`<br>`--echo`
:   回顯 vacuumdb 產生並送往伺服器的命令。

`-f`<br>`--full`
:   執行「完整（full）」清理。

`-F`<br>`--freeze`
:   積極地「凍結（freeze）」資料列（tuple）。

`--force-index-cleanup`
:   一律移除指向死亡資料列的索引項目。

`-j njobs`<br>`--jobs=njobs`

同時執行 *`njobs`* 個命令，以平行方式執行清理或分析命令。此選項可能會縮短處理時間，但也會增加資料庫伺服器的負載。

vacuumdb 會開啟 *`njobs`* 個資料庫連線，因此請確認你的 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 設定夠高，足以容納所有連線。

請注意，若某些系統目錄被平行處理，將此模式與 `-f`（`FULL`）選項一起使用可能會導致死結失敗。

`--min-mxid-age mxid_age`

只對 multixact ID 年齡至少為 *`mxid_age`* 的資料表執行清理或分析命令。此設定適合用來安排資料表的處理優先順序，以防止 multixact ID 回捲（請參閱[第 24.1.5.1 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)）。

就此選項而言，關聯的 multixact ID 年齡是主關聯與其相關聯之 TOAST 資料表（若存在）兩者年齡中的最大值。由於 vacuumdb 所發出的命令在必要時也會處理該關聯的 TOAST 資料表，因此不需要另外考慮它。

`--min-xid-age xid_age`

只對交易 ID 年齡至少為 *`xid_age`* 的資料表執行清理或分析命令。此設定適合用來安排資料表的處理優先順序，以防止交易 ID 回捲（請參閱[第 24.1.5 節](../../server-administration/maintenance/routine-vacuuming.md#vacuum-for-wraparound)）。

就此選項而言，關聯的交易 ID 年齡是主關聯與其相關聯之 TOAST 資料表（若存在）兩者年齡中的最大值。由於 vacuumdb 所發出的命令在必要時也會處理該關聯的 TOAST 資料表，因此不需要另外考慮它。

`--missing-stats-only`

只分析缺少某個欄位、索引運算式或延伸統計物件之統計資訊的關聯。與 `--analyze-in-stages` 一起使用時，此選項可防止 vacuumdb 暫時以較低統計目標所產生的統計資訊取代現有的統計資訊，從而避免查詢最佳化器暫時做出較差的選擇。

此選項只能與 `--analyze-only` 或 `--analyze-in-stages` 一起使用。

請注意，`--missing-stats-only` 需要 [`pg_statistic`](../../internals/catalogs/catalog-pg-statistic.md) 與 [`pg_statistic_ext_data`](../../internals/catalogs/catalog-pg-statistic-ext-data.md) 的 `SELECT` 權限，而這些權限預設只限超級使用者擁有。

`-n schema`<br>`--schema=schema`
:   只清理或分析 *`schema`* 中的所有資料表。寫多個 `-n` 參數即可清理多個綱要。

`-N schema`<br>`--exclude-schema=schema`
:   不清理或分析 *`schema`* 中的任何資料表。寫多個 `-N` 參數即可排除多個綱要。

`--no-index-cleanup`
:   不移除指向死亡資料列的索引項目。

`--no-process-main`
:   略過主關聯。

`--no-process-toast`
:   略過與要清理之資料表相關聯的 TOAST 資料表（若有的話）。

`--no-truncate`
:   不截斷資料表結尾的空白頁面。

`-P parallel_workers`<br>`--parallel=parallel_workers`
:   指定*平行清理*（parallel vacuum）的平行工作程序數量。這讓清理作業可以利用多個 CPU 來處理索引。請參閱 [VACUUM](../sql-commands/sql-vacuum.md)。

`-q`<br>`--quiet`
:   不顯示進度訊息。

`--skip-locked`
:   略過無法立即鎖定以進行處理的關聯。

`-t table [ (column [,...]) ]`<br>`--table=table [ (column [,...]) ]`

只清理或分析 *`table`*。只有與 `--analyze` 或 `--analyze-only` 選項一起使用時，才能指定欄位名稱。寫多個 `-t` 參數即可清理多個資料表。

<a id="id-1.9.4.23.6.3.22.2.2"></a>

### 提示 [#](#app-vacuumdb-restored-note-1) <a href="#app-vacuumdb-restored-note-1" id="app-vacuumdb-restored-note-1"></a>

如果你指定了欄位，你可能必須在 shell 中跳脫括號。（請參閱下方的範例。）

`-v`<br>`--verbose`
:   在處理期間印出詳細資訊。

`-V`<br>`--version`
:   印出 vacuumdb 版本後結束。

`-z`<br>`--analyze`
:   同時計算供最佳化器使用的統計資訊。

`-Z`<br>`--analyze-only`
:   只計算供最佳化器使用的統計資訊（不進行清理）。

`--analyze-in-stages`

只計算供最佳化器使用的統計資訊（不進行清理），與 `--analyze-only` 相同。分三個階段執行分析；第一階段使用盡可能最低的統計目標（請參閱 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)），以更快產生可用的統計資訊，後續階段則建立完整的統計資訊。

此選項只適用於分析目前沒有統計資訊、或統計資訊完全不正確的資料庫，例如剛從還原的傾印或由 `pg_upgrade` 填入資料的資料庫。請注意，在已有統計資訊的資料庫中使用此選項執行，可能會因為早期階段的統計目標較低，而使查詢最佳化器暫時做出較差的選擇。

`-?`<br>`--help`
:   顯示 vacuumdb 命令列引數的說明後結束。

vacuumdb 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若此值以斜線開頭，則會被用作 Unix 網域 socket 的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來監聽連線的 TCP 連接埠或本機 Unix 網域 socket 檔案副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   永不發出密碼提示。若伺服器要求密碼認證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，則連線嘗試會失敗。此選項適用於沒有使用者在場輸入密碼的批次工作與腳本。

`-W`<br>`--password`

強制 vacuumdb 在連線到資料庫之前提示輸入密碼。

此選項從來都不是必要的，因為如果伺服器要求密碼認證，vacuumdb 會自動提示輸入密碼。不過，vacuumdb 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   使用 `-a`/`--all` 時，連線到此資料庫以收集要清理的資料庫清單。若未指定，將使用 `postgres` 資料庫；若該資料庫不存在，則使用 `template1`。這可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何相衝突的命令列選項。此外，連線到其他資料庫時，會重複使用資料庫名稱本身以外的連線字串參數。

<a id="id-1.9.4.23.7"></a>

## 環境

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式與大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.23.8"></a>

## 診斷

如果遇到困難，請參閱 [VACUUM](../sql-commands/sql-vacuum.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數都會套用。

<a id="id-1.9.4.23.9"></a>

## 範例

清理資料庫 `test`：

```

$ vacuumdb test
```

清理名為 `bigdb` 的資料庫，並為最佳化器進行分析：

```

$ vacuumdb --analyze bigdb
```

清理名為 `xyzzy` 的資料庫中的單一資料表 `foo`，並為最佳化器分析該資料表的單一欄位 `bar`：

```

$ vacuumdb --analyze --verbose --table='foo(bar)' xyzzy
```

清理名為 `xyzzy` 的資料庫中，`foo` 與 `bar` 綱要內的所有資料表：

```

$ vacuumdb --schema='foo' --schema='bar' xyzzy
```

<a id="id-1.9.4.23.10"></a>

## 另請參閱

[VACUUM](../sql-commands/sql-vacuum.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-vacuumdb.html)（原文版本：18.6；核對日期：2026-10-05）
