## 36.4. User-Defined Procedures [#](#XPROC)

<a id="id-1.8.3.7.2"></a>

A procedure is a database object similar to a function.
The key differences are:

* Procedures are defined with
  the [`CREATE
  PROCEDURE`](../../reference/sql-commands/sql-createprocedure.md) command, not `CREATE
  FUNCTION`.
* Procedures do not return a function value; hence `CREATE
  PROCEDURE` lacks a `RETURNS` clause.
  However, procedures can instead return data to their callers via
  output parameters.
* While a function is called as part of a query or DML command, a
  procedure is called in isolation using
  the [`CALL`](../../reference/sql-commands/sql-call.md) command.
* A procedure can commit or roll back transactions during its
  execution (then automatically beginning a new transaction), so long
  as the invoking `CALL` command is not part of an
  explicit transaction block. A function cannot do that.
* Certain function attributes, such as strictness, don't apply to
  procedures. Those attributes control how the function is
  used in a query, which isn't relevant to procedures.

The explanations in the following sections about how to define
user-defined functions apply to procedures as well, except for the
points made above.

Collectively, functions and procedures are also known
as *routines*<a id="id-1.8.3.7.5.2"></a>.
There are commands such as [`ALTER ROUTINE`](../../reference/sql-commands/sql-alterroutine.md)
and [`DROP ROUTINE`](../../reference/sql-commands/sql-droproutine.md) that can operate on functions and
procedures without having to know which kind it is. Note, however, that
there is no `CREATE ROUTINE` command.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xproc.html)（英文原文，待翻譯）
