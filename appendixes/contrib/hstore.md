## F.17. hstore — hstore 鍵／值資料型別 [#](#HSTORE)

[F.17.1. `hstore` 外部表示法](hstore.md#HSTORE-EXTERNAL-REP)

[F.17.2. `hstore` 運算子與函式](hstore.md#HSTORE-OPS-FUNCS)

[F.17.3. 索引](hstore.md#HSTORE-INDEXES)

[F.17.4. 範例](hstore.md#HSTORE-EXAMPLES)

[F.17.5. 統計資訊](hstore.md#HSTORE-STATISTICS)

[F.17.6. 相容性](hstore.md#HSTORE-COMPATIBILITY)

[F.17.7. 轉換](hstore.md#HSTORE-TRANSFORMS)

[F.17.8. 作者](hstore.md#HSTORE-AUTHORS)

<a id="id-1.11.7.27.2"></a>

此模組實作 `hstore` 資料型別，用於在單一 PostgreSQL 值中儲存一組鍵／值配對。它適用於多種情境，例如含有許多但很少查閱之屬性的資料列，或半結構化資料。鍵和值都只是文字字串。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="HSTORE-EXTERNAL-REP"></a>

### F.17.1. `hstore` 外部表示法 [#](#HSTORE-EXTERNAL-REP)

`hstore` 用於輸入與輸出的文字表示法，包含零個或多個以逗號分隔的 *`key`* `=>` *`value`* 配對。範例：

```

k => v
foo => bar, baz => whatever
"1-a" => "anything at all"
```

配對順序並不重要（輸出時也可能不會重現）。配對之間或 `=>` 符號周圍的空白會被忽略。包含空白、逗號、`=` 或 `>` 的鍵和值必須以雙引號括住。若鍵或值中要包含雙引號或反斜線，請以反斜線逸出。

`hstore` 中的每個鍵都是唯一的。若宣告含有重複鍵的 `hstore`，只會有一個儲存在 `hstore` 中，且不保證會保留哪一個：

```

SELECT 'a=>1,a=>2'::hstore;
  hstore
----------
 "a"=>"1"
```

值（但鍵不可）可以是 SQL `NULL`。例如：

```

key => NULL
```

`NULL` 關鍵字不區分大小寫。以雙引號括住 `NULL`，即可將其視為一般字串「NULL」。

### 注意

請記得，作為輸入使用時，`hstore` 文字格式會在任何必要的引號或逸出處理*之前*套用。若透過參數傳遞 `hstore` 字面值，則不需要額外處理。但若將它作為帶引號的字面常數傳遞，則任何單引號字元及（依 `standard_conforming_strings` 組態參數的設定而定）反斜線字元，都必須正確逸出。關於字串常數的處理，請參閱[第 4.1.2.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)。

輸出時，鍵和值一律會以雙引號括住，即使嚴格而言並非必要。

<a id="HSTORE-OPS-FUNCS"></a>

### F.17.2. `hstore` 運算子與函式 [#](#HSTORE-OPS-FUNCS)

`hstore` 模組提供的運算子列於[表 F.6](hstore.md#HSTORE-OP-TABLE)，函式列於[表 F.7](hstore.md#HSTORE-FUNC-TABLE)。

<a id="HSTORE-OP-TABLE"></a>

**表 F.6. `hstore` 運算子**

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

**表 F.7. `hstore` 函式**

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

<a id="HSTORE-INDEXES"></a>

### F.17.3. 索引 [#](#HSTORE-INDEXES)

`hstore` 對 `@>`、`?`、`?&` 與 `?|` 運算子支援 GiST 與 GIN 索引。例如：

```

CREATE INDEX hidx ON testhstore USING GIST (h);

CREATE INDEX hidx ON testhstore USING GIN (h);
```

`gist_hstore_ops` GiST 運算子類別會將一組鍵／值配對近似為點陣圖簽章。其可選整數參數 `siglen` 決定簽章長度（以位元組計）。預設長度為 16 位元組。有效的簽章長度介於 1 至 2024 位元組之間。較長的簽章可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

以下範例建立簽章長度為 32 位元組的此類索引：

```

CREATE INDEX hidx ON testhstore USING GIST (h gist_hstore_ops(siglen=32));
```

`hstore` 也支援 `=` 運算子的 `btree` 或 `hash` 索引。這讓 `hstore` 欄位可宣告為 `UNIQUE`，或用於 `GROUP BY`、`ORDER BY` 或 `DISTINCT` 表達式。`hstore` 值的排序順序不特別實用，但這些索引可能適合等值查找。請如下為 `=` 比較建立索引：

```

CREATE INDEX hidx ON testhstore USING BTREE (h);

CREATE INDEX hidx ON testhstore USING HASH (h);
```

<a id="HSTORE-EXAMPLES"></a>

### F.17.4. 範例 [#](#HSTORE-EXAMPLES)

新增一個鍵，或以新值更新現有鍵：

```

UPDATE tab SET h['c'] = '3';
```

另一種執行相同工作的方式是：

```

UPDATE tab SET h = h || hstore('c', '3');
```

若要在一次操作中新增或變更多個鍵，串接方式比使用下標更有效率：

```

UPDATE tab SET h = h || hstore(array['q', 'w'], array['11', '12']);
```

刪除一個鍵：

```

UPDATE tab SET h = delete(h, 'k1');
```

將 `record` 轉換為 `hstore`：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT hstore(t) FROM test AS t;
                   hstore
---------------------------------------------
 "col1"=>"123", "col2"=>"foo", "col3"=>"bar"
(1 row)
```

將 `hstore` 轉換為預先定義的 `record` 型別：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);

SELECT * FROM populate_record(null::test,
                              '"col1"=>"456", "col2"=>"zzz"');
 col1 | col2 | col3
------+------+------
  456 | zzz  |
(1 row)
```

使用 `hstore` 中的值修改現有記錄：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT (r).* FROM (SELECT t #= '"col3"=>"baz"' AS r FROM test t) s;
 col1 | col2 | col3
------+------+------
  123 | foo  | baz
(1 row)
```

<a id="HSTORE-STATISTICS"></a>

### F.17.5. 統計資訊 [#](#HSTORE-STATISTICS)

`hstore` 型別天生具有彈性，因此可能含有許多不同的鍵。檢查鍵是否有效是應用程式的責任。以下範例示範數種檢查鍵與取得統計資訊的技術。

簡單範例：

```

SELECT * FROM each('aaa=>bq, b=>NULL, ""=>1');
```

使用資料表：

```

CREATE TABLE stat AS SELECT (each(h)).key, (each(h)).value FROM testhstore;
```

即時統計資訊：

```

SELECT key, count(*) FROM
  (SELECT (each(h)).key FROM testhstore) AS stat
  GROUP BY key
  ORDER BY count DESC, key;
    key    | count
-----------+-------
 line      |   883
 query     |   207
 pos       |   203
 node      |   202
 space     |   197
 status    |   195
 public    |   194
 title     |   190
 org       |   189
...................
```

<a id="HSTORE-COMPATIBILITY"></a>

### F.17.6. 相容性 [#](#HSTORE-COMPATIBILITY)

自 PostgreSQL 9.0 起，`hstore` 使用與舊版不同的內部表示法。這不會造成傾印／還原升級的阻礙，因為文字表示法（用於傾印）未變更。

進行二進位升級時，新程式碼會辨識舊格式資料以維持向上相容性。處理尚未由新程式碼修改的資料時，這會產生些微效能損失。可如下執行 `UPDATE` 陳述式，強制升級資料表欄位中的所有值：

```

UPDATE tablename SET hstorecol = hstorecol || '';
```

另一種方式是：

```

ALTER TABLE tablename ALTER hstorecol TYPE hstore USING hstorecol || '';
```

`ALTER TABLE` 方法需要在資料表上取得 `ACCESS EXCLUSIVE` 鎖定，但不會因舊資料列版本而使資料表膨脹。

<a id="HSTORE-TRANSFORMS"></a>

### F.17.7. 轉換 [#](#HSTORE-TRANSFORMS)

另有可用擴充功能，為 PL/Perl 與 PL/Python 語言實作 `hstore` 型別的轉換。PL/Perl 的擴充功能分別名為 `hstore_plperl` 與 `hstore_plperlu`，對應受信任與不受信任的 PL/Perl。若安裝這些轉換並在建立函式時指定它們，`hstore` 值會對應到 Perl 雜湊。PL/Python 的擴充功能名為 `hstore_plpython3u`；若使用它，`hstore` 值會對應到 Python 字典。

<a id="HSTORE-AUTHORS"></a>

### F.17.8. 作者 [#](#HSTORE-AUTHORS)

Oleg Bartunov `<oleg@sai.msu.su>`, Moscow, Moscow University, Russia

Teodor Sigaev `<teodor@sigaev.ru>`, Moscow, Delta-Soft Ltd., Russia

Andrew Gierth `<andrew@tao11.riddles.org.uk>`（英國）的額外改進

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/hstore.html)
