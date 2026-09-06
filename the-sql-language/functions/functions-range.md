## 9.20. Range/Multirange Functions and Operators [#](#FUNCTIONS-RANGE)

See [Section 8.17](../datatype/rangetypes.md) for an overview of range types.

[Table 9.58](functions-range.md#RANGE-OPERATORS-TABLE) shows the specialized operators
available for range types.
[Table 9.59](functions-range.md#MULTIRANGE-OPERATORS-TABLE) shows the specialized operators
available for multirange types.
In addition to those, the usual comparison operators shown in
[Table 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) are available for range
and multirange types. The comparison operators order first by the range lower
bounds, and only if those are equal do they compare the upper bounds. The
multirange operators compare each range until one is unequal. This
does not usually result in a useful overall ordering, but the operators are
provided to allow unique indexes to be constructed on ranges.

<a id="RANGE-OPERATORS-TABLE"></a>

**Table 9.58. Range Operators**

<table border="1" class="table" summary="Range Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first range contain the second?
       </p>
<p>
<code class="literal">int4range(2,4) @&gt; int4range(2,3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anyelement</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the range contain the element?
       </p>
<p>
<code class="literal">'[2011-01-01,2011-03-01)'::tsrange @&gt; '2011-01-10'::timestamp</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first range contained by the second?
       </p>
<p>
<code class="literal">int4range(2,4) &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyelement</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the element contained in the range?
       </p>
<p>
<code class="literal">42 &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&amp;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Do the ranges overlap, that is, have any elements in common?
       </p>
<p>
<code class="literal">int8range(3,7) &amp;&amp; int8range(4,12)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first range strictly left of the second?
       </p>
<p>
<code class="literal">int8range(1,10) &lt;&lt; int8range(100,110)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&gt;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first range strictly right of the second?
       </p>
<p>
<code class="literal">int8range(50,60) &gt;&gt; int8range(20,30)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first range not extend to the right of the second?
       </p>
<p>
<code class="literal">int8range(1,20) &amp;&lt; int8range(18,20)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first range not extend to the left of the second?
       </p>
<p>
<code class="literal">int8range(7,20) &amp;&gt; int8range(5,10)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-|-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Are the ranges adjacent?
       </p>
<p>
<code class="literal">numrange(1.1,2.2) -|- numrange(2.2,3.3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">+</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        Computes the union of the ranges.  The ranges must overlap or be
        adjacent, so that the union is a single range (but
        see <code class="function">range_merge()</code>).
       </p>
<p>
<code class="literal">numrange(5,15) + numrange(10,20)</code>
        → <code class="returnvalue">[5,20)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">*</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        Computes the intersection of the ranges.
       </p>
<p>
<code class="literal">int8range(5,15) * int8range(10,20)</code>
        → <code class="returnvalue">[10,15)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">anyrange</code>
</p>
<p>
        Computes the difference of the ranges.  The second range must not be
        contained in the first in such a way that the difference would not be
        a single range.
       </p>
<p>
<code class="literal">int8range(5,15) - int8range(10,20)</code>
        → <code class="returnvalue">[5,10)</code>
</p></td></tr></tbody></table>

<br><a id="MULTIRANGE-OPERATORS-TABLE"></a>

**Table 9.59. Multirange Operators**

<table border="1" class="table" summary="Multirange Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first multirange contain the second?
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange @&gt; '{[2,3)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the multirange contain the range?
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange @&gt; int4range(2,3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">@&gt;</code> <code class="type">anyelement</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the multirange contain the element?
       </p>
<p>
<code class="literal">'{[2011-01-01,2011-03-01)}'::tsmultirange @&gt; '2011-01-10'::timestamp</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">@&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the range contain the multirange?
       </p>
<p>
<code class="literal">'[2,4)'::int4range @&gt; '{[2,3)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first multirange contained by the second?
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;@</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the multirange contained by the range?
       </p>
<p>
<code class="literal">'{[2,4)}'::int4multirange &lt;@ int4range(1,7)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the range contained by the multirange?
       </p>
<p>
<code class="literal">int4range(2,4) &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyelement</code> <code class="literal">&lt;@</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the element contained by the multirange?
       </p>
<p>
<code class="literal">4 &lt;@ '{[1,7)}'::int4multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&amp;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Do the multiranges overlap, that is, have any elements in common?
       </p>
<p>
<code class="literal">'{[3,7)}'::int8multirange &amp;&amp; '{[4,12)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&amp;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the multirange overlap the range?
       </p>
<p>
<code class="literal">'{[3,7)}'::int8multirange &amp;&amp; int8range(4,12)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&amp;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the range overlap the multirange?
       </p>
<p>
<code class="literal">int8range(3,7) &amp;&amp; '{[4,12)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first multirange strictly left of the second?
       </p>
<p>
<code class="literal">'{[1,10)}'::int8multirange &lt;&lt; '{[100,110)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&lt;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the multirange strictly left of the range?
       </p>
<p>
<code class="literal">'{[1,10)}'::int8multirange &lt;&lt; int8range(100,110)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&lt;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the range strictly left of the multirange?
       </p>
<p>
<code class="literal">int8range(1,10) &lt;&lt; '{[100,110)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&gt;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first multirange strictly right of the second?
       </p>
<p>
<code class="literal">'{[50,60)}'::int8multirange &gt;&gt; '{[20,30)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&gt;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the multirange strictly right of the range?
       </p>
<p>
<code class="literal">'{[50,60)}'::int8multirange &gt;&gt; int8range(20,30)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&gt;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the range strictly right of the multirange?
       </p>
<p>
<code class="literal">int8range(50,60) &gt;&gt; '{[20,30)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first multirange not extend to the right of the second?
       </p>
<p>
<code class="literal">'{[1,20)}'::int8multirange &amp;&lt; '{[18,20)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&lt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the multirange not extend to the right of the range?
       </p>
<p>
<code class="literal">'{[1,20)}'::int8multirange &amp;&lt; int8range(18,20)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&lt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the range not extend to the right of the multirange?
       </p>
<p>
<code class="literal">int8range(1,20) &amp;&lt; '{[18,20)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first multirange not extend to the left of the second?
       </p>
<p>
<code class="literal">'{[7,20)}'::int8multirange &amp;&gt; '{[5,10)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">&amp;&gt;</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the multirange not extend to the left of the range?
       </p>
<p>
<code class="literal">'{[7,20)}'::int8multirange &amp;&gt; int8range(5,10)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">&amp;&gt;</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the range not extend to the left of the multirange?
       </p>
<p>
<code class="literal">int8range(7,20) &amp;&gt; '{[5,10)}'::int8multirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-|-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Are the multiranges adjacent?
       </p>
<p>
<code class="literal">'{[1.1,2.2)}'::nummultirange -|- '{[2.2,3.3)}'::nummultirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-|-</code> <code class="type">anyrange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the multirange adjacent to the range?
       </p>
<p>
<code class="literal">'{[1.1,2.2)}'::nummultirange -|- numrange(2.2,3.3)</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anyrange</code> <code class="literal">-|-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the range adjacent to the multirange?
       </p>
<p>
<code class="literal">numrange(1.1,2.2) -|- '{[2.2,3.3)}'::nummultirange</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">+</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        Computes the union of the multiranges.  The multiranges need not overlap
        or be adjacent.
       </p>
<p>
<code class="literal">'{[5,10)}'::nummultirange + '{[15,20)}'::nummultirange</code>
        → <code class="returnvalue">{[5,10), [15,20)}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">*</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        Computes the intersection of the multiranges.
       </p>
<p>
<code class="literal">'{[5,15)}'::int8multirange * '{[10,20)}'::int8multirange</code>
        → <code class="returnvalue">{[10,15)}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">anymultirange</code> <code class="literal">-</code> <code class="type">anymultirange</code>
        → <code class="returnvalue">anymultirange</code>
</p>
<p>
        Computes the difference of the multiranges.
       </p>
<p>
<code class="literal">'{[5,20)}'::int8multirange - '{[10,15)}'::int8multirange</code>
        → <code class="returnvalue">{[5,10), [15,20)}</code>
</p></td></tr></tbody></table>

<br>

The left-of/right-of/adjacent operators always return false when an empty
range or multirange is involved; that is, an empty range is not considered to
be either before or after any other range.

Elsewhere empty ranges and multiranges are treated as the additive identity:
anything unioned with an empty value is itself. Anything minus an empty
value is itself. An empty multirange has exactly the same points as an empty
range. Every range contains the empty range. Every multirange contains as many
empty ranges as you like.

The range union and difference operators will fail if the resulting range would
need to contain two disjoint sub-ranges, as such a range cannot be
represented. There are separate operators for union and difference that take
multirange parameters and return a multirange, and they do not fail even if
their arguments are disjoint. So if you need a union or difference operation
for ranges that may be disjoint, you can avoid errors by first casting your
ranges to multiranges.

[Table 9.60](functions-range.md#RANGE-FUNCTIONS-TABLE) shows the functions
available for use with range types.
[Table 9.61](functions-range.md#MULTIRANGE-FUNCTIONS-TABLE) shows the functions
available for use with multirange types.

<a id="RANGE-FUNCTIONS-TABLE"></a>

**Table 9.60. Range Functions**

<table border="1" class="table" summary="Range Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.10.2.2.1.1.1.1"></a>
<code class="function">lower</code> ( <code class="type">anyrange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        Extracts the lower bound of the range (<code class="literal">NULL</code> if the
        range is empty or has no lower bound).
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
        Extracts the upper bound of the range (<code class="literal">NULL</code> if the
        range is empty or has no upper bound).
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
        Is the range empty?
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
        Is the range's lower bound inclusive?
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
        Is the range's upper bound inclusive?
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
        Does the range have no lower bound?  (A lower bound of
        <code class="literal">-Infinity</code> returns false.)
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
        Does the range have no upper bound?  (An upper bound of
        <code class="literal">Infinity</code> returns false.)
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
        Computes the smallest range that includes both of the given ranges.
       </p>
<p>
<code class="literal">range_merge('[1,2)'::int4range, '[3,4)'::int4range)</code>
        → <code class="returnvalue">[1,4)</code>
</p></td></tr></tbody></table>

<br><a id="MULTIRANGE-FUNCTIONS-TABLE"></a>

**Table 9.61. Multirange Functions**

<table border="1" class="table" summary="Multirange Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.26.11.2.2.1.1.1.1"></a>
<code class="function">lower</code> ( <code class="type">anymultirange</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        Extracts the lower bound of the multirange (<code class="literal">NULL</code> if the
        multirange is empty or has no lower bound).
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
        Extracts the upper bound of the multirange (<code class="literal">NULL</code> if the
        multirange is empty or has no upper bound).
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
        Is the multirange empty?
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
        Is the multirange's lower bound inclusive?
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
        Is the multirange's upper bound inclusive?
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
        Does the multirange have no lower bound?  (A lower bound of
        <code class="literal">-Infinity</code> returns false.)
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
        Does the multirange have no upper bound?  (An upper bound of
        <code class="literal">Infinity</code> returns false.)
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
        Computes the smallest range that includes the entire multirange.
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
        Returns a multirange containing just the given range.
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
        Expands a multirange into a set of ranges in ascending order.
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

The `lower_inc`, `upper_inc`,
`lower_inf`, and `upper_inf`
functions all return false for an empty range or multirange.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-range.html)（英文原文，待翻譯）
