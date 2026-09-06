# 37.14. column\_options

The view `column_options` contains all the options defined for foreign table columns in the current database. Only those foreign table columns are shown that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.12. `column_options` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the foreign table (always the current database)</p> |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the foreign table</p>                                  |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the foreign table</p>                                                             |
| <p><code>column_name</code> <code>sql_identifier</code></p><p>Name of the column</p>                                                                   |
| <p><code>option_name</code> <code>sql_identifier</code></p><p>Name of an option</p>                                                                    |
| <p><code>option_value</code> <code>character_data</code></p><p>Value of the option</p>                                                                 |
