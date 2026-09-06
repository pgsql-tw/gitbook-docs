## 53.34. `pg_timezone_names` [#](#VIEW-PG-TIMEZONE-NAMES)

<a id="id-1.10.5.38.2"></a>

檢視表 `pg_timezone_names` 提供 `SET TIMEZONE` 所辨識的時區名稱清單，以及相關縮寫、UTC 偏移量與日光節約時間狀態。（嚴格而言，PostgreSQL 不使用 UTC，因為它不處理閏秒。）與 [`pg_timezone_abbrevs`](view-pg-timezone-abbrevs.md) 顯示的縮寫不同，其中許多名稱隱含一組日光節約時間轉換日期規則。因此，相關資訊會隨當地 DST 邊界改變。顯示的資訊是根據 `CURRENT_TIMESTAMP` 的目前值計算。

<a id="id-1.10.5.38.4"></a>

**表 53.34. `pg_timezone_names` 欄位**

<table border="1" class="table" summary="pg_timezone_names Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       時區名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">abbrev</code> <code class="type">text</code>
</p>
<p>
       時區縮寫
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">utc_offset</code> <code class="type">interval</code>
</p>
<p>
       與 UTC 的偏移量（正值代表位於格林威治以東）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_dst</code> <code class="type">bool</code>
</p>
<p>
       目前採用日光節約時間時為 true
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-timezone-names.html)（原文版本：18.6；核對日期：2026-09-06）
