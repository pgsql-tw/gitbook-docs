# 37.16. column\_udt\_usage

The view `column_udt_usage` identifies all columns that use data types owned by a currently enabled role. Note that in PostgreSQL, built-in data types behave like user-defined types, so they are included here as well. See also [Section 37.17](https://www.postgresql.org/docs/current/infoschema-columns.html) for details.

#### **Table 37.14. `column_udt_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>udt_catalog</code> <code>sql_identifier</code></p><p>Name of the database that the column data type (the underlying type of the domain, if applicable) is defined in (always the current database)</p> |
| <p><code>udt_schema</code> <code>sql_identifier</code></p><p>Name of the schema that the column data type (the underlying type of the domain, if applicable) is defined in</p>                                  |
| <p><code>udt_name</code> <code>sql_identifier</code></p><p>Name of the column data type (the underlying type of the domain, if applicable)</p>                                                                  |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the table (always the current database)</p>                                                                     |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the table</p>                                                                                                      |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the table</p>                                                                                                                              |
| <p><code>column_name</code> <code>sql_identifier</code></p><p>Name of the column</p>                                                                                                                            |
