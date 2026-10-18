<a id="INFORMATION-SCHEMA"></a>

## 第 35 章 資訊綱要

**目錄**

[35.1. 資訊結構描述](infoschema-schema.md)

[35.2. 資料型別](infoschema-datatypes.md)

[35.3. `information_schema_catalog_name`](infoschema-information-schema-catalog-name.md)

[35.4. `administrable_role_​authorizations`](infoschema-administrable-role-authorizations.md)

[35.5. `applicable_roles`](infoschema-applicable-roles.md)

[35.6. `attributes`](infoschema-attributes.md)

[35.7. `character_sets`](infoschema-character-sets.md)

[35.8. `check_constraint_routine_usage`](infoschema-check-constraint-routine-usage.md)

[35.9. `check_constraints`](infoschema-check-constraints.md)

[35.10. `collations`](infoschema-collations.md)

[35.11. `collation_character_set_​applicability`](infoschema-collation-character-set-applicab.md)

[35.12. `column_column_usage`](infoschema-column-column-usage.md)

[35.13. `column_domain_usage`](infoschema-column-domain-usage.md)

[35.14. `column_options`](infoschema-column-options.md)

[35.15. `column_privileges`](infoschema-column-privileges.md)

[35.16. `column_udt_usage`](infoschema-column-udt-usage.md)

[35.17. `columns`](infoschema-columns.md)

[35.18. `constraint_column_usage`](infoschema-constraint-column-usage.md)

[35.19. `constraint_table_usage`](infoschema-constraint-table-usage.md)

[35.20. `data_type_privileges`](infoschema-data-type-privileges.md)

[35.21. `domain_constraints`](infoschema-domain-constraints.md)

[35.22. `domain_udt_usage`](infoschema-domain-udt-usage.md)

[35.23. `domains`](infoschema-domains.md)

[35.24. `element_types`](infoschema-element-types.md)

[35.25. `enabled_roles`](infoschema-enabled-roles.md)

[35.26. `foreign_data_wrapper_options`](infoschema-foreign-data-wrapper-options.md)

[35.27. `foreign_data_wrappers`](infoschema-foreign-data-wrappers.md)

[35.28. `foreign_server_options`](infoschema-foreign-server-options.md)

[35.29. `foreign_servers`](infoschema-foreign-servers.md)

[35.30. `foreign_table_options`](infoschema-foreign-table-options.md)

[35.31. `foreign_tables`](infoschema-foreign-tables.md)

[35.32. `key_column_usage`](infoschema-key-column-usage.md)

[35.33. `parameters`](infoschema-parameters.md)

[35.34. `referential_constraints`](infoschema-referential-constraints.md)

[35.35. `role_column_grants`](infoschema-role-column-grants.md)

[35.36. `role_routine_grants`](infoschema-role-routine-grants.md)

[35.37. `role_table_grants`](infoschema-role-table-grants.md)

[35.38. `role_udt_grants`](infoschema-role-udt-grants.md)

[35.39. `role_usage_grants`](infoschema-role-usage-grants.md)

[35.40. `routine_column_usage`](infoschema-routine-column-usage.md)

[35.41. `routine_privileges`](infoschema-routine-privileges.md)

[35.42. `routine_routine_usage`](infoschema-routine-routine-usage.md)

[35.43. `routine_sequence_usage`](infoschema-routine-sequence-usage.md)

[35.44. `routine_table_usage`](infoschema-routine-table-usage.md)

[35.45. `routines`](infoschema-routines.md)

[35.46. `schemata`](infoschema-schemata.md)

[35.47. `sequences`](infoschema-sequences.md)

[35.48. `sql_features`](infoschema-sql-features.md)

[35.49. `sql_implementation_info`](infoschema-sql-implementation-info.md)

[35.50. `sql_parts`](infoschema-sql-parts.md)

[35.51. `sql_sizing`](infoschema-sql-sizing.md)

[35.52. `table_constraints`](infoschema-table-constraints.md)

[35.53. `table_privileges`](infoschema-table-privileges.md)

[35.54. `tables`](infoschema-tables.md)

[35.55. `transforms`](infoschema-transforms.md)

[35.56. `triggered_update_columns`](infoschema-triggered-update-columns.md)

[35.57. `triggers`](infoschema-triggers.md)

[35.58. `udt_privileges`](infoschema-udt-privileges.md)

[35.59. `usage_privileges`](infoschema-usage-privileges.md)

[35.60. `user_defined_types`](infoschema-user-defined-types.md)

[35.61. `user_mapping_options`](infoschema-user-mapping-options.md)

[35.62. `user_mappings`](infoschema-user-mappings.md)

[35.63. `view_column_usage`](infoschema-view-column-usage.md)

[35.64. `view_routine_usage`](infoschema-view-routine-usage.md)

[35.65. `view_table_usage`](infoschema-view-table-usage.md)

[35.66. `views`](infoschema-views.md)

<a id="id-1.7.6.2"></a>

資訊綱要由一組檢視表組成，其中包含目前資料庫中所定義物件的相關資訊。資訊綱要定義於
SQL 標準中，因此可以預期它具有可攜性並保持穩定——這點與系統目錄不同，系統目錄是
PostgreSQL 特有的，並且是依照實作上的考量來設計。不過，資訊綱要檢視表並不包含
PostgreSQL 特有功能的相關資訊；若要查詢這些資訊，你需要查詢系統目錄或其他
PostgreSQL 特有的檢視表。

### 注意

向資料庫查詢限制條件資訊時，預期傳回一筆資料列的符合標準查詢，有可能傳回多筆
資料列。這是因為 SQL 標準要求限制條件名稱在綱要內必須唯一，但 PostgreSQL 並不
強制執行此限制。PostgreSQL 自動產生的限制條件名稱會避免在同一綱要中重複，但使用者
可以指定這種重複的名稱。

查詢 `check_constraint_routine_usage`、
`check_constraints`、`domain_constraints` 與
`referential_constraints` 等資訊綱要檢視表時，可能會出現這個問題。其他一些檢視表
也有類似的問題，但包含資料表名稱以協助區分重複的資料列，例如 `constraint_column_usage`、
`constraint_table_usage`、`table_constraints`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/information-schema.html)（原文版本：18.6；核對日期：2026-10-18）
