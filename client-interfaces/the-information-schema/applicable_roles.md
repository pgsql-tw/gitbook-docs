# 37.5. applicable\_roles

The view `applicable_roles` identifies all roles whose privileges the current user can use. This means there is some chain of role grants from the current user to the role in question. The current user itself is also an applicable role. The set of applicable roles is generally used for permission checking.

#### **Table 37.3. `applicable_roles` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>grantee</code> <code>sql_identifier</code></p><p>Name of the role to which this role membership was granted (can be the current user, or a different role in case of nested role memberships)</p> |
| <p><code>role_name</code> <code>sql_identifier</code></p><p>Name of a role</p>                                                                                                                             |
| <p><code>is_grantable</code> <code>yes_or_no</code></p><p><code>YES</code> if the grantee has the admin option on the role, <code>NO</code> if not</p>                                                     |
