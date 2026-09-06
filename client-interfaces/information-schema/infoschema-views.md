## 35.66. `views` [#](#INFOSCHEMA-VIEWS)

The view `views` contains all views defined in the
current database. Only those views are shown that the current user
has access to (by way of being the owner or having some privilege).

<a id="id-1.7.6.70.3"></a>

**Table 35.64. `views` Columns**

<table border="1" class="table" summary="views Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the view (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_definition</code> <code class="type">character_data</code>
</p>
<p>
       Query expression defining the view (null if the view is not
       owned by a currently enabled role)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">check_option</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">CASCADED</code> or <code class="literal">LOCAL</code> if the view
       has a <code class="literal">CHECK OPTION</code> defined on it,
       <code class="literal">NONE</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_updatable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the view is updatable (allows
       <code class="command">UPDATE</code> and <code class="command">DELETE</code>),
       <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_insertable_into</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the view is insertable into (allows
       <code class="command">INSERT</code>), <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_updatable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the view has an <code class="literal">INSTEAD OF</code>
<code class="command">UPDATE</code> trigger defined on it, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_deletable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the view has an <code class="literal">INSTEAD OF</code>
<code class="command">DELETE</code> trigger defined on it, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_insertable_into</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the view has an <code class="literal">INSTEAD OF</code>
<code class="command">INSERT</code> trigger defined on it, <code class="literal">NO</code> if not
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-views.html)（英文原文，待翻譯）
