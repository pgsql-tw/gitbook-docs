## 53.4. `pg_available_extension_versions` [#](#VIEW-PG-AVAILABLE-EXTENSION-VERSIONS)

<a id="id-1.10.5.8.2"></a>

The `pg_available_extension_versions` view lists the
specific extension versions that are available for installation.
See also the [`pg_extension`](../catalogs/catalog-pg-extension.md)
catalog, which shows the extensions currently installed.

<a id="id-1.10.5.8.4"></a>

**Table 53.4. `pg_available_extension_versions` Columns**

<table border="1" class="table" summary="pg_available_extension_versions Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">name</code>
</p>
<p>
       Extension name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">version</code> <code class="type">text</code>
</p>
<p>
       Version name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">installed</code> <code class="type">bool</code>
</p>
<p>
       True if this version of this extension is currently
       installed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">superuser</code> <code class="type">bool</code>
</p>
<p>
       True if only superusers are allowed to install this extension
       (but see <code class="structfield">trusted</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trusted</code> <code class="type">bool</code>
</p>
<p>
       True if the extension can be installed by non-superusers
       with appropriate privileges
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relocatable</code> <code class="type">bool</code>
</p>
<p>
       True if extension can be relocated to another schema
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema</code> <code class="type">name</code>
</p>
<p>
       Name of the schema that the extension must be installed into,
       or <code class="literal">NULL</code> if partially or fully relocatable
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">requires</code> <code class="type">name[]</code>
</p>
<p>
       Names of prerequisite extensions,
       or <code class="literal">NULL</code> if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comment</code> <code class="type">text</code>
</p>
<p>
       Comment string from the extension's control file
      </p></td></tr></tbody></table>

<br>

The `pg_available_extension_versions` view is
read-only.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-available-extension-versions.html)（英文原文，待翻譯）
