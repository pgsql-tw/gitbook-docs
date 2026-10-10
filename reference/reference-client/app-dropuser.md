<a id="APP-DROPUSER"></a><a id="id-1.9.4.7.1"></a>

## dropuser

dropuser — 移除 PostgreSQL 使用者帳號

<a id="id-1.9.4.7.4"></a>

## 語法

<a id="id-1.9.4.7.4.1"></a>

`dropuser` [*`connection-option`*...] [*`option`*...] [*`username`*]

<a id="id-1.9.4.7.5"></a>

## 說明

dropuser 會移除一個現有的 PostgreSQL 使用者。超級使用者可以使用此命令移除任何角色；否則，只能移除非超級使用者的角色，而且只有具備 `CREATEROLE` 權限、並已獲授予目標角色之 `ADMIN OPTION` 的使用者才能移除。

dropuser 是 SQL 命令 [`DROP ROLE`](../sql-commands/sql-droprole.md) 的包裝程式。透過此工具程式刪除使用者，與透過其他存取伺服器的方法刪除使用者，實際上沒有任何差別。

<a id="id-1.9.4.7.6"></a>

## 選項

dropuser 接受下列命令列引數：

*`username`*
:   指定要移除的 PostgreSQL 使用者名稱。若命令列上未指定名稱，且使用了 `-i`/`--interactive` 選項，則會提示你輸入名稱。

`-e`<br>`--echo`
:   回顯 dropuser 產生並送往伺服器的命令。

`-i`<br>`--interactive`
:   在實際移除使用者之前提示確認；若命令列上未指定使用者名稱，也會提示輸入使用者名稱。

`-V`<br>`--version`
:   印出 dropuser 的版本後結束。

`--if-exists`
:   使用者不存在時不擲出錯誤；此情況會發出 notice。

`-?`<br>`--help`
:   顯示 dropuser 命令列引數的說明後結束。

dropuser 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱（不是要刪除的使用者名稱）。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`
:   強制 dropuser 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，dropuser 會自動提示輸入密碼。不過，dropuser 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

<a id="id-1.9.4.7.7"></a>

## 環境

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.7.8"></a>

## 診斷

若遇到困難，請參閱 [DROP ROLE](../sql-commands/sql-droprole.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.7.9"></a>

## 範例

從預設資料庫伺服器移除使用者 `joe`：

```

$ dropuser joe
```

使用主機 `eden`、連接埠 5000 上的伺服器移除使用者 `joe`，並進行確認，同時查看底層實際執行的命令：

```

$ dropuser -p 5000 -h eden -i -e joe
Role "joe" will be permanently removed.
Are you sure? (y/n) y
DROP ROLE joe;
```

<a id="id-1.9.4.7.10"></a>

## 另請參閱

[createuser](app-createuser.md), [DROP ROLE](../sql-commands/sql-droprole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-dropuser.html)（原文版本：18.6；核對日期：2026-10-09）
