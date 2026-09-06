## 53.33. `pg_timezone_abbrevs` [#](#VIEW-PG-TIMEZONE-ABBREVS)

<a id="id-1.10.5.37.2"></a>

The view `pg_timezone_abbrevs` provides a list
of time zone abbreviations that are currently recognized by the datetime
input routines. The contents of this view change when the
[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) or
[timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) run-time parameters are
modified.

<a id="id-1.10.5.37.4"></a>

**Table 53.33. `pg_timezone_abbrevs` Columns**

<table border="1" class="table" summary="pg_timezone_abbrevs Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">abbrev</code> <code class="type">text</code>
</p>
<p>
       Time zone abbreviation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">utc_offset</code> <code class="type">interval</code>
</p>
<p>
       Offset from UTC (positive means east of Greenwich)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_dst</code> <code class="type">bool</code>
</p>
<p>
       True if this is a daylight-savings abbreviation
      </p></td></tr></tbody></table>

<br>

While most timezone abbreviations represent fixed offsets from UTC,
there are some that have historically varied in value
(see [Section B.4](../../appendixes/datetime-appendix/datetime-config-files.md) for more information).
In such cases this view presents their current meaning.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-timezone-abbrevs.html)（英文原文，待翻譯）
