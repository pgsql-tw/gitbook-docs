## 52.21. `pg_event_trigger` [#](#CATALOG-PG-EVENT-TRIGGER)

<a id="id-1.10.4.23.2"></a>

The catalog `pg_event_trigger` stores event triggers.
See [Chapter 38](../../server-programming/event-triggers/README.md) for more information.

<a id="id-1.10.4.23.4"></a>

**Table 52.21. `pg_event_trigger` Columns**

<table border="1" class="table" summary="pg_event_trigger Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">evtname</code> <code class="type">name</code>
</p>
<p>
       Trigger name (must be unique)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtevent</code> <code class="type">name</code>
</p>
<p>
       Identifies the event for which this trigger fires
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the event trigger
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtfoid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The function to be called
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtenabled</code> <code class="type">char</code>
</p>
<p>
       Controls in which <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> modes
       the event trigger fires.
       <code class="literal">O</code> = trigger fires in <span class="quote">“<span class="quote">origin</span>”</span> and <span class="quote">“<span class="quote">local</span>”</span> modes,
       <code class="literal">D</code> = trigger is disabled,
       <code class="literal">R</code> = trigger fires in <span class="quote">“<span class="quote">replica</span>”</span> mode,
       <code class="literal">A</code> = trigger fires always.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evttags</code> <code class="type">text[]</code>
</p>
<p>
       Command tags for which this trigger will fire.  If NULL, the firing
       of this trigger is not restricted on the basis of the command tag.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-event-trigger.html)（英文原文，待翻譯）
