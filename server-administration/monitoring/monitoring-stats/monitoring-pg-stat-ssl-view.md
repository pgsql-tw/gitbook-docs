# 27.2.10. pg_stat_ssl

<a id="MONITORING-PG-STAT-SSL-VIEW"></a>

## 27.2.10. `pg_stat_ssl` [#](#monitoring-pg-stat-ssl-view) <a href="#monitoring-pg-stat-ssl-view" id="monitoring-pg-stat-ssl-view"></a>

<a id="id-1.6.14.7.14.2"></a>

`pg_stat_ssl` 檢視表中，每個
後端或 WAL 傳送程序都會有一筆資料列，顯示有關該連線 SSL
使用情形的統計資訊。可以在 `pid` 欄位上
與 `pg_stat_activity` 或 `pg_stat_replication`
進行連接（join），以取得有關該
連線的更多詳情。

<a id="PG-STAT-SSL-VIEW"></a>

### 表 27.20. `pg_stat_ssl` 檢視表 [#](#pg-stat-ssl-view) <a href="#pg-stat-ssl-view" id="pg-stat-ssl-view"></a>

<table border="1" class="table" summary="pg_stat_ssl 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       某個後端或 WAL 傳送程序的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ssl</code> <code class="type">boolean</code>
</p>
<p>
       若此連線使用 SSL，則為 True
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">version</code> <code class="type">text</code>
</p>
<p>
       所使用的 SSL 版本；若此連線未使用 SSL，
       則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cipher</code> <code class="type">text</code>
</p>
<p>
       所使用之 SSL 加密演算法（cipher）的名稱；若此連線
       未使用 SSL，則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bits</code> <code class="type">integer</code>
</p>
<p>
       所使用加密演算法的位元數；若此連線未使用 SSL，
       則為 NULL
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_dn</code> <code class="type">text</code>
</p>
<p>
       所使用用戶端憑證中的辨別名稱（Distinguished Name, DN）欄位；
       若未提供用戶端憑證，或此連線未使用 SSL，則為 NULL。若 DN
       欄位長度超過 <code class="symbol">NAMEDATALEN</code>（在標準組建中為 64 個字元），
       此欄位將會被截斷。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_serial</code> <code class="type">numeric</code>
</p>
<p>
       用戶端憑證的序號；若未提供用戶端
       憑證，或此連線未使用 SSL，則為 NULL。憑證序號與憑證
       發行者的組合可唯一識別一張憑證（除非發行者錯誤地重複使用序
       號）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">issuer_dn</code> <code class="type">text</code>
</p>
<p>
       用戶端憑證發行者的 DN；若未提供用戶端
       憑證，或此連線未使用 SSL，則為 NULL。
       此欄位的截斷方式與 <code class="structfield">client_dn</code> 相同。
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
