---
description: 版本：11
---

# 51.11 pg\_class

The catalog `pg_class` catalogs tables and most everything else that has columns or is otherwise similar to a table. This includes indexes \(but see also `pg_index`\), sequences \(but see also `pg_sequence`\), views, materialized views, composite types, and TOAST tables; see `relkind`. Below, when we mean all of these kinds of objects we speak of “relations”. Not all columns are meaningful for all relation types.

#### **Table 51.11. `pg_class` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>oid</code>  <code>oid</code>
        </p>
        <p>Row identifier</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of the table, index, view, etc.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relnamespace</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-namespace.html"><code>pg_namespace</code></a>.<code>oid</code>)</p>
        <p>The OID of the namespace that contains this relation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reltype</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-type.html"><code>pg_type</code></a>.<code>oid</code>)</p>
        <p>The OID of the data type that corresponds to this table&apos;s row type,
          if any (zero for indexes, which have no <code>pg_type</code> entry)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reloftype</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-type.html"><code>pg_type</code></a>.<code>oid</code>)</p>
        <p>For typed tables, the OID of the underlying composite type, zero for all
          other relations</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relowner</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>oid</code>)</p>
        <p>Owner of the relation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relam</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-am.html"><code>pg_am</code></a>.<code>oid</code>)</p>
        <p>If this is a table or an index, the access method used (heap, B-tree,
          hash, etc.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relfilenode</code>  <code>oid</code>
        </p>
        <p>Name of the on-disk file of this relation; zero means this is a &#x201C;mapped&#x201D;
          relation whose disk file name is determined by low-level state</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reltablespace</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-tablespace.html"><code>pg_tablespace</code></a>.<code>oid</code>)</p>
        <p>The tablespace in which this relation is stored. If zero, the database&apos;s
          default tablespace is implied. (Not meaningful if the relation has no on-disk
          file.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relpages</code>  <code>int4</code>
        </p>
        <p>Size of the on-disk representation of this table in pages (of size <code>BLCKSZ</code>).
          This is only an estimate used by the planner. It is updated by <code>VACUUM</code>, <code>ANALYZE</code>,
          and a few DDL commands such as <code>CREATE INDEX</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reltuples</code>  <code>float4</code>
        </p>
        <p>Number of live rows in the table. This is only an estimate used by the
          planner. It is updated by <code>VACUUM</code>, <code>ANALYZE</code>, and
          a few DDL commands such as <code>CREATE INDEX</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relallvisible</code>  <code>int4</code>
        </p>
        <p>Number of pages that are marked all-visible in the table&apos;s visibility
          map. This is only an estimate used by the planner. It is updated by <code>VACUUM</code>, <code>ANALYZE</code>,
          and a few DDL commands such as <code>CREATE INDEX</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reltoastrelid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>OID of the TOAST table associated with this table, 0 if none. The TOAST
          table stores large attributes &#x201C;out of line&#x201D; in a secondary
          table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relhasindex</code>  <code>bool</code>
        </p>
        <p>True if this is a table and it has (or recently had) any indexes</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relisshared</code>  <code>bool</code>
        </p>
        <p>True if this table is shared across all databases in the cluster. Only
          certain system catalogs (such as <code>pg_database</code>) are shared.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relpersistence</code>  <code>char</code>
        </p>
        <p><code>p</code> = permanent table, <code>u</code> = unlogged table, <code>t</code> =
          temporary table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relkind</code>  <code>char</code>
        </p>
        <p><code>r</code> = ordinary table, <code>i</code> = index, <code>S</code> = sequence, <code>t</code> =
          TOAST table, <code>v</code> = view, <code>m</code> = materialized view, <code>c</code> =
          composite type, <code>f</code> = foreign table, <code>p</code> = partitioned
          table, <code>I</code> = partitioned index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relnatts</code>  <code>int2</code>
        </p>
        <p>Number of user columns in the relation (system columns not counted). There
          must be this many corresponding entries in <code>pg_attribute</code>. See
          also <code>pg_attribute.attnum</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relchecks</code>  <code>int2</code>
        </p>
        <p>Number of <code>CHECK</code> constraints on the table; see <a href="https://www.postgresql.org/docs/13/catalog-pg-constraint.html"><code>pg_constraint</code></a> catalog</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relhasrules</code>  <code>bool</code>
        </p>
        <p>True if table has (or once had) rules; see <a href="https://www.postgresql.org/docs/13/catalog-pg-rewrite.html"><code>pg_rewrite</code></a> catalog</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relhastriggers</code>  <code>bool</code>
        </p>
        <p>True if table has (or once had) triggers; see <a href="https://www.postgresql.org/docs/13/catalog-pg-trigger.html"><code>pg_trigger</code></a> catalog</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relhassubclass</code>  <code>bool</code>
        </p>
        <p>True if table or index has (or once had) any inheritance children</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relrowsecurity</code>  <code>bool</code>
        </p>
        <p>True if table has row level security enabled; see <a href="https://www.postgresql.org/docs/13/catalog-pg-policy.html"><code>pg_policy</code></a> catalog</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relforcerowsecurity</code>  <code>bool</code>
        </p>
        <p>True if row level security (when enabled) will also apply to table owner;
          see <a href="https://www.postgresql.org/docs/13/catalog-pg-policy.html"><code>pg_policy</code></a> catalog</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relispopulated</code>  <code>bool</code>
        </p>
        <p>True if relation is populated (this is true for all relations other than
          some materialized views)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relreplident</code>  <code>char</code>
        </p>
        <p>Columns used to form &#x201C;replica identity&#x201D; for rows: <code>d</code> =
          default (primary key, if any), <code>n</code> = nothing, <code>f</code> = all
          columns, <code>i</code> = index with <code>indisreplident</code> set (same
          as nothing if the index used has been dropped)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relispartition</code>  <code>bool</code>
        </p>
        <p>True if table or index is a partition</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relrewrite</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>For new relations being written during a DDL operation that requires a
          table rewrite, this contains the OID of the original relation; otherwise
          0. That state is only visible internally; this field should never contain
          anything other than 0 for a user-visible relation.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relfrozenxid</code>  <code>xid</code>
        </p>
        <p>All transaction IDs before this one have been replaced with a permanent
          (&#x201C;frozen&#x201D;) transaction ID in this table. This is used to
          track whether the table needs to be vacuumed in order to prevent transaction
          ID wraparound or to allow <code>pg_xact</code> to be shrunk. Zero (<code>InvalidTransactionId</code>)
          if the relation is not a table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relminmxid</code>  <code>xid</code>
        </p>
        <p>All multixact IDs before this one have been replaced by a transaction
          ID in this table. This is used to track whether the table needs to be vacuumed
          in order to prevent multixact ID wraparound or to allow <code>pg_multixact</code> to
          be shrunk. Zero (<code>InvalidMultiXactId</code>) if the relation is not
          a table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relacl</code>  <code>aclitem[]</code>
        </p>
        <p>Access privileges; see <a href="https://www.postgresql.org/docs/13/ddl-priv.html">Section 5.7</a> for
          details</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reloptions</code>  <code>text[]</code>
        </p>
        <p>Access-method-specific options, as &#x201C;keyword=value&#x201D; strings</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relpartbound</code>  <code>pg_node_tree</code>
        </p>
        <p>If table is a partition (see <code>relispartition</code>), internal representation
          of the partition bound</p>
      </td>
    </tr>
  </tbody>
</table>

Several of the Boolean flags in `pg_class` are maintained lazily: they are guaranteed to be true if that's the correct state, but may not be reset to false immediately when the condition is no longer true. For example, `relhasindex` is set by `CREATE INDEX`, but it is never cleared by `DROP INDEX`. Instead, `VACUUM` clears `relhasindex` if it finds the table has no indexes. This arrangement avoids race conditions and improves concurrency.  


