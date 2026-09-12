<a id="FUNCTIONS-RANGE"></a>

## 9.20. 範圍／多重範圍函式與運算子 [#](#FUNCTIONS-RANGE)

範圍型別的概觀請參閱[第 8.17 節](../datatype/rangetypes.md)。

[表 9.58](functions-range.md#RANGE-OPERATORS-TABLE) 列出了可用於範圍型別的特殊運算子。[表 9.59](functions-range.md#MULTIRANGE-OPERATORS-TABLE) 列出了可用於多重範圍型別的特殊運算子。除此之外，範圍與多重範圍型別也可以使用[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子。比較運算子會先依範圍的下界排序，只有在下界相等時才比較上界。多重範圍運算子會逐一比較每個範圍，直到遇到不相等的範圍為止。這通常不會產生有用的整體排序，但提供這些運算子是為了能在範圍上建立唯一索引。

<a id="RANGE-OPERATORS-TABLE"></a>

**表 9.58. 範圍運算子**

<table border="1" class="table" summary="Range Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否包含第二個範圍？
       </p>
<p>
<code class="literal">int4range(2,4) @&gt; int4range(2,3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anyelement</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否包含該元素？
       </p>
<p>
<code class="literal">'[2011-01-01,2011-03-01)'::tsrange @&gt; '2011-01-10'::timestamp</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否被第二個範圍包含？
       </p>
<p>
<code class="literal">int4range(2,4) &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyelement</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        元素是否包含在範圍內？
       </p>
<p>
<code class="literal">42 &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&amp;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個範圍是否重疊，也就是有任何共同的元素？
       </p>
<p>
<code class="literal">int8range(3,7) &amp;&amp; int8range(4,12)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否嚴格位於第二個範圍的左邊？
       </p>
<p>
<code class="literal">int8range(1,10) &lt;&lt; int8range(100,110)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&gt;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否嚴格位於第二個範圍的右邊？
       </p>
<p>
<code class="literal">int8range(50,60) &gt;&gt; int8range(20,30)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否沒有延伸到第二個範圍的右邊？
       </p>
<p>
<code class="literal">int8range(1,20) &amp;&lt; int8range(18,20)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個範圍是否沒有延伸到第二個範圍的左邊？
       </p>
<p>
<code class="literal">int8range(7,20) &amp;&gt; int8range(5,10)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-|-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個範圍是否相鄰？
       </p>
<p>
<code class="literal">numrange(1.1,2.2) -|- numrange(2.2,3.3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">+</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        計算兩個範圍的聯集。兩個範圍必須重疊或相鄰，使聯集成為單一範圍（但請參閱 <code class="function">range_merge()</code>）。
       </p>
<p>
<code class="literal">numrange(5,15) + numrange(10,20)</code>
        → <code class="returnvalue">[5,20)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">*</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        計算兩個範圍的交集。
       </p>
<p>
<code class="literal">int8range(5,15) * int8range(10,20)</code>
        → <code class="returnvalue">[10,15)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        計算兩個範圍的差集。第二個範圍不得以使差集無法成為單一範圍的方式包含在第一個範圍中。
       </p>
<p>
<code class="literal">int8range(5,15) - int8range(10,20)</code>
        → <code class="returnvalue">[5,10)</code>
</p></td></tr></tbody></table>

<br><a id="MULTIRANGE-OPERATORS-TABLE"></a>

**表 9.59. 多重範圍運算子**

<table border="1" class="table" summary="Multirange Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否包含第二個多重範圍？
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange @&gt; '{[2,3)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否包含該範圍？
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange @&gt; int4range(2,3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anyelement</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否包含該元素？
       </p>
<p>
<code class="literal">'{[2011-01-01,2011-03-01)}'::tsmultirange @&gt; '2011-01-10'::timestamp</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否包含該多重範圍？
       </p>
<p>
<code class="literal">'[2,4)'::int4range @&gt; '{[2,3)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否被第二個多重範圍包含？
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否被該範圍包含？
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否被該多重範圍包含？
       </p>
<p>
<code class="literal">int4range(2,4) &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyelement</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        元素是否被該多重範圍包含？
       </p>
<p>
<code class="literal">4 &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&amp;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個多重範圍是否重疊，也就是有任何共同的元素？
       </p>
<p>
<code class="literal">'{[3,7)}'::int8multirange &amp;&amp; '{[4,12)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&amp;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否與該範圍重疊？
       </p>
<p>
<code class="literal">'{[3,7)}'::int8multirange &amp;&amp; int8range(4,12)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&amp;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否與該多重範圍重疊？
       </p>
<p>
<code class="literal">int8range(3,7) &amp;&amp; '{[4,12)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否嚴格位於第二個多重範圍的左邊？
       </p>
<p>
<code class="literal">'{[1,10)}'::int8multirange &lt;&lt; '{[100,110)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否嚴格位於該範圍的左邊？
       </p>
<p>
<code class="literal">'{[1,10)}'::int8multirange &lt;&lt; int8range(100,110)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否嚴格位於該多重範圍的左邊？
       </p>
<p>
<code class="literal">int8range(1,10) &lt;&lt; '{[100,110)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&gt;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否嚴格位於第二個多重範圍的右邊？
       </p>
<p>
<code class="literal">'{[50,60)}'::int8multirange &gt;&gt; '{[20,30)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&gt;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否嚴格位於該範圍的右邊？
       </p>
<p>
<code class="literal">'{[50,60)}'::int8multirange &gt;&gt; int8range(20,30)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&gt;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否嚴格位於該多重範圍的右邊？
       </p>
<p>
<code class="literal">int8range(50,60) &gt;&gt; '{[20,30)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否沒有延伸到第二個多重範圍的右邊？
       </p>
<p>
<code class="literal">'{[1,20)}'::int8multirange &amp;&lt; '{[18,20)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否沒有延伸到該範圍的右邊？
       </p>
<p>
<code class="literal">'{[1,20)}'::int8multirange &amp;&lt; int8range(18,20)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否沒有延伸到該多重範圍的右邊？
       </p>
<p>
<code class="literal">int8range(1,20) &amp;&lt; '{[18,20)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個多重範圍是否沒有延伸到第二個多重範圍的左邊？
       </p>
<p>
<code class="literal">'{[7,20)}'::int8multirange &amp;&gt; '{[5,10)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否沒有延伸到該範圍的左邊？
       </p>
<p>
<code class="literal">'{[7,20)}'::int8multirange &amp;&gt; int8range(5,10)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否沒有延伸到該多重範圍的左邊？
       </p>
<p>
<code class="literal">int8range(7,20) &amp;&gt; '{[5,10)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-|-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個多重範圍是否相鄰？
       </p>
<p>
<code class="literal">'{[1.1,2.2)}'::nummultirange -|- '{[2.2,3.3)}'::nummultirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-|-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否與該範圍相鄰？
       </p>
<p>
<code class="literal">'{[1.1,2.2)}'::nummultirange -|- numrange(2.2,3.3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-|-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否與該多重範圍相鄰？
       </p>
<p>
<code class="literal">numrange(1.1,2.2) -|- '{[2.2,3.3)}'::nummultirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">+</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        計算兩個多重範圍的聯集。兩個多重範圍不需要重疊或相鄰。
       </p>
<p>
<code class="literal">'{[5,10)}'::nummultirange + '{[15,20)}'::nummultirange</code>
        → <code class="returnvalue">{[5,10), [15,20)}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">*</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        計算兩個多重範圍的交集。
       </p>
<p>
<code class="literal">'{[5,15)}'::int8multirange * '{[10,20)}'::int8multirange</code>
        → <code class="returnvalue">{[10,15)}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        計算兩個多重範圍的差集。
       </p>
<p>
<code class="literal">'{[5,20)}'::int8multirange - '{[10,15)}'::int8multirange</code>
        → <code class="returnvalue">{[5,10), [15,20)}</code>
</p></td></tr></tbody></table>

<br>

當涉及空範圍或空多重範圍時，在左邊／在右邊／相鄰運算子一律回傳 false；也就是說，空範圍不會被視為位於任何其他範圍之前或之後。

在其他情況下，空範圍與空多重範圍會被視為加法單位元：任何東西與空值取聯集都等於它本身。任何東西減去空值也都等於它本身。空多重範圍與空範圍所含的點完全相同。每個範圍都包含空範圍。每個多重範圍都可以包含任意多個空範圍。

如果結果範圍需要包含兩個不相交的子範圍，範圍的聯集與差集運算子就會失敗，因為這樣的範圍無法表示。另外有一組接受多重範圍參數並回傳多重範圍的聯集與差集運算子，即使它們的引數不相交也不會失敗。所以，如果你需要對可能不相交的範圍進行聯集或差集運算，可以先將範圍轉換為多重範圍來避免錯誤。

[表 9.60](functions-range.md#RANGE-FUNCTIONS-TABLE) 列出了可用於範圍型別的函式。[表 9.61](functions-range.md#MULTIRANGE-FUNCTIONS-TABLE) 列出了可用於多重範圍型別的函式。

<a id="RANGE-FUNCTIONS-TABLE"></a>

**表 9.60. 範圍函式**

<table border="1" class="table" summary="Range Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.1.1.1.1"></a>
<code class="function">lower</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        擷取範圍的下界（如果範圍是空的或沒有下界，則為 <code class="literal">NULL</code>）。
       </p>
<p>
<code class="literal">lower(numrange(1.1,2.2))</code>
        → <code class="returnvalue">1.1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.2.1.1.1"></a>
<code class="function">upper</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        擷取範圍的上界（如果範圍是空的或沒有上界，則為 <code class="literal">NULL</code>）。
       </p>
<p>
<code class="literal">upper(numrange(1.1,2.2))</code>
        → <code class="returnvalue">2.2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.3.1.1.1"></a>
<code class="function">isempty</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否為空？
       </p>
<p>
<code class="literal">isempty(numrange(1.1,2.2))</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.4.1.1.1"></a>
<code class="function">lower_inc</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍的下界是否為包含的？
       </p>
<p>
<code class="literal">lower_inc(numrange(1.1,2.2))</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.5.1.1.1"></a>
<code class="function">upper_inc</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍的上界是否為包含的？
       </p>
<p>
<code class="literal">upper_inc(numrange(1.1,2.2))</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.6.1.1.1"></a>
<code class="function">lower_inf</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否沒有下界？（下界為 <code class="literal">-Infinity</code> 時會回傳 false。）
       </p>
<p>
<code class="literal">lower_inf('(,)'::daterange)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.7.1.1.1"></a>
<code class="function">upper_inf</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        範圍是否沒有上界？（上界為 <code class="literal">Infinity</code> 時會回傳 false。）
       </p>
<p>
<code class="literal">upper_inf('(,)'::daterange)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.8.1.1.1"></a>
<code class="function">range_merge</code> ( <code class="type">anyrange</code>, <code class="type">anyrange</code> )
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        計算同時包含兩個給定範圍的最小範圍。
       </p>
<p>
<code class="literal">range_merge('[1,2)'::int4range, '[3,4)'::int4range)</code>
        → <code class="returnvalue">[1,4)</code>
</p></td></tr></tbody></table>

<br><a id="MULTIRANGE-FUNCTIONS-TABLE"></a>

**表 9.61. 多重範圍函式**

<table border="1" class="table" summary="Multirange Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.1.1.1.1"></a>
<code class="function">lower</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        擷取多重範圍的下界（如果多重範圍是空的或沒有下界，則為 <code class="literal">NULL</code>）。
       </p>
<p>
<code class="literal">lower('{[1.1,2.2)}'::nummultirange)</code>
        → <code class="returnvalue">1.1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.2.1.1.1"></a>
<code class="function">upper</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        擷取多重範圍的上界（如果多重範圍是空的或沒有上界，則為 <code class="literal">NULL</code>）。
       </p>
<p>
<code class="literal">upper('{[1.1,2.2)}'::nummultirange)</code>
        → <code class="returnvalue">2.2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.3.1.1.1"></a>
<code class="function">isempty</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否為空？
       </p>
<p>
<code class="literal">isempty('{[1.1,2.2)}'::nummultirange)</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.4.1.1.1"></a>
<code class="function">lower_inc</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍的下界是否為包含的？
       </p>
<p>
<code class="literal">lower_inc('{[1.1,2.2)}'::nummultirange)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.5.1.1.1"></a>
<code class="function">upper_inc</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍的上界是否為包含的？
       </p>
<p>
<code class="literal">upper_inc('{[1.1,2.2)}'::nummultirange)</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.6.1.1.1"></a>
<code class="function">lower_inf</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否沒有下界？（下界為 <code class="literal">-Infinity</code> 時會回傳 false。）
       </p>
<p>
<code class="literal">lower_inf('{(,)}'::datemultirange)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.7.1.1.1"></a>
<code class="function">upper_inf</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        多重範圍是否沒有上界？（上界為 <code class="literal">Infinity</code> 時會回傳 false。）
       </p>
<p>
<code class="literal">upper_inf('{(,)}'::datemultirange)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.8.1.1.1"></a>
<code class="function">range_merge</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        計算包含整個多重範圍的最小範圍。
       </p>
<p>
<code class="literal">range_merge('{[1,2), [3,4)}'::int4multirange)</code>
        → <code class="returnvalue">[1,4)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.9.1.1.1"></a>
<code class="function">multirange</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        回傳只包含給定範圍的多重範圍。
       </p>
<p>
<code class="literal">multirange('[1,2)'::int4range)</code>
        → <code class="returnvalue">{[1,2)}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.10.1.1.1"></a>
<code class="function">unnest</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">setof anyrange</code>
</p>
<p>
        將多重範圍展開成一組依遞增順序排列的範圍。
       </p>
<p>
<code class="literal">unnest('{[1,2), [3,4)}'::int4multirange)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 [1,2)
 [3,4)
</pre><p>
</p></td></tr></tbody></table>

<br>

對於空範圍或空多重範圍，`lower_inc`、`upper_inc`、`lower_inf` 與 `upper_inf` 函式都會回傳 false。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-range.html)（原文版本：18.6；核對日期：2026-09-11）
