# 27.2.6. pg_stat_wal_receiver

<a id="MONITORING-PG-STAT-WAL-RECEIVER-VIEW"></a>

## 27.2.6. `pg_stat_wal_receiver` [#](#monitoring-pg-stat-wal-receiver-view) <a href="#monitoring-pg-stat-wal-receiver-view" id="monitoring-pg-stat-wal-receiver-view"></a>

<a id="id-1.6.14.7.10.2"></a>

`pg_stat_wal_receiver` 檢視表僅會有
一筆資料列，顯示 WAL 接收程序從其所連線
伺服器接收 WAL 的相關統計資訊。

<a id="PG-STAT-WAL-RECEIVER-VIEW"></a>

### 表 27.16. `pg_stat_wal_receiver` 檢視表 [#](#pg-stat-wal-receiver-view) <a href="#pg-stat-wal-receiver-view" id="pg-stat-wal-receiver-view"></a>

<table border="1" class="table" summary="pg_stat_wal_receiver 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       WAL 接收程序的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">status</code> <code class="type">text</code>
</p>
<p>
       WAL 接收程序的活動狀態
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">receive_start_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       啟動 WAL 接收程序時所使用的第一個預寫式日誌
       位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">receive_start_tli</code> <code class="type">integer</code>
</p>
<p>
       啟動 WAL 接收程序時所使用的第一個時間軸編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">written_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       已接收並寫入磁碟，但尚未刷寫的最後一個預寫式日誌位置。
       此欄位不應用於資料完整性檢查。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flushed_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       已接收並刷寫至磁碟的最後一個預寫式日誌位置，此欄位的
       初始值為啟動 WAL 接收程序時所使用的第一個日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">received_tli</code> <code class="type">integer</code>
</p>
<p>
       已接收並刷寫至磁碟之最後一個預寫式日誌位置的時間軸
       編號，此欄位的初始值為啟動 WAL 接收程序時所使用第一個日誌位置的
       時間軸編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_send_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       從來源 WAL 傳送程序收到最後一則訊息的傳送時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_receipt_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       從來源 WAL 傳送程序收到最後一則訊息的接收時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       回報給來源 WAL 傳送程序的最後一個預寫式日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       回報給來源 WAL 傳送程序最後一個預寫式日誌位置的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">text</code>
</p>
<p>
       此 WAL 接收程序所使用的複寫插槽名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sender_host</code> <code class="type">text</code>
</p>
<p>
       此 WAL 接收程序所連線 <span class="productname">PostgreSQL</span> 執行個體的主機。
       這可以是主機名稱、IP 位址，或者若透過 Unix socket 連線，
       則為目錄路徑。（路徑的情況可以透過它必定是以
       <code class="literal">/</code> 開頭的絕對路徑來辨別。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sender_port</code> <code class="type">integer</code>
</p>
<p>
       此 WAL 接收程序所連線 <span class="productname">PostgreSQL</span> 執行個體的埠號。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conninfo</code> <code class="type">text</code>
</p>
<p>
       此 WAL 接收程序所使用的連線字串，
       其中具安全敏感性的欄位已被模糊化處理。
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
