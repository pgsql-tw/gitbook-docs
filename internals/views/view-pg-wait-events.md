## 53.38. `pg_wait_events` [#](#VIEW-PG-WAIT-EVENTS)

<a id="id-1.10.5.42.2"></a>

The view `pg_wait_events` provides description about the
wait events.

<a id="id-1.10.5.42.4"></a>

**Table 53.38. `pg_wait_events` Columns**

<table border="1" class="table" summary="pg_wait_events Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       Wait event type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       Wait event name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">description</code> <code class="type">text</code>
</p>
<p>
       Wait event description
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-wait-events.html)（英文原文，待翻譯）
