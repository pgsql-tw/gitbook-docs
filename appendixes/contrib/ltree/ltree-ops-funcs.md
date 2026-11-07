# F.22.2. 運算子與函式

<a id="LTREE-OPS-FUNCS"></a>

## F.22.2. 運算子與函式 [#](#ltree-ops-funcs) <a href="#ltree-ops-funcs" id="ltree-ops-funcs"></a>

型別 `ltree` 具有一般比較運算子 `=`、`<>`、`<`、`>`、`<=`、`>=`。比較會依樹狀走訪順序排序，節點子項目則依標籤文字排序。此外，還提供[表 F.12](#ltree-op-table) 所示的專用運算子。

<a id="LTREE-OP-TABLE"></a>

### 表 F.12. `ltree` 運算子 [#](#ltree-op-table) <a href="#ltree-op-table" id="ltree-op-table"></a>

<table border="1" class="table" summary="ltree Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側引數是否為右側引數的祖先（或相等）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側引數是否為右側引數的子孫（或相等）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">~</code> <code class="type">lquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery</code> <code class="literal">~</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合 <code class="type">lquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">?</code> <code class="type">lquery[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery[]</code> <code class="literal">?</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合陣列中的任何 <code class="type">lquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltxtquery</code> <code class="literal">@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合 <code class="type">ltxtquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">||</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        串接 <code class="type">ltree</code> 路徑。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">||</code> <code class="type">text</code>
        → <code class="returnvalue">ltree</code>
</p>
<p class="func_signature">
<code class="type">text</code> <code class="literal">||</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        將文字轉換為 <code class="type">ltree</code> 並串接。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltree</code> <code class="literal">&lt;@</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含 <code class="type">ltree</code> 的祖先？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltree</code> <code class="literal">@&gt;</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含 <code class="type">ltree</code> 的子孫？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">~</code> <code class="type">lquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery</code> <code class="literal">~</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含符合 <code class="type">lquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?</code> <code class="type">lquery[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery[]</code> <code class="literal">?</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 陣列是否包含符合任何 <code class="type">lquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltxtquery</code> <code class="literal">@</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含符合 <code class="type">ltxtquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個為 <code class="type">ltree</code> 祖先的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個為 <code class="type">ltree</code> 子孫的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?~</code> <code class="type">lquery</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個符合 <code class="type">lquery</code> 的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個符合 <code class="type">ltxtquery</code> 的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr></tbody></table>

<br>

`<@`、`@>`、`@` 與 `~` 運算子有對應的 `^<@`、`^@>`、`^@`、`^~`；它們相同，但不使用索引。這些只適合測試用途。

可用函式列於[表 F.13](#ltree-func-table)。

<a id="LTREE-FUNC-TABLE"></a>

### 表 F.13. `ltree` 函式 [#](#ltree-func-table) <a href="#ltree-func-table" id="ltree-func-table"></a>

<table border="1" class="table" summary="ltree Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.1.1.1.1"></a>
<code class="function">subltree</code> ( <code class="type">ltree</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code>, <em class="parameter"><code>end</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回 <code class="type">ltree</code> 從位置 <em class="parameter"><code>start</code></em> 到位置 <em class="parameter"><code>end</code></em>-1 的子路徑（從 0 起算）。
       </p>
<p>
<code class="literal">subltree('Top.Child1.Child2', 1, 2)</code>
        → <code class="returnvalue">Child1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.2.1.1.1"></a>
<code class="function">subpath</code> ( <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code>, <em class="parameter"><code>len</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回從位置 <em class="parameter"><code>offset</code></em> 開始、長度為 <em class="parameter"><code>len</code></em> 的 <code class="type">ltree</code> 子路徑。若 <em class="parameter"><code>offset</code></em> 為負數，子路徑從距路徑結尾該數量的位置開始。若 <em class="parameter"><code>len</code></em> 為負數，會從路徑結尾移除該數量的標籤。
       </p>
<p>
<code class="literal">subpath('Top.Child1.Child2', 0, 2)</code>
        → <code class="returnvalue">Top.Child1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">subpath</code> ( <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回從位置 <em class="parameter"><code>offset</code></em> 開始並延伸至路徑結尾的 <code class="type">ltree</code> 子路徑。若 <em class="parameter"><code>offset</code></em> 為負數，子路徑從距路徑結尾該數量的位置開始。
       </p>
<p>
<code class="literal">subpath('Top.Child1.Child2', 1)</code>
        → <code class="returnvalue">Child1.Child2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.4.1.1.1"></a>
<code class="function">nlevel</code> ( <code class="type">ltree</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回路徑中的標籤數量。
       </p>
<p>
<code class="literal">nlevel('Top.Child1.Child2')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.5.1.1.1"></a>
<code class="function">index</code> ( <em class="parameter"><code>a</code></em> <code class="type">ltree</code>, <em class="parameter"><code>b</code></em> <code class="type">ltree</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回 <em class="parameter"><code>b</code></em> 在 <em class="parameter"><code>a</code></em> 中第一次出現的位置；若找不到則傳回 -1。
       </p>
<p>
<code class="literal">index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6')</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">index</code> ( <em class="parameter"><code>a</code></em> <code class="type">ltree</code>,  <em class="parameter"><code>b</code></em> <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回 <em class="parameter"><code>b</code></em> 在 <em class="parameter"><code>a</code></em> 中第一次出現的位置；若找不到則傳回 -1。搜尋從位置 <em class="parameter"><code>offset</code></em> 開始；若 <em class="parameter"><code>offset</code></em> 為負數，則從距離路徑結尾 <em class="parameter"><code>-offset</code></em> 個標籤的位置開始。
       </p>
<p>
<code class="literal">index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6', -4)</code>
        → <code class="returnvalue">9</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.7.1.1.1"></a>
<code class="function">text2ltree</code> ( <code class="type">text</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        將 <code class="type">text</code> 轉型為 <code class="type">ltree</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.8.1.1.1"></a>
<code class="function">ltree2text</code> ( <code class="type">ltree</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <code class="type">ltree</code> 轉型為 <code class="type">text</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.9.1.1.1"></a>
<code class="function">lca</code> ( <code class="type">ltree</code> [<span class="optional">, <code class="type">ltree</code> [<span class="optional">, ... </span>]</span>] )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        計算各路徑最長的共同祖先路徑（最多支援 8 個引數）。
       </p>
<p>
<code class="literal">lca('1.2.3', '1.2.3.4.5.6')</code>
        → <code class="returnvalue">1.2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">lca</code> ( <code class="type">ltree[]</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        計算陣列中各路徑最長的共同祖先路徑。
       </p>
<p>
<code class="literal">lca(array['1.2.3'::ltree,'1.2.3.4'])</code>
        → <code class="returnvalue">1.2</code>
</p></td></tr></tbody></table>

<br>

[返回 F.22. ltree — 階層式樹狀資料型別](../ltree.md#ltree)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ltree.html)（核對日期：2026-09-11）
