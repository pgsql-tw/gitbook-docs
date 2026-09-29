# 第 III 部：伺服器管理

<a id="id-1.6.2"></a>

本部涵蓋 PostgreSQL 管理者會感興趣的主題，
包括安裝、伺服器設定、使用者與資料庫的管理，以及維護工作。
任何執行 PostgreSQL 伺服器的人，即使只是個人使用，
但尤其是在正式環境中使用時，都應該熟悉這些主題。

本部的資訊嘗試依照新使用者應該閱讀的順序來安排。
各章節本身內容完整，可依需要單獨閱讀。這些資訊是以主題單元的方式，
用敘事的形式呈現。若讀者想尋找某個指令的完整說明，
建議參閱 [第 VI 部](../reference/README.md)。

最初幾章的撰寫方式，不需要任何先備知識即可理解，
因此需要自行架設伺服器的新使用者可以由此開始探索。
本部其餘部分則是關於調校與管理；這部分的內容假設讀者已熟悉
PostgreSQL 資料庫系統的一般使用方式。
建議讀者參閱 [第 I 部](../tutorial/README.md) 與
[第 II 部](../the-sql-language/README.md) 以取得補充資訊。

**目錄**

[第 16 章：從二進位檔安裝](install-binaries/README.md)

[第 17 章：從原始碼安裝](installation/README.md)
:   [17.1. 需求](installation/install-requirements.md)

    [17.2. 取得原始碼](installation/install-getsource.md)

    [17.3. 使用 Autoconf 與 Make 建置與安裝](installation/install-make.md)

    [17.4. 使用 Meson 建置與安裝](installation/install-meson.md)

    [17.5. 安裝後設定](installation/install-post.md)

    [17.6. 支援的平台](installation/supported-platforms.md)

    [17.7. 特定平台注意事項](installation/installation-platform-notes.md)

[第 18 章：伺服器設定與運作](runtime/README.md)
:   [18.1. PostgreSQL 使用者帳號](runtime/postgres-user.md)

    [18.2. 建立資料庫叢集](runtime/creating-cluster.md)

    [18.3. 啟動資料庫伺服器](runtime/server-start.md)

    [18.4. 管理核心資源](runtime/kernel-resources.md)

    [18.5. 關閉伺服器](runtime/server-shutdown.md)

    [18.6. 升級 PostgreSQL 叢集](runtime/upgrading.md)

    [18.7. 防止伺服器偽冒](runtime/preventing-server-spoofing.md)

    [18.8. 加密選項](runtime/encryption-options.md)

    [18.9. 使用 SSL 建立安全的 TCP/IP 連線](runtime/ssl-tcp.md)

    [18.10. 使用 GSSAPI 加密建立安全的 TCP/IP 連線](runtime/gssapi-enc.md)

    [18.11. 使用 SSH 通道建立安全的 TCP/IP 連線](runtime/ssh-tunnels.md)

    [18.12. 在 Windows 上註冊事件日誌](runtime/event-log-registration.md)

[第 19 章：伺服器設定](runtime-config/README.md)
:   [19.1. 設定參數](runtime-config/config-setting.md)

    [19.2. 檔案位置](runtime-config/runtime-config-file-locations.md)

    [19.3. 連線與驗證](runtime-config/runtime-config-connection.md)

    [19.4. 資源耗用](runtime-config/runtime-config-resource.md)

    [19.5. 預寫日誌](runtime-config/runtime-config-wal.md)

    [19.6. 複寫](runtime-config/runtime-config-replication.md)

    [19.7. 查詢規劃](runtime-config/runtime-config-query.md)

    [19.8. 錯誤回報與日誌記錄](runtime-config/runtime-config-logging.md)

    [19.9. 執行期統計資訊](runtime-config/runtime-config-statistics.md)

    [19.10. 資料清理（Vacuuming）](runtime-config/runtime-config-vacuum.md)

    [19.11. 用戶端連線預設值](runtime-config/runtime-config-client.md)

    [19.12. 鎖定管理](runtime-config/runtime-config-locks.md)

    [19.13. 版本與平台相容性](runtime-config/runtime-config-compatible.md)

    [19.14. 錯誤處理](runtime-config/runtime-config-error-handling.md)

    [19.15. 預先設定的選項](runtime-config/runtime-config-preset.md)

    [19.16. 自訂選項](runtime-config/runtime-config-custom.md)

    [19.17. 開發者選項](runtime-config/runtime-config-developer.md)

    [19.18. 簡寫選項](runtime-config/runtime-config-short.md)

[第 20 章：用戶端驗證](client-authentication/README.md)
:   [20.1. `pg_hba.conf` 檔案](client-authentication/auth-pg-hba-conf.md)

    [20.2. 使用者名稱對應](client-authentication/auth-username-maps.md)

    [20.3. 驗證方法](client-authentication/auth-methods.md)

    [20.4. Trust 驗證](client-authentication/auth-trust.md)

    [20.5. 密碼驗證](client-authentication/auth-password.md)

    [20.6. GSSAPI 驗證](client-authentication/gssapi-auth.md)

    [20.7. SSPI 驗證](client-authentication/sspi-auth.md)

    [20.8. Ident 驗證](client-authentication/auth-ident.md)

    [20.9. Peer 驗證](client-authentication/auth-peer.md)

    [20.10. LDAP 驗證](client-authentication/auth-ldap.md)

    [20.11. RADIUS 驗證](client-authentication/auth-radius.md)

    [20.12. 憑證驗證](client-authentication/auth-cert.md)

    [20.13. PAM 驗證](client-authentication/auth-pam.md)

    [20.14. BSD 驗證](client-authentication/auth-bsd.md)

    [20.15. OAuth 授權／驗證](client-authentication/auth-oauth.md)

    [20.16. 驗證疑難排解](client-authentication/client-authentication-problems.md)

[第 21 章：資料庫角色](user-manag/README.md)
:   [21.1. 資料庫角色](user-manag/database-roles.md)

    [21.2. 角色屬性](user-manag/role-attributes.md)

    [21.3. 角色成員資格](user-manag/role-membership.md)

    [21.4. 刪除角色](user-manag/role-removal.md)

    [21.5. 預先定義的角色](user-manag/predefined-roles.md)

    [21.6. 函式安全性](user-manag/perm-functions.md)

[第 22 章：管理資料庫](managing-databases/README.md)
:   [22.1. 概觀](managing-databases/manage-ag-overview.md)

    [22.2. 建立資料庫](managing-databases/manage-ag-createdb.md)

    [22.3. 範本資料庫](managing-databases/manage-ag-templatedbs.md)

    [22.4. 資料庫設定](managing-databases/manage-ag-config.md)

    [22.5. 刪除資料庫](managing-databases/manage-ag-dropdb.md)

    [22.6. 資料表空間](managing-databases/manage-ag-tablespaces.md)

[第 23 章：在地化](charset/README.md)
:   [23.1. 地區設定支援](charset/locale.md)

    [23.2. 定序支援](charset/collation.md)

    [23.3. 字元集支援](charset/multibyte.md)

[第 24 章：例行性資料庫維護工作](maintenance/README.md)
:   [24.1. 例行性資料清理（Vacuuming）](maintenance/routine-vacuuming.md)

    [24.2. 例行性重建索引](maintenance/routine-reindex.md)

    [24.3. 日誌檔維護](maintenance/logfile-maintenance.md)

[第 25 章：備份與還原](backup/README.md)
:   [25.1. SQL 傾印](backup/backup-dump.md)

    [25.2. 檔案系統層級備份](backup/backup-file.md)

    [25.3. 持續歸檔與時間點還原（PITR）](backup/continuous-archiving.md)

[第 26 章：高可用性、負載平衡與複寫](high-availability/README.md)
:   [26.1. 不同解決方案的比較](high-availability/different-replication-solutions.md)

    [26.2. 日誌傳送備援伺服器](high-availability/warm-standby.md)

    [26.3. 容錯移轉](high-availability/warm-standby-failover.md)

    [26.4. 熱備援](high-availability/hot-standby.md)

[第 27 章：監控資料庫活動](monitoring/README.md)
:   [27.1. 標準 Unix 工具](monitoring/monitoring-ps.md)

    [27.2. 累積統計資訊系統](monitoring/monitoring-stats.md)

    [27.3. 檢視鎖定](monitoring/monitoring-locks.md)

    [27.4. 進度回報](monitoring/progress-reporting.md)

    [27.5. 動態追蹤](monitoring/dynamic-trace.md)

    [27.6. 監控磁碟用量](monitoring/diskusage.md)

[第 28 章：可靠性與預寫日誌](wal/README.md)
:   [28.1. 可靠性](wal/wal-reliability.md)

    [28.2. 資料檢查碼](wal/checksums.md)

    [28.3. 預寫日誌（WAL）](wal/wal-intro.md)

    [28.4. 非同步提交](wal/wal-async-commit.md)

    [28.5. WAL 設定](wal/wal-configuration.md)

    [28.6. WAL 內部機制](wal/wal-internals.md)

[第 29 章：邏輯複寫](logical-replication/README.md)
:   [29.1. 發佈](logical-replication/logical-replication-publication.md)

    [29.2. 訂閱](logical-replication/logical-replication-subscription.md)

    [29.3. 邏輯複寫容錯移轉](logical-replication/logical-replication-failover.md)

    [29.4. 資料列篩選器](logical-replication/logical-replication-row-filter.md)

    [29.5. 欄位清單](logical-replication/logical-replication-col-lists.md)

    [29.6. 產生欄位的複寫](logical-replication/logical-replication-gencols.md)

    [29.7. 衝突](logical-replication/logical-replication-conflicts.md)

    [29.8. 限制](logical-replication/logical-replication-restrictions.md)

    [29.9. 架構](logical-replication/logical-replication-architecture.md)

    [29.10. 監控](logical-replication/logical-replication-monitoring.md)

    [29.11. 安全性](logical-replication/logical-replication-security.md)

    [29.12. 設定值](logical-replication/logical-replication-config.md)

    [29.13. 升級](logical-replication/logical-replication-upgrade.md)

    [29.14. 快速設定](logical-replication/logical-replication-quick-setup.md)

[第 30 章：即時編譯（JIT）](jit/README.md)
:   [30.1. 什麼是 JIT 編譯？](jit/jit-reason.md)

    [30.2. 何時該使用 JIT？](jit/jit-decision.md)

    [30.3. 設定](jit/jit-configuration.md)

    [30.4. 可延伸性](jit/jit-extensibility.md)

[第 31 章：迴歸測試](regress/README.md)
:   [31.1. 執行測試](regress/regress-run.md)

    [31.2. 測試評估](regress/regress-evaluation.md)

    [31.3. 變體比較檔](regress/regress-variant.md)

    [31.4. TAP 測試](regress/regress-tap.md)

    [31.5. 測試涵蓋率檢查](regress/regress-coverage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/admin.html)（原文版本：18.6；核對日期：2026-09-28）
