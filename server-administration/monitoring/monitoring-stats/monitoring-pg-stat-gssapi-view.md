# 27.2.11. pg_stat_gssapi

<a id="MONITORING-PG-STAT-GSSAPI-VIEW"></a>

## 27.2.11. `pg_stat_gssapi` [#](#monitoring-pg-stat-gssapi-view) <a href="#monitoring-pg-stat-gssapi-view" id="monitoring-pg-stat-gssapi-view"></a>

<a id="id-1.6.14.7.15.2"></a>

`pg_stat_gssapi` 檢視表中，每個
後端都會有一筆資料列，顯示有關該連線 GSSAPI 使用情形的資訊。可以在
`pid` 欄位上與 `pg_stat_activity` 或
`pg_stat_replication`
進行連接（join），以取得有關該
連線的更多詳情。

<a id="PG-STAT-GSSAPI-VIEW"></a>

### 表 27.21. `pg_stat_gssapi` 檢視表 [#](#pg-stat-gssapi-view) <a href="#pg-stat-gssapi-view" id="pg-stat-gssapi-view"></a>

<table border="1" class="table" summary="pg_stat_gssapi 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       某個後端的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">gss_authenticated</code> <code class="type">boolean</code>
</p>
<p>
       若此連線使用 GSSAPI 驗證，則為 True
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">principal</code> <code class="type">text</code>
</p>
<p>
       用於驗證此連線的主體（principal）；若此連線
       未使用 GSSAPI 進行驗證，則為 NULL。若主體
       長度超過 <code class="symbol">NAMEDATALEN</code>（在標準組建中為 64 個字元），
       此欄位將會被截斷。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">encrypted</code> <code class="type">boolean</code>
</p>
<p>
       若此連線使用 GSSAPI 加密，則為 True
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">credentials_delegated</code> <code class="type">boolean</code>
</p>
<p>
       若此連線的 GSSAPI 憑證已被委派，則為 True。
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
