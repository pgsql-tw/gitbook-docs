<a id="FUNCTIONS-FORMATTING"></a>

## 9.8. 資料型別格式化函式 [#](#FUNCTIONS-FORMATTING)

<a id="id-1.5.8.14.2"></a>

PostgreSQL 的格式化函式提供了一套強大的工具，可以將各種資料型別（日期／時間、整數、浮點數、numeric）轉換為格式化的字串，也可以將格式化的字串轉換為特定的資料型別。[表 9.26](functions-formatting.md#FUNCTIONS-FORMATTING-TABLE) 列出了這些函式。這些函式都遵循一個共同的呼叫慣例：第一個引數是要格式化的值，第二個引數是定義輸出或輸入格式的範本。

<a id="FUNCTIONS-FORMATTING-TABLE"></a>

**表 9.26. 格式化函式**

<table border="1" class="table" summary="Formatting Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
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
        依照給定的格式將時間戳記轉換為字串。
       </p>
<p>
<code class="literal">to_char(timestamp '2002-04-20 17:31:12.66', 'HH12:MI:SS')</code>
        → <code class="returnvalue">05:31:12</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">to_char</code> ( <code class="type">interval</code>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        依照給定的格式將時間間隔轉換為字串。
       </p>
<p>
<code class="literal">to_char(interval '15h 2m 12s', 'HH24:MI:SS')</code>
       → <code class="returnvalue">15:02:12</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">to_char</code> ( <em class="replaceable"><code>numeric_type</code></em>, <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        依照給定的格式將數字轉換為字串；適用於 <code class="type">integer</code>、<code class="type">bigint</code>、<code class="type">numeric</code>、<code class="type">real</code>、<code class="type">double precision</code>。
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
        依照給定的格式將字串轉換為日期。
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
        依照給定的格式將字串轉換為 numeric。
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
        依照給定的格式將字串轉換為時間戳記。（另請參閱<a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TABLE">表 9.33</a> 中的 <code class="function">to_timestamp(double precision)</code>。）
       </p>
<p>
<code class="literal">to_timestamp('05 Dec 2000', 'DD Mon YYYY')</code>
        → <code class="returnvalue">2000-12-05 00:00:00-05</code>
</p></td></tr></tbody></table>

<br>

### 提示

`to_timestamp` 與 `to_date` 是為了處理無法以簡單型別轉換來轉換的輸入格式而存在的。對於大多數標準的日期／時間格式，只要將來源字串轉換為所需的資料型別就可以了，而且簡單得多。同樣地，對於標準的數值表示，也不需要使用 `to_number`。

在 `to_char` 的輸出範本字串中，有一些樣式會被辨識出來，並依據給定的值替換為適當格式化的資料。任何不是範本樣式的文字都會原封不動地複製。同樣地，在（其他函式的）輸入範本字串中，範本樣式用來識別輸入資料字串所要提供的值。如果範本字串中有不是範本樣式的字元，輸入資料字串中對應的字元就會直接被略過（無論它們是否與範本字串的字元相同）。

[表 9.27](functions-formatting.md#FUNCTIONS-FORMATTING-DATETIME-TABLE) 列出了可用於格式化日期與時間值的範本樣式。

<a id="FUNCTIONS-FORMATTING-DATETIME-TABLE"></a>

**表 9.27. 日期／時間格式化的範本樣式**

<table border="1" class="table" summary="Template Patterns for Date/Time Formatting"><colgroup><col/><col/></colgroup><thead><tr><th>樣式</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">HH</code></td><td>一天中的小時（01–12）</td></tr><tr><td><code class="literal">HH12</code></td><td>一天中的小時（01–12）</td></tr><tr><td><code class="literal">HH24</code></td><td>一天中的小時（00–23）</td></tr><tr><td><code class="literal">MI</code></td><td>分（00–59）</td></tr><tr><td><code class="literal">SS</code></td><td>秒（00–59）</td></tr><tr><td><code class="literal">MS</code></td><td>毫秒（000–999）</td></tr><tr><td><code class="literal">US</code></td><td>微秒（000000–999999）</td></tr><tr><td><code class="literal">FF1</code></td><td>十分之一秒（0–9）</td></tr><tr><td><code class="literal">FF2</code></td><td>百分之一秒（00–99）</td></tr><tr><td><code class="literal">FF3</code></td><td>毫秒（000–999）</td></tr><tr><td><code class="literal">FF4</code></td><td>十分之一毫秒（0000–9999）</td></tr><tr><td><code class="literal">FF5</code></td><td>百分之一毫秒（00000–99999）</td></tr><tr><td><code class="literal">FF6</code></td><td>微秒（000000–999999）</td></tr><tr><td><code class="literal">SSSS</code>, <code class="literal">SSSSS</code></td><td>午夜之後經過的秒數（0–86399）</td></tr><tr><td><code class="literal">AM</code>, <code class="literal">am</code>,
        <code class="literal">PM</code> or <code class="literal">pm</code></td><td>上午／下午指示符（不含句點）</td></tr><tr><td><code class="literal">A.M.</code>, <code class="literal">a.m.</code>,
        <code class="literal">P.M.</code> or <code class="literal">p.m.</code></td><td>上午／下午指示符（含句點）</td></tr><tr><td><code class="literal">Y,YYY</code></td><td>含逗號的年份（4 位數或更多）</td></tr><tr><td><code class="literal">YYYY</code></td><td>年份（4 位數或更多）</td></tr><tr><td><code class="literal">YYY</code></td><td>年份的最後 3 位數</td></tr><tr><td><code class="literal">YY</code></td><td>年份的最後 2 位數</td></tr><tr><td><code class="literal">Y</code></td><td>年份的最後一位數</td></tr><tr><td><code class="literal">IYYY</code></td><td>ISO 8601 週編號年（4 位數或更多）</td></tr><tr><td><code class="literal">IYY</code></td><td>ISO 8601 週編號年的最後 3 位數</td></tr><tr><td><code class="literal">IY</code></td><td>ISO 8601 週編號年的最後 2 位數</td></tr><tr><td><code class="literal">I</code></td><td>ISO 8601 週編號年的最後一位數</td></tr><tr><td><code class="literal">BC</code>, <code class="literal">bc</code>,
        <code class="literal">AD</code> or <code class="literal">ad</code></td><td>紀元指示符（不含句點）</td></tr><tr><td><code class="literal">B.C.</code>, <code class="literal">b.c.</code>,
        <code class="literal">A.D.</code> or <code class="literal">a.d.</code></td><td>紀元指示符（含句點）</td></tr><tr><td><code class="literal">MONTH</code></td><td>全大寫的完整月份名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">Month</code></td><td>首字母大寫的完整月份名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">month</code></td><td>全小寫的完整月份名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">MON</code></td><td>全大寫的月份名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">Mon</code></td><td>首字母大寫的月份名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">mon</code></td><td>全小寫的月份名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">MM</code></td><td>月份編號（01–12）</td></tr><tr><td><code class="literal">DAY</code></td><td>全大寫的完整星期名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">Day</code></td><td>首字母大寫的完整星期名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">day</code></td><td>全小寫的完整星期名稱（以空白填補至 9 個字元）</td></tr><tr><td><code class="literal">DY</code></td><td>全大寫的星期名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">Dy</code></td><td>首字母大寫的星期名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">dy</code></td><td>全小寫的星期名稱縮寫（英文為 3 個字元，本地化的長度不一）</td></tr><tr><td><code class="literal">DDD</code></td><td>一年中的第幾天（001–366）</td></tr><tr><td><code class="literal">IDDD</code></td><td>ISO 8601 週編號年中的第幾天（001–371；一年的第 1 天是第一個 ISO 週的星期一）</td></tr><tr><td><code class="literal">DD</code></td><td>月中的第幾天（01–31）</td></tr><tr><td><code class="literal">D</code></td><td>星期幾，從星期日（<code class="literal">1</code>）到星期六（<code class="literal">7</code>）</td></tr><tr><td><code class="literal">ID</code></td><td>ISO 8601 的星期幾，從星期一（<code class="literal">1</code>）到星期日（<code class="literal">7</code>）</td></tr><tr><td><code class="literal">W</code></td><td>月中的第幾週（1–5）（第一週從該月的第一天開始）</td></tr><tr><td><code class="literal">WW</code></td><td>一年中的週數（1–53）（第一週從該年的第一天開始）</td></tr><tr><td><code class="literal">IW</code></td><td>ISO 8601 週編號年中的週數（01–53；一年中的第一個星期四位於第 1 週）</td></tr><tr><td><code class="literal">CC</code></td><td>世紀（2 位數）（二十一世紀從 2001-01-01 開始）</td></tr><tr><td><code class="literal">J</code></td><td>儒略日（自西元前 4714 年 11 月 24 日當地午夜起算的整數天數；請參閱<a class="xref" href="../../appendixes/datetime-appendix/datetime-julian-dates.md">第 B.7 節</a>）</td></tr><tr><td><code class="literal">Q</code></td><td>季</td></tr><tr><td><code class="literal">RM</code></td><td>以大寫羅馬數字表示的月份（I–XII；I=一月）</td></tr><tr><td><code class="literal">rm</code></td><td>以小寫羅馬數字表示的月份（i–xii；i=一月）</td></tr><tr><td><code class="literal">TZ</code></td><td>大寫的時區縮寫</td></tr><tr><td><code class="literal">tz</code></td><td>小寫的時區縮寫</td></tr><tr><td><code class="literal">TZH</code></td><td>時區的小時</td></tr><tr><td><code class="literal">TZM</code></td><td>時區的分鐘</td></tr><tr><td><code class="literal">OF</code></td><td>相對於 UTC 的時區位移（<em class="replaceable"><code>HH</code></em> 或 <em class="replaceable"><code>HH</code></em><code class="literal">:</code><em class="replaceable"><code>MM</code></em>）</td></tr></tbody></table>

<br>

修飾詞可以套用到任何範本樣式上，以改變其行為。例如，`FMMonth` 就是加上 `FM` 修飾詞的 `Month` 樣式。[表 9.28](functions-formatting.md#FUNCTIONS-FORMATTING-DATETIMEMOD-TABLE) 列出了日期／時間格式化的修飾詞樣式。

<a id="FUNCTIONS-FORMATTING-DATETIMEMOD-TABLE"></a>

**表 9.28. 日期／時間格式化的範本樣式修飾詞**

<table border="1" class="table" summary="Template Pattern Modifiers for Date/Time Formatting"><colgroup><col/><col/><col/></colgroup><thead><tr><th>修飾詞</th><th>說明</th><th>範例</th></tr></thead><tbody><tr><td><code class="literal">FM</code> 前綴</td><td>填補模式（抑制前導零與填補空白）</td><td><code class="literal">FMMonth</code></td></tr><tr><td><code class="literal">TH</code> 字尾</td><td>大寫的序數字尾</td><td><code class="literal">DDTH</code>, e.g., <code class="literal">12TH</code></td></tr><tr><td><code class="literal">th</code> 字尾</td><td>小寫的序數字尾</td><td><code class="literal">DDth</code>, e.g., <code class="literal">12th</code></td></tr><tr><td><code class="literal">FX</code> 前綴</td><td>固定格式的全域選項（請參閱使用注意事項）</td><td><code class="literal">FX Month DD Day</code></td></tr><tr><td><code class="literal">TM</code> 前綴</td><td>翻譯模式（依據 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-TIME">lc_time</a> 使用本地化的星期與月份名稱）</td><td><code class="literal">TMMonth</code></td></tr><tr><td><code class="literal">SP</code> 字尾</td><td>拼寫模式（未實作）</td><td><code class="literal">DDSP</code></td></tr></tbody></table>

<br>

日期／時間格式化的使用注意事項：

* `FM` 會抑制原本為了讓樣式輸出成為固定寬度而加上的前導零與尾端空白。在 PostgreSQL 中，`FM` 只會修飾下一個規格；而在 Oracle 中，`FM` 會影響所有後續的規格，重複的 `FM` 修飾詞則會切換填補模式的開關。
* 無論是否指定了 `FM`，`TM` 都會抑制尾端空白。
* `to_timestamp` 與 `to_date` 會忽略輸入中的大小寫；因此，例如 `MON`、`Mon` 與 `mon` 都接受相同的字串。使用 `TM` 修飾詞時，大小寫摺疊會依照函式輸入定序的規則進行（請參閱[第 23.2 節](../../server-administration/charset/collation.md)）。
* 除非使用 `FX` 選項，否則 `to_timestamp` 與 `to_date` 會略過輸入字串開頭以及日期與時間值周圍的多個空白。例如，`to_timestamp(' 2000    JUN', 'YYYY MON')` 與 `to_timestamp('2000 - JUN', 'YYYY-MON')` 都可以運作，但 `to_timestamp('2000    JUN', 'FXYYYY MON')` 會回傳錯誤，因為 `to_timestamp` 只預期一個空白。`FX` 必須指定為範本中的第一個項目。
* 除非使用 `FX` 選項，否則 `to_timestamp` 與 `to_date` 範本字串中的分隔符號（空白或非字母／非數字的字元），會比對輸入字串中的任何單一分隔符號，或是被略過。例如，`to_timestamp('2000JUN', 'YYYY///MON')` 與 `to_timestamp('2000/JUN', 'YYYY MON')` 都可以運作，但 `to_timestamp('2000//JUN', 'YYYY/MON')` 會回傳錯誤，因為輸入字串中的分隔符號數量超過了範本中的分隔符號數量。

  如果指定了 `FX`，範本字串中的一個分隔符號會正好比對輸入字串中的一個字元。但請注意，輸入字串的字元不必與範本字串中的分隔符號相同。例如，`to_timestamp('2000/JUN', 'FXYYYY MON')` 可以運作，但 `to_timestamp('2000/JUN', 'FXYYYY MON')` 會回傳錯誤，因為範本字串中的第二個空白會取用輸入字串中的字母 `J`。
* `TZH` 範本樣式可以比對帶正負號的數字。在沒有 `FX` 選項的情況下，減號可能會有歧義，可能被解讀為分隔符號。這個歧義的解決方式如下：如果範本字串中 `TZH` 之前的分隔符號數量，少於輸入字串中減號之前的分隔符號數量，減號就會被解讀為 `TZH` 的一部分。否則，減號會被視為值之間的分隔符號。例如，`to_timestamp('2000 -10', 'YYYY TZH')` 會將 `-10` 比對到 `TZH`，但 `to_timestamp('2000 -10', 'YYYY TZH')` 會將 `10` 比對到 `TZH`。
* `to_char` 範本中允許使用一般文字，它們會按字面輸出。你可以將子字串放在雙引號中，強制將它解讀為字面文字，即使其中包含範本樣式也一樣。例如，在 `'"Hello Year "YYYY'` 中，`YYYY` 會被替換為年份資料，但 `Year` 中的單一 `Y` 則不會。在 `to_date`、`to_number` 與 `to_timestamp` 中，字面文字與雙引號字串會導致略過與字串所含字元數相同的字元數；例如 `"XX"` 會略過兩個輸入字元（無論它們是否為 `XX`）。

  ### 提示

  在 PostgreSQL 12 之前，可以使用非字母或非數字的字元來略過輸入字串中的任意文字。例如，`to_timestamp('2000y6m1d', 'yyyy-MM-DD')` 以前可以運作。現在你只能使用字母字元來達到這個目的。例如，`to_timestamp('2000y6m1d', 'yyyytMMtDDt')` 與 `to_timestamp('2000y6m1d', 'yyyy"y"MM"m"DD"d"')` 會略過 `y`、`m` 與 `d`。
* 如果你想在輸出中包含雙引號，必須在它前面加上反斜線，例如 `'\"YYYY Month\"'`。在雙引號字串之外，反斜線沒有其他特殊意義。在雙引號字串之內，反斜線會使下一個字元被按字面解讀，無論它是什麼字元（但除非下一個字元是雙引號或另一個反斜線，否則這並沒有特殊的效果）。
* 在 `to_timestamp` 與 `to_date` 中，如果年份格式規格少於四位數（例如 `YYY`），而提供的年份也少於四位數，年份會被調整為最接近 2020 年的年份，例如 `95` 會變成 1995。
* 在 `to_timestamp` 與 `to_date` 中，負的年份被視為表示西元前（BC）。如果你同時寫出負的年份與明確的 `BC` 欄位，就會再次得到西元（AD）。輸入年份零會被視為西元前 1 年。
* 在 `to_timestamp` 與 `to_date` 中，處理超過 4 位數的年份時，`YYYY` 轉換有一項限制。你必須在 `YYYY` 之後使用某個非數字字元或範本，否則年份一律會被解讀為 4 位數。例如（以年份 20000 為例）：`to_date('200001130', 'YYYYMMDD')` 會被解讀為 4 位數的年份；請改為在年份之後使用非數字的分隔符號，例如 `to_date('20000-1130', 'YYYY-MMDD')` 或 `to_date('20000Nov30', 'YYYYMonDD')`。
* 在 `to_timestamp` 與 `to_date` 中，如果有 `YYY`、`YYYY` 或 `Y,YYY` 欄位，`CC`（世紀）欄位會被接受但忽略。如果 `CC` 與 `YY` 或 `Y` 一起使用，結果會計算為指定世紀中的那一年。如果指定了世紀但沒有指定年份，就假設為該世紀的第一年。
* 在 `to_timestamp` 與 `to_date` 中，星期的名稱或數字（`DAY`、`D` 以及相關的欄位類型）會被接受，但在計算結果時會被忽略。季（`Q`）欄位也是如此。
* 在 `to_timestamp` 與 `to_date` 中，ISO 8601 週編號日期（有別於格里曆日期）可以用下列兩種方式之一指定：

  * 年、週數與星期幾：例如 `to_date('2006-42-4', 'IYYY-IW-ID')` 會回傳日期 `2006-10-19`。如果省略星期幾，就假設為 1（星期一）。
  * 年與一年中的第幾天：例如 `to_date('2006-291', 'IYYY-IDDD')` 也會回傳 `2006-10-19`。

  嘗試混用 ISO 8601 週編號欄位與格里曆日期欄位來輸入日期是沒有意義的，而且會導致錯誤。在 ISO 8601 週編號年的情境中，「月」或「月中的第幾天」的概念沒有意義。在格里曆年的情境中，ISO 週則沒有意義。

  ### 警示

  雖然 `to_date` 會拒絕格里曆與 ISO 週編號日期欄位的混用，但 `to_char` 不會，因為像 `YYYY-MM-DD (IYYY-IDDD)` 這樣的輸出格式規格可能很有用。但請避免寫出像 `IYYY-MM-DD` 這樣的東西；它在年初附近會產生令人意外的結果。（更多資訊請參閱[第 9.9.1 節](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)。）
* 在 `to_timestamp` 中，毫秒（`MS`）或微秒（`US`）欄位會被用作小數點之後的秒數位數。例如，`to_timestamp('12.3', 'SS.MS')` 不是 3 毫秒，而是 300 毫秒，因為轉換會將它視為 12 + 0.3 秒。因此，對於格式 `SS.MS`，輸入值 `12.3`、`12.30` 與 `12.300` 指定的都是相同的毫秒數。要得到三毫秒，必須寫成 `12.003`，轉換會將它視為 12 + 0.003 = 12.003 秒。

  以下是一個更複雜的範例：`to_timestamp('15:12:02.020.001230', 'HH24:MI:SS.MS.US')` 是 15 小時 12 分 2 秒 + 20 毫秒 + 1230 微秒 = 2.021230 秒。
* `to_char(..., 'ID')` 的星期編號與 `extract(isodow from ...)` 函式相符，但 `to_char(..., 'D')` 的星期編號與 `extract(dow from ...)` 的並不相符。
* `to_char(interval)` 將 `HH` 與 `HH12` 格式化為 12 小時制時鐘上所顯示的值，例如零小時與 36 小時都會輸出為 `12`；而 `HH24` 會輸出完整的小時值，在 `interval` 值中可能超過 23。

[表 9.29](functions-formatting.md#FUNCTIONS-FORMATTING-NUMERIC-TABLE) 列出了可用於格式化數值的範本樣式。

<a id="FUNCTIONS-FORMATTING-NUMERIC-TABLE"></a>

**表 9.29. 數值格式化的範本樣式**

<table border="1" class="table" summary="Template Patterns for Numeric Formatting"><colgroup><col/><col/></colgroup><thead><tr><th>樣式</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">9</code></td><td>數字位置（若不重要可以省略）</td></tr><tr><td><code class="literal">0</code></td><td>數字位置（即使不重要也不會省略）</td></tr><tr><td><code class="literal">.</code>（句點）</td><td>小數點</td></tr><tr><td><code class="literal">,</code>（逗號）</td><td>群組（千位）分隔符號</td></tr><tr><td><code class="literal">PR</code></td><td>以角括號表示負值</td></tr><tr><td><code class="literal">S</code></td><td>固定在數字旁的正負號（使用語系設定）</td></tr><tr><td><code class="literal">L</code></td><td>貨幣符號（使用語系設定）</td></tr><tr><td><code class="literal">D</code></td><td>小數點（使用語系設定）</td></tr><tr><td><code class="literal">G</code></td><td>群組分隔符號（使用語系設定）</td></tr><tr><td><code class="literal">MI</code></td><td>在指定位置的減號（若數字 &lt; 0）</td></tr><tr><td><code class="literal">PL</code></td><td>在指定位置的加號（若數字 &gt; 0）</td></tr><tr><td><code class="literal">SG</code></td><td>在指定位置的正負號</td></tr><tr><td><code class="literal">RN</code> or <code class="literal">rn</code></td><td>羅馬數字（1 到 3999 之間的值）</td></tr><tr><td><code class="literal">TH</code> or <code class="literal">th</code></td><td>序數字尾</td></tr><tr><td><code class="literal">V</code></td><td>位移指定的位數（請參閱注意事項）</td></tr><tr><td><code class="literal">EEEE</code></td><td>科學記號的指數</td></tr></tbody></table>

<br>

數值格式化的使用注意事項：

* `0` 指定一個一定會印出的數字位置，即使它包含前導零或尾端零也一樣。`9` 也指定一個數字位置，但如果它是前導零，就會被替換為空白；而如果它是尾端零且指定了填補模式，就會被刪除。（對於 `to_number()`，這兩個樣式字元是等價的。）
* 如果格式提供的小數位數少於要格式化的數字，`to_char()` 會將數字四捨五入到指定的小數位數。
* 樣式字元 `S`、`L`、`D` 與 `G` 分別代表由目前語系所定義的正負號、貨幣符號、小數點與千位分隔符號字元（請參閱 [lc_monetary](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MONETARY) 與 [lc_numeric](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-NUMERIC)）。樣式字元句點與逗號則代表這些字元本身，分別具有小數點與千位分隔符號的意義，與語系無關。
* 如果 `to_char()` 的樣式中沒有明確為正負號做安排，就會為正負號保留一欄，並將它固定在數字旁（出現在數字的正左邊）。如果 `S` 出現在某些 `9` 的正左邊，它同樣會被固定在數字旁。
* 使用 `SG`、`PL` 或 `MI` 格式化的正負號不會固定在數字旁；例如，`to_char(-12, 'MI9999')` 會產生 `'-  12'`，但 `to_char(-12, 'S9999')` 會產生 `'  -12'`。（Oracle 的實作不允許在 `9` 之前使用 `MI`，而是要求 `9` 位於 `MI` 之前。）
* `TH` 不會轉換小於零的值，也不會轉換小數。
* `PL`、`SG` 與 `TH` 是 PostgreSQL 的擴充功能。
* 在 `to_number` 中，如果使用了 `L` 或 `TH` 這類非資料的範本樣式，就會略過相應數量的輸入字元，無論它們是否符合範本樣式，除非它們是資料字元（也就是數字、正負號、小數點或逗號）。例如，`TH` 會略過兩個非資料字元。
* `V` 搭配 `to_char` 使用時，會將輸入值乘以 `10^n`，其中 *`n`* 是 `V` 之後的位數。`V` 搭配 `to_number` 使用時，則以類似的方式進行除法。可以將 `V` 想成是在輸入或輸出字串中標記隱含小數點的位置。`to_char` 與 `to_number` 不支援將 `V` 與小數點結合使用（例如，不允許 `99.9V99`）。
* `EEEE`（科學記號）不能與數字及小數點樣式以外的任何其他格式化樣式或修飾詞結合使用，而且必須位於格式字串的最後（例如，`9.99EEEE` 是有效的樣式）。
* 在 `to_number()` 中，`RN` 樣式會將（標準形式的）羅馬數字轉換為數字。輸入不區分大小寫，因此 `RN` 與 `rn` 是等價的。`RN` 不能與任何其他格式化樣式或修飾詞結合使用，唯一的例外是 `FM`，但它只適用於 `to_char()`，在 `to_number()` 中會被忽略。

某些修飾詞可以套用到任何範本樣式上，以改變其行為。例如，`FM99.99` 就是加上 `FM` 修飾詞的 `99.99` 樣式。[表 9.30](functions-formatting.md#FUNCTIONS-FORMATTING-NUMERICMOD-TABLE) 列出了數值格式化的修飾詞樣式。

<a id="FUNCTIONS-FORMATTING-NUMERICMOD-TABLE"></a>

**表 9.30. 數值格式化的範本樣式修飾詞**

<table border="1" class="table" summary="Template Pattern Modifiers for Numeric Formatting"><colgroup><col/><col/><col/></colgroup><thead><tr><th>修飾詞</th><th>說明</th><th>範例</th></tr></thead><tbody><tr><td><code class="literal">FM</code> 前綴</td><td>填補模式（抑制尾端零與填補空白）</td><td><code class="literal">FM99.99</code></td></tr><tr><td><code class="literal">TH</code> 字尾</td><td>大寫的序數字尾</td><td><code class="literal">999TH</code></td></tr><tr><td><code class="literal">th</code> 字尾</td><td>小寫的序數字尾</td><td><code class="literal">999th</code></td></tr></tbody></table>

<br>

[表 9.31](functions-formatting.md#FUNCTIONS-FORMATTING-EXAMPLES-TABLE) 列出了一些使用 `to_char` 函式的範例。

<a id="FUNCTIONS-FORMATTING-EXAMPLES-TABLE"></a>

**表 9.31. `to_char` 範例**

<table border="1" class="table" summary="to_char Examples"><colgroup><col/><col/></colgroup><thead><tr><th>運算式</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">to_char(current_timestamp, 'Day, DD  HH12:MI:SS')</code></td><td><code class="literal">'Tuesday  , 06  05:39:18'</code></td></tr><tr><td><code class="literal">to_char(current_timestamp, 'FMDay, FMDD  HH12:MI:SS')</code></td><td><code class="literal">'Tuesday, 6  05:39:18'</code></td></tr><tr><td><code class="literal">to_char(current_timestamp AT TIME ZONE
        'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')</code></td><td><code class="literal">'2022-12-06T05:39:18Z'</code>，<acronym class="acronym">ISO</acronym> 8601 延伸格式</td></tr><tr><td><code class="literal">to_char(-0.1, '99.99')</code></td><td><code class="literal">'  -.10'</code></td></tr><tr><td><code class="literal">to_char(-0.1, 'FM9.99')</code></td><td><code class="literal">'-.1'</code></td></tr><tr><td><code class="literal">to_char(-0.1, 'FM90.99')</code></td><td><code class="literal">'-0.1'</code></td></tr><tr><td><code class="literal">to_char(0.1, '0.9')</code></td><td><code class="literal">' 0.1'</code></td></tr><tr><td><code class="literal">to_char(12, '9990999.9')</code></td><td><code class="literal">'    0012.0'</code></td></tr><tr><td><code class="literal">to_char(12, 'FM9990999.9')</code></td><td><code class="literal">'0012.'</code></td></tr><tr><td><code class="literal">to_char(485, '999')</code></td><td><code class="literal">' 485'</code></td></tr><tr><td><code class="literal">to_char(-485, '999')</code></td><td><code class="literal">'-485'</code></td></tr><tr><td><code class="literal">to_char(485, '9 9 9')</code></td><td><code class="literal">' 4 8 5'</code></td></tr><tr><td><code class="literal">to_char(1485, '9,999')</code></td><td><code class="literal">' 1,485'</code></td></tr><tr><td><code class="literal">to_char(1485, '9G999')</code></td><td><code class="literal">' 1 485'</code></td></tr><tr><td><code class="literal">to_char(148.5, '999.999')</code></td><td><code class="literal">' 148.500'</code></td></tr><tr><td><code class="literal">to_char(148.5, 'FM999.999')</code></td><td><code class="literal">'148.5'</code></td></tr><tr><td><code class="literal">to_char(148.5, 'FM999.990')</code></td><td><code class="literal">'148.500'</code></td></tr><tr><td><code class="literal">to_char(148.5, '999D999')</code></td><td><code class="literal">' 148,500'</code></td></tr><tr><td><code class="literal">to_char(3148.5, '9G999D999')</code></td><td><code class="literal">' 3 148,500'</code></td></tr><tr><td><code class="literal">to_char(-485, '999S')</code></td><td><code class="literal">'485-'</code></td></tr><tr><td><code class="literal">to_char(-485, '999MI')</code></td><td><code class="literal">'485-'</code></td></tr><tr><td><code class="literal">to_char(485, '999MI')</code></td><td><code class="literal">'485 '</code></td></tr><tr><td><code class="literal">to_char(485, 'FM999MI')</code></td><td><code class="literal">'485'</code></td></tr><tr><td><code class="literal">to_char(485, 'PL999')</code></td><td><code class="literal">'+485'</code></td></tr><tr><td><code class="literal">to_char(485, 'SG999')</code></td><td><code class="literal">'+485'</code></td></tr><tr><td><code class="literal">to_char(-485, 'SG999')</code></td><td><code class="literal">'-485'</code></td></tr><tr><td><code class="literal">to_char(-485, '9SG99')</code></td><td><code class="literal">'4-85'</code></td></tr><tr><td><code class="literal">to_char(-485, '999PR')</code></td><td><code class="literal">'&lt;485&gt;'</code></td></tr><tr><td><code class="literal">to_char(485, 'L999')</code></td><td><code class="literal">'DM 485'</code></td></tr><tr><td><code class="literal">to_char(485, 'RN')</code></td><td><code class="literal">'        CDLXXXV'</code></td></tr><tr><td><code class="literal">to_char(485, 'FMRN')</code></td><td><code class="literal">'CDLXXXV'</code></td></tr><tr><td><code class="literal">to_char(5.2, 'FMRN')</code></td><td><code class="literal">'V'</code></td></tr><tr><td><code class="literal">to_char(482, '999th')</code></td><td><code class="literal">' 482nd'</code></td></tr><tr><td><code class="literal">to_char(485, '"Good number:"999')</code></td><td><code class="literal">'Good number: 485'</code></td></tr><tr><td><code class="literal">to_char(485.8, '"Pre:"999" Post:" .999')</code></td><td><code class="literal">'Pre: 485 Post: .800'</code></td></tr><tr><td><code class="literal">to_char(12, '99V999')</code></td><td><code class="literal">' 12000'</code></td></tr><tr><td><code class="literal">to_char(12.4, '99V999')</code></td><td><code class="literal">' 12400'</code></td></tr><tr><td><code class="literal">to_char(12.45, '99V9')</code></td><td><code class="literal">' 125'</code></td></tr><tr><td><code class="literal">to_char(0.0004859, '9.99EEEE')</code></td><td><code class="literal">' 4.86e-04'</code></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-formatting.html)（原文版本：18.6；核對日期：2026-09-11）
