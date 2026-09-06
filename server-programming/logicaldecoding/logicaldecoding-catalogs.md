## 47.5. 與邏輯解碼相關的系統目錄 [#](#LOGICALDECODING-CATALOGS)

[`pg_replication_slots`](../../internals/views/view-pg-replication-slots.md) 檢視表與 [`pg_stat_replication`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW) 檢視表，分別提供複寫槽與串流複寫連線目前狀態的資訊。這些檢視表同時適用於實體複寫與邏輯複寫。[`pg_stat_replication_slots`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) 檢視表則提供邏輯複寫槽的統計資訊。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-catalogs.html)（原文版本：18.6；核對日期：2026-09-07）
