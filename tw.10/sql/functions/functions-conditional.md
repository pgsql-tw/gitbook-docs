# 9.17. 條件表示式

This section describes the SQL-compliant conditional expressions available in PostgreSQL.

#### Tip

If your needs go beyond the capabilities of these conditional expressions, you might want to consider writing a stored procedure in a more expressive programming language.

#### 9.17.1. `CASE`

The SQL `CASE` expression is a generic conditional expression, similar to if/else statements in other programming languages:

```text
CASE WHEN condition THEN result
     [WHEN ...]
     [ELSE result]
END
```

`CASE` clauses can be used wherever an expression is valid. Each _`condition`_ is an expression that returns a `boolean` result. If the condition's result is true, the value of the `CASE` expression is the _`result`_ that follows the condition, and the remainder of the `CASE` expression is not processed. If the condition's result is not true, any subsequent `WHEN` clauses are examined in the same manner. If no `WHEN` _`condition`_ yields true, the value of the `CASE`expression is the _`result`_ of the `ELSE` clause. If the `ELSE` clause is omitted and no condition is true, the result is null.

An example:

```text
SELECT * FROM test;

 a
---
 1
 2
 3


SELECT a,
       CASE WHEN a=1 THEN 'one'
            WHEN a=2 THEN 'two'
            ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

The data types of all the _`result`_ expressions must be convertible to a single output type. See [Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html) for more details.

There is a “simple” form of `CASE` expression that is a variant of the general form above:

```text
CASE expression
    WHEN value THEN result
    [WHEN ...]
    [ELSE result]
END
```

The first _`expression`_ is computed, then compared to each of the _`value`_ expressions in the `WHEN` clauses until one is found that is equal to it. If no match is found, the _`result`_ of the `ELSE` clause \(or a null value\) is returned. This is similar to the `switch` statement in C.

The example above can be written using the simple `CASE` syntax:

```text
SELECT a,
       CASE a WHEN 1 THEN 'one'
              WHEN 2 THEN 'two'
              ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

A `CASE` expression does not evaluate any subexpressions that are not needed to determine the result. For example, this is a possible way of avoiding a division-by-zero failure:

```text
SELECT ... WHERE CASE WHEN x <> 0 THEN y/x > 1.5 ELSE false END;
```

#### Note

As described in [Section 4.2.14](https://www.postgresql.org/docs/10/static/sql-expressions.html#SYNTAX-EXPRESS-EVAL), there are various situations in which subexpressions of an expression are evaluated at different times, so that the principle that “`CASE` evaluates only necessary subexpressions” is not ironclad. For example a constant `1/0` subexpression will usually result in a division-by-zero failure at planning time, even if it's within a `CASE` arm that would never be entered at run time.

#### 9.17.2. `COALESCE`

```text
COALESCE(value [, ...])
```

The `COALESCE` function returns the first of its arguments that is not null. Null is returned only if all arguments are null. It is often used to substitute a default value for null values when data is retrieved for display, for example:

```text
SELECT COALESCE(description, short_description, '(none)') ...
```

This returns `description` if it is not null, otherwise `short_description` if it is not null, otherwise `(none)`.

Like a `CASE` expression, `COALESCE` only evaluates the arguments that are needed to determine the result; that is, arguments to the right of the first non-null argument are not evaluated. This SQL-standard function provides capabilities similar to `NVL` and `IFNULL`, which are used in some other database systems.

#### 9.17.3. `NULLIF`

```text
NULLIF(value1, value2)
```

The `NULLIF` function returns a null value if _`value1`_ equals _`value2`_; otherwise it returns _`value1`_. This can be used to perform the inverse operation of the `COALESCE` example given above:

```text
SELECT NULLIF(value, '(none)') ...
```

In this example, if `value` is `(none)`, null is returned, otherwise the value of `value` is returned.

#### 9.17.4. `GREATEST` and `LEAST`

```text
GREATEST(value [, ...])
```

```text
LEAST(value [, ...])
```

The `GREATEST` and `LEAST` functions select the largest or smallest value from a list of any number of expressions. The expressions must all be convertible to a common data type, which will be the type of the result \(see [Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html) for details\). NULL values in the list are ignored. The result will be NULL only if all the expressions evaluate to NULL.

Note that `GREATEST` and `LEAST` are not in the SQL standard, but are a common extension. Some other databases make them return NULL if any argument is NULL, rather than only when all are NULL.

