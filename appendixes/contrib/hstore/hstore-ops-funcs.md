# F.17.2. hstore 運算子與函式

<a id="HSTORE-OPS-FUNCS"></a>

## F.17.2. `hstore` 運算子與函式 [#](#hstore-ops-funcs) <a href="#hstore-ops-funcs" id="hstore-ops-funcs"></a>

`hstore` 模組提供的運算子列於[表 F.6](#hstore-op-table)，函式列於[表 F.7](#hstore-func-table)。

<a id="HSTORE-OP-TABLE"></a>

### 表 F.6. `hstore` 運算子 [#](#hstore-op-table) <a href="#hstore-op-table" id="hstore-op-table"></a>

<table border="1" class="table" summary="hstore Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        傳回與指定鍵關聯的值；若不存在則傳回 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">'a=&gt;x, b=&gt;y'::hstore -&gt; 'a'</code>
        → <code class="returnvalue">x</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">-&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">text[]</code>
</p>
<p>
        傳回與指定鍵關聯的值；若不存在則傳回 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">'a=&gt;x, b=&gt;y, c=&gt;z'::hstore -&gt; ARRAY['c','a']</code>
        → <code class="returnvalue">{"z","x"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">||</code> <code class="type">hstore</code>
        → <code class="returnvalue">hstore</code>
</p>
<p>
        串接兩個 <code class="type">hstore</code>。
       </p>
<p>
<code class="literal">'a=&gt;b, c=&gt;d'::hstore || 'c=&gt;x, d=&gt;q'::hstore</code>
        → <code class="returnvalue">"a"=&gt;"b", "c"=&gt;"x", "d"=&gt;"q"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">?</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">hstore</code> 是否包含該鍵？
       </p>
<p>
<code class="literal">'a=&gt;1'::hstore ? 'a'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">?&amp;</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">hstore</code> 是否包含所有指定鍵？
       </p>
<p>
<code class="literal">'a=&gt;1,b=&gt;2'::hstore ?&amp; ARRAY['a','b']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">?|</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">hstore</code> 是否包含任何指定鍵？
       </p>
<p>
<code class="literal">'a=&gt;1,b=&gt;2'::hstore ?| ARRAY['b','c']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">@&gt;</code> <code class="type">hstore</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左運算元是否包含右運算元？
       </p>
<p>
<code class="literal">'a=&gt;b, b=&gt;1, c=&gt;NULL'::hstore @&gt; 'b=&gt;1'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">&lt;@</code> <code class="type">hstore</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左運算元是否包含於右運算元？
       </p>
<p>
<code class="literal">'a=&gt;c'::hstore &lt;@ 'a=&gt;b, b=&gt;1, c=&gt;NULL'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">-</code> <code class="type">text</code>
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從左運算元刪除鍵。
       </p>
<p>
<code class="literal">'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - 'b'::text</code>
        → <code class="returnvalue">"a"=&gt;"1", "c"=&gt;"3"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">-</code> <code class="type">text[]</code>
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從左運算元刪除鍵。
       </p>
<p>
<code class="literal">'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - ARRAY['a','b']</code>
        → <code class="returnvalue">"c"=&gt;"3"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">hstore</code> <code class="literal">-</code> <code class="type">hstore</code>
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從左運算元刪除與右運算元配對相符的配對。
       </p>
<p>
<code class="literal">'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - 'a=&gt;4, b=&gt;2'::hstore</code>
        → <code class="returnvalue">"a"=&gt;"1", "c"=&gt;"3"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyelement</code> <code class="literal">#=</code> <code class="type">hstore</code>
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        以 <code class="type">hstore</code> 的相符值取代左運算元（必須是複合型別）的欄位。
       </p>
<p>
<code class="literal">ROW(1,3) #= 'f1=&gt;11'::hstore</code>
        → <code class="returnvalue">(11,3)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">%%</code> <code class="type">hstore</code>
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為鍵和值交錯排列的陣列。
       </p>
<p>
<code class="literal">%% 'a=&gt;foo, b=&gt;bar'::hstore</code>
        → <code class="returnvalue">{a,foo,b,bar}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">%#</code> <code class="type">hstore</code>
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為二維鍵／值陣列。
       </p>
<p>
<code class="literal">%# 'a=&gt;foo, b=&gt;bar'::hstore</code>
        → <code class="returnvalue">{{a,foo},{b,bar}}</code>
</p></td></tr></tbody></table>

<br><a id="HSTORE-FUNC-TABLE"></a>

### 表 F.7. `hstore` 函式 [#](#hstore-func-table) <a href="#hstore-func-table" id="hstore-func-table"></a>

<table border="1" class="table" summary="hstore Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.1.1.1.1"></a>
<code class="function">hstore</code> ( <code class="type">record</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從記錄或資料列建構 <code class="type">hstore</code>。
       </p>
<p>
<code class="literal">hstore(ROW(1,2))</code>
        → <code class="returnvalue">"f1"=&gt;"1", "f2"=&gt;"2"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hstore</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從陣列建構 <code class="type">hstore</code>；該陣列可以是鍵／值陣列或二維陣列。
       </p>
<p>
<code class="literal">hstore(ARRAY['a','1','b','2'])</code>
        → <code class="returnvalue">"a"=&gt;"1", "b"=&gt;"2"</code>
</p>
<p>
<code class="literal">hstore(ARRAY[['c','3'],['d','4']])</code>
        → <code class="returnvalue">"c"=&gt;"3", "d"=&gt;"4"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hstore</code> ( <code class="type">text[]</code>, <code class="type">text[]</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        從分離的鍵和值陣列建構 <code class="type">hstore</code>。
       </p>
<p>
<code class="literal">hstore(ARRAY['a','b'], ARRAY['1','2'])</code>
        → <code class="returnvalue">"a"=&gt;"1", "b"=&gt;"2"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hstore</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        建立只含一個項目的 <code class="type">hstore</code>。
       </p>
<p>
<code class="literal">hstore('a', 'b')</code>
        → <code class="returnvalue">"a"=&gt;"b"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.5.1.1.1"></a>
<code class="function">akeys</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 的鍵擷取為陣列。
       </p>
<p>
<code class="literal">akeys('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue">{a,b}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.6.1.1.1"></a>
<code class="function">skeys</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        將 <code class="type">hstore</code> 的鍵擷取為集合。
       </p>
<p>
<code class="literal">skeys('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
a
b
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.7.1.1.1"></a>
<code class="function">avals</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 的值擷取為陣列。
       </p>
<p>
<code class="literal">avals('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue">{1,2}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.8.1.1.1"></a>
<code class="function">svals</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        將 <code class="type">hstore</code> 的值擷取為集合。
       </p>
<p>
<code class="literal">svals('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
1
2
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.9.1.1.1"></a>
<code class="function">hstore_to_array</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 的鍵和值擷取為鍵和值交錯排列的陣列。
       </p>
<p>
<code class="literal">hstore_to_array('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue">{a,1,b,2}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.10.1.1.1"></a>
<code class="function">hstore_to_matrix</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <code class="type">hstore</code> 的鍵和值擷取為二維陣列。
       </p>
<p>
<code class="literal">hstore_to_matrix('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue">{{a,1},{b,2}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.11.1.1.1"></a>
<code class="function">hstore_to_json</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">json</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為 <code class="type">json</code> 值，並將所有非 NULL 值轉換為 JSON 字串。
       </p>
<p>
        將 <code class="type">hstore</code> 值轉型為 <code class="type">json</code> 時，會隱含使用此函式。
       </p>
<p>
<code class="literal">hstore_to_json('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')</code>
        → <code class="returnvalue">{"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.12.1.1.1"></a>
<code class="function">hstore_to_jsonb</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為 <code class="type">jsonb</code> 值，並將所有非 NULL 值轉換為 JSON 字串。
       </p>
<p>
        將 <code class="type">hstore</code> 值轉型為 <code class="type">jsonb</code> 時，會隱含使用此函式。
       </p>
<p>
<code class="literal">hstore_to_jsonb('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')</code>
        → <code class="returnvalue">{"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.13.1.1.1"></a>
<code class="function">hstore_to_json_loose</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">json</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為 <code class="type">json</code> 值，但會嘗試區分數值與布林值，讓它們在 JSON 中不加引號。
       </p>
<p>
<code class="literal">hstore_to_json_loose('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')</code>
        → <code class="returnvalue">{"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.14.1.1.1"></a>
<code class="function">hstore_to_jsonb_loose</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        將 <code class="type">hstore</code> 轉換為 <code class="type">jsonb</code> 值，但會嘗試區分數值與布林值，讓它們在 JSON 中不加引號。
       </p>
<p>
<code class="literal">hstore_to_jsonb_loose('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')</code>
        → <code class="returnvalue">{"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.15.1.1.1"></a>
<code class="function">slice</code> ( <code class="type">hstore</code>, <code class="type">text[]</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        擷取只含指定鍵的 <code class="type">hstore</code> 子集。
       </p>
<p>
<code class="literal">slice('a=&gt;1,b=&gt;2,c=&gt;3'::hstore, ARRAY['b','c','x'])</code>
        → <code class="returnvalue">"b"=&gt;"2", "c"=&gt;"3"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.16.1.1.1"></a>
<code class="function">each</code> ( <code class="type">hstore</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">text</code> )
       </p>
<p>
        將 <code class="type">hstore</code> 的鍵和值擷取為一組記錄。
       </p>
<p>
<code class="literal">select * from each('a=&gt;1,b=&gt;2')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 key | value
-----+-------
 a   | 1
 b   | 2
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.17.1.1.1"></a>
<code class="function">exist</code> ( <code class="type">hstore</code>, <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">hstore</code> 是否包含該鍵？
       </p>
<p>
<code class="literal">exist('a=&gt;1', 'a')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.18.1.1.1"></a>
<code class="function">defined</code> ( <code class="type">hstore</code>, <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">hstore</code> 是否包含該鍵的非 <code class="literal">NULL</code> 值？
       </p>
<p>
<code class="literal">defined('a=&gt;NULL', 'a')</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.19.1.1.1"></a>
<code class="function">delete</code> ( <code class="type">hstore</code>, <code class="type">text</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        刪除鍵相符的配對。
       </p>
<p>
<code class="literal">delete('a=&gt;1,b=&gt;2', 'b')</code>
        → <code class="returnvalue">"a"=&gt;"1"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">delete</code> ( <code class="type">hstore</code>, <code class="type">text[]</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        刪除鍵相符的配對。
       </p>
<p>
<code class="literal">delete('a=&gt;1,b=&gt;2,c=&gt;3', ARRAY['a','b'])</code>
        → <code class="returnvalue">"c"=&gt;"3"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">delete</code> ( <code class="type">hstore</code>, <code class="type">hstore</code> )
        → <code class="returnvalue">hstore</code>
</p>
<p>
        刪除與第二個引數相符的配對。
       </p>
<p>
<code class="literal">delete('a=&gt;1,b=&gt;2', 'a=&gt;4,b=&gt;2'::hstore)</code>
        → <code class="returnvalue">"a"=&gt;"1"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.27.6.4.2.2.22.1.1.1"></a>
<code class="function">populate_record</code> ( <code class="type">anyelement</code>, <code class="type">hstore</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        以 <code class="type">hstore</code> 的相符值取代左運算元（必須是複合型別）的欄位。
       </p>
<p>
<code class="literal">populate_record(ROW(1,2), 'f1=&gt;42'::hstore)</code>
        → <code class="returnvalue">(42,2)</code>
</p></td></tr></tbody></table>

<br>

除了這些運算子與函式之外，`hstore` 型別的值也可使用下標，讓它們可作為關聯陣列使用。只能指定一個 `text` 型別的下標；它會被解讀為鍵，並擷取或儲存對應的值。例如：

```

CREATE TABLE mytable (h hstore);
INSERT INTO mytable VALUES ('a=>b, c=>d');
SELECT h['a'] FROM mytable;
 h
---
 b
(1 row)

UPDATE mytable SET h['c'] = 'new';
SELECT h FROM mytable;
          h
----------------------
 "a"=>"b", "c"=>"new"
(1 row)
```

若下標為 `NULL`，或該鍵不存在於 `hstore` 中，使用下標的擷取會傳回 `NULL`。（因此，使用下標的擷取與 `->` 運算子並沒有很大差異。）若下標為 `NULL`，使用下標的更新會失敗；否則會取代該鍵的值，若鍵尚不存在，則會在 `hstore` 中新增項目。

[返回 F.17. hstore — hstore 鍵／值資料型別](../hstore.md#hstore)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/hstore.html)
