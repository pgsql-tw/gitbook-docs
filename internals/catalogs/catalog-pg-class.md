## 52.11. `pg_class` [#](#CATALOG-PG-CLASS)

<a id="id-1.10.4.13.2"></a>

The catalog `pg_class` describes tables and
other objects that have columns or are otherwise similar to a
table. This includes indexes (but see also [`pg_index`](catalog-pg-index.md)),
sequences (but see also [`pg_sequence`](catalog-pg-sequence.md)),
views, materialized views, composite types, and TOAST tables;
see `relkind`.
Below, when we mean all of these kinds of objects we speak of
“relations”. Not all of `pg_class`'s
columns are meaningful for all relation kinds.

<a id="id-1.10.4.13.4"></a>

**Table 52.11. `pg_class` Columns**

<table border="1" class="table" summary="pg_class Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of the table, index, view, etc.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this relation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the data type that corresponds to this table's row type,
       if any; zero for indexes, sequences, and toast tables, which have
       no <code class="structname">pg_type</code> entry
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reloftype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       For typed tables, the OID of the underlying composite type;
       zero for all other relations
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the relation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relam</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The access method used to access this table or index.
       Not meaningful if the relation is a sequence or
       has no on-disk file,
       except for partitioned tables, where, if set, it takes
       precedence over <code class="varname">default_table_access_method</code>
       when determining the access method to use for partitions created
       when one is not specified in the creation command.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfilenode</code> <code class="type">oid</code>
</p>
<p>
       Name of the on-disk file of this relation; zero means this
       is a <span class="quote">“<span class="quote">mapped</span>”</span> relation whose disk file name is determined
       by low-level state
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltablespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The tablespace in which this relation is stored.
       If zero, the database's default tablespace is implied.
       Not meaningful if the relation has no on-disk file,
       except for partitioned tables, where this is the tablespace
       in which partitions will be created when one is not
       specified in the creation command.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpages</code> <code class="type">int4</code>
</p>
<p>
       Size of the on-disk representation of this table in pages (of size
       <code class="symbol">BLCKSZ</code>).  This is only an estimate used by the
       planner.  It is updated by <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>,
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>, and a few DDL commands such as
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltuples</code> <code class="type">float4</code>
</p>
<p>
       Number of live rows in the table.  This is only an estimate used by
       the planner.  It is updated by <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>,
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>, and a few DDL commands such as
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>.
       If the table has never yet been vacuumed or
       analyzed, <code class="structfield">reltuples</code>
       contains <code class="literal">-1</code> indicating that the row count is
       unknown.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relallvisible</code> <code class="type">int4</code>
</p>
<p>
       Number of pages that are marked all-visible in the table's
       visibility map.  This is only an estimate used by the
       planner.  It is updated by <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>,
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>, and a few DDL commands such as
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relallfrozen</code> <code class="type">int4</code>
</p>
<p>
       Number of pages that are marked all-frozen in the table's visibility
       map.  This is only an estimate used for triggering autovacuums. It can
       also be used along with <code class="structfield">relallvisible</code> for
       scheduling manual vacuums and tuning <a class="link" href="../../server-administration/runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING">vacuum's freezing
       behavior</a>.

       It is updated by
       <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>,
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>,
       and a few DDL commands such as
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltoastrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the TOAST table associated with this table, zero if none.  The
       TOAST table stores large attributes <span class="quote">“<span class="quote">out of line</span>”</span> in a
       secondary table.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhasindex</code> <code class="type">bool</code>
</p>
<p>
       True if this is a table and it has (or recently had) any indexes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relisshared</code> <code class="type">bool</code>
</p>
<p>
       True if this table is shared across all databases in the cluster.  Only
       certain system catalogs (such as <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>)
       are shared.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpersistence</code> <code class="type">char</code>
</p>
<p>
<code class="literal">p</code> = permanent table/sequence, <code class="literal">u</code> = unlogged table/sequence,
       <code class="literal">t</code> = temporary table/sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relkind</code> <code class="type">char</code>
</p>
<p>
<code class="literal">r</code> = ordinary table,
       <code class="literal">i</code> = index,
       <code class="literal">S</code> = sequence,
       <code class="literal">t</code> = TOAST table,
       <code class="literal">v</code> = view,
       <code class="literal">m</code> = materialized view,
       <code class="literal">c</code> = composite type,
       <code class="literal">f</code> = foreign table,
       <code class="literal">p</code> = partitioned table,
       <code class="literal">I</code> = partitioned index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relnatts</code> <code class="type">int2</code>
</p>
<p>
       Number of user columns in the relation (system columns not
       counted).  There must be this many corresponding entries in
       <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.  See also
       <code class="structname">pg_attribute</code>.<code class="structfield">attnum</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relchecks</code> <code class="type">int2</code>
</p>
<p>
       Number of <code class="literal">CHECK</code> constraints on the table; see
       <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a> catalog
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhasrules</code> <code class="type">bool</code>
</p>
<p>
       True if table has (or once had) rules; see
       <a class="link" href="catalog-pg-rewrite.md"><code class="structname">pg_rewrite</code></a> catalog
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhastriggers</code> <code class="type">bool</code>
</p>
<p>
       True if table has (or once had) triggers; see
       <a class="link" href="catalog-pg-trigger.md"><code class="structname">pg_trigger</code></a> catalog
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhassubclass</code> <code class="type">bool</code>
</p>
<p>
       True if table or index has (or once had) any inheritance children or partitions
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relrowsecurity</code> <code class="type">bool</code>
</p>
<p>
       True if table has row-level security enabled; see
       <a class="link" href="catalog-pg-policy.md"><code class="structname">pg_policy</code></a> catalog
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relforcerowsecurity</code> <code class="type">bool</code>
</p>
<p>
       True if row-level security (when enabled) will also apply to table owner; see
       <a class="link" href="catalog-pg-policy.md"><code class="structname">pg_policy</code></a> catalog
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relispopulated</code> <code class="type">bool</code>
</p>
<p>
       True if relation is populated (this is true for all
       relations other than some materialized views)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relreplident</code> <code class="type">char</code>
</p>
<p>
       Columns used to form <span class="quote">“<span class="quote">replica identity</span>”</span> for rows:
       <code class="literal">d</code> = default (primary key, if any),
       <code class="literal">n</code> = nothing,
       <code class="literal">f</code> = all columns,
       <code class="literal">i</code> = index with
       <code class="structfield">indisreplident</code> set (same as nothing if the
       index used has been dropped)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relispartition</code> <code class="type">bool</code>
</p>
<p>
       True if table or index is a partition
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relrewrite</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       For new relations being written during a DDL operation that requires a
       table rewrite, this contains the OID of the original relation;
       otherwise zero.  That state is only visible internally; this field should
       never contain anything other than zero for a user-visible relation.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfrozenxid</code> <code class="type">xid</code>
</p>
<p>
       All transaction IDs before this one have been replaced with a permanent
       (<span class="quote">“<span class="quote">frozen</span>”</span>) transaction ID in this table.  This is used to track
       whether the table needs to be vacuumed in order to prevent transaction
       ID wraparound or to allow <code class="literal">pg_xact</code> to be shrunk.  Zero
       (<code class="symbol">InvalidTransactionId</code>) if the relation is not a table.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relminmxid</code> <code class="type">xid</code>
</p>
<p>
       All multixact IDs before this one have been replaced by a
       transaction ID in this table.  This is used to track
       whether the table needs to be vacuumed in order to prevent multixact ID
       wraparound or to allow <code class="literal">pg_multixact</code> to be shrunk.  Zero
       (<code class="symbol">InvalidMultiXactId</code>) if the relation is not a table.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Access privileges; see <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reloptions</code> <code class="type">text[]</code>
</p>
<p>
       Access-method-specific options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpartbound</code> <code class="type">pg_node_tree</code>
</p>
<p>
       If table is a partition (see <code class="structfield">relispartition</code>),
       internal representation of the partition bound
      </p></td></tr></tbody></table>

<br>

Several of the Boolean flags in `pg_class` are maintained
lazily: they are guaranteed to be true if that's the correct state, but
may not be reset to false immediately when the condition is no longer
true. For example, `relhasindex` is set by
[`CREATE INDEX`](../../reference/sql-commands/sql-createindex.md), but it is never cleared by
[`DROP INDEX`](../../reference/sql-commands/sql-dropindex.md). Instead, [`VACUUM`](../../reference/sql-commands/sql-vacuum.md) clears
`relhasindex` if it finds the table has no indexes. This
arrangement avoids race conditions and improves concurrency.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-class.html)（英文原文，待翻譯）
