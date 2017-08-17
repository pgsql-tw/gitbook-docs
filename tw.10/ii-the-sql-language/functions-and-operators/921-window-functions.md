# 9.21. Window函式[^1]

_Window functions_provide the ability to perform calculations across sets of rows that are related to the current query row. See[Section 3.5](https://www.postgresql.org/docs/10/static/tutorial-window.html)for an introduction to this feature, and[Section 4.2.8](https://www.postgresql.org/docs/10/static/sql-expressions.html#syntax-window-functions)for syntax details.

The built-in window functions are listed in[Table 9.57](https://www.postgresql.org/docs/10/static/functions-window.html#functions-window-table). Note that these functions_must_be invoked using window function syntax, i.e., an`OVER`clause is required.

In addition to these functions, any built-in or user-defined general-purpose or statistical aggregate \(i.e., not ordered-set or hypothetical-set aggregates\) can be used as a window function; see[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html)for a list of the built-in aggregates. Aggregate functions act as window functions only when an`OVER`clause follows the call; otherwise they act as non-window aggregates and return a single row for the entire set.

**Table 9.57. General-Purpose Window Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `row_number()` | `bigint` | number of the current row within its partition, counting from 1 |
| `rank()` | `bigint` | rank of the current row with gaps; same as`row_number`of its first peer |
| `dense_rank()` | `bigint` | rank of the current row without gaps; this function counts peer groups |
| `percent_rank()` | `double precision` | relative rank of the current row: \(`rank`- 1\) / \(total partition rows - 1\) |
| `cume_dist()` | `double precision` | cumulative distribution: \(number of partition rows preceding or peer with current row\) / total partition rows |
| `ntile(`_`num_buckets`_`integer`\) | `integer` | integer ranging from 1 to the argument value, dividing the partition as equally as possible |
| `lag(`_`value`_`anyelement`\[,_`offset`_`integer`\[,_`default`_`anyelement`\]\]\) | `same type as`_`value`_ | returns_`value`_evaluated at the row that is_`offset`_rows before the current row within the partition; if there is no such row, instead return_`default`_\(which must be of the same type as_`value`_\). Both_`offset`_and_`default`_are evaluated with respect to the current row. If omitted,_`offset`_defaults to 1 and_`default`_to null |
| `lead(`_`value`_`anyelement`\[,_`offset`_`integer`\[,_`default`_`anyelement`\]\]\) | `same type as`_`value`_ | returns_`value`_evaluated at the row that is_`offset`_rows after the current row within the partition; if there is no such row, instead return_`default`_\(which must be of the same type as_`value`_\). Both_`offset`_and_`default`_are evaluated with respect to the current row. If omitted,_`offset`_defaults to 1 and_`default`_to null |
| `first_value(`_`value`_`any`\) | `same type as`_`value`_ | returns_`value`_evaluated at the row that is the first row of the window frame |
| `last_value(`_`value`_`any`\) | `same type as`_`value`_ | returns_`value`_evaluated at the row that is the last row of the window frame |
| `nth_value(`_`value`_`any`,_`nth`_`integer`\) | `same type as`_`value`_ | returns_`value`_evaluated at the row that is the_`nth`_row of the window frame \(counting from 1\); null if no such row |

  


All of the functions listed in[Table 9.57](https://www.postgresql.org/docs/10/static/functions-window.html#functions-window-table)depend on the sort ordering specified by the`ORDER BY`clause of the associated window definition. Rows that are not distinct when considering only the`ORDER BY`columns are said to be_peers_. The four ranking functions \(including`cume_dist`\) are defined so that they give the same answer for all peer rows.

Note that`first_value`,`last_value`, and`nth_value`consider only the rows within the“window frame”, which by default contains the rows from the start of the partition through the last peer of the current row. This is likely to give unhelpful results for`last_value`and sometimes also`nth_value`. You can redefine the frame by adding a suitable frame specification \(`RANGE`or`ROWS`\) to the`OVER`clause. See[Section 4.2.8](https://www.postgresql.org/docs/10/static/sql-expressions.html#syntax-window-functions)for more information about frame specifications.

When an aggregate function is used as a window function, it aggregates over the rows within the current row's window frame. An aggregate used with`ORDER BY`and the default window frame definition produces a“running sum”type of behavior, which may or may not be what's wanted. To obtain aggregation over the whole partition, omit`ORDER BY`or use`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Other frame specifications can be used to obtain other effects.

### Note

The SQL standard defines a`RESPECT NULLS`or`IGNORE NULLS`option for`lead`,`lag`,`first_value`,`last_value`, and`nth_value`. This is not implemented inPostgreSQL: the behavior is always the same as the standard's default, namely`RESPECT NULLS`. Likewise, the standard's`FROM FIRST`or`FROM LAST`option for`nth_value`is not implemented: only the default`FROM FIRST`behavior is supported. \(You can achieve the result of`FROM LAST`by reversing the`ORDER BY`ordering.\)

`cume_dist`computes the fraction of partition rows that are less than or equal to the current row and its peers, while`percent_rank`computes the fraction of partition rows that are less than the current row, assuming the current row does not exist in the partition.

---

  


[^1]:  [PostgreSQL: Documentation: 10: 9.21. Window Functions](https://www.postgresql.org/docs/10/static/functions-window.html)

