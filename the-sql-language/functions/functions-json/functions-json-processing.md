# 9.16.1. 處理與建立 JSON 資料

<a id="FUNCTIONS-JSON-PROCESSING"></a>

## 9.16.1. 處理與建立 JSON 資料 [#](#functions-json-processing) <a href="#functions-json-processing" id="functions-json-processing"></a>

[表 9.47](#functions-json-op-table) 列出了可用於 JSON 資料型別的運算子（請參閱[第 8.14 節](../../datatype/datatype-json.md)）。此外，[表 9.1](../functions-comparison.md#functions-comparison-table) 所列的一般比較運算子也可用於 `jsonb`，但不能用於 `json`。這些比較運算子遵循[第 8.14.4 節](../../datatype/datatype-json.md#json-indexing)所述之 B-tree 操作的排序規則。另請參閱[第 9.21 節](../functions-aggregate.md)中的彙總函式 `json_agg`（將記錄值彙總為 JSON）、彙總函式 `json_object_agg`（將成對的值彙總為 JSON 物件），以及它們對應的 `jsonb` 版本 `jsonb_agg` 與 `jsonb_object_agg`。

<a id="FUNCTIONS-JSON-OP-TABLE"></a>

### 表 9.47. `json` 與 `jsonb` 運算子 [#](#functions-json-op-table) <a href="#functions-json-op-table" id="functions-json-op-table"></a>

<table border="1" class="table" summary="json and jsonb Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        擷取 JSON 陣列的第 <em class="parameter"><code>n</code></em> 個元素（陣列元素的索引從零開始，但負整數會從結尾倒數）。
       </p>
<p>
<code class="literal">'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; 2</code>
        → <code class="returnvalue">{"c":"baz"}</code>
</p>
<p>
<code class="literal">'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; -3</code>
        → <code class="returnvalue">{"a":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        擷取具有指定鍵的 JSON 物件欄位。
       </p>
<p>
<code class="literal">'{"a": {"b":"foo"}}'::json -&gt; 'a'</code>
        → <code class="returnvalue">{"b":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取 JSON 陣列的第 <em class="parameter"><code>n</code></em> 個元素，以 <code class="type">text</code> 形式回傳。
       </p>
<p>
<code class="literal">'[1,2,3]'::json -&gt;&gt; 2</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取具有指定鍵的 JSON 物件欄位，以 <code class="type">text</code> 形式回傳。
       </p>
<p>
<code class="literal">'{"a":1,"b":2}'::json -&gt;&gt; 'b'</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">#&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        擷取位於指定路徑的 JSON 子物件，其中路徑元素可以是欄位鍵或陣列索引。
       </p>
<p>
<code class="literal">'{"a": {"b": ["foo","bar"]}}'::json #&gt; '{a,b,1}'</code>
        → <code class="returnvalue">"bar"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">#&gt;&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#&gt;&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取位於指定路徑的 JSON 子物件，以 <code class="type">text</code> 形式回傳。
       </p>
<p>
<code class="literal">'{"a": {"b": ["foo","bar"]}}'::json #&gt;&gt; '{a,b,1}'</code>
        → <code class="returnvalue">bar</code>
</p></td></tr></tbody></table>

<br>

### 注意

如果 JSON 輸入不具有符合請求的正確結構，例如不存在這樣的鍵或陣列元素，欄位／元素／路徑擷取運算子會回傳 NULL，而不會失敗。

另外還有一些只適用於 `jsonb` 的運算子，如[表 9.48](#functions-jsonb-op-table) 所示。[第 8.14.4 節](../../datatype/datatype-json.md#json-indexing)說明了如何使用這些運算子來有效率地搜尋已建立索引的 `jsonb` 資料。

<a id="FUNCTIONS-JSONB-OP-TABLE"></a>

### 表 9.48. 其他 `jsonb` 運算子 [#](#functions-jsonb-op-table) <a href="#functions-jsonb-op-table" id="functions-jsonb-op-table"></a>

<table border="1" class="table" summary="Additional jsonb Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@&gt;</code> <code class="type">jsonb</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 JSON 值是否包含第二個 JSON 值？（關於包含的詳細說明，請參閱<a class="xref" href="../../datatype/datatype-json.md#json-containment">第 8.14.3 節</a>。）
       </p>
<p>
<code class="literal">'{"a":1, "b":2}'::jsonb @&gt; '{"b":2}'::jsonb</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">&lt;@</code> <code class="type">jsonb</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 JSON 值是否被包含在第二個 JSON 值之中？
       </p>
<p>
<code class="literal">'{"b":2}'::jsonb &lt;@ '{"a":1, "b":2}'::jsonb</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        該文字字串是否以最上層的鍵或陣列元素的形式存在於 JSON 值中？
       </p>
<p>
<code class="literal">'{"a":1, "b":2}'::jsonb ? 'b'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">'["a", "b", "c"]'::jsonb ? 'b'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?|</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        文字陣列中是否有任何字串以最上層的鍵或陣列元素的形式存在？
       </p>
<p>
<code class="literal">'{"a":1, "b":2, "c":3}'::jsonb ?| array['b', 'd']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?&amp;</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        文字陣列中的所有字串是否都以最上層的鍵或陣列元素的形式存在？
       </p>
<p>
<code class="literal">'["a", "b", "c"]'::jsonb ?&amp; array['a', 'b']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">||</code> <code class="type">jsonb</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        串接兩個 <code class="type">jsonb</code> 值。串接兩個陣列會產生一個包含兩個輸入之所有元素的陣列。串接兩個物件會產生一個包含兩者之鍵聯集的物件，當有重複的鍵時，採用第二個物件的值。所有其他情況的處理方式，都是先將非陣列的輸入轉換為單一元素的陣列，再依照兩個陣列的方式處理。這個運算不會遞迴進行：只會合併最上層的陣列或物件結構。
       </p>
<p>
<code class="literal">'["a", "b"]'::jsonb || '["a", "d"]'::jsonb</code>
        → <code class="returnvalue">["a", "b", "a", "d"]</code>
</p>
<p>
<code class="literal">'{"a": "b"}'::jsonb || '{"c": "d"}'::jsonb</code>
        → <code class="returnvalue">{"a": "b", "c": "d"}</code>
</p>
<p>
<code class="literal">'[1, 2]'::jsonb || '3'::jsonb</code>
        → <code class="returnvalue">[1, 2, 3]</code>
</p>
<p>
<code class="literal">'{"a": "b"}'::jsonb || '42'::jsonb</code>
        → <code class="returnvalue">[{"a": "b"}, 42]</code>
</p>
<p>
        若要將一個陣列作為單一項目附加到另一個陣列，請再用一層陣列將它包起來，例如：
       </p>
<p>
<code class="literal">'[1, 2]'::jsonb || jsonb_build_array('[3, 4]'::jsonb)</code>
        → <code class="returnvalue">[1, 2, [3, 4]]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">text</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從 JSON 物件中刪除一個鍵（及其值），或從 JSON 陣列中刪除相符的字串值。
       </p>
<p>
<code class="literal">'{"a": "b", "c": "d"}'::jsonb - 'a'</code>
        → <code class="returnvalue">{"c": "d"}</code>
</p>
<p>
<code class="literal">'["a", "b", "c", "b"]'::jsonb - 'b'</code>
        → <code class="returnvalue">["a", "c"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從左運算元中刪除所有相符的鍵或陣列元素。
       </p>
<p>
<code class="literal">'{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]</code>
        → <code class="returnvalue">{}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">integer</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        刪除具有指定索引的陣列元素（負整數會從結尾倒數）。如果 JSON 值不是陣列，就會拋出錯誤。
       </p>
<p>
<code class="literal">'["a", "b"]'::jsonb - 1 </code>
        → <code class="returnvalue">["a"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#-</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        刪除位於指定路徑的欄位或陣列元素，其中路徑元素可以是欄位鍵或陣列索引。
       </p>
<p>
<code class="literal">'["a", {"b":1}]'::jsonb #- '{1,b}'</code>
        → <code class="returnvalue">["a", {}]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@?</code> <code class="type">jsonpath</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        對於指定的 JSON 值，JSON 路徑是否回傳任何項目？（這只對符合 SQL 標準的 JSON 路徑運算式有用，對<a class="link" href="../functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>則沒有用處，因為後者一定會回傳一個值。）
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ &gt; 2)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@@</code> <code class="type">jsonpath</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        回傳對指定的 JSON 值進行 JSON 路徑述詞檢查的結果。（這只對<a class="link" href="../functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>有用，對符合 SQL 標準的 JSON 路徑運算式則沒有用處，因為如果路徑結果不是單一的布林值，它會回傳 <code class="literal">NULL</code>。）
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] &gt; 2'</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

### 注意

`jsonpath` 運算子 `@?` 與 `@@` 會抑制下列錯誤：缺少物件欄位或陣列元素、非預期的 JSON 項目型別，以及日期時間與數值錯誤。下面所述與 `jsonpath` 相關的函式，也可以指示它們抑制這些類型的錯誤。在搜尋結構不一的 JSON 文件集合時，這種行為可能很有幫助。

[表 9.49](#functions-json-creation-table) 列出了可用於建構 `json` 與 `jsonb` 值的函式。這個表格中的某些函式具有 `RETURNING` 子句，用來指定回傳的資料型別。它必須是 `json`、`jsonb`、`bytea`、字元字串型別（`text`、`char` 或 `varchar`）之一，或是可以轉換為 `json` 的型別。預設會回傳 `json` 型別。

<a id="FUNCTIONS-JSON-CREATION-TABLE"></a>

### 表 9.49. JSON 建立函式 [#](#functions-json-creation-table) <a href="#functions-json-creation-table" id="functions-json-creation-table"></a>

<table border="1" class="table" summary="JSON Creation Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.1.1.1.1"></a>
<code class="function">to_json</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.1.1.2.1"></a>
<code class="function">to_jsonb</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將任何 SQL 值轉換為 <code class="type">json</code> 或 <code class="type">jsonb</code>。陣列與複合值會被遞迴地轉換為陣列與物件（多維陣列在 JSON 中會成為陣列的陣列）。否則，如果存在從該 SQL 資料型別到 <code class="type">json</code> 的型別轉換，就會使用該轉換函式來執行轉換；<a class="footnote" href="#ftn.id-1.5.8.22.8.9.2.2.1.1.3.4"><sup class="footnote" id="id-1.5.8.22.8.9.2.2.1.1.3.4">[a]</sup></a>否則，會產生一個純量 JSON 值。對於數值、布林值或 null 值以外的任何純量，會使用其文字表示，並視需要加以跳脫，使其成為有效的 JSON 字串值。
       </p>
<p>
<code class="literal">to_json('Fred said "Hi."'::text)</code>
        → <code class="returnvalue">"Fred said \"Hi.\""</code>
</p>
<p>
<code class="literal">to_jsonb(row(42, 'Fred said "Hi."'::text))</code>
        → <code class="returnvalue">{"f1": 42, "f2": "Fred said \"Hi.\""}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.2.1.1.1"></a>
<code class="function">array_to_json</code> ( <code class="type">anyarray</code> [<span class="optional">, <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p>
        將 SQL 陣列轉換為 JSON 陣列。其行為與 <code class="function">to_json</code> 相同，差別在於如果選用的布林參數為 true，會在最上層的陣列元素之間加入換行字元。
       </p>
<p>
<code class="literal">array_to_json('{{1,5},{99,100}}'::int[])</code>
        → <code class="returnvalue">[[1,5],[99,100]]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.3.1.1.1"></a>
<code class="function">json_array</code> (
         [<span class="optional"> { <em class="replaceable"><code>value_expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> </span>] } [<span class="optional">, ...</span>] </span>]
         [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p class="func_signature">
<code class="function">json_array</code> (
         [<span class="optional"> <em class="replaceable"><code>query_expression</code></em> </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p>
         從一連串的 <em class="replaceable"><code>value_expression</code></em> 參數，或是從 <em class="replaceable"><code>query_expression</code></em> 的結果（必須是回傳單一欄位的 SELECT 查詢）建構 JSON 陣列。如果指定了 <code class="literal">ABSENT ON NULL</code>，NULL 值會被忽略。如果使用的是 <em class="replaceable"><code>query_expression</code></em>，則一律如此。
        </p>
<p>
<code class="literal">json_array(1,true,json '{"a":null}')</code>
         → <code class="returnvalue">[1, true, {"a":null}]</code>
</p>
<p>
<code class="literal">json_array(SELECT * FROM (VALUES(1),(2)) t)</code>
         → <code class="returnvalue">[1, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.4.1.1.1"></a>
<code class="function">row_to_json</code> ( <code class="type">record</code> [<span class="optional">, <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p>
        將 SQL 複合值轉換為 JSON 物件。其行為與 <code class="function">to_json</code> 相同，差別在於如果選用的布林參數為 true，會在最上層的元素之間加入換行字元。
       </p>
<p>
<code class="literal">row_to_json(row(1,'foo'))</code>
        → <code class="returnvalue">{"f1":1,"f2":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.5.1.1.1"></a>
<code class="function">json_build_array</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.5.1.2.1"></a>
<code class="function">jsonb_build_array</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從可變參數的引數列表建立一個型別可能各不相同的 JSON 陣列。每個引數都會依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。
       </p>
<p>
<code class="literal">json_build_array(1, 2, 'foo', 4, 5)</code>
        → <code class="returnvalue">[1, 2, "foo", 4, 5]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.6.1.1.1"></a>
<code class="function">json_build_object</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.6.1.2.1"></a>
<code class="function">jsonb_build_object</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從可變參數的引數列表建立一個 JSON 物件。依照慣例，引數列表由交替出現的鍵與值組成。鍵引數會被強制轉換為文字；值引數則依照 <code class="function">to_json</code> 或 <code class="function">to_jsonb</code> 的方式轉換。
       </p>
<p>
<code class="literal">json_build_object('foo', 1, 2, row(3,'bar'))</code>
        → <code class="returnvalue">{"foo" : 1, "2" : {"f1":3,"f2":"bar"}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.7.1.1.1"></a>
<code class="function">json_object</code> (
         [<span class="optional"> { <em class="replaceable"><code>key_expression</code></em> { <code class="literal">VALUE</code> | ':' }
          <em class="replaceable"><code>value_expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] }[<span class="optional">, ...</span>] </span>]
         [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
         [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>] </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p>
         以所給的全部鍵／值對建構一個 JSON 物件，如果沒有給任何鍵／值對，則建構一個空物件。<em class="replaceable"><code>key_expression</code></em> 是定義 <acronym class="acronym">JSON</acronym> 鍵的純量運算式，它會被轉換為 <code class="type">text</code> 型別。它不能是 <code class="literal">NULL</code>，也不能屬於具有到 <code class="type">json</code> 型別之型別轉換的型別。如果指定了 <code class="literal">WITH UNIQUE KEYS</code>，就不得有任何重複的 <em class="replaceable"><code>key_expression</code></em>。任何 <em class="replaceable"><code>value_expression</code></em> 求值結果為 <code class="literal">NULL</code> 的鍵／值對，在指定了 <code class="literal">ABSENT ON NULL</code> 時都會從輸出中省略；如果指定了 <code class="literal">NULL ON NULL</code> 或省略了該子句，則會包含該鍵，其值為 <code class="literal">NULL</code>。
        </p>
<p>
<code class="literal">json_object('code' VALUE 'P123', 'title': 'Jaws')</code>
         → <code class="returnvalue">{"code" : "P123", "title" : "Jaws"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.8.1.1.1"></a>
<code class="function">json_object</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.8.1.2.1"></a>
<code class="function">jsonb_object</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從文字陣列建立 JSON 物件。該陣列必須是恰好一維且成員個數為偶數，此時成員會被視為交替出現的鍵／值對；或者是二維，且每個內層陣列恰好有兩個元素，這兩個元素會被視為一個鍵／值對。所有的值都會被轉換為 JSON 字串。
       </p>
<p>
<code class="literal">json_object('{a, 1, b, "def", c, 3.5}')</code>
        → <code class="returnvalue">{"a" : "1", "b" : "def", "c" : "3.5"}</code>
</p>
<p><code class="literal">json_object('{{a, 1}, {b, "def"}, {c, 3.5}}')</code>
        → <code class="returnvalue">{"a" : "1", "b" : "def", "c" : "3.5"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">json_object</code> ( <em class="parameter"><code>keys</code></em> <code class="type">text[]</code>, <em class="parameter"><code>values</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="function">jsonb_object</code> ( <em class="parameter"><code>keys</code></em> <code class="type">text[]</code>, <em class="parameter"><code>values</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        這種形式的 <code class="function">json_object</code> 會從兩個分開的文字陣列中成對地取得鍵與值。除此之外，它與單一引數的形式完全相同。
       </p>
<p>
<code class="literal">json_object('{a,b}', '{1,2}')</code>
        → <code class="returnvalue">{"a": "1", "b": "2"}</code>
</p></td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.10.1.1.1"></a>
<code class="function">json</code> (
         <em class="replaceable"><code>expression</code></em>
         [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>]</span>]
         [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>]</span>] )
         → <code class="returnvalue">json</code>
</p>
<p>
         將以 <code class="type">text</code> 或 <code class="type">bytea</code> 字串（UTF8 編碼）指定的運算式轉換為 JSON 值。如果 <em class="replaceable"><code>expression</code></em> 為 NULL，會回傳 <acronym class="acronym">SQL</acronym> null 值。如果指定了 <code class="literal">WITH UNIQUE</code>，<em class="replaceable"><code>expression</code></em> 中就不得包含任何重複的物件鍵。
        </p>
<p>
<code class="literal">json('{"a":123, "b":[true,"foo"], "a":"bar"}')</code>
         → <code class="returnvalue">{"a":123, "b":[true,"foo"], "a":"bar"}</code>
</p>
</td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.11.1.1.1"></a>
<code class="function">json_scalar</code> ( <em class="replaceable"><code>expression</code></em> )
       </p>
<p>
        將指定的 SQL 純量值轉換為 JSON 純量值。如果輸入為 NULL，會回傳 <acronym class="acronym">SQL</acronym> null。如果輸入是數值或布林值，會回傳對應的 JSON 數值或布林值。對於任何其他的值，則回傳 JSON 字串。
       </p>
<p>
<code class="literal">json_scalar(123.45)</code>
        → <code class="returnvalue">123.45</code>
</p>
<p>
<code class="literal">json_scalar(CURRENT_TIMESTAMP)</code>
        → <code class="returnvalue">"2022-05-10T10:51:04.62128-04:00"</code>
</p></td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<code class="function">json_serialize</code> (
        <em class="replaceable"><code>expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>]
        [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>] )
       </p>
<p>
        將 SQL/JSON 運算式轉換為字元字串或二進位字串。<em class="replaceable"><code>expression</code></em> 可以是任何 JSON 型別、任何字元字串型別，或是 UTF8 編碼的 <code class="type">bytea</code>。<code class="literal"> RETURNING</code> 中使用的回傳型別可以是任何字元字串型別或 <code class="type">bytea</code>。預設為 <code class="type">text</code>。
       </p>
<p>
<code class="literal">json_serialize('{ "a" : 1 } ' RETURNING bytea)</code>
        → <code class="returnvalue">\x7b20226122203a2031207d20</code>
</p></td></tr></tbody><tbody class="footnotes"><tr><td colspan="1"><div class="footnote" id="ftn.id-1.5.8.22.8.9.2.2.1.1.3.4"><p><a class="para" href="#id-1.5.8.22.8.9.2.2.1.1.3.4"><sup class="para">[a] </sup></a>例如，<a class="xref" href="../../../appendixes/contrib/hstore.md">hstore</a> 擴充功能具有從 <code class="type">hstore</code> 到 <code class="type">json</code> 的型別轉換，因此透過 JSON 建立函式轉換的 <code class="type">hstore</code> 值，會以 JSON 物件表示，而不是以原始的字串值表示。
         </p></div></td></tr></tbody></table>

<br>

[表 9.50](#functions-sqljson-misc) 詳細列出了用於測試 JSON 的 SQL/JSON 功能。

<a id="FUNCTIONS-SQLJSON-MISC"></a>

### 表 9.50. SQL/JSON 測試函式 [#](#functions-sqljson-misc) <a href="#functions-sqljson-misc" id="functions-sqljson-misc"></a>

<table border="1" class="table" summary="SQL/JSON Testing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式簽章
       </p>
<p>
        說明
       </p>
<p>
        範例
      </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.11.2.2.1.1.1.1"></a>
<em class="replaceable"><code>expression</code></em> <code class="literal">IS</code> [<span class="optional"> <code class="literal">NOT</code> </span>] <code class="literal">JSON</code>
        [<span class="optional"> { <code class="literal">VALUE</code> | <code class="literal">SCALAR</code> | <code class="literal">ARRAY</code> | <code class="literal">OBJECT</code> } </span>]
        [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>] </span>]
       </p>
<p>
        這個述詞測試 <em class="replaceable"><code>expression</code></em> 是否可以被剖析為 JSON，並可指定特定的型別。如果指定了 <code class="literal">SCALAR</code>、<code class="literal">ARRAY</code> 或 <code class="literal">OBJECT</code>，則測試的是該 JSON 是否屬於該特定型別。如果指定了 <code class="literal">WITH UNIQUE KEYS</code>，也會測試 <em class="replaceable"><code>expression</code></em> 中的每個物件是否有重複的鍵。
       </p>
<p>
</p><pre class="programlisting">
SELECT js,
  js IS JSON "json?",
  js IS JSON SCALAR "scalar?",
  js IS JSON OBJECT "object?",
  js IS JSON ARRAY "array?"
FROM (VALUES
      ('123'), ('"abc"'), ('{"a": "b"}'), ('[1,2]'),('abc')) foo(js);
     js     | json? | scalar? | object? | array?
------------+-------+---------+---------+--------
 123        | t     | t       | f       | f
 "abc"      | t     | t       | f       | f
 {"a": "b"} | t     | f       | t       | f
 [1,2]      | t     | f       | f       | t
 abc        | f     | f       | f       | f
</pre><p>
</p>
<p>
</p><pre class="programlisting">
SELECT js,
  js IS JSON OBJECT "object?",
  js IS JSON ARRAY "array?",
  js IS JSON ARRAY WITH UNIQUE KEYS "array w. UK?",
  js IS JSON ARRAY WITHOUT UNIQUE KEYS "array w/o UK?"
FROM (VALUES ('[{"a":"1"},
 {"b":"2","b":"3"}]')) foo(js);
-[ RECORD 1 ]-+--------------------
js            | [{"a":"1"},        +
              |  {"b":"2","b":"3"}]
object?       | f
array?        | t
array w. UK?  | f
array w/o UK? | t
</pre><p>
</p></td></tr></tbody></table>

<br>

[表 9.51](#functions-json-processing-table) 列出了可用於處理 `json` 與 `jsonb` 值的函式。

<a id="FUNCTIONS-JSON-PROCESSING-TABLE"></a>

### 表 9.51. JSON 處理函式 [#](#functions-json-processing-table) <a href="#functions-json-processing-table" id="functions-json-processing-table"></a>

<table border="1" class="table" summary="JSON Processing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.1.1.1.1"></a>
<code class="function">json_array_elements</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.1.1.2.1"></a>
<code class="function">jsonb_array_elements</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p>
        將最上層的 JSON 陣列展開為一組 JSON 值。
       </p>
<p>
<code class="literal">select * from json_array_elements('[1,true, [2,false]]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
   value
-----------
 1
 true
 [2,false]
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.2.1.1.1"></a>
<code class="function">json_array_elements_text</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.2.1.2.1"></a>
<code class="function">jsonb_array_elements_text</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        將最上層的 JSON 陣列展開為一組 <code class="type">text</code> 值。
       </p>
<p>
<code class="literal">select * from json_array_elements_text('["foo", "bar"]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
   value
-----------
 foo
 bar
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.3.1.1.1"></a>
<code class="function">json_array_length</code> ( <code class="type">json</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.3.1.2.1"></a>
<code class="function">jsonb_array_length</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳最上層 JSON 陣列中的元素個數。
       </p>
<p>
<code class="literal">json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]')</code>
        → <code class="returnvalue">5</code>
</p>
<p>
<code class="literal">jsonb_array_length('[]')</code>
        → <code class="returnvalue">0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.4.1.1.1"></a>
<code class="function">json_each</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">json</code> )
       </p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.4.1.2.1"></a>
<code class="function">jsonb_each</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">jsonb</code> )
       </p>
<p>
        將最上層的 JSON 物件展開為一組鍵／值對。
       </p>
<p>
<code class="literal">select * from json_each('{"a":"foo", "b":"bar"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 key | value
-----+-------
 a   | "foo"
 b   | "bar"
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.5.1.1.1"></a>
<code class="function">json_each_text</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">text</code> )
       </p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.5.1.2.1"></a>
<code class="function">jsonb_each_text</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">text</code> )
       </p>
<p>
        將最上層的 JSON 物件展開為一組鍵／值對。回傳的 <em class="parameter"><code>value</code></em> 會是 <code class="type">text</code> 型別。
       </p>
<p>
<code class="literal">select * from json_each_text('{"a":"foo", "b":"bar"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 key | value
-----+-------
 a   | foo
 b   | bar
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.6.1.1.1"></a>
<code class="function">json_extract_path</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">json</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.6.1.2.1"></a>
<code class="function">jsonb_extract_path</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        擷取位於指定路徑的 JSON 子物件。（這在功能上等同於 <code class="literal">#&gt;</code> 運算子，但在某些情況下，將路徑寫成可變參數的列表會更方便。）
       </p>
<p>
<code class="literal">json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')</code>
        → <code class="returnvalue">"foo"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.7.1.1.1"></a>
<code class="function">json_extract_path_text</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">json</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.7.1.2.1"></a>
<code class="function">jsonb_extract_path_text</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取位於指定路徑的 JSON 子物件，以 <code class="type">text</code> 形式回傳。（這在功能上等同於 <code class="literal">#&gt;&gt;</code> 運算子。）
       </p>
<p>
<code class="literal">json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')</code>
        → <code class="returnvalue">foo</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.8.1.1.1"></a>
<code class="function">json_object_keys</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.8.1.2.1"></a>
<code class="function">jsonb_object_keys</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        回傳最上層 JSON 物件中的鍵的集合。
       </p>
<p>
<code class="literal">select * from json_object_keys('{"f1":"abc","f2":{"f3":"a", "f4":"b"}}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 json_object_keys
------------------
 f1
 f2
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.9.1.1.1"></a>
<code class="function">json_populate_record</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.9.1.2.1"></a>
<code class="function">jsonb_populate_record</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        將最上層的 JSON 物件展開為一個資料列，其具有 <em class="parameter"><code>base</code></em> 引數的複合型別。系統會在 JSON 物件中掃描名稱與輸出資料列型別之欄位名稱相符的欄位，並將它們的值插入輸出的那些欄位中。（不對應任何輸出欄位名稱的欄位會被忽略。）在一般用法中，<em class="parameter"><code>base</code></em> 的值就是 <code class="literal">NULL</code>，這表示任何不符合任何物件欄位的輸出欄位都會被填入 null。不過，如果 <em class="parameter"><code>base</code></em> 不是 <code class="literal">NULL</code>，則它所包含的值將用於那些不相符的欄位。
       </p>
<p>
        為了將 JSON 值轉換為輸出欄位的 SQL 型別，會依序套用下列規則：
        </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
           JSON null 值在所有情況下都會轉換為 SQL null。
          </p></li><li class="listitem"><p>
           如果輸出欄位的型別是 <code class="type">json</code> 或 <code class="type">jsonb</code>，JSON 值就會原封不動地重現。
          </p></li><li class="listitem"><p>
           如果輸出欄位是複合（資料列）型別，而 JSON 值是 JSON 物件，則物件的欄位會透過遞迴套用這些規則，轉換為輸出資料列型別的欄位。
          </p></li><li class="listitem"><p>
           同樣地，如果輸出欄位是陣列型別，而 JSON 值是 JSON 陣列，則 JSON 陣列的元素會透過遞迴套用這些規則，轉換為輸出陣列的元素。
          </p></li><li class="listitem"><p>
           否則，如果 JSON 值是字串，就會將字串的內容送入該欄位資料型別的輸入轉換函式。
          </p></li><li class="listitem"><p>
           否則，就會將 JSON 值的一般文字表示送入該欄位資料型別的輸入轉換函式。
          </p></li></ul></div><p>
</p>
<p>
        雖然下面的範例使用常數 JSON 值，但一般用法是以 lateral 方式參照另一個資料表的 <code class="type">json</code> 或 <code class="type">jsonb</code> 欄位，而那個資料表位於查詢的 <code class="literal">FROM</code> 子句中。將 <code class="function">json_populate_record</code> 寫在 <code class="literal">FROM</code> 子句中是很好的做法，因為所有擷取出的欄位都可以直接使用，而不需要重複呼叫函式。
       </p>
<p>
<code class="literal">create type subrowtype as (d int, e text);</code>
<code class="literal">create type myrowtype as (a int, b text[], c subrowtype);</code>
</p>
<p>
<code class="literal">select * from json_populate_record(null::myrowtype,
         '{"a": 1, "b": ["2", "a b"], "c": {"d": 4, "e": "a  b c"}, "x": "foo"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |   b       |      c
---+-----------+-------------
 1 | {2,"a b"} | (4,"a b c")
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.10.1.1.1"></a>
<code class="function">jsonb_populate_record_valid</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        用於測試 <code class="function">jsonb_populate_record</code> 的函式。回傳 <code class="literal">true</code> 表示對於指定的輸入 JSON 物件，輸入的 <code class="function">jsonb_populate_record</code> 能夠順利完成而不發生錯誤，也就是說它是有效的輸入；否則回傳 <code class="literal">false</code>。
       </p>
<p>
<code class="literal">create type jsb_char2 as (a char(2));</code>
</p>
<p>
<code class="literal">select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aaa"}');</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_populate_record_valid
-----------------------------
 f
(1 row)
</pre><p>
<code class="literal">select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aaa"}') q;</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  value too long for type character(2)
</pre><p>
<code class="literal">select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aa"}');</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_populate_record_valid
-----------------------------
 t
(1 row)
</pre><p>
<code class="literal">select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aa"}') q;</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a
----
 aa
(1 row)
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.11.1.1.1"></a>
<code class="function">json_populate_recordset</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">setof anyelement</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.11.1.2.1"></a>
<code class="function">jsonb_populate_recordset</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">setof anyelement</code>
</p>
<p>
        將最上層的物件 JSON 陣列展開為一組資料列，這些資料列具有 <em class="parameter"><code>base</code></em> 引數的複合型別。JSON 陣列的每個元素，都會依照上面針對 <code class="function">json[b]_populate_record</code> 所述的方式處理。
       </p>
<p>
<code class="literal">create type twoints as (a int, b int);</code>
</p>
<p>
<code class="literal">select * from json_populate_recordset(null::twoints, '[{"a":1,"b":2}, {"a":3,"b":4}]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a | b
---+---
 1 | 2
 3 | 4
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.12.1.1.1"></a>
<code class="function">json_to_record</code> ( <code class="type">json</code> )
        → <code class="returnvalue">record</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.12.1.2.1"></a>
<code class="function">jsonb_to_record</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        將最上層的 JSON 物件展開為一個資料列，其具有由 <code class="literal">AS</code> 子句所定義的複合型別。（如同所有回傳 <code class="type">record</code> 的函式，呼叫的查詢必須以 <code class="literal">AS</code> 子句明確定義記錄的結構。）輸出記錄會從 JSON 物件的欄位填入，方式與上面針對 <code class="function">json[b]_populate_record</code> 所述的相同。由於沒有輸入的記錄值，不相符的欄位一律會填入 null。
       </p>
<p>
<code class="literal">create type myrowtype as (a int, b text);</code>
</p>
<p>
<code class="literal">select * from json_to_record('{"a":1,"b":[1,2,3],"c":[1,2,3],"e":"bar","r": {"a": 123, "b": "a b c"}}') as x(a int, b text, c int[], d text, r myrowtype)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |    b    |    c    | d |       r
---+---------+---------+---+---------------
 1 | [1,2,3] | {1,2,3} |   | (123,"a b c")
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.13.1.1.1"></a>
<code class="function">json_to_recordset</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.13.1.2.1"></a>
<code class="function">jsonb_to_recordset</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        將最上層的物件 JSON 陣列展開為一組資料列，這些資料列具有由 <code class="literal">AS</code> 子句所定義的複合型別。（如同所有回傳 <code class="type">record</code> 的函式，呼叫的查詢必須以 <code class="literal">AS</code> 子句明確定義記錄的結構。）JSON 陣列的每個元素，都會依照上面針對 <code class="function">json[b]_populate_record</code> 所述的方式處理。
       </p>
<p>
<code class="literal">select * from json_to_recordset('[{"a":1,"b":"foo"}, {"a":"2","c":"bar"}]') as x(a int, b text)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |  b
---+-----
 1 | foo
 2 |
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.14.1.1.1"></a>
<code class="function">jsonb_set</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>create_if_missing</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        回傳 <em class="parameter"><code>target</code></em>，其中由 <em class="parameter"><code>path</code></em> 指定的項目被替換為 <em class="parameter"><code>new_value</code></em>；或者在其中加入 <em class="parameter"><code>new_value</code></em>，前提是 <em class="parameter"><code>create_if_missing</code></em> 為 true（這是預設值），且由 <em class="parameter"><code>path</code></em> 指定的項目不存在。路徑中所有較前面的步驟都必須存在，否則會原封不動地回傳 <em class="parameter"><code>target</code></em>。與路徑導向的運算子一樣，出現在 <em class="parameter"><code>path</code></em> 中的負整數會從 JSON 陣列的結尾倒數。如果最後一個路徑步驟是超出範圍的陣列索引，且 <em class="parameter"><code>create_if_missing</code></em> 為 true，則當索引為負數時，新值會加在陣列的開頭；當索引為正數時，則加在陣列的結尾。
       </p>
<p>
<code class="literal">jsonb_set('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', '[2,3,4]', false)</code>
        → <code class="returnvalue">[{"f1": [2, 3, 4], "f2": null}, 2, null, 3]</code>
</p>
<p>
<code class="literal">jsonb_set('[{"f1":1,"f2":null},2]', '{0,f3}', '[2,3,4]')</code>
        → <code class="returnvalue">[{"f1": 1, "f2": null, "f3": [2, 3, 4]}, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.15.1.1.1"></a>
<code class="function">jsonb_set_lax</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>create_if_missing</code></em> <code class="type">boolean</code> [<span class="optional">, <em class="parameter"><code>null_value_treatment</code></em> <code class="type">text</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        如果 <em class="parameter"><code>new_value</code></em> 不是 <code class="literal">NULL</code>，其行為與 <code class="literal">jsonb_set</code> 完全相同。否則，其行為取決於 <em class="parameter"><code>null_value_treatment</code></em> 的值，該值必須是 <code class="literal">'raise_exception'</code>、<code class="literal">'use_json_null'</code>、<code class="literal">'delete_key'</code> 或 <code class="literal">'return_target'</code> 之一。預設值為 <code class="literal">'use_json_null'</code>。
       </p>
<p>
<code class="literal">jsonb_set_lax('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', null)</code>
        → <code class="returnvalue">[{"f1": null, "f2": null}, 2, null, 3]</code>
</p>
<p>
<code class="literal">jsonb_set_lax('[{"f1":99,"f2":null},2]', '{0,f3}', null, true, 'return_target')</code>
        → <code class="returnvalue">[{"f1": 99, "f2": null}, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.16.1.1.1"></a>
<code class="function">jsonb_insert</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>insert_after</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        回傳 <em class="parameter"><code>target</code></em>，其中已插入 <em class="parameter"><code>new_value</code></em>。如果由 <em class="parameter"><code>path</code></em> 指定的項目是陣列元素，<em class="parameter"><code>new_value</code></em> 會在 <em class="parameter"><code>insert_after</code></em> 為 false（這是預設值）時插入在該項目之前，在 <em class="parameter"><code>insert_after</code></em> 為 true 時則插入在該項目之後。如果由 <em class="parameter"><code>path</code></em> 指定的項目是物件欄位，<em class="parameter"><code>new_value</code></em> 只有在物件尚未包含該鍵時才會被插入。路徑中所有較前面的步驟都必須存在，否則會原封不動地回傳 <em class="parameter"><code>target</code></em>。與路徑導向的運算子一樣，出現在 <em class="parameter"><code>path</code></em> 中的負整數會從 JSON 陣列的結尾倒數。如果最後一個路徑步驟是超出範圍的陣列索引，則當索引為負數時，新值會加在陣列的開頭；當索引為正數時，則加在陣列的結尾。
       </p>
<p>
<code class="literal">jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"')</code>
        → <code class="returnvalue">{"a": [0, "new_value", 1, 2]}</code>
</p>
<p>
<code class="literal">jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"', true)</code>
        → <code class="returnvalue">{"a": [0, 1, "new_value", 2]}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.17.1.1.1"></a>
<code class="function">json_strip_nulls</code> ( <em class="parameter"><code>target</code></em> <code class="type">json</code> [<span class="optional">,<em class="parameter"><code>strip_in_arrays</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.17.1.2.1"></a>
<code class="function">jsonb_strip_nulls</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code> [<span class="optional">,<em class="parameter"><code>strip_in_arrays</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        從指定的 JSON 值中，遞迴地刪除所有值為 null 的物件欄位。如果 <em class="parameter"><code>strip_in_arrays</code></em> 為 true（預設為 false），null 陣列元素也會被移除；否則不會移除它們。單獨的 null 值永遠不會被移除。
       </p>
<p>
<code class="literal">json_strip_nulls('[{"f1":1, "f2":null}, 2, null, 3]')</code>
        → <code class="returnvalue">[{"f1":1},2,null,3]</code>
</p>
<p>
<code class="literal">jsonb_strip_nulls('[1,2,null,3,4]', true)</code>
        → <code class="returnvalue">[1,2,3,4]</code>
</p>
</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.18.1.1.1"></a>
<code class="function">jsonb_path_exists</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢查對於指定的 JSON 值，JSON 路徑是否回傳任何項目。（這只對符合 SQL 標準的 JSON 路徑運算式有用，對<a class="link" href="../functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>則沒有用處，因為後者一定會回傳一個值。）如果指定了 <em class="parameter"><code>vars</code></em> 引數，它必須是一個 JSON 物件，其欄位提供要代入 <code class="type">jsonpath</code> 運算式中的具名值。如果指定了 <em class="parameter"><code>silent</code></em> 引數且其值為 <code class="literal">true</code>，函式會抑制與 <code class="literal">@?</code> 及 <code class="literal">@@</code> 運算子相同的錯誤。
       </p>
<p>
<code class="literal">jsonb_path_exists('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.19.1.1.1"></a>
<code class="function">jsonb_path_match</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        回傳對指定的 JSON 值進行 JSON 路徑述詞檢查的 SQL 布林結果。（這只對<a class="link" href="../functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>有用，對符合 SQL 標準的 JSON 路徑運算式則沒有用處，因為如果路徑結果不是單一的布林值，它不是失敗就是回傳 <code class="literal">NULL</code>。）選用的 <em class="parameter"><code>vars</code></em> 與 <em class="parameter"><code>silent</code></em> 引數的作用與 <code class="function">jsonb_path_exists</code> 的相同。
       </p>
<p>
<code class="literal">jsonb_path_match('{"a":[1,2,3,4,5]}', 'exists($.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max))', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.20.1.1.1"></a>
<code class="function">jsonb_path_query</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p>
        回傳對於指定的 JSON 值，JSON 路徑所回傳的所有 JSON 項目。對於符合 SQL 標準的 JSON 路徑運算式，它會回傳從 <em class="parameter"><code>target</code></em> 中選取的 JSON 值。對於<a class="link" href="../functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>，它會回傳述詞檢查的結果：<code class="literal">true</code>、<code class="literal">false</code> 或 <code class="literal">null</code>。選用的 <em class="parameter"><code>vars</code></em> 與 <em class="parameter"><code>silent</code></em> 引數的作用與 <code class="function">jsonb_path_exists</code> 的相同。
       </p>
<p>
<code class="literal">select * from jsonb_path_query('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_path_query
------------------
 2
 3
 4
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.21.1.1.1"></a>
<code class="function">jsonb_path_query_array</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        以 JSON 陣列的形式，回傳對於指定的 JSON 值，JSON 路徑所回傳的所有 JSON 項目。參數與 <code class="function">jsonb_path_query</code> 的相同。
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">[2, 3, 4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.22.1.1.1"></a>
<code class="function">jsonb_path_query_first</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        回傳對於指定的 JSON 值，JSON 路徑所回傳的第一個 JSON 項目；如果沒有結果，則回傳 <code class="literal">NULL</code>。參數與 <code class="function">jsonb_path_query</code> 的相同。
       </p>
<p>
<code class="literal">jsonb_path_query_first('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.1.1"></a>
<code class="function">jsonb_path_exists_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.2.1"></a>
<code class="function">jsonb_path_match_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.3.1"></a>
<code class="function">jsonb_path_query_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.4.1"></a>
<code class="function">jsonb_path_query_array_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.5.1"></a>
<code class="function">jsonb_path_query_first_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        這些函式的作用與上面所述、不帶 <code class="literal">_tz</code> 字尾的對應函式相同，差別在於這些函式支援需要具時區感知之轉換的日期／時間值比較。下面的範例需要將只有日期的值 <code class="literal">2015-08-02</code> 解讀為帶時區的時間戳記，因此結果取決於目前的 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> 設定。由於這種相依性，這些函式被標記為 stable，這表示這些函式不能用於索引中。它們的對應函式是 immutable，因此可以用於索引中；但如果要求它們進行這類比較，就會拋出錯誤。
       </p>
<p>
<code class="literal">jsonb_path_exists_tz('["2015-08-01 12:00:00-05"]', '$[*] ? (@.datetime() &lt; "2015-08-02".datetime())')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.24.1.1.1"></a>
<code class="function">jsonb_pretty</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將指定的 JSON 值轉換為經過美化輸出（pretty-printed）、帶有縮排的文字。
       </p>
<p>
<code class="literal">jsonb_pretty('[{"f1":1,"f2":null}, 2]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
[
    {
        "f1": 1,
        "f2": null
    },
    2
]
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.25.1.1.1"></a>
<code class="function">json_typeof</code> ( <code class="type">json</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.25.1.2.1"></a>
<code class="function">jsonb_typeof</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        以文字字串的形式回傳最上層 JSON 值的型別。可能的型別有 <code class="literal">object</code>、<code class="literal">array</code>、<code class="literal">string</code>、<code class="literal">number</code>、<code class="literal">boolean</code> 與 <code class="literal">null</code>。（<code class="literal">null</code> 結果不應與 SQL NULL 混淆；請參閱範例。）
       </p>
<p>
<code class="literal">json_typeof('-123.4')</code>
        → <code class="returnvalue">number</code>
</p>
<p>
<code class="literal">json_typeof('null'::json)</code>
        → <code class="returnvalue">null</code>
</p>
<p>
<code class="literal">json_typeof(NULL::json) IS NULL</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

[返回 9.16. JSON 函式與運算子](../functions-json.md#functions-json)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（原文版本：18.6；核對日期：2026-09-11）
