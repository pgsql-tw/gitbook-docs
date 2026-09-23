## 第 18 章 伺服器設定與操作

**目錄**

[18.1. PostgreSQL 使用者帳號](postgres-user.md)

[18.2. 建立資料庫叢集](creating-cluster.md)
:   [18.2.1. 次要檔案系統的使用](creating-cluster.md#CREATING-CLUSTER-MOUNT-POINTS)

    [18.2.2. 檔案系統](creating-cluster.md#CREATING-CLUSTER-FILESYSTEM)

[18.3. 啟動資料庫伺服器](server-start.md)
:   [18.3.1. 伺服器啟動失敗](server-start.md#SERVER-START-FAILURES)

    [18.3.2. 用戶端連線問題](server-start.md#CLIENT-CONNECTION-PROBLEMS)

[18.4. 管理核心資源](kernel-resources.md)
:   [18.4.1. 共享記憶體與號誌（Semaphore）](kernel-resources.md#SYSVIPC)

    [18.4.2. systemd RemoveIPC](kernel-resources.md#SYSTEMD-REMOVEIPC)

    [18.4.3. 資源限制](kernel-resources.md#KERNEL-RESOURCES-LIMITS)

    [18.4.4. Linux 記憶體超額分配（Overcommit）](kernel-resources.md#LINUX-MEMORY-OVERCOMMIT)

    [18.4.5. Linux 大頁（Huge Pages）](kernel-resources.md#LINUX-HUGE-PAGES)

[18.5. 關閉伺服器](server-shutdown.md)

[18.6. 升級 PostgreSQL 叢集](upgrading.md)
:   [18.6.1. 透過 pg_dumpall 升級資料](upgrading.md#UPGRADING-VIA-PGDUMPALL)

    [18.6.2. 透過 pg_upgrade 升級資料](upgrading.md#UPGRADING-VIA-PG-UPGRADE)

    [18.6.3. 透過複寫升級資料](upgrading.md#UPGRADING-VIA-REPLICATION)

[18.7. 防止伺服器被偽造（Spoofing）](preventing-server-spoofing.md)

[18.8. 加密選項](encryption-options.md)

[18.9. 使用 SSL 的安全 TCP/IP 連線](ssl-tcp.md)
:   [18.9.1. 基本設定](ssl-tcp.md#SSL-SETUP)

    [18.9.2. OpenSSL 組態設定](ssl-tcp.md#SSL-OPENSSL-CONFIG)

    [18.9.3. 使用用戶端憑證](ssl-tcp.md#SSL-CLIENT-CERTIFICATES)

    [18.9.4. SSL 伺服器檔案的使用](ssl-tcp.md#SSL-SERVER-FILES)

    [18.9.5. 建立憑證](ssl-tcp.md#SSL-CERTIFICATE-CREATION)

[18.10. 使用 GSSAPI 加密的安全 TCP/IP 連線](gssapi-enc.md)
:   [18.10.1. 基本設定](gssapi-enc.md#GSSAPI-SETUP)

[18.11. 使用 SSH 通道的安全 TCP/IP 連線](ssh-tunnels.md)

[18.12. 在 Windows 註冊事件日誌](event-log-registration.md)

本章討論如何設定並執行資料庫伺服器，
以及它與作業系統之間的互動方式。

本章中的指示，假設您使用的是不含任何額外基礎架構的
純 PostgreSQL，例如依照前幾章的說明，
自原始碼自行建置出來的版本。
若您使用的是預先封裝、或由廠商提供的 PostgreSQL 版本，
封裝提供者很可能已依照您系統的慣例，
針對安裝與啟動資料庫伺服器，做了特別的處理。
詳情請參閱套件層級的相關文件。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime.html)（原文版本：18.6；核對日期：2026-09-22）
