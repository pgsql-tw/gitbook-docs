<a id="DATATYPE-DATETIME"></a>
## 8.5. 日期／時間型別 [#](#DATATYPE-DATETIME)

[8.5.1. 日期／時間輸入](datatype-datetime.md#DATATYPE-DATETIME-INPUT)

[8.5.2. 日期／時間輸出](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT)

[8.5.3. 時區](datatype-datetime.md#DATATYPE-TIMEZONES)

[8.5.4. 時間區間輸入](datatype-datetime.md#DATATYPE-INTERVAL-INPUT)

[8.5.5. 時間區間輸出](datatype-datetime.md#DATATYPE-INTERVAL-OUTPUT)

<a id="id-1.5.7.13.2"></a><a id="id-1.5.7.13.3"></a><a id="id-1.5.7.13.4"></a><a id="id-1.5.7.13.5"></a><a id="id-1.5.7.13.6"></a><a id="id-1.5.7.13.7"></a><a id="id-1.5.7.13.8"></a><a id="id-1.5.7.13.9"></a><a id="id-1.5.7.13.10"></a><a id="id-1.5.7.13.11"></a>

PostgreSQL 支援
[表 8.9](datatype-datetime.md#DATATYPE-DATETIME-TABLE) 中所示的完整一組
SQL 日期與時間型別。這些資料型別上可用的運算，
說明於
[9.9 節](../functions/functions-datetime.md)。
日期是依照格里曆（Gregorian calendar）計算的，
即使是在該曆法引入之前的年份也是如此
（詳情請參閱[B.6 節](../../appendixes/datetime-appendix/datetime-units-history.md)）。

<a id="DATATYPE-DATETIME-TABLE"></a>

**表 8.9. 日期／時間型別**

<table border="1" class="table" summary="日期/時間型別"><colgroup><col/><col/><col/><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>儲存大小</th><th>說明</th><th>最小值</th><th>最大值</th><th>解析度</th></tr></thead><tbody><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td>8 位元組</td><td>日期與時間（無時區）</td><td>4713 BC</td><td>294276 AD</td><td>1 微秒</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td>8 位元組</td><td>日期與時間，含時區</td><td>4713 BC</td><td>294276 AD</td><td>1 微秒</td></tr><tr><td><code class="type">date</code></td><td>4 位元組</td><td>日期（無時刻）</td><td>4713 BC</td><td>5874897 AD</td><td>1 天</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td>8 位元組</td><td>時刻（無日期）</td><td>00:00:00</td><td>24:00:00</td><td>1 微秒</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td>12 位元組</td><td>時刻（無日期），含時區</td><td>00:00:00+1559</td><td>24:00:00-1559</td><td>1 微秒</td></tr><tr><td><code class="type">interval [ <em class="replaceable"><code>fields</code></em> ] [ (<em class="replaceable"><code>p</code></em>) ]</code></td><td>16 位元組</td><td>時間區間</td><td>-178000000 年</td><td>178000000 年</td><td>1 微秒</td></tr></tbody></table>

<br>

### 注意

SQL 標準要求單獨寫
`timestamp`，須等同於 `timestamp without time
zone`，PostgreSQL 也遵循這項
行為。`timestamptz` 可作為
`timestamp with time zone` 的縮寫來使用；這是
PostgreSQL 的擴充功能。

`time`、`timestamp` 與
`interval`，都可以接受一個選用的精確度值
*`p`*，用來指定秒欄位中
保留的小數位數。預設情況下，
精確度沒有明確的上限。
*`p`* 允許的範圍為 0 到 6。

`interval` 型別還有一項額外的選項，
可以透過寫下以下其中一個片語，來限制所儲存欄位的集合：

```

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

請注意，若同時指定了 *`fields`* 與
*`p`*，則
*`fields`* 必須包含 `SECOND`，
因為精確度只適用於秒。

`time with time zone` 型別，是由 SQL
標準所定義的，但這項定義所呈現的特性，
使其實用性令人存疑。在大多數情況下，
`date`、`time`、`timestamp without time
zone` 與 `timestamp with time zone` 的組合，
應該就能提供任何應用程式
所需的完整日期／時間功能範圍。

<a id="DATATYPE-DATETIME-INPUT"></a>

### 8.5.1. 日期／時間輸入 [#](#DATATYPE-DATETIME-INPUT)

日期與時間輸入，幾乎能接受任何合理的格式，包括
ISO 8601、SQL 相容格式、
傳統的 POSTGRES 格式，以及其他格式。
對於某些格式而言，日期輸入中日、月、年的順序
是模糊的，因此系統支援指定
這些欄位預期的順序。將
[DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數
設為 `MDY`，可選擇月-日-年的解讀方式，
設為 `DMY`，可選擇日-月-年的解讀方式，
或設為 `YMD`，可選擇年-月-日的解讀方式。

在處理日期／時間輸入時，
PostgreSQL 比 SQL 標準要求的
更為靈活。
關於日期／時間輸入的精確剖析規則，
以及所能識別的文字欄位（包括月份、星期幾與
時區），請參閱[附錄 B](../../appendixes/datetime-appendix/README.md)。

請記得，任何日期或時間常值輸入，
都需要像文字字串一樣，用單引號括起來。詳情請參閱
[4.1.2.7 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC)。
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

#### 8.5.1.1. 日期 [#](#DATATYPE-DATETIME-INPUT-DATES)

<a id="id-1.5.7.13.18.5.2"></a>

[表 8.10](datatype-datetime.md#DATATYPE-DATETIME-DATE-TABLE) 展示了
`date` 型別的一些可能輸入方式。

<a id="DATATYPE-DATETIME-DATE-TABLE"></a>

**表 8.10. 日期輸入**

<table border="1" class="table" summary="日期輸入"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td>1999-01-08</td><td>ISO 8601；任何模式下皆為 1 月 8 日
         （建議格式）</td></tr><tr><td>January 8, 1999</td><td>在任何 <code class="varname">datestyle</code> 輸入模式下皆無歧義</td></tr><tr><td>1/8/1999</td><td><code class="literal">MDY</code> 模式下為 1 月 8 日；
          <code class="literal">DMY</code> 模式下為 8 月 1 日</td></tr><tr><td>1/18/1999</td><td><code class="literal">MDY</code> 模式下為 1 月 18 日；
          在其他模式下會被拒絕</td></tr><tr><td>01/02/03</td><td><code class="literal">MDY</code> 模式下為 2003 年 1 月 2 日；
          <code class="literal">DMY</code> 模式下為 2003 年 2 月 1 日；
          <code class="literal">YMD</code> 模式下為 2001 年 2 月 3 日
         </td></tr><tr><td>1999-Jan-08</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>Jan-08-1999</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>08-Jan-1999</td><td>任何模式下皆為 1 月 8 日</td></tr><tr><td>99-Jan-08</td><td><code class="literal">YMD</code> 模式下為 1 月 8 日，否則錯誤</td></tr><tr><td>08-Jan-99</td><td>1 月 8 日，但在 <code class="literal">YMD</code> 模式下錯誤</td></tr><tr><td>Jan-08-99</td><td>1 月 8 日，但在 <code class="literal">YMD</code> 模式下錯誤</td></tr><tr><td>19990108</td><td>ISO 8601；任何模式下皆為 1999 年 1 月 8 日</td></tr><tr><td>990108</td><td>ISO 8601；任何模式下皆為 1999 年 1 月 8 日</td></tr><tr><td>1999.008</td><td>年份與該年的第幾天</td></tr><tr><td>J2451187</td><td>儒略日（Julian date）</td></tr><tr><td>January 8, 99 BC</td><td>西元前 99 年</td></tr></tbody></table>

<br>

<a id="DATATYPE-DATETIME-INPUT-TIMES"></a>

#### 8.5.1.2. 時刻 [#](#DATATYPE-DATETIME-INPUT-TIMES)

<a id="id-1.5.7.13.18.6.2"></a><a id="id-1.5.7.13.18.6.3"></a><a id="id-1.5.7.13.18.6.4"></a>

時刻型別為 `time [
(p) ] without time zone` 與
`time [ (p) ] with time
zone`。單獨寫 `time`，等同於
`time without time zone`。

這些型別的有效輸入，由一個時刻，
加上選用的時區組成。（請參閱[表 8.11](datatype-datetime.md#DATATYPE-DATETIME-TIME-TABLE)
與[表 8.12](datatype-datetime.md#DATATYPE-TIMEZONE-TABLE)。）若在
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

**表 8.11. 時刻輸入**

<table border="1" class="table" summary="時刻輸入"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">04:05:06.789</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05:06</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">040506</code></td><td>ISO 8601</td></tr><tr><td><code class="literal">04:05 AM</code></td><td>與 04:05 相同；AM 不影響數值</td></tr><tr><td><code class="literal">04:05 PM</code></td><td>與 16:05 相同；輸入的小時必須 &lt;= 12</td></tr><tr><td><code class="literal">04:05:06.789-8</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">04:05:06-08:00</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">04:05-08:00</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506-08</code></td><td>ISO 8601，時區以 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506+0730</code></td><td>ISO 8601，時區以帶小數小時的 UTC 偏移量表示</td></tr><tr><td><code class="literal">040506+07:30:00</code></td><td>UTC 偏移量精確到秒（ISO 8601 中不允許）</td></tr><tr><td><code class="literal">04:05:06 PST</code></td><td>以縮寫指定時區</td></tr><tr><td><code class="literal">2003-04-12 04:05:06 America/New_York</code></td><td>以完整名稱指定時區</td></tr></tbody></table>

<br><a id="DATATYPE-TIMEZONE-TABLE"></a>

**表 8.12. 時區輸入**

<table border="1" class="table" summary="時區輸入"><colgroup><col/><col/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">PST</code></td><td>縮寫（代表 Pacific Standard Time）</td></tr><tr><td><code class="literal">America/New_York</code></td><td>完整時區名稱</td></tr><tr><td><code class="literal">PST8PDT</code></td><td>POSIX 風格的時區規格</td></tr><tr><td><code class="literal">-8:00:00</code></td><td>PST 的 UTC 偏移量</td></tr><tr><td><code class="literal">-8:00</code></td><td>PST 的 UTC 偏移量（ISO 8601 擴充格式）</td></tr><tr><td><code class="literal">-800</code></td><td>PST 的 UTC 偏移量（ISO 8601 基本格式）</td></tr><tr><td><code class="literal">-8</code></td><td>PST 的 UTC 偏移量（ISO 8601 基本格式）</td></tr><tr><td><code class="literal">zulu</code></td><td>UTC 的軍用縮寫</td></tr><tr><td><code class="literal">z</code></td><td><code class="literal">zulu</code> 的簡短形式（同樣也出現在 ISO 8601 中）</td></tr></tbody></table>

<br>

關於如何指定時區的更多資訊，請參閱[8.5.3 節](datatype-datetime.md#DATATYPE-TIMEZONES)。

<a id="DATATYPE-DATETIME-INPUT-TIME-STAMPS"></a>

#### 8.5.1.3. 時間戳記 [#](#DATATYPE-DATETIME-INPUT-TIME-STAMPS)

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
被轉換為 UTC（[*[協調世界時
（Universal Coordinated
Time）](../../appendixes/glossary/README.md#GLOSSARY-UTC)*](../../appendixes/glossary/README.md#GLOSSARY-UTC)）。
若輸入字串中未指定時區，
則會假設它是採用系統
[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 參數所指示的時區，
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
（請參閱[9.9.4 節](../functions/functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)）。

在 `timestamp without time zone` 與
`timestamp with time zone` 之間轉換時，
一般會假設 `timestamp without time zone` 的值，
應該被視為或給定為 `timezone`
的當地時間。可以使用 `AT TIME ZONE`
為這個轉換，指定不同的時區。

<a id="DATATYPE-DATETIME-SPECIAL-VALUES"></a>

#### 8.5.1.4. 特殊值 [#](#DATATYPE-DATETIME-SPECIAL-VALUES)

<a id="id-1.5.7.13.18.8.2"></a><a id="id-1.5.7.13.18.8.3"></a>

為了方便起見，PostgreSQL
支援幾種特殊的日期／時間輸入值，
如[表 8.13](datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-TABLE)所示。值
`infinity` 與 `-infinity`
在系統內部有特殊的表示方式，會原樣
顯示；但其他值只是單純的標記簡寫，
在讀取時，會被轉換為一般的日期／時間值。
（具體來說，`now` 以及相關的字串，
一經讀取，就會立即被轉換為某個特定的時間值。）
在 SQL 指令中，將以下所有這些值
作為常值使用時，都需要以單引號括起來。

<a id="DATATYPE-DATETIME-SPECIAL-TABLE"></a>

**表 8.13. 特殊日期／時間輸入**

<table border="1" class="table" summary="特殊日期/時間輸入"><colgroup><col/><col/><col/></colgroup><thead><tr><th>輸入字串</th><th>有效型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">epoch</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>1970-01-01 00:00:00+00（Unix 系統時間的零點）</td></tr><tr><td><code class="literal">infinity</code></td><td><code class="type">date</code>、<code class="type">timestamp</code>、<code class="type">interval</code></td><td>比所有其他時間戳記都晚</td></tr><tr><td><code class="literal">-infinity</code></td><td><code class="type">date</code>、<code class="type">timestamp</code>、<code class="type">interval</code></td><td>比所有其他時間戳記都早</td></tr><tr><td><code class="literal">now</code></td><td><code class="type">date</code>、<code class="type">time</code>、<code class="type">timestamp</code></td><td>目前交易的開始時間</td></tr><tr><td><code class="literal">today</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>今天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">tomorrow</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>明天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">yesterday</code></td><td><code class="type">date</code>、<code class="type">timestamp</code></td><td>昨天的午夜（<code class="literal">00:00</code>）</td></tr><tr><td><code class="literal">allballs</code></td><td><code class="type">time</code></td><td>00:00:00.00 UTC</td></tr></tbody></table>

<br>

以下相容於 SQL 的函式，
同樣可用來取得對應資料型別的目前時刻值：
`CURRENT_DATE`、`CURRENT_TIME`、
`CURRENT_TIMESTAMP`、`LOCALTIME`、
`LOCALTIMESTAMP`。（請參閱[9.9.5 節](../functions/functions-datetime.md#FUNCTIONS-DATETIME-CURRENT)。）請注意，這些是
SQL 函式，在資料輸入字串中，*不會*被識別。

### 小心

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

<a id="DATATYPE-DATETIME-OUTPUT"></a>

### 8.5.2. 日期／時間輸出 [#](#DATATYPE-DATETIME-OUTPUT)

<a id="id-1.5.7.13.19.2"></a><a id="id-1.5.7.13.19.3"></a>

日期／時間型別的輸出格式，可以設定為以下
四種風格之一：ISO 8601、
SQL（Ingres）、傳統的 POSTGRES
（Unix 日期格式），或
German（德式）。預設值
是 ISO 格式。（SQL 標準
要求使用 ISO 8601 格式。
「SQL」這個輸出格式的名稱，
是一段歷史上的巧合。）[表 8.14](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT-TABLE) 展示了
每一種輸出風格的範例。`date` 型別與
`time` 型別的輸出，通常只會依照給定範例，
只顯示日期或時刻的部分。不過，
POSTGRES 風格會以 ISO 格式輸出僅含日期的值。

<a id="DATATYPE-DATETIME-OUTPUT-TABLE"></a>

**表 8.14. 日期／時間輸出風格**

<table border="1" class="table" summary="日期/時間輸出樣式"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>風格規格</th><th>說明</th><th>範例</th></tr></thead><tbody><tr><td><code class="literal">ISO</code></td><td>ISO 8601，SQL 標準</td><td><code class="literal">1997-12-17 07:37:16-08</code></td></tr><tr><td><code class="literal">SQL</code></td><td>傳統風格</td><td><code class="literal">12/17/1997 07:37:16.00 PST</code></td></tr><tr><td><code class="literal">Postgres</code></td><td>原始風格</td><td><code class="literal">Wed Dec 17 07:37:16 1997 PST</code></td></tr><tr><td><code class="literal">German</code></td><td>地區風格</td><td><code class="literal">17.12.1997 07:37:16.00 PST</code></td></tr></tbody></table>

<br>

### 注意

ISO 8601 規定使用大寫字母 `T`，
來分隔日期與時刻。PostgreSQL 在輸入時
接受這種格式，但在輸出時，如上所示，
會使用空白而非 `T`。這是為了
提高可讀性，並與
[RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)
以及其他一些資料庫系統保持一致。

在 SQL 與 POSTGRES 風格中，
若指定了 DMY 欄位順序，日會出現在
月之前，否則月會出現在
日之前。
（關於此設定如何同時影響輸入值的解讀方式，
請參閱[8.5.1 節](datatype-datetime.md#DATATYPE-DATETIME-INPUT)。）
[表 8.15](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT2-TABLE) 展示了一些範例。

<a id="DATATYPE-DATETIME-OUTPUT2-TABLE"></a>

**表 8.15. 日期順序慣例**

<table border="1" class="table" summary="日期順序慣例"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th><code class="varname">datestyle</code> 設定</th><th>輸入順序</th><th>範例輸出</th></tr></thead><tbody><tr><td><code class="literal">SQL, DMY</code></td><td><em class="replaceable"><code>day</code></em>/<em class="replaceable"><code>month</code></em>/<em class="replaceable"><code>year</code></em></td><td><code class="literal">17/12/1997 15:37:16.00 CET</code></td></tr><tr><td><code class="literal">SQL, MDY</code></td><td><em class="replaceable"><code>month</code></em>/<em class="replaceable"><code>day</code></em>/<em class="replaceable"><code>year</code></em></td><td><code class="literal">12/17/1997 07:37:16.00 PST</code></td></tr><tr><td><code class="literal">Postgres, DMY</code></td><td><em class="replaceable"><code>day</code></em>/<em class="replaceable"><code>month</code></em>/<em class="replaceable"><code>year</code></em></td><td><code class="literal">Wed 17 Dec 07:37:16 1997 PST</code></td></tr></tbody></table>

<br>

在 ISO 風格中，時區永遠會以一個
帶正負號的數值偏移量表示，相對於 UTC，
格林威治以東的時區使用正號。若時區偏移量
是整數小時，則會顯示為
*`hh`*（僅小時）；若是整數分鐘，
則顯示為
*`hh`*:*`mm`*；否則
顯示為
*`hh`*:*`mm`*:*`ss`*。
（第三種情況，在任何現代時區標準下都不可能出現，
但在處理早於標準化時區採用之前的時間戳記時，
可能會出現。）
在其他日期風格中，若目前時區有常用的字母縮寫，
時區就會以該字母縮寫顯示。否則
會以 ISO 8601 基本格式中，
帶正負號的數值偏移量顯示
（*`hh`* 或 *`hhmm`*）。
這些風格中所顯示的字母縮寫，
是取自 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 執行時期參數
目前所選擇的 IANA 時區資料庫項目；它們
不受 [timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) 設定的影響。

使用者可以透過
`SET datestyle` 指令、
`postgresql.conf` 組態檔中的
[DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數，
或伺服器或用戶端上的
`PGDATESTYLE` 環境變數，
來選擇日期／時間風格。

格式化函式 `to_char`
（請參閱[9.8 節](../functions/functions-formatting.md)），
也提供了一種更靈活的方式，
來格式化日期／時間輸出。

<a id="DATATYPE-TIMEZONES"></a>

### 8.5.3. 時區 [#](#DATATYPE-TIMEZONES)

<a id="id-1.5.7.13.20.2"></a>

時區與時區慣例，受政治決策的影響，
而不只是地球幾何。全球的時區，
在二十世紀期間變得相對標準化，
但至今仍然容易出現任意的變動，
尤其是在日光節約時間規則方面。
PostgreSQL 使用廣為使用的
IANA（Olson）時區資料庫，
來取得歷史時區規則的資訊。對於未來的時刻，
其假設是，某個給定時區目前已知的最新規則，
將會無限期地持續適用下去。

PostgreSQL 力求在典型用法上，
與 SQL 標準的定義相容。
然而，SQL 標準對日期與時間型別及功能，
有著相當奇特的組合。有兩個明顯的問題：

* 雖然 `date` 型別
  不能有相關聯的時區，
  但 `time` 型別卻可以。
  現實世界中的時區，除非同時與日期
  及時刻相關聯，否則意義不大，
  因為隨著日光節約時間的邊界，偏移量
  可能在一年當中有所不同。
* 預設時區，是以相對於 UTC 的
  固定數值偏移量來指定的。因此，
  在跨越日光節約時間邊界進行日期／時間運算時，
  無法適應日光節約時間。

為了解決這些困難，我們建議在使用時區時，
使用同時包含日期與時刻的日期／時間型別。我們
*不*建議使用 `time with
time zone` 型別（儘管 PostgreSQL
基於舊有應用程式的相容性，
以及符合 SQL 標準的考量，支援這個型別）。
對於任何僅包含日期或時刻的型別，
PostgreSQL 都會假設採用
您的本地時區。

所有具時區感知能力的日期與時刻，
在內部都是以 UTC 儲存的。在顯示給用戶端之前，
它們會被轉換為
[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 組態
參數所指定時區的當地時間。

PostgreSQL 讓您能以三種
不同的形式，指定時區：

* 完整的時區名稱，例如 `America/New_York`。
  可識別的時區名稱，列於
  `pg_timezone_names` 檢視表中
  （請參閱[53.34 節](../../internals/views/view-pg-timezone-names.md)）。
  PostgreSQL 為此目的，使用廣為使用的
  IANA 時區資料，因此，其他軟體，
  也同樣能識別相同的時區
  名稱。
* 時區縮寫，例如 `PST`。這樣的
  指定方式，只是單純定義了相對於 UTC 的某個特定
  偏移量，相對地，完整時區名稱，
  也可能隱含一組日光節約
  轉換規則。可識別的縮寫，
  列於 `pg_timezone_abbrevs` 檢視表中
  （請參閱[53.33 節](../../internals/views/view-pg-timezone-abbrevs.md)）。您無法將
  組態參數 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 或
  [log_timezone](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-TIMEZONE) 設定為
  時區縮寫，但您可以在
  日期／時間輸入值中，以及搭配 `AT TIME ZONE`
  運算子使用縮寫。
* 除了時區名稱與縮寫之外，
  PostgreSQL 也會接受 POSIX 風格的時區
  規格，說明請見
  [B.5 節](../../appendixes/datetime-appendix/datetime-posix-timezone-specs.md)。這個選項，
  一般而言，並不比使用具名時區更受青睞，
  但若沒有合適的 IANA 時區項目可用，
  可能就有必要使用它。

簡言之，這就是縮寫
與完整名稱之間的差異：縮寫代表相對於 UTC 的
特定偏移量，而許多完整名稱，
則隱含了本地的日光節約時間規則，
因此有兩種可能的 UTC 偏移量。舉例來說，
`2014-06-04 12:00 America/New_York` 代表紐約當地
時間的中午，而對於這個特定日期而言，
當時是東部日光節約時間
（UTC-4）。因此 `2014-06-04 12:00 EDT` 指定的是
同一個時刻。但 `2014-06-04 12:00 EST` 指定的是
東部標準時間（UTC-5）的中午，
無論那一天名義上是否實施日光
節約時間。

<a id="id-1.5.7.13.20.3"></a>

### 注意

POSIX 風格時區規格中的正負號，
與 ISO-8601 日期時間值中的正負號，意義相反。舉例來說，
`2014-06-04 12:00+04` 對應的 POSIX 時區，
會是 UTC-4。

更複雜的是，有些司法管轄區，
在不同的時期，會使用同一個時區
縮寫，來代表不同的 UTC 偏移量；舉例來說，
在莫斯科，`MSK` 在某些年份代表 UTC+3，
在其他年份則代表 UTC+4。PostgreSQL
會依照這類縮寫在指定日期當時所代表的意義來解讀；
若該縮寫在該日期並無對應的意義，
則改採其最近一次代表的意義；但，如同上面
`EST` 的例子，這未必與
該日期的當地民用時間相同。

在所有情況下，時區名稱與縮寫，
都是不分大小寫來辨識的。（這是相對於
8.2 之前的 PostgreSQL 版本的一項變更，
先前的版本，在某些情境下區分大小寫，
但在其他情境下則不區分。）

無論是時區名稱還是縮寫，都不是寫死在
伺服器中的；它們是從安裝目錄下的
`.../share/timezone/` 與 `.../share/timezonesets/`
組態檔中取得的
（請參閱[B.4 節](../../appendixes/datetime-appendix/datetime-config-files.md)）。

[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 組態參數，可以
在檔案 `postgresql.conf` 中設定，
或以[第 19 章](../../server-administration/runtime-config/README.md)中所述的
其他任何標準方式來設定。
此外，還有一些特殊的設定方式：

* SQL 指令 `SET TIME ZONE`，
  可以設定工作階段的時區。這是
  `SET TIMEZONE TO` 的另一種寫法，
  其語法更符合 SQL 規範。
* `PGTZ` 環境變數，
  由 libpq 用戶端使用，
  在連線時，向伺服器傳送一則
  `SET TIME ZONE`
  指令。

<a id="DATATYPE-INTERVAL-INPUT"></a>

### 8.5.4. 時間區間輸入 [#](#DATATYPE-INTERVAL-INPUT)

<a id="id-1.5.7.13.21.2"></a>

`interval` 值可以使用以下的
詳細語法來撰寫：

```

[@] quantity unit [quantity unit...] [direction]
```

其中 *`quantity`* 是一個數字（可以帶正負號）；
*`unit`* 是 `microsecond`、
`millisecond`、`second`、
`minute`、`hour`、`day`、
`week`、`month`、`year`、
`decade`、`century`、`millennium`，
或這些單位的縮寫或複數形式；
*`direction`* 可以是 `ago` 或
空白。at 符號（`@`）是選用的裝飾，不影響意義。
不同單位的數量，會依照適當的正負號
隱含地相加。`ago` 會將所有欄位取負。
若 [IntervalStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-INTERVALSTYLE) 設為
`postgres_verbose`，
這種語法也會用於 interval 的輸出。

天、時、分、秒的數量，可以在不明確標示
單位的情況下指定。舉例來說，`'1 12:59:10'`，
讀起來與 `'1 day 12 hours 59 min 10 sec'`
相同。此外，
年與月的組合，也可以用一個連字號來指定；
舉例來說，`'200-10'`，讀起來與 `'200 years
10 months'` 相同。（這些較短的形式，
實際上是 SQL 標準唯一允許的形式，
在 `IntervalStyle` 設為
`sql_standard` 時，會用於輸出。）

時間區間值，也可以寫成 ISO 8601 時間區間，
使用標準第 4.4.3.2 節的「帶指示符格式」，
或第 4.4.3.3 節的「替代格式」。帶指示符
的格式看起來像這樣：

```

P quantity unit [ quantity unit ...] [ T [ quantity unit ...]]
```

該字串必須以 `P` 開頭，且可以包含一個
`T`，用來引出時刻的單位。可用的
單位縮寫，列於[表 8.16](datatype-datetime.md#DATATYPE-INTERVAL-ISO8601-UNITS)中。單位
可以省略，也可以以任何順序指定，但小於
一天的單位，必須出現在 `T` 之後。特別是，
`M` 的意義，取決於它是出現在
`T` 之前還是之後。

<a id="DATATYPE-INTERVAL-ISO8601-UNITS"></a>

**表 8.16. ISO 8601 時間區間單位縮寫**

<table border="1" class="table" summary="ISO 8601 時間區間單位縮寫"><colgroup><col/><col/></colgroup><thead><tr><th>縮寫</th><th>意義</th></tr></thead><tbody><tr><td>Y</td><td>年</td></tr><tr><td>M</td><td>月（在日期部分）</td></tr><tr><td>W</td><td>週</td></tr><tr><td>D</td><td>日</td></tr><tr><td>H</td><td>時</td></tr><tr><td>M</td><td>分（在時刻部分）</td></tr><tr><td>S</td><td>秒</td></tr></tbody></table>

<br>

在替代格式中：

```

P [ years-months-days ] [ T hours:minutes:seconds ]
```

該字串必須以 `P` 開頭，且以
`T` 分隔該 interval 的日期部分與時刻部分。
這些值，是以類似 ISO 8601 日期的數字形式給出的。

在撰寫帶有 *`fields`*
規格的 interval 常值時，或將字串指定給
以 *`fields`* 規格所定義的 interval 欄位時，
未標記數量的解讀方式，取決於 *`fields`*。舉
例來說，`INTERVAL '1' YEAR` 會被讀作 1 年，而
`INTERVAL '1'` 則代表 1 秒。此外，
`fields` 規格所允許的最小有效欄位
「右側」的欄位值，會被悄悄捨棄。舉
例來說，寫 `INTERVAL '1 day 2:03:04' HOUR TO MINUTE`
會導致秒欄位被捨去，但日欄位不會。

依照 SQL 標準，某個 interval
值的所有欄位，都必須具有相同的正負號，因此開頭的負號，
會套用到所有欄位；舉例來說，interval 常值
`'-1 2:03:04'` 中的負號，
會同時套用到天以及時／分／秒的部分。
PostgreSQL 允許各欄位擁有不同的
正負號，並依照傳統，將文字表示法中的每個欄位，
視為各自帶有獨立正負號，因此在這個例子中，
時／分／秒的部分，會被視為正值。若
`IntervalStyle` 設為
`sql_standard`，則開頭的正負號，會被視為
套用到所有欄位（但僅限於沒有其他正負號出現的情況）。
否則，就會使用 PostgreSQL 傳統的
解讀方式。為避免歧義，建議在任何欄位為
負值時，為每個欄位附上明確的正負號。

在內部，`interval` 值是以三個
整數欄位儲存的：月、日與微秒。這些欄位
之所以分開保存，是因為一個月的天數會有所變化，
而若牽涉到日光節約時間的轉換，一天可能會有
23 或 25 個小時。使用其他單位的 interval
輸入字串，會被正規化為這種格式，
接著再以標準化的方式，重新建構為輸出，舉例來說：

```

SELECT '2 years 15 months 100 weeks 99 hours 123456789 milliseconds'::interval;
               interval
---------------------------------------
 3 years 3 mons 700 days 133:17:36.789
```

在這裡，被理解為「7 天」的週，
會以天數的形式獨立呈現（而非併入其他欄位）；
至於其他較大與較小的時間單位，則會被合併並正規化。

輸入的欄位值，可以帶有小數部分，
舉例來說 `'1.5
weeks'` 或 `'01:02:03.45'`。不過，
因為 `interval` 在內部只儲存整數欄位，
小數值必須被轉換為較小的
單位。大於月的單位，其小數部分，
會被四捨五入為整數個月，
舉例來說 `'1.5 years'`
會變成 `'1 year 6 mons'`。週
與日的小數部分，會被計算為整數個日
與微秒，假設每月 30 天、每天 24 小時，
舉例來說，
`'1.75 months'` 會變成 `1 mon 22 days
12:00:00`。在輸出中，只有秒才會
顯示為小數。

[表 8.17](datatype-datetime.md#DATATYPE-INTERVAL-INPUT-EXAMPLES) 展示了一些有效
`interval` 輸入的範例。

<a id="DATATYPE-INTERVAL-INPUT-EXAMPLES"></a>

**表 8.17. 時間區間輸入**

<table border="1" class="table" summary="時間區間輸入"><colgroup><col/><col/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">1-2</code></td><td>SQL 標準格式：1 年 2 個月</td></tr><tr><td><code class="literal">3 4:05:06</code></td><td>SQL 標準格式：3 天 4 小時 5 分 6 秒</td></tr><tr><td><code class="literal">1 year 2 months 3 days 4 hours 5 minutes 6 seconds</code></td><td>傳統 Postgres 格式：1 年 2 個月 3 天 4 小時 5 分 6 秒</td></tr><tr><td><code class="literal">P1Y2M3DT4H5M6S</code></td><td>ISO 8601 <span class="quote">「<span class="quote">帶指示符格式</span>」</span>：意義與上面相同</td></tr><tr><td><code class="literal">P0001-02-03T04:05:06</code></td><td>ISO 8601 <span class="quote">「<span class="quote">替代格式</span>」</span>：意義與上面相同</td></tr></tbody></table>

<br>

<a id="DATATYPE-INTERVAL-OUTPUT"></a>

### 8.5.5. 時間區間輸出 [#](#DATATYPE-INTERVAL-OUTPUT)

<a id="id-1.5.7.13.22.2"></a>

如前所述，PostgreSQL
以月、日與微秒，儲存 `interval` 值。
對於輸出而言，月欄位會除以 12，轉換為
年與月。日欄位則原樣顯示。
微秒欄位，會被轉換為時、分、秒，以及
秒的小數部分。因此，月、分、秒，永遠不會
顯示超過 0–11、0–59 與 0–59
的範圍，而所顯示的年、日與時欄位，
則可能相當大。（若希望將較大的日或
時值，轉移到下一個較高的欄位，
可以使用 [`justify_days`](../functions/functions-datetime.md#FUNCTION-JUSTIFY-DAYS)
與 [`justify_hours`](../functions/functions-datetime.md#FUNCTION-JUSTIFY-HOURS)
函式。）

interval 型別的輸出格式，可以使用指令
`SET intervalstyle`，
設定為 `sql_standard`、`postgres`、
`postgres_verbose` 或 `iso_8601`
這四種風格之一。
預設為 `postgres` 格式。
[表 8.18](datatype-datetime.md#INTERVAL-STYLE-OUTPUT-TABLE) 展示了每一種
輸出風格的範例。

若某個 interval 值符合標準的限制
（僅有年-月，或僅有日-時，
且正負分量不混用），
`sql_standard` 風格，會產生符合
SQL 標準對 interval 常值字串規格的輸出。
否則，輸出看起來，就像是一個標準的
年-月常值字串，後面接著一個日-時常值字串，
並加上明確的正負號，以消除混合正負號 interval 的歧義。

`postgres` 風格的輸出，
與 [DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數設為 `ISO` 時，
8.4 之前的 PostgreSQL 發行版本的輸出相符。

`postgres_verbose` 風格的輸出，
與 `DateStyle` 參數設為非 `ISO`
輸出時，8.4 之前的 PostgreSQL 發行版本的輸出相符。

`iso_8601` 風格的輸出，
與 ISO 8601 標準第 4.4.3.2 節中所描述的
「帶指示符格式」相符。

<a id="INTERVAL-STYLE-OUTPUT-TABLE"></a>

**表 8.18. 時間區間輸出風格範例**

<table border="1" class="table" summary="時間區間輸出樣式範例"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>風格規格</th><th>年-月時間區間</th><th>日-時時間區間</th><th>混合時間區間</th></tr></thead><tbody><tr><td><code class="literal">sql_standard</code></td><td>1-2</td><td>3 4:05:06</td><td>-1-2 +3 -4:05:06</td></tr><tr><td><code class="literal">postgres</code></td><td>1 year 2 mons</td><td>3 days 04:05:06</td><td>-1 year -2 mons +3 days -04:05:06</td></tr><tr><td><code class="literal">postgres_verbose</code></td><td>@ 1 year 2 mons</td><td>@ 3 days 4 hours 5 mins 6 secs</td><td>@ 1 year 2 mons -3 days 4 hours 5 mins 6 secs ago</td></tr><tr><td><code class="literal">iso_8601</code></td><td>P1Y2M</td><td>P3DT4H5M6S</td><td>P-1Y-2M3D​T-4H-5M-6S</td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
