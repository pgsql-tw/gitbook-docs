# 8.5.1. 日期／時間輸入

<a id="DATATYPE-DATETIME-INPUT"></a>

## 8.5.1. 日期／時間輸入 [#](#datatype-datetime-input) <a href="#datatype-datetime-input" id="datatype-datetime-input"></a>

日期與時間輸入，幾乎能接受任何合理的格式，包括
ISO 8601、SQL 相容格式、
傳統的 POSTGRES 格式，以及其他格式。
對於某些格式而言，日期輸入中日、月、年的順序
是模糊的，因此系統支援指定
這些欄位預期的順序。將
[DateStyle](../../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數
設為 `MDY`，可選擇月-日-年的解讀方式，
設為 `DMY`，可選擇日-月-年的解讀方式，
或設為 `YMD`，可選擇年-月-日的解讀方式。

在處理日期／時間輸入時，
PostgreSQL 比 SQL 標準要求的
更為靈活。
關於日期／時間輸入的精確剖析規則，
以及所能識別的文字欄位（包括月份、星期幾與
時區），請參閱[附錄 B](../../../appendixes/datetime-appendix/README.md)。

請記得，任何日期或時間常值輸入，
都需要像文字字串一樣，用單引號括起來。詳情請參閱
[4.1.2.7 節](../../sql-syntax/sql-syntax-lexical/sql-syntax-constants.md#sql-syntax-constants-generic)。
SQL 要求使用以下語法

```

type [ (p) ] 'value'
```

其中 *`p`* 是一個選用的精確度
指定，用來給出秒欄位中的小數
位數。可以為 `time`、`timestamp` 與
`interval` 型別指定精確度，
範圍可以是 0 到 6。
若在常值規格中未指定精確度，
則預設為該常值本身的精確度（但
不超過 6 位）。

<a id="DATATYPE-DATETIME-INPUT-DATES"></a>

### 8.5.1.1. 日期 [#](#datatype-datetime-input-dates) <a href="#datatype-datetime-input-dates" id="datatype-datetime-input-dates"></a>

<a id="id-1.5.7.13.18.5.2"></a>

[表 8.10](#datatype-datetime-date-table) 展示了
`date` 型別的一些可能輸入方式。

<a id="DATATYPE-DATETIME-DATE-TABLE"></a>

### 表 8.10. 日期輸入 [#](#datatype-datetime-date-table) <a href="#datatype-datetime-date-table" id="datatype-datetime-date-table"></a>

<table border="1" class="table" summary="日期輸入"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td>1999-01-08</td><td>ISO 8601；任何模式下皆為 1 月 8 日
         （建議格式）</td></tr><tr><td>January 8, 1999</td><td>在任何 <code class="varname">datestyle</code> 輸入模式下皆無歧義</td></tr><tr><td>1/8/1999</td><td><code class="literal">MDY</code> 模式下為 1 月 8 日；
          <code class="literal">DMY</code> 模式下為 8 月 1 日</td></tr><tr><td>1/18/1999</td><td><code class="literal">MDY</code> 模式下為 1 月 18 日；
          在其他模式下會被拒絕</td></tr><tr><td>01/02/03</td><td><code class="literal">MDY</code> 模式下為 2003 年 1 月 2 日；
          <code class="literal">DMY</code> 模式下為 2003 年 2 月 1 日；
          <code class="literal">YMD</code> 模式下為 2001 年 2 月 3 日
         </td></tr><tr><td>1999-Jan-08</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>Jan-08-1999</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>08-Jan-1999</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>99-Jan-08</td><td><code class="literal">YMD</code> 模式下為 1 月 8 日，否則錯誤</td></tr><tr><td>08-Jan-99</td><td>1 月 8 日，但在 <code class="literal">YMD</code> 模式下錯誤</td></tr><tr><td>Jan-08-99</td><td>1 月 8 日，但在 <code class="literal">YMD</code> 模式下錯誤</td></tr><tr><td>19990108</td><td>ISO 8601；任何模式下皆為 1999 年 1 月 8 日</td></tr><tr><td>990108</td><td>ISO 8601；任何模式下皆為 1999 年 1 月 8 日</td></tr><tr><td>1999.008</td><td>年份與該年的第幾天</td></tr><tr><td>J2451187</td><td>儒略日（Julian date）</td></tr><tr><td>January 8, 99 BC</td><td>西元前 99 年</td></tr></tbody></table>

<br>

<a id="DATATYPE-DATETIME-INPUT-TIMES"></a>

### 8.5.1.2. 時刻 [#](#datatype-datetime-input-times) <a href="#datatype-datetime-input-times" id="datatype-datetime-input-times"></a>

<a id="id-1.5.7.13.18.6.2"></a><a id="id-1.5.7.13.18.6.3"></a><a id="id-1.5.7.13.18.6.4"></a>

時刻型別為 `time [
(p) ] without time zone` 與
`time [ (p) ] with time
zone`。單獨寫 `time`，等同於
`time without time zone`。

這些型別的有效輸入，由一個時刻，
加上選用的時區組成。（請參閱[表 8.11](#datatype-datetime-time-table)
與[表 8.12](#datatype-timezone-table)。）若在
`time without time zone` 的輸入中，
指定了時區，該時區會被悄悄地忽略。您也可以指定
日期，但它會被忽略，除非您使用了一個
牽涉到日光節約時間（daylight-savings）規則的時區名稱，
例如
`America/New_York`。在這種情況下，
必須指定日期，才能判斷應該套用標準時間
還是日光節約時間。適當的時區偏移量，
會被記錄在
`time with time zone` 值中，並依原樣輸出；
不會依目前的時區來調整。

<a id="DATATYPE-DATETIME-TIME-TABLE"></a>

### 表 8.11. 時刻輸入 [#](#datatype-datetime-time-table) <a href="#datatype-datetime-time-table" id="datatype-datetime-time-table"></a>

<table border="1" class="table" summary="時刻輸入"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">04:05:06.789</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05:06</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">040506</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05 AM</code></td><td>與 04:05 相同；AM 不影響數值</td></tr><tr><td><code class="literal">04:05 PM</code></td><td>與 16:05 相同；輸入的小時必須 &lt;= 12</td></tr><tr><td><code class="literal">04:05:06.789-8</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">04:05:06-08:00</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">04:05-08:00</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506-08</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506+0730</code></td><td>ISO 8601，時區以帶小數小時的 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506+07:30:00</code></td><td>UTC 偏移量精確到秒（ISO 8601 中不允許）</td></tr><tr><td><code class="literal">04:05:06 PST</code></td><td>以縮寫指定時區</td></tr><tr><td><code class="literal">2003-04-12 04:05:06 America/New_York</code></td><td>以完整名稱指定時區</td></tr></tbody></table>

<br><a id="DATATYPE-TIMEZONE-TABLE"></a>

### 表 8.12. 時區輸入 [#](#datatype-timezone-table) <a href="#datatype-timezone-table" id="datatype-timezone-table"></a>

<table border="1" class="table" summary="時區輸入"><colgroup><col/><col/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">PST</code></td><td>縮寫（代表 Pacific Standard Time）</td></tr><tr><td><code class="literal">America/New_York</code></td><td>完整時區名稱</td></tr><tr><td><code class="literal">PST8PDT</code></td><td>POSIX 風格的時區規格</td></tr><tr><td><code class="literal">-8:00:00</code></td><td>PST 的 UTC 偏移量</td></tr><tr><td><code class="literal">-8:00</code></td><td>PST 的 UTC 偏移量（ISO 8601 擴充格式）</td></tr><tr><td><code class="literal">-800</code></td><td>PST 的 UTC 偏移量（ISO 8601 基本格式）</td></tr><tr><td><code class="literal">-8</code></td><td>PST 的 UTC 偏移量（ISO 8601 基本格式）</td></tr><tr><td><code class="literal">zulu</code></td><td>UTC 的軍用縮寫</td></tr><tr><td><code class="literal">z</code></td><td><code class="literal">zulu</code> 的簡短形式（同樣也出現在 ISO 8601 中）</td></tr></tbody></table>

<br>

關於如何指定時區的更多資訊，請參閱[8.5.3 節](../datatype-datetime.md#datatype-timezones)。

<a id="DATATYPE-DATETIME-INPUT-TIME-STAMPS"></a>

### 8.5.1.3. 時間戳記 [#](#datatype-datetime-input-time-stamps) <a href="#datatype-datetime-input-time-stamps" id="datatype-datetime-input-time-stamps"></a>

<a id="id-1.5.7.13.18.7.2"></a><a id="id-1.5.7.13.18.7.3"></a><a id="id-1.5.7.13.18.7.4"></a>

時間戳記型別的有效輸入，
由日期與時刻串接，
後面加上選用的時區，
再加上選用的 `AD` 或 `BC` 組成。
（另外，`AD`/`BC` 也可以出現在
時區之前，但這不是偏好的順序。）
因此：

```

1999-01-08 04:05:06
```

以及：

```

1999-01-08 04:05:06 -8:00
```

都是有效的值，且遵循 ISO 8601
標準。此外，也支援常見的格式：

```

January 8 04:05:06 1999 PST
```

SQL 標準是透過時刻後面
是否出現「+」或「-」符號及時區偏移量，
來區分 `timestamp without time zone`
與 `timestamp with time zone` 常值的。
因此，依照標準，

```

TIMESTAMP '2004-10-19 10:23:54'
```

是一個 `timestamp without time zone`，而

```

TIMESTAMP '2004-10-19 10:23:54+02'
```

則是一個 `timestamp with time zone`。
PostgreSQL 在判斷型別之前，
永遠不會檢視常值字串的內容，因此
會將上述兩者，都視為 `timestamp without time zone`。
若要確保某個常值，被視為 `timestamp with time
zone`，請為它明確指定正確的型別：

```

TIMESTAMP WITH TIME ZONE '2004-10-19 10:23:54+02'
```

對於已判定為 `timestamp without time
zone` 的值，PostgreSQL
會悄悄地忽略其中的任何時區指示。
也就是說，最終結果值，是從輸入字串中的
日期／時間欄位得出的，不會因時區而調整。

對於 `timestamp with time zone` 的值，
若輸入字串包含明確的時區，
會使用該時區適當的偏移量，
被轉換為 UTC（[*協調世界時
（Universal Coordinated
Time）*](../../../appendixes/glossary/README.md#glossary-utc)）。
若輸入字串中未指定時區，
則會假設它是採用系統
[TimeZone](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 參數所指示的時區，
並使用該
`timezone` 時區的偏移量，轉換為 UTC。
無論哪一種情況，該值都會以 UTC 的形式，
儲存在內部，而原本陳述或假設的時區，
並不會被保留。

當輸出 `timestamp with time
zone` 值時，永遠會從 UTC 轉換為
目前的 `timezone` 時區，並以該
時區的當地時間顯示。若要以另一個時區來檢視時刻，
可以變更
`timezone`，或使用 `AT TIME ZONE` 結構
（請參閱[9.9.4 節](../../functions/functions-datetime/functions-datetime-zoneconvert.md#functions-datetime-zoneconvert)）。

在 `timestamp without time zone` 與
`timestamp with time zone` 之間轉換時，
一般會假設 `timestamp without time zone` 的值，
應該被視為或給定為 `timezone`
的當地時間。可以使用 `AT TIME ZONE`
為這個轉換，指定不同的時區。

<a id="DATATYPE-DATETIME-SPECIAL-VALUES"></a>

### 8.5.1.4. 特殊值 [#](#datatype-datetime-special-values) <a href="#datatype-datetime-special-values" id="datatype-datetime-special-values"></a>

<a id="id-1.5.7.13.18.8.2"></a><a id="id-1.5.7.13.18.8.3"></a>

為了方便起見，PostgreSQL
支援幾種特殊的日期／時間輸入值，
如[表 8.13](#datatype-datetime-special-table)所示。值
`infinity` 與 `-infinity`
在系統內部有特殊的表示方式，會原樣
顯示；但其他值只是單純的標記簡寫，
在讀取時，會被轉換為一般的日期／時間值。
（具體來說，`now` 以及相關的字串，
一經讀取，就會立即被轉換為某個特定的時間值。）
在 SQL 指令中，將以下所有這些值
作為常值使用時，都需要以單引號括起來。

<a id="DATATYPE-DATETIME-SPECIAL-TABLE"></a>

### 表 8.13. 特殊日期／時間輸入 [#](#datatype-datetime-special-table) <a href="#datatype-datetime-special-table" id="datatype-datetime-special-table"></a>

<table border="1" class="table" summary="特殊日期/時間輸入"><colgroup><col/><col/><col/></colgroup><thead><tr><th>輸入字串</th><th>有效型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">epoch</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>1970-01-01 00:00:00+00（Unix 系統時間的零點）</td></tr><tr><td><code class="literal">infinity</code></td><td><code class="type">date</code>、<code class="type">timestamp</code>、<code class="type">interval</code></td><td>比所有其他時間戳記都晚</td></tr><tr><td><code class="literal">-infinity</code></td><td><code class="type">date</code>、<code class="type">timestamp</code>、<code class="type">interval</code></td><td>比所有其他時間戳記都早</td></tr><tr><td><code class="literal">now</code></td><td><code class="type">date</code>、<code class="type">time</code>、<code class="type">timestamp</code></td><td>目前交易的開始時間</td></tr><tr><td><code class="literal">today</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>今天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">tomorrow</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>明天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">yesterday</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>昨天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">allballs</code></td><td><code class="type">time</code></td><td>00:00:00.00 UTC</td></tr></tbody></table>

<br>

以下相容於 SQL 的函式，
同樣可用來取得對應資料型別的目前時刻值：
`CURRENT_DATE`、`CURRENT_TIME`、
`CURRENT_TIMESTAMP`、`LOCALTIME`、
`LOCALTIMESTAMP`。（請參閱[9.9.5 節](../../functions/functions-datetime.md#functions-datetime-current)。）請注意，這些是
SQL 函式，在資料輸入字串中，*不會*被識別。

### 注意 [#](#xiao-xin) <a href="#xiao-xin" id="xiao-xin"></a>

{% hint style="warning" %}
雖然輸入字串 `now`、
`today`、`tomorrow`
與 `yesterday`，很適合用於互動式 SQL
指令中，但當該指令被儲存下來，稍後才執行時，
例如在預備陳述式、檢視表與函式定義中，
它們的行為可能會令人意外。這個字串，可能會被轉換為
某個特定的時間值，而該值在過時許久之後，
仍會持續被使用。在這類情境中，請改用
其中一種 SQL 函式。舉例來說，
`CURRENT_DATE + 1` 就比
`'tomorrow'::date` 更安全。
{% endhint %}

[返回 8.5. 日期／時間型別](../datatype-datetime.md#datatype-datetime)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
