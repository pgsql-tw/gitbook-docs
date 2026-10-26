<a id="APP-CREATEDB"></a><a id="id-1.9.4.4.1"></a>

## createdb

createdb — 建立新的 PostgreSQL 資料庫

<a id="id-1.9.4.4.4"></a>

## 語法

<a id="id-1.9.4.4.4.1"></a>

`createdb` [*`connection-option`*...] [*`option`*...] [*`dbname`*
[*`description`*]]

<a id="R1-APP-CREATEDB-1"></a>

## 說明

createdb 會建立一個新的 PostgreSQL 資料庫。

通常，執行此命令的資料庫使用者會成為新資料庫的擁有者。不過，若執行的使用者具有適當的權限，可以透過 `-O` 選項指定不同的擁有者。

createdb 是 SQL 命令 [`CREATE DATABASE`](../sql-commands/sql-createdatabase.md) 的包裝程式。透過此工具程式建立資料庫，與透過其他存取伺服器的方法建立資料庫，實際上沒有任何差別。

<a id="id-1.9.4.4.6"></a>

## 選項

createdb 接受下列命令列引數：

*`dbname`*
:   指定要建立的資料庫名稱。此名稱在此叢集的所有 PostgreSQL 資料庫中必須是唯一的。預設會建立一個與目前系統使用者同名的資料庫。

*`description`*
:   指定要與新建立之資料庫相關聯的註解。

`-D tablespace`<br>`--tablespace=tablespace`
:   指定資料庫的預設資料表空間。（此名稱會被當作加上雙引號的識別字處理。）

`-e`<br>`--echo`
:   回顯 createdb 產生並送往伺服器的命令。

`-E encoding`<br>`--encoding=encoding`
:   指定此資料庫要使用的字元編碼方式。PostgreSQL 伺服器支援的字元集說明於[第 23.3.1 節](../../server-administration/charset/multibyte.md#multibyte-charset-supported)。

`-l locale`<br>`--locale=locale`
:   指定此資料庫要使用的區域設定。這等同於將 `--lc-collate`、`--lc-ctype` 與 `--icu-locale` 指定為相同的值。有些區域設定只對 ICU 有效，必須以 `--icu-locale` 設定。

`--lc-collate=locale`
:   指定此資料庫要使用的 LC_COLLATE 設定。

`--lc-ctype=locale`
:   指定此資料庫要使用的 LC_CTYPE 設定。

`--builtin-locale=locale`
:   指定使用內建（builtin）提供者時的區域設定名稱。區域設定支援說明於[第 23.1 節](../../server-administration/charset/locale.md)。

`--icu-locale=locale`
:   在選擇 ICU 區域設定提供者時，指定此資料庫要使用的 ICU 區域設定 ID。

`--icu-rules=rules`
:   指定額外的定序規則，用來自訂此資料庫預設定序的行為。只有 ICU 支援此功能。

`--locale-provider={builtin|libc|icu}`
:   指定資料庫預設定序所用的區域設定提供者。

`-O owner`<br>`--owner=owner`
:   指定將擁有新資料庫的資料庫使用者。（此名稱會被當作加上雙引號的識別字處理。）

`-S strategy`<br>`--strategy=strategy`
:   指定資料庫的建立策略。詳情請參閱 [CREATE DATABASE STRATEGY](../sql-commands/sql-createdatabase.md#CREATE-DATABASE-STRATEGY)。

`-T template`<br>`--template=template`
:   指定用來建立此資料庫的範本資料庫。（此名稱會被當作加上雙引號的識別字處理。）

`-V`<br>`--version`
:   印出 createdb 的版本後結束。

`-?`<br>`--help`
:   顯示 createdb 命令列引數的說明後結束。

選項 `-D`、`-l`、`-E`、`-O` 與 `-T` 對應於底層 SQL 命令 [`CREATE DATABASE`](../sql-commands/sql-createdatabase.md) 的選項；關於這些選項的更多資訊，請參閱該頁。

createdb 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`
:   強制 createdb 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，createdb 會自動提示輸入密碼。不過，createdb 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   指定建立新資料庫時要連線的資料庫名稱。若未指定，將使用 `postgres` 資料庫；若該資料庫不存在（或它就是要建立的新資料庫的名稱），則使用 `template1`。這可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

<a id="id-1.9.4.4.7"></a>

## 環境

`PGDATABASE`
:   若有設定，則為要建立的資料庫名稱，除非在命令列上被覆寫。

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數。若命令列上或 `PGDATABASE` 都未指定要建立的資料庫名稱，`PGUSER` 也會決定該名稱。

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.4.8"></a>

## 診斷

若遇到困難，請參閱 [CREATE DATABASE](../sql-commands/sql-createdatabase.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.4.9"></a>

## 範例

使用預設資料庫伺服器建立資料庫 `demo`：

```

$ createdb demo
```

使用主機 `eden`、連接埠 5000 上的伺服器，以 `template0` 範本資料庫建立資料庫 `demo`，命令列命令與底層 SQL 命令如下：

```

$ createdb -p 5000 -h eden -T template0 -e demo
CREATE DATABASE demo TEMPLATE template0;
```

<a id="id-1.9.4.4.10"></a>

## 另請參閱

[dropdb](app-dropdb.md), [CREATE DATABASE](../sql-commands/sql-createdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-createdb.html)（原文版本：18.6；核對日期：2026-10-09）
