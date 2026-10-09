<a id="APP-PGWALSUMMARY"></a><a id="id-1.9.5.15.1"></a>

## pg_walsummary

pg_walsummary — 印出 WAL 摘要檔案的內容

<a id="id-1.9.5.15.4"></a>

## 語法

<a id="id-1.9.5.15.4.1"></a>

`pg_walsummary` [*`option`*...] [*`file`*...]

<a id="id-1.9.5.15.5"></a>

## 說明

pg_walsummary 用於印出 WAL 摘要檔案的內容。這些二進位檔案位於資料目錄的 `pg_wal/summaries` 子目錄中，可以使用此工具轉換為文字。通常不需要這麼做，因為 WAL 摘要檔案主要是為了支援[增量備份](../../server-administration/backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)而存在，但它可能對除錯有幫助。

WAL 摘要檔案以資料表空間 OID、關聯 OID 與關聯分支（relation fork）作為索引。對於每個關聯分支，它會儲存在該檔案所摘要的範圍內被 WAL 修改過的區塊清單。它也可以儲存一個「限制區塊」（limit block）：若該關聯分支是在相關的 WAL 範圍內建立或截斷的，其值為 0；否則為該關聯分支被截斷到的最短長度。若該關聯分支在相關的 WAL 範圍內既未被建立、刪除，也未被截斷，則限制區塊為未定義或無限大，此工具不會印出它。

<a id="id-1.9.5.15.6"></a>

## 選項

`-i`<br>`--individual`
:   預設情況下，`pg_walsummary` 會為每一段由一個或多個連續修改區塊組成的範圍印出一行輸出。這可以讓輸出精簡許多，因為一個從區塊 0 到 999 全部被修改的關聯，只會產生一行輸出，而不是 1000 個個別的行。此選項要求為每一個被修改的區塊各印出一行輸出。

`-q`<br>`--quiet`
:   除了錯誤之外，不印出任何輸出。當你想知道某個 WAL 摘要檔案能否成功剖析，但不在意其內容時，這可能很有用。

`-V`<br>`--version`
:   顯示版本資訊，然後結束。

`-?`<br>`--help`
:   顯示 pg_walsummary 命令列引數的說明，然後結束。

<a id="id-1.9.5.15.7"></a>

## 環境

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.15.8"></a>

## 另請參閱

[pg_basebackup](../reference-client/app-pgbasebackup.md), [pg_combinebackup](../reference-client/app-pgcombinebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgwalsummary.html)（原文版本：18.6；核對日期：2026-10-05）
