# 37.64. view\_routine\_usage

The view `view_routine_usage` identifies all routines (functions and procedures) that are used in the query expression of a view (the `SELECT` statement that defines the view). A routine is only included if that routine is owned by a currently enabled role.

#### **Table 37.62. `view_routine_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the view (always the current database)</p>                                                                                      |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the view</p>                                                                                                                       |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the view</p>                                                                                                                                               |
| <p><code>specific_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                               |
| <p><code>specific_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                                |
| <p><code>specific_name</code> <code>sql_identifier</code></p><p>The “specific name” of the function. See <a href="https://www.postgresql.org/docs/current/infoschema-routines.html">Section 37.45</a> for more information.</p> |
