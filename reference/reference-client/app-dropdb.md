<a id="APP-DROPDB"></a><a id="id-1.9.4.6.1"></a>

## dropdb

dropdb — 移除 PostgreSQL 資料庫

<a id="id-1.9.4.6.4"></a>

## 語法

<a id="id-1.9.4.6.4.1"></a>

`dropdb` [*`connection-option`*...] [*`option`*...] *`dbname`*

<a id="id-1.9.4.6.5"></a>

## 說明

dropdb 會刪除一個現有的 PostgreSQL 資料庫。執行此命令的使用者必須是資料庫超級使用者或該資料庫的擁有者。

dropdb 是 SQL 命令 [`DROP DATABASE`](../sql-commands/sql-dropdatabase.md) 的包裝程式。透過此工具程式刪除資料庫，與透過其他存取伺服器的方法刪除資料庫，實際上沒有任何差別。

<a id="id-1.9.4.6.6"></a>

## 選項

dropdb 接受下列命令列引數：

*`dbname`*
:   指定要移除的資料庫名稱。

`-e`<br>`--echo`
:   回顯 dropdb 產生並送往伺服器的命令。

`-f`<br>`--force`
:   在刪除目標資料庫之前，嘗試終止所有連往該資料庫的現有連線。關於此選項的更多資訊，請參閱 [DROP DATABASE](../sql-commands/sql-dropdatabase.md)。

`-i`<br>`--interactive`
:   在執行任何破壞性動作之前發出確認提示。

`-V`<br>`--version`
:   印出 dropdb 的版本後結束。

`--if-exists`
:   資料庫不存在時不擲出錯誤；此情況會發出 notice。

`-?`<br>`--help`
:   顯示 dropdb 命令列引數的說明後結束。

dropdb 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`
:   強制 dropdb 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，dropdb 會自動提示輸入密碼。不過，dropdb 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   指定為了刪除目標資料庫而要連線的資料庫名稱。若未指定，將使用 `postgres` 資料庫；若該資料庫不存在（或它就是要刪除的資料庫），則使用 `template1`。這可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

<a id="id-1.9.4.6.7"></a>

## 環境

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.6.8"></a>

## 診斷

若遇到困難，請參閱 [DROP DATABASE](../sql-commands/sql-dropdatabase.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.6.9"></a>

## 範例

刪除預設資料庫伺服器上的資料庫 `demo`：

```

$ dropdb demo
```

使用主機 `eden`、連接埠 5000 上的伺服器刪除資料庫 `demo`，並進行確認，同時查看底層實際執行的命令：

```

$ dropdb -p 5000 -h eden -i -e demo
Database "demo" will be permanently deleted.
Are you sure? (y/n) y
DROP DATABASE demo;
```

<a id="id-1.9.4.6.10"></a>

## 另請參閱

[createdb](app-createdb.md), [DROP DATABASE](../sql-commands/sql-dropdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-dropdb.html)（原文版本：18.6；核對日期：2026-10-09）
