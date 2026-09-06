## 18.12. 在 Windows 註冊事件日誌 [#](#EVENT-LOG-REGISTRATION)

<a id="id-1.6.5.15.2"></a>

若要向作業系統註冊 Windows 事件日誌程式庫，請執行以下命令：

```

regsvr32 pgsql_library_directory/pgevent.dll
```

這會在預設名稱為 `PostgreSQL` 的事件來源下，建立事件檢視器使用的登錄項目。

若要指定其他事件來源名稱（請參閱 [event_source](../runtime-config/runtime-config-logging.md#GUC-EVENT-SOURCE)），請使用 `/n` 與 `/i` 選項：

```

regsvr32 /n /i:event_source_name pgsql_library_directory/pgevent.dll
```

若要從作業系統取消註冊事件日誌程式庫，請執行以下命令：

```

regsvr32 /u [/i:event_source_name] pgsql_library_directory/pgevent.dll
```

### 注意

若要在資料庫伺服器中啟用事件記錄，請修改 `postgresql.conf` 中的 [log_destination](../runtime-config/runtime-config-logging.md#GUC-LOG-DESTINATION)，使其包含 `eventlog`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-log-registration.html)（原文版本：18.6；核對日期：2026-09-07）
