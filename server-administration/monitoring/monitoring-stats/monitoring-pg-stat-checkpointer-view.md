# 27.2.15. pg_stat_checkpointer

<a id="MONITORING-PG-STAT-CHECKPOINTER-VIEW"></a>

## 27.2.15. `pg_stat_checkpointer` [#](#monitoring-pg-stat-checkpointer-view) <a href="#monitoring-pg-stat-checkpointer-view" id="monitoring-pg-stat-checkpointer-view"></a>

<a id="id-1.6.14.7.19.2"></a>

`pg_stat_checkpointer` 檢視表始終只會有
一筆資料列，包含有關該叢集檢查點程序的資料。

<a id="PG-STAT-CHECKPOINTER-VIEW"></a>

### 表 27.25. `pg_stat_checkpointer` 檢視表 [#](#pg-stat-checkpointer-view) <a href="#pg-stat-checkpointer-view" id="pg-stat-checkpointer-view"></a>

<table border="1" class="table" summary="pg_stat_checkpointer 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_timed</code> <code class="type">bigint</code>
</p>
<p>
       因逾時而排定的檢查點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_requested</code> <code class="type">bigint</code>
</p>
<p>
       已要求的檢查點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_done</code> <code class="type">bigint</code>
</p>
<p>
       已執行完成的檢查點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_timed</code> <code class="type">bigint</code>
</p>
<p>
       因逾時或先前執行嘗試失敗，而排定的重新啟動點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_req</code> <code class="type">bigint</code>
</p>
<p>
       已要求的重新啟動點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_done</code> <code class="type">bigint</code>
</p>
<p>
       已執行完成的重新啟動點次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_time</code> <code class="type">double precision</code>
</p>
<p>
       在處理檢查點與重新啟動點過程中，用於將檔案寫入磁碟
       這一部分所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_time</code> <code class="type">double precision</code>
</p>
<p>
       在處理檢查點與重新啟動點過程中，用於將檔案同步至
       磁碟這一部分所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_written</code> <code class="type">bigint</code>
</p>
<p>
       在檢查點與重新啟動點期間所寫入的共享緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slru_written</code> <code class="type">bigint</code>
</p>
<p>
        在檢查點與重新啟動點期間所寫入的 SLRU 緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       這些統計資訊上次重設的時間
      </p></td></tr></tbody></table>

<br>

若伺服器自上一次檢查點以來一直處於閒置狀態，則檢查點可能會被跳過。
`num_timed` 與
`num_requested` 會同時計算已完成與已跳過的
檢查點，而 `num_done` 則僅追蹤
已完成的檢查點。同樣地，若最後重播的檢查點記錄已經是最後一個
重新啟動點，則重新啟動點可能會被跳過。
`restartpoints_timed` 與
`restartpoints_req` 會同時計算已完成與
已跳過的重新啟動點，而 `restartpoints_done`
則僅追蹤已完成的重新啟動點。

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
