## 52.12. `pg_collation` [#](#CATALOG-PG-COLLATION)

<a id="id-1.10.4.14.2"></a>

The catalog `pg_collation` describes the
available collations, which are essentially mappings from an SQL
name to operating system locale categories.
See [Section 23.2](../../server-administration/charset/collation.md) for more information.

<a id="id-1.10.4.14.4"></a>

**Table 52.12. `pg_collation` Columns**

<table border="1" class="table" summary="pg_collation Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">collname</code> <code class="type">name</code>
</p>
<p>
       Collation name (unique per namespace and encoding)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this collation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the collation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collprovider</code> <code class="type">char</code>
</p>
<p>
       Provider of the collation: <code class="literal">d</code> = database default,
       <code class="literal">b</code> = builtin, <code class="literal">c</code> = libc,
       <code class="literal">i</code> = icu </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collisdeterministic</code> <code class="type">bool</code>
</p>
<p>
       Is the collation deterministic?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collencoding</code> <code class="type">int4</code>
</p>
<p>
       Encoding in which the collation is applicable, or -1 if it
       works for any encoding
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collcollate</code> <code class="type">text</code>
</p>
<p>
<code class="symbol">LC_COLLATE</code> for this collation object. If the provider is
       not <code class="literal">libc</code>, <code class="structfield">collcollate</code> is
       <code class="literal">NULL</code> and <code class="structfield">colllocale</code> is
       used instead.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collctype</code> <code class="type">text</code>
</p>
<p>
<code class="symbol">LC_CTYPE</code> for this collation object. If the provider is
       not <code class="literal">libc</code>, <code class="structfield">collctype</code> is
       <code class="literal">NULL</code> and <code class="structfield">colllocale</code> is
       used instead.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">colllocale</code> <code class="type">text</code>
</p>
<p>
       Collation provider locale name for this collation object. If the
       provider is <code class="literal">libc</code>,
       <code class="structfield">colllocale</code> is <code class="literal">NULL</code>;
       <code class="structfield">collcollate</code> and
       <code class="structfield">collctype</code> are used instead.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collicurules</code> <code class="type">text</code>
</p>
<p>
       ICU collation rules for this collation object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collversion</code> <code class="type">text</code>
</p>
<p>
       Provider-specific version of the collation.  This is recorded when the
       collation is created and then checked when it is used, to detect
       changes in the collation definition that could lead to data corruption.
      </p></td></tr></tbody></table>

<br>

Note that the unique key on this catalog is (`collname`,
`collencoding`, `collnamespace`) not just
(`collname`, `collnamespace`).
PostgreSQL generally ignores all
collations that do not have `collencoding` equal to
either the current database's encoding or -1, and creation of new entries
with the same name as an entry with `collencoding` = -1
is forbidden. Therefore it is sufficient to use a qualified SQL name
(*`schema`*.*`name`*) to identify a collation,
even though this is not unique according to the catalog definition.
The reason for defining the catalog this way is that
initdb fills it in at cluster initialization time with
entries for all locales available on the system, so it must be able to
hold entries for all encodings that might ever be used in the cluster.

In the `template0` database, it could be useful to create
collations whose encoding does not match the database encoding,
since they could match the encodings of databases later cloned from
`template0`. This would currently have to be done manually.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-collation.html)（英文原文，待翻譯）
