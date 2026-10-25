<a id="APP-CLUSTERDB"></a><a id="id-1.9.4.3.1"></a>

## clusterdb

clusterdb — 叢集化 PostgreSQL 資料庫

<a id="id-1.9.4.3.4"></a>

## 語法

<a id="id-1.9.4.3.4.1"></a>

`clusterdb` [*`connection-option`*...] [*`option`*...]
[
`--table` | `-t`
*`table`*
]
... [
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.3.5"></a>

## 說明

clusterdb 是用來重新叢集化 PostgreSQL 資料庫中資料表的工具程式。它會找出先前已叢集化的資料表，並依據上次所用的同一個索引再次將它們叢集化。從未叢集化過的資料表不受影響。

clusterdb 是 SQL 命令 [CLUSTER](../sql-commands/sql-cluster.md) 的包裝程式。透過此工具程式叢集化資料庫，與透過其他存取伺服器的方法叢集化資料庫，實際上沒有任何差別。

<a id="id-1.9.4.3.6"></a>

## 選項

clusterdb 接受下列命令列引數：

`-a`<br>`--all`
:   叢集化所有資料庫。

`[-d] dbname`<br>`[--dbname=]dbname`
:   在未使用 `-a`/`--all` 時，指定要叢集化的資料庫名稱。若未指定，資料庫名稱會從環境變數 `PGDATABASE` 讀取。若該變數也未設定，則使用連線時指定的使用者名稱。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

`-e`<br>`--echo`
:   回顯 clusterdb 產生並送往伺服器的命令。

`-q`<br>`--quiet`
:   不顯示進度訊息。

`-t table`<br>`--table=table`
:   只叢集化 *`table`*。寫多個 `-t` 參數即可叢集化多個資料表。

`-v`<br>`--verbose`
:   在處理過程中印出詳細資訊。

`-V`<br>`--version`
:   印出 clusterdb 的版本後結束。

`-?`<br>`--help`
:   顯示 clusterdb 命令列引數的說明後結束。

clusterdb 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`
:   強制 clusterdb 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，clusterdb 會自動提示輸入密碼。不過，clusterdb 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   使用 `-a`/`--all` 時，連線到此資料庫以收集要叢集化的資料庫清單。若未指定，將使用 `postgres` 資料庫；若該資料庫不存在，則使用 `template1`。這可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。此外，連線到其他資料庫時，也會重複使用資料庫名稱本身以外的連線字串參數。

<a id="id-1.9.4.3.7"></a>

## 環境

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.3.8"></a>

## 診斷

若遇到困難，請參閱 [CLUSTER](../sql-commands/sql-cluster.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.3.9"></a>

## 範例

叢集化資料庫 `test`：

```

$ clusterdb test
```

叢集化名為 `xyzzy` 的資料庫中的單一資料表 `foo`：

```

$ clusterdb --table=foo xyzzy
```

<a id="id-1.9.4.3.10"></a>

## 另請參閱

[CLUSTER](../sql-commands/sql-cluster.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-clusterdb.html)（原文版本：18.6；核對日期：2026-10-09）
