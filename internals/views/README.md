<a id="VIEWS"></a>

## 第 53 章 系統檢視表

**目錄**

[53.1. 概觀](views-overview.md)

[53.2. `pg_aios`](view-pg-aios.md)

[53.3. `pg_available_extensions`](view-pg-available-extensions.md)

[53.4. `pg_available_extension_versions`](view-pg-available-extension-versions.md)

[53.5. `pg_backend_memory_contexts`](view-pg-backend-memory-contexts.md)

[53.6. `pg_config`](view-pg-config.md)

[53.7. `pg_cursors`](view-pg-cursors.md)

[53.8. `pg_file_settings`](view-pg-file-settings.md)

[53.9. `pg_group`](view-pg-group.md)

[53.10. `pg_hba_file_rules`](view-pg-hba-file-rules.md)

[53.11. `pg_ident_file_mappings`](view-pg-ident-file-mappings.md)

[53.12. `pg_indexes`](view-pg-indexes.md)

[53.13. `pg_locks`](view-pg-locks.md)

[53.14. `pg_matviews`](view-pg-matviews.md)

[53.15. `pg_policies`](view-pg-policies.md)

[53.16. `pg_prepared_statements`](view-pg-prepared-statements.md)

[53.17. `pg_prepared_xacts`](view-pg-prepared-xacts.md)

[53.18. `pg_publication_tables`](view-pg-publication-tables.md)

[53.19. `pg_replication_origin_status`](view-pg-replication-origin-status.md)

[53.20. `pg_replication_slots`](view-pg-replication-slots.md)

[53.21. `pg_roles`](view-pg-roles.md)

[53.22. `pg_rules`](view-pg-rules.md)

[53.23. `pg_seclabels`](view-pg-seclabels.md)

[53.24. `pg_sequences`](view-pg-sequences.md)

[53.25. `pg_settings`](view-pg-settings.md)

[53.26. `pg_shadow`](view-pg-shadow.md)

[53.27. `pg_shmem_allocations`](view-pg-shmem-allocations.md)

[53.28. `pg_shmem_allocations_numa`](view-pg-shmem-allocations-numa.md)

[53.29. `pg_stats`](view-pg-stats.md)

[53.30. `pg_stats_ext`](view-pg-stats-ext.md)

[53.31. `pg_stats_ext_exprs`](view-pg-stats-ext-exprs.md)

[53.32. `pg_tables`](view-pg-tables.md)

[53.33. `pg_timezone_abbrevs`](view-pg-timezone-abbrevs.md)

[53.34. `pg_timezone_names`](view-pg-timezone-names.md)

[53.35. `pg_user`](view-pg-user.md)

[53.36. `pg_user_mappings`](view-pg-user-mappings.md)

[53.37. `pg_views`](view-pg-views.md)

[53.38. `pg_wait_events`](view-pg-wait-events.md)

除了系統目錄之外，PostgreSQL 還提供了一些內建的檢視表。有些系統檢視表讓你能方便地取用一些對系統目錄常用的查詢；其他檢視表則提供對伺服器內部狀態的存取。

資訊綱要（[第 35 章](../../client-interfaces/information-schema/README.md)）提供了另一組檢視表，其功能與系統檢視表有所重疊。由於資訊綱要屬於 SQL 標準，而此處描述的檢視表是 PostgreSQL 特有的，因此如果資訊綱要能提供你所需的全部資訊，通常最好使用資訊綱要。

[表 53.1](views-overview.md#VIEW-TABLE) 列出此處描述的系統檢視表。後文接著提供每個檢視表更詳細的說明。另外還有一些提供累積統計資訊存取的檢視表，它們描述於
[表 27.2](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-VIEWS-TABLE)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/views.html)（原文版本：18.6；核對日期：2026-10-12）
