# F.32.2. pg_stat_statements_info 檢視表

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO"></a>

## F.32.2. `pg_stat_statements_info` 檢視表 [#](#pgstatstatements-pg-stat-statements-info) <a href="#pgstatstatements-pg-stat-statements-info" id="pgstatstatements-pg-stat-statements-info"></a>

<a id="id-1.11.7.42.7.2"></a>

`pg_stat_statements` 模組本身的統計資訊也會被追蹤，並透過名為 `pg_stat_statements_info` 的檢視表提供。此檢視表只包含單一資料列。此檢視表的欄位列於[表 F.23](#pgstatstatementsinfo-columns)。

<a id="PGSTATSTATEMENTSINFO-COLUMNS"></a>

### 表 F.23. `pg_stat_statements_info` 欄位 [#](#pgstatstatementsinfo-columns) <a href="#pgstatstatementsinfo-columns" id="pgstatstatementsinfo-columns"></a>

<table border="1" class="table" summary="表 F.23. pg_stat_statements_info 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dealloc</code> <code class="type">bigint</code>
</p>
<p>
       <code class="structname">pg_stat_statements</code> 中有關執行次數最少之陳述式的項目，因觀察到的不同陳述式超過 <code class="varname">pg_stat_statements.max</code> 個而被釋放的總次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       <code class="structname">pg_stat_statements</code> 檢視表中所有統計資訊最後一次重設的時間。
      </p></td></tr></tbody></table>

<br>

[返回 F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊](../pgstatstatements.md#pgstatstatements)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)（原文版本：18.6；核對日期：2026-10-23）
