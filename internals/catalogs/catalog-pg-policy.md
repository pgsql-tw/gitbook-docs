## 52.38. `pg_policy` [#](#CATALOG-PG-POLICY)

<a id="id-1.10.4.40.2"></a>

The catalog `pg_policy` stores row-level
security policies for tables. A policy includes the kind of
command that it applies to (possibly all commands), the roles that it
applies to, the expression to be added as a security-barrier
qualification to queries that include the table, and the expression
to be added as a `WITH CHECK` option for queries that attempt to
add new records to the table.

<a id="id-1.10.4.40.4"></a>

**Table 52.38. `pg_policy` Columns**

<table border="1" class="table" summary="pg_policy Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">polname</code> <code class="type">name</code>
</p>
<p>
       The name of the policy
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table to which the policy applies
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polcmd</code> <code class="type">char</code>
</p>
<p>
       The command type to which the policy is applied:
       <code class="literal">r</code> for <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a>,
       <code class="literal">a</code> for <a class="xref" href="../../reference/sql-commands/sql-insert.md"><span class="refentrytitle">INSERT</span></a>,
       <code class="literal">w</code> for <a class="xref" href="../../reference/sql-commands/sql-update.md"><span class="refentrytitle">UPDATE</span></a>,
       <code class="literal">d</code> for <a class="xref" href="../../reference/sql-commands/sql-delete.md"><span class="refentrytitle">DELETE</span></a>,
       or <code class="literal">*</code> for all
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polpermissive</code> <code class="type">bool</code>
</p>
<p>
       Is the policy permissive or restrictive?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polroles</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The roles to which the policy is applied;
       zero means <code class="literal">PUBLIC</code>
       (and normally appears alone in the array)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polqual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       The expression tree to be added to the security barrier qualifications for queries that use the table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polwithcheck</code> <code class="type">pg_node_tree</code>
</p>
<p>
       The expression tree to be added to the WITH CHECK qualifications for queries that attempt to add rows to the table
      </p></td></tr></tbody></table>

<br>

### Note

Policies stored in `pg_policy` are applied only when
[`pg_class`](catalog-pg-class.md).`relrowsecurity` is set for
their table.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-policy.html)（英文原文，待翻譯）
