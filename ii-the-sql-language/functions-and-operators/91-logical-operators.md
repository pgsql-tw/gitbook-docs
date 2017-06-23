# 9.1. 邏輯運算子[^1]

The usual logical operators are available:

| `AND` |
| :--- |
| `OR` |
| `NOT` |

SQLuses a three-valued logic system with true, false, and`null`, which represents“unknown”. Observe the following truth tables:

| _`a`_ | _`b`_ | _`a`_ | AND | _`b`_ | _`a`_ | OR | _`b`_ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|  |  |  |  | TRUE | TRUE | TRUE | TRUE |
|  |  |  |  | TRUE | FALSE | FALSE | TRUE |
|  |  |  |  | TRUE | NULL | NULL | TRUE |
|  |  |  |  | FALSE | FALSE | FALSE | FALSE |
|  |  |  |  | FALSE | NULL | FALSE | NULL |
|  |  |  |  | NULL | NULL | NULL | NULL |

| _`a`_ | NOT | _`a`_ |
| :--- | :--- | :--- |
|  | TRUE | FALSE |
|  | FALSE | TRUE |
|  | NULL | NULL |

The operators`AND`and`OR`are commutative, that is, you can switch the left and right operand without affecting the result. But see[Section 4.2.14](https://www.postgresql.org/docs/10/static/sql-expressions.html#syntax-express-eval)for more information about the order of evaluation of subexpressions.

---



[^1]:  [PostgreSQL: Documentation: 10: 9.1. Logical Operators](https://www.postgresql.org/docs/10/static/functions-logical.html)

