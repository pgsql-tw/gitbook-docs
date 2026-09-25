<a id="ARCHIVE-MODULE-CALLBACKS"></a>

## 49.2. 封存模組回呼函式 [#](#ARCHIVE-MODULE-CALLBACKS)

[49.2.1. 啟動回呼函式](archive-module-callbacks.md#ARCHIVE-MODULE-STARTUP)

[49.2.2. 檢查回呼函式](archive-module-callbacks.md#ARCHIVE-MODULE-CHECK)

[49.2.3. 封存回呼函式](archive-module-callbacks.md#ARCHIVE-MODULE-ARCHIVE)

[49.2.4. 關閉回呼函式](archive-module-callbacks.md#ARCHIVE-MODULE-SHUTDOWN)

封存回呼函式定義了模組實際的封存行為。伺服器會依需要呼叫這些函式，以處理每一個 WAL 檔案。

<a id="ARCHIVE-MODULE-STARTUP"></a>

### 49.2.1. 啟動回呼函式 [#](#ARCHIVE-MODULE-STARTUP)

`startup_cb` 回呼函式會在模組載入後不久被呼叫。這個回呼函式
可以用來執行任何需要的額外初始化工作。若封存模組有任何狀態，可以使用
`state->private_data` 來儲存。

```

typedef void (*ArchiveStartupCB) (ArchiveModuleState *state);
```

<a id="ARCHIVE-MODULE-CHECK"></a>

### 49.2.2. 檢查回呼函式 [#](#ARCHIVE-MODULE-CHECK)

`check_configured_cb` 回呼函式會被呼叫，用來判斷模組是否
已完成完整設定並準備好接受 WAL 檔案（例如，其設定參數已設為有效值）。若未定義
`check_configured_cb`，伺服器一律會假設模組已完成設定。

```

typedef bool (*ArchiveCheckConfiguredCB) (ArchiveModuleState *state);
```

若回傳 `true`，伺服器會接著進行封存，
呼叫 `archive_file_cb`
回呼函式。若回傳 `false`，則不會進行封存，
封存程序會在伺服器記錄檔中發出以下訊息：

```

WARNING:  archive_mode enabled, yet archiving is not configured
```

在後者的情況下，伺服器會定期呼叫這個函式，並且只有在它回傳 `true` 時才會進行封存。

### 注意

在回傳 `false` 時，附加一些額外資訊到通用的
警告訊息中可能會很有幫助。要這麼做，請在回傳 `false` 之前，透過
`arch_module_check_errdetail` 巨集
提供一則訊息。與
`errdetail()` 一樣，這個巨集接受一個格式字串，
後面接上一份選擇性的參數清單。產生的字串會作為警告訊息的
`DETAIL` 行輸出。

<a id="ARCHIVE-MODULE-ARCHIVE"></a>

### 49.2.3. 封存回呼函式 [#](#ARCHIVE-MODULE-ARCHIVE)

`archive_file_cb` 回呼函式會被呼叫，用來封存一個
單一 WAL 檔案。

```

typedef bool (*ArchiveFileCB) (ArchiveModuleState *state, const char *file, const char *path);
```

若回傳 `true`，伺服器會視同該檔案已成功封存，
接下來的處理可能包含回收或移除
原始的 WAL 檔案。若回傳 `false` 或拋出錯誤，伺服器會
保留原始的 WAL 檔案，並稍後重試封存。
*`file`* 只會包含要封存的 WAL
檔案的檔名，而 *`path`* 則包含該 WAL 檔案的
完整路徑（含檔名）。

### 注意

`archive_file_cb` 回呼函式是在一個
短生命週期的記憶體上下文中被呼叫的，該記憶體上下文會在每次呼叫之間
重置。如果你需要生命週期較長的儲存空間，請在模組的
`startup_cb` 回呼函式中建立一個記憶體上下文。

<a id="ARCHIVE-MODULE-SHUTDOWN"></a>

### 49.2.4. 關閉回呼函式 [#](#ARCHIVE-MODULE-SHUTDOWN)

`shutdown_cb` 回呼函式會在封存程序結束時
（例如發生錯誤之後），或是
[archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 的值改變時被呼叫。若未定義
`shutdown_cb`，在這些情況下不會採取任何特別動作。若封存模組有任何狀態，這個回呼函式應該要
釋放它，以避免記憶體洩漏。

```

typedef void (*ArchiveShutdownCB) (ArchiveModuleState *state);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/archive-module-callbacks.html)（原文版本：18.6；核對日期：2026-09-25）
