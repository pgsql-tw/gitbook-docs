## 42.3. Data Values in PL/Tcl [#](#PLTCL-DATA)

The argument values supplied to a PL/Tcl function's code are simply
the input arguments converted to text form (just as if they had been
displayed by a `SELECT` statement). Conversely, the
`return` and `return_next` commands will accept
any string that is acceptable input format for the function's declared
result type, or for the specified column of a composite result type.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-data.html)（英文原文，待翻譯）
