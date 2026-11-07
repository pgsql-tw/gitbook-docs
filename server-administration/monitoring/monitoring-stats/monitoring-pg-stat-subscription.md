# 27.2.8. pg_stat_subscription

<a id="MONITORING-PG-STAT-SUBSCRIPTION"></a>

## 27.2.8. `pg_stat_subscription` [#](#monitoring-pg-stat-subscription) <a href="#monitoring-pg-stat-subscription" id="monitoring-pg-stat-subscription"></a>

<a id="id-1.6.14.7.12.2"></a><a id="PG-STAT-SUBSCRIPTION"></a>

### 表 27.18. `pg_stat_subscription` 檢視表 [#](#pg-stat-subscription) <a href="#pg-stat-subscription" id="pg-stat-subscription"></a>

<table border="1" class="table" summary="pg_stat_subscription 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subid</code> <code class="type">oid</code>
</p>
<p>
       此訂閱的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       此訂閱的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">worker_type</code> <code class="type">text</code>
</p>
<p>
       訂閱工作程序的類型。可能的類型有
       <code class="literal">apply</code>、<code class="literal">parallel apply</code> 以及
       <code class="literal">table synchronization</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       訂閱工作程序的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">leader_pid</code> <code class="type">integer</code>
</p>
<p>
       若此程序為平行套用工作程序，則為領導套用工作程序的程序 ID；
       若此程序為領導套用工作程序或資料表同步
       工作程序，則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       此工作程序正在同步之關聯的 OID；對於領導套用工作程序以及
       平行套用工作程序，則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">received_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       最後接收到的預寫式日誌位置，此欄位的
       初始值為 0；對於平行套用工作程序則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_send_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       從來源 WAL 傳送程序收到最後一則訊息的傳送時間；對於
       平行套用工作程序則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_receipt_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       從來源 WAL 傳送程序收到最後一則訊息的接收時間；對於
       平行套用工作程序則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       回報給來源 WAL 傳送程序的最後一個預寫式日誌位置；對於
       平行套用工作程序則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       回報給來源 WAL 傳送程序最後一個預寫式日誌位置的
       時間；對於平行套用工作程序則為 NULL
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
