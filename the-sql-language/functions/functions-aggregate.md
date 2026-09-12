<a id="FUNCTIONS-AGGREGATE"></a>

## 9.21. 彙總函式 [#](#FUNCTIONS-AGGREGATE)

<a id="id-1.5.8.27.2"></a>

*彙總函式*（aggregate function）會從一組輸入值計算出單一結果。內建的通用彙總函式列於[表 9.62](functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE)，統計用的彙總函式則列於[表 9.63](functions-aggregate.md#FUNCTIONS-AGGREGATE-STATISTICS-TABLE)。內建的組內有序集合彙總函式列於[表 9.64](functions-aggregate.md#FUNCTIONS-ORDEREDSET-TABLE)，而內建的組內假設集合彙總函式則列於[表 9.65](functions-aggregate.md#FUNCTIONS-HYPOTHETICAL-TABLE)。與彙總函式密切相關的分組操作，列於[表 9.66](functions-aggregate.md#FUNCTIONS-GROUPING-TABLE)。彙總函式在語法上的特殊考量，說明於[第 4.2.7 節](../sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)。其他入門資訊請參閱[第 2.7 節](../../tutorial/tutorial-sql/tutorial-agg.md)。

支援*部分模式*（Partial Mode）的彙總函式，可以參與各種最佳化，例如平行彙總。

雖然下列所有彙總函式都接受選用的 `ORDER BY` 子句（如[第 4.2.7 節](../sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)所述），但只有輸出會受到排序影響的彙總函式，才在表中加上了這個子句。

<a id="FUNCTIONS-AGGREGATE-TABLE"></a>

**表 9.62. 通用彙總函式**

<table border="1" class="table" summary="General-Purpose Aggregate Functions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th><th>部分模式</th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.1.1.1.1"></a>
<code class="function">any_value</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue"><em class="replaceable"><code>same as input type</code></em></code>
</p>
<p>
        從非 null 的輸入值中回傳任意一個值。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.2.1.1.1"></a>
<code class="function">array_agg</code> ( <code class="type">anynonarray</code> <code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        將所有輸入值（包括 null）收集成一個陣列。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">array_agg</code> ( <code class="type">anyarray</code> <code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        將所有輸入陣列串接成一個維數多一維的陣列。（所有輸入必須具有相同的維數，而且不能是空的或 null。）
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.4.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.6.2.4.4.1.1.2"></a>
<code class="function">avg</code> ( <code class="type">smallint</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">real</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p class="func_signature">
<code class="function">avg</code> ( <code class="type">interval</code> )
        → <code class="returnvalue">interval</code>
</p>
<p>
        計算所有非 null 輸入值的平均值（算術平均數）。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.5.1.1.1"></a>
<code class="function">bit_and</code> ( <code class="type">smallint</code> )
        → <code class="returnvalue">smallint</code>
</p>
<p class="func_signature">
<code class="function">bit_and</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<code class="function">bit_and</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">bit_and</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">bit</code>
</p>
<p>
        計算所有非 null 輸入值的位元 AND。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.6.1.1.1"></a>
<code class="function">bit_or</code> ( <code class="type">smallint</code> )
        → <code class="returnvalue">smallint</code>
</p>
<p class="func_signature">
<code class="function">bit_or</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<code class="function">bit_or</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">bit_or</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">bit</code>
</p>
<p>
        計算所有非 null 輸入值的位元 OR。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.7.1.1.1"></a>
<code class="function">bit_xor</code> ( <code class="type">smallint</code> )
        → <code class="returnvalue">smallint</code>
</p>
<p class="func_signature">
<code class="function">bit_xor</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<code class="function">bit_xor</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">bit_xor</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">bit</code>
</p>
<p>
        計算所有非 null 輸入值的位元互斥 OR。可以用作無序值集合的檢查碼。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.8.1.1.1"></a>
<code class="function">bool_and</code> ( <code class="type">boolean</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果所有非 null 的輸入值都是 true，就回傳 true，否則回傳 false。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.9.1.1.1"></a>
<code class="function">bool_or</code> ( <code class="type">boolean</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果有任何非 null 的輸入值為 true，就回傳 true，否則回傳 false。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.10.1.1.1"></a>
<code class="function">count</code> ( <code class="literal">*</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算輸入資料列的數量。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">count</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算輸入值不為 null 的輸入資料列數量。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.12.1.1.1"></a>
<code class="function">every</code> ( <code class="type">boolean</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這是 SQL 標準中與 <code class="function">bool_and</code> 等價的函式。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.13.1.1.1"></a>
<code class="function">json_agg</code> ( <code class="type">anyelement</code> <code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.13.1.2.1"></a>
<code class="function">jsonb_agg</code> ( <code class="type">anyelement</code> <code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有輸入值（包括 null）收集成一個 JSON 陣列。值會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換為 JSON。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.14.1.1.1"></a>
<code class="function">json_agg_strict</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.14.1.2.1"></a>
<code class="function">jsonb_agg_strict</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有輸入值（略過 null）收集成一個 JSON 陣列。值會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換為 JSON。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.15.1.1.1"></a>
<code class="function">json_arrayagg</code> (
        [<span class="optional"> <em class="replaceable"><code>value_expression</code></em> </span>]
        [<span class="optional"> <code class="literal">ORDER BY</code> <em class="replaceable"><code>sort_expression</code></em> </span>]
        [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
        [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
       </p>
<p>
        行為與 <code class="function">json_array</code> 相同，但作為彙總函式，因此只接受一個 <em class="replaceable"><code>value_expression</code></em> 參數。如果指定了 <code class="literal">ABSENT ON NULL</code>，任何 NULL 值都會被省略。如果指定了 <code class="literal">ORDER BY</code>，元素會依該順序出現在陣列中，而不是依輸入順序。
       </p>
<p>
<code class="literal">SELECT json_arrayagg(v) FROM (VALUES(2),(1)) t(v)</code>
        → <code class="returnvalue">[2, 1]</code>
</p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.16.1.1.1"></a>
<code class="function">json_objectagg</code> (
         [<span class="optional"> { <em class="replaceable"><code>key_expression</code></em> { <code class="literal">VALUE</code> | ':' } <em class="replaceable"><code>value_expression</code></em> } </span>]
         [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
        [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>] </span>]
        [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p>
         行為類似 <code class="function">json_object</code>，但作為彙總函式，因此只接受一個 <em class="replaceable"><code>key_expression</code></em> 參數與一個 <em class="replaceable"><code>value_expression</code></em> 參數。
        </p>
<p>
<code class="literal">SELECT json_objectagg(k:v) FROM (VALUES ('a'::text,current_date),('b',current_date + 1)) AS t(k,v)</code>
         → <code class="returnvalue">{ "a" : "2022-05-10", "b" : "2022-05-11" }</code>
</p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.17.1.1.1"></a>
<code class="function">json_object_agg</code> ( <em class="parameter"><code>key</code></em>
<code class="type">"any"</code>, <em class="parameter"><code>value</code></em>
<code class="type">"any"</code>
<code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.17.1.2.1"></a>
<code class="function">jsonb_object_agg</code> ( <em class="parameter"><code>key</code></em>
<code class="type">"any"</code>, <em class="parameter"><code>value</code></em>
<code class="type">"any"</code>
<code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有鍵／值配對收集成一個 JSON 物件。鍵引數會被強制轉換為文字；值引數會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。值可以是 null，但鍵不可以。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.18.1.1.1"></a>
<code class="function">json_object_agg_strict</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.18.1.2.1"></a>
<code class="function">jsonb_object_agg_strict</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有鍵／值配對收集成一個 JSON 物件。鍵引數會被強制轉換為文字；值引數會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。<em class="parameter"><code>key</code></em> 不能是 null。如果 <em class="parameter"><code>value</code></em> 為 null，該項目就會被略過，
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.19.1.1.1"></a>
<code class="function">json_object_agg_unique</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.19.1.2.1"></a>
<code class="function">jsonb_object_agg_unique</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有鍵／值配對收集成一個 JSON 物件。鍵引數會被強制轉換為文字；值引數會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。值可以是 null，但鍵不可以。如果有重複的鍵，就會引發錯誤。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.20.1.1.1"></a>
<code class="function">json_object_agg_unique_strict</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.20.1.2.1"></a>
<code class="function">jsonb_object_agg_unique_strict</code> (
         <em class="parameter"><code>key</code></em> <code class="type">"any"</code>,
         <em class="parameter"><code>value</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將所有鍵／值配對收集成一個 JSON 物件。鍵引數會被強制轉換為文字；值引數會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。<em class="parameter"><code>key</code></em> 不能是 null。如果 <em class="parameter"><code>value</code></em> 為 null，該項目就會被略過。如果有重複的鍵，就會引發錯誤。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.21.1.1.1"></a>
<code class="function">max</code> ( <em class="replaceable"><code>see text</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>same as input type</code></em></code>
</p>
<p>
        計算非 null 輸入值中的最大值。適用於任何數值、字串、日期／時間或列舉型別，以及 <code class="type">bytea</code>、<code class="type">inet</code>、<code class="type">interval</code>、<code class="type">money</code>、<code class="type">oid</code>、<code class="type">pg_lsn</code>、<code class="type">tid</code>、<code class="type">xid8</code>，還有包含可排序資料型別的陣列與複合型別。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.22.1.1.1"></a>
<code class="function">min</code> ( <em class="replaceable"><code>see text</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>same as input type</code></em></code>
</p>
<p>
        計算非 null 輸入值中的最小值。適用於任何數值、字串、日期／時間或列舉型別，以及 <code class="type">bytea</code>、<code class="type">inet</code>、<code class="type">interval</code>、<code class="type">money</code>、<code class="type">oid</code>、<code class="type">pg_lsn</code>、<code class="type">tid</code>、<code class="type">xid8</code>，還有包含可排序資料型別的陣列與複合型別。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.23.1.1.1"></a>
<code class="function">range_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">anyrange</code> )
        → <code class="returnvalue">anymultirange</code>
</p>
<p class="func_signature">
<code class="function">range_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">anymultirange</code> )
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        計算非 null 輸入值的聯集。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.24.1.1.1"></a>
<code class="function">range_intersect_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">anyrange</code> )
        → <code class="returnvalue">anyrange</code>
</p>
<p class="func_signature">
<code class="function">range_intersect_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">anymultirange</code> )
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        計算非 null 輸入值的交集。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.25.1.1.1"></a>
<code class="function">string_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">text</code>, <em class="parameter"><code>delimiter</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">string_agg</code> ( <em class="parameter"><code>value</code></em>
<code class="type">bytea</code>, <em class="parameter"><code>delimiter</code></em> <code class="type">bytea</code>
<code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將非 null 的輸入值串接成一個字串。第一個值之後的每個值前面，都會加上對應的 <em class="parameter"><code>delimiter</code></em>（如果它不是 null）。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.26.1.1.1"></a>
<code class="function">sum</code> ( <code class="type">smallint</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">real</code> )
        → <code class="returnvalue">real</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">interval</code> )
        → <code class="returnvalue">interval</code>
</p>
<p class="func_signature">
<code class="function">sum</code> ( <code class="type">money</code> )
        → <code class="returnvalue">money</code>
</p>
<p>
        計算非 null 輸入值的總和。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.6.2.4.27.1.1.1"></a>
<code class="function">xmlagg</code> ( <code class="type">xml</code> <code class="literal">ORDER BY</code> <code class="literal">input_sort_columns</code> )
        → <code class="returnvalue">xml</code>
</p>
<p>
        串接非 null 的 XML 輸入值（請參閱<a class="xref" href="functions-xml.md#FUNCTIONS-XML-XMLAGG">第 9.15.1.8 節</a>）。
       </p></td><td>否</td></tr></tbody></table>

<br>

應該注意的是，除了 `count` 之外，這些函式在沒有選取任何資料列時都會回傳 null 值。特別是，沒有資料列時 `sum` 會回傳 null，而不是一般人可能預期的零；而在沒有輸入資料列時，`array_agg` 會回傳 null 而不是空陣列。必要時，可以使用 `coalesce` 函式以零或空陣列取代 null。

彙總函式 `array_agg`、`json_agg`、`jsonb_agg`、`json_agg_strict`、`jsonb_agg_strict`、`json_object_agg`、`jsonb_object_agg`、`json_object_agg_strict`、`jsonb_object_agg_strict`、`json_object_agg_unique`、`jsonb_object_agg_unique`、`json_object_agg_unique_strict`、`jsonb_object_agg_unique_strict`、`string_agg` 與 `xmlagg`，以及類似的使用者定義彙總函式，會依輸入值的順序產生意義上不同的結果值。這個順序預設是未指定的，但可以在彙總呼叫中寫出 `ORDER BY` 子句來控制，如[第 4.2.7 節](../sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)所示。另外，從排序過的子查詢提供輸入值通常也可行。例如：

```

SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;
```

請注意，如果外層查詢層級包含額外的處理（例如聯結），這種做法可能會失敗，因為那可能導致子查詢的輸出在計算彙總之前被重新排序。

### 注意

<a id="id-1.5.8.27.9.1"></a><a id="id-1.5.8.27.9.2"></a>

布林彙總函式 `bool_and` 與 `bool_or`，分別對應到標準 SQL 的彙總函式 `every` 以及 `any` 或 `some`。PostgreSQL 支援 `every`，但不支援 `any` 或 `some`，因為標準語法本身存在歧義：

```

SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;
```

在這裡，如果子查詢回傳一筆帶有布林值的資料列，`ANY` 既可以被視為引出一個子查詢，也可以被視為一個彙總函式。因此，無法為這些彙總函式使用標準名稱。

### 注意

習慣使用其他 SQL 資料庫管理系統的使用者，可能會對將 `count` 彙總函式套用到整個資料表時的效能感到失望。像這樣的查詢：

```

SELECT count(*) FROM sometable;
```

所需的工作量會與資料表的大小成正比：PostgreSQL 必須掃描整個資料表，或掃描一個包含資料表所有資料列的索引的全部內容。

[表 9.63](functions-aggregate.md#FUNCTIONS-AGGREGATE-STATISTICS-TABLE) 列出了通常用於統計分析的彙總函式。（將它們分開列出，只是為了避免讓較常用彙總函式的清單顯得雜亂。）顯示為接受 *`numeric_type`* 的函式，適用於 `smallint`、`integer`、`bigint`、`numeric`、`real` 與 `double precision` 等所有型別。說明中提到 *`N`* 時，指的是所有輸入運算式都不為 null 的輸入資料列數。在所有情況下，如果計算沒有意義（例如當 *`N`* 為零時），就會回傳 null。

<a id="id-1.5.8.27.12"></a><a id="id-1.5.8.27.13"></a><a id="FUNCTIONS-AGGREGATE-STATISTICS-TABLE"></a>

**表 9.63. 統計用彙總函式**

<table border="1" class="table" summary="Aggregate Functions for Statistics"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th><th>部分模式</th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.1.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.14.2.4.1.1.1.2"></a>
<code class="function">corr</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算相關係數。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.2.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.14.2.4.2.1.1.2"></a>
<code class="function">covar_pop</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算母體共變異數。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.3.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.14.2.4.3.1.1.2"></a>
<code class="function">covar_samp</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算樣本共變異數。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.4.1.1.1"></a>
<code class="function">regr_avgx</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算自變數的平均值，<code class="literal">sum(<em class="parameter"><code>X</code></em>)/<em class="parameter"><code>N</code></em></code>。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.5.1.1.1"></a>
<code class="function">regr_avgy</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算應變數的平均值，<code class="literal">sum(<em class="parameter"><code>Y</code></em>)/<em class="parameter"><code>N</code></em></code>。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.6.1.1.1"></a>
<code class="function">regr_count</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算兩個輸入都不為 null 的資料列數量。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.7.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.14.2.4.7.1.1.2"></a>
<code class="function">regr_intercept</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算由 (<em class="parameter"><code>X</code></em>, <em class="parameter"><code>Y</code></em>) 配對所決定之最小平方擬合直線方程式的 y 截距。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.8.1.1.1"></a>
<code class="function">regr_r2</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算相關係數的平方。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.9.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.27.14.2.4.9.1.1.2"></a>
<code class="function">regr_slope</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算由 (<em class="parameter"><code>X</code></em>, <em class="parameter"><code>Y</code></em>) 配對所決定之最小平方擬合直線方程式的斜率。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.10.1.1.1"></a>
<code class="function">regr_sxx</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算自變數的<span class="quote">“<span class="quote">平方和</span>”</span>，<code class="literal">sum(<em class="parameter"><code>X</code></em>^2) - sum(<em class="parameter"><code>X</code></em>)^2/<em class="parameter"><code>N</code></em></code>。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.11.1.1.1"></a>
<code class="function">regr_sxy</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算自變數乘以應變數的<span class="quote">“<span class="quote">乘積和</span>”</span>，<code class="literal">sum(<em class="parameter"><code>X</code></em>*<em class="parameter"><code>Y</code></em>) - sum(<em class="parameter"><code>X</code></em>) * sum(<em class="parameter"><code>Y</code></em>)/<em class="parameter"><code>N</code></em></code>。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.12.1.1.1"></a>
<code class="function">regr_syy</code> ( <em class="parameter"><code>Y</code></em> <code class="type">double precision</code>, <em class="parameter"><code>X</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算應變數的<span class="quote">“<span class="quote">平方和</span>”</span>，<code class="literal">sum(<em class="parameter"><code>Y</code></em>^2) - sum(<em class="parameter"><code>Y</code></em>)^2/<em class="parameter"><code>N</code></em></code>。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.13.1.1.1"></a> <a class="indexterm" id="id-1.5.8.27.14.2.4.13.1.1.2"></a> <code class="function">stddev</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        這是 <code class="function">stddev_samp</code> 的歷史別名。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.14.1.1.1"></a> <a class="indexterm" id="id-1.5.8.27.14.2.4.14.1.1.2"></a> <code class="function">stddev_pop</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        計算輸入值的母體標準差。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.15.1.1.1"></a> <a class="indexterm" id="id-1.5.8.27.14.2.4.15.1.1.2"></a> <code class="function">stddev_samp</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        計算輸入值的樣本標準差。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.16.1.1.1"></a> <code class="function">variance</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        這是 <code class="function">var_samp</code> 的歷史別名。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.17.1.1.1"></a> <a class="indexterm" id="id-1.5.8.27.14.2.4.17.1.1.2"></a> <code class="function">var_pop</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        計算輸入值的母體變異數（母體標準差的平方）。
       </p></td><td>是</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.14.2.4.18.1.1.1"></a> <a class="indexterm" id="id-1.5.8.27.14.2.4.18.1.1.2"></a> <code class="function">var_samp</code> ( <em class="replaceable"><code>numeric_type</code></em> ) → <code class="returnvalue"></code> <code class="type">double precision</code>（對於 <code class="type">real</code> 或 <code class="type">double precision</code>），否則為 <code class="type">numeric</code>
</p>
<p>
        計算輸入值的樣本變異數（樣本標準差的平方）。
       </p></td><td>是</td></tr></tbody></table>

<br>

[表 9.64](functions-aggregate.md#FUNCTIONS-ORDEREDSET-TABLE) 列出了一些使用*有序集合彙總*（ordered-set aggregate）語法的彙總函式。這些函式有時稱為「逆分布」（inverse distribution）函式。它們的彙總輸入由 `ORDER BY` 引出，而且它們還可以接受一個不被彙總、只計算一次的*直接引數*（direct argument）。所有這些函式都會忽略彙總輸入中的 null 值。對於接受 *`fraction`* 參數的函式，比例值必須介於 0 與 1 之間；否則會引發錯誤。不過，null 的 *`fraction`* 值只會產生 null 結果。

<a id="id-1.5.8.27.16"></a><a id="id-1.5.8.27.17"></a><a id="FUNCTIONS-ORDEREDSET-TABLE"></a>

**表 9.64. 有序集合彙總函式**

<table border="1" class="table" summary="Ordered-Set Aggregate Functions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th><th>部分模式</th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.18.2.4.1.1.1.1"></a>
<code class="function">mode</code> () <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">anyelement</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        計算<em class="firstterm">眾數</em>（mode），也就是彙總引數中出現最頻繁的值（如果有多個出現頻率相同的值，就任意選擇第一個）。彙總引數必須是可排序的型別。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.18.2.4.2.1.1.1"></a>
<code class="function">percentile_cont</code> ( <em class="parameter"><code>fraction</code></em> <code class="type">double precision</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p class="func_signature">
<code class="function">percentile_cont</code> ( <em class="parameter"><code>fraction</code></em> <code class="type">double precision</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">interval</code> )
        → <code class="returnvalue">interval</code>
</p>
<p>
        計算<em class="firstterm">連續百分位數</em>（continuous percentile），也就是在彙總引數值的有序集合中，對應於指定 <em class="parameter"><code>fraction</code></em> 的值。必要時會在相鄰的輸入項目之間進行內插。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">percentile_cont</code> ( <em class="parameter"><code>fractions</code></em> <code class="type">double precision[]</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision[]</code>
</p>
<p class="func_signature">
<code class="function">percentile_cont</code> ( <em class="parameter"><code>fractions</code></em> <code class="type">double precision[]</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">interval</code> )
        → <code class="returnvalue">interval[]</code>
</p>
<p>
        計算多個連續百分位數。結果是一個與 <em class="parameter"><code>fractions</code></em> 參數具有相同維度的陣列，其中每個非 null 元素都會被替換為對應於該百分位數的（可能經過內插的）值。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.18.2.4.4.1.1.1"></a>
<code class="function">percentile_disc</code> ( <em class="parameter"><code>fraction</code></em> <code class="type">double precision</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">anyelement</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        計算<em class="firstterm">離散百分位數</em>（discrete percentile），也就是在彙總引數值的有序集合中，其排序位置等於或超過指定 <em class="parameter"><code>fraction</code></em> 的第一個值。彙總引數必須是可排序的型別。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">percentile_disc</code> ( <em class="parameter"><code>fractions</code></em> <code class="type">double precision[]</code> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <code class="type">anyelement</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        計算多個離散百分位數。結果是一個與 <em class="parameter"><code>fractions</code></em> 參數具有相同維度的陣列，其中每個非 null 元素都會被替換為對應於該百分位數的輸入值。彙總引數必須是可排序的型別。
       </p></td><td>否</td></tr></tbody></table>

<br><a id="id-1.5.8.27.19"></a>

[表 9.65](functions-aggregate.md#FUNCTIONS-HYPOTHETICAL-TABLE) 所列的每一個「假設集合」（hypothetical-set）彙總函式，都與[第 9.22 節](functions-window.md)中定義的同名 window 函式相關聯。在每一種情況下，彙總函式的結果，就是假如將由 *`args`* 建構的「假設」資料列加入由 *`sorted_args`* 所代表的已排序資料列群組中，相關聯的 window 函式會回傳的值。對於這些函式中的每一個，*`args`* 中給定的直接引數清單，必須與 *`sorted_args`* 中給定之彙總引數的數量與型別相符。與大多數內建彙總函式不同，這些彙總函式不是嚴格的，也就是說，它們不會捨棄包含 null 的輸入資料列。null 值會依照 `ORDER BY` 子句所指定的規則排序。

<a id="FUNCTIONS-HYPOTHETICAL-TABLE"></a>

**表 9.65. 假設集合彙總函式**

<table border="1" class="table" summary="Hypothetical-Set Aggregate Functions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th><th>部分模式</th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.21.2.4.1.1.1.1"></a>
<code class="function">rank</code> ( <em class="replaceable"><code>args</code></em> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <em class="replaceable"><code>sorted_args</code></em> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算假設資料列的排名，有間隙；也就是其同儕群組中第一筆資料列的資料列編號。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.21.2.4.2.1.1.1"></a>
<code class="function">dense_rank</code> ( <em class="replaceable"><code>args</code></em> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <em class="replaceable"><code>sorted_args</code></em> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算假設資料列的排名，沒有間隙；這個函式實際上是在計算同儕群組的數量。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.21.2.4.3.1.1.1"></a>
<code class="function">percent_rank</code> ( <em class="replaceable"><code>args</code></em> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <em class="replaceable"><code>sorted_args</code></em> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算假設資料列的相對排名，也就是 (<code class="function">rank</code> - 1) / (資料列總數 - 1)。因此其值的範圍是 0 到 1（含）。
       </p></td><td>否</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.21.2.4.4.1.1.1"></a>
<code class="function">cume_dist</code> ( <em class="replaceable"><code>args</code></em> ) <code class="literal">WITHIN GROUP</code> ( <code class="literal">ORDER BY</code> <em class="replaceable"><code>sorted_args</code></em> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算累積分布，也就是（排在假設資料列之前或與之同儕的資料列數）/（資料列總數）。因此其值的範圍是 1/<em class="parameter"><code>N</code></em> 到 1。
       </p></td><td>否</td></tr></tbody></table>

<br><a id="FUNCTIONS-GROUPING-TABLE"></a>

**表 9.66. 分組操作**

<table border="1" class="table" summary="Grouping Operations"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.27.22.2.2.1.1.1.1"></a>
<code class="function">GROUPING</code> ( <em class="replaceable"><code>group_by_expression(s)</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳一個位元遮罩，指出哪些 <code class="literal">GROUP BY</code> 運算式沒有包含在目前的分組集合中。位元的指派方式是最右邊的引數對應到最低有效位元；如果對應的運算式包含在產生目前結果資料列之分組集合的分組條件中，該位元就是 0，否則為 1。
       </p></td></tr></tbody></table>

<br>

[表 9.66](functions-aggregate.md#FUNCTIONS-GROUPING-TABLE) 所列的分組操作，會與分組集合（請參閱[第 7.2.4 節](../queries/queries-table-expressions.md#QUERIES-GROUPING-SETS)）搭配使用，以區分結果資料列。`GROUPING` 函式的引數實際上不會被評估，但它們必須與相關聯查詢層級之 `GROUP BY` 子句中所給定的運算式完全相符。例如：

```

=> SELECT * FROM items_sold;
 make  | model | sales
-------+-------+-------
 Foo   | GT    |  10
 Foo   | Tour  |  20
 Bar   | City  |  15
 Bar   | Sport |  5
(4 rows)

=> SELECT make, model, GROUPING(make,model), sum(sales) FROM items_sold GROUP BY ROLLUP(make,model);
 make  | model | grouping | sum
-------+-------+----------+-----
 Foo   | GT    |        0 | 10
 Foo   | Tour  |        0 | 20
 Bar   | City  |        0 | 15
 Bar   | Sport |        0 | 5
 Foo   |       |        1 | 30
 Bar   |       |        1 | 20
       |       |        3 | 50
(7 rows)
```

在這裡，前四筆資料列中的 `grouping` 值 `0` 顯示這些資料列是依兩個分組欄位正常分組的。值 `1` 表示在倒數第二與第三筆資料列中，並未依 `model` 分組；而值 `3` 表示在最後一筆資料列中，既未依 `make` 也未依 `model` 分組（因此它是對所有輸入資料列的彙總）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-aggregate.html)（原文版本：18.6；核對日期：2026-09-11）
