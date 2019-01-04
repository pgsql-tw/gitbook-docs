---
description: 版本：11
---

# 9.20. 彙總函式

_Aggregate functions_ compute a single result from a set of input values. The built-in general-purpose aggregate functions are listed in [Table 9.52](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-AGGREGATE-TABLE) and statistical aggregates in [Table 9.53](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-AGGREGATE-STATISTICS-TABLE). The built-in within-group ordered-set aggregate functions are listed in [Table 9.54](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) while the built-in within-group hypothetical-set ones are in [Table 9.55](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-HYPOTHETICAL-TABLE). Grouping operations, which are closely related to aggregate functions, are listed in [Table 9.56](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-GROUPING-TABLE). The special syntax considerations for aggregate functions are explained in [Section 4.2.7](https://www.postgresql.org/docs/11/sql-expressions.html#SYNTAX-AGGREGATES). Consult [Section 2.7](https://www.postgresql.org/docs/11/tutorial-agg.html) for additional introductory information.

#### **Table 9.52. General-Purpose Aggregate Functions**

| Function | Argument Type\(s\) | Return Type | Partial Mode | Description |
| :--- | :--- | :--- | :--- | :--- |
| `array_agg(`_`expression`_\) | any non-array type | array of the argument type | No | input values, including nulls, concatenated into an array |
| `array_agg(`_`expression`_\) | any array type | same as argument data type | No | input arrays concatenated into array of one higher dimension \(inputs must all have same dimensionality, and cannot be empty or NULL\) |
| `avg(`_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, `numeric`, or `interval` | `numeric` for any integer-type argument, `double precision`for a floating-point argument, otherwise the same as the argument data type | Yes | the average \(arithmetic mean\) of all input values |
| `bit_and(`_`expression`_\) | `smallint`, `int`, `bigint`, or `bit` | same as argument data type | Yes | the bitwise AND of all non-null input values, or null if none |
| `bit_or(`_`expression`_\) | `smallint`, `int`, `bigint`, or `bit` | same as argument data type | Yes | the bitwise OR of all non-null input values, or null if none |
| `bool_and(`_`expression`_\) | `bool` | `bool` | Yes | true if all input values are true, otherwise false |
| `bool_or(`_`expression`_\) | `bool` | `bool` | Yes | true if at least one input value is true, otherwise false |
| `count(*)` |  | `bigint` | Yes | number of input rows |
| `count(`_`expression`_\) | any | `bigint` | Yes | number of input rows for which the value of _`expression`_is not null |
| `every(`_`expression`_\) | `bool` | `bool` | Yes | equivalent to `bool_and` |
| `json_agg(`_`expression`_\) | `any` | `json` | No | aggregates values as a JSON array |
| `jsonb_agg(`_`expression`_\) | `any` | `jsonb` | No | aggregates values as a JSON array |
| `json_object_agg(`_`name`_,_`value`_\) | `(any, any)` | `json` | No | aggregates name/value pairs as a JSON object |
| `jsonb_object_agg(`_`name`_,_`value`_\) | `(any, any)` | `jsonb` | No | aggregates name/value pairs as a JSON object |
| `max(`_`expression`_\) | any numeric, string, date/time, network, or enum type, or arrays of these types | same as argument type | Yes | maximum value of _`expression`_ across all input values |
| `min(`_`expression`_\) | any numeric, string, date/time, network, or enum type, or arrays of these types | same as argument type | Yes | minimum value of _`expression`_ across all input values |
| `string_agg(`_`expression`_,_`delimiter`_\) | \(`text`, `text`\) or \(`bytea`, `bytea`\) | same as argument types | No | input values concatenated into a string, separated by delimiter |
| `sum(`_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, `numeric`, `interval`, or `money` | `bigint` for `smallint` or `int` arguments, `numeric` for`bigint` arguments, otherwise the same as the argument data type | Yes | sum of _`expression`_ across all input values |
| `xmlagg(`_`expression`_\) | `xml` | `xml` | No | concatenation of XML values \(see also [Section 9.14.1.7](https://www.postgresql.org/docs/11/functions-xml.html#FUNCTIONS-XML-XMLAGG)\) |

It should be noted that except for `count`, these functions return a null value when no rows are selected. In particular, `sum` of no rows returns null, not zero as one might expect, and `array_agg` returns null rather than an empty array when there are no input rows. The `coalesce` function can be used to substitute zero or an empty array for null when necessary.

Aggregate functions which support _Partial Mode_ are eligible to participate in various optimizations, such as parallel aggregation.

#### Note

Boolean aggregates `bool_and` and `bool_or` correspond to standard SQL aggregates `every` and `any` or `some`. As for `any` and `some`, it seems that there is an ambiguity built into the standard syntax:

```text
SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;
```

Here `ANY` can be considered either as introducing a subquery, or as being an aggregate function, if the subquery returns one row with a Boolean value. Thus the standard name cannot be given to these aggregates.

#### Note

Users accustomed to working with other SQL database management systems might be disappointed by the performance of the `count` aggregate when it is applied to the entire table. A query like:

```text
SELECT count(*) FROM sometable;
```

will require effort proportional to the size of the table: PostgreSQL will need to scan either the entire table or the entirety of an index which includes all rows in the table.

The aggregate functions `array_agg`, `json_agg`, `jsonb_agg`, `json_object_agg`, `jsonb_object_agg`, `string_agg`, and `xmlagg`, as well as similar user-defined aggregate functions, produce meaningfully different result values depending on the order of the input values. This ordering is unspecified by default, but can be controlled by writing an `ORDER BY` clause within the aggregate call, as shown in [Section 4.2.7](https://www.postgresql.org/docs/11/sql-expressions.html#SYNTAX-AGGREGATES). Alternatively, supplying the input values from a sorted subquery will usually work. For example:

```text
SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;
```

Beware that this approach can fail if the outer query level contains additional processing, such as a join, because that might cause the subquery's output to be reordered before the aggregate is computed.

[Table 9.53](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-AGGREGATE-STATISTICS-TABLE) shows aggregate functions typically used in statistical analysis. \(These are separated out merely to avoid cluttering the listing of more-commonly-used aggregates.\) Where the description mentions _`N`_, it means the number of input rows for which all the input expressions are non-null. In all cases, null is returned if the computation is meaningless, for example when _`N`_ is zero.

#### **Table 9.53. Aggregate Functions for Statistics**

| Function | Argument Type | Return Type | Partial Mode | Description |
| :--- | :--- | :--- | :--- | :--- |
| `corr(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | correlation coefficient |
| `covar_pop(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | population covariance |
| `covar_samp(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | sample covariance |
| `regr_avgx(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | average of the independent variable \(`sum(`_`X`_\)/_`N`_\) |
| `regr_avgy(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | average of the dependent variable \(`sum(`_`Y`_\)/_`N`_\) |
| `regr_count(`_`Y`_, _`X`_\) | `double precision` | `bigint` | Yes | number of input rows in which both expressions are nonnull |
| `regr_intercept(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | y-intercept of the least-squares-fit linear equation determined by the \(_`X`_, _`Y`_\) pairs |
| `regr_r2(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | square of the correlation coefficient |
| `regr_slope(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | slope of the least-squares-fit linear equation determined by the \(_`X`_, _`Y`_\) pairs |
| `regr_sxx(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | `sum(`_`X`_^2\) - sum\(_`X`_\)^2/_`N`_ \(“sum of squares” of the independent variable\) |
| `regr_sxy(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | `sum(`_`X`_\*_`Y`_\) - sum\(_`X`_\) \* sum\(_`Y`_\)/_`N`_ \(“sum of products” of independent times dependent variable\) |
| `regr_syy(`_`Y`_, _`X`_\) | `double precision` | `double precision` | Yes | `sum(`_`Y`_^2\) - sum\(_`Y`_\)^2/_`N`_ \(“sum of squares” of the dependent variable\) |
| `stddev(`_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | historical alias for `stddev_samp` |
| `stddev_pop(`_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | population standard deviation of the input values |
| `stddev_samp(`_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | sample standard deviation of the input values |
| `variance`\(_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | historical alias for `var_samp` |
| `var_pop`\(_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | population variance of the input values \(square of the population standard deviation\) |
| `var_samp`\(_`expression`_\) | `smallint`, `int`, `bigint`, `real`, `double precision`, or `numeric` | `double precision` for floating-point arguments, otherwise `numeric` | Yes | sample variance of the input values \(square of the sample standard deviation\) |

[Table 9.54](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) shows some aggregate functions that use the _ordered-set aggregate_ syntax. These functions are sometimes referred to as “inverse distribution” functions.

#### **Table 9.54. Ordered-Set Aggregate Functions**

| Function | Direct Argument Type\(s\) | Aggregated Argument Type\(s\) | Return Type | Partial Mode | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `mode() WITHIN GROUP (ORDER BY`_`sort_expression`_\) |  | any sortable type | same as sort expression | No | returns the most frequent input value \(arbitrarily choosing the first one if there are multiple equally-frequent results\) |
| `percentile_cont(`_`fraction`_\) WITHIN GROUP \(ORDER BY _`sort_expression`_\) | `double precision` | `double precision` or`interval` | same as sort expression | No | continuous percentile: returns a value corresponding to the specified fraction in the ordering, interpolating between adjacent input items if needed |
| `percentile_cont(`_`fractions`_\) WITHIN GROUP \(ORDER BY _`sort_expression`_\) | `double precision[]` | `double precision` or`interval` | array of sort expression's type | No | multiple continuous percentile: returns an array of results matching the shape of the _`fractions`_parameter, with each non-null element replaced by the value corresponding to that percentile |
| `percentile_disc(`_`fraction`_\) WITHIN GROUP \(ORDER BY _`sort_expression`_\) | `double precision` | any sortable type | same as sort expression | No | discrete percentile: returns the first input value whose position in the ordering equals or exceeds the specified fraction |
| `percentile_disc(`_`fractions`_\) WITHIN GROUP \(ORDER BY _`sort_expression`_\) | `double precision[]` | any sortable type | array of sort expression's type | No | multiple discrete percentile: returns an array of results matching the shape of the _`fractions`_parameter, with each non-null element replaced by the input value corresponding to that percentile |

All the aggregates listed in [Table 9.54](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) ignore null values in their sorted input. For those that take a _`fraction`_ parameter, the fraction value must be between 0 and 1; an error is thrown if not. However, a null fraction value simply produces a null result.

Each of the aggregates listed in [Table 9.55](https://www.postgresql.org/docs/11/functions-aggregate.html#FUNCTIONS-HYPOTHETICAL-TABLE) is associated with a window function of the same name defined in [Section 9.21](https://www.postgresql.org/docs/11/functions-window.html). In each case, the aggregate result is the value that the associated window function would have returned for the “hypothetical” row constructed from _`args`_, if such a row had been added to the sorted group of rows computed from the _`sorted_args`_.

#### **Table 9.55. Hypothetical-Set Aggregate Functions**

| Function | Direct Argument Type\(s\) | Aggregated Argument Type\(s\) | Return Type | Partial Mode | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `rank(`_`args`_\) WITHIN GROUP \(ORDER BY _`sorted_args`_\) | `VARIADIC` `"any"` | `VARIADIC` `"any"` | `bigint` | No | rank of the hypothetical row, with gaps for duplicate rows |
| `dense_rank(`_`args`_\) WITHIN GROUP \(ORDER BY_`sorted_args`_\) | `VARIADIC` `"any"` | `VARIADIC` `"any"` | `bigint` | No | rank of the hypothetical row, without gaps |
| `percent_rank(`_`args`_\) WITHIN GROUP \(ORDER BY_`sorted_args`_\) | `VARIADIC` `"any"` | `VARIADIC` `"any"` | `double precision` | No | relative rank of the hypothetical row, ranging from 0 to 1 |
| `cume_dist(`_`args`_\) WITHIN GROUP \(ORDER BY_`sorted_args`_\) | `VARIADIC` `"any"` | `VARIADIC` `"any"` | `double precision` | No | relative rank of the hypothetical row, ranging from 1/_`N`_ to 1 |

For each of these hypothetical-set aggregates, the list of direct arguments given in _`args`_ must match the number and types of the aggregated arguments given in _`sorted_args`_. Unlike most built-in aggregates, these aggregates are not strict, that is they do not drop input rows containing nulls. Null values sort according to the rule specified in the `ORDER BY` clause.

#### **Table 9.56. Grouping Operations**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `GROUPING(`_`args...`_\) | `integer` | Integer bit mask indicating which arguments are not being included in the current grouping set |

Grouping operations are used in conjunction with grouping sets \(see [Section 7.2.4](https://www.postgresql.org/docs/11/queries-table-expressions.html#QUERIES-GROUPING-SETS)\) to distinguish result rows. The arguments to the `GROUPING` operation are not actually evaluated, but they must match exactly expressions given in the `GROUP BY` clause of the associated query level. Bits are assigned with the rightmost argument being the least-significant bit; each bit is 0 if the corresponding expression is included in the grouping criteria of the grouping set generating the result row, and 1 if it is not. For example:

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

