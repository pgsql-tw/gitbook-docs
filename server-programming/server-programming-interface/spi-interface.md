<a id="SPI-INTERFACE"></a>

# 47.1. Interface Functions

[SPI_connect](spi-interface/spi-spi-connect.md) — connect a C function to the SPI manager

[SPI_finish](spi-interface/spi-spi-finish.md) — disconnect a C function from the SPI manager

[SPI_execute](spi-interface/spi-spi-execute.md) — execute a command

[SPI_exec](spi-interface/spi-spi-exec.md) — execute a read/write command

[SPI_execute_extended](spi-interface/spi-spi-execute-extended.md) — execute a command with out-of-line parameters

[SPI_execute_with_args](spi-interface/spi-spi-execute-with-args.md) — execute a command with out-of-line parameters

[SPI_prepare](spi-interface/spi-spi-prepare.md) — prepare a statement, without executing it yet

[SPI_prepare_cursor](spi-interface/spi-spi-prepare-cursor.md) — prepare a statement, without executing it yet

[SPI_prepare_extended](spi-interface/spi-spi-prepare-extended.md) — prepare a statement, without executing it yet

[SPI_prepare_params](spi-interface/spi-spi-prepare-params.md) — prepare a statement, without executing it yet

[SPI_getargcount](spi-interface/spi-spi-getargcount.md) — return the number of arguments needed by a statement prepared by `SPI_prepare`

[SPI_getargtypeid](spi-interface/spi-spi-getargtypeid.md) — return the data type OID for an argument of a statement prepared by `SPI_prepare`

[SPI_is_cursor_plan](spi-interface/spi-spi-is-cursor-plan.md) — return `true` if a statement prepared by `SPI_prepare` can be used with `SPI_cursor_open`

[SPI_execute_plan](spi-interface/spi-spi-execute-plan.md) — execute a statement prepared by `SPI_prepare`

[SPI_execute_plan_extended](spi-interface/spi-spi-execute-plan-extended.md) — execute a statement prepared by `SPI_prepare`

[SPI_execute_plan_with_paramlist](spi-interface/spi-spi-execute-plan-with-paramlist.md) — execute a statement prepared by `SPI_prepare`

[SPI_execp](spi-interface/spi-spi-execp.md) — execute a statement in read/write mode

[SPI_cursor_open](spi-interface/spi-spi-cursor-open.md) — set up a cursor using a statement created with `SPI_prepare`

[SPI_cursor_open_with_args](spi-interface/spi-spi-cursor-open-with-args.md) — set up a cursor using a query and parameters

[SPI_cursor_open_with_paramlist](spi-interface/spi-spi-cursor-open-with-paramlist.md) — set up a cursor using parameters

[SPI_cursor_parse_open](spi-interface/spi-spi-cursor-parse-open.md) — set up a cursor using a query string and parameters

[SPI_cursor_find](spi-interface/spi-spi-cursor-find.md) — find an existing cursor by name

[SPI_cursor_fetch](spi-interface/spi-spi-cursor-fetch.md) — fetch some rows from a cursor

[SPI_cursor_move](spi-interface/spi-spi-cursor-move.md) — move a cursor

[SPI_scroll_cursor_fetch](spi-interface/spi-spi-scroll-cursor-fetch.md) — fetch some rows from a cursor

[SPI_scroll_cursor_move](spi-interface/spi-spi-scroll-cursor-move.md) — move a cursor

[SPI_cursor_close](spi-interface/spi-spi-cursor-close.md) — close a cursor

[SPI_keepplan](spi-interface/spi-spi-keepplan.md) — save a prepared statement

[SPI_saveplan](spi-interface/spi-spi-saveplan.md) — save a prepared statement

[SPI_register_relation](spi-interface/spi-spi-register-relation.md) — make an ephemeral named relation available by name in SPI queries

[SPI_unregister_relation](spi-interface/spi-spi-unregister-relation.md) — remove an ephemeral named relation from the registry

[SPI_register_trigger_data](spi-interface/spi-spi-register-trigger-data.md) — make ephemeral trigger data available in SPI queries

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-interface.html)（英文原文，待翻譯）
