# 37.21. domain\_constraints

The view `domain_constraints` contains all constraints belonging to domains defined in the current database. Only those domains are shown that the current user has access to (by way of being the owner or having some privilege).

**Table 37.19. `domain_constraints` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>constraint_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the constraint (always the current database)</p>            |
| <p><code>constraint_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the constraint</p>                                             |
| <p><code>constraint_name</code> <code>sql_identifier</code></p><p>Name of the constraint</p>                                                                        |
| <p><code>domain_catalog</code> <code>sql_identifier</code></p><p>Name of the database that contains the domain (always the current database)</p>                    |
| <p><code>domain_schema</code> <code>sql_identifier</code></p><p>Name of the schema that contains the domain</p>                                                     |
| <p><code>domain_name</code> <code>sql_identifier</code></p><p>Name of the domain</p>                                                                                |
| <p><code>is_deferrable</code> <code>yes_or_no</code></p><p><code>YES</code> if the constraint is deferrable, <code>NO</code> if not</p>                             |
| <p><code>initially_deferred</code> <code>yes_or_no</code></p><p><code>YES</code> if the constraint is deferrable and initially deferred, <code>NO</code> if not</p> |
