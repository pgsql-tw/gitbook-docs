## Chapter 10. Type Conversion

**Table of Contents**

[10.1. Overview](typeconv-overview.md)

[10.2. Operators](typeconv-oper.md)

[10.3. Functions](typeconv-func.md)

[10.4. Value Storage](typeconv-query.md)

[10.5. `UNION`, `CASE`, and Related Constructs](typeconv-union-case.md)

[10.6. `SELECT` Output Columns](typeconv-select.md)

<a id="id-1.5.9.2"></a>

SQL statements can, intentionally or not, require
the mixing of different data types in the same expression.
PostgreSQL has extensive facilities for
evaluating mixed-type expressions.

In many cases a user does not need
to understand the details of the type conversion mechanism.
However, implicit conversions done by PostgreSQL
can affect the results of a query. When necessary, these results
can be tailored by using *explicit* type conversion.

This chapter introduces the PostgreSQL
type conversion mechanisms and conventions.
Refer to the relevant sections in [Chapter 8](../datatype/README.md) and [Chapter 9](../functions/README.md)
for more information on specific data types and allowed functions and
operators.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv.html)（英文原文，待翻譯）
