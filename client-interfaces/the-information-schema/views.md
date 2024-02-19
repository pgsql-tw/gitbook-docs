# 37.66. views

The view `views` contains all views defined in the current database. Only those views are shown that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.64. `views` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>table_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the view (always the current database)</p>                                                             |
| <p><code>table_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the view</p>                                                                                              |
| <p><code>table_name</code> <code>sql_identifier</code></p><p>Name of the view</p>                                                                                                                         |
| <p><code>view_definition</code> <code>character_data</code></p><p>Query expression defining the view (null if the view is not owned by a currently enabled role)</p>                                      |
| <p><code>check_option</code> <code>character_data</code></p><p><code>CASCADED</code> or <code>LOCAL</code> if the view has a <code>CHECK OPTION</code> defined on it, <code>NONE</code> if not</p>        |
| <p><code>is_updatable</code> <code>yes_or_no</code></p><p><code>YES</code> if the view is updatable (allows <code>UPDATE</code> and <code>DELETE</code>), <code>NO</code> if not</p>                      |
| <p><code>is_insertable_into</code> <code>yes_or_no</code></p><p><code>YES</code> if the view is insertable into (allows <code>INSERT</code>), <code>NO</code> if not</p>                                  |
| <p><code>is_trigger_updatable</code> <code>yes_or_no</code></p><p><code>YES</code> if the view has an <code>INSTEAD OF</code> <code>UPDATE</code> trigger defined on it, <code>NO</code> if not</p>       |
| <p><code>is_trigger_deletable</code> <code>yes_or_no</code></p><p><code>YES</code> if the view has an <code>INSTEAD OF</code> <code>DELETE</code> trigger defined on it, <code>NO</code> if not</p>       |
| <p><code>is_trigger_insertable_into</code> <code>yes_or_no</code></p><p><code>YES</code> if the view has an <code>INSTEAD OF</code> <code>INSERT</code> trigger defined on it, <code>NO</code> if not</p> |
