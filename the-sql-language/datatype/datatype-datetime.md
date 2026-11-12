<a id="DATATYPE-DATETIME"></a>
## 8.5. 日期／時間型別 [#](#datatype-datetime) <a href="#datatype-datetime" id="datatype-datetime"></a>

[8.5.1. 日期／時間輸入](datatype-datetime/datatype-datetime-input.md#datatype-datetime-input)

[8.5.2. 日期／時間輸出](datatype-datetime/datatype-datetime-output.md#datatype-datetime-output)

[8.5.3. 時區](datatype-datetime.md#datatype-timezones)

[8.5.4. 時間區間輸入](datatype-datetime/datatype-interval-input.md#datatype-interval-input)

[8.5.5. 時間區間輸出](datatype-datetime/datatype-interval-output.md#datatype-interval-output)

<a id="id-1.5.7.13.2"></a><a id="id-1.5.7.13.3"></a><a id="id-1.5.7.13.4"></a><a id="id-1.5.7.13.5"></a><a id="id-1.5.7.13.6"></a><a id="id-1.5.7.13.7"></a><a id="id-1.5.7.13.8"></a><a id="id-1.5.7.13.9"></a><a id="id-1.5.7.13.10"></a><a id="id-1.5.7.13.11"></a>

PostgreSQL 支援
[表 8.9](datatype-datetime.md#datatype-datetime-table) 中所示的完整一組
SQL 日期與時間型別。這些資料型別上可用的運算，
說明於
[9.9 節](../functions/functions-datetime.md)。
日期是依照格里曆（Gregorian calendar）計算的，
即使是在該曆法引入之前的年份也是如此
（詳情請參閱[B.6 節](../../appendixes/datetime-appendix/datetime-units-history.md)）。

<a id="DATATYPE-DATETIME-TABLE"></a>

### 表 8.9. 日期／時間型別 [#](#datatype-datetime-table) <a href="#datatype-datetime-table" id="datatype-datetime-table"></a>

<table border="1" class="table" summary="日期/時間型別"><colgroup><col/><col/><col/><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>儲存大小</th><th>說明</th><th>最小值</th><th>最大值</th><th>解析度</th></tr></thead><tbody><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td>8 位元組</td><td>日期與時間（無時區）</td><td>4713 BC</td><td>294276 AD</td><td>1 微秒</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td>8 位元組</td><td>日期與時間，含時區</td><td>4713 BC</td><td>294276 AD</td><td>1 微秒</td></tr><tr><td><code class="type">date</code></td><td>4 位元組</td><td>日期（無時刻）</td><td>4713 BC</td><td>5874897 AD</td><td>1 天</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td>8 位元組</td><td>時刻（無日期）</td><td>00:00:00</td><td>24:00:00</td><td>1 微秒</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td>12 位元組</td><td>時刻（無日期），含時區</td><td>00:00:00+1559</td><td>24:00:00-1559</td><td>1 微秒</td></tr><tr><td><code class="type">interval [ <em class="replaceable"><code>fields</code></em> ] [ (<em class="replaceable"><code>p</code></em>) ]</code></td><td>16 位元組</td><td>時間區間</td><td>-178000000 年</td><td>178000000 年</td><td>1 微秒</td></tr></tbody></table>

<br>

### 注意 [#](#zhu-yi) <a href="#zhu-yi" id="zhu-yi"></a>

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

### 8.5.1. 日期／時間輸入 [#](#datatype-datetime-input) <a href="#datatype-datetime-input" id="datatype-datetime-input"></a>

完整內容請見 [8.5.1. 日期／時間輸入](datatype-datetime/datatype-datetime-input.md#datatype-datetime-input)。

### 8.5.2. 日期／時間輸出 [#](#datatype-datetime-output) <a href="#datatype-datetime-output" id="datatype-datetime-output"></a>

完整內容請見 [8.5.2. 日期／時間輸出](datatype-datetime/datatype-datetime-output.md#datatype-datetime-output)。

<a id="DATATYPE-TIMEZONES"></a>

### 8.5.3. 時區 [#](#datatype-timezones) <a href="#datatype-timezones" id="datatype-timezones"></a>

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

### 注意 [#](#zhu-yi-2) <a href="#zhu-yi-2" id="zhu-yi-2"></a>

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

### 8.5.4. 時間區間輸入 [#](#datatype-interval-input) <a href="#datatype-interval-input" id="datatype-interval-input"></a>

完整內容請見 [8.5.4. 時間區間輸入](datatype-datetime/datatype-interval-input.md#datatype-interval-input)。

### 8.5.5. 時間區間輸出 [#](#datatype-interval-output) <a href="#datatype-interval-output" id="datatype-interval-output"></a>

完整內容請見 [8.5.5. 時間區間輸出](datatype-datetime/datatype-interval-output.md#datatype-interval-output)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
