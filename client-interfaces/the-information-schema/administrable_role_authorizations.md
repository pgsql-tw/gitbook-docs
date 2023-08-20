# 37.4. administrable\_role\_authorizations

The view `administrable_role_authorizations` identifies all roles that the current user has the admin option for.

**Table 37.2. `administrable_role_authorizations` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>grantee</code> <code>sql_identifier</code></p><p>Name of the role to which this role membership was granted (can be the current user, or a different role in case of nested role memberships)</p> |
| <p><code>role_name</code> <code>sql_identifier</code></p><p>Name of a role</p>                                                                                                                             |
| <p><code>is_grantable</code> <code>yes_or_no</code></p><p>Always <code>YES</code></p>                                                                                                                      |
