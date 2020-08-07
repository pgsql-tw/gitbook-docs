# 8.5. 日期時間型別

PostgreSQL 支援完整的 SQL 日期和時間格式，如表 8.9 所示。對於這些資料型態能使用的操作，將會在[9.9節](../functions-and-operators/9.9-ri-qi-shi-jian-han-shi-ji-yun-suan-zi.md)說明。

**Table 8.9. 日期/時間型態**

| Name | Storage Size | Description | Low Value | High Value | Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `timestamp [ (p`\) \] \[ without time zone \] | 8 bytes | both date and time \(no time zone\) | 4713 BC | 294276 AD | 1 microsecond |
| `timestamp [ (p`\) \] with time zone | 8 bytes | both date and time, with time zone | 4713 BC | 294276 AD | 1 microsecond |
| `date` | 4 bytes | date \(no time of day\) | 4713 BC | 5874897 AD | 1 day |
| `time [ (p`\) \] \[ without time zone \] | 8 bytes | time of day \(no date\) | 00:00:00 | 24:00:00 | 1 microsecond |
| `time [ (p`\) \] with time zone | 12 bytes | time of day \(no date\), with time zone | 00:00:00+1459 | 24:00:00-1459 | 1 microsecond |
| `interval [` `fields` \] \[ \(`p`\) \] | 16 bytes | time interval | -178000000 years | 178000000 years | 1 microsecond |

## 注意

SQL 標準中要求 `timestamp` 的效果等同於 `timestamp without time zone`，對此 PostgreSQL 尊重這個行為。同時 PostgreSQL 額外擴充了 `timestamptz` 作為 `timestamp with time zone` 的縮寫。

`time`、`timestamp` 和 `interval` 接受 `p` 作為非必須的精度參數，可指定秒的欄位保留的小數位數。預設情況下，精度沒有明確的界限。其中 `p` 允許的範圍是 0 到 6。

`interval` 型態有個額外的選項，可以寫下下列其中一個詞組來限制存放的欄位：

```text
YEAR
MONTH
DAY
HOUR
MINUTE
SECOND
YEAR TO MONTH
DAY TO HOUR
DAY TO MINUTE
DAY TO SECOND
HOUR TO MINUTE
HOUR TO SECOND
MINUTE TO SECOND
```

需注意若是 `fields` 和 `p` 同時指定時，`fields` 必須要包含 `SECOND`。這是因為精度只會套用在秒上。

`time with time zone` 型態是由 SQL 標準所定義的，但是在定義中展示的屬性會導致對有用性產生疑問。在多數狀況下，`date`、`time`、`timestamp without time zone` 和 `timestamp with time zone` 的組合應該就能提供任何應用程式需要的完整日期/時間功能。

`abstime` 和 `reltime` 型態是較低精度的內部用型態，並不建議將這些型態用在應用程式中；這些內部型態也可能在未來的釋出中消失。

## 8.5.1. 日期/時間輸入

日期和時間的輸入格式可以接受幾乎任何合理的格式，包括 ISO 8601、相容於 SQL 的格式、傳統 POSTGRES 格式或者其他格式。在部份格式中，日期的年、月、日的順序可能很含糊，因此有支援指定這些欄位期望的順序。可以設定 [DateStyle](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DATESTYLE) 參數為 `MDY` 來以 月-日-年 表示、設定為 `DMY` 以 日-月-年 表示、或者設定為 `YMD` 以 年-月-日 表示。

PostgreSQL 在處理日期/時間的輸入是比 SQL 標準要求的更加靈活，關於精確的解析規則以及包含月份、一週天數、時區等可以接受的文字欄位，可以參閱[附錄 B](https://www.postgresql.org/docs/10/static/datetime-appendix.html)。

請記得，任何日期和時間字面的輸入，都需要像文字一樣以單引號結束，詳細的資訊請參閱[4.1.2.7 節](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#SQL-SYNTAX-CONSTANTS-GENERIC)。SQL 要求使用以下的語法：

```text
type [ (p) ] 'value'
```

其中 `p` 是非必須的精度設定，用來指定秒欄位的小數位數。精度可以用來指定 `time`、`timestamp` 和 `interval` 型態，可指定範圍為 0 到 6。如果沒有指定精度時，預設將以字面數值的精度為準（但最多不超過 6 位）。

### **8.5.1.1. 日期**

[表 8.10](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-DATETIME-DATE-TABLE) 列出 `date` 型態的一些可能的輸入格式：

**表 8.10. 日期輸入**

| Example | Description |
| :--- | :--- |
| 1999-01-08 | ISO 8601; January 8 in any mode \(recommended format\) |
| January 8, 1999 | unambiguous in any `datestyle` input mode |
| 1/8/1999 | January 8 in `MDY` mode; August 1 in `DMY` mode |
| 1/18/1999 | January 18 in `MDY` mode; rejected in other modes |
| 01/02/03 | January 2, 2003 in `MDY` mode; February 1, 2003 in `DMY` mode; February 3, 2001 in `YMD` mode |
| 1999-Jan-08 | January 8 in any mode |
| Jan-08-1999 | January 8 in any mode |
| 08-Jan-1999 | January 8 in any mode |
| 99-Jan-08 | January 8 in `YMD` mode, else error |
| 08-Jan-99 | January 8, except error in `YMD` mode |
| Jan-08-99 | January 8, except error in `YMD` mode |
| 19990108 | ISO 8601; January 8, 1999 in any mode |
| 990108 | ISO 8601; January 8, 1999 in any mode |
| 1999.008 | year and day of year |
| J2451187 | Julian date |
| January 8, 99 BC | year 99 BC |

### **8.5.1.2. 時間**

time-of-day 格式包含 `time [ (p`\) \] without time zone`和`time \[ \(`_`p`_\) \] with time zone`，其中 `time` 單獨出現時等同於 `time without time zone`。

這些型態的合法輸入包含了一天當中的時間，以及非必須的時區。（請參照[表 8.11](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-DATETIME-TIME-TABLE) 和[表 8.12](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-TIMEZONE-TABLE)）。如果在 `time without time zone` 的輸入中指定了時區，則時區會被無聲地忽略。你也可以指定日期，但日期也會被忽略，除非你指定的時區名稱是像 `America/New_York` 這種具有日光節約規則的時區，因為在這種狀況下，為了能夠決定要套用一般規則或是日光節約規則，必須要有日期。適合的時差資訊會被紀錄在 `time with time zone` 的值當中。

**表 8.11. 時間輸入**

| Example | Description |
| :--- | :--- |
| `04:05:06.789` | ISO 8601 |
| `04:05:06` | ISO 8601 |
| `04:05` | ISO 8601 |
| `040506` | ISO 8601 |
| `04:05 AM` | same as 04:05; AM does not affect value |
| `04:05 PM` | same as 16:05; input hour must be &lt;= 12 |
| `04:05:06.789-8` | ISO 8601 |
| `04:05:06-08:00` | ISO 8601 |
| `04:05-08:00` | ISO 8601 |
| `040506-08` | ISO 8601 |
| `04:05:06 PST` | time zone specified by abbreviation |
| `2003-04-12 04:05:06 America/New_York` | time zone specified by full name |

**表 8.12. 時區輸入**

| Example | Description |
| :--- | :--- |
| `PST` | Abbreviation \(for Pacific Standard Time\) |
| `America/New_York` | Full time zone name |
| `PST8PDT` | POSIX-style time zone specification |
| `-8:00` | ISO-8601 offset for PST |
| `-800` | ISO-8601 offset for PST |
| `-8` | ISO-8601 offset for PST |
| `zulu` | Military abbreviation for UTC |
| `z` | Short form of `zulu` |

關於指定時區的其他資訊，請參照[8.5.3節](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-TIMEZONES)。

### **8.5.1.3. 時間戳記**

時間戳記型態的合法輸入，依序包含了日期、時間、非必須的時區、以及非必須的 `AD` 或者 `BC`。 （其中，`AD` 或者 `BC` 也可以寫在時區前面，但這並非推薦的格式。）因此：

```text
1999-01-08 04:05:06
```

以及：

```text
1999-01-08 04:05:06 -8:00
```

都是遵循 ISO 8601 標準的合法值。除此之外，常見的格式：

```text
January 8 04:05:06 1999 PST
```

也有支援。

SQL 標準中，`timestamp without time zone` 和 `timestamp with time zone` 字面可以在時間後面加上 “+” 或 “-” 符號和時差來做區別，因此根據這個標準，

```text
TIMESTAMP '2004-10-19 10:23:54'
```

是 `timestamp without time zone` 型態，而

```text
TIMESTAMP '2004-10-19 10:23:54+02'
```

則是 `timestamp with time zone` 型態。PostgreSQL 從不會在識別型態前就解析字面的內容，因此會將上述兩種值都視為 `timestamp without time zone` 型態。如要確保字面會被視為 `timestamp with time zone`，請給它正確而明確的型態：

```text
TIMESTAMP WITH TIME ZONE '2004-10-19 10:23:54+02'
```

在一個已被確定為沒有時區的時間戳記的字串中，PostgreSQL 將默默地忽略任何時區指示。也就是說，結果值是從輸入值中的日期/時間字串產生的，而不針對時區進行調整。

對於帶有時區的時間戳記，內部儲存的值始終為 UTC（Universal Coordinated Time，傳統上稱為格林威治標準時間，GMT）。具有指定時區的輸入值將使用該時區的相對偏移量轉換為 UTC。如果輸入字串中未指定時區，則假定它位於系統的 [TimeZone](../../server-administration/server-configuration/client-connection-defaults.md#timezone-string) 參數所指示的時區中，並使用時區的偏移量轉換為 UTC。

輸出帶有時區值的時間戳記時，始終由 UTC 轉換為目前時區，並在該時區中顯示為本地時間。要查看另一個時區的時間，請變更時區或使用 AT TIME ZONE 語法（參閱[第 9.9.3 節](../functions-and-operators/9.9-ri-qi-shi-jian-han-shi-ji-yun-suan-zi.md#9-9-3-at-time-zone)）。

沒有時區的時間戳記和帶時區的時間戳記之間的轉換通常假定應該採用沒有時區值的時間戳記或本地時間所給予的時區。可以使用 AT TIME ZONE 為指定轉換不同的時區。

### **8.5.1.4. 特殊值**

為方便起見，PostgreSQL 支援幾個特殊的日期/時間輸入值，如 Table 8.13 所示。infinaity 和 -infinity 值在系統內部有特別的表示，但不會顯示；而其他的只是符號縮寫，在閱讀時會轉換為普通的日期/時間值。（特別是，now 和相關的字串一旦被讀取就會被轉換為特定的時間值。）當在 SQL 命令中要作為常數使用時，所有這些值都需要用單引號括起來。

**Table 8.13. Special Date/Time Inputs**

| Input String | Valid Types | Description |
| :--- | :--- | :--- |
| `epoch` | `date`, `timestamp` | 1970-01-01 00:00:00+00 \(Unix system time zero\) |
| `infinity` | `date`, `timestamp` | later than all other time stamps |
| `-infinity` | `date`, `timestamp` | earlier than all other time stamps |
| `now` | `date`, `time`, `timestamp` | current transaction's start time |
| `today` | `date`, `timestamp` | midnight today |
| `tomorrow` | `date`, `timestamp` | midnight tomorrow |
| `yesterday` | `date`, `timestamp` | midnight yesterday |
| `allballs` | `time` | 00:00:00.00 UTC |

以下 SQL 相容函數也可用於取得相對應資料型別目前的時間值：CURRENT\_DATE，CURRENT\_TIME，CURRENT\_TIMESTAMP，LOCALTIME，LOCALTIMESTAMP。後四者接受選擇性的 subsecond 級精確度。 （請參閱[第 9.9.4 節](../functions-and-operators/9.9-ri-qi-shi-jian-han-shi-ji-yun-suan-zi.md#9-9-4-current-date-time)。）請注意，這些是 SQL 函數，在資料輸入字串中會無法識別。

## 8.5.2. Date/Time Output

The output format of the date/time types can be set to one of the four styles ISO 8601, SQL \(Ingres\), traditional POSTGRES \(Unix date format\), or German. The default is the ISO format. \(The SQL standard requires the use of the ISO 8601 format. The name of the “SQL” output format is a historical accident.\) [Table 8.14](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-DATETIME-OUTPUT-TABLE) shows examples of each output style. The output of the `date` and `time` types is generally only the date or time part in accordance with the given examples. However, the POSTGRES style outputs date-only values in ISO format.

**Table 8.14. Date/Time Output Styles**

| Style Specification | Description | Example |
| :--- | :--- | :--- |
| `ISO` | ISO 8601, SQL standard | `1997-12-17 07:37:16-08` |
| `SQL` | traditional style | `12/17/1997 07:37:16.00 PST` |
| `Postgres` | original style | `Wed Dec 17 07:37:16 1997 PST` |
| `German` | regional style | `17.12.1997 07:37:16.00 PST` |

## Note

ISO 8601 specifies the use of uppercase letter `T` to separate the date and time. PostgreSQLaccepts that format on input, but on output it uses a space rather than `T`, as shown above. This is for readability and for consistency with RFC 3339 as well as some other database systems.

In the SQL and POSTGRES styles, day appears before month if DMY field ordering has been specified, otherwise month appears before day. \(See [Section 8.5.1](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-DATETIME-INPUT) for how this setting also affects interpretation of input values.\) [Table 8.15](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-DATETIME-OUTPUT2-TABLE) shows examples.

**Table 8.15. Date Order Conventions**

| `datestyle` Setting | Input Ordering | Example Output |
| :--- | :--- | :--- |
| `SQL, DMY` | `day`/`month`/`year` | `17/12/1997 15:37:16.00 CET` |
| `SQL, MDY` | `month`/`day`/`year` | `12/17/1997 07:37:16.00 PST` |
| `Postgres, DMY` | `day`/`month`/`year` | `Wed 17 Dec 07:37:16 1997 PST` |

The date/time style can be selected by the user using the `SET datestyle` command, the [DateStyle](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DATESTYLE) parameter in the `postgresql.conf` configuration file, or the `PGDATESTYLE` environment variable on the server or client.

The formatting function `to_char` \(see [Section 9.8](https://www.postgresql.org/docs/10/static/functions-formatting.html)\) is also available as a more flexible way to format date/time output.

## 8.5.3. Time Zones

Time zones, and time-zone conventions, are influenced by political decisions, not just earth geometry. Time zones around the world became somewhat standardized during the 1900s, but continue to be prone to arbitrary changes, particularly with respect to daylight-savings rules. PostgreSQL uses the widely-used IANA \(Olson\) time zone database for information about historical time zone rules. For times in the future, the assumption is that the latest known rules for a given time zone will continue to be observed indefinitely far into the future.

PostgreSQL endeavors to be compatible with the SQL standard definitions for typical usage. However, the SQL standard has an odd mix of date and time types and capabilities. Two obvious problems are:

* Although the `date` type cannot have an associated time zone, the `time` type can. Time zones in the real world have little meaning unless associated with a date as well as a time, since the offset can vary through the year with daylight-saving time boundaries.
* The default time zone is specified as a constant numeric offset from UTC. It is therefore impossible to adapt to daylight-saving time when doing date/time arithmetic across DST boundaries.

To address these difficulties, we recommend using date/time types that contain both date and time when using time zones. We do _not_ recommend using the type `time with time zone` \(though it is supported by PostgreSQL for legacy applications and for compliance with the SQL standard\). PostgreSQL assumes your local time zone for any type containing only date or time.

All timezone-aware dates and times are stored internally in UTC. They are converted to local time in the zone specified by the [TimeZone](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TIMEZONE) configuration parameter before being displayed to the client.

PostgreSQL allows you to specify time zones in three different forms:

* A full time zone name, for example `America/New_York`. The recognized time zone names are listed in the `pg_timezone_names` view \(see [Section 51.90](https://www.postgresql.org/docs/10/static/view-pg-timezone-names.html)\). PostgreSQL uses the widely-used IANA time zone data for this purpose, so the same time zone names are also recognized by much other software.
* A time zone abbreviation, for example `PST`. Such a specification merely defines a particular offset from UTC, in contrast to full time zone names which can imply a set of daylight savings transition-date rules as well. The recognized abbreviations are listed in the `pg_timezone_abbrevs` view \(see [Section 51.89](https://www.postgresql.org/docs/10/static/view-pg-timezone-abbrevs.html)\). You cannot set the configuration parameters [TimeZone](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TIMEZONE) or [log\_timezone](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-TIMEZONE) to a time zone abbreviation, but you can use abbreviations in date/time input values and with the `AT TIME ZONE` operator.
* In addition to the timezone names and abbreviations, PostgreSQL will accept POSIX-style time zone specifications of the form `STDoffset` or `STDoffsetDST`, where `STD` is a zone abbreviation, `offset` is a numeric offset in hours west from UTC, and `DST` is an optional daylight-savings zone abbreviation, assumed to stand for one hour ahead of the given offset. For example, if `EST5EDT` were not already a recognized zone name, it would be accepted and would be functionally equivalent to United States East Coast time. In this syntax, a zone abbreviation can be a string of letters, or an arbitrary string surrounded by angle brackets \(`<>`\). When a daylight-savings zone abbreviation is present, it is assumed to be used according to the same daylight-savings transition rules used in the IANA time zone database's `posixrules` entry. In a standard PostgreSQL installation, `posixrules` is the same as `US/Eastern`, so that POSIX-style time zone specifications follow USA daylight-savings rules. If needed, you can adjust this behavior by replacing the `posixrules` file.

In short, this is the difference between abbreviations and full names: abbreviations represent a specific offset from UTC, whereas many of the full names imply a local daylight-savings time rule, and so have two possible UTC offsets. As an example, `2014-06-04 12:00 America/New_York` represents noon local time in New York, which for this particular date was Eastern Daylight Time \(UTC-4\). So `2014-06-04 12:00 EDT` specifies that same time instant. But `2014-06-04 12:00 EST` specifies noon Eastern Standard Time \(UTC-5\), regardless of whether daylight savings was nominally in effect on that date.

To complicate matters, some jurisdictions have used the same timezone abbreviation to mean different UTC offsets at different times; for example, in Moscow `MSK` has meant UTC+3 in some years and UTC+4 in others. PostgreSQLinterprets such abbreviations according to whatever they meant \(or had most recently meant\) on the specified date; but, as with the `EST` example above, this is not necessarily the same as local civil time on that date.

One should be wary that the POSIX-style time zone feature can lead to silently accepting bogus input, since there is no check on the reasonableness of the zone abbreviations. For example, `SET TIMEZONE TO FOOBAR0` will work, leaving the system effectively using a rather peculiar abbreviation for UTC. Another issue to keep in mind is that in POSIX time zone names, positive offsets are used for locations _west_ of Greenwich. Everywhere else, PostgreSQLfollows the ISO-8601 convention that positive timezone offsets are _east_ of Greenwich.

In all cases, timezone names and abbreviations are recognized case-insensitively. \(This is a change from PostgreSQL versions prior to 8.2, which were case-sensitive in some contexts but not others.\)

Neither timezone names nor abbreviations are hard-wired into the server; they are obtained from configuration files stored under `.../share/timezone/` and `.../share/timezonesets/` of the installation directory \(see [Section B.3](https://www.postgresql.org/docs/10/static/datetime-config-files.html)\).

The [TimeZone](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TIMEZONE) configuration parameter can be set in the file `postgresql.conf`, or in any of the other standard ways described in [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html). There are also some special ways to set it:

* The SQL command `SET TIME ZONE` sets the time zone for the session. This is an alternative spelling of `SET TIMEZONE TO` with a more SQL-spec-compatible syntax.
* The `PGTZ` environment variable is used by libpq clients to send a `SET TIME ZONE` command to the server upon connection.

## 8.5.4. Interval Input

`interval` values can be written using the following verbose syntax:

```text
[@] quantity unit [quantity unit...] [direction]
```

where `quantity` is a number \(possibly signed\); `unit` is `microsecond`, `millisecond`, `second`, `minute`, `hour`, `day`, `week`, `month`, `year`, `decade`, `century`, `millennium`, or abbreviations or plurals of these units; `direction` can be `ago` or empty. The at sign \(`@`\) is optional noise. The amounts of the different units are implicitly added with appropriate sign accounting. `ago` negates all the fields. This syntax is also used for interval output, if [IntervalStyle](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-INTERVALSTYLE) is set to `postgres_verbose`.

Quantities of days, hours, minutes, and seconds can be specified without explicit unit markings. For example, `'1 12:59:10'` is read the same as `'1 day 12 hours 59 min 10 sec'`. Also, a combination of years and months can be specified with a dash; for example `'200-10'` is read the same as `'200 years 10 months'`. \(These shorter forms are in fact the only ones allowed by the SQL standard, and are used for output when `IntervalStyle` is set to `sql_standard`.\)

Interval values can also be written as ISO 8601 time intervals, using either the “format with designators” of the standard's section 4.4.3.2 or the “alternative format” of section 4.4.3.3. The format with designators looks like this:

```text
P quantity unit [ quantity unit ...] [ T [ quantity unit ...]]
```

The string must start with a `P`, and may include a `T` that introduces the time-of-day units. The available unit abbreviations are given in [Table 8.16](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-INTERVAL-ISO8601-UNITS). Units may be omitted, and may be specified in any order, but units smaller than a day must appear after `T`. In particular, the meaning of `M` depends on whether it is before or after `T`.

**Table 8.16. ISO 8601 Interval Unit Abbreviations**

| Abbreviation | Meaning |
| :--- | :--- |
| Y | Years |
| M | Months \(in the date part\) |
| W | Weeks |
| D | Days |
| H | Hours |
| M | Minutes \(in the time part\) |
| S | Seconds |

In the alternative format:

```text
P [ years-months-days ] [ T hours:minutes:seconds ]
```

the string must begin with `P`, and a `T` separates the date and time parts of the interval. The values are given as numbers similar to ISO 8601 dates.

When writing an interval constant with a `fields` specification, or when assigning a string to an interval column that was defined with a `fields` specification, the interpretation of unmarked quantities depends on the `fields`. For example `INTERVAL '1' YEAR` is read as 1 year, whereas `INTERVAL '1'` means 1 second. Also, field values “to the right” of the least significant field allowed by the `fields` specification are silently discarded. For example, writing `INTERVAL '1 day 2:03:04' HOUR TO MINUTE` results in dropping the seconds field, but not the day field.

According to the SQL standard all fields of an interval value must have the same sign, so a leading negative sign applies to all fields; for example the negative sign in the interval literal `'-1 2:03:04'` applies to both the days and hour/minute/second parts. PostgreSQL allows the fields to have different signs, and traditionally treats each field in the textual representation as independently signed, so that the hour/minute/second part is considered positive in this example. If `IntervalStyle` is set to `sql_standard` then a leading sign is considered to apply to all fields \(but only if no additional signs appear\). Otherwise the traditional PostgreSQL interpretation is used. To avoid ambiguity, it's recommended to attach an explicit sign to each field if any field is negative.

Internally `interval` values are stored as months, days, and seconds. This is done because the number of days in a month varies, and a day can have 23 or 25 hours if a daylight savings time adjustment is involved. The months and days fields are integers while the seconds field can store fractions. Because intervals are usually created from constant strings or `timestamp` subtraction, this storage method works well in most cases. Functions `justify_days` and `justify_hours` are available for adjusting days and hours that overflow their normal ranges.

In the verbose input format, and in some fields of the more compact input formats, field values can have fractional parts; for example `'1.5 week'` or `'01:02:03.45'`. Such input is converted to the appropriate number of months, days, and seconds for storage. When this would result in a fractional number of months or days, the fraction is added to the lower-order fields using the conversion factors 1 month = 30 days and 1 day = 24 hours. For example,`'1.5 month'` becomes 1 month and 15 days. Only seconds will ever be shown as fractional on output.

[Table 8.17](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-INTERVAL-INPUT-EXAMPLES) shows some examples of valid `interval` input.

**Table 8.17. Interval Input**

| Example | Description |
| :--- | :--- |
| 1-2 | SQL standard format: 1 year 2 months |
| 3 4:05:06 | SQL standard format: 3 days 4 hours 5 minutes 6 seconds |
| 1 year 2 months 3 days 4 hours 5 minutes 6 seconds | Traditional Postgres format: 1 year 2 months 3 days 4 hours 5 minutes 6 seconds |
| P1Y2M3DT4H5M6S | ISO 8601 “format with designators”: same meaning as above |
| P0001-02-03T04:05:06 | ISO 8601 “alternative format”: same meaning as above |

## 8.5.5. Interval Output

The output format of the interval type can be set to one of the four styles `sql_standard`, `postgres`, `postgres_verbose`, or `iso_8601`, using the command `SET intervalstyle`. The default is the `postgres` format. [Table 8.18](https://www.postgresql.org/docs/10/static/datatype-datetime.html#INTERVAL-STYLE-OUTPUT-TABLE) shows examples of each output style.

The `sql_standard` style produces output that conforms to the SQL standard's specification for interval literal strings, if the interval value meets the standard's restrictions \(either year-month only or day-time only, with no mixing of positive and negative components\). Otherwise the output looks like a standard year-month literal string followed by a day-time literal string, with explicit signs added to disambiguate mixed-sign intervals.

The output of the `postgres` style matches the output of PostgreSQL releases prior to 8.4 when the [DateStyle](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DATESTYLE) parameter was set to `ISO`.

The output of the `postgres_verbose` style matches the output of PostgreSQL releases prior to 8.4 when the `DateStyle` parameter was set to non-`ISO` output.

The output of the `iso_8601` style matches the “format with designators” described in section 4.4.3.2 of the ISO 8601 standard.

**Table 8.18. Interval Output Style Examples**

| Style Specification | Year-Month Interval | Day-Time Interval | Mixed Interval |
| :--- | :--- | :--- | :--- |
| `sql_standard` | 1-2 | 3 4:05:06 | -1-2 +3 -4:05:06 |
| `postgres` | 1 year 2 mons | 3 days 04:05:06 | -1 year -2 mons +3 days -04:05:06 |
| `postgres_verbose` | @ 1 year 2 mons | @ 3 days 4 hours 5 mins 6 secs | @ 1 year 2 mons -3 days 4 hours 5 mins 6 secs ago |
| `iso_8601` | P1Y2M | P3DT4H5M6S | P-1Y-2M3DT-4H-5M-6S |

