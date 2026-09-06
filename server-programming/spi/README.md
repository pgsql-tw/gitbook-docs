## Chapter 45. Server Programming Interface

**Table of Contents**

[45.1. Interface Functions](spi-interface.md)
:   [SPI_connect](spi-spi-connect.md) — connect a C function to the SPI manager

    [SPI_finish](spi-spi-finish.md) — disconnect a C function from the SPI manager

    [SPI_execute](spi-spi-execute.md) — execute a command

    [SPI_exec](spi-spi-exec.md) — execute a read/write command

    [SPI_execute_extended](spi-spi-execute-extended.md) — execute a command with out-of-line parameters

    [SPI_execute_with_args](spi-spi-execute-with-args.md) — execute a command with out-of-line parameters

    [SPI_prepare](spi-spi-prepare.md) — prepare a statement, without executing it yet

    [SPI_prepare_cursor](spi-spi-prepare-cursor.md) — prepare a statement, without executing it yet

    [SPI_prepare_extended](spi-spi-prepare-extended.md) — prepare a statement, without executing it yet

    [SPI_prepare_params](spi-spi-prepare-params.md) — prepare a statement, without executing it yet

    [SPI_getargcount](spi-spi-getargcount.md) — return the number of arguments needed by a statement prepared by `SPI_prepare`

    [SPI_getargtypeid](spi-spi-getargtypeid.md) — return the data type OID for an argument of a statement prepared by `SPI_prepare`

    [SPI_is_cursor_plan](spi-spi-is-cursor-plan.md) — return `true` if a statement prepared by `SPI_prepare` can be used with `SPI_cursor_open`

    [SPI_execute_plan](spi-spi-execute-plan.md) — execute a statement prepared by `SPI_prepare`

    [SPI_execute_plan_extended](spi-spi-execute-plan-extended.md) — execute a statement prepared by `SPI_prepare`

    [SPI_execute_plan_with_paramlist](spi-spi-execute-plan-with-paramlist.md) — execute a statement prepared by `SPI_prepare`

    [SPI_execp](spi-spi-execp.md) — execute a statement in read/write mode

    [SPI_cursor_open](spi-spi-cursor-open.md) — set up a cursor using a statement created with `SPI_prepare`

    [SPI_cursor_open_with_args](spi-spi-cursor-open-with-args.md) — set up a cursor using a query and parameters

    [SPI_cursor_open_with_paramlist](spi-spi-cursor-open-with-paramlist.md) — set up a cursor using parameters

    [SPI_cursor_parse_open](spi-spi-cursor-parse-open.md) — set up a cursor using a query string and parameters

    [SPI_cursor_find](spi-spi-cursor-find.md) — find an existing cursor by name

    [SPI_cursor_fetch](spi-spi-cursor-fetch.md) — fetch some rows from a cursor

    [SPI_cursor_move](spi-spi-cursor-move.md) — move a cursor

    [SPI_scroll_cursor_fetch](spi-spi-scroll-cursor-fetch.md) — fetch some rows from a cursor

    [SPI_scroll_cursor_move](spi-spi-scroll-cursor-move.md) — move a cursor

    [SPI_cursor_close](spi-spi-cursor-close.md) — close a cursor

    [SPI_keepplan](spi-spi-keepplan.md) — save a prepared statement

    [SPI_saveplan](spi-spi-saveplan.md) — save a prepared statement

    [SPI_register_relation](spi-spi-register-relation.md) — make an ephemeral named relation available by name in SPI queries

    [SPI_unregister_relation](spi-spi-unregister-relation.md) — remove an ephemeral named relation from the registry

    [SPI_register_trigger_data](spi-spi-register-trigger-data.md) — make ephemeral trigger data available in SPI queries

[45.2. Interface Support Functions](spi-interface-support.md)
:   [SPI_fname](spi-spi-fname.md) — determine the column name for the specified column number

    [SPI_fnumber](spi-spi-fnumber.md) — determine the column number for the specified column name

    [SPI_getvalue](spi-spi-getvalue.md) — return the string value of the specified column

    [SPI_getbinval](spi-spi-getbinval.md) — return the binary value of the specified column

    [SPI_gettype](spi-spi-gettype.md) — return the data type name of the specified column

    [SPI_gettypeid](spi-spi-gettypeid.md) — return the data type OID of the specified column

    [SPI_getrelname](spi-spi-getrelname.md) — return the name of the specified relation

    [SPI_getnspname](spi-spi-getnspname.md) — return the namespace of the specified relation

    [SPI_result_code_string](spi-spi-result-code-string.md) — return error code as string

[45.3. Memory Management](spi-memory.md)
:   [SPI_palloc](spi-spi-palloc.md) — allocate memory in the upper executor context

    [SPI_repalloc](spi-realloc.md) — reallocate memory in the upper executor context

    [SPI_pfree](spi-spi-pfree.md) — free memory in the upper executor context

    [SPI_copytuple](spi-spi-copytuple.md) — make a copy of a row in the upper executor context

    [SPI_returntuple](spi-spi-returntuple.md) — prepare to return a tuple as a Datum

    [SPI_modifytuple](spi-spi-modifytuple.md) — create a row by replacing selected fields of a given row

    [SPI_freetuple](spi-spi-freetuple.md) — free a row allocated in the upper executor context

    [SPI_freetuptable](spi-spi-freetupletable.md) — free a row set created by `SPI_execute` or a similar function

    [SPI_freeplan](spi-spi-freeplan.md) — free a previously saved prepared statement

[45.4. Transaction Management](spi-transaction.md)
:   [SPI_commit](spi-spi-commit.md) — commit the current transaction

    [SPI_rollback](spi-spi-rollback.md) — abort the current transaction

    [SPI_start_transaction](spi-spi-start-transaction.md) — obsolete function

[45.5. Visibility of Data Changes](spi-visibility.md)

[45.6. Examples](spi-examples.md)

<a id="id-1.8.12.2"></a>

The *Server Programming Interface*
(SPI) gives writers of user-defined
C functions the ability to run
SQL commands inside their functions or procedures.
SPI is a set of
interface functions to simplify access to the parser, planner,
and executor. SPI also does some
memory management.

### Note

The available procedural languages provide various means to
execute SQL commands from functions. Most of these facilities are
based on SPI, so this documentation might be of use for users
of those languages as well.

Note that if a command invoked via SPI fails, then control will not be
returned to your C function. Rather, the
transaction or subtransaction in which your C function executes will be
rolled back. (This might seem surprising given that the SPI functions mostly
have documented error-return conventions. Those conventions only apply
for errors detected within the SPI functions themselves, however.)
It is possible to recover control after an error by establishing your own
subtransaction surrounding SPI calls that might fail.

SPI functions return a nonnegative result on
success (either via a returned integer value or in the global
variable `SPI_result`, as described below). On
error, a negative result or `NULL` will be returned.

Source code files that use SPI must include the header file
`executor/spi.h`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi.html)（英文原文，待翻譯）
