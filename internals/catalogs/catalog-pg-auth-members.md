## 52.9. `pg_auth_members` [#](#CATALOG-PG-AUTH-MEMBERS)

<a id="id-1.10.4.11.2"></a>

The catalog `pg_auth_members` shows the membership
relations between roles. Any non-circular set of relationships is allowed.

Because user identities are cluster-wide,
`pg_auth_members`
is shared across all databases of a cluster: there is only one
copy of `pg_auth_members` per cluster, not
one per database.

<a id="id-1.10.4.11.5"></a>

**Table 52.9. `pg_auth_members` Columns**

<table border="1" class="table" summary="pg_auth_members Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">roleid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of a role that has a member
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">member</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of a role that is a member of <code class="structfield">roleid</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of the role that granted this membership
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">admin_option</code> <code class="type">bool</code>
</p>
<p>
       True if <code class="structfield">member</code> can grant membership in
       <code class="structfield">roleid</code> to others
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherit_option</code> <code class="type">bool</code>
</p>
<p>
       True if the member automatically inherits the privileges of the
       granted role
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">set_option</code> <code class="type">bool</code>
</p>
<p>
       True if the member can
       <a class="link" href="../../reference/sql-commands/sql-set-role.md"><code class="command">SET ROLE</code></a>
       to the granted role
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-auth-members.html)（英文原文，待翻譯）
