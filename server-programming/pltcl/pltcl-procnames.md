## 42.12. Tcl Procedure Names [#](#PLTCL-PROCNAMES)

In PostgreSQL, the same function name can be used for
different function definitions if the functions are placed in different
schemas, or if the number of arguments or their types
differ. Tcl, however, requires all procedure names to be distinct.
PL/Tcl deals with this by including the argument type names in the
internal Tcl procedure name, and then appending the function's object
ID (OID) to the internal Tcl procedure name if necessary to make it
different from the names of all previously-loaded functions in the
same Tcl interpreter. Thus,
PostgreSQL functions with the same name
and different argument types will be different Tcl procedures, too. This
is not normally a concern for a PL/Tcl programmer, but it might be visible
when debugging.

For this reason among others, a PL/Tcl function cannot call another one
directly (that is, within Tcl). If you need to do that, you must go
through SQL, using `spi_exec` or a related command.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-procnames.html)（英文原文，待翻譯）
