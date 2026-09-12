<a id="FUNCTIONS-JSON"></a>

## 9.16. JSON 函式與運算子 [#](#FUNCTIONS-JSON)

[9.16.1. 處理與建立 JSON 資料](functions-json.md#FUNCTIONS-JSON-PROCESSING)

[9.16.2. SQL/JSON 路徑語言](functions-json.md#FUNCTIONS-SQLJSON-PATH)

[9.16.3. SQL/JSON 查詢函式](functions-json.md#SQLJSON-QUERY-FUNCTIONS)

[9.16.4. JSON_TABLE](functions-json.md#FUNCTIONS-SQLJSON-TABLE)

<a id="id-1.5.8.22.2"></a><a id="id-1.5.8.22.3"></a>

本節說明：

* 用於處理與建立 JSON 資料的函式與運算子
* SQL/JSON 路徑語言
* SQL/JSON 查詢函式

為了在 SQL 環境中原生支援 JSON 資料型別，PostgreSQL 實作了 *SQL/JSON 資料模型*。這個模型由項目的序列所組成。每個項目可以存放 SQL 純量值（另外加上一個 SQL/JSON null 值），以及使用 JSON 陣列與物件的複合資料結構。這個模型是將 JSON 規格 [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159) 中隱含的資料模型加以形式化的結果。

SQL/JSON 讓你能夠在交易支援之下，將 JSON 資料與一般的 SQL 資料一併處理，包括：

* 將 JSON 資料上傳到資料庫，並以字元字串或二進位字串的形式儲存在一般的 SQL 欄位中。
* 從關聯式資料產生 JSON 物件與陣列。
* 使用 SQL/JSON 查詢函式與 SQL/JSON 路徑語言運算式來查詢 JSON 資料。

若要進一步了解 SQL/JSON 標準，請參閱 [[sqltr-19075-6]](../../bibliography.md#SQLTR-19075-6)。關於 PostgreSQL 所支援之 JSON 型別的詳細資訊，請參閱[第 8.14 節](../datatype/datatype-json.md)。

<a id="FUNCTIONS-JSON-PROCESSING"></a>

### 9.16.1. 處理與建立 JSON 資料 [#](#FUNCTIONS-JSON-PROCESSING)

[表 9.47](functions-json.md#FUNCTIONS-JSON-OP-TABLE) 列出了可用於 JSON 資料型別的運算子（請參閱[第 8.14 節](../datatype/datatype-json.md)）。此外，[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子也可用於 `jsonb`，但不能用於 `json`。這些比較運算子遵循[第 8.14.4 節](../datatype/datatype-json.md#JSON-INDEXING)所述之 B-tree 操作的排序規則。另請參閱[第 9.21 節](functions-aggregate.md)中的彙總函式 `json_agg`（將記錄值彙總為 JSON）、彙總函式 `json_object_agg`（將成對的值彙總為 JSON 物件），以及它們對應的 `jsonb` 版本 `jsonb_agg` 與 `jsonb_object_agg`。

<a id="FUNCTIONS-JSON-OP-TABLE"></a>

**表 9.47. `json` 與 `jsonb` 運算子**

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

另外還有一些只適用於 `jsonb` 的運算子，如[表 9.48](functions-json.md#FUNCTIONS-JSONB-OP-TABLE) 所示。[第 8.14.4 節](../datatype/datatype-json.md#JSON-INDEXING)說明了如何使用這些運算子來有效率地搜尋已建立索引的 `jsonb` 資料。

<a id="FUNCTIONS-JSONB-OP-TABLE"></a>

**表 9.48. 其他 `jsonb` 運算子**

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
        第一個 JSON 值是否包含第二個 JSON 值？（關於包含的詳細說明，請參閱<a class="xref" href="../datatype/datatype-json.md#JSON-CONTAINMENT">第 8.14.3 節</a>。）
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
        對於指定的 JSON 值，JSON 路徑是否回傳任何項目？（這只對符合 SQL 標準的 JSON 路徑運算式有用，對<a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>則沒有用處，因為後者一定會回傳一個值。）
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ &gt; 2)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@@</code> <code class="type">jsonpath</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        回傳對指定的 JSON 值進行 JSON 路徑述詞檢查的結果。（這只對<a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>有用，對符合 SQL 標準的 JSON 路徑運算式則沒有用處，因為如果路徑結果不是單一的布林值，它會回傳 <code class="literal">NULL</code>。）
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] &gt; 2'</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

### 注意

`jsonpath` 運算子 `@?` 與 `@@` 會抑制下列錯誤：缺少物件欄位或陣列元素、非預期的 JSON 項目型別，以及日期時間與數值錯誤。下面所述與 `jsonpath` 相關的函式，也可以指示它們抑制這些類型的錯誤。在搜尋結構不一的 JSON 文件集合時，這種行為可能很有幫助。

[表 9.49](functions-json.md#FUNCTIONS-JSON-CREATION-TABLE) 列出了可用於建構 `json` 與 `jsonb` 值的函式。這個表格中的某些函式具有 `RETURNING` 子句，用來指定回傳的資料型別。它必須是 `json`、`jsonb`、`bytea`、字元字串型別（`text`、`char` 或 `varchar`）之一，或是可以轉換為 `json` 的型別。預設會回傳 `json` 型別。

<a id="FUNCTIONS-JSON-CREATION-TABLE"></a>

**表 9.49. JSON 建立函式**

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
</p></td></tr></tbody><tbody class="footnotes"><tr><td colspan="1"><div class="footnote" id="ftn.id-1.5.8.22.8.9.2.2.1.1.3.4"><p><a class="para" href="#id-1.5.8.22.8.9.2.2.1.1.3.4"><sup class="para">[a] </sup></a>例如，<a class="xref" href="../../appendixes/contrib/hstore.md">hstore</a> 擴充功能具有從 <code class="type">hstore</code> 到 <code class="type">json</code> 的型別轉換，因此透過 JSON 建立函式轉換的 <code class="type">hstore</code> 值，會以 JSON 物件表示，而不是以原始的字串值表示。
         </p></div></td></tr></tbody></table>

<br>

[表 9.50](functions-json.md#FUNCTIONS-SQLJSON-MISC) 詳細列出了用於測試 JSON 的 SQL/JSON 功能。

<a id="FUNCTIONS-SQLJSON-MISC"></a>

**表 9.50. SQL/JSON 測試函式**

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

[表 9.51](functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE) 列出了可用於處理 `json` 與 `jsonb` 值的函式。

<a id="FUNCTIONS-JSON-PROCESSING-TABLE"></a>

**表 9.51. JSON 處理函式**

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
        檢查對於指定的 JSON 值，JSON 路徑是否回傳任何項目。（這只對符合 SQL 標準的 JSON 路徑運算式有用，對<a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>則沒有用處，因為後者一定會回傳一個值。）如果指定了 <em class="parameter"><code>vars</code></em> 引數，它必須是一個 JSON 物件，其欄位提供要代入 <code class="type">jsonpath</code> 運算式中的具名值。如果指定了 <em class="parameter"><code>silent</code></em> 引數且其值為 <code class="literal">true</code>，函式會抑制與 <code class="literal">@?</code> 及 <code class="literal">@@</code> 運算子相同的錯誤。
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
        回傳對指定的 JSON 值進行 JSON 路徑述詞檢查的 SQL 布林結果。（這只對<a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>有用，對符合 SQL 標準的 JSON 路徑運算式則沒有用處，因為如果路徑結果不是單一的布林值，它不是失敗就是回傳 <code class="literal">NULL</code>。）選用的 <em class="parameter"><code>vars</code></em> 與 <em class="parameter"><code>silent</code></em> 引數的作用與 <code class="function">jsonb_path_exists</code> 的相同。
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
        回傳對於指定的 JSON 值，JSON 路徑所回傳的所有 JSON 項目。對於符合 SQL 標準的 JSON 路徑運算式，它會回傳從 <em class="parameter"><code>target</code></em> 中選取的 JSON 值。對於<a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">述詞檢查運算式</a>，它會回傳述詞檢查的結果：<code class="literal">true</code>、<code class="literal">false</code> 或 <code class="literal">null</code>。選用的 <em class="parameter"><code>vars</code></em> 與 <em class="parameter"><code>silent</code></em> 引數的作用與 <code class="function">jsonb_path_exists</code> 的相同。
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
        這些函式的作用與上面所述、不帶 <code class="literal">_tz</code> 字尾的對應函式相同，差別在於這些函式支援需要具時區感知之轉換的日期／時間值比較。下面的範例需要將只有日期的值 <code class="literal">2015-08-02</code> 解讀為帶時區的時間戳記，因此結果取決於目前的 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> 設定。由於這種相依性，這些函式被標記為 stable，這表示這些函式不能用於索引中。它們的對應函式是 immutable，因此可以用於索引中；但如果要求它們進行這類比較，就會拋出錯誤。
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

<a id="FUNCTIONS-SQLJSON-PATH"></a>

### 9.16.2. SQL/JSON 路徑語言 [#](#FUNCTIONS-SQLJSON-PATH)

<a id="id-1.5.8.22.9.2"></a>

SQL/JSON 路徑運算式指定要從 JSON 值中取出的項目，類似於用來存取 XML 內容的 XPath 運算式。在 PostgreSQL 中，路徑運算式實作為 `jsonpath` 資料型別，並且可以使用[第 8.14.7 節](../datatype/datatype-json.md#DATATYPE-JSONPATH)所述的任何元素。

JSON 查詢函式與運算子會將所提供的路徑運算式傳遞給*路徑引擎*進行求值。如果運算式與所查詢的 JSON 資料相符，就會回傳對應的 JSON 項目或項目集合。如果沒有相符的結果，依函式的不同，結果會是 `NULL`、`false` 或錯誤。路徑運算式以 SQL/JSON 路徑語言撰寫，並且可以包含算術運算式與函式。

路徑運算式由 `jsonpath` 資料型別所允許的一連串元素組成。路徑運算式通常由左至右求值，但你可以使用括號來改變運算的順序。如果求值成功，就會產生一個 JSON 項目的序列，並將求值結果回傳給完成指定計算的 JSON 查詢函式。

若要參照正在查詢的 JSON 值（*內容項目*），請在路徑運算式中使用 `$` 變數。路徑的第一個元素一定是 `$`。其後可以接著一個或多個[存取子運算子](../datatype/datatype-json.md#TYPE-JSONPATH-ACCESSORS)，它們會逐層向下深入 JSON 結構，以取出內容項目的子項目。每個存取子運算子都作用於前一個求值步驟的結果，並從每個輸入項目產生零個、一個或多個輸出項目。

例如，假設你有一些來自 GPS 追蹤器、想要剖析的 JSON 資料，例如：

```

SELECT '{
  "track": {
    "segments": [
      {
        "location":   [ 47.763, 13.4034 ],
        "start time": "2018-10-14 10:05:14",
        "HR": 73
      },
      {
        "location":   [ 47.706, 13.2635 ],
        "start time": "2018-10-14 10:39:21",
        "HR": 135
      }
    ]
  }
}' AS json \gset
```

（上面的範例可以複製並貼到 psql 中，為接下來的範例做好準備。接著 psql 會將 `:'json'` 展開為包含該 JSON 值、並已適當加上引號的字串常數。）

若要取出可用的軌跡區段（track segment），你需要使用 `.key` 存取子運算子來向下穿過外層的 JSON 物件，例如：

```

=> select jsonb_path_query(:'json', '$.track.segments');
                                                                         jsonb_path_query
-----------------------------------------------------------​-----------------------------------------------------------​---------------------------------------------
 [{"HR": 73, "location": [47.763, 13.4034], "start time": "2018-10-14 10:05:14"}, {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}]
```

若要取出陣列的內容，通常會使用 `[*]` 運算子。下面的範例會回傳所有可用軌跡區段的位置座標：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

這裡我們從整個 JSON 輸入值（`$`）開始，接著 `.track` 存取子選取了與物件鍵 `"track"` 相關聯的 JSON 物件，然後 `.segments` 存取子選取了該物件中與鍵 `"segments"` 相關聯的 JSON 陣列，接著 `[*]` 存取子選取了該陣列的每個元素（產生一連串的項目），然後 `.location` 存取子選取了這些物件中各自與鍵 `"location"` 相關聯的 JSON 陣列。在這個範例中，每個物件都有 `"location"` 鍵；但如果其中有任何物件沒有這個鍵，`.location` 存取子對於該輸入項目就只會不產生任何輸出。

若只要回傳第一個區段的座標，可以在 `[]` 存取子運算子中指定對應的下標。請記得 JSON 陣列的索引是從 0 開始的：

```

=> select jsonb_path_query(:'json', '$.track.segments[0].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
```

每個路徑求值步驟的結果，都可以由[第 9.16.2.3 節](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS)所列的一個或多個 `jsonpath` 運算子與方法加以處理。每個方法名稱前面都必須加上一個句點。例如，你可以取得陣列的大小：

```

=> select jsonb_path_query(:'json', '$.track.segments.size()');
 jsonb_path_query
------------------
 2
```

在路徑運算式中使用 `jsonpath` 運算子與方法的更多範例，請見下方的[第 9.16.2.3 節](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS)。

路徑中也可以包含*篩選運算式*，其作用類似於 SQL 中的 `WHERE` 子句。篩選運算式以問號開頭，並在括號中提供條件：

```

? (condition)
```

篩選運算式必須緊接在它所要套用的路徑求值步驟之後撰寫。該步驟的結果會經過篩選，只保留滿足所提供條件的項目。SQL/JSON 定義了三值邏輯，因此條件可以產生 `true`、`false` 或 `unknown`。`unknown` 值扮演與 SQL `NULL` 相同的角色，並且可以用 `is unknown` 述詞來測試。後續的路徑求值步驟只會使用篩選運算式回傳 `true` 的那些項目。

可以在篩選運算式中使用的函式與運算子列於[表 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE)。在篩選運算式中，`@` 變數代表正在考量的值（也就是前一個路徑步驟的其中一個結果）。你可以在 `@` 之後撰寫存取子運算子來取出其組成項目。

例如，假設你想要取出所有高於 130 的心率值。你可以這樣做：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

若要取得具有這類值之區段的開始時間，你必須在選取開始時間之前先篩選掉不相關的區段，因此篩選運算式要套用在前一個步驟上，而條件中使用的路徑也會有所不同：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

如有需要，你可以依序使用多個篩選運算式。下面的範例會選取所有包含具有相關座標之位置以及高心率值之區段的開始時間：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

也可以在不同的巢狀層級使用篩選運算式。下面的範例會先依位置篩選所有區段，然後回傳這些區段的高心率值（如果有的話）：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

你也可以將篩選運算式彼此巢狀。這個範例會在軌跡包含任何具有高心率值的區段時回傳軌跡的大小，否則回傳空序列：

```

=> select jsonb_path_query(:'json', '$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()');
 jsonb_path_query
------------------
 2
```

<a id="FUNCTIONS-SQLJSON-DEVIATIONS"></a>

#### 9.16.2.1. 與 SQL 標準的差異 [#](#FUNCTIONS-SQLJSON-DEVIATIONS)

PostgreSQL 對 SQL/JSON 路徑語言的實作與 SQL/JSON 標準有下列差異。

<a id="FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS"></a>

##### 9.16.2.1.1. 布林述詞檢查運算式 [#](#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS)

作為 SQL 標準的延伸，PostgreSQL 的路徑運算式可以是布林述詞，而 SQL 標準只允許在篩選中使用述詞。SQL 標準的路徑運算式會回傳所查詢 JSON 值的相關元素，而述詞檢查運算式則會回傳述詞的單一三值 `jsonb` 結果：`true`、`false` 或 `null`。例如，我們可以撰寫這個符合 SQL 標準的篩選運算式：

```

=> select jsonb_path_query(:'json', '$.track.segments ?(@[*].HR > 130)');
                                jsonb_path_query
-----------------------------------------------------------​----------------------
 {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}
```

類似的述詞檢查運算式只會回傳 `true`，表示存在相符的項目：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR > 130');
 jsonb_path_query
------------------
 true
```

### 注意

`@@` 運算子（以及 `jsonb_path_match` 函式）必須使用述詞檢查運算式，而 `@?` 運算子（或 `jsonb_path_exists` 函式）則不應使用述詞檢查運算式。

<a id="FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION"></a>

##### 9.16.2.1.2. 正規表示式的解讀 [#](#FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION)

在 `like_regex` 篩選中使用的正規表示式模式，其解讀方式有一些細微差異，如[第 9.16.2.4 節](functions-json.md#JSONPATH-REGULAR-EXPRESSIONS)所述。

<a id="FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES"></a>

#### 9.16.2.2. 嚴格模式與寬鬆模式 [#](#FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES)

查詢 JSON 資料時，路徑運算式可能與實際的 JSON 資料結構不相符。嘗試存取物件中不存在的成員或陣列中不存在的元素，被定義為結構錯誤。SQL/JSON 路徑運算式有兩種處理結構錯誤的模式：

* lax（寬鬆，預設）— 路徑引擎會隱含地讓所查詢的資料適應指定的路徑。任何無法依下述方式修正的結構錯誤都會被抑制，產生不相符的結果。
* strict（嚴格）— 如果發生結構錯誤，就會引發錯誤。

當 JSON 資料不符合預期的綱要時，寬鬆模式有助於讓 JSON 文件與路徑運算式相符。如果某個運算元不符合特定操作的要求，可以在執行該操作之前，自動將它包裝成 SQL/JSON 陣列，或是將其元素轉換為 SQL/JSON 序列來解除包裝。此外，比較運算子在寬鬆模式下會自動解除運算元的包裝，因此你可以直接比較 SQL/JSON 陣列。大小為 1 的陣列會被視為等於它唯一的元素。在下列情況下不會執行自動解除包裝：

* 路徑運算式包含 `type()` 或 `size()` 方法，這兩個方法分別回傳陣列的型別與元素個數。
* 所查詢的 JSON 資料包含巢狀陣列。在這種情況下，只有最外層的陣列會被解除包裝，所有內層陣列則保持不變。因此，在每個路徑求值步驟中，隱含的解除包裝只能向下深入一層。

例如，查詢上面列出的 GPS 資料時，在使用寬鬆模式下，你可以不必理會它儲存的是區段陣列這件事：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments.location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

在嚴格模式下，指定的路徑必須完全符合所查詢 JSON 文件的結構，因此使用這個路徑運算式會導致錯誤：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments.location');
ERROR:  jsonpath member accessor can only be applied to an object
```

若要得到與寬鬆模式相同的結果，你必須明確地解除 `segments` 陣列的包裝：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

寬鬆模式的解除包裝行為可能會導致出人意料的結果。例如，下面這個使用 `.**` 存取子的查詢，會將每個 `HR` 值都選取兩次：

```

=> select jsonb_path_query(:'json', 'lax $.**.HR');
 jsonb_path_query
------------------
 73
 135
 73
 135
```

會發生這種情況，是因為 `.**` 存取子同時選取了 `segments` 陣列及其每個元素，而 `.HR` 存取子在寬鬆模式下會自動解除陣列的包裝。為了避免出人意料的結果，我們建議只在嚴格模式下使用 `.**` 存取子。下面的查詢只會將每個 `HR` 值選取一次：

```

=> select jsonb_path_query(:'json', 'strict $.**.HR');
 jsonb_path_query
------------------
 73
 135
```

陣列的解除包裝也可能導致非預期的結果。請看這個選取所有 `location` 陣列的範例：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

如預期般，它會回傳完整的陣列。但套用篩選運算式會使陣列被解除包裝，以便對每個項目求值，結果只回傳符合運算式的項目：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
------------------
 47.763
 47.706
(2 rows)
```

儘管路徑運算式選取的是完整的陣列，結果仍是如此。請使用嚴格模式來恢復選取陣列：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

<a id="FUNCTIONS-SQLJSON-PATH-OPERATORS"></a>

#### 9.16.2.3. SQL/JSON 路徑運算子與方法 [#](#FUNCTIONS-SQLJSON-PATH-OPERATORS)

[表 9.52](functions-json.md#FUNCTIONS-SQLJSON-OP-TABLE) 列出了 `jsonpath` 中可用的運算子與方法。請注意，一元運算子與方法可以套用在前一個路徑步驟所產生的多個值上，而二元運算子（加法等）只能套用在單一值上。在寬鬆模式下，套用在陣列上的方法會對陣列中的每個值執行。例外的是 `.type()` 與 `.size()`，它們會套用在陣列本身。

<a id="FUNCTIONS-SQLJSON-OP-TABLE"></a>

**表 9.52. `jsonpath` 運算子與方法**

<table border="1" class="table" summary="jsonpath Operators and Methods"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator/Method
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        加法
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '$[0] + 3')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        一元正號（不做任何運算）；與加法不同，它可以對多個值逐一進行
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '+ $.x')</code>
        → <code class="returnvalue">[2, 3, 4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        減法
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '7 - $[0]')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        取負值；與減法不同，它可以對多個值逐一進行
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '- $.x')</code>
        → <code class="returnvalue">[-2, -3, -4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">*</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        乘法
       </p>
<p>
<code class="literal">jsonb_path_query('[4]', '2 * $[0]')</code>
        → <code class="returnvalue">8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">/</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        除法
       </p>
<p>
<code class="literal">jsonb_path_query('[8.5]', '$[0] / 2')</code>
        → <code class="returnvalue">4.2500000000000000</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">%</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        模數（餘數）
       </p>
<p>
<code class="literal">jsonb_path_query('[32]', '$[0] % 10')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">type()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        JSON 項目的型別（請參閱 <code class="function">json_typeof</code>）
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "2", {}]', '$[*].type()')</code>
        → <code class="returnvalue">["number", "string", "object"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">size()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        JSON 項目的大小（陣列元素的個數；如果不是陣列則為 1）
       </p>
<p>
<code class="literal">jsonb_path_query('{"m": [11, 15]}', '$.m.size()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">boolean()</code>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        從 JSON 布林值、數值或字串轉換而來的布林值
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "yes", false]', '$[*].boolean()')</code>
        → <code class="returnvalue">[true, true, false]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">string()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        從 JSON 布林值、數值、字串或日期時間轉換而來的字串值
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1.23, "xyz", false]', '$[*].string()')</code>
        → <code class="returnvalue">["1.23", "xyz", "false"]</code>
</p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp().string()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">double()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的近似浮點數
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "1.9"}', '$.len.double() * 2')</code>
        → <code class="returnvalue">3.8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">ceiling()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        大於或等於給定數值的最接近整數
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.3}', '$.h.ceiling()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">floor()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        小於或等於給定數值的最接近整數
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.7}', '$.h.floor()')</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">abs()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        給定數值的絕對值
       </p>
<p>
<code class="literal">jsonb_path_query('{"z": -0.3}', '$.z.abs()')</code>
        → <code class="returnvalue">0.3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">bigint()</code>
        → <code class="returnvalue"><em class="replaceable"><code>bigint</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的大整數值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "9876543219"}', '$.len.bigint()')</code>
        → <code class="returnvalue">9876543219</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">decimal( [ <em class="replaceable"><code>precision</code></em> [ , <em class="replaceable"><code>scale</code></em> ] ] )</code>
        → <code class="returnvalue"><em class="replaceable"><code>decimal</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來、經過捨入的十進位值（<code class="literal">precision</code> 與 <code class="literal">scale</code> 必須是整數值）
       </p>
<p>
<code class="literal">jsonb_path_query('1234.5678', '$.decimal(6, 2)')</code>
        → <code class="returnvalue">1234.57</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">integer()</code>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的整數值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "12345"}', '$.len.integer()')</code>
        → <code class="returnvalue">12345</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">number()</code>
        → <code class="returnvalue"><em class="replaceable"><code>numeric</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的 numeric 值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "123.45"}', '$.len.number()')</code>
        → <code class="returnvalue">123.45</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime()</code> → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>（請參閱注意事項）
       </p>
<p>
        從字串轉換而來的日期／時間值
       </p>
<p>
<code class="literal">jsonb_path_query('["2015-8-1", "2015-08-12"]', '$[*] ? (@.datetime() &lt; "2015-08-2".datetime())')</code>
        → <code class="returnvalue">"2015-8-1"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime(<em class="replaceable"><code>template</code></em>)</code> → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>（請參閱注意事項）
       </p>
<p>
        使用指定的 <code class="function">to_timestamp</code> 樣板，從字串轉換而來的日期／時間值
       </p>
<p>
<code class="literal">jsonb_path_query_array('["12:30", "18:40"]', '$[*].datetime("HH24:MI")')</code>
        → <code class="returnvalue">["12:30:00", "18:40:00"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">date()</code>
        → <code class="returnvalue"><em class="replaceable"><code>date</code></em></code>
</p>
<p>
        從字串轉換而來的日期值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15"', '$.date()')</code>
        → <code class="returnvalue">"2023-08-15"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間值
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56"', '$.time()')</code>
        → <code class="returnvalue">"12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789"', '$.time(2)')</code>
        → <code class="returnvalue">"12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間值
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56 +05:30"', '$.time_tz()')</code>
        → <code class="returnvalue">"12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789 +05:30"', '$.time_tz(2)')</code>
        → <code class="returnvalue">"12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間戳記值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間戳記值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789"', '$.timestamp(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間戳記值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56 +05:30"', '$.timestamp_tz()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間戳記值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789 +05:30"', '$.timestamp_tz(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>object</code></em> <code class="literal">.</code> <code class="literal">keyvalue()</code>
        → <code class="returnvalue"><em class="replaceable"><code>array</code></em></code>
</p>
<p>
        物件的鍵值對，表示為一個由物件組成的陣列，每個物件包含三個欄位：<code class="literal">"key"</code>、<code class="literal">"value"</code> 與 <code class="literal">"id"</code>；其中 <code class="literal">"id"</code> 是該鍵值對所屬之物件的唯一識別碼
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": "20", "y": 32}', '$.keyvalue()')</code>
        → <code class="returnvalue">[{"id": 0, "key": "x", "value": "20"}, {"id": 0, "key": "y", "value": 32}]</code>
</p></td></tr></tbody></table>

<br>

### 注意

`datetime()` 與 `datetime(template)` 方法的結果型別可以是 `date`、`timetz`、`time`、`timestamptz` 或 `timestamp`。這兩個方法都會動態地決定其結果型別。

`datetime()` 方法會依序嘗試將其輸入字串與 `date`、`timetz`、`time`、`timestamptz` 以及 `timestamp` 的 ISO 格式進行比對。它會在第一個相符的格式停止，並產生對應的資料型別。

`datetime(template)` 方法會依據所提供之樣板字串中使用的欄位來決定結果型別。

`datetime()` 與 `datetime(template)` 方法使用與 SQL 函式 `to_timestamp` 相同的剖析規則（請參閱[第 9.8 節](functions-formatting.md)），但有三個例外。第一，這些方法不允許不相符的樣板模式。第二，樣板字串中只允許使用下列分隔符號：減號、句點、斜線（solidus）、逗號、撇號、分號、冒號與空白。第三，樣板字串中的分隔符號必須與輸入字串完全相符。

如果需要比較不同的日期／時間型別，會套用隱含的型別轉換。`date` 值可以轉換為 `timestamp` 或 `timestamptz`，`timestamp` 可以轉換為 `timestamptz`，而 `time` 可以轉換為 `timetz`。不過，除了第一種以外，這些轉換都取決於目前的 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定，因此只能在具時區感知能力的 `jsonpath` 函式中執行。同樣地，其他將字串轉換為日期／時間型別之日期／時間相關方法也會進行這種型別轉換，而這可能涉及目前的 [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定。因此，這些轉換也只能在具時區感知能力的 `jsonpath` 函式中執行。

[表 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE) 列出了可用的篩選運算式元素。

<a id="FUNCTIONS-SQLJSON-FILTER-EX-TABLE"></a>

**表 9.53. `jsonpath` 篩選運算式元素**

<table border="1" class="table" summary="jsonpath Filter Expression Elements"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Predicate/Value
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">==</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        相等比較（這個運算子以及其他比較運算子都適用於所有 JSON 純量值）
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == 1)')</code>
        → <code class="returnvalue">[1, 1]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == "a")')</code>
        → <code class="returnvalue">["a"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">!=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        不相等比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 1, 3]', '$[*] ? (@ != 1)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;&gt; "b")')</code>
        → <code class="returnvalue">["a", "c"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        小於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &lt; 2)')</code>
        → <code class="returnvalue">[1]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        小於或等於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;= "b")')</code>
        → <code class="returnvalue">["a", "b"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        大於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt; 2)')</code>
        → <code class="returnvalue">[3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        大於或等於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt;= 2)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">true</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON 常數 <code class="literal">true</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == true)')</code>
        → <code class="returnvalue">{"name": "Chris", "parent": true}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">false</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON 常數 <code class="literal">false</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == false)')</code>
        → <code class="returnvalue">{"name": "John", "parent": false}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">null</code>
        → <code class="returnvalue"><em class="replaceable"><code>value</code></em></code>
</p>
<p>
        JSON 常數 <code class="literal">null</code>（請注意，與 SQL 不同，與 <code class="literal">null</code> 的比較會正常運作）
       </p>
<p>
<code class="literal">jsonb_path_query('[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]', '$[*] ? (@.job == null) .name')</code>
        → <code class="returnvalue">"Mary"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">&amp;&amp;</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 AND
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &gt; 1 &amp;&amp; @ &lt; 5)')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">||</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 OR
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &lt; 1 || @ &gt; 5)')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">!</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 NOT
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (!(@ &lt; 5))')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">is unknown</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試布林條件是否為 <code class="literal">unknown</code>。
       </p>
<p>
<code class="literal">jsonb_path_query('[-1, 2, 7, "foo"]', '$[*] ? ((@ &gt; 0) is unknown)')</code>
        → <code class="returnvalue">"foo"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">like_regex</code> <em class="replaceable"><code>string</code></em> [<span class="optional"> <code class="literal">flag</code> <em class="replaceable"><code>string</code></em> </span>]
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試第一個運算元是否符合第二個運算元所給的正規表示式，並可選擇性地套用由 <code class="literal">flag</code> 字元字串所描述的修改（請參閱<a class="xref" href="functions-json.md#JSONPATH-REGULAR-EXPRESSIONS">第 9.16.2.4 節</a>）。
       </p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c")')</code>
        → <code class="returnvalue">["abc", "abdacb"]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c" flag "i")')</code>
        → <code class="returnvalue">["abc", "aBdC", "abdacb"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">starts with</code> <em class="replaceable"><code>string</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試第二個運算元是否為第一個運算元的開頭子字串。
       </p>
<p>
<code class="literal">jsonb_path_query('["John Smith", "Mary Stone", "Bob Johnson"]', '$[*] ? (@ starts with "John")')</code>
        → <code class="returnvalue">"John Smith"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">exists</code> <code class="literal">(</code> <em class="replaceable"><code>path_expression</code></em> <code class="literal">)</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試路徑運算式是否至少符合一個 SQL/JSON 項目。如果路徑運算式會導致錯誤，就回傳 <code class="literal">unknown</code>；第二個範例利用這一點，避免在嚴格模式下發生鍵不存在的錯誤。
       </p>
<p>
<code class="literal">jsonb_path_query('{"x": [1, 2], "y": [2, 4]}', 'strict $.* ? (exists (@ ? (@[*] &gt; 2)))')</code>
        → <code class="returnvalue">[2, 4]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('{"value": 41}', 'strict $ ? (exists (@.name)) .name')</code>
        → <code class="returnvalue">[]</code>
</p></td></tr></tbody></table>

<br>

<a id="JSONPATH-REGULAR-EXPRESSIONS"></a>

#### 9.16.2.4. SQL/JSON 正規表示式 [#](#JSONPATH-REGULAR-EXPRESSIONS)

<a id="id-1.5.8.22.9.23.2"></a>

SQL/JSON 路徑運算式可以使用 `like_regex` 篩選，將文字與正規表示式進行比對。例如，下面的 SQL/JSON 路徑查詢會以不區分大小寫的方式，比對陣列中所有以英文母音開頭的字串：

```

$[*] ? (@ like_regex "^[aeiou]" flag "i")
```

選用的 `flag` 字串可以包含下列一個或多個字元：`i` 表示不區分大小寫的比對，`m` 允許 `^` 與 `$` 在換行處比對，`s` 允許 `.` 比對換行字元，而 `q` 則將整個模式加上引號（使行為簡化為單純的子字串比對）。

SQL/JSON 標準的正規表示式定義借用自 `LIKE_REGEX` 運算子，而該運算子又使用 XQuery 標準。PostgreSQL 目前並不支援 `LIKE_REGEX` 運算子。因此，`like_regex` 篩選是使用[第 9.7.3 節](functions-matching.md#FUNCTIONS-POSIX-REGEXP)所述的 POSIX 正規表示式引擎實作的。這導致了與標準 SQL/JSON 行為之間的各種細微差異，這些差異整理於[第 9.7.3.8 節](functions-matching.md#POSIX-VS-XQUERY)。不過請注意，該處所述的旗標字母不相容問題並不適用於 SQL/JSON，因為它會將 XQuery 的旗標字母轉換為 POSIX 引擎所預期的形式。

請記住，`like_regex` 的模式引數是一個 JSON 路徑字串字面值，依照[第 8.14.7 節](../datatype/datatype-json.md#DATATYPE-JSONPATH)所述的規則撰寫。這特別意味著，你想在正規表示式中使用的任何反斜線都必須重複兩次。例如，要比對根文件中只包含數字的字串值：

```

$.* ? (@ like_regex "^\\d+$")
```

<a id="SQLJSON-QUERY-FUNCTIONS"></a>

### 9.16.3. SQL/JSON 查詢函式 [#](#SQLJSON-QUERY-FUNCTIONS)

[表 9.54](functions-json.md#FUNCTIONS-SQLJSON-QUERYING) 所述的 SQL/JSON 函式 `JSON_EXISTS()`、`JSON_QUERY()` 與 `JSON_VALUE()` 可用來查詢 JSON 文件。這些函式都會將 *`path_expression`*（SQL/JSON 路徑查詢）套用到 *`context_item`*（文件）上。關於 *`path_expression`* 可以包含哪些內容的詳細資訊，請參閱[第 9.16.2 節](functions-json.md#FUNCTIONS-SQLJSON-PATH)。*`path_expression`* 也可以參照變數，變數的值是透過每個函式都支援的 `PASSING` 子句，以其各自的名稱來指定。*`context_item`* 可以是 `jsonb` 值，或是可以成功轉換為 `jsonb` 的字元字串。

<a id="FUNCTIONS-SQLJSON-QUERYING"></a>

**表 9.54. SQL/JSON 查詢函式**

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

### 注意

如果 *`context_item`* 運算式的型別還不是 `jsonb`，它會透過隱含的型別轉換轉為 `jsonb`。不過請注意，在該轉換過程中發生的任何剖析錯誤都會無條件拋出，也就是說，不會依照（明確指定或隱含的）`ON ERROR` 子句來處理。

### 注意

如果 *`path_expression`* 回傳 JSON `null`，`JSON_VALUE()` 會回傳 SQL NULL，而 `JSON_QUERY()` 則會原樣回傳 JSON `null`。

<a id="FUNCTIONS-SQLJSON-TABLE"></a>

### 9.16.4. JSON_TABLE [#](#FUNCTIONS-SQLJSON-TABLE)

<a id="id-1.5.8.22.11.2"></a>

`JSON_TABLE` 是一個 SQL/JSON 函式，它會查詢 JSON 資料，並將結果呈現為關聯式檢視表，讓你可以像一般 SQL 資料表那樣存取。你可以在 `SELECT`、`UPDATE` 或 `DELETE` 的 `FROM` 子句中使用 `JSON_TABLE`，也可以在 `MERGE` 陳述句中將它作為資料來源。

`JSON_TABLE` 以 JSON 資料作為輸入，使用 JSON 路徑運算式擷取所提供資料的一部分，作為所建構之檢視表的*資料列模式*（row pattern）。由資料列模式所給出的每個 SQL/JSON 值，都會作為所建構檢視表中一個獨立資料列的來源。

為了將資料列模式拆分為欄位，`JSON_TABLE` 提供了 `COLUMNS` 子句，用來定義所建立之檢視表的綱要。對於每個欄位，可以指定一個獨立的 JSON 路徑運算式，針對資料列模式進行求值，以取得一個 SQL/JSON 值，該值將成為指定輸出資料列中指定欄位的值。

儲存在資料列模式之巢狀層級中的 JSON 資料，可以使用 `NESTED PATH` 子句擷取。每個 `NESTED PATH` 子句都可以使用資料列模式某個巢狀層級的資料，產生一個或多個欄位。這些欄位可以使用外觀類似於最上層 COLUMNS 子句的 `COLUMNS` 子句來指定。由 NESTED COLUMNS 建構的資料列稱為*子資料列*（child row），它們會與由上層 `COLUMNS` 子句所指定之欄位建構出的資料列聯結，以得到最終檢視表中的資料列。子欄位本身也可以包含 `NESTED PATH` 規格，因此可以擷取位於任意巢狀層級的資料。在同一層級由多個 `NESTED PATH` 產生的欄位，彼此被視為*兄弟*（sibling），而它們與上層資料列聯結後的資料列會使用 UNION 加以合併。

`JSON_TABLE` 產生的資料列會以 lateral 方式聯結到產生它們的資料列，因此你不必明確地將所建構的檢視表與存放 JSON 資料的原始資料表進行聯結。

語法為：

```

JSON_TABLE (
    context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...] ]
    COLUMNS ( json_table_column [, ...] )
    [ { ERROR | EMPTY [ARRAY]} ON ERROR ]
)


where json_table_column is:

  name FOR ORDINALITY
  | name type
        [ FORMAT JSON [ENCODING UTF8]]
        [ PATH path_expression ]
        [ { WITHOUT | WITH { CONDITIONAL | [UNCONDITIONAL] } } [ ARRAY ] WRAPPER ]
        [ { KEEP | OMIT } QUOTES [ ON SCALAR STRING ] ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON EMPTY ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON ERROR ]
  | name type EXISTS [ PATH path_expression ]
        [ { ERROR | TRUE | FALSE | UNKNOWN } ON ERROR ]
  | NESTED [ PATH ] path_expression [ AS json_path_name ] COLUMNS ( json_table_column [, ...] )
```

下面會更詳細地說明每個語法元素。

`context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...]]`
:   *`context_item`* 指定要查詢的輸入文件，*`path_expression`* 是定義查詢的 SQL/JSON 路徑運算式，而 *`json_path_name`* 則是 *`path_expression`* 的選用名稱。選用的 `PASSING` 子句為 *`path_expression`* 中提到的變數提供資料值。使用上述元素對輸入資料求值的結果稱為*資料列模式*，用來作為所建構之檢視表中資料列值的來源。

`COLUMNS` ( *`json_table_column`* [, ...] )
:   `COLUMNS` 子句定義所建構之檢視表的綱要。在這個子句中，你可以指定每個欄位要填入的 SQL/JSON 值，該值是透過針對資料列模式套用 JSON 路徑運算式所取得。*`json_table_column`* 有下列幾種變形：

    *`name`* `FOR ORDINALITY`
    :   加入一個序數欄位，提供從 1 開始的循序資料列編號。每個 `NESTED PATH`（見下文）對於其中任何巢狀的序數欄位，都有自己的計數器。

    `name type [FORMAT JSON [ENCODING UTF8]] [ PATH path_expression ]`
    :   將針對資料列模式套用 *`path_expression`* 所取得的 SQL/JSON 值，強制轉換為指定的 *`type`* 之後，插入檢視表的輸出資料列中。

        指定 `FORMAT JSON` 可明確表示你預期該值是有效的 `json` 物件。只有當 *`type`* 是 `bpchar`、`bytea`、`character varying`、`name`、`json`、`jsonb`、`text` 之一，或是以這些型別為基礎的領域（domain）時，指定 `FORMAT JSON` 才有意義。

        你可以選擇性地指定 `WRAPPER` 與 `QUOTES` 子句來格式化輸出。請注意，如果同時指定了 `OMIT QUOTES` 與 `FORMAT JSON`，前者會覆寫後者，因為沒有加引號的字面值並不構成有效的 `json` 值。

        你可以選擇性地使用 `ON EMPTY` 與 `ON ERROR` 子句，分別指定當 JSON 路徑求值的結果為空時，以及當 JSON 路徑求值期間或將 SQL/JSON 值強制轉換為指定型別時發生錯誤時，要拋出錯誤還是回傳指定的值。兩者的預設都是回傳 `NULL` 值。

        ### 注意

        這個子句在內部會被轉換為 `JSON_VALUE` 或 `JSON_QUERY`，並具有與其相同的語意。如果指定的型別不是純量型別，或是出現了 `FORMAT JSON`、`WRAPPER` 或 `QUOTES` 子句中的任何一個，就會轉換為後者。

    *`name`* *`type`* `EXISTS` [ `PATH` *`path_expression`* ]
    :   將針對資料列模式套用 *`path_expression`* 所取得的布林值，強制轉換為指定的 *`type`* 之後，插入檢視表的輸出資料列中。

        該值對應於將 `PATH` 運算式套用到資料列模式後，是否產生任何值。

        指定的 *`type`* 應該要有從 `boolean` 型別轉換過來的型別轉換。

        你可以選擇性地使用 `ON ERROR`，指定當 JSON 路徑求值期間或將 SQL/JSON 值強制轉換為指定型別時發生錯誤時，要拋出錯誤還是回傳指定的值。預設是回傳布林值 `FALSE`。

        ### 注意

        這個子句在內部會被轉換為 `JSON_EXISTS`，並具有與其相同的語意。

    `NESTED [ PATH ]` *`path_expression`* [ `AS` *`json_path_name`* ] `COLUMNS` ( *`json_table_column`* [, ...] )
    :   從資料列模式的巢狀層級中擷取 SQL/JSON 值，依照 `COLUMNS` 子子句的定義產生一個或多個欄位，並將擷取出的 SQL/JSON 值插入這些欄位中。`COLUMNS` 子子句中的 *`json_table_column`* 運算式，使用與上層 `COLUMNS` 子句相同的語法。

        `NESTED PATH` 語法是遞迴的，因此你可以透過將數個 `NESTED PATH` 子子句彼此巢狀指定，向下深入多個巢狀層級。它讓你能夠在單一的函式呼叫中，將 JSON 物件與陣列的階層結構展開，而不必在 SQL 陳述句中串接多個 `JSON_TABLE` 運算式。

    ### 注意

    在上述 *`json_table_column`* 的每一種變形中，如果省略了 `PATH` 子句，就會使用路徑運算式 `$.name`，其中 *`name`* 是所提供的欄位名稱。

`AS` *`json_path_name`*
:   選用的 *`json_path_name`* 作為所提供之 *`path_expression`* 的識別符號。這個名稱必須是唯一的，且不得與欄位名稱相同。

{ `ERROR` | `EMPTY` } `ON ERROR`
:   選用的 `ON ERROR` 可用來指定在對最上層 *`path_expression`* 求值時如何處理錯誤。如果你希望拋出錯誤，請使用 `ERROR`；若要回傳空的資料表，也就是包含 0 筆資料列的資料表，請使用 `EMPTY`。請注意，這個子句不會影響對欄位求值時發生的錯誤，那些錯誤的行為取決於是否針對該欄位指定了 `ON ERROR` 子句。

範例

在接下來的範例中，將會使用下面這個包含 JSON 資料的資料表：

```

CREATE TABLE my_films ( js jsonb );

INSERT INTO my_films VALUES (
'{ "favorites" : [
   { "kind" : "comedy", "films" : [
     { "title" : "Bananas",
       "director" : "Woody Allen"},
     { "title" : "The Dinner Game",
       "director" : "Francis Veber" } ] },
   { "kind" : "horror", "films" : [
     { "title" : "Psycho",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "thriller", "films" : [
     { "title" : "Vertigo",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "drama", "films" : [
     { "title" : "Yojimbo",
       "director" : "Akira Kurosawa" } ] }
  ] }');
```

下面的查詢展示了如何使用 `JSON_TABLE`，將 `my_films` 資料表中的 JSON 物件轉換為一個檢視表，其中包含原始 JSON 中的鍵 `kind`、`title` 與 `director` 所對應的欄位，以及一個序數欄位：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*]' COLUMNS (
   id FOR ORDINALITY,
   kind text PATH '$.kind',
   title text PATH '$.films[*].title' WITH WRAPPER,
   director text PATH '$.films[*].director' WITH WRAPPER)) AS jt;
```

```

 id |   kind   |             title              |             director
----+----------+--------------------------------+----------------------------------
  1 | comedy   | ["Bananas", "The Dinner Game"] | ["Woody Allen", "Francis Veber"]
  2 | horror   | ["Psycho"]                     | ["Alfred Hitchcock"]
  3 | thriller | ["Vertigo"]                    | ["Alfred Hitchcock"]
  4 | drama    | ["Yojimbo"]                    | ["Akira Kurosawa"]
(4 rows)
```

下面是上述查詢的修改版本，展示了在最上層 JSON 路徑運算式所指定的篩選中使用 `PASSING` 引數，以及個別欄位的各種選項：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
     COLUMNS (
     id FOR ORDINALITY,
     kind text PATH '$.kind',
     title text FORMAT JSON PATH '$.films[*].title' OMIT QUOTES,
     director text PATH '$.films[*].director' KEEP QUOTES)) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

下面是上述查詢的修改版本，展示了使用 `NESTED PATH` 來填入 title 與 director 欄位，說明它們如何與上層的 id 與 kind 欄位聯結：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

下面是相同的查詢，但在根路徑中沒有篩選：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*]'
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |      title      |      director
----+----------+-----------------+--------------------
  1 | comedy   | Bananas         | "Woody Allen"
  1 | comedy   | The Dinner Game | "Francis Veber"
  2 | horror   | Psycho          | "Alfred Hitchcock"
  3 | thriller | Vertigo         | "Alfred Hitchcock"
  4 | drama    | Yojimbo         | "Akira Kurosawa"
(5 rows)
```

下面展示了另一個使用不同 `JSON` 物件作為輸入的查詢。它展示了 `NESTED` 路徑 `$.movies[*]` 與 `$.books[*]` 之間的 UNION「兄弟聯結」（sibling join），以及在 `NESTED` 層級使用 `FOR ORDINALITY` 欄位（欄位 `movie_id`、`book_id` 與 `author_id`）：

```

SELECT * FROM JSON_TABLE (
'{"favorites":
    [{"movies":
      [{"name": "One", "director": "John Doe"},
       {"name": "Two", "director": "Don Joe"}],
     "books":
      [{"name": "Mystery", "authors": [{"name": "Brown Dan"}]},
       {"name": "Wonder", "authors": [{"name": "Jun Murakami"}, {"name":"Craig Doe"}]}]
}]}'::json, '$.favorites[*]'
COLUMNS (
  user_id FOR ORDINALITY,
  NESTED '$.movies[*]'
    COLUMNS (
    movie_id FOR ORDINALITY,
    mname text PATH '$.name',
    director text),
  NESTED '$.books[*]'
    COLUMNS (
      book_id FOR ORDINALITY,
      bname text PATH '$.name',
      NESTED '$.authors[*]'
        COLUMNS (
          author_id FOR ORDINALITY,
          author_name text PATH '$.name'))));
```

```

 user_id | movie_id | mname | director | book_id |  bname  | author_id | author_name
---------+----------+-------+----------+---------+---------+-----------+--------------
       1 |        1 | One   | John Doe |         |         |           |
       1 |        2 | Two   | Don Joe  |         |         |           |
       1 |          |       |          |       1 | Mystery |         1 | Brown Dan
       1 |          |       |          |       2 | Wonder  |         1 | Jun Murakami
       1 |          |       |          |       2 | Wonder  |         2 | Craig Doe
(5 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（原文版本：18.6；核對日期：2026-09-11）
