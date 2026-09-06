# 37.38. role\_udt\_grants

The view `role_udt_grants` is intended to identify `USAGE` privileges granted on user-defined types where the grantor or grantee is a currently enabled role. Further information can be found under `udt_privileges`. The only effective difference between this view and `udt_privileges` is that this view omits objects that have been made accessible to the current user by way of a grant to `PUBLIC`. Since data types do not have real privileges in PostgreSQL, but only an implicit grant to `PUBLIC`, this view is empty.

#### **Table 37.36. `role_udt_grants` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>grantor</code> <code>sql_identifier</code></p><p>The name of the role that granted the privilege</p>                            |
| <p><code>grantee</code> <code>sql_identifier</code></p><p>The name of the role that the privilege was granted to</p>                     |
| <p><code>udt_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the type (always the current database)</p> |
| <p><code>udt_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the type</p>                                  |
| <p><code>udt_name</code> <code>sql_identifier</code></p><p>Name of the type</p>                                                          |
| <p><code>privilege_type</code> <code>character_data</code></p><p>Always <code>TYPE USAGE</code></p>                                      |
| <p><code>is_grantable</code> <code>yes_or_no</code></p><p><code>YES</code> if the privilege is grantable, <code>NO</code> if not</p>     |
