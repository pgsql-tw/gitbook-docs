# F.39.4. 用法

<a id="SEG-USAGE"></a>

## F.39.4. 用法 [#](#seg-usage) <a href="#seg-usage" id="seg-usage"></a>

`seg` 模組包含一個用於
`seg` 值的 GiST 索引運算子類別。
該 GiST 運算子類別支援的運算子列於[表 F.31](#seg-gist-operators)。

<a id="SEG-GIST-OPERATORS"></a>

### 表 F.31. Seg GiST 運算子 [#](#seg-gist-operators) <a href="#seg-gist-operators" id="seg-gist-operators"></a>

<table border="1" class="table" summary="Seg GiST 運算子"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&lt;&lt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否完全位於第二個的左側？
        若 b &lt; c，則 [a, b] &lt;&lt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&gt;&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否完全位於第二個的右側？
        若 a &gt; d，則 [a, b] &gt;&gt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&lt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否沒有延伸到第二個的右側？
        若 b &lt;= d，則 [a, b] &amp;&lt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否沒有延伸到第二個的左側？
        若 a &gt;= c，則 [a, b] &amp;&gt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">=</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個 <code class="type">seg</code> 是否相等？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&amp;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個 <code class="type">seg</code> 是否重疊？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">@&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否包含第二個？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&lt;@</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否包含於第二個？
       </p></td></tr></tbody></table>

<br>

除了上述運算子之外，[表 9.1](../../../the-sql-language/functions/functions-comparison.md#functions-comparison-table) 所列的一般比較運算子也可用於型別
`seg`。這些運算子會先比較 (a) 與 (c)，若兩者相等，再比較 (b) 與 (d)。在大多數情況下，這會產生相當合理的排序，若你想對此型別使用
ORDER BY，這會很有用。

[返回 F.39. seg — 線段或浮點數區間的資料型別](../seg.md#seg)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/seg.html)（原文版本：18.6；核對日期：2026-10-22）
