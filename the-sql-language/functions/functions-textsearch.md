<a id="FUNCTIONS-TEXTSEARCH"></a>

## 9.13. 文字搜尋函式與運算子 [#](#FUNCTIONS-TEXTSEARCH)

<a id="id-1.5.8.19.2"></a><a id="id-1.5.8.19.3"></a>

[表 9.42](functions-textsearch.md#TEXTSEARCH-OPERATORS-TABLE)、[表 9.43](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-TABLE) 與[表 9.44](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-DEBUG-TABLE) 彙整了為全文檢索所提供的函式與運算子。關於 PostgreSQL 文字搜尋功能的詳細說明，請參閱[第 12 章](../textsearch/README.md)。

<a id="TEXTSEARCH-OPERATORS-TABLE"></a>

**表 9.42. 文字搜尋運算子**

<table border="1" class="table" summary="Text Search Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsvector</code> <code class="literal">@@</code> <code class="type">tsquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">tsquery</code> <code class="literal">@@</code> <code class="type">tsvector</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">tsvector</code> 是否與 <code class="type">tsquery</code> 相符？（引數可以用任何順序給定。）
       </p>
<p>
<code class="literal">to_tsvector('fat cats ate rats') @@ to_tsquery('cat &amp; rat')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">@@</code> <code class="type">tsquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        文字字串在隱含地呼叫 <code class="function">to_tsvector()</code> 之後，是否與 <code class="type">tsquery</code> 相符？
       </p>
<p>
<code class="literal">'fat cats ate rats' @@ to_tsquery('cat &amp; rat')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsvector</code> <code class="literal">||</code> <code class="type">tsvector</code>
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        串接兩個 <code class="type">tsvector</code>。如果兩個輸入都包含詞素位置，第二個輸入的位置會相應地調整。
       </p>
<p>
<code class="literal">'a:1 b:2'::tsvector || 'c:1 d:2 b:3'::tsvector</code>
        → <code class="returnvalue">'a':1 'b':2,5 'c':3 'd':4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsquery</code> <code class="literal">&amp;&amp;</code> <code class="type">tsquery</code>
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將兩個 <code class="type">tsquery</code> 以 AND 結合，產生一個與同時符合兩個輸入查詢之文件相符的查詢。
       </p>
<p>
<code class="literal">'fat | rat'::tsquery &amp;&amp; 'cat'::tsquery</code>
        → <code class="returnvalue">( 'fat' | 'rat' ) &amp; 'cat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsquery</code> <code class="literal">||</code> <code class="type">tsquery</code>
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將兩個 <code class="type">tsquery</code> 以 OR 結合，產生一個與符合任一輸入查詢之文件相符的查詢。
       </p>
<p>
<code class="literal">'fat | rat'::tsquery || 'cat'::tsquery</code>
        → <code class="returnvalue">'fat' | 'rat' | 'cat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">!!</code> <code class="type">tsquery</code>
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        否定一個 <code class="type">tsquery</code>，產生一個與不符合輸入查詢之文件相符的查詢。
       </p>
<p>
<code class="literal">!! 'cat'::tsquery</code>
        → <code class="returnvalue">!'cat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsquery</code> <code class="literal">&lt;-&gt;</code> <code class="type">tsquery</code>
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        建構一個片語查詢，當兩個輸入查詢在連續的詞素上相符時，它就相符。
       </p>
<p>
<code class="literal">to_tsquery('fat') &lt;-&gt; to_tsquery('rat')</code>
        → <code class="returnvalue">'fat' &lt;-&gt; 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsquery</code> <code class="literal">@&gt;</code> <code class="type">tsquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">tsquery</code> 是否包含第二個？（這只考慮出現在一個查詢中的所有詞素是否都出現在另一個查詢中，而忽略組合運算子。）
       </p>
<p>
<code class="literal">'cat'::tsquery @&gt; 'cat &amp; rat'::tsquery</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">tsquery</code> <code class="literal">&lt;@</code> <code class="type">tsquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">tsquery</code> 是否被第二個包含？（這只考慮出現在一個查詢中的所有詞素是否都出現在另一個查詢中，而忽略組合運算子。）
       </p>
<p>
<code class="literal">'cat'::tsquery &lt;@ 'cat &amp; rat'::tsquery</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">'cat'::tsquery &lt;@ '!cat &amp; rat'::tsquery</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

除了這些特殊運算子之外，`tsvector` 與 `tsquery` 型別也可以使用[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子。這些運算子對文字搜尋不是很有用，但它們讓你可以在這些型別的欄位上建立唯一索引等等。

<a id="TEXTSEARCH-FUNCTIONS-TABLE"></a>

**表 9.43. 文字搜尋函式**

<table border="1" class="table" summary="Text Search Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.1.1.1.1"></a>
<code class="function">array_to_tsvector</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將文字字串陣列轉換為 <code class="type">tsvector</code>。給定的字串會原樣用作詞素，不做進一步處理。陣列元素不得為空字串或 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">array_to_tsvector('{fat,cat,rat}'::text[])</code>
        → <code class="returnvalue">'cat' 'fat' 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.2.1.1.1"></a>
<code class="function">get_current_ts_config</code> ( )
        → <code class="returnvalue">regconfig</code>
</p>
<p>
        回傳目前預設文字搜尋組態（由 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG">default_text_search_config</a> 設定）的 OID。
       </p>
<p>
<code class="literal">get_current_ts_config()</code>
        → <code class="returnvalue">english</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.3.1.1.1"></a>
<code class="function">length</code> ( <code class="type">tsvector</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 <code class="type">tsvector</code> 中的詞素數量。
       </p>
<p>
<code class="literal">length('fat:2,4 cat:3 rat:5A'::tsvector)</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.4.1.1.1"></a>
<code class="function">numnode</code> ( <code class="type">tsquery</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 <code class="type">tsquery</code> 中的詞素數量加上運算子數量。
       </p>
<p>
<code class="literal">numnode('(fat &amp; rat) | cat'::tsquery)</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.5.1.1.1"></a>
<code class="function">plainto_tsquery</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將文字轉換為 <code class="type">tsquery</code>，並依照指定的或預設的組態將單字正規化。字串中的任何標點符號都會被忽略（它不會決定查詢運算子）。產生的查詢會與包含該文字中所有非停用詞的文件相符。
       </p>
<p>
<code class="literal">plainto_tsquery('english', 'The Fat Rats')</code>
        → <code class="returnvalue">'fat' &amp; 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.6.1.1.1"></a>
<code class="function">phraseto_tsquery</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將文字轉換為 <code class="type">tsquery</code>，並依照指定的或預設的組態將單字正規化。字串中的任何標點符號都會被忽略（它不會決定查詢運算子）。產生的查詢會與包含該文字中所有非停用詞的片語相符。
       </p>
<p>
<code class="literal">phraseto_tsquery('english', 'The Fat Rats')</code>
        → <code class="returnvalue">'fat' &lt;-&gt; 'rat'</code>
</p>
<p>
<code class="literal">phraseto_tsquery('english', 'The Cat and Rats')</code>
        → <code class="returnvalue">'cat' &lt;2&gt; 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.7.1.1.1"></a>
<code class="function">websearch_to_tsquery</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將文字轉換為 <code class="type">tsquery</code>，並依照指定的或預設的組態將單字正規化。加上引號的單字序列會被轉換為片語測試。單字<span class="quote">“<span class="quote">or</span>”</span>會被理解為產生 OR 運算子，而破折號會產生 NOT 運算子；其他標點符號則會被忽略。這近似於一些常見網路搜尋工具的行為。
       </p>
<p>
<code class="literal">websearch_to_tsquery('english', '"fat rat" or cat dog')</code>
        → <code class="returnvalue">'fat' &lt;-&gt; 'rat' | 'cat' &amp; 'dog'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.8.1.1.1"></a>
<code class="function">querytree</code> ( <code class="type">tsquery</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        產生 <code class="type">tsquery</code> 中可索引部分的表示。結果為空或只有 <code class="literal">T</code> 時，表示該查詢無法使用索引。
       </p>
<p>
<code class="literal">querytree('foo &amp; ! bar'::tsquery)</code>
        → <code class="returnvalue">'foo'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.9.1.1.1"></a>
<code class="function">setweight</code> ( <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>, <em class="parameter"><code>weight</code></em> <code class="type">"char"</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將指定的 <em class="parameter"><code>weight</code></em> 指派給 <em class="parameter"><code>vector</code></em> 的每個元素。
       </p>
<p>
<code class="literal">setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A')</code>
        → <code class="returnvalue">'cat':3A 'fat':2A,4A 'rat':5A</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.10.1.1.1"></a>
<code class="function">setweight</code> ( <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>, <em class="parameter"><code>weight</code></em> <code class="type">"char"</code>, <em class="parameter"><code>lexemes</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將指定的 <em class="parameter"><code>weight</code></em> 指派給 <em class="parameter"><code>vector</code></em> 中列在 <em class="parameter"><code>lexemes</code></em> 裡的元素。<em class="parameter"><code>lexemes</code></em> 中的字串會原樣作為詞素，不做進一步處理。與 <em class="parameter"><code>vector</code></em> 中任何詞素都不相符的字串會被忽略。
       </p>
<p>
<code class="literal">setweight('fat:2,4 cat:3 rat:5,6B'::tsvector, 'A', '{cat,rat}')</code>
        → <code class="returnvalue">'cat':3A 'fat':2,4 'rat':5A,6A</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.11.1.1.1"></a>
<code class="function">strip</code> ( <code class="type">tsvector</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        從 <code class="type">tsvector</code> 中移除位置與權重。
       </p>
<p>
<code class="literal">strip('fat:2,4 cat:3 rat:5A'::tsvector)</code>
        → <code class="returnvalue">'cat' 'fat' 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.12.1.1.1"></a>
<code class="function">to_tsquery</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將文字轉換為 <code class="type">tsquery</code>，並依照指定的或預設的組態將單字正規化。單字必須以有效的 <code class="type">tsquery</code> 運算子組合。
       </p>
<p>
<code class="literal">to_tsquery('english', 'The &amp; Fat &amp; Rats')</code>
        → <code class="returnvalue">'fat' &amp; 'rat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.13.1.1.1"></a>
<code class="function">to_tsvector</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
         <em class="parameter"><code>document</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將文字轉換為 <code class="type">tsvector</code>，並依照指定的或預設的組態將單字正規化。結果中會包含位置資訊。
       </p>
<p>
<code class="literal">to_tsvector('english', 'The Fat Rats')</code>
        → <code class="returnvalue">'fat':2 'rat':3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">to_tsvector</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">json</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p class="func_signature">
<code class="function">to_tsvector</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將 JSON 文件中的每個字串值轉換為 <code class="type">tsvector</code>，並依照指定的或預設的組態將單字正規化。接著依文件順序串接這些結果以產生輸出。產生位置資訊時，就好像每一對字串值之間存在一個停用詞。（請注意，當輸入為 <code class="type">jsonb</code> 時，JSON 物件之欄位的<span class="quote">“<span class="quote">文件順序</span>”</span>取決於實作；請留意範例中的差異。）
       </p>
<p>
<code class="literal">to_tsvector('english', '{"aa": "The Fat Rats", "b": "dog"}'::json)</code>
        → <code class="returnvalue">'dog':5 'fat':2 'rat':3</code>
</p>
<p>
<code class="literal">to_tsvector('english', '{"aa": "The Fat Rats", "b": "dog"}'::jsonb)</code>
        → <code class="returnvalue">'dog':1 'fat':4 'rat':5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.15.1.1.1"></a>
<code class="function">json_to_tsvector</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">json</code>,
        <em class="parameter"><code>filter</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.15.1.2.1"></a>
<code class="function">jsonb_to_tsvector</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">jsonb</code>,
        <em class="parameter"><code>filter</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        選取 JSON 文件中 <em class="parameter"><code>filter</code></em> 所要求的每個項目，並將每個項目轉換為 <code class="type">tsvector</code>，依照指定的或預設的組態將單字正規化。接著依文件順序串接這些結果以產生輸出。產生位置資訊時，就好像每一對選取的項目之間存在一個停用詞。（請注意，當輸入為 <code class="type">jsonb</code> 時，JSON 物件之欄位的<span class="quote">“<span class="quote">文件順序</span>”</span>取決於實作。）<em class="parameter"><code>filter</code></em> 必須是一個 <code class="type">jsonb</code> 陣列，包含零個或多個下列關鍵字：<code class="literal">"string"</code>（包含所有字串值）、<code class="literal">"numeric"</code>（包含所有數值）、<code class="literal">"boolean"</code>（包含所有布林值）、<code class="literal">"key"</code>（包含所有鍵），或 <code class="literal">"all"</code>（包含以上全部）。作為特例，<em class="parameter"><code>filter</code></em> 也可以是屬於這些關鍵字之一的簡單 JSON 值。
       </p>
<p>
<code class="literal">json_to_tsvector('english', '{"a": "The Fat Rats", "b": 123}'::json, '["string", "numeric"]')</code>
        → <code class="returnvalue">'123':5 'fat':2 'rat':3</code>
</p>
<p>
<code class="literal">json_to_tsvector('english', '{"cat": "The Fat Rats", "dog": 123}'::json, '"all"')</code>
        → <code class="returnvalue">'123':9 'cat':1 'dog':7 'fat':4 'rat':5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.16.1.1.1"></a>
<code class="function">ts_delete</code> ( <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>, <em class="parameter"><code>lexeme</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將所有出現的給定 <em class="parameter"><code>lexeme</code></em> 從 <em class="parameter"><code>vector</code></em> 中移除。<em class="parameter"><code>lexeme</code></em> 字串會原樣視為詞素，不做進一步處理。
       </p>
<p>
<code class="literal">ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, 'fat')</code>
        → <code class="returnvalue">'cat':3 'rat':5A</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ts_delete</code> ( <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>, <em class="parameter"><code>lexemes</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        將出現於 <em class="parameter"><code>lexemes</code></em> 中的詞素全部從 <em class="parameter"><code>vector</code></em> 中移除。<em class="parameter"><code>lexemes</code></em> 中的字串會原樣作為詞素，不做進一步處理。與 <em class="parameter"><code>vector</code></em> 中任何詞素都不相符的字串會被忽略。
       </p>
<p>
<code class="literal">ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, ARRAY['fat','rat'])</code>
        → <code class="returnvalue">'cat':3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.18.1.1.1"></a>
<code class="function">ts_filter</code> ( <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>, <em class="parameter"><code>weights</code></em> <code class="type">"char"[]</code> )
        → <code class="returnvalue">tsvector</code>
</p>
<p>
        只選取具有給定 <em class="parameter"><code>weights</code></em> 的 <em class="parameter"><code>vector</code></em> 元素。
       </p>
<p>
<code class="literal">ts_filter('fat:2,4 cat:3b,7c rat:5A'::tsvector, '{a,b}')</code>
        → <code class="returnvalue">'cat':3B 'rat':5A</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.19.1.1.1"></a>
<code class="function">ts_headline</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">text</code>,
        <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>
        [<span class="optional">, <em class="parameter"><code>options</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        以縮略的形式顯示 <em class="parameter"><code>query</code></em> 在 <em class="parameter"><code>document</code></em> 中的相符之處，其中文件必須是原始文字，而不是 <code class="type">tsvector</code>。文件中的單字在與查詢比對之前，會依照指定的或預設的組態進行正規化。這個函式的用法在<a class="xref" href="../textsearch/textsearch-controls.md#TEXTSEARCH-HEADLINE">第 12.3.4 節</a>中討論，該節也說明了可用的 <em class="parameter"><code>options</code></em>。
       </p>
<p>
<code class="literal">ts_headline('The fat cat ate the rat.', 'cat')</code>
        → <code class="returnvalue">The fat &lt;b&gt;cat&lt;/b&gt; ate the rat.</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ts_headline</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">json</code>,
        <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>
        [<span class="optional">, <em class="parameter"><code>options</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">ts_headline</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">jsonb</code>,
        <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>
        [<span class="optional">, <em class="parameter"><code>options</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        以縮略的形式顯示 <em class="parameter"><code>query</code></em> 在 JSON <em class="parameter"><code>document</code></em> 之字串值中的相符之處。更多細節請參閱<a class="xref" href="../textsearch/textsearch-controls.md#TEXTSEARCH-HEADLINE">第 12.3.4 節</a>。
       </p>
<p>
<code class="literal">ts_headline('{"cat":"raining cats and dogs"}'::jsonb, 'cat')</code>
        → <code class="returnvalue">{"cat": "raining &lt;b&gt;cats&lt;/b&gt; and dogs"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.21.1.1.1"></a>
<code class="function">ts_rank</code> (
        [<span class="optional"> <em class="parameter"><code>weights</code></em> <code class="type">real[]</code>, </span>]
        <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>,
        <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>
        [<span class="optional">, <em class="parameter"><code>normalization</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">real</code>
</p>
<p>
        計算一個分數，顯示 <em class="parameter"><code>vector</code></em> 與 <em class="parameter"><code>query</code></em> 的相符程度。詳情請參閱<a class="xref" href="../textsearch/textsearch-controls.md#TEXTSEARCH-RANKING">第 12.3.3 節</a>。
       </p>
<p>
<code class="literal">ts_rank(to_tsvector('raining cats and dogs'), 'cat')</code>
        → <code class="returnvalue">0.06079271</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.22.1.1.1"></a>
<code class="function">ts_rank_cd</code> (
        [<span class="optional"> <em class="parameter"><code>weights</code></em> <code class="type">real[]</code>, </span>]
        <em class="parameter"><code>vector</code></em> <code class="type">tsvector</code>,
        <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>
        [<span class="optional">, <em class="parameter"><code>normalization</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">real</code>
</p>
<p>
        使用涵蓋密度（cover density）演算法，計算一個分數，顯示 <em class="parameter"><code>vector</code></em> 與 <em class="parameter"><code>query</code></em> 的相符程度。詳情請參閱<a class="xref" href="../textsearch/textsearch-controls.md#TEXTSEARCH-RANKING">第 12.3.3 節</a>。
       </p>
<p>
<code class="literal">ts_rank_cd(to_tsvector('raining cats and dogs'), 'cat')</code>
        → <code class="returnvalue">0.1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.23.1.1.1"></a>
<code class="function">ts_rewrite</code> ( <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>,
        <em class="parameter"><code>target</code></em> <code class="type">tsquery</code>,
        <em class="parameter"><code>substitute</code></em> <code class="type">tsquery</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        將出現的 <em class="parameter"><code>target</code></em> 替換為 <em class="parameter"><code>substitute</code></em>，替換範圍限於 <em class="parameter"><code>query</code></em> 之內。詳情請參閱<a class="xref" href="../textsearch/textsearch-features.md#TEXTSEARCH-QUERY-REWRITING">第 12.4.2.1 節</a>。
       </p>
<p>
<code class="literal">ts_rewrite('a &amp; b'::tsquery, 'a'::tsquery, 'foo|bar'::tsquery)</code>
        → <code class="returnvalue">'b' &amp; ( 'foo' | 'bar' )</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ts_rewrite</code> ( <em class="parameter"><code>query</code></em> <code class="type">tsquery</code>,
        <em class="parameter"><code>select</code></em> <code class="type">text</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        替換 <em class="parameter"><code>query</code></em> 的部分內容，依據的是執行 <code class="command">SELECT</code> 命令所取得的目標與替代項目。詳情請參閱<a class="xref" href="../textsearch/textsearch-features.md#TEXTSEARCH-QUERY-REWRITING">第 12.4.2.1 節</a>。
       </p>
<p>
<code class="literal">SELECT ts_rewrite('a &amp; b'::tsquery, 'SELECT t,s FROM aliases')</code>
        → <code class="returnvalue">'b' &amp; ( 'foo' | 'bar' )</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.25.1.1.1"></a>
<code class="function">tsquery_phrase</code> ( <em class="parameter"><code>query1</code></em> <code class="type">tsquery</code>, <em class="parameter"><code>query2</code></em> <code class="type">tsquery</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        建構一個片語查詢，搜尋 <em class="parameter"><code>query1</code></em> 與 <em class="parameter"><code>query2</code></em> 在連續詞素上的相符（與 <code class="literal">&lt;-&gt;</code> 運算子相同）。
       </p>
<p>
<code class="literal">tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'))</code>
        → <code class="returnvalue">'fat' &lt;-&gt; 'cat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">tsquery_phrase</code> ( <em class="parameter"><code>query1</code></em> <code class="type">tsquery</code>, <em class="parameter"><code>query2</code></em> <code class="type">tsquery</code>, <em class="parameter"><code>distance</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">tsquery</code>
</p>
<p>
        建構一個片語查詢，搜尋 <em class="parameter"><code>query1</code></em> 與 <em class="parameter"><code>query2</code></em> 恰好相隔 <em class="parameter"><code>distance</code></em> 個詞素出現的相符。
       </p>
<p>
<code class="literal">tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10)</code>
        → <code class="returnvalue">'fat' &lt;10&gt; 'cat'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.27.1.1.1"></a>
<code class="function">tsvector_to_array</code> ( <code class="type">tsvector</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">tsvector</code> 轉換為詞素陣列。
       </p>
<p>
<code class="literal">tsvector_to_array('fat:2,4 cat:3 rat:5A'::tsvector)</code>
        → <code class="returnvalue">{cat,fat,rat}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.7.2.2.28.1.1.1"></a>
<code class="function">unnest</code> ( <code class="type">tsvector</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>lexeme</code></em> <code class="type">text</code>,
        <em class="parameter"><code>positions</code></em> <code class="type">smallint[]</code>,
        <em class="parameter"><code>weights</code></em> <code class="type">text</code> )
       </p>
<p>
        將 <code class="type">tsvector</code> 展開成一組資料列，每個詞素一筆。
       </p>
<p>
<code class="literal">select * from unnest('cat:3 fat:2,4 rat:5A'::tsvector)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 lexeme | positions | weights
--------+-----------+---------
 cat    | {3}       | {D}
 fat    | {2,4}     | {D,D}
 rat    | {5}       | {A}
</pre><p>
</p></td></tr></tbody></table>

<br>

### 注意

所有接受選用 `regconfig` 引數的文字搜尋函式，在省略該引數時，都會使用 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) 所指定的組態。

[表 9.44](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-DEBUG-TABLE) 中的函式之所以另外列出，是因為它們通常不會用在日常的文字搜尋操作中。它們主要有助於開發與除錯新的文字搜尋組態。

<a id="TEXTSEARCH-FUNCTIONS-DEBUG-TABLE"></a>

**表 9.44. 文字搜尋除錯函式**

<table border="1" class="table" summary="Text Search Debugging Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.10.2.2.1.1.1.1"></a>
<code class="function">ts_debug</code> (
        [<span class="optional"> <em class="parameter"><code>config</code></em> <code class="type">regconfig</code>, </span>]
        <em class="parameter"><code>document</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>alias</code></em> <code class="type">text</code>,
        <em class="parameter"><code>description</code></em> <code class="type">text</code>,
        <em class="parameter"><code>token</code></em> <code class="type">text</code>,
        <em class="parameter"><code>dictionaries</code></em> <code class="type">regdictionary[]</code>,
        <em class="parameter"><code>dictionary</code></em> <code class="type">regdictionary</code>,
        <em class="parameter"><code>lexemes</code></em> <code class="type">text[]</code> )
       </p>
<p>
        依照指定的或預設的文字搜尋組態，從 <em class="parameter"><code>document</code></em> 中擷取並正規化語彙單元，並回傳每個語彙單元如何被處理的資訊。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-CONFIGURATION-TESTING">第 12.8.1 節</a>。
       </p>
<p>
<code class="literal">ts_debug('english', 'The Brightest supernovaes')</code>
        → <code class="returnvalue">(asciiword,"Word, all ASCII",The,{english_stem},english_stem,{}) ...</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.10.2.2.2.1.1.1"></a>
<code class="function">ts_lexize</code> ( <em class="parameter"><code>dict</code></em> <code class="type">regdictionary</code>, <em class="parameter"><code>token</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        如果字典認得輸入的語彙單元，就回傳替換詞素的陣列；如果字典認得該語彙單元但它是停用詞，就回傳空陣列；如果它不是已知的單字，則回傳 NULL。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-DICTIONARY-TESTING">第 12.8.3 節</a>。
       </p>
<p>
<code class="literal">ts_lexize('english_stem', 'stars')</code>
        → <code class="returnvalue">{star}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.10.2.2.3.1.1.1"></a>
<code class="function">ts_parse</code> ( <em class="parameter"><code>parser_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>document</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tokid</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>token</code></em> <code class="type">text</code> )
       </p>
<p>
        使用指定名稱的剖析器，從 <em class="parameter"><code>document</code></em> 中擷取語彙單元。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING">第 12.8.2 節</a>。
       </p>
<p>
<code class="literal">ts_parse('default', 'foo - bar')</code>
        → <code class="returnvalue">(1,foo) ...</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ts_parse</code> ( <em class="parameter"><code>parser_oid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>document</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tokid</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>token</code></em> <code class="type">text</code> )
       </p>
<p>
        使用以 OID 指定的剖析器，從 <em class="parameter"><code>document</code></em> 中擷取語彙單元。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING">第 12.8.2 節</a>。
       </p>
<p>
<code class="literal">ts_parse(3722, 'foo - bar')</code>
        → <code class="returnvalue">(1,foo) ...</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.10.2.2.5.1.1.1"></a>
<code class="function">ts_token_type</code> ( <em class="parameter"><code>parser_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tokid</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>alias</code></em> <code class="type">text</code>,
        <em class="parameter"><code>description</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳一個資料表，描述指定名稱的剖析器能夠辨識的每一種語彙單元類型。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING">第 12.8.2 節</a>。
       </p>
<p>
<code class="literal">ts_token_type('default')</code>
        → <code class="returnvalue">(1,asciiword,"Word, all ASCII") ...</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ts_token_type</code> ( <em class="parameter"><code>parser_oid</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tokid</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>alias</code></em> <code class="type">text</code>,
        <em class="parameter"><code>description</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳一個資料表，描述以 OID 指定的剖析器能夠辨識的每一種語彙單元類型。詳情請參閱<a class="xref" href="../textsearch/textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING">第 12.8.2 節</a>。
       </p>
<p>
<code class="literal">ts_token_type(3722)</code>
        → <code class="returnvalue">(1,asciiword,"Word, all ASCII") ...</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.19.10.2.2.7.1.1.1"></a>
<code class="function">ts_stat</code> ( <em class="parameter"><code>sqlquery</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>weights</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>word</code></em> <code class="type">text</code>,
        <em class="parameter"><code>ndoc</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>nentry</code></em> <code class="type">integer</code> )
       </p>
<p>
        執行 <em class="parameter"><code>sqlquery</code></em>（它必須回傳單一 <code class="type">tsvector</code> 欄位），並回傳資料中所包含之每個相異詞素的統計資訊。詳情請參閱<a class="xref" href="../textsearch/textsearch-features.md#TEXTSEARCH-STATISTICS">第 12.4.4 節</a>。
       </p>
<p>
<code class="literal">ts_stat('SELECT vector FROM apod')</code>
        → <code class="returnvalue">(foo,10,15) ...</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-textsearch.html)（原文版本：18.6；核對日期：2026-09-11）
