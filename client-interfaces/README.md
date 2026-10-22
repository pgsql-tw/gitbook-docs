<a id="CLIENT-INTERFACES"></a>

# 第四部分：用戶端介面

<a id="id-1.7.2"></a>

本部分說明隨 PostgreSQL 一起發佈的用戶端程式設計介面。各章都可以獨立閱讀。另外還有許多單獨發佈、供用戶端程式使用的外部程式設計介面，它們各自附有說明文件（[附錄 H](../appendixes/external-projects/README.md) 列出其中幾個較受歡迎的介面）。本部分的讀者應該熟悉如何使用 SQL 操作與查詢資料庫（請參閱[第二部分](../the-sql-language/README.md)），當然也應該熟悉自己所選用的程式語言。

**目錄**

[32. libpq — C 函式庫](libpq/README.md)
:   [32.1. 資料庫連線控制函式](libpq/libpq-connect.md)

    [32.2. 連線狀態函式](libpq/libpq-status.md)

    [32.3. 命令執行函式](libpq/libpq-exec.md)

    [32.4. 非同步命令處理](libpq/libpq-async.md)

    [32.5. 管線模式](libpq/libpq-pipeline-mode.md)

    [32.6. 分塊取得查詢結果](libpq/libpq-single-row-mode.md)

    [32.7. 取消進行中的查詢](libpq/libpq-cancel.md)

    [32.8. 快速路徑介面](libpq/libpq-fastpath.md)

    [32.9. 非同步通知](libpq/libpq-notify.md)

    [32.10. 與 `COPY` 命令相關的函式](libpq/libpq-copy.md)

    [32.11. 控制函式](libpq/libpq-control.md)

    [32.12. 其他函式](libpq/libpq-misc.md)

    [32.13. 通知訊息處理](libpq/libpq-notice-processing.md)

    [32.14. 事件系統](libpq/libpq-events.md)

    [32.15. 環境變數](libpq/libpq-envars.md)

    [32.16. 密碼檔](libpq/libpq-pgpass.md)

    [32.17. 連線服務檔](libpq/libpq-pgservice.md)

    [32.18. 以 LDAP 查詢連線參數](libpq/libpq-ldap.md)

    [32.19. SSL 支援](libpq/libpq-ssl.md)

    [32.20. OAuth 支援](libpq/libpq-oauth.md)

    [32.21. 多執行緒程式中的行為](libpq/libpq-threading.md)

    [32.22. 建置 libpq 程式](libpq/libpq-build.md)

    [32.23. 範例程式](libpq/libpq-example.md)

[33. 大型物件](largeobjects/README.md)
:   [33.1. 簡介](largeobjects/lo-intro.md)

    [33.2. 實作特性](largeobjects/lo-implementation.md)

    [33.3. 用戶端介面](largeobjects/lo-interfaces.md)

    [33.4. 伺服器端函式](largeobjects/lo-funcs.md)

    [33.5. 範例程式](largeobjects/lo-examplesect.md)

[34. ECPG — C 語言中的嵌入式 SQL](ecpg/README.md)
:   [34.1. 概念](ecpg/ecpg-concept.md)

    [34.2. 管理資料庫連線](ecpg/ecpg-connect.md)

    [34.3. 執行 SQL 命令](ecpg/ecpg-commands.md)

    [34.4. 使用主機變數](ecpg/ecpg-variables.md)

    [34.5. 動態 SQL](ecpg/ecpg-dynamic.md)

    [34.6. pgtypes 函式庫](ecpg/ecpg-pgtypes.md)

    [34.7. 使用描述區](ecpg/ecpg-descriptors.md)

    [34.8. 錯誤處理](ecpg/ecpg-errors.md)

    [34.9. 前置處理器指令](ecpg/ecpg-preproc.md)

    [34.10. 處理嵌入式 SQL 程式](ecpg/ecpg-process.md)

    [34.11. 函式庫函式](ecpg/ecpg-library.md)

    [34.12. 大型物件](ecpg/ecpg-lo.md)

    [34.13. C++ 應用程式](ecpg/ecpg-cpp.md)

    [34.14. 嵌入式 SQL 命令](ecpg/ecpg-sql-commands.md)

    [34.15. Informix 相容模式](ecpg/ecpg-informix-compat.md)

    [34.16. Oracle 相容模式](ecpg/ecpg-oracle-compat.md)

    [34.17. 內部運作](ecpg/ecpg-develop.md)

[35. 資訊綱要](information-schema/README.md)
:   [35.1. 資訊結構描述](information-schema/infoschema-schema.md)

    [35.2. 資料型別](information-schema/infoschema-datatypes.md)

    [35.3. `information_schema_catalog_name`](information-schema/infoschema-information-schema-catalog-name.md)

    [35.4. `administrable_role_​authorizations`](information-schema/infoschema-administrable-role-authorizations.md)

    [35.5. `applicable_roles`](information-schema/infoschema-applicable-roles.md)

    [35.6. `attributes`](information-schema/infoschema-attributes.md)

    [35.7. `character_sets`](information-schema/infoschema-character-sets.md)

    [35.8. `check_constraint_routine_usage`](information-schema/infoschema-check-constraint-routine-usage.md)

    [35.9. `check_constraints`](information-schema/infoschema-check-constraints.md)

    [35.10. `collations`](information-schema/infoschema-collations.md)

    [35.11. `collation_character_set_​applicability`](information-schema/infoschema-collation-character-set-applicab.md)

    [35.12. `column_column_usage`](information-schema/infoschema-column-column-usage.md)

    [35.13. `column_domain_usage`](information-schema/infoschema-column-domain-usage.md)

    [35.14. `column_options`](information-schema/infoschema-column-options.md)

    [35.15. `column_privileges`](information-schema/infoschema-column-privileges.md)

    [35.16. `column_udt_usage`](information-schema/infoschema-column-udt-usage.md)

    [35.17. `columns`](information-schema/infoschema-columns.md)

    [35.18. `constraint_column_usage`](information-schema/infoschema-constraint-column-usage.md)

    [35.19. `constraint_table_usage`](information-schema/infoschema-constraint-table-usage.md)

    [35.20. `data_type_privileges`](information-schema/infoschema-data-type-privileges.md)

    [35.21. `domain_constraints`](information-schema/infoschema-domain-constraints.md)

    [35.22. `domain_udt_usage`](information-schema/infoschema-domain-udt-usage.md)

    [35.23. `domains`](information-schema/infoschema-domains.md)

    [35.24. `element_types`](information-schema/infoschema-element-types.md)

    [35.25. `enabled_roles`](information-schema/infoschema-enabled-roles.md)

    [35.26. `foreign_data_wrapper_options`](information-schema/infoschema-foreign-data-wrapper-options.md)

    [35.27. `foreign_data_wrappers`](information-schema/infoschema-foreign-data-wrappers.md)

    [35.28. `foreign_server_options`](information-schema/infoschema-foreign-server-options.md)

    [35.29. `foreign_servers`](information-schema/infoschema-foreign-servers.md)

    [35.30. `foreign_table_options`](information-schema/infoschema-foreign-table-options.md)

    [35.31. `foreign_tables`](information-schema/infoschema-foreign-tables.md)

    [35.32. `key_column_usage`](information-schema/infoschema-key-column-usage.md)

    [35.33. `parameters`](information-schema/infoschema-parameters.md)

    [35.34. `referential_constraints`](information-schema/infoschema-referential-constraints.md)

    [35.35. `role_column_grants`](information-schema/infoschema-role-column-grants.md)

    [35.36. `role_routine_grants`](information-schema/infoschema-role-routine-grants.md)

    [35.37. `role_table_grants`](information-schema/infoschema-role-table-grants.md)

    [35.38. `role_udt_grants`](information-schema/infoschema-role-udt-grants.md)

    [35.39. `role_usage_grants`](information-schema/infoschema-role-usage-grants.md)

    [35.40. `routine_column_usage`](information-schema/infoschema-routine-column-usage.md)

    [35.41. `routine_privileges`](information-schema/infoschema-routine-privileges.md)

    [35.42. `routine_routine_usage`](information-schema/infoschema-routine-routine-usage.md)

    [35.43. `routine_sequence_usage`](information-schema/infoschema-routine-sequence-usage.md)

    [35.44. `routine_table_usage`](information-schema/infoschema-routine-table-usage.md)

    [35.45. `routines`](information-schema/infoschema-routines.md)

    [35.46. `schemata`](information-schema/infoschema-schemata.md)

    [35.47. `sequences`](information-schema/infoschema-sequences.md)

    [35.48. `sql_features`](information-schema/infoschema-sql-features.md)

    [35.49. `sql_implementation_info`](information-schema/infoschema-sql-implementation-info.md)

    [35.50. `sql_parts`](information-schema/infoschema-sql-parts.md)

    [35.51. `sql_sizing`](information-schema/infoschema-sql-sizing.md)

    [35.52. `table_constraints`](information-schema/infoschema-table-constraints.md)

    [35.53. `table_privileges`](information-schema/infoschema-table-privileges.md)

    [35.54. `tables`](information-schema/infoschema-tables.md)

    [35.55. `transforms`](information-schema/infoschema-transforms.md)

    [35.56. `triggered_update_columns`](information-schema/infoschema-triggered-update-columns.md)

    [35.57. `triggers`](information-schema/infoschema-triggers.md)

    [35.58. `udt_privileges`](information-schema/infoschema-udt-privileges.md)

    [35.59. `usage_privileges`](information-schema/infoschema-usage-privileges.md)

    [35.60. `user_defined_types`](information-schema/infoschema-user-defined-types.md)

    [35.61. `user_mapping_options`](information-schema/infoschema-user-mapping-options.md)

    [35.62. `user_mappings`](information-schema/infoschema-user-mappings.md)

    [35.63. `view_column_usage`](information-schema/infoschema-view-column-usage.md)

    [35.64. `view_routine_usage`](information-schema/infoschema-view-routine-usage.md)

    [35.65. `view_table_usage`](information-schema/infoschema-view-table-usage.md)

    [35.66. `views`](information-schema/infoschema-views.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/client-interfaces.html)（原文版本：18.6；核對日期：2026-10-22）
