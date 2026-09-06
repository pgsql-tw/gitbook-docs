## 53.9. `pg_group` [#](#VIEW-PG-GROUP)

<a id="id-1.10.5.13.2"></a>

The view `pg_group` exists for backwards
compatibility: it emulates a catalog that existed in
PostgreSQL before version 8.1.
It shows the names and members of all roles that are marked as not
`rolcanlogin`, which is an approximation to the set
of roles that are being used as groups.

<a id="id-1.10.5.13.4"></a>

**Table 53.9. `pg_group` Columns**

<table border="1" class="table" summary="pg_group Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">groname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of the group
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grosysid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       ID of this group
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grolist</code> <code class="type">oid[]</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       An array containing the IDs of the roles in this group
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-group.html)（英文原文，待翻譯）
