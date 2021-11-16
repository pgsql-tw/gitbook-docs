# 36.8. check\_constraint\_routine\_usage

The view `check_constraint_routine_usage` identifies routines (functions and procedures) that are used by a check constraint. Only those routines are shown that are owned by a currently enabled role.

**Table 36.6. `check_constraint_routine_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>constraint_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the constraint (always the current database)</p>                                                                      |
| <p><code>constraint_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the constraint</p>                                                                                                       |
| <p><code>constraint_name</code> <code>sql_identifier</code></p><p>Name of the constraint</p>                                                                                                                               |
| <p><code>specific_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the function (always the current database)</p>                                                                          |
| <p><code>specific_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the function</p>                                                                                                           |
| <p><code>specific_name</code> <code>sql_identifier</code></p><p>The “specific name” of the function. See <a href="https://www.postgresql.org/docs/13/infoschema-routines.html">Section 36.41</a> for more information.</p> |
