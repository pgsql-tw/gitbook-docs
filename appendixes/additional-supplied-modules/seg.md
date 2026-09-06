<a id="SEG"></a>

# F.39. seg

[F.39.1. Rationale](#id-1.11.7.48.5)

[F.39.2. Syntax](#id-1.11.7.48.6)

[F.39.3. Precision](#id-1.11.7.48.7)

[F.39.4. Usage](#id-1.11.7.48.8)

[F.39.5. Notes](#id-1.11.7.48.9)

[F.39.6. Credits](#id-1.11.7.48.10)

<a id="id-1.11.7.48.2"></a>

This module implements a data type `seg` for representing line segments, or floating point intervals. `seg` can represent uncertainty in the interval endpoints, making it especially useful for representing laboratory measurements.

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

<a id="id-1.11.7.48.5"></a>

## F.39.1. Rationale

The geometry of measurements is usually more complex than that of a point in a numeric continuum. A measurement is usually a segment of that continuum with somewhat fuzzy limits. The measurements come out as intervals because of uncertainty and randomness, as well as because the value being measured may naturally be an interval indicating some condition, such as the temperature range of stability of a protein.

Using just common sense, it appears more convenient to store such data as intervals, rather than pairs of numbers. In practice, it even turns out more efficient in most applications.

Further along the line of common sense, the fuzziness of the limits suggests that the use of traditional numeric data types leads to a certain loss of information. Consider this: your instrument reads 6.50, and you input this reading into the database. What do you get when you fetch it? Watch:

```

test=> select 6.50 :: float8 as "pH";
 pH
---
6.5
(1 row)
```

In the world of measurements, 6.50 is not the same as 6.5. It may sometimes be critically different. The experimenters usually write down (and publish) the digits they trust. 6.50 is actually a fuzzy interval contained within a bigger and even fuzzier interval, 6.5, with their center points being (probably) the only common feature they share. We definitely do not want such different data items to appear the same.

Conclusion? It is nice to have a special data type that can record the limits of an interval with arbitrarily variable precision. Variable in the sense that each data element records its own precision.

Check this out:

```

test=> select '6.25 .. 6.50'::seg as "pH";
          pH
------------
6.25 .. 6.50
(1 row)
```

<a id="id-1.11.7.48.6"></a>

## F.39.2. Syntax

The external representation of an interval is formed using one or two floating-point numbers joined by the range operator (`..` or `...`). Alternatively, it can be specified as a center point plus or minus a deviation. Optional certainty indicators (`<`, `>` or `~`) can be stored as well. (Certainty indicators are ignored by all the built-in operators, however.) [Table F.26](#SEG-REPR-TABLE) gives an overview of allowed representations; [Table F.27](#SEG-INPUT-EXAMPLES) shows some examples.

In [Table F.26](#SEG-REPR-TABLE), <em class="replaceable"><code>x</code></em>, <em class="replaceable"><code>y</code></em>, and <em class="replaceable"><code>delta</code></em> denote floating-point numbers. <em class="replaceable"><code>x</code></em> and <em class="replaceable"><code>y</code></em>, but not <em class="replaceable"><code>delta</code></em>, can be preceded by a certainty indicator.

<a id="SEG-REPR-TABLE"></a>

<strong>Table F.26. <code class="type">seg</code> External Representations</strong>

<table border="1" class="table" summary="seg External Representations">
<colgroup>
<col/>
<col/>
</colgroup>
<tbody>
<tr>
<td><code class="literal"><em class="replaceable"><code>x</code></em></code></td>
<td>Single value (zero-length interval)</td>
</tr>
<tr>
<td><code class="literal"><em class="replaceable"><code>x</code></em> .. <em class="replaceable"><code>y</code></em></code></td>
<td>Interval from <em class="replaceable"><code>x</code></em> to <em class="replaceable"><code>y</code></em></td>
</tr>
<tr>
<td><code class="literal"><em class="replaceable"><code>x</code></em> (+-) <em class="replaceable"><code>delta</code></em></code></td>
<td>Interval from <em class="replaceable"><code>x</code></em> - <em class="replaceable"><code>delta</code></em> to <em class="replaceable"><code>x</code></em> + <em class="replaceable"><code>delta</code></em></td>
</tr>
<tr>
<td><code class="literal"><em class="replaceable"><code>x</code></em> ..</code></td>
<td>Open interval with lower bound <em class="replaceable"><code>x</code></em></td>
</tr>
<tr>
<td><code class="literal">.. <em class="replaceable"><code>x</code></em></code></td>
<td>Open interval with upper bound <em class="replaceable"><code>x</code></em></td>
</tr>
</tbody>
</table>


<a id="SEG-INPUT-EXAMPLES"></a>

<strong>Table F.27. Examples of Valid <code class="type">seg</code> Input</strong>

<table border="1" class="table" summary="Examples of Valid seg Input">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<tbody>
<tr>
<td><code class="literal">5.0</code></td>
<td>Creates a zero-length segment (a point, if you will)</td>
</tr>
<tr>
<td><code class="literal">~5.0</code></td>
<td>Creates a zero-length segment and records <code class="literal">~</code> in the data. <code class="literal">~</code> is ignored by <code class="type">seg</code> operations, but is preserved as a comment.</td>
</tr>
<tr>
<td><code class="literal">&lt;5.0</code></td>
<td>Creates a point at 5.0. <code class="literal">&lt;</code> is ignored but is preserved as a comment.</td>
</tr>
<tr>
<td><code class="literal">&gt;5.0</code></td>
<td>Creates a point at 5.0. <code class="literal">&gt;</code> is ignored but is preserved as a comment.</td>
</tr>
<tr>
<td><code class="literal">5(+-)0.3</code></td>
<td>Creates an interval <code class="literal">4.7 .. 5.3</code>. Note that the <code class="literal">(+-)</code> notation isn't preserved.</td>
</tr>
<tr>
<td><code class="literal">50 ..</code></td>
<td>Everything that is greater than or equal to 50</td>
</tr>
<tr>
<td><code class="literal">.. 0</code></td>
<td>Everything that is less than or equal to 0</td>
</tr>
<tr>
<td><code class="literal">1.5e-2 .. 2E-2</code></td>
<td>Creates an interval <code class="literal">0.015 .. 0.02</code></td>
</tr>
<tr>
<td><code class="literal">1 ... 2</code></td>
<td>The same as <code class="literal">1...2</code>, or <code class="literal">1 .. 2</code>, or <code class="literal">1..2</code> (spaces around the range operator are ignored)</td>
</tr>
</tbody>
</table>



Because the `...` operator is widely used in data sources, it is allowed as an alternative spelling of the `..` operator. Unfortunately, this creates a parsing ambiguity: it is not clear whether the upper bound in `0...23` is meant to be `23` or `0.23`. This is resolved by requiring at least one digit before the decimal point in all numbers in `seg` input.

As a sanity check, `seg` rejects intervals with the lower bound greater than the upper, for example `5 .. 2`.

<a id="id-1.11.7.48.7"></a>

## F.39.3. Precision

`seg` values are stored internally as pairs of 32-bit floating point numbers. This means that numbers with more than 7 significant digits will be truncated.

Numbers with 7 or fewer significant digits retain their original precision. That is, if your query returns 0.00, you will be sure that the trailing zeroes are not the artifacts of formatting: they reflect the precision of the original data. The number of leading zeroes does not affect precision: the value 0.0067 is considered to have just 2 significant digits.

<a id="id-1.11.7.48.8"></a>

## F.39.4. Usage

The `seg` module includes a GiST index operator class for `seg` values. The operators supported by the GiST operator class are shown in [Table F.28](#SEG-GIST-OPERATORS).

<a id="SEG-GIST-OPERATORS"></a>

<strong>Table F.28. Seg GiST Operators</strong>

<table border="1" class="table" summary="Seg GiST Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operator</p>
<p>Description</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&lt;&lt;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Is the first <code class="type">seg</code> entirely to the left of the second? [a, b] &lt;&lt; [c, d] is true if b &lt; c.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&gt;&gt;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Is the first <code class="type">seg</code> entirely to the right of the second? [a, b] &gt;&gt; [c, d] is true if a &gt; d.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&amp;&lt;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Does the first <code class="type">seg</code> not extend to the right of the second? [a, b] &amp;&lt; [c, d] is true if b &lt;= d.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&amp;&gt;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Does the first <code class="type">seg</code> not extend to the left of the second? [a, b] &amp;&gt; [c, d] is true if a &gt;= c.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">=</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Are the two <code class="type">seg</code>s equal?</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&amp;&amp;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Do the two <code class="type">seg</code>s overlap?</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">@&gt;</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Does the first <code class="type">seg</code> contain the second?</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature"><code class="type">seg</code> <code class="literal">&lt;@</code> <code class="type">seg</code> → <code class="returnvalue">boolean</code></p>
<p>Is the first <code class="type">seg</code> contained in the second?</p>
</td>
</tr>
</tbody>
</table>



In addition to the above operators, the usual comparison operators shown in [Table 9.1](https://www.postgresql.org/docs/15/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE) are available for type `seg`. These operators first compare (a) to (c), and if these are equal, compare (b) to (d). That results in reasonably good sorting in most cases, which is useful if you want to use ORDER BY with this type.

<a id="id-1.11.7.48.9"></a>

## F.39.5. Notes

For examples of usage, see the regression test `sql/seg.sql`.

The mechanism that converts `(+-)` to regular ranges isn't completely accurate in determining the number of significant digits for the boundaries. For example, it adds an extra digit to the lower boundary if the resulting interval includes a power of ten:

```

postgres=> select '10(+-)1'::seg as seg;
      seg
---------
9.0 .. 11             -- should be: 9 .. 11
```

The performance of an R-tree index can largely depend on the initial order of input values. It may be very helpful to sort the input table on the `seg` column; see the script `sort-segments.pl` for an example.

<a id="id-1.11.7.48.10"></a>

## F.39.6. Credits

Original author: Gene Selkov, Jr. <code class="email">&lt;<a class="email" href="mailto:selkovjr@mcs.anl.gov">selkovjr@mcs.anl.gov</a>&gt;</code>, Mathematics and Computer Science Division, Argonne National Laboratory.

My thanks are primarily to Prof. Joe Hellerstein (<https://dsf.berkeley.edu/jmh/>) for elucidating the gist of the GiST (<http://gist.cs.berkeley.edu/>). I am also grateful to all Postgres developers, present and past, for enabling myself to create my own world and live undisturbed in it. And I would like to acknowledge my gratitude to Argonne Lab and to the U.S. Department of Energy for the years of faithful support of my database research.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/seg.html)（英文原文，待翻譯）
