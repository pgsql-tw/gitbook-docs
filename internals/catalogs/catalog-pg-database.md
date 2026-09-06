## 52.15. `pg_database` [#](#CATALOG-PG-DATABASE)

<a id="id-1.10.4.17.2"></a>

The catalog `pg_database` stores information about
the available databases. Databases are created with the [`CREATE DATABASE`](../../reference/sql-commands/sql-createdatabase.md) command.
Consult [Chapter 22](../../server-administration/managing-databases/README.md) for details about the meaning
of some of the parameters.

Unlike most system catalogs, `pg_database`
is shared across all databases of a cluster: there is only one
copy of `pg_database` per cluster, not
one per database.

<a id="id-1.10.4.17.5"></a>

**Table 52.15. `pg_database` Columns**

<table border="1" class="table" summary="pg_database Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Database name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datdba</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the database, usually the user who created it
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">encoding</code> <code class="type">int4</code>
</p>
<p>
       Character encoding for this database
       (<a class="link" href="../../the-sql-language/functions/functions-info.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a> can translate
       this number to the encoding name)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datlocprovider</code> <code class="type">char</code>
</p>
<p>
       Locale provider for this database: <code class="literal">b</code> = builtin,
       <code class="literal">c</code> = libc, <code class="literal">i</code> = icu </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datistemplate</code> <code class="type">bool</code>
</p>
<p>
       If true, then this database can be cloned by
       any user with <code class="literal">CREATEDB</code> privileges;
       if false, then only superusers or the owner of
       the database can clone it.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datallowconn</code> <code class="type">bool</code>
</p>
<p>
       If false then no one can connect to this database.  This is
       used to protect the <code class="literal">template0</code> database from being altered.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dathasloginevt</code> <code class="type">bool</code>
</p>
<p>
        Indicates that there are login event triggers defined for this database.
        This flag is used to avoid extra lookups on the
        <code class="structname">pg_event_trigger</code> table during each backend
        startup.  This flag is used internally by <span class="productname">PostgreSQL</span>
        and should not be manually altered or read for monitoring purposes.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datconnlimit</code> <code class="type">int4</code>
</p>
<p>
       Sets maximum number of concurrent connections that can be made
       to this database.  -1 means no limit, -2 indicates the database is
       invalid.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datfrozenxid</code> <code class="type">xid</code>
</p>
<p>
       All transaction IDs before this one have been replaced with a permanent
       (<span class="quote">“<span class="quote">frozen</span>”</span>) transaction ID in this database.  This is used to
       track whether the database needs to be vacuumed in order to prevent
       transaction ID wraparound or to allow <code class="literal">pg_xact</code> to be shrunk.
       It is the minimum of the per-table
       <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relfrozenxid</code> values.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datminmxid</code> <code class="type">xid</code>
</p>
<p>
       All multixact IDs before this one have been replaced with a
       transaction ID in this database.  This is used to
       track whether the database needs to be vacuumed in order to prevent
       multixact ID wraparound or to allow <code class="literal">pg_multixact</code> to be shrunk.
       It is the minimum of the per-table
       <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relminmxid</code> values.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dattablespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The default tablespace for the database.
       Within this database, all tables for which
       <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">reltablespace</code> is zero
       will be stored in this tablespace; in particular, all the non-shared
       system catalogs will be there.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datcollate</code> <code class="type">text</code>
</p>
<p>
       LC_COLLATE for this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datctype</code> <code class="type">text</code>
</p>
<p>
       LC_CTYPE for this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datlocale</code> <code class="type">text</code>
</p>
<p>
       Collation provider locale name for this database. If the
       provider is <code class="literal">libc</code>,
       <code class="structfield">datlocale</code> is <code class="literal">NULL</code>;
       <code class="structfield">datcollate</code> and
       <code class="structfield">datctype</code> are used instead.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">daticurules</code> <code class="type">text</code>
</p>
<p>
       ICU collation rules for this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datcollversion</code> <code class="type">text</code>
</p>
<p>
       Provider-specific version of the collation.  This is recorded when the
       database is created and then checked when it is used, to detect
       changes in the collation definition that could lead to data corruption.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Access privileges; see <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-database.html)（英文原文，待翻譯）
