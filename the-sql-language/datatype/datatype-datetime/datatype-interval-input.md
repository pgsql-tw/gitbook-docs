# 8.5.4. 時間區間輸入

<a id="DATATYPE-INTERVAL-INPUT"></a>

## 8.5.4. 時間區間輸入 [#](#datatype-interval-input) <a href="#datatype-interval-input" id="datatype-interval-input"></a>

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
若 [IntervalStyle](../../../server-administration/runtime-config/runtime-config-client.md#GUC-INTERVALSTYLE) 設為
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
單位縮寫，列於[表 8.16](#datatype-interval-iso8601-units)中。單位
可以省略，也可以以任何順序指定，但小於
一天的單位，必須出現在 `T` 之後。特別是，
`M` 的意義，取決於它是出現在
`T` 之前還是之後。

<a id="DATATYPE-INTERVAL-ISO8601-UNITS"></a>

### 表 8.16. ISO 8601 時間區間單位縮寫 [#](#datatype-interval-iso8601-units) <a href="#datatype-interval-iso8601-units" id="datatype-interval-iso8601-units"></a>

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

[表 8.17](#datatype-interval-input-examples) 展示了一些有效
`interval` 輸入的範例。

<a id="DATATYPE-INTERVAL-INPUT-EXAMPLES"></a>

### 表 8.17. 時間區間輸入 [#](#datatype-interval-input-examples) <a href="#datatype-interval-input-examples" id="datatype-interval-input-examples"></a>

<table border="1" class="table" summary="時間區間輸入"><colgroup><col/><col/></colgroup><thead><tr><th>範例</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">1-2</code></td><td>SQL 標準格式：1 年 2 個月</td></tr><tr><td><code class="literal">3 4:05:06</code></td><td>SQL 標準格式：3 天 4 小時 5 分 6 秒</td></tr><tr><td><code class="literal">1 year 2 months 3 days 4 hours 5 minutes 6 seconds</code></td><td>傳統 Postgres 格式：1 年 2 個月 3 天 4 小時 5 分 6 秒</td></tr><tr><td><code class="literal">P1Y2M3DT4H5M6S</code></td><td>ISO 8601 <span class="quote">「<span class="quote">帶指示符格式</span>」</span>：意義與上面相同</td></tr><tr><td><code class="literal">P0001-02-03T04:05:06</code></td><td>ISO 8601 <span class="quote">「<span class="quote">替代格式</span>」</span>：意義與上面相同</td></tr></tbody></table>

<br>

[返回 8.5. 日期／時間型別](../datatype-datetime.md#datatype-datetime)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
