## 52.48. `pg_shdepend` [#](#CATALOG-PG-SHDEPEND)

<a id="id-1.10.4.50.2"></a>

The catalog `pg_shdepend` records the
dependency relationships between database objects and shared objects,
such as roles. This information allows
PostgreSQL to ensure that those objects are
unreferenced before attempting to delete them.

See also [`pg_depend`](catalog-pg-depend.md),
which performs a similar function for dependencies involving objects
within a single database.

Unlike most system catalogs, `pg_shdepend`
is shared across all databases of a cluster: there is only one
copy of `pg_shdepend` per cluster, not
one per database.

<a id="id-1.10.4.50.6"></a>

**Table 52.48. `pg_shdepend` Columns**

<table border="1" class="table" summary="pg_shdepend Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dbid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the database the dependent object is in,
       or zero for a shared object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the system catalog the dependent object is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objid</code> <code class="type">oid</code>
       (references any OID column)
      </p>
<p>
       The OID of the specific dependent object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       For a table column, this is the column number (the
       <code class="structfield">objid</code> and <code class="structfield">classid</code> refer to the
       table itself).  For all other object types, this column is zero.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refclassid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the system catalog the referenced object is in
       (must be a shared catalog)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refobjid</code> <code class="type">oid</code>
       (references any OID column)
      </p>
<p>
       The OID of the specific referenced object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">deptype</code> <code class="type">char</code>
</p>
<p>
       A code defining the specific semantics of this dependency relationship; see text
      </p></td></tr></tbody></table>

<br>

In all cases, a `pg_shdepend` entry indicates that
the referenced object cannot be dropped without also dropping the dependent
object. However, there are several subflavors identified by
`deptype`:

`SHARED_DEPENDENCY_OWNER` (`o`)
:   The referenced object (which must be a role) is the owner of the
    dependent object.

`SHARED_DEPENDENCY_ACL` (`a`)
:   The referenced object (which must be a role) is mentioned in the
    ACL of the
    dependent object. (A `SHARED_DEPENDENCY_ACL` entry is
    not made for the owner of the object, since the owner will have
    a `SHARED_DEPENDENCY_OWNER` entry anyway.)

`SHARED_DEPENDENCY_INITACL` (`i`)
:   The referenced object (which must be a role) is mentioned in a
    [`pg_init_privs`](catalog-pg-init-privs.md)
    entry for the dependent object.

`SHARED_DEPENDENCY_POLICY` (`r`)
:   The referenced object (which must be a role) is mentioned as the
    target of a dependent policy object.

`SHARED_DEPENDENCY_TABLESPACE` (`t`)
:   The referenced object (which must be a tablespace) is mentioned as
    the tablespace for a relation that doesn't have storage.

Other dependency flavors might be needed in future. Note in particular
that the current definition only supports roles and tablespaces as referenced
objects.

As in the `pg_depend` catalog, most objects
created during initdb are
considered “pinned”. No entries are made
in `pg_shdepend` that would have a pinned
object as either referenced or dependent object.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-shdepend.html)（英文原文，待翻譯）
