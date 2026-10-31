<a id="REFERENCE-CLIENT"></a>

# PostgreSQL 用戶端應用程式

---

<a id="id-1.9.4.2"></a>

本部分包含 PostgreSQL 用戶端應用程式與工具程式的參考資訊。這些命令並非全都具有一般用途；有些可能需要特殊權限。這些應用程式的共同特點是，無論資料庫伺服器位於何處，都可以在任何主機上執行。

在命令列上指定時，使用者名稱與資料庫名稱會保留其大小寫——若含有空格或特殊字元，可能需要加上引號。資料表名稱與其他識別字則不會保留大小寫（文件另有說明者除外），並且可能需要加上引號。

**目錄**

[clusterdb](app-clusterdb.md) — 叢集化 PostgreSQL 資料庫

[createdb](app-createdb.md) — 建立新的 PostgreSQL 資料庫

[createuser](app-createuser.md) — 定義新的 PostgreSQL 使用者帳號

[dropdb](app-dropdb.md) — 移除 PostgreSQL 資料庫

[dropuser](app-dropuser.md) — 移除 PostgreSQL 使用者帳號

[ecpg](app-ecpg.md) — 嵌入式 SQL C 前置處理器

[pg_amcheck](app-pgamcheck.md) — 檢查一個或多個 PostgreSQL 資料庫是否損毀

[pg_basebackup](app-pgbasebackup.md) — 取得 PostgreSQL 叢集的基礎備份

[pgbench](pgbench.md) — 在 PostgreSQL 上執行效能基準測試

相關子頁：[pgbench 初始化步驟](pgbench-init-steps.md)。

[pg_combinebackup](app-pgcombinebackup.md) — 從增量備份及其相依的備份重建完整備份

[pg_config](app-pgconfig.md) — 取得已安裝之 PostgreSQL 版本的相關資訊

[pg_dump](app-pgdump.md) — 將 PostgreSQL 資料庫匯出為 SQL 腳本或其他格式

[pg_dumpall](app-pg-dumpall.md) — 將 PostgreSQL 資料庫叢集匯出為腳本檔案

[pg_isready](app-pg-isready.md) — 檢查 PostgreSQL 伺服器的連線狀態

[pg_receivewal](app-pgreceivewal.md) — 從 PostgreSQL 伺服器串流接收預寫式日誌

[pg_recvlogical](app-pgrecvlogical.md) — 控制 PostgreSQL 邏輯解碼串流

[pg_restore](app-pgrestore.md) — 從 pg_dump 建立的封存檔還原 PostgreSQL 資料庫

[pg_verifybackup](app-pgverifybackup.md) — 驗證 PostgreSQL 叢集基礎備份的完整性

[psql](app-psql.md) — PostgreSQL 互動式終端機

[reindexdb](app-reindexdb.md) — 重建 PostgreSQL 資料庫的索引

[vacuumdb](app-vacuumdb.md) — 對 PostgreSQL 資料庫進行垃圾回收與分析

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/reference-client.html)（原文版本：18.6；核對日期：2026-10-09）
