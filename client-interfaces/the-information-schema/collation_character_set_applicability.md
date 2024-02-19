# 37.11. collation\_character\_set\_applicability

The view `collation_character_set_applicability` identifies which character set the available collations are applicable to. In PostgreSQL, there is only one character set per database (see explanation in [Section 37.7](https://www.postgresql.org/docs/current/infoschema-character-sets.html)), so this view does not provide much useful information.

#### **Table 37.9. `collation_character_set_applicability` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>collation_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the collation (always the current database)</p>                |
| <p><code>collation_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the collation</p>                                                 |
| <p><code>collation_name</code> <code>sql_identifier</code></p><p>Name of the default collation</p>                                                                 |
| <p><code>character_set_catalog</code> <code>sql_identifier</code></p><p>Character sets are currently not implemented as schema objects, so this column is null</p> |
| <p><code>character_set_schema</code> <code>sql_identifier</code></p><p>Character sets are currently not implemented as schema objects, so this column is null</p>  |
| <p><code>character_set_name</code> <code>sql_identifier</code></p><p>Name of the character set</p>                                                                 |
