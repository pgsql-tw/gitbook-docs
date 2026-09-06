# 54.1. Overview

[Table 54.1](overview.md#VIEW-TABLE) lists the system views. More detailed documentation of each catalog follows below. Except where noted, all the views described here are read-only.

#### **Table 54.1. System Views**

| View Name                                                                                                              | Purpose                                                               |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| [`pg_available_extensions`](../system-catalogs/pg_available_extensions.md)                 | available extensions                                                  |
| [`pg_available_extension_versions`](../system-catalogs/pg_available_extension_versions.md) | available versions of extensions                                      |
| [`pg_backend_memory_contexts`](pg_backend_memory_contexts.md)           | backend memory contexts                                               |
| [`pg_config`](pg_config.md)                                             | compile-time configuration parameters                                 |
| [`pg_cursors`](pg_cursors.md)                                           | open cursors                                                          |
| [`pg_file_settings`](pg_file_settings.md)                               | summary of configuration file contents                                |
| [`pg_group`](pg_group.md)                                               | groups of database users                                              |
| [`pg_hba_file_rules`](../system-catalogs/pg_hba_file_rules.md)                             | summary of client authentication configuration file contents          |
| [`pg_ident_file_mappings`](pg_ident_file_mappings.md)                   | summary of client user name mapping configuration file contents       |
| [`pg_indexes`](../system-catalogs/pg_indexes.md)                                           | indexes                                                               |
| [`pg_locks`](../system-catalogs/pg_locks.md)                                               | locks currently held or awaited                                       |
| [`pg_matviews`](pg_matviews.md)                                         | materialized views                                                    |
| [`pg_policies`](pg_policies.md)                                         | policies                                                              |
| [`pg_prepared_statements`](pg_prepared_statements.md)                   | prepared statements                                                   |
| [`pg_prepared_xacts`](../system-catalogs/pg_prepared_xacts.md)                             | prepared transactions                                                 |
| [`pg_publication_tables`](pg_publication_tables.md)                     | publications and information of their associated tables               |
| [`pg_replication_origin_status`](../system-catalogs/51.79.-pg_replication_origin_status.md)       | information about replication origins, including replication progress |
| [`pg_replication_slots`](pg_replication_slots.md)                       | replication slot information                                          |
| [`pg_roles`](pg_roles.md)                                               | database roles                                                        |
| [`pg_rules`](pg_rules.md)                                               | rules                                                                 |
| [`pg_seclabels`](pg_seclabels.md)                                       | security labels                                                       |
| [`pg_sequences`](pg_sequences.md)                                       | sequences                                                             |
| [`pg_settings`](pg_settings.md)                                         | parameter settings                                                    |
| [`pg_shadow`](pg_shadow.md)                                             | database users                                                        |
| [`pg_shmem_allocations`](pg_shmem_allocations.md)                       | shared memory allocations                                             |
| [`pg_stats`](pg_stats.md)                                               | planner statistics                                                    |
| [`pg_stats_ext`](pg_stats_ext.md)                                       | extended planner statistics                                           |
| [`pg_stats_ext_exprs`](pg_stats_ext_exprs.md)                           | extended planner statistics for expressions                           |
| [`pg_tables`](pg_tables.md)                                             | tables                                                                |
| [`pg_timezone_abbrevs`](../54.-system-views/pg_timezone_abbrevs.md)                         | time zone abbreviations                                               |
| [`pg_timezone_names`](../54.-system-views/pg_timezone_names.md)                             | time zone names                                                       |
| [`pg_user`](../system-catalogs/pg_user.md)                                                 | database users                                                        |
| [`pg_user_mappings`](pg_user_mappings.md)                               | user mappings                                                         |
| [`pg_views`](pg_views.md)                                               | views                                                                 |
