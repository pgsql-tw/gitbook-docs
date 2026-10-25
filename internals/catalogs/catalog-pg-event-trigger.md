<a id="CATALOG-PG-EVENT-TRIGGER"></a>

## 52.21. `pg_event_trigger` [#](#catalog-pg-event-trigger) <a href="#catalog-pg-event-trigger" id="catalog-pg-event-trigger"></a>

<a id="id-1.10.4.23.2"></a>

系統目錄 `pg_event_trigger` 存放事件觸發程序。更多資訊請參閱[第 38 章](../../server-programming/event-triggers/README.md)。

<a id="id-1.10.4.23.4"></a>

**表 52.21. `pg_event_trigger` 欄位**

<table border="1" class="table" summary="表 52.21. pg_event_trigger 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtname</code> <code class="type">name</code>
</p>
<p>
       觸發程序名稱（必須唯一）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtevent</code> <code class="type">name</code>
</p>
<p>
       識別此觸發程序會在哪個事件發生時觸發
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       事件觸發程序的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtfoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       要呼叫的函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evtenabled</code> <code class="type">char</code>
</p>
<p>
       控制事件觸發程序在哪些 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> 模式下觸發。
       <code class="literal">O</code> = 觸發程序在<span class="quote">“<span class="quote">origin</span>”</span>與<span class="quote">“<span class="quote">local</span>”</span>模式下觸發，
       <code class="literal">D</code> = 觸發程序已停用，
       <code class="literal">R</code> = 觸發程序在<span class="quote">“<span class="quote">replica</span>”</span>模式下觸發，
       <code class="literal">A</code> = 觸發程序一律觸發。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">evttags</code> <code class="type">text[]</code>
</p>
<p>
       會使此觸發程序觸發的命令標籤。若為 NULL，則此觸發程序的觸發不會依命令標籤加以限制。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-event-trigger.html)（原文版本：18.6；核對日期：2026-10-17）
