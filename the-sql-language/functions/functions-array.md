<a id="FUNCTIONS-ARRAY"></a>

## 9.19. 陣列函式與運算子 [#](#FUNCTIONS-ARRAY)

[表 9.56](functions-array.md#ARRAY-OPERATORS-TABLE) 列出了可用於陣列型別的特殊運算子。除此之外，陣列也可以使用[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子。比較運算子會使用元素資料型別的預設 B-tree 比較函式逐一比較陣列的內容，並依據第一個差異進行排序。在多維陣列中，元素是依列主序（row-major order）走訪的（最後一個下標變化最快）。如果兩個陣列的內容相等但維度不同，則由維度資訊中的第一個差異決定排序順序。

<a id="ARRAY-OPERATORS-TABLE"></a>

**表 9.56. 陣列運算子**

<table border="1" class="table" summary="Array Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyarray</code> <code class="literal">@&gt;</code> <code class="type">anyarray</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個陣列是否包含第二個陣列，也就是說，第二個陣列中出現的每個元素，是否都等於第一個陣列中的某個元素？（重複的元素不會特別處理，因此 <code class="literal">ARRAY[1]</code> 與 <code class="literal">ARRAY[1,1]</code> 會被視為互相包含。）
       </p>
<p>
<code class="literal">ARRAY[1,4,3] @&gt; ARRAY[3,1,3]</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyarray</code> <code class="literal">&lt;@</code> <code class="type">anyarray</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個陣列是否被第二個陣列包含？
       </p>
<p>
<code class="literal">ARRAY[2,2,7] &lt;@ ARRAY[1,7,4,2,6]</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyarray</code> <code class="literal">&amp;&amp;</code> <code class="type">anyarray</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個陣列是否重疊，也就是有任何共同的元素？
       </p>
<p>
<code class="literal">ARRAY[1,4,3] &amp;&amp; ARRAY[2,1]</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anycompatiblearray</code> <code class="literal">||</code> <code class="type">anycompatiblearray</code>
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        串接兩個陣列。串接 null 或空陣列不會有任何作用；否則這兩個陣列必須有相同的維數（如第一個範例所示），或維數相差一（如第二個範例所示）。如果兩個陣列的元素型別不同，它們會被強制轉換為共同的型別（請參閱<a class="xref" href="../typeconv/typeconv-union-case.md">第 10.5 節</a>）。
       </p>
<p>
<code class="literal">ARRAY[1,2,3] || ARRAY[4,5,6,7]</code>
        → <code class="returnvalue">{1,2,3,4,5,6,7}</code>
</p>
<p>
<code class="literal">ARRAY[1,2,3] || ARRAY[[4,5,6],[7,8,9.9]]</code>
        → <code class="returnvalue">{{1,2,3},{4,5,6},{7,8,9.9}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anycompatible</code> <code class="literal">||</code> <code class="type">anycompatiblearray</code>
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        將一個元素串接到陣列（必須是空的或一維的）的前端。
       </p>
<p>
<code class="literal">3 || ARRAY[4,5,6]</code>
        → <code class="returnvalue">{3,4,5,6}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anycompatiblearray</code> <code class="literal">||</code> <code class="type">anycompatible</code>
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        將一個元素串接到陣列（必須是空的或一維的）的尾端。
       </p>
<p>
<code class="literal">ARRAY[4,5,6] || 7</code>
        → <code class="returnvalue">{4,5,6,7}</code>
</p></td></tr></tbody></table>

<br>

關於陣列運算子行為的更多細節，請參閱[第 8.15 節](../datatype/arrays.md)。關於哪些運算子支援索引操作的更多細節，請參閱[第 11.2 節](../indexes/indexes-types.md)。

[表 9.57](functions-array.md#ARRAY-FUNCTIONS-TABLE) 列出了可用於陣列型別的函式。關於這些函式的更多資訊與使用範例，請參閱[第 8.15 節](../datatype/arrays.md)。

<a id="ARRAY-FUNCTIONS-TABLE"></a>

**表 9.57. 陣列函式**

<table border="1" class="table" summary="Array Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.1.1.1.1"></a>
<code class="function">array_append</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatible</code> )
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        將一個元素附加到陣列的尾端（與 <code class="type">anycompatiblearray</code> <code class="literal">||</code> <code class="type">anycompatible</code> 運算子相同）。
       </p>
<p>
<code class="literal">array_append(ARRAY[1,2], 3)</code>
        → <code class="returnvalue">{1,2,3}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.2.1.1.1"></a>
<code class="function">array_cat</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatiblearray</code> )
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        串接兩個陣列（與 <code class="type">anycompatiblearray</code> <code class="literal">||</code> <code class="type">anycompatiblearray</code> 運算子相同）。
       </p>
<p>
<code class="literal">array_cat(ARRAY[1,2,3], ARRAY[4,5])</code>
        → <code class="returnvalue">{1,2,3,4,5}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.3.1.1.1"></a>
<code class="function">array_dims</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳陣列維度的文字表示。
       </p>
<p>
<code class="literal">array_dims(ARRAY[[1,2,3], [4,5,6]])</code>
        → <code class="returnvalue">[1:2][1:3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.4.1.1.1"></a>
<code class="function">array_fill</code> ( <code class="type">anyelement</code>, <code class="type">integer[]</code>
          [<span class="optional">, <code class="type">integer[]</code> </span>] )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        回傳一個以給定值的副本填滿的陣列，其各維度的長度由第二個引數指定。選用的第三個引數提供每個維度的下界值（預設全部為 <code class="literal">1</code>）。
       </p>
<p>
<code class="literal">array_fill(11, ARRAY[2,3])</code>
        → <code class="returnvalue">{{11,11,11},{11,11,11}}</code>
</p>
<p>
<code class="literal">array_fill(7, ARRAY[3], ARRAY[2])</code>
        → <code class="returnvalue">[2:4]={7,7,7}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.5.1.1.1"></a>
<code class="function">array_length</code> ( <code class="type">anyarray</code>, <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳所要求之陣列維度的長度。（對於空的或不存在的陣列維度，會產生 NULL 而不是 0。）
       </p>
<p>
<code class="literal">array_length(array[1,2,3], 1)</code>
        → <code class="returnvalue">3</code>
</p>
<p>
<code class="literal">array_length(array[]::int[], 1)</code>
        → <code class="returnvalue">NULL</code>
</p>
<p>
<code class="literal">array_length(array['text'], 2)</code>
        → <code class="returnvalue">NULL</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.6.1.1.1"></a>
<code class="function">array_lower</code> ( <code class="type">anyarray</code>, <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳所要求之陣列維度的下界。
       </p>
<p>
<code class="literal">array_lower('[0:2]={1,2,3}'::integer[], 1)</code>
        → <code class="returnvalue">0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.7.1.1.1"></a>
<code class="function">array_ndims</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳陣列的維數。
       </p>
<p>
<code class="literal">array_ndims(ARRAY[[1,2,3], [4,5,6]])</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.8.1.1.1"></a>
<code class="function">array_position</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatible</code> [<span class="optional">, <code class="type">integer</code> </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳第二個引數在陣列中第一次出現的下標；如果不存在則回傳 <code class="literal">NULL</code>。如果給定了第三個引數，就從該下標開始搜尋。陣列必須是一維的。比較是以 <code class="literal">IS NOT DISTINCT FROM</code> 的語意進行的，因此可以搜尋 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">array_position(ARRAY['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'], 'mon')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.9.1.1.1"></a>
<code class="function">array_positions</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatible</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        回傳第二個引數在作為第一個引數之陣列中所有出現位置的下標陣列。陣列必須是一維的。比較是以 <code class="literal">IS NOT DISTINCT FROM</code> 的語意進行的，因此可以搜尋 <code class="literal">NULL</code>。只有在陣列為 <code class="literal">NULL</code> 時才會回傳 <code class="literal">NULL</code>；如果在陣列中找不到該值，就回傳空陣列。
       </p>
<p>
<code class="literal">array_positions(ARRAY['A','A','B','A'], 'A')</code>
        → <code class="returnvalue">{1,2,4}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.10.1.1.1"></a>
<code class="function">array_prepend</code> ( <code class="type">anycompatible</code>, <code class="type">anycompatiblearray</code> )
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        將一個元素加到陣列的開頭（與 <code class="type">anycompatible</code> <code class="literal">||</code> <code class="type">anycompatiblearray</code> 運算子相同）。
       </p>
<p>
<code class="literal">array_prepend(1, ARRAY[2,3])</code>
        → <code class="returnvalue">{1,2,3}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.11.1.1.1"></a>
<code class="function">array_remove</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatible</code> )
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        從陣列中移除所有等於給定值的元素。陣列必須是一維的。比較是以 <code class="literal">IS NOT DISTINCT FROM</code> 的語意進行的，因此可以移除 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">array_remove(ARRAY[1,2,3,2], 2)</code>
        → <code class="returnvalue">{1,3}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.12.1.1.1"></a>
<code class="function">array_replace</code> ( <code class="type">anycompatiblearray</code>, <code class="type">anycompatible</code>, <code class="type">anycompatible</code> )
        → <code class="returnvalue">anycompatiblearray</code>
</p>
<p>
        將陣列中每個等於第二個引數的元素，替換為第三個引數。
       </p>
<p>
<code class="literal">array_replace(ARRAY[1,2,5,4], 5, 3)</code>
        → <code class="returnvalue">{1,2,3,4}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.13.1.1.1"></a>
<code class="function">array_reverse</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        反轉陣列的第一個維度。
       </p>
<p>
<code class="literal">array_reverse(ARRAY[[1,2],[3,4],[5,6]])</code>
        → <code class="returnvalue">{{5,6},{3,4},{1,2}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.14.1.1.1"></a>
<code class="function">array_sample</code> ( <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>, <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        回傳由 <em class="parameter"><code>n</code></em> 個項目組成的陣列，這些項目是從 <em class="parameter"><code>array</code></em> 中隨機選出的。<em class="parameter"><code>n</code></em> 不得超過 <em class="parameter"><code>array</code></em> 第一個維度的長度。如果 <em class="parameter"><code>array</code></em> 是多維的，一個<span class="quote">“<span class="quote">項目</span>”</span>就是具有給定第一個下標的切片。
       </p>
<p>
<code class="literal">array_sample(ARRAY[1,2,3,4,5,6], 3)</code>
        → <code class="returnvalue">{2,6,1}</code>
</p>
<p>
<code class="literal">array_sample(ARRAY[[1,2],[3,4],[5,6]], 2)</code>
        → <code class="returnvalue">{{5,6},{1,2}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.15.1.1.1"></a>
<code class="function">array_shuffle</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        隨機打亂陣列的第一個維度。
       </p>
<p>
<code class="literal">array_shuffle(ARRAY[[1,2],[3,4],[5,6]])</code>
        → <code class="returnvalue">{{5,6},{1,2},{3,4}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.16.1.1.1"></a>
<code class="function">array_sort</code> (
          <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>
          [<span class="optional">, <em class="parameter"><code>descending</code></em> <code class="type">boolean</code>
          [<span class="optional">, <em class="parameter"><code>nulls_first</code></em> <code class="type">boolean</code>
</span>]</span>] )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        對陣列的第一個維度進行排序。排序順序由陣列元素型別的預設排序方式決定；不過，如果元素型別是可定序的，可以將 <code class="literal">COLLATE</code> 子句加在 <em class="parameter"><code>array</code></em> 引數後面，以指定要使用的定序。
       </p>
<p>
        如果 <em class="parameter"><code>descending</code></em> 為 true，就以遞減順序排序，否則以遞增順序排序。如果省略，預設為遞增順序。如果 <em class="parameter"><code>nulls_first</code></em> 為 true，null 會出現在非 null 值之前，否則 null 會出現在非 null 值之後。如果省略，<em class="parameter"><code>nulls_first</code></em> 會被視為與 <em class="parameter"><code>descending</code></em> 的值相同。
       </p>
<p>
<code class="literal">array_sort(ARRAY[[2,4],[2,1],[6,5]])</code>
        → <code class="returnvalue">{{2,1},{2,4},{6,5}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-ARRAY-TO-STRING"></a>
<code class="function">array_to_string</code> ( <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>, <em class="parameter"><code>delimiter</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>null_string</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將每個陣列元素轉換為其文字表示，並以 <em class="parameter"><code>delimiter</code></em> 字串分隔串接起來。如果給定了 <em class="parameter"><code>null_string</code></em> 且其值不是 <code class="literal">NULL</code>，<code class="literal">NULL</code> 陣列項目就以該字串表示；否則會被省略。另請參閱 <a class="link" href="functions-string.md#FUNCTION-STRING-TO-ARRAY"><code class="function">string_to_array</code></a>。
       </p>
<p>
<code class="literal">array_to_string(ARRAY[1, 2, 3, NULL, 5], ',', '*')</code>
        → <code class="returnvalue">1,2,3,*,5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.18.1.1.1"></a>
<code class="function">array_upper</code> ( <code class="type">anyarray</code>, <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳所要求之陣列維度的上界。
       </p>
<p>
<code class="literal">array_upper(ARRAY[1,8,3,7], 1)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.19.1.1.1"></a>
<code class="function">cardinality</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳陣列中的元素總數；如果陣列是空的，則回傳 0。
       </p>
<p>
<code class="literal">cardinality(ARRAY[[1,2],[3,4]])</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.20.1.1.1"></a>
<code class="function">trim_array</code> ( <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>, <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        藉由移除最後 <em class="parameter"><code>n</code></em> 個元素來修剪陣列。如果陣列是多維的，只會修剪第一個維度。
       </p>
<p>
<code class="literal">trim_array(ARRAY[1,2,3,4,5,6], 2)</code>
        → <code class="returnvalue">{1,2,3,4}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.25.6.2.2.21.1.1.1"></a>
<code class="function">unnest</code> ( <code class="type">anyarray</code> )
        → <code class="returnvalue">setof anyelement</code>
</p>
<p>
        將陣列展開成一組資料列。陣列的元素會依照儲存順序讀出。
       </p>
<p>
<code class="literal">unnest(ARRAY[1,2])</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 1
 2
</pre><p>
</p>
<p>
<code class="literal">unnest(ARRAY[['foo','bar'],['baz','quux']])</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 foo
 bar
 baz
 quux
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">unnest</code> ( <code class="type">anyarray</code>, <code class="type">anyarray</code> [<span class="optional">, ... </span>] )
        → <code class="returnvalue">setof anyelement, anyelement [, ... ]</code>
</p>
<p>
        將多個陣列（可能是不同的資料型別）展開成一組資料列。如果這些陣列的長度不全相同，較短的陣列會以 <code class="literal">NULL</code> 填補。這種形式只允許出現在查詢的 FROM 子句中；請參閱<a class="xref" href="../queries/queries-table-expressions.md#QUERIES-TABLEFUNCTIONS">第 7.2.1.4 節</a>。
       </p>
<p>
<code class="literal">select * from unnest(ARRAY[1,2], ARRAY['foo','bar','baz']) as x(a,b)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |  b
---+-----
 1 | foo
 2 | bar
   | baz
</pre><p>
</p></td></tr></tbody></table>

<br>

另請參閱[第 9.21 節](functions-aggregate.md)中關於可搭配陣列使用之彙總函式 `array_agg` 的說明。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-array.html)（原文版本：18.6；核對日期：2026-09-11）
