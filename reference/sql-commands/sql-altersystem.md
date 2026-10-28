<a id="SQL-ALTERSYSTEM"></a><a id="id-1.9.3.34.1"></a>

## ALTER SYSTEM

ALTER SYSTEM — 變更伺服器設定參數

<a id="id-1.9.3.34.4"></a>

## 語法

```

ALTER SYSTEM SET configuration_parameter { TO | = } { value [, ...] | DEFAULT }

ALTER SYSTEM RESET configuration_parameter
ALTER SYSTEM RESET ALL
```

<a id="id-1.9.3.34.5"></a>

## 說明

`ALTER SYSTEM` 用於變更整個資料庫叢集的伺服器設定參數。它可以比手動編輯 `postgresql.conf` 檔案的傳統方法更方便。`ALTER SYSTEM` 會將指定的參數設定寫入 `postgresql.auto.conf` 檔案，該檔案會在 `postgresql.conf` 之外額外被讀取。將參數設定為 `DEFAULT`，或使用 `RESET` 形式，會從 `postgresql.auto.conf` 檔案中移除該設定項目。使用 `RESET
ALL` 可移除所有這類設定項目。

以 `ALTER SYSTEM` 設定的值，會在下一次伺服器設定重新載入後生效；對於只能在伺服器啟動時變更的參數，則在下一次伺服器重新啟動後生效。要命令伺服器重新載入設定，可以呼叫 SQL 函式 `pg_reload_conf()`、執行 `pg_ctl reload`，或對主伺服器程序傳送 SIGHUP 訊號。

只有超級使用者，以及在某個參數上被授予 `ALTER SYSTEM` 權限的使用者，才能使用 `ALTER SYSTEM` 變更該參數。此外，由於此命令直接作用於檔案系統且無法回復，因此不允許在交易區塊或函式內使用。

<a id="id-1.9.3.34.6"></a>

## 參數

*`configuration_parameter`*
:   可設定之設定參數的名稱。可用的參數記載於[第 19 章](../../server-administration/runtime-config/README.md)。

*`value`*

參數的新值。依特定參數的需要，值可以指定為字串常數、識別字、數字，或以逗號分隔的上述項目清單。既不是數字也不是有效識別字的值必須加上引號。可以寫成 `DEFAULT`，以指定從 `postgresql.auto.conf` 中移除該參數及其值。

對於某些接受清單的參數，加上引號的值會產生以雙引號括住的輸出，以保留空白與逗號；對於其他參數，則必須在單引號字串內使用雙引號才能達到此效果。

<a id="id-1.9.3.34.7"></a>

## 注意事項

此命令不能用來設定 [data_directory](../../server-administration/runtime-config/runtime-config-file-locations.md#GUC-DATA-DIRECTORY)、[allow_alter_system](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM)，也不能用來設定不允許出現在 `postgresql.conf` 中的參數（例如[預設選項](../../server-administration/runtime-config/runtime-config-preset.md)）。

設定參數的其他方式，請參閱[第 19.1 節](../../server-administration/runtime-config/config-setting.md)。

將 [allow_alter_system](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM) 設定為 `off` 可以停用 `ALTER SYSTEM`，但這並不是一種安全機制（該參數的文件中有詳細說明）。

<a id="id-1.9.3.34.8"></a>

## 範例

設定 `wal_level`：

```

ALTER SYSTEM SET wal_level = replica;
```

復原上述設定，恢復為 `postgresql.conf` 中原本生效的任何設定：

```

ALTER SYSTEM RESET wal_level;
```

<a id="id-1.9.3.34.9"></a>

## 相容性

`ALTER SYSTEM` 陳述式是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.34.10"></a>

## 另請參閱

[SET](sql-set.md), [SHOW](sql-show.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altersystem.html)（原文版本：18.6；核對日期：2026-10-04）
