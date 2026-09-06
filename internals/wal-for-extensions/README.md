## 第 64 章 擴充套件的預寫式日誌

**目錄**

[64.1. 通用 WAL 記錄](generic-wal.md)

[64.2. 自訂 WAL 資源管理器](custom-rmgr.md)

某些擴充套件，主要是實作自訂存取方法的擴充套件，可能需要使用預寫式日誌，以確保當機時的安全性。PostgreSQL 提供兩種方式來達成此目標。

第一種方式是使用[通用 WAL](generic-wal.md)，這是一種以通用方式描述頁面變更的特殊 WAL 記錄。此方法容易實作，而且套用記錄時不需要載入擴充套件程式庫。不過，執行邏輯解碼時會忽略通用 WAL 記錄。

第二種方式是使用[自訂資源管理器](custom-rmgr.md)。此方法更有彈性，支援邏輯解碼，有時能產生比通用 WAL 小得多的預寫式日誌記錄。不過，擴充套件的實作也會更複雜。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/wal-for-extensions.html)（原文版本：18.6；核對日期：2026-09-07）
