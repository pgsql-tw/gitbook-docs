## 53.26. `pg_shadow` [#](#VIEW-PG-SHADOW)

<a id="id-1.10.5.30.2"></a>

The view `pg_shadow` exists for backwards
compatibility: it emulates a catalog that existed in
PostgreSQL before version 8.1.
It shows properties of all roles that are marked as
`rolcanlogin` in
[`pg_authid`](../catalogs/catalog-pg-authid.md).

The name stems from the fact that this table
should not be readable by the public since it contains passwords.
[`pg_user`](view-pg-user.md)
is a publicly readable view on
`pg_shadow` that blanks out the password field.

<a id="id-1.10.5.30.5"></a>

**Table 53.26. `pg_shadow` Columns**

<table border="1" class="table" summary="pg_shadow Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       User name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of this user
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usecreatedb</code> <code class="type">bool</code>
</p>
<p>
       User can create databases
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesuper</code> <code class="type">bool</code>
</p>
<p>
       User is a superuser
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">userepl</code> <code class="type">bool</code>
</p>
<p>
       User can initiate streaming replication and put the system in and
       out of backup mode.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usebypassrls</code> <code class="type">bool</code>
</p>
<p>
       User bypasses every row-level security policy, see
       <a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">Section 5.9</a> for more information.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">passwd</code> <code class="type">text</code>
</p>
<p>
       Encrypted password; null if none.  See
       <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>
       for details of how encrypted passwords are stored.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">valuntil</code> <code class="type">timestamptz</code>
</p>
<p>
       Password expiry time (only used for password authentication)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">useconfig</code> <code class="type">text[]</code>
</p>
<p>
       Session defaults for run-time configuration variables
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shadow.html)（英文原文，待翻譯）
