# 37.12. column\_column\_usage

The view `column_column_usage` identifies all generated columns that depend on another base column in the same table. Only tables owned by a currently enabled role are included.

#### **Table 37.10. `column_column_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the table (always the current database)</p> |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the table</p>                                  |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the table</p>                                                          |
| <p><code>column_name</code> <code>sql_identifier</code></p><p>Name of the base column that a generated column depends on</p>                |
| <p><code>dependent_column</code> <code>sql_identifier</code></p><p>Name of the generated column</p>                                         |
