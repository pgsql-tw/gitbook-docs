# 37.41. routine\_privileges

The view `routine_privileges` identifies all privileges granted on functions to a currently enabled role or by a currently enabled role. There is one row for each combination of function, grantor, and grantee.

#### **Table 37.39. `routine_privileges` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>grantor</code> <code>sql_identifier</code></p><p>Name of the role that granted the privilege</p>                                                                                                                       |
| <p><code>grantee</code> <code>sql_identifier</code></p><p>Name of the role that the privilege was granted to</p>                                                                                                                |
| <p><code>specific_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                               |
| <p><code>specific_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                                |
| <p><code>specific_name</code> <code>sql_identifier</code></p><p>The “specific name” of the function. See <a href="https://www.postgresql.org/docs/current/infoschema-routines.html">Section 37.45</a> for more information.</p> |
| <p><code>routine_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                                |
| <p><code>routine_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                                 |
| <p><code>routine_name</code> <code>sql_identifier</code></p><p>Name of the function (might be duplicated in case of overloading)</p>                                                                                            |
| <p><code>privilege_type</code> <code>character_data</code></p><p>Always <code>EXECUTE</code> (the only privilege type for functions)</p>                                                                                        |
| <p><code>is_grantable</code> <code>yes_or_no</code></p><p><code>YES</code> if the privilege is grantable, <code>NO</code> if not</p>                                                                                            |
