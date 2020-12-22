# 9.22. Window 函式

_Window functions_ provide the ability to perform calculations across sets of rows that are related to the current query row. See [Section 3.5](https://www.postgresql.org/docs/13/tutorial-window.html) for an introduction to this feature, and [Section 4.2.8](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) for syntax details.

The built-in window functions are listed in [Table 9.60](https://www.postgresql.org/docs/13/functions-window.html#FUNCTIONS-WINDOW-TABLE). Note that these functions _must_ be invoked using window function syntax, i.e., an `OVER` clause is required.

In addition to these functions, any built-in or user-defined ordinary aggregate \(i.e., not ordered-set or hypothetical-set aggregates\) can be used as a window function; see [Section 9.21](https://www.postgresql.org/docs/13/functions-aggregate.html) for a list of the built-in aggregates. Aggregate functions act as window functions only when an `OVER` clause follows the call; otherwise they act as plain aggregates and return a single row for the entire set.

#### **Table 9.60. General-Purpose Window Functions**

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
        <p><code>row_number</code> () &#x2192; <code>bigint</code>
        </p>
        <p>Returns the number of the current row within its partition, counting from
          1.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>rank</code> () &#x2192; <code>bigint</code>
        </p>
        <p>Returns the rank of the current row, with gaps; that is, the <code>row_number</code> of
          the first row in its peer group.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>dense_rank</code> () &#x2192; <code>bigint</code>
        </p>
        <p>Returns the rank of the current row, without gaps; this function effectively
          counts peer groups.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>percent_rank</code> () &#x2192; <code>double precision</code>
        </p>
        <p>Returns the relative rank of the current row, that is (<code>rank</code> -
          1) / (total partition rows - 1). The value thus ranges from 0 to 1 inclusive.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>cume_dist</code> () &#x2192; <code>double precision</code>
        </p>
        <p>Returns the cumulative distribution, that is (number of partition rows
          preceding or peers with current row) / (total partition rows). The value
          thus ranges from 1/<em><code>N</code></em> to 1.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>ntile</code> ( <em><code>num_buckets</code></em>  <code>integer</code> )
          &#x2192; <code>integer</code>
        </p>
        <p>Returns an integer ranging from 1 to the argument value, dividing the
          partition as equally as possible.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>lag</code> ( <em><code>value</code></em>  <code>anyelement</code> [, <em><code>offset</code></em>  <code>integer</code> [, <em><code>default</code></em>  <code>anyelement</code> ]]
          ) &#x2192; <code>anyelement</code>
        </p>
        <p>Returns <em><code>value</code></em> evaluated at the row that is <em><code>offset</code></em> rows
          before the current row within the partition; if there is no such row, instead
          returns <em><code>default</code></em> (which must be of the same type as <em><code>value</code></em>).
          Both <em><code>offset</code></em> and <em><code>default</code></em> are evaluated
          with respect to the current row. If omitted, <em><code>offset</code></em> defaults
          to 1 and <em><code>default</code></em> to <code>NULL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>lead</code> ( <em><code>value</code></em>  <code>anyelement</code> [, <em><code>offset</code></em>  <code>integer</code> [, <em><code>default</code></em>  <code>anyelement</code> ]]
          ) &#x2192; <code>anyelement</code>
        </p>
        <p>Returns <em><code>value</code></em> evaluated at the row that is <em><code>offset</code></em> rows
          after the current row within the partition; if there is no such row, instead
          returns <em><code>default</code></em> (which must be of the same type as <em><code>value</code></em>).
          Both <em><code>offset</code></em> and <em><code>default</code></em> are evaluated
          with respect to the current row. If omitted, <em><code>offset</code></em> defaults
          to 1 and <em><code>default</code></em> to <code>NULL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>first_value</code> ( <em><code>value</code></em>  <code>anyelement</code> )
          &#x2192; <code>anyelement</code>
        </p>
        <p>Returns <em><code>value</code></em> evaluated at the row that is the first
          row of the window frame.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_value</code> ( <em><code>value</code></em>  <code>anyelement</code> )
          &#x2192; <code>anyelement</code>
        </p>
        <p>Returns <em><code>value</code></em> evaluated at the row that is the last
          row of the window frame.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>nth_value</code> ( <em><code>value</code></em>  <code>anyelement</code>, <em><code>n</code></em>  <code>integer</code> )
          &#x2192; <code>anyelement</code>
        </p>
        <p>Returns <em><code>value</code></em> evaluated at the row that is the <em><code>n</code></em>&apos;th
          row of the window frame (counting from 1); returns <code>NULL</code> if there
          is no such row.</p>
      </td>
    </tr>
  </tbody>
</table>

All of the functions listed in [Table 9.60](https://www.postgresql.org/docs/13/functions-window.html#FUNCTIONS-WINDOW-TABLE) depend on the sort ordering specified by the `ORDER BY` clause of the associated window definition. Rows that are not distinct when considering only the `ORDER BY` columns are said to be _peers_. The four ranking functions \(including `cume_dist`\) are defined so that they give the same answer for all rows of a peer group.

Note that `first_value`, `last_value`, and `nth_value` consider only the rows within the “window frame”, which by default contains the rows from the start of the partition through the last peer of the current row. This is likely to give unhelpful results for `last_value` and sometimes also `nth_value`. You can redefine the frame by adding a suitable frame specification \(`RANGE`, `ROWS` or `GROUPS`\) to the `OVER` clause. See [Section 4.2.8](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) for more information about frame specifications.

When an aggregate function is used as a window function, it aggregates over the rows within the current row's window frame. An aggregate used with `ORDER BY` and the default window frame definition produces a “running sum” type of behavior, which may or may not be what's wanted. To obtain aggregation over the whole partition, omit `ORDER BY` or use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Other frame specifications can be used to obtain other effects.

#### Note

The SQL standard defines a `RESPECT NULLS` or `IGNORE NULLS` option for `lead`, `lag`, `first_value`, `last_value`, and `nth_value`. This is not implemented in PostgreSQL: the behavior is always the same as the standard's default, namely `RESPECT NULLS`. Likewise, the standard's `FROM FIRST` or `FROM LAST` option for `nth_value` is not implemented: only the default `FROM FIRST` behavior is supported. \(You can achieve the result of `FROM LAST` by reversing the `ORDER BY` ordering.\)

