<a id="RUNTIME-CONFIG"></a>

## 第 19 章、伺服器組態設定

**目錄**

[19.1. 設定參數](config-setting.md)
:   [19.1.1. 參數名稱與數值](config-setting.md#CONFIG-SETTING-NAMES-VALUES)

    [19.1.2. 透過組態設定檔進行參數互動](config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE)

    [19.1.3. 透過 SQL 進行參數互動](config-setting.md#CONFIG-SETTING-SQL)

    [19.1.4. 透過 Shell 進行參數互動](config-setting.md#CONFIG-SETTING-SHELL)

    [19.1.5. 管理組態設定檔內容](config-setting.md#CONFIG-INCLUDES)

[19.2. 檔案位置](runtime-config-file-locations.md)

[19.3. 連線與驗證](runtime-config-connection.md)
:   [19.3.1. 連線設定](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SETTINGS)

    [19.3.2. TCP 設定](runtime-config-connection.md#RUNTIME-CONFIG-TCP-SETTINGS)

    [19.3.3. 驗證](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)

    [19.3.4. SSL](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SSL)

[19.4. 資源消耗](runtime-config-resource.md)
:   [19.4.1. 記憶體](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)

    [19.4.2. 磁碟](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-DISK)

    [19.4.3. 核心資源使用量](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-KERNEL)

    [19.4.4. 背景寫入程序](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

    [19.4.5. I/O](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-IO)

    [19.4.6. 工作程序](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

[19.5. 預寫日誌](runtime-config-wal.md)
:   [19.5.1. 設定](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)

    [19.5.2. 檢查點](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)

    [19.5.3. 歸檔](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)

    [19.5.4. 復原](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)

    [19.5.5. 歸檔復原](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

    [19.5.6. 復原目標](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

    [19.5.7. WAL 摘要化](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

[19.6. 複製](runtime-config-replication.md)
:   [19.6.1. 傳送端伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SENDER)

    [19.6.2. 主要伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY)

    [19.6.3. 待命伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)

    [19.6.4. 訂閱端](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

[19.7. 查詢規劃](runtime-config-query.md)
:   [19.7.1. 規劃器方法組態設定](runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)

    [19.7.2. 規劃器成本常數](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)

    [19.7.3. 基因查詢最佳化器](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)

    [19.7.4. 其他規劃器選項](runtime-config-query.md#RUNTIME-CONFIG-QUERY-OTHER)

[19.8. 錯誤回報與日誌](runtime-config-logging.md)
:   [19.8.1. 記錄到何處](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE)

    [19.8.2. 何時記錄](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHEN)

    [19.8.3. 記錄什麼內容](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHAT)

    [19.8.4. 使用 CSV 格式日誌輸出](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)

    [19.8.5. 使用 JSON 格式日誌輸出](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)

    [19.8.6. 程序標題](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

[19.9. 執行時期統計資訊](runtime-config-statistics.md)
:   [19.9.1. 累計查詢與索引統計資訊](runtime-config-statistics.md#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

    [19.9.2. 統計資訊監控](runtime-config-statistics.md#RUNTIME-CONFIG-STATISTICS-MONITOR)

[19.10. Vacuum 處理](runtime-config-vacuum.md)
:   [19.10.1. 自動 Vacuum](runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)

    [19.10.2. 以成本為基礎的 Vacuum 延遲](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

    [19.10.3. 預設行為](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-DEFAULT)

    [19.10.4. 凍結](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING)

[19.11. 用戶端連線預設值](runtime-config-client.md)
:   [19.11.1. 陳述式行為](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)

    [19.11.2. 地區設定與格式化](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)

    [19.11.3. 共享程式庫預先載入](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)

    [19.11.4. 其他預設值](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

[19.12. 鎖定管理](runtime-config-locks.md)

[19.13. 版本與平台相容性](runtime-config-compatible.md)
:   [19.13.1. 舊版 PostgreSQL](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)

    [19.13.2. 平台與用戶端相容性](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

[19.14. 錯誤處理](runtime-config-error-handling.md)

[19.15. 預設選項](runtime-config-preset.md)

[19.16. 自訂選項](runtime-config-custom.md)

[19.17. 開發人員選項](runtime-config-developer.md)

[19.18. 簡短選項](runtime-config-short.md)

<a id="id-1.6.6.2"></a>

有許多組態設定參數會影響資料庫系統的行為。在本章第一節中，
我們會說明如何與組態設定參數互動。後續各節則會詳細討論每個參數。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config.html)（原文版本：18.6；核對日期：2026-09-24）
