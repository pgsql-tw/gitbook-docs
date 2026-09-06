## 9.8. Data Type Formatting Functions [#](#FUNCTIONS-FORMATTING)

<a id="id-1.5.8.14.2"></a>

The PostgreSQL formatting functions
provide a powerful set of tools for converting various data types
(date/time, integer, floating point, numeric) to formatted strings
and for converting from formatted strings to specific data types.
[Table 9.26](functions-formatting.md#FUNCTIONS-FORMATTING-TABLE) lists them.
These functions all follow a common calling convention: the first
argument is the value to be formatted and the second argument is a
template that defines the output or input format.

<a id="FUNCTIONS-FORMATTING-TABLE"></a>

**Table 9.26. Formatting Functions**

<table border="1" class="table" summary="Formatting Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.14.4.2.2.1.1.1.1"></a>
<code class="function">to_char</code> ( <code class="type">timestamp</code>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_char</code> ( <code class="type">timestamp with time zone</code>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Converts time stamp to string according to the given format.
       </p>
<p>
<code class="literal">to_char(timestamp '2002-04-20 17:31:12.66', 'HH12:MI:SS')</code>
        → <code class="returnvalue">05:31:12</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">to_char</code> ( <code class="type">interval</code>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Converts interval to string according to the given format.
       </p>
<p>
<code class="literal">to_char(interval '15h 2m 12s', 'HH24:MI:SS')</code>
       → <code class="returnvalue">15:02:12</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">to_char</code> ( <em class="replaceable"><code>numeric_type</code></em>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Converts number to string according to the given format; available
        for <code class="type">integer</code>, <code class="type">bigint</code>, <code class="type">numeric</code>,
        <code class="type">real</code>, <code class="type">double precision</code>.
       </p>
<p>
<code class="literal">to_char(125, '999')</code>
        → <code class="returnvalue">125</code>
</p>
<p>
<code class="literal">to_char(125.8::real, '999D9')</code>
        → <code class="returnvalue">125.8</code>
</p>
<p>
<code class="literal">to_char(-125.8, '999D99S')</code>
        → <code class="returnvalue">125.80-</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.14.4.2.2.4.1.1.1"></a>
<code class="function">to_date</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">date</code>
</p>
<p>
        Converts string to date according to the given format.
       </p>
<p>
<code class="literal">to_date('05 Dec 2000', 'DD Mon YYYY')</code>
        → <code class="returnvalue">2000-12-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.14.4.2.2.5.1.1.1"></a>
<code class="function">to_number</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        Converts string to numeric according to the given format.
       </p>
<p>
<code class="literal">to_number('12,454.8-', '99G999D9S')</code>
        → <code class="returnvalue">-12454.8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.14.4.2.2.6.1.1.1"></a>
<code class="function">to_timestamp</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Converts string to time stamp according to the given format.
        (See also <code class="function">to_timestamp(double precision)</code> in
        <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TABLE">Table 9.33</a>.)
       </p>
<p>
<code class="literal">to_timestamp('05 Dec 2000', 'DD Mon YYYY')</code>
        → <code class="returnvalue">2000-12-05 00:00:00-05</code>
</p></td></tr></tbody></table>

<br>

### Tip

`to_timestamp` and `to_date`
exist to handle input formats that cannot be converted by
simple casting. For most standard date/time formats, simply casting the
source string to the required data type works, and is much easier.
Similarly, `to_number` is unnecessary for standard numeric
representations.

In a `to_char` output template string, there are certain
patterns that are recognized and replaced with appropriately-formatted
data based on the given value. Any text that is not a template pattern is
simply copied verbatim. Similarly, in an input template string (for the
other functions), template patterns identify the values to be supplied by
the input data string. If there are characters in the template string
that are not template patterns, the corresponding characters in the input
data string are simply skipped over (whether or not they are equal to the
template string characters).

[Table 9.27](functions-formatting.md#FUNCTIONS-FORMATTING-DATETIME-TABLE) shows the
template patterns available for formatting date and time values.

<a id="FUNCTIONS-FORMATTING-DATETIME-TABLE"></a>

**Table 9.27. Template Patterns for Date/Time Formatting**

<table border="1" class="table" summary="Template Patterns for Date/Time Formatting"><colgroup><col/><col/></colgroup><thead><tr><th>Pattern</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">HH</code></td><td>hour of day (01–12)</td></tr><tr><td><code class="literal">HH12</code></td><td>hour of day (01–12)</td></tr><tr><td><code class="literal">HH24</code></td><td>hour of day (00–23)</td></tr><tr><td><code class="literal">MI</code></td><td>minute (00–59)</td></tr><tr><td><code class="literal">SS</code></td><td>second (00–59)</td></tr><tr><td><code class="literal">MS</code></td><td>millisecond (000–999)</td></tr><tr><td><code class="literal">US</code></td><td>microsecond (000000–999999)</td></tr><tr><td><code class="literal">FF1</code></td><td>tenth of second (0–9)</td></tr><tr><td><code class="literal">FF2</code></td><td>hundredth of second (00–99)</td></tr><tr><td><code class="literal">FF3</code></td><td>millisecond (000–999)</td></tr><tr><td><code class="literal">FF4</code></td><td>tenth of a millisecond (0000–9999)</td></tr><tr><td><code class="literal">FF5</code></td><td>hundredth of a millisecond (00000–99999)</td></tr><tr><td><code class="literal">FF6</code></td><td>microsecond (000000–999999)</td></tr><tr><td><code class="literal">SSSS</code>, <code class="literal">SSSSS</code></td><td>seconds past midnight (0–86399)</td></tr><tr><td><code class="literal">AM</code>, <code class="literal">am</code>,
        <code class="literal">PM</code> or <code class="literal">pm</code></td><td>meridiem indicator (without periods)</td></tr><tr><td><code class="literal">A.M.</code>, <code class="literal">a.m.</code>,
        <code class="literal">P.M.</code> or <code class="literal">p.m.</code></td><td>meridiem indicator (with periods)</td></tr><tr><td><code class="literal">Y,YYY</code></td><td>year (4 or more digits) with comma</td></tr><tr><td><code class="literal">YYYY</code></td><td>year (4 or more digits)</td></tr><tr><td><code class="literal">YYY</code></td><td>last 3 digits of year</td></tr><tr><td><code class="literal">YY</code></td><td>last 2 digits of year</td></tr><tr><td><code class="literal">Y</code></td><td>last digit of year</td></tr><tr><td><code class="literal">IYYY</code></td><td>ISO 8601 week-numbering year (4 or more digits)</td></tr><tr><td><code class="literal">IYY</code></td><td>last 3 digits of ISO 8601 week-numbering year</td></tr><tr><td><code class="literal">IY</code></td><td>last 2 digits of ISO 8601 week-numbering year</td></tr><tr><td><code class="literal">I</code></td><td>last digit of ISO 8601 week-numbering year</td></tr><tr><td><code class="literal">BC</code>, <code class="literal">bc</code>,
        <code class="literal">AD</code> or <code class="literal">ad</code></td><td>era indicator (without periods)</td></tr><tr><td><code class="literal">B.C.</code>, <code class="literal">b.c.</code>,
        <code class="literal">A.D.</code> or <code class="literal">a.d.</code></td><td>era indicator (with periods)</td></tr><tr><td><code class="literal">MONTH</code></td><td>full upper case month name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">Month</code></td><td>full capitalized month name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">month</code></td><td>full lower case month name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">MON</code></td><td>abbreviated upper case month name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">Mon</code></td><td>abbreviated capitalized month name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">mon</code></td><td>abbreviated lower case month name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">MM</code></td><td>month number (01–12)</td></tr><tr><td><code class="literal">DAY</code></td><td>full upper case day name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">Day</code></td><td>full capitalized day name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">day</code></td><td>full lower case day name (blank-padded to 9 chars)</td></tr><tr><td><code class="literal">DY</code></td><td>abbreviated upper case day name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">Dy</code></td><td>abbreviated capitalized day name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">dy</code></td><td>abbreviated lower case day name (3 chars in English, localized lengths vary)</td></tr><tr><td><code class="literal">DDD</code></td><td>day of year (001–366)</td></tr><tr><td><code class="literal">IDDD</code></td><td>day of ISO 8601 week-numbering year (001–371; day 1 of the year is Monday of the first ISO week)</td></tr><tr><td><code class="literal">DD</code></td><td>day of month (01–31)</td></tr><tr><td><code class="literal">D</code></td><td>day of the week, Sunday (<code class="literal">1</code>) to Saturday (<code class="literal">7</code>)</td></tr><tr><td><code class="literal">ID</code></td><td>ISO 8601 day of the week, Monday (<code class="literal">1</code>) to Sunday (<code class="literal">7</code>)</td></tr><tr><td><code class="literal">W</code></td><td>week of month (1–5) (the first week starts on the first day of the month)</td></tr><tr><td><code class="literal">WW</code></td><td>week number of year (1–53) (the first week starts on the first day of the year)</td></tr><tr><td><code class="literal">IW</code></td><td>week number of ISO 8601 week-numbering year (01–53; the first Thursday of the year is in week 1)</td></tr><tr><td><code class="literal">CC</code></td><td>century (2 digits) (the twenty-first century starts on 2001-01-01)</td></tr><tr><td><code class="literal">J</code></td><td>Julian Date (integer days since November 24, 4714 BC at local
        midnight; see <a class="xref" href="../../appendixes/datetime-appendix/datetime-julian-dates.md">Section B.7</a>)</td></tr><tr><td><code class="literal">Q</code></td><td>quarter</td></tr><tr><td><code class="literal">RM</code></td><td>month in upper case Roman numerals (I–XII; I=January)</td></tr><tr><td><code class="literal">rm</code></td><td>month in lower case Roman numerals (i–xii; i=January)</td></tr><tr><td><code class="literal">TZ</code></td><td>upper case time-zone abbreviation</td></tr><tr><td><code class="literal">tz</code></td><td>lower case time-zone abbreviation</td></tr><tr><td><code class="literal">TZH</code></td><td>time-zone hours</td></tr><tr><td><code class="literal">TZM</code></td><td>time-zone minutes</td></tr><tr><td><code class="literal">OF</code></td><td>time-zone offset from UTC (<em class="replaceable"><code>HH</code></em>
         or <em class="replaceable"><code>HH</code></em><code class="literal">:</code><em class="replaceable"><code>MM</code></em>)</td></tr></tbody></table>

<br>

Modifiers can be applied to any template pattern to alter its
behavior. For example, `FMMonth`
is the `Month` pattern with the
`FM` modifier.
[Table 9.28](functions-formatting.md#FUNCTIONS-FORMATTING-DATETIMEMOD-TABLE) shows the
modifier patterns for date/time formatting.

<a id="FUNCTIONS-FORMATTING-DATETIMEMOD-TABLE"></a>

**Table 9.28. Template Pattern Modifiers for Date/Time Formatting**

<table border="1" class="table" summary="Template Pattern Modifiers for Date/Time Formatting"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Modifier</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code class="literal">FM</code> prefix</td><td>fill mode (suppress leading zeroes and padding blanks)</td><td><code class="literal">FMMonth</code></td></tr><tr><td><code class="literal">TH</code> suffix</td><td>upper case ordinal number suffix</td><td><code class="literal">DDTH</code>, e.g., <code class="literal">12TH</code></td></tr><tr><td><code class="literal">th</code> suffix</td><td>lower case ordinal number suffix</td><td><code class="literal">DDth</code>, e.g., <code class="literal">12th</code></td></tr><tr><td><code class="literal">FX</code> prefix</td><td>fixed format global option (see usage notes)</td><td><code class="literal">FX Month DD Day</code></td></tr><tr><td><code class="literal">TM</code> prefix</td><td>translation mode (use localized day and month names based on
         <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-TIME">lc_time</a>)</td><td><code class="literal">TMMonth</code></td></tr><tr><td><code class="literal">SP</code> suffix</td><td>spell mode (not implemented)</td><td><code class="literal">DDSP</code></td></tr></tbody></table>

<br>

Usage notes for date/time formatting:

* `FM` suppresses leading zeroes and trailing blanks
  that would otherwise be added to make the output of a pattern be
  fixed-width. In PostgreSQL,
  `FM` modifies only the next specification, while in
  Oracle `FM` affects all subsequent
  specifications, and repeated `FM` modifiers
  toggle fill mode on and off.
* `TM` suppresses trailing blanks whether or
  not `FM` is specified.
* `to_timestamp` and `to_date`
  ignore letter case in the input; so for
  example `MON`, `Mon`,
  and `mon` all accept the same strings. When using
  the `TM` modifier, case-folding is done according to
  the rules of the function's input collation (see
  [Section 23.2](../../server-administration/charset/collation.md)).
* `to_timestamp` and `to_date`
  skip multiple blank spaces at the beginning of the input string and
  around date and time values unless the `FX` option is used. For example,
  `to_timestamp(' 2000    JUN', 'YYYY MON')` and
  `to_timestamp('2000 - JUN', 'YYYY-MON')` work, but
  `to_timestamp('2000    JUN', 'FXYYYY MON')` returns an error
  because `to_timestamp` expects only a single space.
  `FX` must be specified as the first item in
  the template.
* A separator (a space or non-letter/non-digit character) in the template string of
  `to_timestamp` and `to_date`
  matches any single separator in the input string or is skipped,
  unless the `FX` option is used.
  For example, `to_timestamp('2000JUN', 'YYYY///MON')` and
  `to_timestamp('2000/JUN', 'YYYY MON')` work, but
  `to_timestamp('2000//JUN', 'YYYY/MON')`
  returns an error because the number of separators in the input string
  exceeds the number of separators in the template.

  If `FX` is specified, a separator in the template string
  matches exactly one character in the input string. But note that the
  input string character is not required to be the same as the separator from the template string.
  For example, `to_timestamp('2000/JUN', 'FXYYYY MON')`
  works, but `to_timestamp('2000/JUN', 'FXYYYY  MON')`
  returns an error because the second space in the template string consumes
  the letter `J` from the input string.
* A `TZH` template pattern can match a signed number.
  Without the `FX` option, minus signs may be ambiguous,
  and could be interpreted as a separator.
  This ambiguity is resolved as follows: If the number of separators before
  `TZH` in the template string is less than the number of
  separators before the minus sign in the input string, the minus sign
  is interpreted as part of `TZH`.
  Otherwise, the minus sign is considered to be a separator between values.
  For example, `to_timestamp('2000 -10', 'YYYY TZH')` matches
  `-10` to `TZH`, but
  `to_timestamp('2000 -10', 'YYYY  TZH')`
  matches `10` to `TZH`.
* Ordinary text is allowed in `to_char`
  templates and will be output literally. You can put a substring
  in double quotes to force it to be interpreted as literal text
  even if it contains template patterns. For example, in
  `'"Hello Year "YYYY'`, the `YYYY`
  will be replaced by the year data, but the single `Y` in `Year`
  will not be.
  In `to_date`, `to_number`,
  and `to_timestamp`, literal text and double-quoted
  strings result in skipping the number of characters contained in the
  string; for example `"XX"` skips two input characters
  (whether or not they are `XX`).

  ### Tip

  Prior to PostgreSQL 12, it was possible to
  skip arbitrary text in the input string using non-letter or non-digit
  characters. For example,
  `to_timestamp('2000y6m1d', 'yyyy-MM-DD')` used to
  work. Now you can only use letter characters for this purpose. For example,
  `to_timestamp('2000y6m1d', 'yyyytMMtDDt')` and
  `to_timestamp('2000y6m1d', 'yyyy"y"MM"m"DD"d"')`
  skip `y`, `m`, and
  `d`.
* If you want to have a double quote in the output you must
  precede it with a backslash, for example `'\"YYYY
  Month\"'`.
  Backslashes are not otherwise special outside of double-quoted
  strings. Within a double-quoted string, a backslash causes the
  next character to be taken literally, whatever it is (but this
  has no special effect unless the next character is a double quote
  or another backslash).
* In `to_timestamp` and `to_date`,
  if the year format specification is less than four digits, e.g.,
  `YYY`, and the supplied year is less than four digits,
  the year will be adjusted to be nearest to the year 2020, e.g.,
  `95` becomes 1995.
* In `to_timestamp` and `to_date`,
  negative years are treated as signifying BC. If you write both a
  negative year and an explicit `BC` field, you get AD
  again. An input of year zero is treated as 1 BC.
* In `to_timestamp` and `to_date`,
  the `YYYY` conversion has a restriction when
  processing years with more than 4 digits. You must
  use some non-digit character or template after `YYYY`,
  otherwise the year is always interpreted as 4 digits. For example
  (with the year 20000):
  `to_date('200001130', 'YYYYMMDD')` will be
  interpreted as a 4-digit year; instead use a non-digit
  separator after the year, like
  `to_date('20000-1130', 'YYYY-MMDD')` or
  `to_date('20000Nov30', 'YYYYMonDD')`.
* In `to_timestamp` and `to_date`,
  the `CC` (century) field is accepted but ignored
  if there is a `YYY`, `YYYY` or
  `Y,YYY` field. If `CC` is used with
  `YY` or `Y` then the result is
  computed as that year in the specified century. If the century is
  specified but the year is not, the first year of the century
  is assumed.
* In `to_timestamp` and `to_date`,
  weekday names or numbers (`DAY`, `D`,
  and related field types) are accepted but are ignored for purposes of
  computing the result. The same is true for quarter
  (`Q`) fields.
* In `to_timestamp` and `to_date`,
  an ISO 8601 week-numbering date (as distinct from a Gregorian date)
  can be specified in one of two ways:

  * Year, week number, and weekday: for
    example `to_date('2006-42-4', 'IYYY-IW-ID')`
    returns the date `2006-10-19`.
    If you omit the weekday it is assumed to be 1 (Monday).
  * Year and day of year: for example `to_date('2006-291',
    'IYYY-IDDD')` also returns `2006-10-19`.

  Attempting to enter a date using a mixture of ISO 8601 week-numbering
  fields and Gregorian date fields is nonsensical, and will cause an
  error. In the context of an ISO 8601 week-numbering year, the
  concept of a “month” or “day of month” has no
  meaning. In the context of a Gregorian year, the ISO week has no
  meaning.

  ### Caution

  While `to_date` will reject a mixture of
  Gregorian and ISO week-numbering date
  fields, `to_char` will not, since output format
  specifications like `YYYY-MM-DD (IYYY-IDDD)` can be
  useful. But avoid writing something like `IYYY-MM-DD`;
  that would yield surprising results near the start of the year.
  (See [Section 9.9.1](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT) for more
  information.)
* In `to_timestamp`, millisecond
  (`MS`) or microsecond (`US`)
  fields are used as the
  seconds digits after the decimal point. For example
  `to_timestamp('12.3', 'SS.MS')` is not 3 milliseconds,
  but 300, because the conversion treats it as 12 + 0.3 seconds.
  So, for the format `SS.MS`, the input values
  `12.3`, `12.30`,
  and `12.300` specify the
  same number of milliseconds. To get three milliseconds, one must write
  `12.003`, which the conversion treats as
  12 + 0.003 = 12.003 seconds.

  Here is a more
  complex example:
  `to_timestamp('15:12:02.020.001230', 'HH24:MI:SS.MS.US')`
  is 15 hours, 12 minutes, and 2 seconds + 20 milliseconds +
  1230 microseconds = 2.021230 seconds.
* `to_char(..., 'ID')`'s day of the week numbering
  matches the `extract(isodow from ...)` function, but
  `to_char(..., 'D')`'s does not match
  `extract(dow from ...)`'s day numbering.
* `to_char(interval)` formats `HH` and
  `HH12` as shown on a 12-hour clock, for example zero hours
  and 36 hours both output as `12`, while `HH24`
  outputs the full hour value, which can exceed 23 in
  an `interval` value.

[Table 9.29](functions-formatting.md#FUNCTIONS-FORMATTING-NUMERIC-TABLE) shows the
template patterns available for formatting numeric values.

<a id="FUNCTIONS-FORMATTING-NUMERIC-TABLE"></a>

**Table 9.29. Template Patterns for Numeric Formatting**

<table border="1" class="table" summary="Template Patterns for Numeric Formatting"><colgroup><col/><col/></colgroup><thead><tr><th>Pattern</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">9</code></td><td>digit position (can be dropped if insignificant)</td></tr><tr><td><code class="literal">0</code></td><td>digit position (will not be dropped, even if insignificant)</td></tr><tr><td><code class="literal">.</code> (period)</td><td>decimal point</td></tr><tr><td><code class="literal">,</code> (comma)</td><td>group (thousands) separator</td></tr><tr><td><code class="literal">PR</code></td><td>negative value in angle brackets</td></tr><tr><td><code class="literal">S</code></td><td>sign anchored to number (uses locale)</td></tr><tr><td><code class="literal">L</code></td><td>currency symbol (uses locale)</td></tr><tr><td><code class="literal">D</code></td><td>decimal point (uses locale)</td></tr><tr><td><code class="literal">G</code></td><td>group separator (uses locale)</td></tr><tr><td><code class="literal">MI</code></td><td>minus sign in specified position (if number &lt; 0)</td></tr><tr><td><code class="literal">PL</code></td><td>plus sign in specified position (if number &gt; 0)</td></tr><tr><td><code class="literal">SG</code></td><td>plus/minus sign in specified position</td></tr><tr><td><code class="literal">RN</code> or <code class="literal">rn</code></td><td>Roman numeral (values between 1 and 3999)</td></tr><tr><td><code class="literal">TH</code> or <code class="literal">th</code></td><td>ordinal number suffix</td></tr><tr><td><code class="literal">V</code></td><td>shift specified number of digits (see notes)</td></tr><tr><td><code class="literal">EEEE</code></td><td>exponent for scientific notation</td></tr></tbody></table>

<br>

Usage notes for numeric formatting:

* `0` specifies a digit position that will always be printed,
  even if it contains a leading/trailing zero. `9` also
  specifies a digit position, but if it is a leading zero then it will
  be replaced by a space, while if it is a trailing zero and fill mode
  is specified then it will be deleted. (For `to_number()`,
  these two pattern characters are equivalent.)
* If the format provides fewer fractional digits than the number being
  formatted, `to_char()` will round the number to
  the specified number of fractional digits.
* The pattern characters `S`, `L`, `D`,
  and `G` represent the sign, currency symbol, decimal point,
  and thousands separator characters defined by the current locale
  (see [lc_monetary](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MONETARY)
  and [lc_numeric](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-NUMERIC)). The pattern characters period
  and comma represent those exact characters, with the meanings of
  decimal point and thousands separator, regardless of locale.
* If no explicit provision is made for a sign
  in `to_char()`'s pattern, one column will be reserved for
  the sign, and it will be anchored to (appear just left of) the
  number. If `S` appears just left of some `9`'s,
  it will likewise be anchored to the number.
* A sign formatted using `SG`, `PL`, or
  `MI` is not anchored to
  the number; for example,
  `to_char(-12, 'MI9999')` produces `'-  12'`
  but `to_char(-12, 'S9999')` produces `'  -12'`.
  (The Oracle implementation does not allow the use of
  `MI` before `9`, but rather
  requires that `9` precede
  `MI`.)
* `TH` does not convert values less than zero
  and does not convert fractional numbers.
* `PL`, `SG`, and
  `TH` are PostgreSQL
  extensions.
* In `to_number`, if non-data template patterns such
  as `L` or `TH` are used, the
  corresponding number of input characters are skipped, whether or not
  they match the template pattern, unless they are data characters
  (that is, digits, sign, decimal point, or comma). For
  example, `TH` would skip two non-data characters.
* `V` with `to_char`
  multiplies the input values by
  `10^n`, where
  *`n`* is the number of digits following
  `V`. `V` with
  `to_number` divides in a similar manner.
  The `V` can be thought of as marking the position
  of an implicit decimal point in the input or output string.
  `to_char` and `to_number`
  do not support the use of
  `V` combined with a decimal point
  (e.g., `99.9V99` is not allowed).
* `EEEE` (scientific notation) cannot be used in
  combination with any of the other formatting patterns or
  modifiers other than digit and decimal point patterns, and must be at the end of the format string
  (e.g., `9.99EEEE` is a valid pattern).
* In `to_number()`, the `RN`
  pattern converts Roman numerals (in standard form) to numbers.
  Input is case-insensitive, so `RN`
  and `rn` are equivalent. `RN`
  cannot be used in combination with any other formatting patterns or
  modifiers except `FM`, which is applicable only
  in `to_char()` and is ignored
  in `to_number()`.

Certain modifiers can be applied to any template pattern to alter its
behavior. For example, `FM99.99`
is the `99.99` pattern with the
`FM` modifier.
[Table 9.30](functions-formatting.md#FUNCTIONS-FORMATTING-NUMERICMOD-TABLE) shows the
modifier patterns for numeric formatting.

<a id="FUNCTIONS-FORMATTING-NUMERICMOD-TABLE"></a>

**Table 9.30. Template Pattern Modifiers for Numeric Formatting**

<table border="1" class="table" summary="Template Pattern Modifiers for Numeric Formatting"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Modifier</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code class="literal">FM</code> prefix</td><td>fill mode (suppress trailing zeroes and padding blanks)</td><td><code class="literal">FM99.99</code></td></tr><tr><td><code class="literal">TH</code> suffix</td><td>upper case ordinal number suffix</td><td><code class="literal">999TH</code></td></tr><tr><td><code class="literal">th</code> suffix</td><td>lower case ordinal number suffix</td><td><code class="literal">999th</code></td></tr></tbody></table>

<br>

[Table 9.31](functions-formatting.md#FUNCTIONS-FORMATTING-EXAMPLES-TABLE) shows some
examples of the use of the `to_char` function.

<a id="FUNCTIONS-FORMATTING-EXAMPLES-TABLE"></a>

**Table 9.31. `to_char` Examples**

<table border="1" class="table" summary="to_char Examples"><colgroup><col/><col/></colgroup><thead><tr><th>Expression</th><th>Result</th></tr></thead><tbody><tr><td><code class="literal">to_char(current_timestamp, 'Day, DD  HH12:MI:SS')</code></td><td><code class="literal">'Tuesday  , 06  05:39:18'</code></td></tr><tr><td><code class="literal">to_char(current_timestamp, 'FMDay, FMDD  HH12:MI:SS')</code></td><td><code class="literal">'Tuesday, 6  05:39:18'</code></td></tr><tr><td><code class="literal">to_char(current_timestamp AT TIME ZONE
        'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')</code></td><td><code class="literal">'2022-12-06T05:39:18Z'</code>,
        <acronym class="acronym">ISO</acronym> 8601 extended format</td></tr><tr><td><code class="literal">to_char(-0.1, '99.99')</code></td><td><code class="literal">'  -.10'</code></td></tr><tr><td><code class="literal">to_char(-0.1, 'FM9.99')</code></td><td><code class="literal">'-.1'</code></td></tr><tr><td><code class="literal">to_char(-0.1, 'FM90.99')</code></td><td><code class="literal">'-0.1'</code></td></tr><tr><td><code class="literal">to_char(0.1, '0.9')</code></td><td><code class="literal">' 0.1'</code></td></tr><tr><td><code class="literal">to_char(12, '9990999.9')</code></td><td><code class="literal">'    0012.0'</code></td></tr><tr><td><code class="literal">to_char(12, 'FM9990999.9')</code></td><td><code class="literal">'0012.'</code></td></tr><tr><td><code class="literal">to_char(485, '999')</code></td><td><code class="literal">' 485'</code></td></tr><tr><td><code class="literal">to_char(-485, '999')</code></td><td><code class="literal">'-485'</code></td></tr><tr><td><code class="literal">to_char(485, '9 9 9')</code></td><td><code class="literal">' 4 8 5'</code></td></tr><tr><td><code class="literal">to_char(1485, '9,999')</code></td><td><code class="literal">' 1,485'</code></td></tr><tr><td><code class="literal">to_char(1485, '9G999')</code></td><td><code class="literal">' 1 485'</code></td></tr><tr><td><code class="literal">to_char(148.5, '999.999')</code></td><td><code class="literal">' 148.500'</code></td></tr><tr><td><code class="literal">to_char(148.5, 'FM999.999')</code></td><td><code class="literal">'148.5'</code></td></tr><tr><td><code class="literal">to_char(148.5, 'FM999.990')</code></td><td><code class="literal">'148.500'</code></td></tr><tr><td><code class="literal">to_char(148.5, '999D999')</code></td><td><code class="literal">' 148,500'</code></td></tr><tr><td><code class="literal">to_char(3148.5, '9G999D999')</code></td><td><code class="literal">' 3 148,500'</code></td></tr><tr><td><code class="literal">to_char(-485, '999S')</code></td><td><code class="literal">'485-'</code></td></tr><tr><td><code class="literal">to_char(-485, '999MI')</code></td><td><code class="literal">'485-'</code></td></tr><tr><td><code class="literal">to_char(485, '999MI')</code></td><td><code class="literal">'485 '</code></td></tr><tr><td><code class="literal">to_char(485, 'FM999MI')</code></td><td><code class="literal">'485'</code></td></tr><tr><td><code class="literal">to_char(485, 'PL999')</code></td><td><code class="literal">'+485'</code></td></tr><tr><td><code class="literal">to_char(485, 'SG999')</code></td><td><code class="literal">'+485'</code></td></tr><tr><td><code class="literal">to_char(-485, 'SG999')</code></td><td><code class="literal">'-485'</code></td></tr><tr><td><code class="literal">to_char(-485, '9SG99')</code></td><td><code class="literal">'4-85'</code></td></tr><tr><td><code class="literal">to_char(-485, '999PR')</code></td><td><code class="literal">'&lt;485&gt;'</code></td></tr><tr><td><code class="literal">to_char(485, 'L999')</code></td><td><code class="literal">'DM 485'</code></td></tr><tr><td><code class="literal">to_char(485, 'RN')</code></td><td><code class="literal">'        CDLXXXV'</code></td></tr><tr><td><code class="literal">to_char(485, 'FMRN')</code></td><td><code class="literal">'CDLXXXV'</code></td></tr><tr><td><code class="literal">to_char(5.2, 'FMRN')</code></td><td><code class="literal">'V'</code></td></tr><tr><td><code class="literal">to_char(482, '999th')</code></td><td><code class="literal">' 482nd'</code></td></tr><tr><td><code class="literal">to_char(485, '"Good number:"999')</code></td><td><code class="literal">'Good number: 485'</code></td></tr><tr><td><code class="literal">to_char(485.8, '"Pre:"999" Post:" .999')</code></td><td><code class="literal">'Pre: 485 Post: .800'</code></td></tr><tr><td><code class="literal">to_char(12, '99V999')</code></td><td><code class="literal">' 12000'</code></td></tr><tr><td><code class="literal">to_char(12.4, '99V999')</code></td><td><code class="literal">' 12400'</code></td></tr><tr><td><code class="literal">to_char(12.45, '99V9')</code></td><td><code class="literal">' 125'</code></td></tr><tr><td><code class="literal">to_char(0.0004859, '9.99EEEE')</code></td><td><code class="literal">' 4.86e-04'</code></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-formatting.html)（英文原文，待翻譯）
