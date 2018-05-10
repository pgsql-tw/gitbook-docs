# 37.3. 使用者自訂函數

PostgreSQL 提供了四種形態的函數：

* 查詢語言函數（用 SQL 語言撰寫的函數）（[第 37.4 節](xfunc-sql.md)）
* procedural language functions \(functions written in, for example, PL/pgSQL or PL/Tcl\) \([Section 37.7](https://www.postgresql.org/docs/10/static/xfunc-pl.html)\)
* internal functions \([Section 37.8](https://www.postgresql.org/docs/10/static/xfunc-internal.html)\)
* C-language functions \([Section 37.9](https://www.postgresql.org/docs/10/static/xfunc-c.html)\)

Every kind of function can take base types, composite types, or combinations of these as arguments \(parameters\). In addition, every kind of function can return a base type or a composite type. Functions can also be defined to return sets of base or composite values.

Many kinds of functions can take or return certain pseudo-types \(such as polymorphic types\), but the available facilities vary. Consult the description of each kind of function for more details.

It's easiest to define SQL functions, so we'll start by discussing those. Most of the concepts presented for SQL functions will carry over to the other types of functions.

Throughout this chapter, it can be useful to look at the reference page of the [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html) command to understand the examples better. Some examples from this chapter can be found in `funcs.sql` and `funcs.c` in the `src/tutorial` directory in the PostgreSQL source distribution.

