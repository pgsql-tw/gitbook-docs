# Part VII. Internals

<a id="id-1.10.2"></a>

This part contains assorted information that might be of use to
PostgreSQL developers.

**Table of Contents**

[51. Overview of PostgreSQL Internals](overview/README.md)
:   [51.1. The Path of a Query](overview/query-path.md)

    [51.2. How Connections Are Established](overview/connect-estab.md)

    [51.3. The Parser Stage](overview/parser-stage.md)

    [51.4. The PostgreSQL Rule System](overview/rule-system.md)

    [51.5. Planner/Optimizer](overview/planner-optimizer.md)

    [51.6. Executor](overview/executor.md)

[52. System Catalogs](catalogs/README.md)
:   [52.1. Overview](catalogs/catalogs-overview.md)

    [52.2. `pg_aggregate`](catalogs/catalog-pg-aggregate.md)

    [52.3. `pg_am`](catalogs/catalog-pg-am.md)

    [52.4. `pg_amop`](catalogs/catalog-pg-amop.md)

    [52.5. `pg_amproc`](catalogs/catalog-pg-amproc.md)

    [52.6. `pg_attrdef`](catalogs/catalog-pg-attrdef.md)

    [52.7. `pg_attribute`](catalogs/catalog-pg-attribute.md)

    [52.8. `pg_authid`](catalogs/catalog-pg-authid.md)

    [52.9. `pg_auth_members`](catalogs/catalog-pg-auth-members.md)

    [52.10. `pg_cast`](catalogs/catalog-pg-cast.md)

    [52.11. `pg_class`](catalogs/catalog-pg-class.md)

    [52.12. `pg_collation`](catalogs/catalog-pg-collation.md)

    [52.13. `pg_constraint`](catalogs/catalog-pg-constraint.md)

    [52.14. `pg_conversion`](catalogs/catalog-pg-conversion.md)

    [52.15. `pg_database`](catalogs/catalog-pg-database.md)

    [52.16. `pg_db_role_setting`](catalogs/catalog-pg-db-role-setting.md)

    [52.17. `pg_default_acl`](catalogs/catalog-pg-default-acl.md)

    [52.18. `pg_depend`](catalogs/catalog-pg-depend.md)

    [52.19. `pg_description`](catalogs/catalog-pg-description.md)

    [52.20. `pg_enum`](catalogs/catalog-pg-enum.md)

    [52.21. `pg_event_trigger`](catalogs/catalog-pg-event-trigger.md)

    [52.22. `pg_extension`](catalogs/catalog-pg-extension.md)

    [52.23. `pg_foreign_data_wrapper`](catalogs/catalog-pg-foreign-data-wrapper.md)

    [52.24. `pg_foreign_server`](catalogs/catalog-pg-foreign-server.md)

    [52.25. `pg_foreign_table`](catalogs/catalog-pg-foreign-table.md)

    [52.26. `pg_index`](catalogs/catalog-pg-index.md)

    [52.27. `pg_inherits`](catalogs/catalog-pg-inherits.md)

    [52.28. `pg_init_privs`](catalogs/catalog-pg-init-privs.md)

    [52.29. `pg_language`](catalogs/catalog-pg-language.md)

    [52.30. `pg_largeobject`](catalogs/catalog-pg-largeobject.md)

    [52.31. `pg_largeobject_metadata`](catalogs/catalog-pg-largeobject-metadata.md)

    [52.32. `pg_namespace`](catalogs/catalog-pg-namespace.md)

    [52.33. `pg_opclass`](catalogs/catalog-pg-opclass.md)

    [52.34. `pg_operator`](catalogs/catalog-pg-operator.md)

    [52.35. `pg_opfamily`](catalogs/catalog-pg-opfamily.md)

    [52.36. `pg_parameter_acl`](catalogs/catalog-pg-parameter-acl.md)

    [52.37. `pg_partitioned_table`](catalogs/catalog-pg-partitioned-table.md)

    [52.38. `pg_policy`](catalogs/catalog-pg-policy.md)

    [52.39. `pg_proc`](catalogs/catalog-pg-proc.md)

    [52.40. `pg_publication`](catalogs/catalog-pg-publication.md)

    [52.41. `pg_publication_namespace`](catalogs/catalog-pg-publication-namespace.md)

    [52.42. `pg_publication_rel`](catalogs/catalog-pg-publication-rel.md)

    [52.43. `pg_range`](catalogs/catalog-pg-range.md)

    [52.44. `pg_replication_origin`](catalogs/catalog-pg-replication-origin.md)

    [52.45. `pg_rewrite`](catalogs/catalog-pg-rewrite.md)

    [52.46. `pg_seclabel`](catalogs/catalog-pg-seclabel.md)

    [52.47. `pg_sequence`](catalogs/catalog-pg-sequence.md)

    [52.48. `pg_shdepend`](catalogs/catalog-pg-shdepend.md)

    [52.49. `pg_shdescription`](catalogs/catalog-pg-shdescription.md)

    [52.50. `pg_shseclabel`](catalogs/catalog-pg-shseclabel.md)

    [52.51. `pg_statistic`](catalogs/catalog-pg-statistic.md)

    [52.52. `pg_statistic_ext`](catalogs/catalog-pg-statistic-ext.md)

    [52.53. `pg_statistic_ext_data`](catalogs/catalog-pg-statistic-ext-data.md)

    [52.54. `pg_subscription`](catalogs/catalog-pg-subscription.md)

    [52.55. `pg_subscription_rel`](catalogs/catalog-pg-subscription-rel.md)

    [52.56. `pg_tablespace`](catalogs/catalog-pg-tablespace.md)

    [52.57. `pg_transform`](catalogs/catalog-pg-transform.md)

    [52.58. `pg_trigger`](catalogs/catalog-pg-trigger.md)

    [52.59. `pg_ts_config`](catalogs/catalog-pg-ts-config.md)

    [52.60. `pg_ts_config_map`](catalogs/catalog-pg-ts-config-map.md)

    [52.61. `pg_ts_dict`](catalogs/catalog-pg-ts-dict.md)

    [52.62. `pg_ts_parser`](catalogs/catalog-pg-ts-parser.md)

    [52.63. `pg_ts_template`](catalogs/catalog-pg-ts-template.md)

    [52.64. `pg_type`](catalogs/catalog-pg-type.md)

    [52.65. `pg_user_mapping`](catalogs/catalog-pg-user-mapping.md)

[53. System Views](views/README.md)
:   [53.1. Overview](views/views-overview.md)

    [53.2. `pg_aios`](views/view-pg-aios.md)

    [53.3. `pg_available_extensions`](views/view-pg-available-extensions.md)

    [53.4. `pg_available_extension_versions`](views/view-pg-available-extension-versions.md)

    [53.5. `pg_backend_memory_contexts`](views/view-pg-backend-memory-contexts.md)

    [53.6. `pg_config`](views/view-pg-config.md)

    [53.7. `pg_cursors`](views/view-pg-cursors.md)

    [53.8. `pg_file_settings`](views/view-pg-file-settings.md)

    [53.9. `pg_group`](views/view-pg-group.md)

    [53.10. `pg_hba_file_rules`](views/view-pg-hba-file-rules.md)

    [53.11. `pg_ident_file_mappings`](views/view-pg-ident-file-mappings.md)

    [53.12. `pg_indexes`](views/view-pg-indexes.md)

    [53.13. `pg_locks`](views/view-pg-locks.md)

    [53.14. `pg_matviews`](views/view-pg-matviews.md)

    [53.15. `pg_policies`](views/view-pg-policies.md)

    [53.16. `pg_prepared_statements`](views/view-pg-prepared-statements.md)

    [53.17. `pg_prepared_xacts`](views/view-pg-prepared-xacts.md)

    [53.18. `pg_publication_tables`](views/view-pg-publication-tables.md)

    [53.19. `pg_replication_origin_status`](views/view-pg-replication-origin-status.md)

    [53.20. `pg_replication_slots`](views/view-pg-replication-slots.md)

    [53.21. `pg_roles`](views/view-pg-roles.md)

    [53.22. `pg_rules`](views/view-pg-rules.md)

    [53.23. `pg_seclabels`](views/view-pg-seclabels.md)

    [53.24. `pg_sequences`](views/view-pg-sequences.md)

    [53.25. `pg_settings`](views/view-pg-settings.md)

    [53.26. `pg_shadow`](views/view-pg-shadow.md)

    [53.27. `pg_shmem_allocations`](views/view-pg-shmem-allocations.md)

    [53.28. `pg_shmem_allocations_numa`](views/view-pg-shmem-allocations-numa.md)

    [53.29. `pg_stats`](views/view-pg-stats.md)

    [53.30. `pg_stats_ext`](views/view-pg-stats-ext.md)

    [53.31. `pg_stats_ext_exprs`](views/view-pg-stats-ext-exprs.md)

    [53.32. `pg_tables`](views/view-pg-tables.md)

    [53.33. `pg_timezone_abbrevs`](views/view-pg-timezone-abbrevs.md)

    [53.34. `pg_timezone_names`](views/view-pg-timezone-names.md)

    [53.35. `pg_user`](views/view-pg-user.md)

    [53.36. `pg_user_mappings`](views/view-pg-user-mappings.md)

    [53.37. `pg_views`](views/view-pg-views.md)

    [53.38. `pg_wait_events`](views/view-pg-wait-events.md)

[54. Frontend/Backend Protocol](protocol/README.md)
:   [54.1. Overview](protocol/protocol-overview.md)

    [54.2. Message Flow](protocol/protocol-flow.md)

    [54.3. SASL Authentication](protocol/sasl-authentication.md)

    [54.4. Streaming Replication Protocol](protocol/protocol-replication.md)

    [54.5. Logical Streaming Replication Protocol](protocol/protocol-logical-replication.md)

    [54.6. Message Data Types](protocol/protocol-message-types.md)

    [54.7. Message Formats](protocol/protocol-message-formats.md)

    [54.8. Error and Notice Message Fields](protocol/protocol-error-fields.md)

    [54.9. Logical Replication Message Formats](protocol/protocol-logicalrep-message-formats.md)

    [54.10. Summary of Changes since Protocol 2.0](protocol/protocol-changes.md)

[55. PostgreSQL Coding Conventions](source/README.md)
:   [55.1. Formatting](source/source-format.md)

    [55.2. Reporting Errors Within the Server](source/error-message-reporting.md)

    [55.3. Error Message Style Guide](source/error-style-guide.md)

    [55.4. Miscellaneous Coding Conventions](source/source-conventions.md)

[56. Native Language Support](nls/README.md)
:   [56.1. For the Translator](nls/nls-translator.md)

    [56.2. For the Programmer](nls/nls-programmer.md)

[57. Writing a Procedural Language Handler](plhandler/README.md)

[58. Writing a Foreign Data Wrapper](fdwhandler/README.md)
:   [58.1. Foreign Data Wrapper Functions](fdwhandler/fdw-functions.md)

    [58.2. Foreign Data Wrapper Callback Routines](fdwhandler/fdw-callbacks.md)

    [58.3. Foreign Data Wrapper Helper Functions](fdwhandler/fdw-helpers.md)

    [58.4. Foreign Data Wrapper Query Planning](fdwhandler/fdw-planning.md)

    [58.5. Row Locking in Foreign Data Wrappers](fdwhandler/fdw-row-locking.md)

[59. Writing a Table Sampling Method](tablesample-method/README.md)
:   [59.1. Sampling Method Support Functions](tablesample-method/tablesample-support-functions.md)

[60. Writing a Custom Scan Provider](custom-scan/README.md)
:   [60.1. Creating Custom Scan Paths](custom-scan/custom-scan-path.md)

    [60.2. Creating Custom Scan Plans](custom-scan/custom-scan-plan.md)

    [60.3. Executing Custom Scans](custom-scan/custom-scan-execution.md)

[61. Genetic Query Optimizer](geqo/README.md)
:   [61.1. Query Handling as a Complex Optimization Problem](geqo/geqo-intro.md)

    [61.2. Genetic Algorithms](geqo/geqo-intro2.md)

    [61.3. Genetic Query Optimization (GEQO) in PostgreSQL](geqo/geqo-pg-intro.md)

    [61.4. Further Reading](geqo/geqo-biblio.md)

[62. Table Access Method Interface Definition](tableam/README.md)

[63. Index Access Method Interface Definition](indexam/README.md)
:   [63.1. Basic API Structure for Indexes](indexam/index-api.md)

    [63.2. Index Access Method Functions](indexam/index-functions.md)

    [63.3. Index Scanning](indexam/index-scanning.md)

    [63.4. Index Locking Considerations](indexam/index-locking.md)

    [63.5. Index Uniqueness Checks](indexam/index-unique-checks.md)

    [63.6. Index Cost Estimation Functions](indexam/index-cost-estimation.md)

[64. Write Ahead Logging for Extensions](wal-for-extensions/README.md)
:   [64.1. Generic WAL Records](wal-for-extensions/generic-wal.md)

    [64.2. Custom WAL Resource Managers](wal-for-extensions/custom-rmgr.md)

[65. Built-in Index Access Methods](indextypes/README.md)
:   [65.1. B-Tree Indexes](indextypes/btree.md)

    [65.2. GiST Indexes](indextypes/gist.md)

    [65.3. SP-GiST Indexes](indextypes/spgist.md)

    [65.4. GIN Indexes](indextypes/gin.md)

    [65.5. BRIN Indexes](indextypes/brin.md)

    [65.6. Hash Indexes](indextypes/hash-index.md)

[66. Database Physical Storage](storage/README.md)
:   [66.1. Database File Layout](storage/storage-file-layout.md)

    [66.2. TOAST](storage/storage-toast.md)

    [66.3. Free Space Map](storage/storage-fsm.md)

    [66.4. Visibility Map](storage/storage-vm.md)

    [66.5. The Initialization Fork](storage/storage-init.md)

    [66.6. Database Page Layout](storage/storage-page-layout.md)

    [66.7. Heap-Only Tuples (HOT)](storage/storage-hot.md)

[67. Transaction Processing](transactions/README.md)
:   [67.1. Transactions and Identifiers](transactions/transaction-id.md)

    [67.2. Transactions and Locking](transactions/xact-locking.md)

    [67.3. Subtransactions](transactions/subxacts.md)

    [67.4. Two-Phase Transactions](transactions/two-phase.md)

[68. System Catalog Declarations and Initial Contents](bki/README.md)
:   [68.1. System Catalog Declaration Rules](bki/system-catalog-declarations.md)

    [68.2. System Catalog Initial Data](bki/system-catalog-initial-data.md)

    [68.3. BKI File Format](bki/bki-format.md)

    [68.4. BKI Commands](bki/bki-commands.md)

    [68.5. Structure of the Bootstrap BKI File](bki/bki-structure.md)

    [68.6. BKI Example](bki/bki-example.md)

[69. How the Planner Uses Statistics](planner-stats-details/README.md)
:   [69.1. Row Estimation Examples](planner-stats-details/row-estimation-examples.md)

    [69.2. Multivariate Statistics Examples](planner-stats-details/multivariate-statistics-examples.md)

    [69.3. Planner Statistics and Security](planner-stats-details/planner-stats-security.md)

[70. Backup Manifest Format](backup-manifest-format/README.md)
:   [70.1. Backup Manifest Top-level Object](backup-manifest-format/backup-manifest-toplevel.md)

    [70.2. Backup Manifest File Object](backup-manifest-format/backup-manifest-files.md)

    [70.3. Backup Manifest WAL Range Object](backup-manifest-format/backup-manifest-wal-ranges.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/internals.html)（英文原文，待翻譯）
