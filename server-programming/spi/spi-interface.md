<a id="SPI-INTERFACE"></a>

## 45.1. 介面函式 [#](#SPI-INTERFACE)

[SPI_connect](spi-spi-connect.md) — 將 C 函式連線到 SPI 管理器

[SPI_finish](spi-spi-finish.md) — 中斷 C 函式與 SPI 管理器的連線

[SPI_execute](spi-spi-execute.md) — 執行一個指令

[SPI_exec](spi-spi-exec.md) — 執行一個讀寫指令

[SPI_execute_extended](spi-spi-execute-extended.md) — 以外部（out-of-line）參數執行指令

[SPI_execute_with_args](spi-spi-execute-with-args.md) — 以外部（out-of-line）參數執行指令

[SPI_prepare](spi-spi-prepare.md) — 預備一個陳述式，但尚未執行它

[SPI_prepare_cursor](spi-spi-prepare-cursor.md) — 預備一個陳述式，但尚未執行它

[SPI_prepare_extended](spi-spi-prepare-extended.md) — 預備一個陳述式，但尚未執行它

[SPI_prepare_params](spi-spi-prepare-params.md) — 預備一個陳述式，但尚未執行它

[SPI_getargcount](spi-spi-getargcount.md) — 回傳由 `SPI_prepare` 所預備之陳述式需要的引數個數

[SPI_getargtypeid](spi-spi-getargtypeid.md) — 回傳由 `SPI_prepare` 所預備之陳述式某個引數的資料型別 OID

[SPI_is_cursor_plan](spi-spi-is-cursor-plan.md) — 若由 `SPI_prepare` 所預備的陳述式可搭配 `SPI_cursor_open` 使用，則回傳 `true`

[SPI_execute_plan](spi-spi-execute-plan.md) — 執行由 `SPI_prepare` 預備好的陳述式

[SPI_execute_plan_extended](spi-spi-execute-plan-extended.md) — 執行由 `SPI_prepare` 預備好的陳述式

[SPI_execute_plan_with_paramlist](spi-spi-execute-plan-with-paramlist.md) — 執行由 `SPI_prepare` 預備好的陳述式

[SPI_execp](spi-spi-execp.md) — 以讀寫模式執行陳述式

[SPI_cursor_open](spi-spi-cursor-open.md) — 使用以 `SPI_prepare` 建立的陳述式設定一個游標

[SPI_cursor_open_with_args](spi-spi-cursor-open-with-args.md) — 使用一個查詢與參數設定一個游標

[SPI_cursor_open_with_paramlist](spi-spi-cursor-open-with-paramlist.md) — 使用參數設定一個游標

[SPI_cursor_parse_open](spi-spi-cursor-parse-open.md) — 使用一個查詢字串與參數設定一個游標

[SPI_cursor_find](spi-spi-cursor-find.md) — 依名稱尋找既有的游標

[SPI_cursor_fetch](spi-spi-cursor-fetch.md) — 從游標取回若干資料列

[SPI_cursor_move](spi-spi-cursor-move.md) — 移動游標

[SPI_scroll_cursor_fetch](spi-spi-scroll-cursor-fetch.md) — 從游標取回若干資料列

[SPI_scroll_cursor_move](spi-spi-scroll-cursor-move.md) — 移動游標

[SPI_cursor_close](spi-spi-cursor-close.md) — 關閉一個游標

[SPI_keepplan](spi-spi-keepplan.md) — 儲存一個預備陳述式

[SPI_saveplan](spi-spi-saveplan.md) — 儲存一個預備陳述式

[SPI_register_relation](spi-spi-register-relation.md) — 讓一個暫時性具名關聯可在 SPI 查詢中以名稱使用

[SPI_unregister_relation](spi-spi-unregister-relation.md) — 將一個暫時性具名關聯從註冊表中移除

[SPI_register_trigger_data](spi-spi-register-trigger-data.md) — 讓暫時性的觸發程序資料可在 SPI 查詢中使用

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-interface.html)（原文版本：18.6；核對日期：2026-09-13）
