# 42.4. Expressions

All expressions used in PL/pgSQL statements are processed using the server's main SQL executor. For example, when you write a PL/pgSQL statement like

```text
IF expression THEN ...
```

PL/pgSQL will evaluate the expression by feeding a query like

```text
SELECT expression
```

to the main SQL engine. While forming the `SELECT` command, any occurrences of PL/pgSQL variable names are replaced by parameters, as discussed in detail in [Section 42.11.1](https://www.postgresql.org/docs/13/plpgsql-implementation.html#PLPGSQL-VAR-SUBST). This allows the query plan for the `SELECT` to be prepared just once and then reused for subsequent evaluations with different values of the variables. Thus, what really happens on first use of an expression is essentially a `PREPARE` command. For example, if we have declared two integer variables `x` and `y`, and we write

```text
IF x < y THEN ...
```

what happens behind the scenes is equivalent to

```text
PREPARE statement_name(integer, integer) AS SELECT $1 < $2;
```

and then this prepared statement is `EXECUTE`d for each execution of the `IF` statement, with the current values of the PL/pgSQL variables supplied as parameter values. Normally these details are not important to a PL/pgSQL user, but they are useful to know when trying to diagnose a problem. More information appears in [Section 42.11.2](https://www.postgresql.org/docs/13/plpgsql-implementation.html#PLPGSQL-PLAN-CACHING).

