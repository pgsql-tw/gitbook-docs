## Chapter 27. Monitoring Database Activity

**Table of Contents**

[27.1. Standard Unix Tools](monitoring-ps.md)

[27.2. The Cumulative Statistics System](monitoring-stats.md)
:   [27.2.1. Statistics Collection Configuration](monitoring-stats.md#MONITORING-STATS-SETUP)

    [27.2.2. Viewing Statistics](monitoring-stats.md#MONITORING-STATS-VIEWS)

    [27.2.3. `pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)

    [27.2.4. `pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)

    [27.2.5. `pg_stat_replication_slots`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)

    [27.2.6. `pg_stat_wal_receiver`](monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)

    [27.2.7. `pg_stat_recovery_prefetch`](monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH)

    [27.2.8. `pg_stat_subscription`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION)

    [27.2.9. `pg_stat_subscription_stats`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS)

    [27.2.10. `pg_stat_ssl`](monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW)

    [27.2.11. `pg_stat_gssapi`](monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW)

    [27.2.12. `pg_stat_archiver`](monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW)

    [27.2.13. `pg_stat_io`](monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)

    [27.2.14. `pg_stat_bgwriter`](monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW)

    [27.2.15. `pg_stat_checkpointer`](monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)

    [27.2.16. `pg_stat_wal`](monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW)

    [27.2.17. `pg_stat_database`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)

    [27.2.18. `pg_stat_database_conflicts`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)

    [27.2.19. `pg_stat_all_tables`](monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)

    [27.2.20. `pg_stat_all_indexes`](monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW)

    [27.2.21. `pg_statio_all_tables`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW)

    [27.2.22. `pg_statio_all_indexes`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)

    [27.2.23. `pg_statio_all_sequences`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)

    [27.2.24. `pg_stat_user_functions`](monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)

    [27.2.25. `pg_stat_slru`](monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW)

    [27.2.26. Statistics Functions](monitoring-stats.md#MONITORING-STATS-FUNCTIONS)

[27.3. Viewing Locks](monitoring-locks.md)

[27.4. Progress Reporting](progress-reporting.md)
:   [27.4.1. ANALYZE Progress Reporting](progress-reporting.md#ANALYZE-PROGRESS-REPORTING)

    [27.4.2. CLUSTER Progress Reporting](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)

    [27.4.3. COPY Progress Reporting](progress-reporting.md#COPY-PROGRESS-REPORTING)

    [27.4.4. CREATE INDEX Progress Reporting](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)

    [27.4.5. VACUUM Progress Reporting](progress-reporting.md#VACUUM-PROGRESS-REPORTING)

    [27.4.6. Base Backup Progress Reporting](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING)

[27.5. Dynamic Tracing](dynamic-trace.md)
:   [27.5.1. Compiling for Dynamic Tracing](dynamic-trace.md#COMPILING-FOR-TRACE)

    [27.5.2. Built-in Probes](dynamic-trace.md#TRACE-POINTS)

    [27.5.3. Using Probes](dynamic-trace.md#USING-TRACE-POINTS)

    [27.5.4. Defining New Probes](dynamic-trace.md#DEFINING-TRACE-POINTS)

[27.6. Monitoring Disk Usage](diskusage.md)
:   [27.6.1. Determining Disk Usage](diskusage.md#DISK-USAGE)

    [27.6.2. Disk Full Failure](diskusage.md#DISK-FULL)

<a id="id-1.6.14.2"></a><a id="id-1.6.14.3"></a>

A database administrator frequently wonders, “What is the system
doing right now?”
This chapter discusses how to find that out.

Several tools are available for monitoring database activity and
analyzing performance. Most of this chapter is devoted to describing
PostgreSQL's cumulative statistics system,
but one should not neglect regular Unix monitoring programs such as
`ps`, `top`, `iostat`, and `vmstat`.
Also, once one has identified a
poorly-performing query, further investigation might be needed using
PostgreSQL's [`EXPLAIN`](../../reference/sql-commands/sql-explain.md) command.
[Section 14.1](../../the-sql-language/performance-tips/using-explain.md) discusses `EXPLAIN`
and other methods for understanding the behavior of an individual
query.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring.html)（英文原文，待翻譯）
