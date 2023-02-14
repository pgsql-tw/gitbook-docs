# 9.2. 比較函式及運算子

The usual comparison operators are available, as shown in [Table 9.1](https://www.postgresql.org/docs/15/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE).

#### **Table 9.1. Comparison Operators**

| Operator                                   | Description              |
| ------------------------------------------ | ------------------------ |
| _`datatype`_ `<` _`datatype`_ → `boolean`  | Less than                |
| _`datatype`_ `>` _`datatype`_ → `boolean`  | Greater than             |
| _`datatype`_ `<=` _`datatype`_ → `boolean` | Less than or equal to    |
| _`datatype`_ `>=` _`datatype`_ → `boolean` | Greater than or equal to |
| _`datatype`_ `=` _`datatype`_ → `boolean`  | Equal                    |
| _`datatype`_ `<>` _`datatype`_ → `boolean` | Not equal                |
| _`datatype`_ `!=` _`datatype`_ → `boolean` | Not equal                |

#### Note

`<>` is the standard SQL notation for “not equal”. `!=` is an alias, which is converted to `<>` at a very early stage of parsing. Hence, it is not possible to implement `!=` and `<>` operators that do different things.

These comparison operators are available for all built-in data types that have a natural ordering, including numeric, string, and date/time types. In addition, arrays, composite types, and ranges can be compared if their component data types are comparable.

It is usually possible to compare values of related data types as well; for example `integer` `>` `bigint` will work. Some cases of this sort are implemented directly by “cross-type” comparison operators, but if no such operator is available, the parser will coerce the less-general type to the more-general type and apply the latter's comparison operator.

As shown above, all comparison operators are binary operators that return values of type `boolean`. Thus, expressions like `1 < 2 < 3` are not valid (because there is no `<` operator to compare a Boolean value with `3`). Use the `BETWEEN` predicates shown below to perform range tests.

There are also some comparison predicates, as shown in [Table 9.2](https://www.postgresql.org/docs/15/functions-comparison.html#FUNCTIONS-COMPARISON-PRED-TABLE). These behave much like operators, but have special syntax mandated by the SQL standard.

#### **Table 9.2. Comparison Predicates**

| <p>Predicate</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><em><code>datatype</code></em> <code>BETWEEN</code> <em><code>datatype</code></em> <code>AND</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Between (inclusive of the range endpoints).</p><p><code>2 BETWEEN 1 AND 3</code> → <code>t</code></p><p><code>2 BETWEEN 3 AND 1</code> → <code>f</code></p>                                                     |
| <p><em><code>datatype</code></em> <code>NOT BETWEEN</code> <em><code>datatype</code></em> <code>AND</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Not between (the negation of <code>BETWEEN</code>).</p><p><code>2 NOT BETWEEN 1 AND 3</code> → <code>f</code></p>                                                                                           |
| <p><em><code>datatype</code></em> <code>BETWEEN SYMMETRIC</code> <em><code>datatype</code></em> <code>AND</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Between, after sorting the two endpoint values.</p><p><code>2 BETWEEN SYMMETRIC 3 AND 1</code> → <code>t</code></p>                                                                                   |
| <p><em><code>datatype</code></em> <code>NOT BETWEEN SYMMETRIC</code> <em><code>datatype</code></em> <code>AND</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Not between, after sorting the two endpoint values.</p><p><code>2 NOT BETWEEN SYMMETRIC 3 AND 1</code> → <code>f</code></p>                                                                       |
| <p><em><code>datatype</code></em> <code>IS DISTINCT FROM</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Not equal, treating null as a comparable value.</p><p><code>1 IS DISTINCT FROM NULL</code> → <code>t</code> (rather than <code>NULL</code>)</p><p><code>NULL IS DISTINCT FROM NULL</code> → <code>f</code> (rather than <code>NULL</code>)</p>         |
| <p><em><code>datatype</code></em> <code>IS NOT DISTINCT FROM</code> <em><code>datatype</code></em> → <code>boolean</code></p><p>Equal, treating null as a comparable value.</p><p><code>1 IS NOT DISTINCT FROM NULL</code> → <code>f</code> (rather than <code>NULL</code>)</p><p><code>NULL IS NOT DISTINCT FROM NULL</code> → <code>t</code> (rather than <code>NULL</code>)</p> |
| <p><em><code>datatype</code></em> <code>IS NULL</code> → <code>boolean</code></p><p>Test whether value is null.</p><p><code>1.5 IS NULL</code> → <code>f</code></p>                                                                                                                                                                                                                |
| <p><em><code>datatype</code></em> <code>IS NOT NULL</code> → <code>boolean</code></p><p>Test whether value is not null.</p><p><code>'null' IS NOT NULL</code> → <code>t</code></p>                                                                                                                                                                                                 |
| <p><em><code>datatype</code></em> <code>ISNULL</code> → <code>boolean</code></p><p>Test whether value is null (nonstandard syntax).</p>                                                                                                                                                                                                                                            |
| <p><em><code>datatype</code></em> <code>NOTNULL</code> → <code>boolean</code></p><p>Test whether value is not null (nonstandard syntax).</p>                                                                                                                                                                                                                                       |
| <p><code>boolean</code> <code>IS TRUE</code> → <code>boolean</code></p><p>Test whether boolean expression yields true.</p><p><code>true IS TRUE</code> → <code>t</code></p><p><code>NULL::boolean IS TRUE</code> → <code>f</code> (rather than <code>NULL</code>)</p>                                                                                                              |
| <p><code>boolean</code> <code>IS NOT TRUE</code> → <code>boolean</code></p><p>Test whether boolean expression yields false or unknown.</p><p><code>true IS NOT TRUE</code> → <code>f</code></p><p><code>NULL::boolean IS NOT TRUE</code> → <code>t</code> (rather than <code>NULL</code>)</p>                                                                                      |
| <p><code>boolean</code> <code>IS FALSE</code> → <code>boolean</code></p><p>Test whether boolean expression yields false.</p><p><code>true IS FALSE</code> → <code>f</code></p><p><code>NULL::boolean IS FALSE</code> → <code>f</code> (rather than <code>NULL</code>)</p>                                                                                                          |
| <p><code>boolean</code> <code>IS NOT FALSE</code> → <code>boolean</code></p><p>Test whether boolean expression yields true or unknown.</p><p><code>true IS NOT FALSE</code> → <code>t</code></p><p><code>NULL::boolean IS NOT FALSE</code> → <code>t</code> (rather than <code>NULL</code>)</p>                                                                                    |
| <p><code>boolean</code> <code>IS UNKNOWN</code> → <code>boolean</code></p><p>Test whether boolean expression yields unknown.</p><p><code>true IS UNKNOWN</code> → <code>f</code></p><p><code>NULL::boolean IS UNKNOWN</code> → <code>t</code> (rather than <code>NULL</code>)</p>                                                                                                  |
| <p><code>boolean</code> <code>IS NOT UNKNOWN</code> → <code>boolean</code></p><p>Test whether boolean expression yields true or false.</p><p><code>true IS NOT UNKNOWN</code> → <code>t</code></p><p><code>NULL::boolean IS NOT UNKNOWN</code> → <code>f</code> (rather than <code>NULL</code>)</p>                                                                                |

The `BETWEEN` predicate simplifies range tests:

```
a BETWEEN x AND y
```

is equivalent to

```
a >= x AND a <= y
```

Notice that `BETWEEN` treats the endpoint values as included in the range. `BETWEEN SYMMETRIC` is like `BETWEEN` except there is no requirement that the argument to the left of `AND` be less than or equal to the argument on the right. If it is not, those two arguments are automatically swapped, so that a nonempty range is always implied.

The various variants of `BETWEEN` are implemented in terms of the ordinary comparison operators, and therefore will work for any data type(s) that can be compared.

#### Note

The use of `AND` in the `BETWEEN` syntax creates an ambiguity with the use of `AND` as a logical operator. To resolve this, only a limited set of expression types are allowed as the second argument of a `BETWEEN` clause. If you need to write a more complex sub-expression in `BETWEEN`, write parentheses around the sub-expression.

Ordinary comparison operators yield null (signifying “unknown”), not true or false, when either input is null. For example, `7 = NULL` yields null, as does `7 <> NULL`. When this behavior is not suitable, use the `IS [ NOT ] DISTINCT FROM` predicates:

```
a IS DISTINCT FROM b
a IS NOT DISTINCT FROM b
```

For non-null inputs, `IS DISTINCT FROM` is the same as the `<>` operator. However, if both inputs are null it returns false, and if only one input is null it returns true. Similarly, `IS NOT DISTINCT FROM` is identical to `=` for non-null inputs, but it returns true when both inputs are null, and false when only one input is null. Thus, these predicates effectively act as though null were a normal data value, rather than “unknown”.

To check whether a value is or is not null, use the predicates:

```
expression IS NULL
expression IS NOT NULL
```

or the equivalent, but nonstandard, predicates:

```
expression ISNULL
expression NOTNULL
```

Do _not_ write _`expression`_` ``= NULL` because `NULL` is not “equal to” `NULL`. (The null value represents an unknown value, and it is not known whether two unknown values are equal.)

#### Tip

Some applications might expect that _`expression`_` ``= NULL` returns true if _`expression`_ evaluates to the null value. It is highly recommended that these applications be modified to comply with the SQL standard. However, if that cannot be done the [transform\_null\_equals](https://www.postgresql.org/docs/15/runtime-config-compatible.html#GUC-TRANSFORM-NULL-EQUALS) configuration variable is available. If it is enabled, PostgreSQL will convert `x = NULL` clauses to `x IS NULL`.

If the _`expression`_ is row-valued, then `IS NULL` is true when the row expression itself is null or when all the row's fields are null, while `IS NOT NULL` is true when the row expression itself is non-null and all the row's fields are non-null. Because of this behavior, `IS NULL` and `IS NOT NULL` do not always return inverse results for row-valued expressions; in particular, a row-valued expression that contains both null and non-null fields will return false for both tests. In some cases, it may be preferable to write _`row`_ `IS DISTINCT FROM NULL` or _`row`_ `IS NOT DISTINCT FROM NULL`, which will simply check whether the overall row value is null without any additional tests on the row fields.

Boolean values can also be tested using the predicates

```
boolean_expression IS TRUE
boolean_expression IS NOT TRUE
boolean_expression IS FALSE
boolean_expression IS NOT FALSE
boolean_expression IS UNKNOWN
boolean_expression IS NOT UNKNOWN
```

These will always return true or false, never a null value, even when the operand is null. A null input is treated as the logical value “unknown”. Notice that `IS UNKNOWN` and `IS NOT UNKNOWN` are effectively the same as `IS NULL` and `IS NOT NULL`, respectively, except that the input expression must be of Boolean type.

Some comparison-related functions are also available, as shown in [Table 9.3](https://www.postgresql.org/docs/15/functions-comparison.html#FUNCTIONS-COMPARISON-FUNC-TABLE).

#### **Table 9.3. Comparison Functions**

| <p>Function</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>num_nonnulls</code> ( <code>VARIADIC</code> <code>"any"</code> ) → <code>integer</code></p><p>Returns the number of non-null arguments.</p><p><code>num_nonnulls(1, NULL, 2)</code> → <code>2</code></p> |
| <p><code>num_nulls</code> ( <code>VARIADIC</code> <code>"any"</code> ) → <code>integer</code></p><p>Returns the number of null arguments.</p><p><code>num_nulls(1, NULL, 2)</code> → <code>1</code></p>           |

\
