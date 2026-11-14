# 9.16.3. SQL/JSON 查詢函式

<a id="SQLJSON-QUERY-FUNCTIONS"></a>

## 9.16.3. SQL/JSON 查詢函式 [#](#sqljson-query-functions) <a href="#sqljson-query-functions" id="sqljson-query-functions"></a>

[表 9.54](#functions-sqljson-querying) 所述的 SQL/JSON 函式 `JSON_EXISTS()`、`JSON_QUERY()` 與 `JSON_VALUE()` 可用來查詢 JSON 文件。這些函式都會將 *`path_expression`*（SQL/JSON 路徑查詢）套用到 *`context_item`*（文件）上。關於 *`path_expression`* 可以包含哪些內容的詳細資訊，請參閱[第 9.16.2 節](../functions-json.md#functions-sqljson-path)。*`path_expression`* 也可以參照變數，變數的值是透過每個函式都支援的 `PASSING` 子句，以其各自的名稱來指定。*`context_item`* 可以是 `jsonb` 值，或是可以成功轉換為 `jsonb` 的字元字串。

<a id="FUNCTIONS-SQLJSON-QUERYING"></a>

### 表 9.54. SQL/JSON 查詢函式 [#](#functions-sqljson-querying) <a href="#functions-sqljson-querying" id="functions-sqljson-querying"></a>

<table border="1" class="table" summary="SQL/JSON Query Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式簽章
       </p>
<p>
        說明
       </p>
<p>
        範例
      </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.1.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_EXISTS</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional">{ <code class="literal">TRUE</code> | <code class="literal">FALSE</code> |<code class="literal"> UNKNOWN</code> | <code class="literal">ERROR</code> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">boolean</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        如果 SQL/JSON <em class="replaceable"><code>path_expression</code></em> 套用到 <em class="replaceable"><code>context_item</code></em> 時產生任何項目，就回傳 true，否則回傳 false。
       </p></li><li class="listitem"><p>
        <code class="literal">ON ERROR</code> 子句指定在 <em class="replaceable"><code>path_expression</code></em> 求值期間發生錯誤時的行為。指定 <code class="literal">ERROR</code> 會拋出帶有適當訊息的錯誤。其他選項包括回傳 <code class="type">boolean</code> 值 <code class="literal">FALSE</code> 或 <code class="literal">TRUE</code>，或是值 <code class="literal">UNKNOWN</code>（實際上就是 SQL NULL）。沒有指定 <code class="literal">ON ERROR</code> 子句時，預設是回傳 <code class="type">boolean</code> 值 <code class="literal">FALSE</code>。
       </p></li></ul></div>
<p>
        範例：
       </p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"key1": [1,2,3]}', 'strict $.key1[*] ? (@ &gt; $x)' PASSING 2 AS x)</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'lax $.a[5]' ERROR ON ERROR)</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'strict $.a[5]' ERROR ON ERROR)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  jsonpath array subscript is out of bounds
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.2.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_QUERY</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>]
[<span class="optional"> { <code class="literal">WITHOUT</code> | <code class="literal">WITH</code> { <code class="literal">CONDITIONAL</code> | [<span class="optional"><code class="literal">UNCONDITIONAL</code></span>] } } [<span class="optional"> <code class="literal">ARRAY</code> </span>] <code class="literal">WRAPPER</code> </span>]
[<span class="optional"> { <code class="literal">KEEP</code> | <code class="literal">OMIT</code> } <code class="literal">QUOTES</code> [<span class="optional"> <code class="literal">ON SCALAR STRING</code> </span>] </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">jsonb</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        回傳將 SQL/JSON <em class="replaceable"><code>path_expression</code></em> 套用到 <em class="replaceable"><code>context_item</code></em> 的結果。
       </p></li><li class="listitem"><p>
         預設情況下，結果會以 <code class="type">jsonb</code> 型別的值回傳，不過可以使用 <code class="literal">RETURNING</code> 子句，以其他可以成功強制轉換的型別回傳。
       </p></li><li class="listitem"><p>
        如果路徑運算式可能回傳多個值，可能就需要使用 <code class="literal">WITH WRAPPER</code> 子句將這些值包裝起來，使其成為有效的 JSON 字串，因為預設行為是不包裝它們，就如同指定了 <code class="literal">WITHOUT WRAPPER</code> 一樣。<code class="literal">WITH WRAPPER</code> 子句預設被視為 <code class="literal">WITH UNCONDITIONAL WRAPPER</code>，這表示即使只有單一結果值也會被包裝。若只想在有多個值時才套用包裝，請指定 <code class="literal">WITH CONDITIONAL WRAPPER</code>。如果指定了 <code class="literal">WITHOUT WRAPPER</code>，結果中出現多個值會被視為錯誤。
       </p></li><li class="listitem"><p>
        如果結果是純量字串，預設情況下，回傳的值會以引號括起來，使其成為有效的 JSON 值。可以透過指定 <code class="literal">KEEP QUOTES</code> 來明確表示這一點。相反地，可以透過指定 <code class="literal">OMIT QUOTES</code> 來省略引號。為了確保結果是有效的 JSON 值，<code class="literal">OMIT QUOTES</code> 不能與 <code class="literal">WITH WRAPPER</code> 同時指定。
       </p></li><li class="listitem"><p>
        <code class="literal">ON EMPTY</code> 子句指定當 <em class="replaceable"><code>path_expression</code></em> 的求值產生空集合時的行為。<code class="literal">ON ERROR</code> 子句則指定在下列情況發生錯誤時的行為：對 <em class="replaceable"><code>path_expression</code></em> 求值時、將結果值強制轉換為 <code class="literal">RETURNING</code> 型別時，或是對 <code class="literal">ON EMPTY</code> 運算式求值時（此時 <em class="replaceable"><code>path_expression</code></em> 的求值回傳了空集合）。
       </p></li><li class="listitem"><p>
        對於 <code class="literal">ON EMPTY</code> 與 <code class="literal">ON ERROR</code> 兩者，指定 <code class="literal">ERROR</code> 都會拋出帶有適當訊息的錯誤。其他選項包括回傳 SQL NULL、空陣列（<code class="literal">EMPTY [<span class="optional">ARRAY</span>]</code>）、空物件（<code class="literal">EMPTY OBJECT</code>），或是使用者指定的運算式（<code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em>），且該運算式可以強制轉換為 jsonb 或 <code class="literal">RETURNING</code> 中所指定的型別。未指定 <code class="literal">ON EMPTY</code> 或 <code class="literal">ON ERROR</code> 時，預設是回傳 SQL NULL 值。
       </p></li></ul></div>
<p>
        範例：
       </p>
<p>
<code class="literal">JSON_QUERY(jsonb '[1,[2,3],null]', 'lax $[*][$off]' PASSING 1 AS off WITH CONDITIONAL WRAPPER)</code>
        → <code class="returnvalue">3</code>
</p>
<p>
<code class="literal">JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' OMIT QUOTES)</code>
        → <code class="returnvalue">[1, 2]</code>
</p>
<p>
<code class="literal">JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' RETURNING int[] OMIT QUOTES ERROR ON ERROR)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  malformed array literal: "[1, 2]"
DETAIL:  Missing "]" after array dimensions.
</pre><p>
</p>
</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.3.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_VALUE</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">text</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        回傳將 SQL/JSON <em class="replaceable"><code>path_expression</code></em> 套用到 <em class="replaceable"><code>context_item</code></em> 的結果。
       </p></li><li class="listitem"><p>
        只有在預期擷取出的值是單一的 <acronym class="acronym">SQL/JSON</acronym> 純量項目時，才使用 <code class="function">JSON_VALUE()</code>；取得多個值會被視為錯誤。如果你預期擷取出的值可能是物件或陣列，請改用 <code class="function">JSON_QUERY</code> 函式。
       </p></li><li class="listitem"><p>
        預設情況下，結果（必須是單一純量值）會以 <code class="type">text</code> 型別的值回傳，不過可以使用 <code class="literal">RETURNING</code> 子句，以其他可以成功強制轉換的型別回傳。
       </p></li><li class="listitem"><p>
        <code class="literal">ON ERROR</code> 與 <code class="literal">ON EMPTY</code> 子句的語意與 <code class="function">JSON_QUERY</code> 的說明中所述者類似，差別在於用來取代拋出錯誤而回傳的值的集合不同。
       </p></li><li class="listitem"><p>
        請注意，<code class="function">JSON_VALUE</code> 回傳的純量字串一律會去除其引號，等同於指定了 <code class="literal">OMIT QUOTES</code> 的 <code class="function">JSON_QUERY</code>。
       </p></li></ul></div>
<p>
        範例：
       </p>
<p>
<code class="literal">JSON_VALUE(jsonb '"123.45"', '$' RETURNING float)</code>
        → <code class="returnvalue">123.45</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '"03:04 2015-02-01"', '$.datetime("HH24:MI YYYY-MM-DD")' RETURNING date)</code>
        → <code class="returnvalue">2015-02-01</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '[1,2]', 'strict $[$off]' PASSING 1 as off)</code>
        → <code class="returnvalue">2</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '[1,2]', 'strict $[*]' DEFAULT 9 ON ERROR)</code>
        → <code class="returnvalue">9</code>
</p>
</td></tr></tbody></table>

<br>

### 注意 [#](#zhu-yi-2) <a href="#zhu-yi-2" id="zhu-yi-2"></a>

如果 *`context_item`* 運算式的型別還不是 `jsonb`，它會透過隱含的型別轉換轉為 `jsonb`。不過請注意，在該轉換過程中發生的任何剖析錯誤都會無條件拋出，也就是說，不會依照（明確指定或隱含的）`ON ERROR` 子句來處理。

### 注意 [#](#zhu-yi-3) <a href="#zhu-yi-3" id="zhu-yi-3"></a>

如果 *`path_expression`* 回傳 JSON `null`，`JSON_VALUE()` 會回傳 SQL NULL，而 `JSON_QUERY()` 則會原樣回傳 JSON `null`。

[返回 9.16. JSON 函式與運算子](../functions-json.md#functions-json)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（原文版本：18.6；核對日期：2026-09-11）
