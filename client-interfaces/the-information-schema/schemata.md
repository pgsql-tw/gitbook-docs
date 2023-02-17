# 37.46. schemata

The view `schemata` contains all schemas in the current database that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.44. `schemata` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>catalog_name</code> <code>sql_identifier</code></p><p>Name of the database that the schema is contained in (always the current database)</p> |
| <p><code>schema_name</code> <code>sql_identifier</code></p><p>Name of the schema</p>                                                                  |
| <p><code>schema_owner</code> <code>sql_identifier</code></p><p>Name of the owner of the schema</p>                                                    |
| <p><code>default_character_set_catalog</code> <code>sql_identifier</code></p><p>Applies to a feature not available in PostgreSQL</p>                  |
| <p><code>default_character_set_schema</code> <code>sql_identifier</code></p><p>Applies to a feature not available in PostgreSQL</p>                   |
| <p><code>default_character_set_name</code> <code>sql_identifier</code></p><p>Applies to a feature not available in PostgreSQL</p>                     |
| <p><code>sql_path</code> <code>character_data</code></p><p>Applies to a feature not available in PostgreSQL</p>                                       |
