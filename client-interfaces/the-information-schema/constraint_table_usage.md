# 37.19. constraint\_table\_usage

The view `constraint_table_usage` identifies all tables in the current database that are used by some constraint and are owned by a currently enabled role. (This is different from the view `table_constraints`, which identifies all table constraints along with the table they are defined on.) For a foreign key constraint, this view identifies the table that the foreign key references. For a unique or primary key constraint, this view simply identifies the table the constraint belongs to. Check constraints and not-null constraints are not included in this view.

#### **Table 37.17. `constraint_table_usage` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the table that is used by some constraint (always the current database)</p> |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the table that is used by some constraint</p>                                  |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the table that is used by some constraint</p>                                                             |
| <p><code>constraint_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the constraint (always the current database)</p>                       |
| <p><code>constraint_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the constraint</p>                                                        |
| <p><code>constraint_name</code> <code>sql_identifier</code></p><p>Name of the constraint</p>                                                                                   |
