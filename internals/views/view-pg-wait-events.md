## 53.38. `pg_wait_events` [#](#VIEW-PG-WAIT-EVENTS)

<a id="id-1.10.5.42.2"></a>

檢視表 `pg_wait_events` 提供等待事件的說明。

<a id="id-1.10.5.42.4"></a>

**表 53.38. `pg_wait_events` 欄位**

<table border="1" class="table" summary="pg_wait_events Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       等待事件類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       等待事件名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">description</code> <code class="type">text</code>
</p>
<p>
       等待事件說明
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-wait-events.html)（原文版本：18.6；核對日期：2026-09-10）
