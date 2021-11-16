# 36.10. collations

The view `collations` contains the collations available in the current database.

#### **Table 36.8. `collations` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>collation_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the collation (always the current database)</p>                     |
| <p><code>collation_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the collation</p>                                                      |
| <p><code>collation_name</code> <code>sql_identifier</code></p><p>Name of the default collation</p>                                                                      |
| <p><code>pad_attribute</code> <code>character_data</code></p><p>Always <code>NO PAD</code> (The alternative <code>PAD SPACE</code> is not supported by PostgreSQL.)</p> |
