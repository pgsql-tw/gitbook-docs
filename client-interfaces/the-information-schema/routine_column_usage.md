# 37.40. routine\_column\_usage

The view `routine_column_usage` is meant to identify all columns that are used by a function or procedure. This information is currently not tracked by PostgreSQL.

#### **Table 37.38. `routine_column_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>specific_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                               |
| <p><code>specific_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                                |
| <p><code>specific_name</code> <code>sql_identifier</code></p><p>The “specific name” of the function. See <a href="https://www.postgresql.org/docs/current/infoschema-routines.html">Section 37.45</a> for more information.</p> |
| <p><code>routine_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                                |
| <p><code>routine_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                                 |
| <p><code>routine_name</code> <code>sql_identifier</code></p><p>Name of the function (might be duplicated in case of overloading)</p>                                                                                            |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the table that is used by the function (always the current database)</p>                                                     |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the table that is used by the function</p>                                                                                      |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the table that is used by the function</p>                                                                                                                 |
| <p><code>column_name</code> <code>sql_identifier</code></p><p>Name of the column that is used by the function</p>                                                                                                               |
