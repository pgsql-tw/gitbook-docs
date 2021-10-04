# 9.20. 範圍函式及運算子

See [Section 8.17](https://www.postgresql.org/docs/13/rangetypes.html) for an overview of range types.

[Table 9.53](https://www.postgresql.org/docs/13/functions-range.html#RANGE-OPERATORS-TABLE) shows the specialized operators available for range types. In addition to those, the usual comparison operators shown in [Table 9.1](https://www.postgresql.org/docs/13/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE) are available for range types. The comparison operators order first by the range lower bounds, and only if those are equal do they compare the upper bounds. This does not usually result in a useful overall ordering, but the operators are provided to allow unique indexes to be constructed on ranges.

#### **Table 9.53. Range Operators**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Operator</p>
        <p>Description</p>
        <p>Example(s)</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>@&gt;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Does the first range contain the second?</p>
        <p><code>int4range(2,4) @&gt; int4range(2,3)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>@&gt;</code>  <code>anyelement</code> &#x2192; <code>boolean</code>
        </p>
        <p>Does the range contain the element?</p>
        <p><code>&apos;[2011-01-01,2011-03-01)&apos;::tsrange @&gt; &apos;2011-01-10&apos;::timestamp</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&lt;@</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Is the first range contained by the second?</p>
        <p><code>int4range(2,4) &lt;@ int4range(1,7)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyelement</code>  <code>&lt;@</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Is the element contained in the range?</p>
        <p><code>42 &lt;@ int4range(1,7)</code> &#x2192; <code>f</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&amp;&amp;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Do the ranges overlap, that is, have any elements in common?</p>
        <p><code>int8range(3,7) &amp;&amp; int8range(4,12)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&lt;&lt;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Is the first range strictly left of the second?</p>
        <p><code>int8range(1,10) &lt;&lt; int8range(100,110)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&gt;&gt;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Is the first range strictly right of the second?</p>
        <p><code>int8range(50,60) &gt;&gt; int8range(20,30)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&amp;&lt;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Does the first range not extend to the right of the second?</p>
        <p><code>int8range(1,20) &amp;&lt; int8range(18,20)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>&amp;&gt;</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Does the first range not extend to the left of the second?</p>
        <p><code>int8range(7,20) &amp;&gt; int8range(5,10)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>-|-</code>  <code>anyrange</code> &#x2192; <code>boolean</code>
        </p>
        <p>Are the ranges adjacent?</p>
        <p><code>numrange(1.1,2.2) -|- numrange(2.2,3.3)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>+</code>  <code>anyrange</code> &#x2192; <code>anyrange</code>
        </p>
        <p>Computes the union of the ranges. The ranges must overlap or be adjacent,
          so that the union is a single range (but see <code>range_merge()</code>).</p>
        <p><code>numrange(5,15) + numrange(10,20)</code> &#x2192; <code>[5,20)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>*</code>  <code>anyrange</code> &#x2192; <code>anyrange</code>
        </p>
        <p>Computes the intersection of the ranges.</p>
        <p><code>int8range(5,15) * int8range(10,20)</code> &#x2192; <code>[10,15)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>anyrange</code>  <code>-</code>  <code>anyrange</code> &#x2192; <code>anyrange</code>
        </p>
        <p>Computes the difference of the ranges. The second range must not be contained
          in the first in such a way that the difference would not be a single range.</p>
        <p><code>int8range(5,15) - int8range(10,20)</code> &#x2192; <code>[5,10)</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

The left-of/right-of/adjacent operators always return false when an empty range is involved; that is, an empty range is not considered to be either before or after any other range.

[Table 9.54](https://www.postgresql.org/docs/13/functions-range.html#RANGE-FUNCTIONS-TABLE) shows the functions available for use with range types.

#### **Table 9.54. Range Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
        <p>Example(s)</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>lower</code> ( <code>anyrange</code> ) &#x2192; <code>anyelement</code>
        </p>
        <p>Extracts the lower bound of the range (<code>NULL</code> if the range is
          empty or the lower bound is infinite).</p>
        <p><code>lower(numrange(1.1,2.2))</code> &#x2192; <code>1.1</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>upper</code> ( <code>anyrange</code> ) &#x2192; <code>anyelement</code>
        </p>
        <p>Extracts the upper bound of the range (<code>NULL</code> if the range is
          empty or the upper bound is infinite).</p>
        <p><code>upper(numrange(1.1,2.2))</code> &#x2192; <code>2.2</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>isempty</code> ( <code>anyrange</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Is the range empty?</p>
        <p><code>isempty(numrange(1.1,2.2))</code> &#x2192; <code>f</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>lower_inc</code> ( <code>anyrange</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Is the range&apos;s lower bound inclusive?</p>
        <p><code>lower_inc(numrange(1.1,2.2))</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>upper_inc</code> ( <code>anyrange</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Is the range&apos;s upper bound inclusive?</p>
        <p><code>upper_inc(numrange(1.1,2.2))</code> &#x2192; <code>f</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>lower_inf</code> ( <code>anyrange</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Is the range&apos;s lower bound infinite?</p>
        <p><code>lower_inf(&apos;(,)&apos;::daterange)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>upper_inf</code> ( <code>anyrange</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Is the range&apos;s upper bound infinite?</p>
        <p><code>upper_inf(&apos;(,)&apos;::daterange)</code> &#x2192; <code>t</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>range_merge</code> ( <code>anyrange</code>, <code>anyrange</code> )
          &#x2192; <code>anyrange</code>
        </p>
        <p>Computes the smallest range that includes both of the given ranges.</p>
        <p><code>range_merge(&apos;[1,2)&apos;::int4range, &apos;[3,4)&apos;::int4range)</code> &#x2192; <code>[1,4)</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

The `lower_inc`, `upper_inc`, `lower_inf`, and `upper_inf` functions all return false for an empty range.

