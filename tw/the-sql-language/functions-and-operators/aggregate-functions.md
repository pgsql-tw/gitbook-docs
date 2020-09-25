---
description: 版本：11
---

# 9.21. 彙總函數

_Aggregate functions_ compute a single result from a set of input values. The built-in general-purpose aggregate functions are listed in [Table 9.55](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-AGGREGATE-TABLE) while statistical aggregates are in [Table 9.56](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-AGGREGATE-STATISTICS-TABLE). The built-in within-group ordered-set aggregate functions are listed in [Table 9.57](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) while the built-in within-group hypothetical-set ones are in [Table 9.58](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-HYPOTHETICAL-TABLE). Grouping operations, which are closely related to aggregate functions, are listed in [Table 9.59](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-GROUPING-TABLE). The special syntax considerations for aggregate functions are explained in [Section 4.2.7](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-AGGREGATES). Consult [Section 2.7](https://www.postgresql.org/docs/13/tutorial-agg.html) for additional introductory information.

Aggregate functions that support _Partial Mode_ are eligible to participate in various optimizations, such as parallel aggregation.

#### **Table 9.55. General-Purpose Aggregate Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
      <th style="text-align:left">Partial Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>array_agg</code> ( <code>anynonarray</code> ) &#x2192; <code>anyarray</code>
        </p>
        <p>Collects all the input values, including nulls, into an array.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>array_agg</code> ( <code>anyarray</code> ) &#x2192; <code>anyarray</code>
        </p>
        <p>Concatenates all the input arrays into an array of one higher dimension.
          (The inputs must all have the same dimensionality, and cannot be empty
          or null.)</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>avg</code> ( <code>smallint</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>avg</code> ( <code>integer</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>avg</code> ( <code>bigint</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>avg</code> ( <code>numeric</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>avg</code> ( <code>real</code> ) &#x2192; <code>double precision</code>
        </p>
        <p><code>avg</code> ( <code>double precision</code> ) &#x2192; <code>double precision</code>
        </p>
        <p><code>avg</code> ( <code>interval</code> ) &#x2192; <code>interval</code>
        </p>
        <p>Computes the average (arithmetic mean) of all the non-null input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>bit_and</code> ( <code>smallint</code> ) &#x2192; <code>smallint</code>
        </p>
        <p><code>bit_and</code> ( <code>integer</code> ) &#x2192; <code>integer</code>
        </p>
        <p><code>bit_and</code> ( <code>bigint</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>bit_and</code> ( <code>bit</code> ) &#x2192; <code>bit</code>
        </p>
        <p>Computes the bitwise AND of all non-null input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>bit_or</code> ( <code>smallint</code> ) &#x2192; <code>smallint</code>
        </p>
        <p><code>bit_or</code> ( <code>integer</code> ) &#x2192; <code>integer</code>
        </p>
        <p><code>bit_or</code> ( <code>bigint</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>bit_or</code> ( <code>bit</code> ) &#x2192; <code>bit</code>
        </p>
        <p>Computes the bitwise OR of all non-null input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>bool_and</code> ( <code>boolean</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if all non-null input values are true, otherwise false.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>bool_or</code> ( <code>boolean</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if any non-null input value is true, otherwise false.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>count</code> ( <code>*</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the number of input rows.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>count</code> ( <code>&quot;any&quot;</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the number of input rows in which the input value is not null.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>every</code> ( <code>boolean</code> ) &#x2192; <code>boolean</code>
        </p>
        <p>This is the SQL standard&apos;s equivalent to <code>bool_and</code>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_agg</code> ( <code>anyelement</code> ) &#x2192; <code>json</code>
        </p>
        <p><code>jsonb_agg</code> ( <code>anyelement</code> ) &#x2192; <code>jsonb</code>
        </p>
        <p>Collects all the input values, including nulls, into a JSON array. Values
          are converted to JSON as per <code>to_json</code> or <code>to_jsonb</code>.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_object_agg</code> ( <em><code>key</code></em>  <code>&quot;any&quot;</code>, <em><code>value</code></em>  <code>&quot;any&quot;</code> )
          &#x2192; <code>json</code>
        </p>
        <p><code>jsonb_object_agg</code> ( <em><code>key</code></em>  <code>&quot;any&quot;</code>, <em><code>value</code></em>  <code>&quot;any&quot;</code> )
          &#x2192; <code>jsonb</code>
        </p>
        <p>Collects all the key/value pairs into a JSON object. Key arguments are
          coerced to text; value arguments are converted as per <code>to_json</code> or <code>to_jsonb</code>.
          Values can be null, but not keys.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>max</code> ( <em><code>see text</code></em> ) &#x2192; <em><code>same as input type</code></em>
        </p>
        <p>Computes the maximum of the non-null input values. Available for any numeric,
          string, date/time, or enum type, as well as <code>inet</code>, <code>interval</code>, <code>money</code>, <code>oid</code>, <code>pg_lsn</code>, <code>tid</code>,
          and arrays of any of these types.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>min</code> ( <em><code>see text</code></em> ) &#x2192; <em><code>same as input type</code></em>
        </p>
        <p>Computes the minimum of the non-null input values. Available for any numeric,
          string, date/time, or enum type, as well as <code>inet</code>, <code>interval</code>, <code>money</code>, <code>oid</code>, <code>pg_lsn</code>, <code>tid</code>,
          and arrays of any of these types.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>string_agg</code> ( <em><code>value</code></em>  <code>text</code>, <em><code>delimiter</code></em>  <code>text</code> )
          &#x2192; <code>text</code>
        </p>
        <p><code>string_agg</code> ( <em><code>value</code></em>  <code>bytea</code>, <em><code>delimiter</code></em>  <code>bytea</code> )
          &#x2192; <code>bytea</code>
        </p>
        <p>Concatenates the non-null input values into a string. Each value after
          the first is preceded by the corresponding <em><code>delimiter</code></em> (if
          it&apos;s not null).</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sum</code> ( <code>smallint</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>sum</code> ( <code>integer</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>sum</code> ( <code>bigint</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>sum</code> ( <code>numeric</code> ) &#x2192; <code>numeric</code>
        </p>
        <p><code>sum</code> ( <code>real</code> ) &#x2192; <code>real</code>
        </p>
        <p><code>sum</code> ( <code>double precision</code> ) &#x2192; <code>double precision</code>
        </p>
        <p><code>sum</code> ( <code>interval</code> ) &#x2192; <code>interval</code>
        </p>
        <p><code>sum</code> ( <code>money</code> ) &#x2192; <code>money</code>
        </p>
        <p>Computes the sum of the non-null input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>xmlagg</code> ( <code>xml</code> ) &#x2192; <code>xml</code>
        </p>
        <p>Concatenates the non-null XML input values (see <a href="https://www.postgresql.org/docs/13/functions-xml.html#FUNCTIONS-XML-XMLAGG">Section 9.15.1.7</a>).</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
  </tbody>
</table>

It should be noted that except for `count`, these functions return a null value when no rows are selected. In particular, `sum` of no rows returns null, not zero as one might expect, and `array_agg` returns null rather than an empty array when there are no input rows. The `coalesce` function can be used to substitute zero or an empty array for null when necessary.

The aggregate functions `array_agg`, `json_agg`, `jsonb_agg`, `json_object_agg`, `jsonb_object_agg`, `string_agg`, and `xmlagg`, as well as similar user-defined aggregate functions, produce meaningfully different result values depending on the order of the input values. This ordering is unspecified by default, but can be controlled by writing an `ORDER BY` clause within the aggregate call, as shown in [Section 4.2.7](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-AGGREGATES). Alternatively, supplying the input values from a sorted subquery will usually work. For example:

```text
SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;
```

Beware that this approach can fail if the outer query level contains additional processing, such as a join, because that might cause the subquery's output to be reordered before the aggregate is computed.

#### Note

The boolean aggregates `bool_and` and `bool_or` correspond to the standard SQL aggregates `every` and `any` or `some`. PostgreSQL supports `every`, but not `any` or `some`, because there is an ambiguity built into the standard syntax:

```text
SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;
```

Here `ANY` can be considered either as introducing a subquery, or as being an aggregate function, if the subquery returns one row with a Boolean value. Thus the standard name cannot be given to these aggregates.

#### Note

Users accustomed to working with other SQL database management systems might be disappointed by the performance of the `count` aggregate when it is applied to the entire table. A query like:

```text
SELECT count(*) FROM sometable;
```

will require effort proportional to the size of the table: PostgreSQL will need to scan either the entire table or the entirety of an index that includes all rows in the table.

[Table 9.56](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-AGGREGATE-STATISTICS-TABLE) shows aggregate functions typically used in statistical analysis. \(These are separated out merely to avoid cluttering the listing of more-commonly-used aggregates.\) Functions shown as accepting _`numeric_type`_ are available for all the types `smallint`, `integer`, `bigint`, `numeric`, `real`, and `double precision`. Where the description mentions _`N`_, it means the number of input rows for which all the input expressions are non-null. In all cases, null is returned if the computation is meaningless, for example when _`N`_ is zero.

#### **Table 9.56. Aggregate Functions for Statistics**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
      <th style="text-align:left">Partial Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>corr</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the correlation coefficient.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>covar_pop</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the population covariance.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>covar_samp</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the sample covariance.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_avgx</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the average of the independent variable, <code>sum(</code><em><code>X</code></em>)/<em><code>N</code></em>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_avgy</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the average of the dependent variable, <code>sum(</code><em><code>Y</code></em>)/<em><code>N</code></em>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_count</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>bigint</code>
        </p>
        <p>Computes the number of rows in which both inputs are non-null.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_intercept</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the y-intercept of the least-squares-fit linear equation determined
          by the (<em><code>X</code></em>, <em><code>Y</code></em>) pairs.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_r2</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the square of the correlation coefficient.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_slope</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the slope of the least-squares-fit linear equation determined
          by the (<em><code>X</code></em>, <em><code>Y</code></em>) pairs.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_sxx</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the &#x201C;sum of squares&#x201D; of the independent variable, <code>sum(</code><em><code>X</code></em>^2)
          - sum(<em><code>X</code></em>)^2/<em><code>N</code></em>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_sxy</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the &#x201C;sum of products&#x201D; of independent times dependent
          variables, <code>sum(</code><em><code>X</code></em>*<em><code>Y</code></em>)
          - sum(<em><code>X</code></em>) * sum(<em><code>Y</code></em>)/<em><code>N</code></em>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>regr_syy</code> ( <em><code>Y</code></em>  <code>double precision</code>, <em><code>X</code></em>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the &#x201C;sum of squares&#x201D; of the dependent variable, <code>sum(</code><em><code>Y</code></em>^2)
          - sum(<em><code>Y</code></em>)^2/<em><code>N</code></em>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stddev</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>This is a historical alias for <code>stddev_samp</code>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stddev_pop</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>Computes the population standard deviation of the input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stddev_samp</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>Computes the sample standard deviation of the input values.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>variance</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>This is a historical alias for <code>var_samp</code>.</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>var_pop</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>Computes the population variance of the input values (square of the population
          standard deviation).</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>var_samp</code> ( <em><code>numeric_type</code></em> ) &#x2192; <code>double precision</code> for <code>real</code> or <code>double precision</code>,
          otherwise <code>numeric</code>
        </p>
        <p>Computes the sample variance of the input values (square of the sample
          standard deviation).</p>
      </td>
      <td style="text-align:left">Yes</td>
    </tr>
  </tbody>
</table>

[Table 9.57](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) shows some aggregate functions that use the _ordered-set aggregate_ syntax. These functions are sometimes referred to as “inverse distribution” functions. Their aggregated input is introduced by `ORDER BY`, and they may also take a _direct argument_ that is not aggregated, but is computed only once. All these functions ignore null values in their aggregated input. For those that take a _`fraction`_ parameter, the fraction value must be between 0 and 1; an error is thrown if not. However, a null _`fraction`_ value simply produces a null result.

#### **Table 9.57. Ordered-Set Aggregate Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
      <th style="text-align:left">Partial Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>mode</code> () <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>anyelement</code> )
          &#x2192; <code>anyelement</code>
        </p>
        <p>Computes the <em>mode</em>, the most frequent value of the aggregated argument
          (arbitrarily choosing the first one if there are multiple equally-frequent
          values). The aggregated argument must be of a sortable type.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percentile_cont</code> ( <em><code>fraction</code></em>  <code>double precision</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>double precision</code> )
          &#x2192; <code>double precision</code>
        </p>
        <p><code>percentile_cont</code> ( <em><code>fraction</code></em>  <code>double precision</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>interval</code> )
          &#x2192; <code>interval</code>
        </p>
        <p>Computes the <em>continuous percentile</em>, a value corresponding to the
          specified <em><code>fraction</code></em> within the ordered set of aggregated
          argument values. This will interpolate between adjacent input items if
          needed.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percentile_cont</code> ( <em><code>fractions</code></em>  <code>double precision[]</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>double precision</code> )
          &#x2192; <code>double precision[]</code>
        </p>
        <p><code>percentile_cont</code> ( <em><code>fractions</code></em>  <code>double precision[]</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>interval</code> )
          &#x2192; <code>interval[]</code>
        </p>
        <p>Computes multiple continuous percentiles. The result is an array of the
          same dimensions as the <em><code>fractions</code></em> parameter, with each
          non-null element replaced by the (possibly interpolated) value corresponding
          to that percentile.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percentile_disc</code> ( <em><code>fraction</code></em>  <code>double precision</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>anyelement</code> )
          &#x2192; <code>anyelement</code>
        </p>
        <p>Computes the <em>discrete percentile</em>, the first value within the ordered
          set of aggregated argument values whose position in the ordering equals
          or exceeds the specified <em><code>fraction</code></em>. The aggregated
          argument must be of a sortable type.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percentile_disc</code> ( <em><code>fractions</code></em>  <code>double precision[]</code> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <code>anyelement</code> )
          &#x2192; <code>anyarray</code>
        </p>
        <p>Computes multiple discrete percentiles. The result is an array of the
          same dimensions as the <em><code>fractions</code></em> parameter, with each
          non-null element replaced by the input value corresponding to that percentile.
          The aggregated argument must be of a sortable type.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
  </tbody>
</table>

Each of the “hypothetical-set” aggregates listed in [Table 9.58](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-HYPOTHETICAL-TABLE) is associated with a window function of the same name defined in [Section 9.22](https://www.postgresql.org/docs/13/functions-window.html). In each case, the aggregate's result is the value that the associated window function would have returned for the “hypothetical” row constructed from _`args`_, if such a row had been added to the sorted group of rows represented by the _`sorted_args`_. For each of these functions, the list of direct arguments given in _`args`_ must match the number and types of the aggregated arguments given in _`sorted_args`_. Unlike most built-in aggregates, these aggregates are not strict, that is they do not drop input rows containing nulls. Null values sort according to the rule specified in the `ORDER BY` clause.

#### **Table 9.58. Hypothetical-Set Aggregate Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
      <th style="text-align:left">Partial Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>rank</code> ( <em><code>args</code></em> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <em><code>sorted_args</code></em> )
          &#x2192; <code>bigint</code>
        </p>
        <p>Computes the rank of the hypothetical row, with gaps; that is, the row
          number of the first row in its peer group.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>dense_rank</code> ( <em><code>args</code></em> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <em><code>sorted_args</code></em> )
          &#x2192; <code>bigint</code>
        </p>
        <p>Computes the rank of the hypothetical row, without gaps; this function
          effectively counts peer groups.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percent_rank</code> ( <em><code>args</code></em> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <em><code>sorted_args</code></em> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the relative rank of the hypothetical row, that is (<code>rank</code> -
          1) / (total rows - 1). The value thus ranges from 0 to 1 inclusive.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>cume_dist</code> ( <em><code>args</code></em> ) <code>WITHIN GROUP</code> ( <code>ORDER BY</code>  <em><code>sorted_args</code></em> )
          &#x2192; <code>double precision</code>
        </p>
        <p>Computes the cumulative distribution, that is (number of rows preceding
          or peers with hypothetical row) / (total rows). The value thus ranges from
          1/<em><code>N</code></em> to 1.</p>
      </td>
      <td style="text-align:left">No</td>
    </tr>
  </tbody>
</table>

#### **Table 9.59. Grouping Operations**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>GROUPING</code> ( <em><code>group_by_expression(s)</code></em> ) &#x2192; <code>integer</code>
        </p>
        <p>Returns a bit mask indicating which <code>GROUP BY</code> expressions are
          not included in the current grouping set. Bits are assigned with the rightmost
          argument corresponding to the least-significant bit; each bit is 0 if the
          corresponding expression is included in the grouping criteria of the grouping
          set generating the current result row, and 1 if it is not included.</p>
      </td>
    </tr>
  </tbody>
</table>

The grouping operations shown in [Table 9.59](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-GROUPING-TABLE) are used in conjunction with grouping sets \(see [Section 7.2.4](https://www.postgresql.org/docs/13/queries-table-expressions.html#QUERIES-GROUPING-SETS)\) to distinguish result rows. The arguments to the `GROUPING` function are not actually evaluated, but they must exactly match expressions given in the `GROUP BY` clause of the associated query level. For example:

```text
=> SELECT * FROM items_sold;
 make  | model | sales
-------+-------+-------
 Foo   | GT    |  10
 Foo   | Tour  |  20
 Bar   | City  |  15
 Bar   | Sport |  5
(4 rows)

=> SELECT make, model, GROUPING(make,model), sum(sales) FROM items_sold GROUP BY ROLLUP(make,model);
 make  | model | grouping | sum
-------+-------+----------+-----
 Foo   | GT    |        0 | 10
 Foo   | Tour  |        0 | 20
 Bar   | City  |        0 | 15
 Bar   | Sport |        0 | 5
 Foo   |       |        1 | 30
 Bar   |       |        1 | 20
       |       |        3 | 50
(7 rows)
```

Here, the `grouping` value `0` in the first four rows shows that those have been grouped normally, over both the grouping columns. The value `1` indicates that `model` was not grouped by in the next-to-last two rows, and the value `3` indicates that neither `make` nor `model` was grouped by in the last row \(which therefore is an aggregate over all the input rows\).

