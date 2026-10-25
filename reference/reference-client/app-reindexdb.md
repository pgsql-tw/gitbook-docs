<a id="APP-REINDEXDB"></a><a id="id-1.9.4.22.1"></a>

## reindexdb

reindexdb — 重建 PostgreSQL 資料庫的索引

<a id="id-1.9.4.22.4"></a>

## 語法

<a id="id-1.9.4.22.4.1"></a>

`reindexdb` [*`connection-option`*...] [*`option`*...]
[
`-S` | `--schema`
*`schema`*
]
...
[
`-t` | `--table`
*`table`*
]
...
[
`-i` | `--index`
*`index`*
]
...
[
`-s` | `--system`
]
[
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.22.5"></a>

## 說明

reindexdb 是用來重建 PostgreSQL 資料庫中索引的工具程式。

reindexdb 是 SQL 命令 [`REINDEX`](../sql-commands/sql-reindex.md) 的包裝程式。透過此工具程式重建資料庫索引，與透過其他存取伺服器的方法重建索引，實際上沒有任何差別。

<a id="id-1.9.4.22.6"></a>

## 選項

reindexdb 接受下列命令列引數：

`-a`<br>`--all`
:   重建所有資料庫的索引。

`--concurrently`
:   使用 `CONCURRENTLY` 選項。請參閱 [REINDEX](../sql-commands/sql-reindex.md)，其中詳細說明了此選項的所有注意事項。

`[-d] dbname`<br>`[--dbname=]dbname`
:   在未使用 `-a`/`--all` 時，指定要重建索引的資料庫名稱。若未指定，資料庫名稱會從環境變數 `PGDATABASE` 讀取。若該變數也未設定，則使用連線時指定的使用者名稱。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

`-e`<br>`--echo`
:   回顯 reindexdb 產生並送往伺服器的命令。

`-i index`<br>`--index=index`
:   只重建 *`index`*。可以寫多個 `-i` 參數來重建多個索引。

`-j njobs`<br>`--jobs=njobs`
:   同時執行 *`njobs`* 個命令，以平行方式執行重建索引命令。此選項可能縮短處理時間，但也會增加資料庫伺服器的負載。

    reindexdb 會對資料庫開啟 *`njobs`* 個連線，因此請確認你的 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 設定夠高，足以容納所有連線。

    請注意，此選項與 `--system` 選項不相容。

`-q`<br>`--quiet`
:   不顯示進度訊息。

`-s`<br>`--system`
:   只重建資料庫系統目錄的索引。

`-S schema`<br>`--schema=schema`
:   只重建 *`schema`* 的索引。可以寫多個 `-S` 參數來重建多個綱要的索引。

`-t table`<br>`--table=table`
:   只重建 *`table`* 的索引。可以寫多個 `-t` 參數來重建多個資料表的索引。

`--tablespace=tablespace`
:   指定重建索引所在的資料表空間。（此名稱會被當作加上雙引號的識別字處理。）

`-v`<br>`--verbose`
:   在處理過程中印出詳細資訊。

`-V`<br>`--version`
:   印出 reindexdb 的版本後結束。

`-?`<br>`--help`
:   顯示 reindexdb 命令列引數的說明後結束。

reindexdb 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`
:   強制 reindexdb 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，reindexdb 會自動提示輸入密碼。不過，reindexdb 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   使用 `-a`/`--all` 時，連線到此資料庫以收集要重建索引的資料庫清單。若未指定，將使用 `postgres` 資料庫；若該資料庫不存在，則使用 `template1`。這可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。此外，連線到其他資料庫時，也會重複使用資料庫名稱本身以外的連線字串參數。

<a id="id-1.9.4.22.7"></a>

## 環境

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.22.8"></a>

## 診斷

若遇到困難，請參閱 [REINDEX](../sql-commands/sql-reindex.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.22.9"></a>

## 範例

重建資料庫 `test` 的索引：

```

$ reindexdb test
```

重建名為 `abcd` 之資料庫中資料表 `foo` 的索引，以及索引 `bar`：

```

$ reindexdb --table=foo --index=bar abcd
```

<a id="id-1.9.4.22.10"></a>

## 另請參閱

[REINDEX](../sql-commands/sql-reindex.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-reindexdb.html)（原文版本：18.6；核對日期：2026-10-10）
