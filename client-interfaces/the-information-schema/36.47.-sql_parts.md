# 37.50. sql\_parts

The table `sql_parts` contains information about which of the several parts of the SQL standard are supported by PostgreSQL.

**Table 37.48. `sql_parts` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>feature_id</code> <code>character_data</code></p><p>An identifier string containing the number of the part</p>                                                         |
| <p><code>feature_name</code> <code>character_data</code></p><p>Descriptive name of the part</p>                                                                                 |
| <p><code>is_supported</code> <code>yes_or_no</code></p><p><code>YES</code> if the part is fully supported by the current version of PostgreSQL, <code>NO</code> if not</p>      |
| <p><code>is_verified_by</code> <code>character_data</code></p><p>Always null, since the PostgreSQL development group does not perform formal testing of feature conformance</p> |
| <p><code>comments</code> <code>character_data</code></p><p>Possibly a comment about the supported status of the part</p>                                                        |
