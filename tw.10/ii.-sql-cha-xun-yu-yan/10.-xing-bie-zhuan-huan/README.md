# 10. 型別轉換

SQLstatements can, intentionally or not, require the mixing of different data types in the same expression.PostgreSQLhas extensive facilities for evaluating mixed-type expressions.

In many cases a user does not need to understand the details of the type conversion mechanism. However, implicit conversions done byPostgreSQLcan affect the results of a query. When necessary, these results can be tailored by using\_explicit\_type conversion.

This chapter introduces thePostgreSQLtype conversion mechanisms and conventions. Refer to the relevant sections in[Chapter 8](https://www.postgresql.org/docs/10/static/datatype.html)and[Chapter 9](https://www.postgresql.org/docs/10/static/functions.html)for more information on specific data types and allowed functions and operators.

