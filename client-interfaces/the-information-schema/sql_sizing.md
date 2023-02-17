# 37.51. sql\_sizing

The table `sql_sizing` contains information about various size limits and maximum values in PostgreSQL. This information is primarily intended for use in the context of the ODBC interface; users of other interfaces will probably find this information to be of little use. For this reason, the individual sizing items are not described here; you will find them in the description of the ODBC interface.

**Table 37.49. `sql_sizing` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>sizing_id</code> <code>cardinal_number</code></p><p>Identifier of the sizing item</p>                                                                                                                                            |
| <p><code>sizing_name</code> <code>character_data</code></p><p>Descriptive name of the sizing item</p>                                                                                                                                     |
| <p><code>supported_value</code> <code>cardinal_number</code></p><p>Value of the sizing item, or 0 if the size is unlimited or cannot be determined, or null if the features for which the sizing item is applicable are not supported</p> |
| <p><code>comments</code> <code>character_data</code></p><p>Possibly a comment pertaining to the sizing item</p>                                                                                                                           |
