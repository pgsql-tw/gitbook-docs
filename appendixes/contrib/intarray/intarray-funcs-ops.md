# F.19.1. intarray 函式與運算子

<a id="INTARRAY-FUNCS-OPS"></a>

## F.19.1. `intarray` 函式與運算子 [#](#intarray-funcs-ops) <a href="#intarray-funcs-ops" id="intarray-funcs-ops"></a>

`intarray` 模組提供的函式列於[表 F.8](#intarray-func-table)，運算子列於[表 F.9](#intarray-op-table)。

<a id="INTARRAY-FUNC-TABLE"></a>

### 表 F.8. `intarray` 函式 [#](#intarray-func-table) <a href="#intarray-func-table" id="intarray-func-table"></a>

<table border="1" class="table" summary="intarray Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.1.1.1.1"></a>
<code class="function">icount</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回陣列中的元素數量。
       </p>
<p>
<code class="literal">icount('{1,2,3}'::integer[])</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.2.1.1.1"></a>
<code class="function">sort</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>dir</code></em> <code class="type">text</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞增或遞減順序排序陣列。<em class="parameter"><code>dir</code></em> 必須是 <code class="literal">asc</code> 或 <code class="literal">desc</code>。
       </p>
<p>
<code class="literal">sort('{1,3,2}'::integer[], 'desc')</code>
        → <code class="returnvalue">{3,2,1}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sort</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.3.1.2.1"></a>
<code class="function">sort_asc</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞增順序排序。
       </p>
<p>
<code class="literal">sort(array[11,77,44])</code>
        → <code class="returnvalue">{11,44,77}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.4.1.1.1"></a>
<code class="function">sort_desc</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞減順序排序。
       </p>
<p>
<code class="literal">sort_desc(array[11,77,44])</code>
        → <code class="returnvalue">{77,44,11}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.5.1.1.1"></a>
<code class="function">uniq</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        移除相鄰的重複項目。常與 <code class="function">sort</code> 搭配使用，以移除所有重複項目。
       </p>
<p>
<code class="literal">uniq('{1,2,2,3,1,1}'::integer[])</code>
        → <code class="returnvalue">{1,2,3,1}</code>
</p>
<p>
<code class="literal">uniq(sort('{1,2,3,2,1}'::integer[]))</code>
        → <code class="returnvalue">{1,2,3}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.6.1.1.1"></a>
<code class="function">idx</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>item</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回第一個符合 <em class="parameter"><code>item</code></em> 的陣列元素索引；若沒有符合項目則傳回 0。
       </p>
<p>
<code class="literal">idx(array[11,22,33,22,11], 22)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.7.1.1.1"></a>
<code class="function">subarray</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code>, <em class="parameter"><code>len</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        擷取從位置 <em class="parameter"><code>start</code></em> 開始、含有 <em class="parameter"><code>len</code></em> 個元素的陣列部分。
       </p>
<p>
<code class="literal">subarray('{1,2,3,2,1}'::integer[], 2, 3)</code>
        → <code class="returnvalue">{2,3,2}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">subarray</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        擷取從位置 <em class="parameter"><code>start</code></em> 開始的陣列部分。
       </p>
<p>
<code class="literal">subarray('{1,2,3,2,1}'::integer[], 2)</code>
        → <code class="returnvalue">{2,3,2,1}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.9.1.1.1"></a>
<code class="function">intset</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        建立單一元素陣列。
       </p>
<p>
<code class="literal">intset(42)</code>
        → <code class="returnvalue">{42}</code>
</p></td></tr></tbody></table>

<br><a id="INTARRAY-OP-TABLE"></a>

### 表 F.9. `intarray` 運算子 [#](#intarray-op-table) <a href="#intarray-op-table" id="intarray-op-table"></a>

<table border="1" class="table" summary="intarray Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&amp;&amp;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否重疊（至少有一個共同元素）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">@&gt;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側陣列是否包含右側陣列？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&lt;@</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側陣列是否包含於右側陣列？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type"></code> <code class="literal">#</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回陣列中的元素數量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">#</code> <code class="type">integer</code>
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回第一個符合右側引數的陣列元素索引；若沒有符合項目則傳回 0。（與 <code class="function">idx</code> 函式相同。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">+</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        將元素新增至陣列末端。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">+</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        串接陣列。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">-</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        從陣列移除符合右側引數的項目。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">-</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        從左側陣列移除右側陣列的元素。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">|</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的聯集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">|</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的聯集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&amp;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的交集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">@@</code> <code class="type">query_int</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否滿足查詢？（見下文）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">query_int</code> <code class="literal">~~</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否滿足查詢？（<code class="literal">@@</code> 的交換子）
       </p></td></tr></tbody></table>

<br>

`&&`、`@>` 與 `<@` 運算子等同於 PostgreSQL 同名內建運算子，但它們僅可處理不含 NULL 的整數陣列，而內建運算子可處理任何陣列型別。這項限制使它們在許多情況下比內建運算子更快。

`@@` 與 `~~` 運算子測試陣列是否滿足*查詢*；查詢以專用資料型別 `query_int` 的值表示。*查詢*由要與陣列元素比對的整數值組成，可能使用 `&`（AND）、`|`（OR）與 `!`（NOT）運算子組合。可視需要使用括號。例如，查詢 `1&(2|3)` 符合包含 1 且包含 2 或 3 其中之一的陣列。

[返回 F.19. intarray — 操作整數陣列](../intarray.md#intarray)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intarray.html)
