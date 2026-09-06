## 35.48. `sql_features` [#](#INFOSCHEMA-SQL-FEATURES)

The table `sql_features` contains information
about which formal features defined in the SQL standard are
supported by PostgreSQL. This is the
same information that is presented in [Appendix D](../../appendixes/features/README.md).
There you can also find some additional background information.

<a id="id-1.7.6.52.3"></a>

**Table 35.46. `sql_features` Columns**

<table border="1" class="table" summary="sql_features Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_id</code> <code class="type">character_data</code>
</p>
<p>
       Identifier string of the feature
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_name</code> <code class="type">character_data</code>
</p>
<p>
       Descriptive name of the feature
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sub_feature_id</code> <code class="type">character_data</code>
</p>
<p>
       Identifier string of the subfeature, or a zero-length string if not a subfeature
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sub_feature_name</code> <code class="type">character_data</code>
</p>
<p>
       Descriptive name of the subfeature, or a zero-length string if not a subfeature
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_supported</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the feature is fully supported by the
       current version of <span class="productname">PostgreSQL</span>, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_verified_by</code> <code class="type">character_data</code>
</p>
<p>
       Always null, since the <span class="productname">PostgreSQL</span> development group does not
       perform formal testing of feature conformance
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       Possibly a comment about the supported status of the feature
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-features.html)（英文原文，待翻譯）
