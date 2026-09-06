# 37.48. sql\_features

The table `sql_features` contains information about which formal features defined in the SQL standard are supported by PostgreSQL. This is the same information that is presented in [Appendix D](https://www.postgresql.org/docs/current/features.html). There you can also find some additional background information.

#### **Table 37.46. `sql_features` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>feature_id</code> <code>character_data</code></p><p>Identifier string of the feature</p>                                                                               |
| <p><code>feature_name</code> <code>character_data</code></p><p>Descriptive name of the feature</p>                                                                              |
| <p><code>sub_feature_id</code> <code>character_data</code></p><p>Identifier string of the subfeature, or a zero-length string if not a subfeature</p>                           |
| <p><code>sub_feature_name</code> <code>character_data</code></p><p>Descriptive name of the subfeature, or a zero-length string if not a subfeature</p>                          |
| <p><code>is_supported</code> <code>yes_or_no</code></p><p><code>YES</code> if the feature is fully supported by the current version of PostgreSQL, <code>NO</code> if not</p>   |
| <p><code>is_verified_by</code> <code>character_data</code></p><p>Always null, since the PostgreSQL development group does not perform formal testing of feature conformance</p> |
| <p><code>comments</code> <code>character_data</code></p><p>Possibly a comment about the supported status of the feature</p>                                                     |
