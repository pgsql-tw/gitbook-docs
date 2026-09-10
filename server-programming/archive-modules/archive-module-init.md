## 49.1. 初始化函式 [#](#ARCHIVE-MODULE-INIT)

<a id="id-1.8.16.7.2"></a>

封存程式庫會以 [archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 的名稱作為程式庫基底名稱，透過動態載入共用程式庫來載入。系統會使用一般程式庫搜尋路徑尋找程式庫。若要提供必要的封存模組回呼並表明此程式庫確實為封存模組，它必須提供名為 `_PG_archive_module_init` 的函式。函式結果必須是 `ArchiveModuleCallbacks` 型別 struct 的指標；其中包含核心程式碼使用封存模組所需的全部資訊。回傳值必須具有伺服器存續期，通常是在全域範圍將其定義為 `static const` 變數來達成。

```

typedef struct ArchiveModuleCallbacks
{
    ArchiveStartupCB startup_cb;
    ArchiveCheckConfiguredCB check_configured_cb;
    ArchiveFileCB archive_file_cb;
    ArchiveShutdownCB shutdown_cb;
} ArchiveModuleCallbacks;
typedef const ArchiveModuleCallbacks *(*ArchiveModuleInit) (void);
```

僅 `archive_file_cb` 回呼為必要；其餘均為選用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/archive-module-init.html)（原文版本：18.6；核對日期：2026-09-10）
