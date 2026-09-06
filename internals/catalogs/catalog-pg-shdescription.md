## 52.49. `pg_shdescription` [#](#CATALOG-PG-SHDESCRIPTION)

<a id="id-1.10.4.51.2"></a>

The catalog `pg_shdescription` stores optional
descriptions (comments) for shared database objects. Descriptions can be
manipulated with the [`COMMENT`](../../reference/sql-commands/sql-comment.md) command and viewed with
psql's `\d` commands.

See also [`pg_description`](catalog-pg-description.md),
which performs a similar function for descriptions involving objects
within a single database.

Unlike most system catalogs, `pg_shdescription`
is shared across all databases of a cluster: there is only one
copy of `pg_shdescription` per cluster, not
one per database.

<a id="id-1.10.4.51.6"></a>

**Table 52.49. `pg_shdescription` Columns**

<table border="1" class="table" summary="pg_shdescription Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       (references any OID column)
      </p>
<p>
       The OID of the object this description pertains to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the system catalog this object appears in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">description</code> <code class="type">text</code>
</p>
<p>
       Arbitrary text that serves as the description of this object
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-shdescription.html)（英文原文，待翻譯）
