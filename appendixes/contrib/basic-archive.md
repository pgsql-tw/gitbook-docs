## F.5. `basic_archive` — WAL 封存模組範例 [#](#BASIC-ARCHIVE)

[F.5.1. 設定參數](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

[F.5.2. 注意事項](basic-archive.md#BASIC-ARCHIVE-NOTES)

[F.5.3. 作者](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

<a id="id-1.11.7.15.2"></a>

`basic_archive` 是封存模組的範例。此模組會將已完成的 WAL 區段檔案複製到指定目錄。它或許沒有特別實用，但可作為開發自訂封存模組的起點。關於封存模組的更多資訊，請參閱[第 49 章](../../server-programming/archive-modules/README.md)。

此模組必須透過 [archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 載入，且必須啟用 [archive_mode](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-MODE)，才能運作。

<a id="BASIC-ARCHIVE-CONFIGURATION-PARAMETERS"></a>

### F.5.1. 設定參數 [#](#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

`basic_archive.archive_directory` (`string`) <a id="id-1.11.7.15.5.2.1.1.3"></a>
:   伺服器應複製 WAL 區段檔案的目錄。此目錄必須已存在。預設值是空字串，實際上會停止 WAL 封存；但若啟用 [archive_mode](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-MODE)，伺服器會累積 WAL 區段檔案，預期很快就會提供設定值。

這些參數必須在 `postgresql.conf` 中設定。典型的使用方式如下：

```

# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'
```

<a id="BASIC-ARCHIVE-NOTES"></a>

### F.5.2. 注意事項 [#](#BASIC-ARCHIVE-NOTES)

伺服器當機可能會在封存目錄中留下以 `archtemp` 為前綴的暫存檔。建議在當機後重新啟動伺服器之前刪除這類檔案。伺服器運作期間，只要這些檔案與任何仍在進行的封存無關，便可安全移除；但使用者進行此操作時應格外小心。

<a id="BASIC-ARCHIVE-AUTHOR"></a>

### F.5.3. 作者 [#](#BASIC-ARCHIVE-AUTHOR)

Nathan Bossart

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/basic-archive.html)（原文版本：18.6；核對日期：2026-09-06）
