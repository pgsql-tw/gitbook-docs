<a id="id-1.11.8.4.4.1"></a>

## vacuumlo

vacuumlo — 從 PostgreSQL 資料庫移除孤立的大型物件

## 語法

<a id="id-1.11.8.4.4.4.1"></a>

`vacuumlo` [*`option`*...] *`dbname`*...

<a id="id-1.11.8.4.4.5"></a>

## 說明

vacuumlo 是一個簡單的工具程式，會從 PostgreSQL 資料庫移除任何「孤立」的大型物件。孤立的大型物件（LO）是指 OID 未出現在資料庫任何 `oid` 或 `lo` 資料欄位中的 LO。

如果使用此工具，你可能也會對 [lo](../contrib/lo.md) 模組中的 `lo_manage` 觸發程序感興趣。`lo_manage` 有助於從一開始就避免建立孤立的 LO。

命令列中指定的所有資料庫都會被處理。

<a id="id-1.11.8.4.4.6"></a>

## 選項

vacuumlo 接受下列命令列引數：

`-l limit`<br>`--limit=limit`
:   每筆交易移除的大型物件不超過 *`limit`* 個（預設為 1000）。伺服器會為每個移除的 LO 取得一個鎖定，因此在一筆交易中移除過多 LO，可能超過 [max_locks_per_transaction](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-LOCKS-PER-TRANSACTION)。若要在單一交易中完成所有移除，請將限制設為零。

`-n`<br>`--dry-run`
:   不移除任何物件，只顯示將執行的動作。

`-v`<br>`--verbose`
:   輸出大量進度訊息。

`-V`<br>`--version`
:   顯示 vacuumlo 版本後結束。

`-?`<br>`--help`
:   顯示 vacuumlo 命令列引數的說明後結束。

vacuumlo 也接受下列連線參數的命令列引數：

`-h host`<br>`--host=host`
:   資料庫伺服器主機。

`-p port`<br>`--port=port`
:   資料庫伺服器連接埠。

`-U username`<br>`--username=username`
:   用於連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不顯示密碼提示。若伺服器要求密碼驗證，且無法透過 `.pgpass` 檔案等其他方式取得密碼，連線嘗試就會失敗。此選項適用於沒有使用者可輸入密碼的批次工作與指令碼。

`-W`<br>`--password`
:   強制 vacuumlo 在連線至資料庫前提示輸入密碼。

    這個選項絕非必要，因為伺服器要求密碼驗證時，vacuumlo 會自動提示輸入密碼。不過，vacuumlo 必須先浪費一次連線嘗試，才能得知伺服器需要密碼。在某些情況下，使用 `-W` 值得，因為可避免額外的連線嘗試。

<a id="id-1.11.8.4.4.7"></a>

## 環境

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數。

此工具與大多數其他 PostgreSQL 工具一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定是否在診斷訊息中使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.11.8.4.4.8"></a>

## 注意事項

vacuumlo 的運作方式如下：首先，vacuumlo 建立一個暫存資料表，其中包含所選資料庫內所有大型物件的 OID。接著，它掃描資料庫中所有型別為 `oid` 或 `lo` 的欄位，並從暫存資料表移除相符的項目。（注意：只考慮具有這些名稱的型別；尤其不考慮以其為基礎的 domain。）暫存資料表中剩餘的項目即為孤立 LO，並會被移除。

<a id="id-1.11.8.4.4.9"></a>

## 作者

Peter Mount `<peter@retep.org.uk>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/vacuumlo.html)
