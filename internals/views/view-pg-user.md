## 53.35. `pg_user` [#](#VIEW-PG-USER)

<a id="id-1.10.5.39.2"></a>

The view `pg_user` provides access to
information about database users. This is simply a publicly
readable view of
[`pg_shadow`](view-pg-shadow.md)
that blanks out the password field.

<a id="id-1.10.5.39.4"></a>

**Table 53.35. `pg_user` Columns**

<table border="1" class="table" summary="pg_user Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       User name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
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
       Not the password (always reads as <code class="literal">********</code>)
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-user.html)（英文原文，待翻譯）
