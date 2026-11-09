# 8.5.5. 時間區間輸出

<a id="DATATYPE-INTERVAL-OUTPUT"></a>

## 8.5.5. 時間區間輸出 [#](#datatype-interval-output) <a href="#datatype-interval-output" id="datatype-interval-output"></a>

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
可以使用 [`justify_days`](../../functions/functions-datetime.md#FUNCTION-JUSTIFY-DAYS)
與 [`justify_hours`](../../functions/functions-datetime.md#FUNCTION-JUSTIFY-HOURS)
函式。）

interval 型別的輸出格式，可以使用指令
`SET intervalstyle`，
設定為 `sql_standard`、`postgres`、
`postgres_verbose` 或 `iso_8601`
這四種風格之一。
預設為 `postgres` 格式。
[表 8.18](#interval-style-output-table) 展示了每一種
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
與 [DateStyle](../../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數設為 `ISO` 時，
8.4 之前的 PostgreSQL 發行版本的輸出相符。

`postgres_verbose` 風格的輸出，
與 `DateStyle` 參數設為非 `ISO`
輸出時，8.4 之前的 PostgreSQL 發行版本的輸出相符。

`iso_8601` 風格的輸出，
與 ISO 8601 標準第 4.4.3.2 節中所描述的
「帶指示符格式」相符。

<a id="INTERVAL-STYLE-OUTPUT-TABLE"></a>

### 表 8.18. 時間區間輸出風格範例 [#](#interval-style-output-table) <a href="#interval-style-output-table" id="interval-style-output-table"></a>

<table border="1" class="table" summary="時間區間輸出樣式範例"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>風格規格</th><th>年-月時間區間</th><th>日-時時間區間</th><th>混合時間區間</th></tr></thead><tbody><tr><td><code class="literal">sql_standard</code></td><td>1-2</td><td>3 4:05:06</td><td>-1-2 +3 -4:05:06</td></tr><tr><td><code class="literal">postgres</code></td><td>1 year 2 mons</td><td>3 days 04:05:06</td><td>-1 year -2 mons +3 days -04:05:06</td></tr><tr><td><code class="literal">postgres_verbose</code></td><td>@ 1 year 2 mons</td><td>@ 3 days 4 hours 5 mins 6 secs</td><td>@ 1 year 2 mons -3 days 4 hours 5 mins 6 secs ago</td></tr><tr><td><code class="literal">iso_8601</code></td><td>P1Y2M</td><td>P3DT4H5M6S</td><td>P-1Y-2M3D​T-4H-5M-6S</td></tr></tbody></table>

<br>

[返回 8.5. 日期／時間型別](../datatype-datetime.md#datatype-datetime)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
