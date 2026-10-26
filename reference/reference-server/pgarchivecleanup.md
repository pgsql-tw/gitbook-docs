<a id="PGARCHIVECLEANUP"></a><a id="id-1.9.5.4.1"></a>

## pg_archivecleanup

pg_archivecleanup — 清理 PostgreSQL WAL 歸檔檔案

<a id="id-1.9.5.4.4"></a>

## 語法

<a id="id-1.9.5.4.4.1"></a>

`pg_archivecleanup` [*`option`*...] *`archivelocation`* *`oldestkeptwalfile`*

<a id="id-1.9.5.4.5"></a>

## 說明

pg_archivecleanup 的設計用途是作為 `archive_cleanup_command`，在以待命伺服器身分執行時清理 WAL 檔案歸檔（請參閱[第 26.2 節](../../server-administration/high-availability/warm-standby.md)）。pg_archivecleanup 也可以作為獨立程式，用來清理 WAL 檔案歸檔。

若要設定待命伺服器使用 pg_archivecleanup，請將以下內容放入其 `postgresql.conf` 設定檔：

```

archive_cleanup_command = 'pg_archivecleanup archivelocation %r'
```

其中 *`archivelocation`* 是應從中移除 WAL 區段檔案的目錄。

在 [archive_cleanup_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND) 中使用時，所有在邏輯上位於 `%r` 引數值之前的 WAL 檔案，都會從 *`archivelocation`* 中移除。這能將需要保留的檔案數量降到最低，同時保有當機後重新啟動的能力。若 *`archivelocation`* 是此特定待命伺服器的暫時中繼區，就適合使用此參數；但若 *`archivelocation`* 是要作為長期 WAL 歸檔區，或有多台待命伺服器從同一個歸檔位置進行復原，則*不*適合使用。

作為獨立程式使用時，所有在邏輯上位於 *`oldestkeptwalfile`* 之前的 WAL 檔案，都會從 *`archivelocation`* 中移除。在此模式下，若你指定 `.partial` 或 `.backup` 檔名，則只會以檔名前綴作為 *`oldestkeptwalfile`*。對 `.backup` 檔名的這種處理方式，讓你能夠移除在某個特定基礎備份之前歸檔的所有 WAL 檔案而不發生錯誤。例如，以下範例會移除所有比 WAL 檔名 `000000010000003700000010` 更舊的檔案：

```

pg_archivecleanup -d archive 000000010000003700000010.00000020.backup

pg_archivecleanup:  keep WAL file "archive/000000010000003700000010" and later
pg_archivecleanup:  removing file "archive/00000001000000370000000F"
pg_archivecleanup:  removing file "archive/00000001000000370000000E"
```

pg_archivecleanup 假設 *`archivelocation`* 是擁有伺服器之使用者可讀寫的目錄。

<a id="id-1.9.5.4.6"></a>

## 選項

pg_archivecleanup 接受下列命令列引數：

`-b`<br>`--clean-backup-history`
:   一併移除備份歷史檔案。關於備份歷史檔案的詳細資訊，請參閱[第 25.3.2 節](../../server-administration/backup/continuous-archiving.md#backup-base-backup)。

`-d`<br>`--debug`
:   在 `stderr` 上印出大量除錯日誌輸出。

`-n`<br>`--dry-run`
:   在 `stdout` 上印出原本會被移除的檔案名稱（執行試運行）。

`-V`<br>`--version`
:   印出 pg_archivecleanup 版本後結束。

`-x extension`<br>`--strip-extension=extension`
:   提供一個副檔名，在判斷檔案是否應刪除之前，會先從所有檔名中去除此副檔名。這通常適用於清理在儲存時經過壓縮、因而被壓縮程式加上副檔名的歸檔。例如：`-x
    .gz`。

`-?`<br>`--help`
:   顯示 pg_archivecleanup 命令列引數的說明後結束。

<a id="id-1.9.5.4.7"></a>

## 環境

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可能的值為 `always`、`auto` 與 `never`。

<a id="id-1.9.5.4.8"></a>

## 注意事項

pg_archivecleanup 設計為作為獨立工具使用時可搭配 PostgreSQL 8.0 及之後的版本，作為歸檔清理命令使用時可搭配 PostgreSQL 9.0 及之後的版本。

pg_archivecleanup 以 C 撰寫，原始碼容易修改，並有特別標示的區段供你依自己的需求修改。

<a id="id-1.9.5.4.9"></a>

## 範例

在 Linux 或 Unix 系統上，你可能會使用：

```

archive_cleanup_command = 'pg_archivecleanup -d /mnt/standby/archive %r 2>>cleanup.log'
```

其中歸檔目錄實體上位於待命伺服器，因此 `archive_command` 是透過 NFS 存取它，但這些檔案對待命伺服器而言是本機檔案。這會：

* 在 `cleanup.log` 中產生除錯輸出
* 從歸檔目錄中移除不再需要的檔案

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgarchivecleanup.html)（原文版本：18.6；核對日期：2026-10-09）
