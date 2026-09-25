## 第 49 章 封存模組

**目錄**

[49.1. 初始化函式](archive-module-init.md)

[49.2. 封存模組回呼](archive-module-callbacks.md)
:   [49.2.1. 啟動回呼](archive-module-callbacks.md#ARCHIVE-MODULE-STARTUP)

    [49.2.2. 檢查回呼](archive-module-callbacks.md#ARCHIVE-MODULE-CHECK)

    [49.2.3. 封存回呼](archive-module-callbacks.md#ARCHIVE-MODULE-ARCHIVE)

    [49.2.4. 關閉回呼](archive-module-callbacks.md#ARCHIVE-MODULE-SHUTDOWN)

<a id="id-1.8.16.2"></a>

PostgreSQL 提供了基礎架構，可用來建立自訂的連續封存模組
（見[25.3 節](../../server-administration/backup/continuous-archiving.md)）。
雖然透過 shell 指令進行封存（也就是
[archive_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND)）
簡單得多，但自訂封存模組通常會更加穩健且更具效能。

當設定了自訂的
[archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY)
之後，PostgreSQL 會將已完成的 WAL 檔案提交給該模組，
且伺服器在該模組指出這些檔案已成功封存之前，
都會避免回收或移除這些 WAL 檔案。至於每個 WAL 檔案該如何處理，
最終取決於該模組，但
[25.3.1 節](../../server-administration/backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL)
列出了許多建議做法。

封存模組至少必須包含一個初始化函式（見
[49.1 節](archive-module-init.md)）以及所需的回呼函式（見
[49.2 節](archive-module-callbacks.md)）。不過，封存模組
也允許做更多事情（例如宣告 GUC 或註冊背景工作程序）。

`contrib/basic_archive` 模組包含一個可運作的範例，
展示了一些實用的技巧。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/archive-modules.html)（原文版本：18.6；核對日期：2026-09-25）
