# 37.9. check\_constraints

The view `check_constraints` contains all check constraints, either defined on a table or on a domain, that are owned by a currently enabled role. (The owner of the table or domain is the owner of the constraint.)

#### **Table 37.7. `check_constraints` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>constraint_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the constraint (always the current database)</p> |
| <p><code>constraint_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the constraint</p>                                  |
| <p><code>constraint_name</code> <code>sql_identifier</code></p><p>Name of the constraint</p>                                                          |
| <p><code>check_clause</code> <code>character_data</code></p><p>The check expression of the check constraint</p>                                       |
