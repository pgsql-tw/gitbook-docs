# 9.2. 比較函式及運算子

The usual comparison operators are available, as shown in [Table 9.1](https://www.postgresql.org/docs/12/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE).

## **Table 9.1. Comparison Operators**

| Operator | Description |
| :--- | :--- |
| `<` | less than |
| `>` | greater than |
| `<=` | less than or equal to |
| `>=` | greater than or equal to |
| `=` | equal |
| `<>` or `!=` | not equal |

## Note

The `!=` operator is converted to `<>` in the parser stage. It is not possible to implement `!=` and `<>` operators that do different things.

Comparison operators are available for all relevant data types. All comparison operators are binary operators that return values of type `boolean`; expressions like `1 < 2 < 3` are not valid \(because there is no `<` operator to compare a Boolean value with `3`\).

There are also some comparison predicates, as shown in [Table 9.2](https://www.postgresql.org/docs/12/functions-comparison.html#FUNCTIONS-COMPARISON-PRED-TABLE). These behave much like operators, but have special syntax mandated by the SQL standard.

## **Table 9.2. Comparison Predicates**

| Predicate | Description |
| :--- | :--- |
| _`a`_ `BETWEEN` _`x`_ `AND` _`y`_ | between |
| _`a`_ `NOT BETWEEN` _`x`_ `AND` _`y`_ | not between |
| _`a`_ `BETWEEN SYMMETRIC` _`x`_ `AND` _`y`_ | between, after sorting the comparison values |
| _`a`_ `NOT BETWEEN SYMMETRIC` _`x`_ `AND` _`y`_ | not between, after sorting the comparison values |
| _`a`_ `IS DISTINCT FROM` _`b`_ | not equal, treating null like an ordinary value |
| _`a`_ `IS NOT DISTINCT FROM` _`b`_ | equal, treating null like an ordinary value |
| _`expression`_ `IS NULL` | is null |
| _`expression`_ `IS NOT NULL` | is not null |
| _`expression`_ `ISNULL` | is null \(nonstandard syntax\) |
| _`expression`_ `NOTNULL` | is not null \(nonstandard syntax\) |
| _`boolean_expression`_ `IS TRUE` | is true |
| _`boolean_expression`_ `IS NOT TRUE` | is false or unknown |
| _`boolean_expression`_ `IS FALSE` | is false |
| _`boolean_expression`_ `IS NOT FALSE` | is true or unknown |
| _`boolean_expression`_ `IS UNKNOWN` | is unknown |
| _`boolean_expression`_ `IS NOT UNKNOWN` | is true or false |

The `BETWEEN` predicate simplifies range tests:

```text
a BETWEEN x AND y
```

is equivalent to

```text
a >= x AND a <= y
```

Notice that `BETWEEN` treats the endpoint values as included in the range. `NOT BETWEEN` does the opposite comparison:

```text
a NOT BETWEEN x AND y
```

is equivalent to

```text
a < x OR a > y
```

`BETWEEN SYMMETRIC` is like `BETWEEN` except there is no requirement that the argument to the left of `AND` be less than or equal to the argument on the right. If it is not, those two arguments are automatically swapped, so that a nonempty range is always implied.

Ordinary comparison operators yield null \(signifying “unknown”\), not true or false, when either input is null. For example, `7 = NULL` yields null, as does `7 <> NULL`. When this behavior is not suitable, use the `IS [ NOT ] DISTINCT FROM` predicates:

```text
a IS DISTINCT FROM b
a IS NOT DISTINCT FROM b
```

For non-null inputs, `IS DISTINCT FROM` is the same as the `<>` operator. However, if both inputs are null it returns false, and if only one input is null it returns true. Similarly, `IS NOT DISTINCT FROM` is identical to `=` for non-null inputs, but it returns true when both inputs are null, and false when only one input is null. Thus, these predicates effectively act as though null were a normal data value, rather than “unknown”.

To check whether a value is or is not null, use the predicates:

```text
expression IS NULL
expression IS NOT NULL
```

or the equivalent, but nonstandard, predicates:

```text
expression ISNULL
expression NOTNULL
```

Do _not_ write _`expression`_ = NULL because `NULL` is not “equal to” `NULL`. \(The null value represents an unknown value, and it is not known whether two unknown values are equal.\)

## Tip

Some applications might expect that _`expression`_ = NULL returns true if _`expression`_ evaluates to the null value. It is highly recommended that these applications be modified to comply with the SQL standard. However, if that cannot be done the [transform\_null\_equals](https://www.postgresql.org/docs/12/runtime-config-compatible.html#GUC-TRANSFORM-NULL-EQUALS) configuration variable is available. If it is enabled, PostgreSQL will convert `x = NULL` clauses to `x IS NULL`.

If the _`expression`_ is row-valued, then `IS NULL` is true when the row expression itself is null or when all the row's fields are null, while `IS NOT NULL` is true when the row expression itself is non-null and all the row's fields are non-null. Because of this behavior, `IS NULL` and `IS NOT NULL` do not always return inverse results for row-valued expressions; in particular, a row-valued expression that contains both null and non-null fields will return false for both tests. In some cases, it may be preferable to write _`row`_ `IS DISTINCT FROM NULL` or _`row`_ `IS NOT DISTINCT FROM NULL`, which will simply check whether the overall row value is null without any additional tests on the row fields.

Boolean values can also be tested using the predicates

```text
boolean_expression IS TRUE
boolean_expression IS NOT TRUE
boolean_expression IS FALSE
boolean_expression IS NOT FALSE
boolean_expression IS UNKNOWN
boolean_expression IS NOT UNKNOWN
```

These will always return true or false, never a null value, even when the operand is null. A null input is treated as the logical value “unknown”. Notice that `IS UNKNOWN` and `IS NOT UNKNOWN` are effectively the same as `IS NULL` and `IS NOT NULL`, respectively, except that the input expression must be of Boolean type.

Some comparison-related functions are also available, as shown in [Table 9.3](https://www.postgresql.org/docs/12/functions-comparison.html#FUNCTIONS-COMPARISON-FUNC-TABLE).

## **Table 9.3. Comparison Functions**

| Function | Description | Example | Example Result |
| :--- | :--- | :--- | :--- |
| `num_nonnulls(VARIADIC "any")` | returns the number of non-null arguments | `num_nonnulls(1, NULL, 2)` | `2` |
| `num_nulls(VARIADIC "any")` | returns the number of null arguments | `num_nulls(1, NULL, 2)` | `1` |

