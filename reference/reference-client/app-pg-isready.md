<a id="APP-PG-ISREADY"></a><a id="id-1.9.4.16.1"></a>

## pg_isready

pg_isready — 檢查 PostgreSQL 伺服器的連線狀態

<a id="id-1.9.4.16.4"></a>

## 語法

<a id="id-1.9.4.16.4.1"></a>

`pg_isready` [*`connection-option`*...] [*`option`*...]

<a id="APP-PG-ISREADY-DESCRIPTION"></a>

## 說明

pg_isready 是用來檢查 PostgreSQL 資料庫伺服器連線狀態的工具程式。其結束狀態代表連線檢查的結果。

<a id="APP-PG-ISREADY-OPTIONS"></a>

## 選項

`-d dbname`<br>`--dbname=dbname`
:   指定要連線的資料庫名稱。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

`-h hostname`<br>`--host=hostname`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。預設為環境變數 `PGPORT` 的值；若該變數未設定，則為編譯時指定的連接埠，通常是 5432。

`-q`<br>`--quiet`
:   不顯示狀態訊息。這在撰寫腳本時很有用。

`-t seconds`<br>`--timeout=seconds`
:   嘗試連線時，在回報伺服器沒有回應之前所等待的最大秒數。設為 0 會停用此逾時。預設為 3 秒。

`-U username`<br>`--username=username`
:   以使用者 *`username`* 而非預設使用者的身分連線到資料庫。

`-V`<br>`--version`
:   印出 pg_isready 的版本後結束。

`-?`<br>`--help`
:   顯示 pg_isready 命令列引數的說明後結束。

<a id="id-1.9.4.16.7"></a>

## 結束狀態

若伺服器正常接受連線，pg_isready 會向 shell 傳回 `0`；若伺服器拒絕連線（例如在啟動期間），傳回 `1`；若連線嘗試沒有回應，傳回 `2`；若未進行任何嘗試（例如因為參數無效），則傳回 `3`。

<a id="id-1.9.4.16.8"></a>

## 環境

`pg_isready` 與大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="APP-PG-ISREADY-NOTES"></a>

## 注意事項

要取得伺服器狀態，不需要提供正確的使用者名稱、密碼或資料庫名稱值；不過，若提供的值不正確，伺服器會在日誌中記錄一次失敗的連線嘗試。

<a id="APP-PG-ISREADY-EXAMPLES"></a>

## 範例

標準用法：

```

$ pg_isready
/tmp:5432 - accepting connections
$ echo $?
0
```

使用連線參數連線到正在啟動中的 PostgreSQL 叢集：

```

$ pg_isready -h localhost -p 5433
localhost:5433 - rejecting connections
$ echo $?
1
```

使用連線參數連線到沒有回應的 PostgreSQL 叢集：

```

$ pg_isready -h someremotehost
someremotehost:5432 - no response
$ echo $?
2
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pg-isready.html)（原文版本：18.6；核對日期：2026-10-09）
