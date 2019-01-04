---
description: 版本：11
---

# 38.4. User-defined Procedures

A procedure is a database object similar to a function. The difference is that a procedure does not return a value, so there is no return type declaration. While a function is called as part of a query or DML command, a procedure is called explicitly using the [CALL](https://www.postgresql.org/docs/11/sql-call.html) statement.

The explanations on how to define user-defined functions in the rest of this chapter apply to procedures as well, except that the [CREATE PROCEDURE](https://www.postgresql.org/docs/11/sql-createprocedure.html) command is used instead, there is no return type, and some other features such as strictness don't apply.

Collectively, functions and procedures are also known as _routines_. There are commands such as [ALTER ROUTINE](https://www.postgresql.org/docs/11/sql-alterroutine.html) and [DROP ROUTINE](https://www.postgresql.org/docs/11/sql-droproutine.html) that can operate on functions and procedures without having to know which kind it is. Note, however, that there is no `CREATE ROUTINE` command.

