## 53.21. `pg_roles` [#](#VIEW-PG-ROLES)

<a id="id-1.10.5.25.2"></a>

The view `pg_roles` provides access to
information about database roles. This is simply a publicly
readable view of
[`pg_authid`](../catalogs/catalog-pg-authid.md)
that blanks out the password field.

<a id="id-1.10.5.25.4"></a>

**Table 53.21. `pg_roles` Columns**

<table border="1" class="table" summary="pg_roles Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
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
       session authorization identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolreplication</code> <code class="type">bool</code>
</p>
<p>
       Role is a replication role. A replication role can initiate replication
       connections and create and drop replication slots.
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
       Not the password (always reads as <code class="literal">********</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolvaliduntil</code> <code class="type">timestamptz</code>
</p>
<p>
       Password expiry time (only used for password authentication);
       null if no expiration
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolbypassrls</code> <code class="type">bool</code>
</p>
<p>
       Role bypasses every row-level security policy, see
       <a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">Section 5.9</a> for more information.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolconfig</code> <code class="type">text[]</code>
</p>
<p>
       Role-specific defaults for run-time configuration variables
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of role
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-roles.html)（英文原文，待翻譯）
