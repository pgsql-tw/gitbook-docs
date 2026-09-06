## 52.45. `pg_rewrite` [#](#CATALOG-PG-REWRITE)

<a id="id-1.10.4.47.2"></a>

The catalog `pg_rewrite` stores rewrite rules for tables and views.

<a id="id-1.10.4.47.4"></a>

**Table 52.45. `pg_rewrite` Columns**

<table border="1" class="table" summary="pg_rewrite Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">rulename</code> <code class="type">name</code>
</p>
<p>
       Rule name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_class</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table this rule is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_type</code> <code class="type">char</code>
</p>
<p>
       Event type that the rule is for: 1 = <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a>, 2 =
       <a class="xref" href="../../reference/sql-commands/sql-update.md"><span class="refentrytitle">UPDATE</span></a>, 3 = <a class="xref" href="../../reference/sql-commands/sql-insert.md"><span class="refentrytitle">INSERT</span></a>, 4 =
       <a class="xref" href="../../reference/sql-commands/sql-delete.md"><span class="refentrytitle">DELETE</span></a>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_enabled</code> <code class="type">char</code>
</p>
<p>
       Controls in which <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> modes
       the rule fires.
       <code class="literal">O</code> = rule fires in <span class="quote">“<span class="quote">origin</span>”</span> and <span class="quote">“<span class="quote">local</span>”</span> modes,
       <code class="literal">D</code> = rule is disabled,
       <code class="literal">R</code> = rule fires in <span class="quote">“<span class="quote">replica</span>”</span> mode,
       <code class="literal">A</code> = rule fires always.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_instead</code> <code class="type">bool</code>
</p>
<p>
       True if the rule is an <code class="literal">INSTEAD</code> rule
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_qual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression tree (in the form of a
       <code class="function">nodeToString()</code> representation) for the
       rule's qualifying condition
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_action</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Query tree (in the form of a
       <code class="function">nodeToString()</code> representation) for the
       rule's action
      </p></td></tr></tbody></table>

<br>

### Note

`pg_class.relhasrules`
must be true if a table has any rules in this catalog.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-rewrite.html)（英文原文，待翻譯）
