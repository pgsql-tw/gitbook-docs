<a id="BASIC-ARCHIVE"></a>

# F.6. basic_archive

[F.6.1. Configuration Parameters](#id-1.11.7.15.5)

[F.6.2. Notes](#id-1.11.7.15.6)

[F.6.3. Author](#id-1.11.7.15.7)

<a id="id-1.11.7.15.2"></a>

`basic_archive` 是一個封存模組範例。此模組會將已完成的 WAL 段檔案複製到指定目錄。它未必特別實用，但可作為開發自訂封存模組的起點。關於封存模組的詳細資訊，請參閱[第 51 章](../../51.-archive-modules.md)。

若要運作，必須透過 [archive_library](../../server-administration/server-configuration/write-ahead-log.md#GUC-ARCHIVE-LIBRARY) 載入此模組，並啟用 [archive_mode](../../server-administration/server-configuration/write-ahead-log.md#GUC-ARCHIVE-MODE)。

<a id="id-1.11.7.15.5"></a>

## F.6.1. Configuration Parameters

`basic_archive.archive_directory` (`string`) <a id="id-1.11.7.15.5.2.1.1.3"></a>

伺服器應複製 WAL 段檔案到此目錄。此目錄必須事先存在。預設值為空字串，實際上會停止 WAL 封存；不過若已啟用 [archive_mode](../../server-administration/server-configuration/write-ahead-log.md#GUC-ARCHIVE-MODE)，伺服器會累積 WAL 段檔案，等待你提供設定值。

這些參數必須在 `postgresql.conf` 中設定。典型用法如下：

```

# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'
```

<a id="id-1.11.7.15.6"></a>

## F.6.2. Notes

伺服器當機時，可能在封存目錄留下以 `archtemp` 為前綴的暫存檔。建議在當機後重新啟動伺服器之前刪除這些檔案。伺服器運作期間也可以安全地移除它們，前提是它們與任何正在進行的封存無關；不過操作時仍應格外謹慎。

<a id="id-1.11.7.15.7"></a>

## F.6.3. Author

Nathan Bossart

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/basic-archive.html)
