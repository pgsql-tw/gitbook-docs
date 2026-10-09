<a id="PGWALDUMP"></a><a id="id-1.9.5.14.1"></a>

## pg_waldump

pg_waldump — 以人類可讀的形式顯示 PostgreSQL 資料庫叢集的預寫日誌

<a id="id-1.9.5.14.4"></a>

## 語法

<a id="id-1.9.5.14.4.1"></a>

`pg_waldump` [`option`...] [`startseg` [`endseg`]]

<a id="R1-APP-PGWALDUMP-1"></a>

## 說明

`pg_waldump` 會顯示預寫日誌（WAL），主要用於除錯或教學用途。

此工具只能由安裝伺服器的使用者執行，因為它需要資料目錄的唯讀存取權。

<a id="id-1.9.5.14.6"></a>

## 選項

下列命令列選項控制輸出的位置與格式：

*`startseg`*
:   從指定的 WAL 區段檔案開始讀取。這會隱含決定搜尋檔案的路徑，以及要使用的時間軸。

*`endseg`*
:   讀取指定的 WAL 區段檔案後停止。

`-b`<br>`--bkp-details`
:   輸出關於備份區塊的詳細資訊。

`-B block`<br>`--block=block`
:   只顯示修改指定區塊的記錄。也必須以 `--relation` 或 `-R` 提供該關聯。

`-e end`<br>`--end=end`
:   在指定的 WAL 位置停止讀取，而不是讀取到日誌串流的結尾。

`-f`<br>`--follow`
:   到達有效 WAL 的結尾後，繼續每秒輪詢一次，等待新的 WAL 出現。

`-F fork`<br>`--fork=fork`
:   只顯示修改指定分支（fork）中區塊的記錄。有效值為：`main` 表示主分支、`fsm` 表示可用空間對映（free space map）、`vm` 表示可見性對映（visibility map），以及 `init` 表示初始化分支（init fork）。

`-n limit`<br>`--limit=limit`
:   顯示指定數量的記錄後停止。

`-p path`<br>`--path=path`
:   指定要在其中搜尋 WAL 區段檔案的目錄，或包含存放這類檔案之 `pg_wal` 子目錄的目錄。預設會在目前目錄、目前目錄的 `pg_wal` 子目錄，以及 `PGDATA` 的 `pg_wal` 子目錄中搜尋。

`-q`<br>`--quiet`
:   除錯誤外不印出任何輸出。當你想知道某個範圍的 WAL 記錄能否成功剖析，但不在意記錄內容時，此選項可能很有用。

`-r rmgr`<br>`--rmgr=rmgr`
:   只顯示由指定資源管理器產生的記錄。你可以多次指定此選項，以選取多個資源管理器。若傳入 `list` 作為名稱，則印出有效的資源管理器名稱清單後結束。

    擴充功能可以定義自訂資源管理器，但 pg_waldump 不會載入擴充功能模組，因此不會依名稱辨識自訂資源管理器。你可以改為以 `custom###` 的形式指定自訂資源管理器，其中 *`###`* 是三位數的資源管理器 ID。此形式的名稱一律會被視為有效。

`-R tblspc/db/rel`<br>`--relation=tblspc/db/rel`
:   只顯示修改指定關聯中區塊的記錄。關聯以資料表空間 OID、資料庫 OID 與 relfilenode 指定，三者以斜線分隔，例如 `1234/12345/12345`。這與程式輸出中表示關聯所用的格式相同。

`-s start`<br>`--start=start`
:   開始讀取的 WAL 位置。預設會從在最早找到的檔案中找到的第一筆有效 WAL 記錄開始讀取。

`-t timeline`<br>`--timeline=timeline`
:   要從中讀取 WAL 記錄的時間軸。若有指定 *`startseg`*，預設使用其中的值；否則預設為 1。此值可以十進位或十六進位指定，例如 `17` 或 `0x11`。

`-V`<br>`--version`
:   印出 pg_waldump 版本後結束。

`-w`<br>`--fullpage`
:   只顯示包含完整頁面映像（full page image）的記錄。

`-x xid`<br>`--xid=xid`
:   只顯示標記有指定交易 ID 的記錄。

`-z`<br>`--stats[=record]`
:   顯示摘要統計資訊（記錄與完整頁面映像的數量及大小），而非個別記錄。可選擇改以每種記錄（per-record）而非每個 rmgr（per-rmgr）為單位產生統計資訊。

    若 pg_waldump 被訊號 SIGINT（**Control**+**C**）終止，會顯示截至終止時點所計算的統計摘要。Windows 上不支援此操作。

`--save-fullpage=save_path`
:   將 WAL 記錄中找到的完整頁面映像儲存到 *`save_path`* 目錄。所儲存的映像與所顯示的記錄適用相同的篩選與限制條件。

    完整頁面映像會以下列檔名格式儲存：`TIMELINE-LSN.RELTABLESPACE.DATOID.RELNODE.BLKNO_FORK`。檔名由下列部分組成：

    <table border="1" class="informaltable"><colgroup><col/><col/></colgroup><thead><tr><th>組成部分</th><th>說明</th></tr></thead><tbody><tr><td>TIMELINE</td><td>記錄所在之 WAL 區段檔案的時間軸，格式化為一個 8 字元的十六進位數字
                 <code class="literal">%08X</code></td></tr><tr><td>LSN</td><td>含有此映像之記錄的 <acronym class="acronym">LSN</acronym>，格式化為兩個 8 字元的十六進位數字
                 <code class="literal">%08X-%08X</code></td></tr><tr><td>RELTABLESPACE</td><td>該區塊的資料表空間 OID</td></tr><tr><td>DATOID</td><td>該區塊的資料庫 OID</td></tr><tr><td>RELNODE</td><td>該區塊的 filenode</td></tr><tr><td>BLKNO</td><td>該區塊的區塊編號</td></tr><tr><td>FORK</td><td>
                 完整頁面映像來源分支的名稱，例如
                 <code class="literal">main</code>、<code class="literal">fsm</code>、
                 <code class="literal">vm</code> 或 <code class="literal">init</code>。
                </td></tr></tbody></table>

`-?`<br>`--help`
:   顯示 pg_waldump 命令列引數的說明後結束。

<a id="id-1.9.5.14.7"></a>

## 環境

`PGDATA`
:   資料目錄；另請參閱 `-p` 選項。

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可能的值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.14.8"></a>

## 注意事項

在伺服器執行中時，可能會產生錯誤的結果。

只會顯示指定的時間軸（若未指定，則顯示預設時間軸）。其他時間軸中的記錄會被忽略。

pg_waldump 無法讀取副檔名為 `.partial` 的 WAL 檔案。若需要讀取這些檔案，必須從檔名中移除 `.partial` 副檔名。

<a id="id-1.9.5.14.9"></a>

## 另請參閱

[第 28.6 節](../../server-administration/wal/wal-internals.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgwaldump.html)（原文版本：18.6；核對日期：2026-10-09）
