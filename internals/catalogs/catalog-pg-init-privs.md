## 52.28. `pg_init_privs` [#](#CATALOG-PG-INIT-PRIVS)

<a id="id-1.10.4.30.2"></a>

The catalog `pg_init_privs` records information about
the initial privileges of objects in the system. There is one entry
for each object in the database which has a non-default (non-NULL)
initial set of privileges.

Objects can have initial privileges either by having those privileges set
when the system is initialized (by initdb) or when the
object is created during a [`CREATE EXTENSION`](../../reference/sql-commands/sql-createextension.md) and the
extension script sets initial privileges using the [`GRANT`](../../reference/sql-commands/sql-grant.md)
system. Note that the system will automatically handle recording of the
privileges during the extension script and that extension authors need
only use the `GRANT` and `REVOKE`
statements in their script to have the privileges recorded. The
`privtype` column indicates if the initial privilege was
set by initdb or during a
`CREATE EXTENSION` command.

Objects which have initial privileges set by initdb will
have entries where `privtype` is
`'i'`, while objects which have initial privileges set
by `CREATE EXTENSION` will have entries where
`privtype` is `'e'`.

<a id="id-1.10.4.30.6"></a>

**Table 52.28. `pg_init_privs` Columns**

<table border="1" class="table" summary="pg_init_privs Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       (references any OID column)
      </p>
<p>
       The OID of the specific object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the system catalog the object is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       For a table column, this is the column number (the
       <code class="structfield">objoid</code> and <code class="structfield">classoid</code> refer to the
       table itself).  For all other object types, this column is
       zero.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privtype</code> <code class="type">char</code>
</p>
<p>
       A code defining the type of initial privilege of this object; see text
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">initprivs</code> <code class="type">aclitem[]</code>
</p>
<p>
       The initial access privileges; see
       <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-init-privs.html)（英文原文，待翻譯）
