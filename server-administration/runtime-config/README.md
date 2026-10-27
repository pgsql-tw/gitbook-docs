<a id="RUNTIME-CONFIG"></a>

## 第 19 章、伺服器組態設定

**目錄**

- [19.1. 設定參數](config-setting.md)
  - [19.1.1. 參數名稱與數值](config-setting.md#config-setting-names-values)

  - [19.1.2. 透過組態設定檔進行參數互動](config-setting.md#config-setting-configuration-file)

  - [19.1.3. 透過 SQL 進行參數互動](config-setting.md#config-setting-sql)

  - [19.1.4. 透過 Shell 進行參數互動](config-setting.md#config-setting-shell)

  - [19.1.5. 管理組態設定檔內容](config-setting.md#config-includes)

- [19.2. 檔案位置](runtime-config-file-locations.md)

- [19.3. 連線與驗證](runtime-config-connection.md)
  - [19.3.1. 連線設定](runtime-config-connection.md#runtime-config-connection-settings)

  - [19.3.2. TCP 設定](runtime-config-connection.md#runtime-config-tcp-settings)

  - [19.3.3. 驗證](runtime-config-connection.md#runtime-config-connection-authentication)

  - [19.3.4. SSL](runtime-config-connection.md#runtime-config-connection-ssl)

- [19.4. 資源消耗](runtime-config-resource.md)
  - [19.4.1. 記憶體](runtime-config-resource.md#runtime-config-resource-memory)

  - [19.4.2. 磁碟](runtime-config-resource.md#runtime-config-resource-disk)

  - [19.4.3. 核心資源使用量](runtime-config-resource.md#runtime-config-resource-kernel)

  - [19.4.4. 背景寫入程序](runtime-config-resource.md#runtime-config-resource-background-writer)

  - [19.4.5. I/O](runtime-config-resource.md#runtime-config-resource-io)

  - [19.4.6. 工作程序](runtime-config-resource.md#runtime-config-resource-worker-processes)

- [19.5. 預寫日誌](runtime-config-wal.md)
  - [19.5.1. 設定](runtime-config-wal.md#runtime-config-wal-settings)

  - [19.5.2. 檢查點](runtime-config-wal.md#runtime-config-wal-checkpoints)

  - [19.5.3. 歸檔](runtime-config-wal.md#runtime-config-wal-archiving)

  - [19.5.4. 復原](runtime-config-wal.md#runtime-config-wal-recovery)

  - [19.5.5. 歸檔復原](runtime-config-wal.md#runtime-config-wal-archive-recovery)

  - [19.5.6. 復原目標](runtime-config-wal.md#runtime-config-wal-recovery-target)

  - [19.5.7. WAL 摘要化](runtime-config-wal.md#runtime-config-wal-summarization)

- [19.6. 複製](runtime-config-replication.md)
  - [19.6.1. 傳送端伺服器](runtime-config-replication.md#runtime-config-replication-sender)

  - [19.6.2. 主要伺服器](runtime-config-replication.md#runtime-config-replication-primary)

  - [19.6.3. 待命伺服器](runtime-config-replication.md#runtime-config-replication-standby)

  - [19.6.4. 訂閱端](runtime-config-replication.md#runtime-config-replication-subscriber)

- [19.7. 查詢規劃](runtime-config-query.md)
  - [19.7.1. 規劃器方法組態設定](runtime-config-query.md#runtime-config-query-enable)

  - [19.7.2. 規劃器成本常數](runtime-config-query.md#runtime-config-query-constants)

  - [19.7.3. 基因查詢最佳化器](runtime-config-query.md#runtime-config-query-geqo)

  - [19.7.4. 其他規劃器選項](runtime-config-query.md#runtime-config-query-other)

- [19.8. 錯誤回報與日誌](runtime-config-logging.md)
  - [19.8.1. 記錄到何處](runtime-config-logging.md#runtime-config-logging-where)

  - [19.8.2. 何時記錄](runtime-config-logging.md#runtime-config-logging-when)

  - [19.8.3. 記錄什麼內容](runtime-config-logging.md#runtime-config-logging-what)

  - [19.8.4. 使用 CSV 格式日誌輸出](runtime-config-logging.md#runtime-config-logging-csvlog)

  - [19.8.5. 使用 JSON 格式日誌輸出](runtime-config-logging.md#runtime-config-logging-jsonlog)

  - [19.8.6. 程序標題](runtime-config-logging.md#runtime-config-logging-proc-title)

- [19.9. 執行時期統計資訊](runtime-config-statistics.md)
  - [19.9.1. 累計查詢與索引統計資訊](runtime-config-statistics.md#runtime-config-cumulative-statistics)

  - [19.9.2. 統計資訊監控](runtime-config-statistics.md#runtime-config-statistics-monitor)

- [19.10. Vacuum 處理](runtime-config-vacuum.md)
  - [19.10.1. 自動 Vacuum](runtime-config-vacuum.md#runtime-config-autovacuum)

  - [19.10.2. 以成本為基礎的 Vacuum 延遲](runtime-config-vacuum.md#runtime-config-resource-vacuum-cost)

  - [19.10.3. 預設行為](runtime-config-vacuum.md#runtime-config-vacuum-default)

  - [19.10.4. 凍結](runtime-config-vacuum.md#runtime-config-vacuum-freezing)

- [19.11. 用戶端連線預設值](runtime-config-client.md)
  - [19.11.1. 陳述式行為](runtime-config-client.md#runtime-config-client-statement)

  - [19.11.2. 地區設定與格式化](runtime-config-client.md#runtime-config-client-format)

  - [19.11.3. 共享程式庫預先載入](runtime-config-client.md#runtime-config-client-preload)

  - [19.11.4. 其他預設值](runtime-config-client.md#runtime-config-client-other)

- [19.12. 鎖定管理](runtime-config-locks.md)

- [19.13. 版本與平台相容性](runtime-config-compatible.md)
  - [19.13.1. 舊版 PostgreSQL](runtime-config-compatible.md#runtime-config-compatible-version)

  - [19.13.2. 平台與用戶端相容性](runtime-config-compatible.md#runtime-config-compatible-clients)

- [19.14. 錯誤處理](runtime-config-error-handling.md)

- [19.15. 預設選項](runtime-config-preset.md)

- [19.16. 自訂選項](runtime-config-custom.md)

- [19.17. 開發人員選項](runtime-config-developer.md)

- [19.18. 簡短選項](runtime-config-short.md)

<a id="id-1.6.6.2"></a>

有許多組態設定參數會影響資料庫系統的行為。在本章第一節中，
我們會說明如何與組態設定參數互動。後續各節則會詳細討論每個參數。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config.html)（原文版本：18.6；核對日期：2026-09-24）
