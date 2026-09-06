## 47.5. System Catalogs Related to Logical Decoding [#](#LOGICALDECODING-CATALOGS)

The [`pg_replication_slots`](../../internals/views/view-pg-replication-slots.md)
view and the
[`pg_stat_replication`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)
view provide information about the current state of replication slots and
streaming replication connections respectively. These views apply to both physical and
logical replication. The
[`pg_stat_replication_slots`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)
view provides statistics information about the logical replication slots.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-catalogs.html)（英文原文，待翻譯）
