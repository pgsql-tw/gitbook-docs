# Part IV. Client Interfaces

<a id="id-1.7.2"></a>

This part describes the client programming interfaces distributed
with PostgreSQL. Each of these chapters can be
read independently. There are many external programming
interfaces for client programs that are distributed separately. They
contain their own documentation ([Appendix H](../appendixes/external-projects/README.md)
lists some of the more popular ones). Readers of this part should be
familiar with using SQL to manipulate
and query the database (see [Part II](../the-sql-language/README.md)) and of course
with the programming language of their choice.

**Table of Contents**

[32. libpq — C Library](libpq/README.md)
:   [32.1. Database Connection Control Functions](libpq/libpq-connect.md)

    [32.2. Connection Status Functions](libpq/libpq-status.md)

    [32.3. Command Execution Functions](libpq/libpq-exec.md)

    [32.4. Asynchronous Command Processing](libpq/libpq-async.md)

    [32.5. Pipeline Mode](libpq/libpq-pipeline-mode.md)

    [32.6. Retrieving Query Results in Chunks](libpq/libpq-single-row-mode.md)

    [32.7. Canceling Queries in Progress](libpq/libpq-cancel.md)

    [32.8. The Fast-Path Interface](libpq/libpq-fastpath.md)

    [32.9. Asynchronous Notification](libpq/libpq-notify.md)

    [32.10. Functions Associated with the `COPY` Command](libpq/libpq-copy.md)

    [32.11. Control Functions](libpq/libpq-control.md)

    [32.12. Miscellaneous Functions](libpq/libpq-misc.md)

    [32.13. Notice Processing](libpq/libpq-notice-processing.md)

    [32.14. Event System](libpq/libpq-events.md)

    [32.15. Environment Variables](libpq/libpq-envars.md)

    [32.16. The Password File](libpq/libpq-pgpass.md)

    [32.17. The Connection Service File](libpq/libpq-pgservice.md)

    [32.18. LDAP Lookup of Connection Parameters](libpq/libpq-ldap.md)

    [32.19. SSL Support](libpq/libpq-ssl.md)

    [32.20. OAuth Support](libpq/libpq-oauth.md)

    [32.21. Behavior in Threaded Programs](libpq/libpq-threading.md)

    [32.22. Building libpq Programs](libpq/libpq-build.md)

    [32.23. Example Programs](libpq/libpq-example.md)

[33. Large Objects](largeobjects/README.md)
:   [33.1. Introduction](largeobjects/lo-intro.md)

    [33.2. Implementation Features](largeobjects/lo-implementation.md)

    [33.3. Client Interfaces](largeobjects/lo-interfaces.md)

    [33.4. Server-Side Functions](largeobjects/lo-funcs.md)

    [33.5. Example Program](largeobjects/lo-examplesect.md)

[34. ECPG — Embedded SQL in C](ecpg/README.md)
:   [34.1. The Concept](ecpg/ecpg-concept.md)

    [34.2. Managing Database Connections](ecpg/ecpg-connect.md)

    [34.3. Running SQL Commands](ecpg/ecpg-commands.md)

    [34.4. Using Host Variables](ecpg/ecpg-variables.md)

    [34.5. Dynamic SQL](ecpg/ecpg-dynamic.md)

    [34.6. pgtypes Library](ecpg/ecpg-pgtypes.md)

    [34.7. Using Descriptor Areas](ecpg/ecpg-descriptors.md)

    [34.8. Error Handling](ecpg/ecpg-errors.md)

    [34.9. Preprocessor Directives](ecpg/ecpg-preproc.md)

    [34.10. Processing Embedded SQL Programs](ecpg/ecpg-process.md)

    [34.11. Library Functions](ecpg/ecpg-library.md)

    [34.12. Large Objects](ecpg/ecpg-lo.md)

    [34.13. C++ Applications](ecpg/ecpg-cpp.md)

    [34.14. Embedded SQL Commands](ecpg/ecpg-sql-commands.md)

    [34.15. Informix Compatibility Mode](ecpg/ecpg-informix-compat.md)

    [34.16. Oracle Compatibility Mode](ecpg/ecpg-oracle-compat.md)

    [34.17. Internals](ecpg/ecpg-develop.md)

[35. The Information Schema](information-schema/README.md)
:   [35.1. The Schema](information-schema/infoschema-schema.md)

    [35.2. Data Types](information-schema/infoschema-datatypes.md)

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/client-interfaces.html)（英文原文，待翻譯）
