## 第 24 章、常規資料庫維護工作

**目錄**

[24.1. 常規 VACUUM 作業](routine-vacuuming.md)
:   [24.1.1. VACUUM 基礎知識](routine-vacuuming.md#VACUUM-BASICS)

    [24.1.2. 回收磁碟空間](routine-vacuuming.md#VACUUM-FOR-SPACE-RECOVERY)

    [24.1.3. 更新規劃器統計資訊](routine-vacuuming.md#VACUUM-FOR-STATISTICS)

    [24.1.4. 更新可見性對照表](routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)

    [24.1.5. 避免交易 ID 回卷失敗](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)

    [24.1.6. Autovacuum 常駐程序](routine-vacuuming.md#AUTOVACUUM)

[24.2. 常規重新索引](routine-reindex.md)

[24.3. 日誌檔維護](logfile-maintenance.md)

<a id="id-1.6.11.2"></a><a id="id-1.6.11.3"></a>

PostgreSQL 和任何資料庫軟體一樣，需要定期執行某些工作，
才能達到最佳效能。這裡所討論的工作都是*必要*的，
但它們本質上具有重複性，可以很容易地透過 cron 指令碼
或 Windows 的工作排程器（Task Scheduler）等標準工具來自動化。
設定適當的指令碼、並檢查它們確實成功執行，是資料庫管理員的責任。

一項顯而易見的維護工作，是定期建立資料的備份副本。
如果沒有近期的備份，一旦發生災難（例如磁碟故障、火災、
不慎刪除重要資料表等），你就完全沒有復原的機會。
PostgreSQL 提供的備份與復原機制，
在[第 25 章](../backup/README.md)中有詳盡的討論。

另一大類主要的維護工作，是定期對資料庫進行「VACUUM 清理」。
這項作業在[第 24.1 節](routine-vacuuming.md)中有所討論。
與此密切相關的，是更新查詢規劃器所使用的統計資訊，
這部分則在[第 24.1.3 節](routine-vacuuming.md#VACUUM-FOR-STATISTICS)中討論。

另一項可能需要定期關注的工作，是日誌檔管理，
這部分在[第 24.3 節](logfile-maintenance.md)中討論。

[check_postgres](https://bucardo.org/check_postgres/)
可用來監控資料庫健康狀態，並回報異常情況。check_postgres
可與 Nagios 及 MRTG 整合，但也可以獨立執行。

相較於其他一些資料庫管理系統，PostgreSQL 屬於低維護需求的系統。
儘管如此，對這些工作給予適當的關注，將大大有助於確保你在使用
這套系統時，能有愉快而高效的體驗。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/maintenance.html)（原文版本：18.6；核對日期：2026-09-25）
