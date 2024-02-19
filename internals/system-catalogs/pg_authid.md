# 51.8. pg\_authid

The catalog `pg_authid` contains information about database authorization identifiers (roles). A role subsumes the concepts of “users” and “groups”. A user is essentially just a role with the `rolcanlogin` flag set. Any role (with or without `rolcanlogin`) can have other roles as members; see [`pg_auth_members`](https://www.postgresql.org/docs/13/catalog-pg-auth-members.html).

Since this catalog contains passwords, it must not be publicly readable. [`pg_roles`](https://www.postgresql.org/docs/13/view-pg-roles.html) is a publicly readable view on `pg_authid` that blanks out the password field.

[Chapter 21](https://www.postgresql.org/docs/13/user-manag.html) contains detailed information about user and privilege management.

Because user identities are cluster-wide, `pg_authid` is shared across all databases of a cluster: there is only one copy of `pg_authid` per cluster, not one per database.

#### **Table 51.8. `pg_authid` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>oid</code> <code>oid</code></p><p>Row identifier</p>                                                                                                                                                       |
| <p><code>rolname</code> <code>name</code></p><p>Role name</p>                                                                                                                                                       |
| <p><code>rolsuper</code> <code>bool</code></p><p>Role has superuser privileges</p>                                                                                                                                  |
| <p><code>rolinherit</code> <code>bool</code></p><p>Role automatically inherits privileges of roles it is a member of</p>                                                                                            |
| <p><code>rolcreaterole</code> <code>bool</code></p><p>Role can create more roles</p>                                                                                                                                |
| <p><code>rolcreatedb</code> <code>bool</code></p><p>Role can create databases</p>                                                                                                                                   |
| <p><code>rolcanlogin</code> <code>bool</code></p><p>Role can log in. That is, this role can be given as the initial session authorization identifier</p>                                                            |
| <p><code>rolreplication</code> <code>bool</code></p><p>Role is a replication role. A replication role can initiate replication connections and create and drop replication slots.</p>                               |
| <p><code>rolbypassrls</code> <code>bool</code></p><p>Role bypasses every row level security policy, see <a href="https://www.postgresql.org/docs/13/ddl-rowsecurity.html">Section 5.8</a> for more information.</p> |
| <p><code>rolconnlimit</code> <code>int4</code></p><p>For roles that can log in, this sets maximum number of concurrent connections this role can make. -1 means no limit.</p>                                       |
| <p><code>rolpassword</code> <code>text</code></p><p>Password (possibly encrypted); null if none. The format depends on the form of encryption used.</p>                                                             |
| <p><code>rolvaliduntil</code> <code>timestamptz</code></p><p>Password expiry time (only used for password authentication); null if no expiration</p>                                                                |

For an MD5 encrypted password, `rolpassword` column will begin with the string `md5` followed by a 32-character hexadecimal MD5 hash. The MD5 hash will be of the user's password concatenated to their user name. For example, if user `joe` has password `xyzzy`, PostgreSQL will store the md5 hash of `xyzzyjoe`.

If the password is encrypted with SCRAM-SHA-256, it has the format:

```
SCRAM-SHA-256$<iteration count>:<salt>$<StoredKey>:<ServerKey>
```

where _`salt`_, _`StoredKey`_ and _`ServerKey`_ are in Base64 encoded format. This format is the same as that specified by RFC 5803.

A password that does not follow either of those formats is assumed to be unencrypted.
