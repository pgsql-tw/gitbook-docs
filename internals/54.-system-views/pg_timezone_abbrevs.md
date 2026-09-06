# 54.31. pg\_timezone\_abbrevs

The view `pg_timezone_abbrevs` provides a list of time zone abbreviations that are currently recognized by the datetime input routines. The contents of this view change when the [timezone\_abbreviations](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-TIMEZONE-ABBREVIATIONS) run-time parameter is modified.

#### **Table 54.31. `pg_timezone_abbrevs` Columns**

| <p>Column Type</p><p>Description</p>                                                                          |
| ------------------------------------------------------------------------------------------------------------- |
| <p><code>abbrev</code> <code>text</code></p><p>Time zone abbreviation</p>                                     |
| <p><code>utc_offset</code> <code>interval</code></p><p>Offset from UTC (positive means east of Greenwich)</p> |
| <p><code>is_dst</code> <code>bool</code></p><p>True if this is a daylight-savings abbreviation</p>            |

While most timezone abbreviations represent fixed offsets from UTC, there are some that have historically varied in value (see [Section B.4](https://www.postgresql.org/docs/current/datetime-config-files.html) for more information). In such cases this view presents their current meaning.
