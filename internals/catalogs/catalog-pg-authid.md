## 52.8. `pg_authid` [#](#CATALOG-PG-AUTHID)

<a id="id-1.10.4.10.2"></a>

The catalog `pg_authid` contains information about
database authorization identifiers (roles). A role subsumes the concepts
of “users” and “groups”. A user is essentially just a
role with the `rolcanlogin` flag set. Any role (with or
without `rolcanlogin`) can have other roles as members; see
[`pg_auth_members`](catalog-pg-auth-members.md).

Since this catalog contains passwords, it must not be publicly readable.
[`pg_roles`](../views/view-pg-roles.md)
is a publicly readable view on
`pg_authid` that blanks out the password field.

[Chapter 21](../../server-administration/user-manag/README.md) contains detailed information about user and
privilege management.

Because user identities are cluster-wide,
`pg_authid`
is shared across all databases of a cluster: there is only one
copy of `pg_authid` per cluster, not
one per database.

<a id="id-1.10.4.10.7"></a>

**Table 52.8. `pg_authid` Columns**

<table border="1" class="table" summary="pg_authid Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolname</code> <code class="type">name</code>
</p>
<p>
       Role name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolsuper</code> <code class="type">bool</code>
</p>
<p>
       Role has superuser privileges
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolinherit</code> <code class="type">bool</code>
</p>
<p>
       Role automatically inherits privileges of roles it is a
       member of
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreaterole</code> <code class="type">bool</code>
</p>
<p>
       Role can create more roles
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreatedb</code> <code class="type">bool</code>
</p>
<p>
       Role can create databases
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcanlogin</code> <code class="type">bool</code>
</p>
<p>
       Role can log in. That is, this role can be given as the initial
       session authorization identifier.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolreplication</code> <code class="type">bool</code>
</p>
<p>
       Role is a replication role. A replication role can initiate replication
       connections and create and drop replication slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolbypassrls</code> <code class="type">bool</code>
</p>
<p>
       Role bypasses every row-level security policy, see
       <a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">Section 5.9</a> for more information.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolconnlimit</code> <code class="type">int4</code>
</p>
<p>
       For roles that can log in, this sets maximum number of concurrent
       connections this role can make.  -1 means no limit.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolpassword</code> <code class="type">text</code>
</p>
<p>
       Encrypted password; null if none. The format depends
       on the form of encryption used.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolvaliduntil</code> <code class="type">timestamptz</code>
</p>
<p>
       Password expiry time (only used for password authentication);
       null if no expiration
      </p></td></tr></tbody></table>

<br>

For an MD5 encrypted password, `rolpassword`
column will begin with the string `md5` followed by a
32-character hexadecimal MD5 hash. The MD5 hash will be of the user's
password concatenated to their user name. For example, if user
`joe` has password `xyzzy`, PostgreSQL
will store the md5 hash of `xyzzyjoe`.

### Warning

Support for MD5-encrypted passwords is deprecated and will be removed in a
future release of PostgreSQL. Refer to
[Section 20.5](../../server-administration/client-authentication/auth-password.md) for details about migrating to another
password type.

If the password is encrypted with SCRAM-SHA-256, it has the format:

```

SCRAM-SHA-256$<iteration count>:<salt>$<StoredKey>:<ServerKey>
```

where *`salt`*, *`StoredKey`* and
*`ServerKey`* are in Base64 encoded format. This format is
the same as that specified by [RFC 5803](https://datatracker.ietf.org/doc/html/rfc5803).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-authid.html)（英文原文，待翻譯）
