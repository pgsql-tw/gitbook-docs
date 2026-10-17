<a id="CATALOGS"></a>

## 第 52 章 系統目錄

**目錄**

[52.1. 概觀](catalogs-overview.md)

[52.2. `pg_aggregate`](catalog-pg-aggregate.md)

[52.3. `pg_am`](catalog-pg-am.md)

[52.4. `pg_amop`](catalog-pg-amop.md)

[52.5. `pg_amproc`](catalog-pg-amproc.md)

[52.6. `pg_attrdef`](catalog-pg-attrdef.md)

[52.7. `pg_attribute`](catalog-pg-attribute.md)

[52.8. `pg_authid`](catalog-pg-authid.md)

[52.9. `pg_auth_members`](catalog-pg-auth-members.md)

[52.10. `pg_cast`](catalog-pg-cast.md)

[52.11. `pg_class`](catalog-pg-class.md)

[52.12. `pg_collation`](catalog-pg-collation.md)

[52.13. `pg_constraint`](catalog-pg-constraint.md)

[52.14. `pg_conversion`](catalog-pg-conversion.md)

[52.15. `pg_database`](catalog-pg-database.md)

[52.16. `pg_db_role_setting`](catalog-pg-db-role-setting.md)

[52.17. `pg_default_acl`](catalog-pg-default-acl.md)

[52.18. `pg_depend`](catalog-pg-depend.md)

[52.19. `pg_description`](catalog-pg-description.md)

[52.20. `pg_enum`](catalog-pg-enum.md)

[52.21. `pg_event_trigger`](catalog-pg-event-trigger.md)

[52.22. `pg_extension`](catalog-pg-extension.md)

[52.23. `pg_foreign_data_wrapper`](catalog-pg-foreign-data-wrapper.md)

[52.24. `pg_foreign_server`](catalog-pg-foreign-server.md)

[52.25. `pg_foreign_table`](catalog-pg-foreign-table.md)

[52.26. `pg_index`](catalog-pg-index.md)

[52.27. `pg_inherits`](catalog-pg-inherits.md)

[52.28. `pg_init_privs`](catalog-pg-init-privs.md)

[52.29. `pg_language`](catalog-pg-language.md)

[52.30. `pg_largeobject`](catalog-pg-largeobject.md)

[52.31. `pg_largeobject_metadata`](catalog-pg-largeobject-metadata.md)

[52.32. `pg_namespace`](catalog-pg-namespace.md)

[52.33. `pg_opclass`](catalog-pg-opclass.md)

[52.34. `pg_operator`](catalog-pg-operator.md)

[52.35. `pg_opfamily`](catalog-pg-opfamily.md)

[52.36. `pg_parameter_acl`](catalog-pg-parameter-acl.md)

[52.37. `pg_partitioned_table`](catalog-pg-partitioned-table.md)

[52.38. `pg_policy`](catalog-pg-policy.md)

[52.39. `pg_proc`](catalog-pg-proc.md)

[52.40. `pg_publication`](catalog-pg-publication.md)

[52.41. `pg_publication_namespace`](catalog-pg-publication-namespace.md)

[52.42. `pg_publication_rel`](catalog-pg-publication-rel.md)

[52.43. `pg_range`](catalog-pg-range.md)

[52.44. `pg_replication_origin`](catalog-pg-replication-origin.md)

[52.45. `pg_rewrite`](catalog-pg-rewrite.md)

[52.46. `pg_seclabel`](catalog-pg-seclabel.md)

[52.47. `pg_sequence`](catalog-pg-sequence.md)

[52.48. `pg_shdepend`](catalog-pg-shdepend.md)

[52.49. `pg_shdescription`](catalog-pg-shdescription.md)

[52.50. `pg_shseclabel`](catalog-pg-shseclabel.md)

[52.51. `pg_statistic`](catalog-pg-statistic.md)

[52.52. `pg_statistic_ext`](catalog-pg-statistic-ext.md)

[52.53. `pg_statistic_ext_data`](catalog-pg-statistic-ext-data.md)

[52.54. `pg_subscription`](catalog-pg-subscription.md)

[52.55. `pg_subscription_rel`](catalog-pg-subscription-rel.md)

[52.56. `pg_tablespace`](catalog-pg-tablespace.md)

[52.57. `pg_transform`](catalog-pg-transform.md)

[52.58. `pg_trigger`](catalog-pg-trigger.md)

[52.59. `pg_ts_config`](catalog-pg-ts-config.md)

[52.60. `pg_ts_config_map`](catalog-pg-ts-config-map.md)

[52.61. `pg_ts_dict`](catalog-pg-ts-dict.md)

[52.62. `pg_ts_parser`](catalog-pg-ts-parser.md)

[52.63. `pg_ts_template`](catalog-pg-ts-template.md)

[52.64. `pg_type`](catalog-pg-type.md)

[52.65. `pg_user_mapping`](catalog-pg-user-mapping.md)

系統目錄是關聯式資料庫管理系統存放綱要中繼資料（例如資料表與欄位的相關資訊）以及內部記錄資訊的地方。
PostgreSQL 的系統目錄就是一般的資料表。你可以移除並重新建立這些資料表、新增欄位、插入與更新值，
而這樣做可能嚴重地搞亂你的系統。
一般而言，不應該手動變更系統目錄，通常都有 SQL 命令可以完成這些事。（例如，`CREATE
DATABASE` 會在
`pg_database` 目錄中插入一筆資料列——而且實際在磁碟上建立該資料庫。）對於某些特別冷僻的操作有一些例外，
但其中許多操作隨著時間推移已經以 SQL 命令的形式提供，因此直接操作系統目錄的需求正在逐漸減少。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalogs.html)（原文版本：18.6；核對日期：2026-10-17）
