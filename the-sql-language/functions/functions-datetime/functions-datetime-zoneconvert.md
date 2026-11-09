# 9.9.4. AT TIME ZONE 與 AT LOCAL

<a id="FUNCTIONS-DATETIME-ZONECONVERT"></a>

## 9.9.4. `AT TIME ZONE` 與 `AT LOCAL` [#](#functions-datetime-zoneconvert) <a href="#functions-datetime-zoneconvert" id="functions-datetime-zoneconvert"></a>

<a id="id-1.5.8.15.16.2"></a><a id="id-1.5.8.15.16.3"></a><a id="id-1.5.8.15.16.4"></a>

`AT TIME ZONE` 運算子可以在*不帶*時區的時間戳記與*帶*時區的時間戳記之間互相轉換，也可以將 `time with time zone` 值轉換到不同的時區。[表 9.34](#functions-datetime-zoneconvert-table) 列出了它的變化形式。

<a id="FUNCTIONS-DATETIME-ZONECONVERT-TABLE"></a>

### 表 9.34. `AT TIME ZONE` 與 `AT LOCAL` 的變化形式 [#](#functions-datetime-zoneconvert-table) <a href="#functions-datetime-zoneconvert-table" id="functions-datetime-zoneconvert-table"></a>

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

在這些運算式中，所需的時區 *`zone`* 可以指定為文字值（例如 `'America/Los_Angeles'`），也可以指定為時間間隔（例如 `INTERVAL '-08:00'`）。在文字的情況下，時區名稱可以用[第 8.5.3 節](../../datatype/datatype-datetime.md#datatype-timezones)所述的任何方式指定。時間間隔的情況只對與 UTC 有固定位移的時區有用，因此在實務上不太常見。

語法 `AT LOCAL` 可以用作 `AT TIME ZONE local` 的簡寫，其中 *`local`* 是工作階段的 `TimeZone` 值。

範例（假設目前的 [TimeZone](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定為 `America/Los_Angeles`）：

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

第一個範例為缺少時區的值加上時區，並使用目前的 `TimeZone` 設定顯示該值。第二個範例將帶時區的時間戳記值轉換到指定的時區，並回傳不帶時區的值。這樣就可以儲存與顯示和目前 `TimeZone` 設定不同的值。第三個範例將東京時間轉換為芝加哥時間。第四個範例將帶時區的時間戳記值轉換到目前 `TimeZone` 設定所指定的時區，並回傳不帶時區的值。第五個範例示範了 POSIX 風格時區規格中的正負號，與 ISO-8601 日期時間字面值中的正負號意義相反，如[第 8.5.3 節](../../datatype/datatype-datetime.md#datatype-timezones)與[附錄 B](../../../appendixes/datetime-appendix/README.md) 所述。

第六個範例是一個警世故事。由於輸入值沒有相關聯的日期，轉換會使用工作階段的目前日期進行。因此，這個靜態範例可能會依照查看時是一年中的哪個時候而顯示錯誤的結果，因為 `'America/Los_Angeles'` 實施日光節約時間。

函式 `timezone(zone, timestamp)` 等同於符合 SQL 標準的結構 `timestamp AT TIME ZONE zone`。

函式 `timezone(zone, time)` 等同於符合 SQL 標準的結構 `time AT TIME ZONE zone`。

函式 `timezone(timestamp)` 等同於符合 SQL 標準的結構 `timestamp AT LOCAL`。

函式 `timezone(time)` 等同於符合 SQL 標準的結構 `time AT LOCAL`。

[返回 9.9. 日期／時間函式與運算子](../functions-datetime.md#functions-datetime)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-datetime.html)（原文版本：18.6；核對日期：2026-09-11）
