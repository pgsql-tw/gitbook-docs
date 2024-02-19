# 54.1. Overview

[Table 54.1](https://www.postgresql.org/docs/current/views-overview.html#VIEW-TABLE) lists the system views. More detailed documentation of each catalog follows below. Except where noted, all the views described here are read-only.

#### **Table 54.1. System Views**

| View Name                                                                                                              | Purpose                                                               |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| [`pg_available_extensions`](https://www.postgresql.org/docs/current/view-pg-available-extensions.html)                 | available extensions                                                  |
| [`pg_available_extension_versions`](https://www.postgresql.org/docs/current/view-pg-available-extension-versions.html) | available versions of extensions                                      |
| [`pg_backend_memory_contexts`](https://www.postgresql.org/docs/current/view-pg-backend-memory-contexts.html)           | backend memory contexts                                               |
| [`pg_config`](https://www.postgresql.org/docs/current/view-pg-config.html)                                             | compile-time configuration parameters                                 |
| [`pg_cursors`](https://www.postgresql.org/docs/current/view-pg-cursors.html)                                           | open cursors                                                          |
| [`pg_file_settings`](https://www.postgresql.org/docs/current/view-pg-file-settings.html)                               | summary of configuration file contents                                |
| [`pg_group`](https://www.postgresql.org/docs/current/view-pg-group.html)                                               | groups of database users                                              |
| [`pg_hba_file_rules`](https://www.postgresql.org/docs/current/view-pg-hba-file-rules.html)                             | summary of client authentication configuration file contents          |
| [`pg_ident_file_mappings`](https://www.postgresql.org/docs/current/view-pg-ident-file-mappings.html)                   | summary of client user name mapping configuration file contents       |
| [`pg_indexes`](https://www.postgresql.org/docs/current/view-pg-indexes.html)                                           | indexes                                                               |
| [`pg_locks`](https://www.postgresql.org/docs/current/view-pg-locks.html)                                               | locks currently held or awaited                                       |
| [`pg_matviews`](https://www.postgresql.org/docs/current/view-pg-matviews.html)                                         | materialized views                                                    |
| [`pg_policies`](https://www.postgresql.org/docs/current/view-pg-policies.html)                                         | policies                                                              |
| [`pg_prepared_statements`](https://www.postgresql.org/docs/current/view-pg-prepared-statements.html)                   | prepared statements                                                   |
| [`pg_prepared_xacts`](https://www.postgresql.org/docs/current/view-pg-prepared-xacts.html)                             | prepared transactions                                                 |
| [`pg_publication_tables`](https://www.postgresql.org/docs/current/view-pg-publication-tables.html)                     | publications and information of their associated tables               |
| [`pg_replication_origin_status`](https://www.postgresql.org/docs/current/view-pg-replication-origin-status.html)       | information about replication origins, including replication progress |
| [`pg_replication_slots`](https://www.postgresql.org/docs/current/view-pg-replication-slots.html)                       | replication slot information                                          |
| [`pg_roles`](https://www.postgresql.org/docs/current/view-pg-roles.html)                                               | database roles                                                        |
| [`pg_rules`](https://www.postgresql.org/docs/current/view-pg-rules.html)                                               | rules                                                                 |
| [`pg_seclabels`](https://www.postgresql.org/docs/current/view-pg-seclabels.html)                                       | security labels                                                       |
| [`pg_sequences`](https://www.postgresql.org/docs/current/view-pg-sequences.html)                                       | sequences                                                             |
| [`pg_settings`](https://www.postgresql.org/docs/current/view-pg-settings.html)                                         | parameter settings                                                    |
| [`pg_shadow`](https://www.postgresql.org/docs/current/view-pg-shadow.html)                                             | database users                                                        |
| [`pg_shmem_allocations`](https://www.postgresql.org/docs/current/view-pg-shmem-allocations.html)                       | shared memory allocations                                             |
| [`pg_stats`](https://www.postgresql.org/docs/current/view-pg-stats.html)                                               | planner statistics                                                    |
| [`pg_stats_ext`](https://www.postgresql.org/docs/current/view-pg-stats-ext.html)                                       | extended planner statistics                                           |
| [`pg_stats_ext_exprs`](https://www.postgresql.org/docs/current/view-pg-stats-ext-exprs.html)                           | extended planner statistics for expressions                           |
| [`pg_tables`](https://www.postgresql.org/docs/current/view-pg-tables.html)                                             | tables                                                                |
| [`pg_timezone_abbrevs`](https://www.postgresql.org/docs/current/view-pg-timezone-abbrevs.html)                         | time zone abbreviations                                               |
| [`pg_timezone_names`](https://www.postgresql.org/docs/current/view-pg-timezone-names.html)                             | time zone names                                                       |
| [`pg_user`](https://www.postgresql.org/docs/current/view-pg-user.html)                                                 | database users                                                        |
| [`pg_user_mappings`](https://www.postgresql.org/docs/current/view-pg-user-mappings.html)                               | user mappings                                                         |
| [`pg_views`](https://www.postgresql.org/docs/current/view-pg-views.html)                                               | views                                                                 |
