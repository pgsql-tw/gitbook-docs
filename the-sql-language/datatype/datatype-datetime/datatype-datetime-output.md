# 8.5.2. 日期／時間輸出

<a id="DATATYPE-DATETIME-OUTPUT"></a>

## 8.5.2. 日期／時間輸出 [#](#datatype-datetime-output) <a href="#datatype-datetime-output" id="datatype-datetime-output"></a>

<a id="id-1.5.7.13.19.2"></a><a id="id-1.5.7.13.19.3"></a>

日期／時間型別的輸出格式，可以設定為以下
四種風格之一：ISO 8601、
SQL（Ingres）、傳統的 POSTGRES
（Unix 日期格式），或
German（德式）。預設值
是 ISO 格式。（SQL 標準
要求使用 ISO 8601 格式。
「SQL」這個輸出格式的名稱，
是一段歷史上的巧合。）[表 8.14](#datatype-datetime-output-table) 展示了
每一種輸出風格的範例。`date` 型別與
`time` 型別的輸出，通常只會依照給定範例，
只顯示日期或時刻的部分。不過，
POSTGRES 風格會以 ISO 格式輸出僅含日期的值。

<a id="DATATYPE-DATETIME-OUTPUT-TABLE"></a>

### 表 8.14. 日期／時間輸出風格 [#](#datatype-datetime-output-table) <a href="#datatype-datetime-output-table" id="datatype-datetime-output-table"></a>

<table border="1" class="table" summary="日期/時間輸出樣式"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>風格規格</th><th>說明</th><th>範例</th></tr></thead><tbody><tr><td><code class="literal">ISO</code></td><td>ISO 8601，SQL 標準</td><td><code class="literal">1997-12-17 07:37:16-08</code></td></tr><tr><td><code class="literal">SQL</code></td><td>傳統風格</td><td><code class="literal">12/17/1997 07:37:16.00 PST</code></td></tr><tr><td><code class="literal">Postgres</code></td><td>原始風格</td><td><code class="literal">Wed Dec 17 07:37:16 1997 PST</code></td></tr><tr><td><code class="literal">German</code></td><td>地區風格</td><td><code class="literal">17.12.1997 07:37:16.00 PST</code></td></tr></tbody></table>

<br>

### 注意 [#](#zhu-yi-1) <a href="#zhu-yi-1" id="zhu-yi-1"></a>

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
請參閱[8.5.1 節](../datatype-datetime.md#datatype-datetime-input)。）
[表 8.15](#datatype-datetime-output2-table) 展示了一些範例。

<a id="DATATYPE-DATETIME-OUTPUT2-TABLE"></a>

### 表 8.15. 日期順序慣例 [#](#datatype-datetime-output2-table) <a href="#datatype-datetime-output2-table" id="datatype-datetime-output2-table"></a>

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
是取自 [TimeZone](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 執行時期參數
目前所選擇的 IANA 時區資料庫項目；它們
不受 [timezone_abbreviations](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) 設定的影響。

使用者可以透過
`SET datestyle` 指令、
`postgresql.conf` 組態檔中的
[DateStyle](../../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 參數，
或伺服器或用戶端上的
`PGDATESTYLE` 環境變數，
來選擇日期／時間風格。

格式化函式 `to_char`
（請參閱[9.8 節](../../functions/functions-formatting.md)），
也提供了一種更靈活的方式，
來格式化日期／時間輸出。

[返回 8.5. 日期／時間型別](../datatype-datetime.md#datatype-datetime)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-datetime.html)（原文版本：18.6；核對日期：2026-09-26）
