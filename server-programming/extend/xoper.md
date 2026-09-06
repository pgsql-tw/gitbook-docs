## 36.14. User-Defined Operators [#](#XOPER)

<a id="id-1.8.3.17.2"></a>

Every operator is “syntactic sugar” for a call to an
underlying function that does the real work; so you must
first create the underlying function before you can create
the operator. However, an operator is *not merely*
syntactic sugar, because it carries additional information
that helps the query planner optimize queries that use the
operator. The next section will be devoted to explaining
that additional information.

PostgreSQL supports prefix
and infix operators. Operators can be
overloaded;<a id="id-1.8.3.17.4.2"></a>
that is, the same operator name can be used for different operators
that have different numbers and types of operands. When a query is
executed, the system determines the operator to call from the
number and types of the provided operands.

Here is an example of creating an operator for adding two complex
numbers. We assume we've already created the definition of type
`complex` (see [Section 36.13](xtypes.md)). First we need a
function that does the work, then we can define the operator:

```

CREATE FUNCTION complex_add(complex, complex)
    RETURNS complex
    AS 'filename', 'complex_add'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR + (
    leftarg = complex,
    rightarg = complex,
    function = complex_add,
    commutator = +
);
```

Now we could execute a query like this:

```

SELECT (a + b) AS c FROM test_complex;

        c
-----------------
 (5.2,6.05)
 (133.42,144.95)
```

We've shown how to create a binary operator here. To create a prefix
operator, just omit the `leftarg`.
The `function`
clause and the argument clauses are the only required items in
`CREATE OPERATOR`. The `commutator`
clause shown in the example is an optional hint to the query
optimizer. Further details about `commutator` and other
optimizer hints appear in the next section.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xoper.html)（英文原文，待翻譯）
