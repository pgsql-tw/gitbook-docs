## 52.58. `pg_trigger` [#](#CATALOG-PG-TRIGGER)

<a id="id-1.10.4.60.2"></a>

The catalog `pg_trigger` stores triggers on tables
and views.
See [CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md)
for more information.

<a id="id-1.10.4.60.4"></a>

**Table 52.58. `pg_trigger` Columns**

<table border="1" class="table" summary="pg_trigger Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">tgrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table this trigger is on
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgparentid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-trigger.md"><code class="structname">pg_trigger</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Parent trigger that this trigger is cloned from (this happens when
       partitions are created or attached to a partitioned table);
       zero if not a clone
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgname</code> <code class="type">name</code>
</p>
<p>
       Trigger name (must be unique among triggers of same table)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgfoid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The function to be called
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgtype</code> <code class="type">int2</code>
</p>
<p>
       Bit mask identifying trigger firing conditions
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgenabled</code> <code class="type">char</code>
</p>
<p>
       Controls in which <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> modes
       the trigger fires.
       <code class="literal">O</code> = trigger fires in <span class="quote">“<span class="quote">origin</span>”</span> and <span class="quote">“<span class="quote">local</span>”</span> modes,
       <code class="literal">D</code> = trigger is disabled,
       <code class="literal">R</code> = trigger fires in <span class="quote">“<span class="quote">replica</span>”</span> mode,
       <code class="literal">A</code> = trigger fires always.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgisinternal</code> <code class="type">bool</code>
</p>
<p>
       True if trigger is internally generated (usually, to enforce
       the constraint identified by <code class="structfield">tgconstraint</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstrrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table referenced by a referential integrity constraint
       (zero if trigger is not for a referential integrity constraint)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstrindid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The index supporting a unique, primary key, referential integrity,
       or exclusion constraint
       (zero if trigger is not for one of these types of constraint)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstraint</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a> entry associated with the trigger
       (zero if trigger is not for a constraint)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgdeferrable</code> <code class="type">bool</code>
</p>
<p>
       True if constraint trigger is deferrable
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tginitdeferred</code> <code class="type">bool</code>
</p>
<p>
       True if constraint trigger is initially deferred
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgnargs</code> <code class="type">int2</code>
</p>
<p>
       Number of argument strings passed to trigger function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgattr</code> <code class="type">int2vector</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       Column numbers, if trigger is column-specific; otherwise an
       empty array
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgargs</code> <code class="type">bytea</code>
</p>
<p>
       Argument strings to pass to trigger, each NULL-terminated
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgqual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression tree (in <code class="function">nodeToString()</code>
       representation) for the trigger's <code class="literal">WHEN</code> condition, or null
       if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgoldtable</code> <code class="type">name</code>
</p>
<p>
<code class="literal">REFERENCING</code> clause name for <code class="literal">OLD TABLE</code>,
       or null if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgnewtable</code> <code class="type">name</code>
</p>
<p>
<code class="literal">REFERENCING</code> clause name for <code class="literal">NEW TABLE</code>,
       or null if none
      </p></td></tr></tbody></table>

<br>

Currently, column-specific triggering is supported only for
`UPDATE` events, and so `tgattr` is relevant
only for that event type. `tgtype` might
contain bits for other event types as well, but those are presumed
to be table-wide regardless of what is in `tgattr`.

### Note

When `tgconstraint` is nonzero,
`tgconstrrelid`, `tgconstrindid`,
`tgdeferrable`, and `tginitdeferred` are
largely redundant with the referenced [`pg_constraint`](catalog-pg-constraint.md) entry.
However, it is possible for a non-deferrable trigger to be associated
with a deferrable constraint: foreign key constraints can have some
deferrable and some non-deferrable triggers.

### Note

`pg_class.relhastriggers`
must be true if a relation has any triggers in this catalog.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-trigger.html)（英文原文，待翻譯）
