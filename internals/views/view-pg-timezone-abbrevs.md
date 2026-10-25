<a id="VIEW-PG-TIMEZONE-ABBREVS"></a>

## 53.33. `pg_timezone_abbrevs` [#](#view-pg-timezone-abbrevs) <a href="#view-pg-timezone-abbrevs" id="view-pg-timezone-abbrevs"></a>

<a id="id-1.10.5.37.2"></a>

檢視表 `pg_timezone_abbrevs` 提供日期時間輸入常式目前所辨識的時區縮寫清單。當 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 或 [timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) 執行期參數被修改時，此檢視表的內容就會改變。

<a id="id-1.10.5.37.4"></a>

**表 53.33. `pg_timezone_abbrevs` 欄位**

<table border="1" class="table" summary="表 53.33. pg_timezone_abbrevs 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
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
       若這是日光節約時間的縮寫則為 true
      </p></td></tr></tbody></table>

<br>

雖然大多數時區縮寫代表與 UTC 的固定偏移量，但有些縮寫的值在歷史上曾經改變過（更多資訊請參閱[第 B.4 節](../../appendixes/datetime-appendix/datetime-config-files.md)）。在這種情況下，此檢視表會呈現它們目前的意義。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-timezone-abbrevs.html)（原文版本：18.6；核對日期：2026-10-09）
