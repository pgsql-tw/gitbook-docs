<a id="MONITORING"></a>

## 第 27 章 監控資料庫活動

**目錄**

- [27.1. 標準 Unix 工具](monitoring-ps.md)

- [27.2. 累積統計資訊系統](monitoring-stats.md)
  - [27.2.1. 統計資訊收集設定](monitoring-stats.md#monitoring-stats-setup)

  - [27.2.2. 檢視統計資訊](monitoring-stats.md#monitoring-stats-views)

  - [27.2.3. `pg_stat_activity`](monitoring-stats.md#monitoring-pg-stat-activity-view)

  - [27.2.4. `pg_stat_replication`](monitoring-stats.md#monitoring-pg-stat-replication-view)

  - [27.2.5. `pg_stat_replication_slots`](monitoring-stats.md#monitoring-pg-stat-replication-slots-view)

  - [27.2.6. `pg_stat_wal_receiver`](monitoring-stats.md#monitoring-pg-stat-wal-receiver-view)

  - [27.2.7. `pg_stat_recovery_prefetch`](monitoring-stats.md#monitoring-pg-stat-recovery-prefetch)

  - [27.2.8. `pg_stat_subscription`](monitoring-stats.md#monitoring-pg-stat-subscription)

  - [27.2.9. `pg_stat_subscription_stats`](monitoring-stats.md#monitoring-pg-stat-subscription-stats)

  - [27.2.10. `pg_stat_ssl`](monitoring-stats.md#monitoring-pg-stat-ssl-view)

  - [27.2.11. `pg_stat_gssapi`](monitoring-stats.md#monitoring-pg-stat-gssapi-view)

  - [27.2.12. `pg_stat_archiver`](monitoring-stats.md#monitoring-pg-stat-archiver-view)

  - [27.2.13. `pg_stat_io`](monitoring-stats.md#monitoring-pg-stat-io-view)

  - [27.2.14. `pg_stat_bgwriter`](monitoring-stats.md#monitoring-pg-stat-bgwriter-view)

  - [27.2.15. `pg_stat_checkpointer`](monitoring-stats.md#monitoring-pg-stat-checkpointer-view)

  - [27.2.16. `pg_stat_wal`](monitoring-stats.md#monitoring-pg-stat-wal-view)

  - [27.2.17. `pg_stat_database`](monitoring-stats.md#monitoring-pg-stat-database-view)

  - [27.2.18. `pg_stat_database_conflicts`](monitoring-stats.md#monitoring-pg-stat-database-conflicts-view)

  - [27.2.19. `pg_stat_all_tables`](monitoring-stats.md#monitoring-pg-stat-all-tables-view)

  - [27.2.20. `pg_stat_all_indexes`](monitoring-stats.md#monitoring-pg-stat-all-indexes-view)

  - [27.2.21. `pg_statio_all_tables`](monitoring-stats.md#monitoring-pg-statio-all-tables-view)

  - [27.2.22. `pg_statio_all_indexes`](monitoring-stats.md#monitoring-pg-statio-all-indexes-view)

  - [27.2.23. `pg_statio_all_sequences`](monitoring-stats.md#monitoring-pg-statio-all-sequences-view)

  - [27.2.24. `pg_stat_user_functions`](monitoring-stats.md#monitoring-pg-stat-user-functions-view)

  - [27.2.25. `pg_stat_slru`](monitoring-stats.md#monitoring-pg-stat-slru-view)

  - [27.2.26. 統計資訊函式](monitoring-stats.md#monitoring-stats-functions)

- [27.3. 檢視鎖定](monitoring-locks.md)

- [27.4. 進度回報](progress-reporting.md)
  - [27.4.1. ANALYZE 進度回報](progress-reporting.md#analyze-progress-reporting)

  - [27.4.2. CLUSTER 進度回報](progress-reporting.md#cluster-progress-reporting)

  - [27.4.3. COPY 進度回報](progress-reporting.md#copy-progress-reporting)

  - [27.4.4. CREATE INDEX 進度回報](progress-reporting.md#create-index-progress-reporting)

  - [27.4.5. VACUUM 進度回報](progress-reporting.md#vacuum-progress-reporting)

  - [27.4.6. 基礎備份進度回報](progress-reporting.md#basebackup-progress-reporting)

- [27.5. 動態追蹤](dynamic-trace.md)
  - [27.5.1. 為動態追蹤編譯](dynamic-trace.md#compiling-for-trace)

  - [27.5.2. 內建探針](dynamic-trace.md#trace-points)

  - [27.5.3. 使用探針](dynamic-trace.md#using-trace-points)

  - [27.5.4. 定義新探針](dynamic-trace.md#defining-trace-points)

- [27.6. 監控磁碟用量](diskusage.md)
  - [27.6.1. 判斷磁碟用量](diskusage.md#disk-usage)

  - [27.6.2. 磁碟已滿故障](diskusage.md#disk-full)

<a id="id-1.6.14.2"></a><a id="id-1.6.14.3"></a>

資料庫管理員常常會想：「系統現在正在做什麼？」
本章討論如何找出答案。

有好幾種工具可用來監控資料庫活動與分析效能。
本章大部分內容在說明
PostgreSQL 的累積統計資訊系統，
但也不應忽略一般的 Unix 監控程式，例如
`ps`、`top`、`iostat` 與 `vmstat`。
此外，一旦找出了
效能不佳的查詢，可能還需要使用
PostgreSQL 的 [`EXPLAIN`](../../reference/sql-commands/sql-explain.md) 命令進一步調查。
[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)討論了 `EXPLAIN`
以及其他用來了解個別查詢行為的方法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring.html)（原文版本：18.6；核對日期：2026-10-10）
