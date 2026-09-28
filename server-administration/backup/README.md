## 第 25 章：備份與還原

**目錄**

[25.1. SQL 傾印](backup-dump.md)
:   [25.1.1. 還原傾印內容](backup-dump.md#BACKUP-DUMP-RESTORE)

    [25.1.2. 使用 pg_dumpall](backup-dump.md#BACKUP-DUMP-ALL)

    [25.1.3. 處理大型資料庫](backup-dump.md#BACKUP-DUMP-LARGE)

[25.2. 檔案系統層級備份](backup-file.md)

[25.3. 持續歸檔與時間點還原（PITR）](continuous-archiving.md)
:   [25.3.1. 設定 WAL 歸檔](continuous-archiving.md#BACKUP-ARCHIVING-WAL)

    [25.3.2. 製作基礎備份](continuous-archiving.md#BACKUP-BASE-BACKUP)

    [25.3.3. 製作增量備份](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)

    [25.3.4. 使用低階 API 製作基礎備份](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)

    [25.3.5. 使用持續歸檔備份進行還原](continuous-archiving.md#BACKUP-PITR-RECOVERY)

    [25.3.6. 時間軸](continuous-archiving.md#BACKUP-TIMELINES)

    [25.3.7. 技巧與範例](continuous-archiving.md#BACKUP-TIPS)

    [25.3.8. 注意事項](continuous-archiving.md#CONTINUOUS-ARCHIVING-CAVEATS)

<a id="id-1.6.12.2"></a>

如同任何存放重要資料的系統一樣，PostgreSQL
資料庫應該定期備份。雖然備份程序基本上很簡單，
但重要的是要清楚理解其背後所依據的技術與前提假設。

備份 PostgreSQL 資料有三種根本不同的方式：

* SQL 傾印
* 檔案系統層級備份
* 持續歸檔

每種方式各有其優缺點；以下各節將依序討論每一種方式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup.html)（原文版本：18.6；核對日期：2026-09-28）
