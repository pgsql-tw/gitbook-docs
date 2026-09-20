## 第 45 章 伺服器程式設計介面

**目錄**

[45.1. 介面函式](spi-interface.md)
:   [SPI_connect](spi-spi-connect.md) — 將 C 函式連線到 SPI 管理器

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

[45.2. 介面輔助函式](spi-interface-support.md)
:   [SPI_fname](spi-spi-fname.md) — 判斷指定欄位編號所對應的欄位名稱

    [SPI_fnumber](spi-spi-fnumber.md) — 判斷指定欄位名稱所對應的欄位編號

    [SPI_getvalue](spi-spi-getvalue.md) — 回傳指定欄位的字串值

    [SPI_getbinval](spi-spi-getbinval.md) — 回傳指定欄位的二進位值

    [SPI_gettype](spi-spi-gettype.md) — 回傳指定欄位的資料型別名稱

    [SPI_gettypeid](spi-spi-gettypeid.md) — 回傳指定欄位的資料型別 OID

    [SPI_getrelname](spi-spi-getrelname.md) — 回傳指定關聯的名稱

    [SPI_getnspname](spi-spi-getnspname.md) — 回傳指定關聯所屬的命名空間

    [SPI_result_code_string](spi-spi-result-code-string.md) — 以字串形式回傳錯誤碼

[45.3. 記憶體管理](spi-memory.md)
:   [SPI_palloc](spi-spi-palloc.md) — 在上層執行器記憶體上下文中配置記憶體

    [SPI_repalloc](spi-realloc.md) — 在上層執行器記憶體上下文中重新配置記憶體

    [SPI_pfree](spi-spi-pfree.md) — 釋放上層執行器記憶體上下文中的記憶體

    [SPI_copytuple](spi-spi-copytuple.md) — 在上層執行器記憶體上下文中複製一個資料列

    [SPI_returntuple](spi-spi-returntuple.md) — 準備以 Datum 形式回傳一個 tuple（值組）

    [SPI_modifytuple](spi-spi-modifytuple.md) — 以取代指定資料列中某些欄位的方式建立一個資料列

    [SPI_freetuple](spi-spi-freetuple.md) — 釋放在上層執行器記憶體上下文中配置的資料列

    [SPI_freetuptable](spi-spi-freetupletable.md) — 釋放由 `SPI_execute` 或類似函式所建立的資料列集合

    [SPI_freeplan](spi-spi-freeplan.md) — 釋放先前儲存的預備陳述式

[45.4. 交易管理](spi-transaction.md)
:   [SPI_commit](spi-spi-commit.md) — 提交目前的交易

    [SPI_rollback](spi-spi-rollback.md) — 中止目前的交易

    [SPI_start_transaction](spi-spi-start-transaction.md) — 已過時的函式

[45.5. 資料變更的可見性](spi-visibility.md)

[45.6. 範例](spi-examples.md)

<a id="id-1.8.12.2"></a>

*伺服器程式設計介面*（Server Programming Interface，SPI）讓撰寫使用者自訂 C 函式的人能夠在其函式或程序內部執行 SQL 指令。SPI 是一組介面函式，用來簡化對剖析器、規劃器與執行器的存取。SPI 也會處理一部分的記憶體管理。

<a id="SPI-OVERVIEW-NOTE"></a>

### 注意

現有的各種程序語言提供了多種從函式中執行 SQL 指令的方法。這些機制大多以 SPI 為基礎，因此這份說明文件對那些語言的使用者可能也有幫助。

請注意，如果透過 SPI 呼叫的指令失敗，控制權並不會回到你的 C 函式。取而代之的是，執行你的 C 函式的那個交易或子交易會被回復。（既然這些 SPI 函式大多有明文記載的錯誤回傳慣例，這一點可能會讓人意外。不過那些慣例只適用於在 SPI 函式本身內部所偵測到的錯誤。）你可以在可能失敗的 SPI 呼叫外圍建立自己的子交易，藉此在錯誤發生後取回控制權。

SPI 函式在成功時會回傳非負的結果（可能是透過回傳的整數值，也可能是透過後面說明的全域變數 `SPI_result`）。發生錯誤時，則會回傳負值或 `NULL`。

使用 SPI 的原始程式碼檔案必須引入標頭檔 `executor/spi.h`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi.html)（原文版本：18.6；核對日期：2026-09-15）
