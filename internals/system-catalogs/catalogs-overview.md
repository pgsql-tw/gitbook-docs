<a id="CATALOGS-OVERVIEW"></a>

# 53.1. Overview

[Table 53.1](#CATALOG-TABLE) lists the system catalogs. More detailed documentation of each catalog follows below.

Most system catalogs are copied from the template database during database creation and are thereafter database-specific. A few catalogs are physically shared across all databases in a cluster; these are noted in the descriptions of the individual catalogs.

<a id="CATALOG-TABLE"></a>

<strong>Table 53.1. System Catalogs</strong>

<table border="1" class="table" summary="System Catalogs">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Catalog Name</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><a class="link" href="pg_aggregate.md"><code class="structname">pg_aggregate</code></a></td>
<td>aggregate functions</td>
</tr>
<tr>
<td><a class="link" href="pg_am.md"><code class="structname">pg_am</code></a></td>
<td>relation access methods</td>
</tr>
<tr>
<td><a class="link" href="pg_amop.md"><code class="structname">pg_amop</code></a></td>
<td>access method operators</td>
</tr>
<tr>
<td><a class="link" href="pg_amproc.md"><code class="structname">pg_amproc</code></a></td>
<td>access method support functions</td>
</tr>
<tr>
<td><a class="link" href="pg_attrdef.md"><code class="structname">pg_attrdef</code></a></td>
<td>column default values</td>
</tr>
<tr>
<td><a class="link" href="pg_attribute.md"><code class="structname">pg_attribute</code></a></td>
<td>table columns (<span class="quote">“<span class="quote">attributes</span>”</span>)</td>
</tr>
<tr>
<td><a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a></td>
<td>authorization identifiers (roles)</td>
</tr>
<tr>
<td><a class="link" href="pg_auth_members.md"><code class="structname">pg_auth_members</code></a></td>
<td>authorization identifier membership relationships</td>
</tr>
<tr>
<td><a class="link" href="pg_cast.md"><code class="structname">pg_cast</code></a></td>
<td>casts (data type conversions)</td>
</tr>
<tr>
<td><a class="link" href="pg_class.md"><code class="structname">pg_class</code></a></td>
<td>tables, indexes, sequences, views (<span class="quote">“<span class="quote">relations</span>”</span>)</td>
</tr>
<tr>
<td><a class="link" href="pg_collation.md"><code class="structname">pg_collation</code></a></td>
<td>collations (locale information)</td>
</tr>
<tr>
<td><a class="link" href="pg_constraint.md"><code class="structname">pg_constraint</code></a></td>
<td>check constraints, unique constraints, primary key constraints, foreign key constraints</td>
</tr>
<tr>
<td><a class="link" href="pg_conversion.md"><code class="structname">pg_conversion</code></a></td>
<td>encoding conversion information</td>
</tr>
<tr>
<td><a class="link" href="pg_database.md"><code class="structname">pg_database</code></a></td>
<td>databases within this database cluster</td>
</tr>
<tr>
<td><a class="link" href="pg_db_role_setting.md"><code class="structname">pg_db_role_setting</code></a></td>
<td>per-role and per-database settings</td>
</tr>
<tr>
<td><a class="link" href="pg_default_acl.md"><code class="structname">pg_default_acl</code></a></td>
<td>default privileges for object types</td>
</tr>
<tr>
<td><a class="link" href="pg_depend.md"><code class="structname">pg_depend</code></a></td>
<td>dependencies between database objects</td>
</tr>
<tr>
<td><a class="link" href="pg_description.md"><code class="structname">pg_description</code></a></td>
<td>descriptions or comments on database objects</td>
</tr>
<tr>
<td><a class="link" href="pg_enum.md"><code class="structname">pg_enum</code></a></td>
<td>enum label and value definitions</td>
</tr>
<tr>
<td><a class="link" href="pg_event_trigger.md"><code class="structname">pg_event_trigger</code></a></td>
<td>event triggers</td>
</tr>
<tr>
<td><a class="link" href="pg_extension.md"><code class="structname">pg_extension</code></a></td>
<td>installed extensions</td>
</tr>
<tr>
<td><a class="link" href="pg_foreign_data_wrapper.md"><code class="structname">pg_foreign_data_wrapper</code></a></td>
<td>foreign-data wrapper definitions</td>
</tr>
<tr>
<td><a class="link" href="pg_foreign_server.md"><code class="structname">pg_foreign_server</code></a></td>
<td>foreign server definitions</td>
</tr>
<tr>
<td><a class="link" href="pg_foreign_table.md"><code class="structname">pg_foreign_table</code></a></td>
<td>additional foreign table information</td>
</tr>
<tr>
<td><a class="link" href="pg_index.md"><code class="structname">pg_index</code></a></td>
<td>additional index information</td>
</tr>
<tr>
<td><a class="link" href="pg_inherits.md"><code class="structname">pg_inherits</code></a></td>
<td>table inheritance hierarchy</td>
</tr>
<tr>
<td><a class="link" href="pg_init_privs.md"><code class="structname">pg_init_privs</code></a></td>
<td>object initial privileges</td>
</tr>
<tr>
<td><a class="link" href="pg_language.md"><code class="structname">pg_language</code></a></td>
<td>languages for writing functions</td>
</tr>
<tr>
<td><a class="link" href="pg_largeobject.md"><code class="structname">pg_largeobject</code></a></td>
<td>data pages for large objects</td>
</tr>
<tr>
<td><a class="link" href="pg_largeobject_metadata.md"><code class="structname">pg_largeobject_metadata</code></a></td>
<td>metadata for large objects</td>
</tr>
<tr>
<td><a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a></td>
<td>schemas</td>
</tr>
<tr>
<td><a class="link" href="pg_opclass.md"><code class="structname">pg_opclass</code></a></td>
<td>access method operator classes</td>
</tr>
<tr>
<td><a class="link" href="pg_operator.md"><code class="structname">pg_operator</code></a></td>
<td>operators</td>
</tr>
<tr>
<td><a class="link" href="pg_opfamily.md"><code class="structname">pg_opfamily</code></a></td>
<td>access method operator families</td>
</tr>
<tr>
<td><a class="link" href="pg_parameter_acl.md"><code class="structname">pg_parameter_acl</code></a></td>
<td>configuration parameters for which privileges have been granted</td>
</tr>
<tr>
<td><a class="link" href="pg_partitioned_table.md"><code class="structname">pg_partitioned_table</code></a></td>
<td>information about partition key of tables</td>
</tr>
<tr>
<td><a class="link" href="pg_policy.md"><code class="structname">pg_policy</code></a></td>
<td>row-security policies</td>
</tr>
<tr>
<td><a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a></td>
<td>functions and procedures</td>
</tr>
<tr>
<td><a class="link" href="pg_publication.md"><code class="structname">pg_publication</code></a></td>
<td>publications for logical replication</td>
</tr>
<tr>
<td><a class="link" href="pg_publication_namespace.md"><code class="structname">pg_publication_namespace</code></a></td>
<td>schema to publication mapping</td>
</tr>
<tr>
<td><a class="link" href="pg_publication_rel.md"><code class="structname">pg_publication_rel</code></a></td>
<td>relation to publication mapping</td>
</tr>
<tr>
<td><a class="link" href="pg_range.md"><code class="structname">pg_range</code></a></td>
<td>information about range types</td>
</tr>
<tr>
<td><a class="link" href="pg_replication_origin.md"><code class="structname">pg_replication_origin</code></a></td>
<td>registered replication origins</td>
</tr>
<tr>
<td><a class="link" href="51.44.-pg_rewrite.md"><code class="structname">pg_rewrite</code></a></td>
<td>query rewrite rules</td>
</tr>
<tr>
<td><a class="link" href="pg_seclabel.md"><code class="structname">pg_seclabel</code></a></td>
<td>security labels on database objects</td>
</tr>
<tr>
<td><a class="link" href="pg_sequence.md"><code class="structname">pg_sequence</code></a></td>
<td>information about sequences</td>
</tr>
<tr>
<td><a class="link" href="pg_shdepend.md"><code class="structname">pg_shdepend</code></a></td>
<td>dependencies on shared objects</td>
</tr>
<tr>
<td><a class="link" href="pg_shdescription.md"><code class="structname">pg_shdescription</code></a></td>
<td>comments on shared objects</td>
</tr>
<tr>
<td><a class="link" href="pg_shseclabel.md"><code class="structname">pg_shseclabel</code></a></td>
<td>security labels on shared database objects</td>
</tr>
<tr>
<td><a class="link" href="pg_statistic.md"><code class="structname">pg_statistic</code></a></td>
<td>planner statistics</td>
</tr>
<tr>
<td><a class="link" href="pg_statistic_ext.md"><code class="structname">pg_statistic_ext</code></a></td>
<td>extended planner statistics (definition)</td>
</tr>
<tr>
<td><a class="link" href="pg_statistic_ext_data.md"><code class="structname">pg_statistic_ext_data</code></a></td>
<td>extended planner statistics (built statistics)</td>
</tr>
<tr>
<td><a class="link" href="pg_subscription.md"><code class="structname">pg_subscription</code></a></td>
<td>logical replication subscriptions</td>
</tr>
<tr>
<td><a class="link" href="pg_subscription_rel.md"><code class="structname">pg_subscription_rel</code></a></td>
<td>relation state for subscriptions</td>
</tr>
<tr>
<td><a class="link" href="51.54.-pg_tablespace.md"><code class="structname">pg_tablespace</code></a></td>
<td>tablespaces within this database cluster</td>
</tr>
<tr>
<td><a class="link" href="pg_transform.md"><code class="structname">pg_transform</code></a></td>
<td>transforms (data type to procedural language conversions)</td>
</tr>
<tr>
<td><a class="link" href="51.56.-pg_trigger.md"><code class="structname">pg_trigger</code></a></td>
<td>triggers</td>
</tr>
<tr>
<td><a class="link" href="pg_ts_config.md"><code class="structname">pg_ts_config</code></a></td>
<td>text search configurations</td>
</tr>
<tr>
<td><a class="link" href="pg_ts_config_map.md"><code class="structname">pg_ts_config_map</code></a></td>
<td>text search configurations' token mappings</td>
</tr>
<tr>
<td><a class="link" href="pg_ts_dict.md"><code class="structname">pg_ts_dict</code></a></td>
<td>text search dictionaries</td>
</tr>
<tr>
<td><a class="link" href="pg_ts_parser.md"><code class="structname">pg_ts_parser</code></a></td>
<td>text search parsers</td>
</tr>
<tr>
<td><a class="link" href="pg_ts_template.md"><code class="structname">pg_ts_template</code></a></td>
<td>text search templates</td>
</tr>
<tr>
<td><a class="link" href="pg_type.md"><code class="structname">pg_type</code></a></td>
<td>data types</td>
</tr>
<tr>
<td><a class="link" href="pg_user_mapping.md"><code class="structname">pg_user_mapping</code></a></td>
<td>mappings of users to foreign servers</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](catalogs-overview.md)（英文原文，待翻譯）
