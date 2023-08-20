# 37.18. constraint\_column\_usage

The view `constraint_column_usage` identifies all columns in the current database that are used by some constraint. Only those columns are shown that are contained in a table owned by a currently enabled role. For a check constraint, this view identifies the columns that are used in the check expression. For a foreign key constraint, this view identifies the columns that the foreign key references. For a unique or primary key constraint, this view identifies the constrained columns.

#### **Table 37.16. `constraint_column_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the table that contains the column that is used by some constraint (always the current database)</p> |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the table that contains the column that is used by some constraint</p>                                  |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the table that contains the column that is used by some constraint</p>                                                             |
| <p><code>column_name</code> <code>sql_identifier</code></p><p>Name of the column that is used by some constraint</p>                                                                                    |
| <p><code>constraint_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the constraint (always the current database)</p>                                                |
| <p><code>constraint_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the constraint</p>                                                                                 |
| <p><code>constraint_name</code> <code>sql_identifier</code></p><p>Name of the constraint</p>                                                                                                            |
