<a id="FUNCTIONS-DATETIME"></a>

## 9.9. 日期／時間函式與運算子 [#](#FUNCTIONS-DATETIME)

[9.9.1. `EXTRACT`、`date_part`](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)

[9.9.2. `date_trunc`](functions-datetime.md#FUNCTIONS-DATETIME-TRUNC)

[9.9.3. `date_bin`](functions-datetime.md#FUNCTIONS-DATETIME-BIN)

[9.9.4. `AT TIME ZONE` 與 `AT LOCAL`](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)

[9.9.5. 目前日期／時間](functions-datetime.md#FUNCTIONS-DATETIME-CURRENT)

[9.9.6. 延遲執行](functions-datetime.md#FUNCTIONS-DATETIME-DELAY)

[表 9.33](functions-datetime.md#FUNCTIONS-DATETIME-TABLE) 列出了可用於處理日期／時間值的函式，細節則在後續各小節中說明。[表 9.32](functions-datetime.md#OPERATORS-DATETIME-TABLE) 說明了基本算術運算子（`+`、`*` 等）的行為。關於格式化函式，請參閱[第 9.8 節](functions-formatting.md)。你應該熟悉[第 8.5 節](../datatype/datatype-datetime.md)中關於日期／時間資料型別的背景資訊。

此外，日期／時間型別也可以使用[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子。日期與時間戳記（無論是否帶時區）彼此之間都可以比較，而時間（無論是否帶時區）與時間間隔則只能與相同資料型別的其他值比較。比較不帶時區的時間戳記與帶時區的時間戳記時，前者的值會被假設為以 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 組態參數所指定的時區表示，並被轉換為 UTC，以便與後者的值（它在內部已經是 UTC）比較。同樣地，將日期值與時間戳記比較時，日期值會被假設為代表 `TimeZone` 時區中的午夜。

下面所說明的所有接受 `time` 或 `timestamp` 輸入的函式與運算子，實際上都有兩種變化形式：一種接受 `time with time zone` 或 `timestamp with time zone`，另一種接受 `time without time zone` 或 `timestamp without time zone`。為了簡潔起見，這些變化形式不另外列出。此外，`+` 與 `*` 運算子都是成對的可交換形式（例如 `date` `+` `integer` 與 `integer` `+` `date` 兩者都有）；每一對我們只列出其中一個。

<a id="OPERATORS-DATETIME-TABLE"></a>

**表 9.32. 日期／時間運算子**

<table border="1" class="table" summary="Date/Time Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         運算子
        </p>
<p>
         說明
        </p>
<p>
         範例
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">+</code> <code class="type">integer</code>
         → <code class="returnvalue">date</code>
</p>
<p>
         將天數加到日期上
        </p>
<p>
<code class="literal">date '2001-09-28' + 7</code>
         → <code class="returnvalue">2001-10-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">+</code> <code class="type">interval</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         將時間間隔加到日期上
        </p>
<p>
<code class="literal">date '2001-09-28' + interval '1 hour'</code>
         → <code class="returnvalue">2001-09-28 01:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">+</code> <code class="type">time</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         將一天中的時間加到日期上
        </p>
<p>
<code class="literal">date '2001-09-28' + time '03:00'</code>
         → <code class="returnvalue">2001-09-28 03:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">interval</code> <code class="literal">+</code> <code class="type">interval</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間間隔相加
        </p>
<p>
<code class="literal">interval '1 day' + interval '1 hour'</code>
         → <code class="returnvalue">1 day 01:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp</code> <code class="literal">+</code> <code class="type">interval</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         將時間間隔加到時間戳記上
        </p>
<p>
<code class="literal">timestamp '2001-09-28 01:00' + interval '23 hours'</code>
         → <code class="returnvalue">2001-09-29 00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">time</code> <code class="literal">+</code> <code class="type">interval</code>
         → <code class="returnvalue">time</code>
</p>
<p>
         將時間間隔加到時間上
        </p>
<p>
<code class="literal">time '01:00' + interval '3 hours'</code>
         → <code class="returnvalue">04:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <code class="type">interval</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間間隔取負
        </p>
<p>
<code class="literal">- interval '23 hours'</code>
         → <code class="returnvalue">-23:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">-</code> <code class="type">date</code>
         → <code class="returnvalue">integer</code>
</p>
<p>
         將日期相減，產生經過的天數
        </p>
<p>
<code class="literal">date '2001-10-01' - date '2001-09-28'</code>
         → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">-</code> <code class="type">integer</code>
         → <code class="returnvalue">date</code>
</p>
<p>
         從日期減去天數
        </p>
<p>
<code class="literal">date '2001-10-01' - 7</code>
         → <code class="returnvalue">2001-09-24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">date</code> <code class="literal">-</code> <code class="type">interval</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         從日期減去時間間隔
        </p>
<p>
<code class="literal">date '2001-09-28' - interval '1 hour'</code>
         → <code class="returnvalue">2001-09-27 23:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">time</code> <code class="literal">-</code> <code class="type">time</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間相減
        </p>
<p>
<code class="literal">time '05:00' - time '03:00'</code>
         → <code class="returnvalue">02:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">time</code> <code class="literal">-</code> <code class="type">interval</code>
         → <code class="returnvalue">time</code>
</p>
<p>
         從時間減去時間間隔
        </p>
<p>
<code class="literal">time '05:00' - interval '2 hours'</code>
         → <code class="returnvalue">03:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp</code> <code class="literal">-</code> <code class="type">interval</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         從時間戳記減去時間間隔
        </p>
<p>
<code class="literal">timestamp '2001-09-28 23:00' - interval '23 hours'</code>
         → <code class="returnvalue">2001-09-28 00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">interval</code> <code class="literal">-</code> <code class="type">interval</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間間隔相減
        </p>
<p>
<code class="literal">interval '1 day' - interval '1 hour'</code>
         → <code class="returnvalue">1 day -01:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp</code> <code class="literal">-</code> <code class="type">timestamp</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間戳記相減（將 24 小時的時間間隔轉換為天，類似於 <a class="link" href="functions-datetime.md#FUNCTION-JUSTIFY-HOURS"><code class="function">justify_hours()</code></a>）
        </p>
<p>
<code class="literal">timestamp '2001-09-29 03:00' - timestamp '2001-07-27 12:00'</code>
         → <code class="returnvalue">63 days 15:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">interval</code> <code class="literal">*</code> <code class="type">double precision</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間間隔乘以純量
        </p>
<p>
<code class="literal">interval '1 second' * 900</code>
         → <code class="returnvalue">00:15:00</code>
</p>
<p>
<code class="literal">interval '1 day' * 21</code>
         → <code class="returnvalue">21 days</code>
</p>
<p>
<code class="literal">interval '1 hour' * 3.5</code>
         → <code class="returnvalue">03:30:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">interval</code> <code class="literal">/</code> <code class="type">double precision</code>
         → <code class="returnvalue">interval</code>
</p>
<p>
         將時間間隔除以純量
        </p>
<p>
<code class="literal">interval '1 hour' / 1.5</code>
         → <code class="returnvalue">00:40:00</code>
</p></td></tr></tbody></table>

<br><a id="FUNCTIONS-DATETIME-TABLE"></a>

**表 9.33. 日期／時間函式**

<table border="1" class="table" summary="Date/Time Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         函式
        </p>
<p>
         說明
        </p>
<p>
         範例
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.1.1.1.1"></a>
<code class="function">age</code> ( <code class="type">timestamp</code>, <code class="type">timestamp</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         將引數相減，產生一個使用年與月而不只是天數的<span class="quote">“<span class="quote">符號式</span>”</span>結果
        </p>
<p>
<code class="literal">age(timestamp '2001-04-10', timestamp '1957-06-13')</code>
         → <code class="returnvalue">43 years 9 mons 27 days</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">age</code> ( <code class="type">timestamp</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         從 <code class="function">current_date</code>（午夜）減去引數
        </p>
<p>
<code class="literal">age(timestamp '1957-06-13')</code>
         → <code class="returnvalue">62 years 6 mons 10 days</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.3.1.1.1"></a>
<code class="function">clock_timestamp</code> ( )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（在陳述式執行期間會改變）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">clock_timestamp()</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.4.1.1.1"></a>
<code class="function">current_date</code>
         → <code class="returnvalue">date</code>
</p>
<p>
         目前的日期；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">current_date</code>
         → <code class="returnvalue">2019-12-23</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.5.1.1.1"></a>
<code class="function">current_time</code>
         → <code class="returnvalue">time with time zone</code>
</p>
<p>
         一天中的目前時間；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">current_time</code>
         → <code class="returnvalue">14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">current_time</code> ( <code class="type">integer</code> )
         → <code class="returnvalue">time with time zone</code>
</p>
<p>
         一天中的目前時間，精度有限；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">current_time(2)</code>
         → <code class="returnvalue">14:39:53.66-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.7.1.1.1"></a>
<code class="function">current_timestamp</code>
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">current_timestamp</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">current_timestamp</code> ( <code class="type">integer</code> )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間），精度有限；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">current_timestamp(0)</code>
         → <code class="returnvalue">2019-12-23 14:39:53-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.9.1.1.1"></a>
<code class="function">date_add</code> ( <code class="type">timestamp with time zone</code>, <code class="type">interval</code> [<span class="optional">, <code class="type">text</code> </span>] )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         將 <code class="type">interval</code> 加到 <code class="type">timestamp with time
         zone</code> 上，並依照第三個引數所指定的時區（如果省略，則依照目前的 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> 設定）計算一天中的時間與日光節約時間的調整。雙引數形式等同於 <code class="type">timestamp with
         time zone</code> <code class="literal">+</code> <code class="type">interval</code> 運算子。
        </p>
<p>
<code class="literal">date_add('2021-10-31 00:00:00+02'::timestamptz, '1 day'::interval, 'Europe/Warsaw')</code>
         → <code class="returnvalue">2021-10-31 23:00:00+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">date_bin</code> ( <code class="type">interval</code>, <code class="type">timestamp</code>, <code class="type">timestamp</code> )
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         將輸入分箱到與指定原點對齊的指定時間間隔中；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-BIN">第 9.9.3 節</a>
</p>
<p>
<code class="literal">date_bin('15 minutes', timestamp '2001-02-16 20:38:40', timestamp '2001-02-16 20:05:00')</code>
         → <code class="returnvalue">2001-02-16 20:35:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.11.1.1.1"></a>
<code class="function">date_part</code> ( <code class="type">text</code>, <code class="type">timestamp</code> )
         → <code class="returnvalue">double precision</code>
</p>
<p>
         取得時間戳記的子欄位（等同於 <code class="function">extract</code>）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT">第 9.9.1 節</a>
</p>
<p>
<code class="literal">date_part('hour', timestamp '2001-02-16 20:38:40')</code>
         → <code class="returnvalue">20</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">date_part</code> ( <code class="type">text</code>, <code class="type">interval</code> )
         → <code class="returnvalue">double precision</code>
</p>
<p>
         取得時間間隔的子欄位（等同於 <code class="function">extract</code>）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT">第 9.9.1 節</a>
</p>
<p>
<code class="literal">date_part('month', interval '2 years 3 months')</code>
         → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.13.1.1.1"></a>
<code class="function">date_subtract</code> ( <code class="type">timestamp with time zone</code>, <code class="type">interval</code> [<span class="optional">, <code class="type">text</code> </span>] )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         將 <code class="type">interval</code> 從 <code class="type">timestamp with time
         zone</code> 中減去，並依照第三個引數所指定的時區（如果省略，則依照目前的 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> 設定）計算一天中的時間與日光節約時間的調整。雙引數形式等同於 <code class="type">timestamp with
         time zone</code> <code class="literal">-</code> <code class="type">interval</code> 運算子。
        </p>
<p>
<code class="literal">date_subtract('2021-11-01 00:00:00+01'::timestamptz, '1 day'::interval, 'Europe/Warsaw')</code>
         → <code class="returnvalue">2021-10-30 22:00:00+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.14.1.1.1"></a>
<code class="function">date_trunc</code> ( <code class="type">text</code>, <code class="type">timestamp</code> )
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         截斷到指定的精度；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC">第 9.9.2 節</a>
</p>
<p>
<code class="literal">date_trunc('hour', timestamp '2001-02-16 20:38:40')</code>
         → <code class="returnvalue">2001-02-16 20:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">date_trunc</code> ( <code class="type">text</code>, <code class="type">timestamp with time zone</code>, <code class="type">text</code> )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         在指定的時區中截斷到指定的精度；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC">第 9.9.2 節</a>
</p>
<p>
<code class="literal">date_trunc('day', timestamptz '2001-02-16 20:38:40+00', 'Australia/Sydney')</code>
         → <code class="returnvalue">2001-02-16 13:00:00+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">date_trunc</code> ( <code class="type">text</code>, <code class="type">interval</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         截斷到指定的精度；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC">第 9.9.2 節</a>
</p>
<p>
<code class="literal">date_trunc('hour', interval '2 days 3 hours 40 minutes')</code>
         → <code class="returnvalue">2 days 03:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.17.1.1.1"></a>
<code class="function">extract</code> ( <em class="parameter"><code>field</code></em> <code class="literal">from</code> <code class="type">timestamp</code> )
         → <code class="returnvalue">numeric</code>
</p>
<p>
         取得時間戳記的子欄位；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT">第 9.9.1 節</a>
</p>
<p>
<code class="literal">extract(hour from timestamp '2001-02-16 20:38:40')</code>
         → <code class="returnvalue">20</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">extract</code> ( <em class="parameter"><code>field</code></em> <code class="literal">from</code> <code class="type">interval</code> )
         → <code class="returnvalue">numeric</code>
</p>
<p>
         取得時間間隔的子欄位；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT">第 9.9.1 節</a>
</p>
<p>
<code class="literal">extract(month from interval '2 years 3 months')</code>
         → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.19.1.1.1"></a>
<code class="function">isfinite</code> ( <code class="type">date</code> )
         → <code class="returnvalue">boolean</code>
</p>
<p>
         檢驗是否為有限的日期（不是 +/-infinity）
        </p>
<p>
<code class="literal">isfinite(date '2001-02-16')</code>
         → <code class="returnvalue">true</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">isfinite</code> ( <code class="type">timestamp</code> )
         → <code class="returnvalue">boolean</code>
</p>
<p>
         檢驗是否為有限的時間戳記（不是 +/-infinity）
        </p>
<p>
<code class="literal">isfinite(timestamp 'infinity')</code>
         → <code class="returnvalue">false</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">isfinite</code> ( <code class="type">interval</code> )
         → <code class="returnvalue">boolean</code>
</p>
<p>
         檢驗是否為有限的時間間隔（不是 +/-infinity）
        </p>
<p>
<code class="literal">isfinite(interval '4 hours')</code>
         → <code class="returnvalue">true</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-JUSTIFY-DAYS"></a>
<code class="function">justify_days</code> ( <code class="type">interval</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         調整時間間隔，將 30 天的時間區段轉換為月
        </p>
<p>
<code class="literal">justify_days(interval '1 year 65 days')</code>
         → <code class="returnvalue">1 year 2 mons 5 days</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-JUSTIFY-HOURS"></a>
<code class="function">justify_hours</code> ( <code class="type">interval</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         調整時間間隔，將 24 小時的時間區段轉換為天
        </p>
<p>
<code class="literal">justify_hours(interval '50 hours 10 minutes')</code>
         → <code class="returnvalue">2 days 02:10:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.24.1.1.1"></a>
<code class="function">justify_interval</code> ( <code class="type">interval</code> )
         → <code class="returnvalue">interval</code>
</p>
<p>
         使用 <code class="function">justify_days</code> 與 <code class="function">justify_hours</code> 調整時間間隔，並額外進行正負號的調整
        </p>
<p>
<code class="literal">justify_interval(interval '1 mon -1 hour')</code>
         → <code class="returnvalue">29 days 23:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.25.1.1.1"></a>
<code class="function">localtime</code>
         → <code class="returnvalue">time</code>
</p>
<p>
         一天中的目前時間；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">localtime</code>
         → <code class="returnvalue">14:39:53.662522</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">localtime</code> ( <code class="type">integer</code> )
         → <code class="returnvalue">time</code>
</p>
<p>
         一天中的目前時間，精度有限；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">localtime(0)</code>
         → <code class="returnvalue">14:39:53</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.27.1.1.1"></a>
<code class="function">localtimestamp</code>
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">localtimestamp</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">localtimestamp</code> ( <code class="type">integer</code> )
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間），精度有限；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">localtimestamp(2)</code>
         → <code class="returnvalue">2019-12-23 14:39:53.66</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.29.1.1.1"></a>
<code class="function">make_date</code> ( <em class="parameter"><code>year</code></em> <code class="type">int</code>,
         <em class="parameter"><code>month</code></em> <code class="type">int</code>,
         <em class="parameter"><code>day</code></em> <code class="type">int</code> )
         → <code class="returnvalue">date</code>
</p>
<p>
         從年、月、日欄位建立日期（負的年份表示西元前）
        </p>
<p>
<code class="literal">make_date(2013, 7, 15)</code>
         → <code class="returnvalue">2013-07-15</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature"><a class="indexterm" id="id-1.5.8.15.6.2.2.30.1.1.1"></a>
<code class="function">make_interval</code> ( [<span class="optional"> <em class="parameter"><code>years</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>months</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>weeks</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>days</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>hours</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>mins</code></em> <code class="type">int</code>
         [<span class="optional">, <em class="parameter"><code>secs</code></em> <code class="type">double precision</code>
</span>]</span>]</span>]</span>]</span>]</span>]</span>] )
         → <code class="returnvalue">interval</code>
</p>
<p>
         從年、月、週、日、時、分與秒欄位建立時間間隔，每個欄位都可以預設為零
        </p>
<p>
<code class="literal">make_interval(days =&gt; 10)</code>
         → <code class="returnvalue">10 days</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.31.1.1.1"></a>
<code class="function">make_time</code> ( <em class="parameter"><code>hour</code></em> <code class="type">int</code>,
         <em class="parameter"><code>min</code></em> <code class="type">int</code>,
         <em class="parameter"><code>sec</code></em> <code class="type">double precision</code> )
         → <code class="returnvalue">time</code>
</p>
<p>
         從時、分與秒欄位建立時間
        </p>
<p>
<code class="literal">make_time(8, 15, 23.5)</code>
         → <code class="returnvalue">08:15:23.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.32.1.1.1"></a>
<code class="function">make_timestamp</code> ( <em class="parameter"><code>year</code></em> <code class="type">int</code>,
         <em class="parameter"><code>month</code></em> <code class="type">int</code>,
         <em class="parameter"><code>day</code></em> <code class="type">int</code>,
         <em class="parameter"><code>hour</code></em> <code class="type">int</code>,
         <em class="parameter"><code>min</code></em> <code class="type">int</code>,
         <em class="parameter"><code>sec</code></em> <code class="type">double precision</code> )
         → <code class="returnvalue">timestamp</code>
</p>
<p>
         從年、月、日、時、分與秒欄位建立時間戳記（負的年份表示西元前）
        </p>
<p>
<code class="literal">make_timestamp(2013, 7, 15, 8, 15, 23.5)</code>
         → <code class="returnvalue">2013-07-15 08:15:23.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.33.1.1.1"></a>
<code class="function">make_timestamptz</code> ( <em class="parameter"><code>year</code></em> <code class="type">int</code>,
         <em class="parameter"><code>month</code></em> <code class="type">int</code>,
         <em class="parameter"><code>day</code></em> <code class="type">int</code>,
         <em class="parameter"><code>hour</code></em> <code class="type">int</code>,
         <em class="parameter"><code>min</code></em> <code class="type">int</code>,
         <em class="parameter"><code>sec</code></em> <code class="type">double precision</code>
         [<span class="optional">, <em class="parameter"><code>timezone</code></em> <code class="type">text</code> </span>] )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         從年、月、日、時、分與秒欄位建立帶時區的時間戳記（負的年份表示西元前）。如果沒有指定 <em class="parameter"><code>timezone</code></em>，就使用目前的時區；範例假設工作階段時區為 <code class="literal">Europe/London</code>
</p>
<p>
<code class="literal">make_timestamptz(2013, 7, 15, 8, 15, 23.5)</code>
         → <code class="returnvalue">2013-07-15 08:15:23.5+01</code>
</p>
<p>
<code class="literal">make_timestamptz(2013, 7, 15, 8, 15, 23.5, 'America/New_York')</code>
         → <code class="returnvalue">2013-07-15 13:15:23.5+01</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.34.1.1.1"></a>
<code class="function">now</code> ( )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">now()</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.35.1.1.1"></a>
<code class="function">statement_timestamp</code> ( )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（目前陳述式的開始時間）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">statement_timestamp()</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.36.1.1.1"></a>
<code class="function">timeofday</code> ( )
         → <code class="returnvalue">text</code>
</p>
<p>
         目前的日期與時間（類似 <code class="function">clock_timestamp</code>，但以 <code class="type">text</code> 字串表示）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">timeofday()</code>
         → <code class="returnvalue">Mon Dec 23 14:39:53.662522 2019 EST</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.37.1.1.1"></a>
<code class="function">transaction_timestamp</code> ( )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         目前的日期與時間（目前交易的開始時間）；請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT">第 9.9.5 節</a>
</p>
<p>
<code class="literal">transaction_timestamp()</code>
         → <code class="returnvalue">2019-12-23 14:39:53.662522-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.15.6.2.2.38.1.1.1"></a>
<code class="function">to_timestamp</code> ( <code class="type">double precision</code> )
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         將 Unix epoch（自 1970-01-01 00:00:00+00 起的秒數）轉換為帶時區的時間戳記
        </p>
<p>
<code class="literal">to_timestamp(1284352323)</code>
         → <code class="returnvalue">2010-09-13 04:32:03+00</code>
</p></td></tr></tbody></table>

<br>

<a id="id-1.5.8.15.7.1"></a>
除了這些函式之外，也支援 SQL 的 `OVERLAPS` 運算子：

```

(start1, end1) OVERLAPS (start2, end2)
(start1, length1) OVERLAPS (start2, length2)
```

當兩個時間區段（由其端點定義）重疊時，這個運算式會產生 true；不重疊時則產生 false。端點可以指定為成對的日期、時間或時間戳記；或者指定為一個日期、時間或時間戳記，後面接著一個時間間隔。提供一對值時，可以先寫開始或結束；`OVERLAPS` 會自動將該對值中較早的值當作開始。每個時間區段都被視為代表半開區間 *`start`* `<=` *`time`* `<` *`end`*，除非 *`start`* 與 *`end`* 相等，在這種情況下它代表那單一個時間點。這表示，例如兩個只有一個端點相同的時間區段並不重疊。

```

SELECT (DATE '2001-02-16', DATE '2001-12-21') OVERLAPS
       (DATE '2001-10-30', DATE '2002-10-30');
Result: true
SELECT (DATE '2001-02-16', INTERVAL '100 days') OVERLAPS
       (DATE '2001-10-30', DATE '2002-10-30');
Result: false
SELECT (DATE '2001-10-29', DATE '2001-10-30') OVERLAPS
       (DATE '2001-10-30', DATE '2001-10-31');
Result: false
SELECT (DATE '2001-10-30', DATE '2001-10-30') OVERLAPS
       (DATE '2001-10-30', DATE '2001-10-31');
Result: true
```

將 `interval` 值加到 `timestamp` 或 `timestamp with time zone` 值（或從中減去 `interval` 值）時，會依序處理 `interval` 值的月、日與微秒欄位。首先，非零的月欄位會將時間戳記的日期推進或後退指定的月數，並保持月中的日期不變，除非那會超過新月份的最後一天，在這種情況下會使用該月的最後一天。（例如，3 月 31 日加 1 個月會變成 4 月 30 日，但 3 月 31 日加 2 個月會變成 5 月 31 日。）接著，日欄位會將時間戳記的日期推進或後退指定的天數。在這兩個步驟中，一天中的當地時間都保持不變。最後，如果有非零的微秒欄位，就會按字面加上或減去。在承認日光節約時間的時區中，對 `timestamp with time zone` 值進行算術運算時，這表示加上或減去（比方說）`interval '1 day'`，與加上或減去 `interval '24 hours'` 的結果不一定相同。例如，在工作階段時區設為 `America/Denver` 的情況下：

```

SELECT timestamp with time zone '2005-04-02 12:00:00-07' + interval '1 day';
Result: 2005-04-03 12:00:00-06
SELECT timestamp with time zone '2005-04-02 12:00:00-07' + interval '24 hours';
Result: 2005-04-03 13:00:00-06
```

之所以會這樣，是因為在 `America/Denver` 時區中，`2005-04-03 02:00:00` 時發生了日光節約時間的轉換，使得有一個小時被跳過了。

請注意，由於不同的月份有不同的天數，`age` 所回傳的 `months` 欄位可能會有歧義。PostgreSQL 的做法是在計算不足一個月的部分時，使用兩個日期中較早那個日期的月份。例如，`age('2004-06-01', '2004-04-30')` 使用四月，產生 `1 mon 1 day`；而如果使用五月，則會產生 `1 mon 2 days`，因為五月有 31 天，而四月只有 30 天。

日期與時間戳記的減法也可能很複雜。一種概念上簡單的減法做法，是使用 `EXTRACT(EPOCH FROM ...)` 將每個值轉換為秒數，然後將結果相減；這會產生兩個值之間相差的*秒數*。這會考量每個月的天數、時區變更以及日光節約時間的調整。使用「`-`」運算子對日期或時間戳記值進行減法，會回傳兩個值之間相差的天數（24 小時）與時／分／秒，並進行相同的調整。`age` 函式會回傳年、月、日與時／分／秒，它會逐欄位進行減法，然後再針對負的欄位值進行調整。下列查詢說明了這些做法之間的差異。範例結果是在 `timezone = 'US/Eastern'` 的情況下產生的；所使用的兩個日期之間有一次日光節約時間的轉換：

```

SELECT EXTRACT(EPOCH FROM timestamptz '2013-07-01 12:00:00') -
       EXTRACT(EPOCH FROM timestamptz '2013-03-01 12:00:00');
Result: 10537200.000000
SELECT (EXTRACT(EPOCH FROM timestamptz '2013-07-01 12:00:00') -
        EXTRACT(EPOCH FROM timestamptz '2013-03-01 12:00:00'))
        / 60 / 60 / 24;
Result: 121.9583333333333333
SELECT timestamptz '2013-07-01 12:00:00' - timestamptz '2013-03-01 12:00:00';
Result: 121 days 23:00:00
SELECT age(timestamptz '2013-07-01 12:00:00', timestamptz '2013-03-01 12:00:00');
Result: 4 mons
```

<a id="FUNCTIONS-DATETIME-EXTRACT"></a>

### 9.9.1. `EXTRACT`、`date_part` [#](#FUNCTIONS-DATETIME-EXTRACT)

<a id="id-1.5.8.15.13.2"></a><a id="id-1.5.8.15.13.3"></a>

```

EXTRACT(field FROM source)
```

`extract` 函式會從日期／時間值中取出年或小時等子欄位。*`source`* 必須是 `timestamp`、`date`、`time` 或 `interval` 型別的值運算式。（時間戳記與時間可以帶時區，也可以不帶。）*`field`* 是一個識別符號或字串，用來選擇要從來源值中取出哪一個欄位。並非所有欄位對每種輸入資料型別都有效；例如，小於一天的欄位無法從 `date` 中取出，而一天或以上的欄位則無法從 `time` 中取出。`extract` 函式回傳 `numeric` 型別的值。

以下是有效的欄位名稱：

`century`
:   世紀；對於 `interval` 值，則是年欄位除以 100

    ```

    SELECT EXTRACT(CENTURY FROM TIMESTAMP '2000-12-16 12:21:13');
    Result: 20
    SELECT EXTRACT(CENTURY FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 21
    SELECT EXTRACT(CENTURY FROM DATE '0001-01-01 AD');
    Result: 1
    SELECT EXTRACT(CENTURY FROM DATE '0001-12-31 BC');
    Result: -1
    SELECT EXTRACT(CENTURY FROM INTERVAL '2001 years');
    Result: 20
    ```

`day`
:   月中的第幾天（1–31）；對於 `interval` 值，則是天數

    ```

    SELECT EXTRACT(DAY FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 16
    SELECT EXTRACT(DAY FROM INTERVAL '40 days 1 minute');
    Result: 40
    ```

`decade`
:   年欄位除以 10

    ```

    SELECT EXTRACT(DECADE FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 200
    ```

`dow`
:   星期幾，從星期日（`0`）到星期六（`6`）

    ```

    SELECT EXTRACT(DOW FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 5
    ```

    請注意，`extract` 的星期編號與 `to_char(..., 'D')` 函式的不同。

`doy`
:   一年中的第幾天（1–365/366）

    ```

    SELECT EXTRACT(DOY FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 47
    ```

`epoch`
:   對於 `timestamp with time zone` 值，是自 1970-01-01 00:00:00 UTC 起的秒數（之前的時間戳記為負數）；對於 `date` 與 `timestamp` 值，是自 1970-01-01 00:00:00 起的名目秒數，不考慮時區或日光節約時間規則；對於 `interval` 值，則是該時間間隔的總秒數

    ```

    SELECT EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40.12-08');
    Result: 982384720.120000
    SELECT EXTRACT(EPOCH FROM TIMESTAMP '2001-02-16 20:38:40.12');
    Result: 982355920.120000
    SELECT EXTRACT(EPOCH FROM INTERVAL '5 days 3 hours');
    Result: 442800.000000
    ```

    你可以使用 `to_timestamp` 將 epoch 值轉換回 `timestamp with time zone`：

    ```

    SELECT to_timestamp(982384720.12);
    Result: 2001-02-17 04:38:40.12+00
    ```

    請注意，對從 `date` 或 `timestamp` 值取出的 epoch 套用 `to_timestamp`，可能會產生誤導性的結果：結果實際上會假設原始值是以 UTC 給定的，而事實不一定如此。

`hour`
:   小時欄位（在時間戳記中為 0–23，在時間間隔中則不受限制）

    ```

    SELECT EXTRACT(HOUR FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 20
    ```

`isodow`
:   星期幾，從星期一（`1`）到星期日（`7`）

    ```

    SELECT EXTRACT(ISODOW FROM TIMESTAMP '2001-02-18 20:38:40');
    Result: 7
    ```

    除了星期日之外，這與 `dow` 相同。這符合 ISO 8601 的星期編號。

`isoyear`
:   該日期所屬的 ISO 8601 週編號年

    ```

    SELECT EXTRACT(ISOYEAR FROM DATE '2006-01-01');
    Result: 2005
    SELECT EXTRACT(ISOYEAR FROM DATE '2006-01-02');
    Result: 2006
    ```

    每個 ISO 8601 週編號年都從包含 1 月 4 日那一週的星期一開始，因此在一月初或十二月底，ISO 年可能會與格里曆年不同。更多資訊請參閱 `week` 欄位。

`julian`
:   對應於該日期或時間戳記的*儒略日*（Julian Date）。不是當地午夜的時間戳記會產生帶小數的值。更多資訊請參閱[第 B.7 節](../../appendixes/datetime-appendix/datetime-julian-dates.md)。

    ```

    SELECT EXTRACT(JULIAN FROM DATE '2006-01-01');
    Result: 2453737
    SELECT EXTRACT(JULIAN FROM TIMESTAMP '2006-01-01 12:00');
    Result: 2453737.50000000000000000000
    ```

`microseconds`
:   秒欄位（包括小數部分）乘以 1 000 000；請注意，這包括完整的秒數

    ```

    SELECT EXTRACT(MICROSECONDS FROM TIME '17:12:28.5');
    Result: 28500000
    ```

`millennium`
:   千禧年；對於 `interval` 值，則是年欄位除以 1000

    ```

    SELECT EXTRACT(MILLENNIUM FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 3
    SELECT EXTRACT(MILLENNIUM FROM INTERVAL '2001 years');
    Result: 2
    ```

    1900 年代屬於第二個千禧年。第三個千禧年從 2001 年 1 月 1 日開始。

`milliseconds`
:   秒欄位（包括小數部分）乘以 1000。請注意，這包括完整的秒數。

    ```

    SELECT EXTRACT(MILLISECONDS FROM TIME '17:12:28.5');
    Result: 28500.000
    ```

`minute`
:   分鐘欄位（0–59）

    ```

    SELECT EXTRACT(MINUTE FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 38
    ```

`month`
:   一年中的月份編號（1–12）；對於 `interval` 值，則是月數除以 12 的餘數（0–11）

    ```

    SELECT EXTRACT(MONTH FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 2
    SELECT EXTRACT(MONTH FROM INTERVAL '2 years 3 months');
    Result: 3
    SELECT EXTRACT(MONTH FROM INTERVAL '2 years 13 months');
    Result: 1
    ```

`quarter`
:   該日期所在的季（1–4）；對於 `interval` 值，則是月欄位除以 3 再加 1

    ```

    SELECT EXTRACT(QUARTER FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 1
    SELECT EXTRACT(QUARTER FROM INTERVAL '1 year 6 months');
    Result: 3
    ```

`second`
:   秒欄位，包括任何小數部分的秒數

    ```

    SELECT EXTRACT(SECOND FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 40.000000
    SELECT EXTRACT(SECOND FROM TIME '17:12:28.5');
    Result: 28.500000
    ```

`timezone`
:   相對於 UTC 的時區位移，以秒為單位。正值對應於 UTC 以東的時區，負值對應於 UTC 以西的時區。（嚴格來說，PostgreSQL 並不使用 UTC，因為它不處理閏秒。）

`timezone_hour`
:   時區位移的小時部分

`timezone_minute`
:   時區位移的分鐘部分

`week`
:   一年中 ISO 8601 週編號週的編號。依照定義，ISO 週從星期一開始，而一年的第一週包含該年的 1 月 4 日。換句話說，一年中的第一個星期四位於該年的第 1 週。

    在 ISO 週編號系統中，一月初的日期有可能屬於前一年的第 52 或第 53 週，而十二月底的日期也有可能屬於下一年的第一週。例如，`2005-01-01` 屬於 2004 年的第 53 週，`2006-01-01` 屬於 2005 年的第 52 週，而 `2012-12-31` 則屬於 2013 年的第一週。建議將 `isoyear` 欄位與 `week` 一起使用，以得到一致的結果。

    對於 `interval` 值，週欄位就是整數天數除以 7。

    ```

    SELECT EXTRACT(WEEK FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 7
    SELECT EXTRACT(WEEK FROM INTERVAL '13 days 24 hours');
    Result: 1
    ```

`year`
:   年欄位。請記住，並沒有 `0 AD`（西元 0 年），因此從 `AD`（西元）年份減去 `BC`（西元前）年份時應該小心。

    ```

    SELECT EXTRACT(YEAR FROM TIMESTAMP '2001-02-16 20:38:40');
    Result: 2001
    ```

處理 `interval` 值時，`extract` 函式所產生的欄位值，會與時間間隔輸出函式所使用的解讀方式一致。如果一開始使用的是未正規化的時間間隔表示，就可能產生令人意外的結果，例如：

```

SELECT INTERVAL '80 minutes';
Result: 01:20:00
SELECT EXTRACT(MINUTES FROM INTERVAL '80 minutes');
Result: 20
```

### 注意

當輸入值為 +/-Infinity 時，對於單調遞增的欄位（`timestamp` 輸入的 `epoch`、`julian`、`year`、`isoyear`、`decade`、`century` 與 `millennium`；`interval` 輸入的 `epoch`、`hour`、`day`、`year`、`decade`、`century` 與 `millennium`），`extract` 會回傳 +/-Infinity。對於其他欄位，則回傳 NULL。9.6 之前的 PostgreSQL 版本，對於所有無限的輸入都回傳零。

`extract` 函式主要用於計算處理。關於將日期／時間值格式化以供顯示，請參閱[第 9.8 節](functions-formatting.md)。

`date_part` 函式是仿照傳統 Ingres 中與 SQL 標準函式 `extract` 等價的函式而設計的：

```

date_part('field', source)
```

請注意，這裡的 *`field`* 參數必須是字串值，而不是名稱。`date_part` 的有效欄位名稱與 `extract` 相同。基於歷史原因，`date_part` 函式回傳 `double precision` 型別的值。這在某些用途中可能會導致精度損失。建議改用 `extract`。

```

SELECT date_part('day', TIMESTAMP '2001-02-16 20:38:40');
Result: 16
SELECT date_part('hour', INTERVAL '4 hours 3 minutes');
Result: 4
```

<a id="FUNCTIONS-DATETIME-TRUNC"></a>

### 9.9.2. `date_trunc` [#](#FUNCTIONS-DATETIME-TRUNC)

<a id="id-1.5.8.15.14.2"></a>

函式 `date_trunc` 在概念上類似於用於數字的 `trunc` 函式。

```

date_trunc(field, source [, time_zone ])
```

*`source`* 是 `timestamp`、`timestamp with time zone` 或 `interval` 型別的值運算式。（`date` 與 `time` 型別的值，會分別自動轉換為 `timestamp` 或 `interval`。）*`field`* 選擇要將輸入值截斷到哪一個精度。回傳值同樣是 `timestamp`、`timestamp with time zone` 或 `interval` 型別，而且所有比所選欄位更不重要的欄位都會被設為零（對於日與月則設為一）。

*`field`* 的有效值為：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">microseconds</code></td></tr><tr><td><code class="literal">milliseconds</code></td></tr><tr><td><code class="literal">second</code></td></tr><tr><td><code class="literal">minute</code></td></tr><tr><td><code class="literal">hour</code></td></tr><tr><td><code class="literal">day</code></td></tr><tr><td><code class="literal">week</code></td></tr><tr><td><code class="literal">month</code></td></tr><tr><td><code class="literal">quarter</code></td></tr><tr><td><code class="literal">year</code></td></tr><tr><td><code class="literal">decade</code></td></tr><tr><td><code class="literal">century</code></td></tr><tr><td><code class="literal">millennium</code></td></tr></table>

當輸入值是 `timestamp with time zone` 型別時，截斷是相對於特定時區進行的；例如，截斷到 `day` 會產生該時區中午夜的值。預設情況下，截斷是相對於目前的 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定進行的，但可以提供選用的 *`time_zone`* 引數來指定不同的時區。時區名稱可以用[第 8.5.3 節](../datatype/datatype-datetime.md#DATATYPE-TIMEZONES)所述的任何方式指定。

處理 `timestamp without time zone` 或 `interval` 輸入時，無法指定時區。這些輸入一律按其表面值處理。

範例（假設當地時區為 `America/New_York`）：

```

SELECT date_trunc('hour', TIMESTAMP '2001-02-16 20:38:40');
Result: 2001-02-16 20:00:00
SELECT date_trunc('year', TIMESTAMP '2001-02-16 20:38:40');
Result: 2001-01-01 00:00:00
SELECT date_trunc('day', TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40+00');
Result: 2001-02-16 00:00:00-05
SELECT date_trunc('day', TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40+00', 'Australia/Sydney');
Result: 2001-02-16 08:00:00-05
SELECT date_trunc('hour', INTERVAL '3 days 02:47:33');
Result: 3 days 02:00:00
```

<a id="FUNCTIONS-DATETIME-BIN"></a>

### 9.9.3. `date_bin` [#](#FUNCTIONS-DATETIME-BIN)

<a id="id-1.5.8.15.15.2"></a>

函式 `date_bin` 會將輸入的時間戳記「分箱」（bin）到與指定原點對齊的指定時間間隔（*步幅*，stride）中。

```

date_bin(stride, source, origin)
```

*`source`* 是 `timestamp` 或 `timestamp with time zone` 型別的值運算式。（`date` 型別的值會自動轉換為 `timestamp`。）*`stride`* 是 `interval` 型別的值運算式。回傳值同樣是 `timestamp` 或 `timestamp with time zone` 型別，它標示了 *`source`* 所放入之箱的起點。

範例：

```

SELECT date_bin('15 minutes', TIMESTAMP '2020-02-11 15:44:17', TIMESTAMP '2001-01-01');
Result: 2020-02-11 15:30:00
SELECT date_bin('15 minutes', TIMESTAMP '2020-02-11 15:44:17', TIMESTAMP '2001-01-01 00:02:30');
Result: 2020-02-11 15:32:30
```

對於完整的單位（1 分鐘、1 小時等），它會產生與類似的 `date_trunc` 呼叫相同的結果，但差別在於 `date_bin` 可以截斷到任意的時間間隔。

*`stride`* 時間間隔必須大於零，而且不能包含月或更大的單位。

<a id="FUNCTIONS-DATETIME-ZONECONVERT"></a>

### 9.9.4. `AT TIME ZONE` 與 `AT LOCAL` [#](#FUNCTIONS-DATETIME-ZONECONVERT)

<a id="id-1.5.8.15.16.2"></a><a id="id-1.5.8.15.16.3"></a><a id="id-1.5.8.15.16.4"></a>

`AT TIME ZONE` 運算子可以在*不帶*時區的時間戳記與*帶*時區的時間戳記之間互相轉換，也可以將 `time with time zone` 值轉換到不同的時區。[表 9.34](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT-TABLE) 列出了它的變化形式。

<a id="FUNCTIONS-DATETIME-ZONECONVERT-TABLE"></a>

**表 9.34. `AT TIME ZONE` 與 `AT LOCAL` 的變化形式**

<table border="1" class="table" summary="AT TIME ZONE and AT LOCAL Variants"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         運算子
        </p>
<p>
         說明
        </p>
<p>
         範例
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp without time zone</code> <code class="literal">AT TIME ZONE</code> <em class="replaceable"><code>zone</code></em>
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>不帶</em></span>時區的時間戳記，轉換為<span class="emphasis"><em>帶</em></span>時區的時間戳記，並假設給定的值位於指定名稱的時區中。
        </p>
<p>
<code class="literal">timestamp '2001-02-16 20:38:40' at time zone 'America/Denver'</code>
         → <code class="returnvalue">2001-02-17 03:38:40+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp without time zone</code> <code class="literal">AT LOCAL</code>
         → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>不帶</em></span>時區的時間戳記，轉換為以工作階段的 <code class="varname">TimeZone</code> 值作為時區的<span class="emphasis"><em>帶</em></span>時區時間戳記。
        </p>
<p>
<code class="literal">timestamp '2001-02-16 20:38:40' at local</code>
         → <code class="returnvalue">2001-02-17 03:38:40+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp with time zone</code> <code class="literal">AT TIME ZONE</code> <em class="replaceable"><code>zone</code></em>
         → <code class="returnvalue">timestamp without time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>帶</em></span>時區的時間戳記，轉換為<span class="emphasis"><em>不帶</em></span>時區的時間戳記，其時間為在該時區中所呈現的時間。
        </p>
<p>
<code class="literal">timestamp with time zone '2001-02-16 20:38:40-05' at time zone 'America/Denver'</code>
         → <code class="returnvalue">2001-02-16 18:38:40</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">timestamp with time zone</code> <code class="literal">AT LOCAL</code>
         → <code class="returnvalue">timestamp without time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>帶</em></span>時區的時間戳記，轉換為<span class="emphasis"><em>不帶</em></span>時區的時間戳記，其時間為以工作階段的 <code class="varname">TimeZone</code> 值作為時區時所呈現的時間。
        </p>
<p>
<code class="literal">timestamp with time zone '2001-02-16 20:38:40-05' at local</code>
         → <code class="returnvalue">2001-02-16 18:38:40</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">time with time zone</code> <code class="literal">AT TIME ZONE</code> <em class="replaceable"><code>zone</code></em>
         → <code class="returnvalue">time with time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>帶</em></span>時區的時間轉換到新的時區。由於沒有提供日期，這會使用指定名稱之目的時區目前生效的 UTC 位移。
        </p>
<p>
<code class="literal">time with time zone '05:34:17-05' at time zone 'UTC'</code>
         → <code class="returnvalue">10:34:17+00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">time with time zone</code> <code class="literal">AT LOCAL</code>
         → <code class="returnvalue">time with time zone</code>
</p>
<p>
         將給定的<span class="emphasis"><em>帶</em></span>時區的時間轉換到新的時區。由於沒有提供日期，這會使用工作階段之 <code class="varname">TimeZone</code> 值目前生效的 UTC 位移。
        </p>
<p>
         假設工作階段的 <code class="varname">TimeZone</code> 設為 <code class="literal">UTC</code>：
        </p>
<p>
<code class="literal">time with time zone '05:34:17-05' at local</code>
         → <code class="returnvalue">10:34:17+00</code>
</p></td></tr></tbody></table>

<br>

在這些運算式中，所需的時區 *`zone`* 可以指定為文字值（例如 `'America/Los_Angeles'`），也可以指定為時間間隔（例如 `INTERVAL '-08:00'`）。在文字的情況下，時區名稱可以用[第 8.5.3 節](../datatype/datatype-datetime.md#DATATYPE-TIMEZONES)所述的任何方式指定。時間間隔的情況只對與 UTC 有固定位移的時區有用，因此在實務上不太常見。

語法 `AT LOCAL` 可以用作 `AT TIME ZONE local` 的簡寫，其中 *`local`* 是工作階段的 `TimeZone` 值。

範例（假設目前的 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定為 `America/Los_Angeles`）：

```

SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'America/Denver';
Result: 2001-02-16 19:38:40-08
SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE 'America/Denver';
Result: 2001-02-16 18:38:40
SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'Asia/Tokyo' AT TIME ZONE 'America/Chicago';
Result: 2001-02-16 05:38:40
SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT LOCAL;
Result: 2001-02-16 17:38:40
SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE '+05';
Result: 2001-02-16 20:38:40
SELECT TIME WITH TIME ZONE '20:38:40-05' AT LOCAL;
Result: 17:38:40
```

第一個範例為缺少時區的值加上時區，並使用目前的 `TimeZone` 設定顯示該值。第二個範例將帶時區的時間戳記值轉換到指定的時區，並回傳不帶時區的值。這樣就可以儲存與顯示和目前 `TimeZone` 設定不同的值。第三個範例將東京時間轉換為芝加哥時間。第四個範例將帶時區的時間戳記值轉換到目前 `TimeZone` 設定所指定的時區，並回傳不帶時區的值。第五個範例示範了 POSIX 風格時區規格中的正負號，與 ISO-8601 日期時間字面值中的正負號意義相反，如[第 8.5.3 節](../datatype/datatype-datetime.md#DATATYPE-TIMEZONES)與[附錄 B](../../appendixes/datetime-appendix/README.md) 所述。

第六個範例是一個警世故事。由於輸入值沒有相關聯的日期，轉換會使用工作階段的目前日期進行。因此，這個靜態範例可能會依照查看時是一年中的哪個時候而顯示錯誤的結果，因為 `'America/Los_Angeles'` 實施日光節約時間。

函式 `timezone(zone, timestamp)` 等同於符合 SQL 標準的結構 `timestamp AT TIME ZONE zone`。

函式 `timezone(zone, time)` 等同於符合 SQL 標準的結構 `time AT TIME ZONE zone`。

函式 `timezone(timestamp)` 等同於符合 SQL 標準的結構 `timestamp AT LOCAL`。

函式 `timezone(time)` 等同於符合 SQL 標準的結構 `time AT LOCAL`。

<a id="FUNCTIONS-DATETIME-CURRENT"></a>

### 9.9.5. 目前日期／時間 [#](#FUNCTIONS-DATETIME-CURRENT)

<a id="id-1.5.8.15.17.2"></a><a id="id-1.5.8.15.17.3"></a>

PostgreSQL 提供了許多回傳與目前日期與時間相關之值的函式。這些 SQL 標準函式回傳的值，都是以目前交易的開始時間為基礎：

```

CURRENT_DATE
CURRENT_TIME
CURRENT_TIMESTAMP
CURRENT_TIME(precision)
CURRENT_TIMESTAMP(precision)
LOCALTIME
LOCALTIMESTAMP
LOCALTIME(precision)
LOCALTIMESTAMP(precision)
```

`CURRENT_TIME` 與 `CURRENT_TIMESTAMP` 提供帶時區的值；`LOCALTIME` 與 `LOCALTIMESTAMP` 提供不帶時區的值。

`CURRENT_TIME`、`CURRENT_TIMESTAMP`、`LOCALTIME` 與 `LOCALTIMESTAMP` 可以選擇性地接受一個精度參數，使結果在秒欄位中四捨五入到該數量的小數位數。沒有精度參數時，結果會以完整的可用精度提供。

一些範例：

```

SELECT CURRENT_TIME;
Result: 14:39:53.662522-05
SELECT CURRENT_DATE;
Result: 2019-12-23
SELECT CURRENT_TIMESTAMP;
Result: 2019-12-23 14:39:53.662522-05
SELECT CURRENT_TIMESTAMP(2);
Result: 2019-12-23 14:39:53.66-05
SELECT LOCALTIMESTAMP;
Result: 2019-12-23 14:39:53.662522
```

由於這些函式回傳的是目前交易的開始時間，它們的值在交易期間不會改變。這被視為一項功能：其目的是讓單一交易對「目前」時間有一致的概念，使得同一個交易中的多次修改帶有相同的時間戳記。

### 注意

其他資料庫系統可能會更頻繁地推進這些值。

PostgreSQL 也提供了回傳目前陳述式之開始時間的函式，以及回傳呼叫函式那一刻之實際目前時間的函式。非 SQL 標準的時間函式完整清單如下：

```

transaction_timestamp()
statement_timestamp()
clock_timestamp()
timeofday()
now()
```

`transaction_timestamp()` 等同於 `CURRENT_TIMESTAMP`，但其名稱清楚反映了它所回傳的內容。`statement_timestamp()` 回傳目前陳述式的開始時間（更具體地說，是收到用戶端最新命令訊息的時間）。在交易的第一個陳述式期間，`statement_timestamp()` 與 `transaction_timestamp()` 會回傳相同的值，但在後續陳述式期間則可能不同。`clock_timestamp()` 回傳實際的目前時間，因此即使在單一 SQL 陳述式中，它的值也會改變。`timeofday()` 是一個歷史悠久的 PostgreSQL 函式。與 `clock_timestamp()` 一樣，它回傳實際的目前時間，但回傳的是格式化的 `text` 字串，而不是 `timestamp with time zone` 值。`now()` 是傳統的 PostgreSQL 函式，等同於 `transaction_timestamp()`。

所有日期／時間資料型別也都接受特殊的字面值 `now`，用來指定目前的日期與時間（同樣解讀為交易的開始時間）。因此，下面三者都會回傳相同的結果：

```

SELECT CURRENT_TIMESTAMP;
SELECT now();
SELECT TIMESTAMP 'now';  -- but see tip below
```

### 提示

在指定之後才要評估的值時，例如在資料表欄位的 `DEFAULT` 子句中，不要使用第三種形式。系統在剖析常數時就會立即將 `now` 轉換為 `timestamp`，因此在需要預設值時，所使用的會是建立資料表的時間！前兩種形式因為是函式呼叫，所以要到實際使用預設值時才會被評估。因此，它們會產生預設為插入資料列時間的預期行為。（另請參閱[第 8.5.1.4 節](../datatype/datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-VALUES)。）

<a id="FUNCTIONS-DATETIME-DELAY"></a>

### 9.9.6. 延遲執行 [#](#FUNCTIONS-DATETIME-DELAY)

<a id="id-1.5.8.15.18.2"></a><a id="id-1.5.8.15.18.3"></a><a id="id-1.5.8.15.18.4"></a><a id="id-1.5.8.15.18.5"></a><a id="id-1.5.8.15.18.6"></a>

下列函式可用來延遲伺服器程序的執行：

```

pg_sleep ( double precision )
pg_sleep_for ( interval )
pg_sleep_until ( timestamp with time zone )
```

`pg_sleep` 會使目前工作階段的程序休眠，直到經過給定的秒數為止。可以指定帶小數的秒數延遲。`pg_sleep_for` 是一個方便的函式，讓休眠時間可以用 `interval` 指定。`pg_sleep_until` 則是在需要特定喚醒時間時使用的方便函式。例如：

```

SELECT pg_sleep(1.5);
SELECT pg_sleep_for('5 minutes');
SELECT pg_sleep_until('tomorrow 03:00');
```

### 注意

休眠時間的有效解析度取決於平台；0.01 秒是常見的值。休眠延遲至少會與指定的一樣長。視伺服器負載等因素而定，它可能會更長。特別是，`pg_sleep_until` 並不保證會正好在指定的時間醒來，但它不會更早醒來。

### 警告

呼叫 `pg_sleep` 或其變化形式時，請確保你的工作階段沒有持有超過必要的鎖定。否則，其他工作階段可能必須等待你正在休眠的程序，拖慢整個系統。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-datetime.html)（原文版本：18.6；核對日期：2026-09-11）
