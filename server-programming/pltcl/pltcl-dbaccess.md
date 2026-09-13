<a id="PLTCL-DBACCESS"></a>

## 42.5. 從 PL/Tcl 存取資料庫 [#](#PLTCL-DBACCESS)

在本節中，我們遵循 Tcl 一般的慣例，在語法概要中使用問號（而非方括號）來表示可選的元素。以下這些指令可以用來從 PL/Tcl 函式的主體存取資料庫：

`spi_exec ?-count n? ?-array name? command ?loop-body?`
:   執行以字串形式給定的 SQL 指令。指令中若有錯誤，會引發錯誤。否則，`spi_exec` 的回傳值是該指令所處理（選取、插入、更新或刪除）的資料列數量；若該指令是公用程式陳述式，則回傳零。此外，如果該指令是 `SELECT` 陳述式，被選取欄位的值會依照下面所述放進 Tcl 變數中。

    可選的 `-count` 值會告訴 `spi_exec` 在取得 *`n`* 筆資料列之後就停止，就好像查詢中包含了 `LIMIT` 子句一樣。如果 *`n`* 是零，查詢會執行到完成，與省略 `-count` 時相同。

    如果該指令是 `SELECT` 陳述式，結果欄位的值會被放進以欄位命名的 Tcl 變數中。如果有給定 `-array` 選項，欄位值則改為儲存到所指定的關聯陣列的元素中，並以欄位名稱作為陣列索引。此外，結果中目前的資料列編號（從零開始計算）會被存放到名為「`.tupno`」的陣列元素中，除非該名稱已被結果中的某個欄位名稱佔用。

    如果該指令是 `SELECT` 陳述式，而且沒有給定 *`loop-body`* 指令稿，那麼只有結果的第一筆資料列會被存入 Tcl 變數或陣列元素中；其餘的資料列（如果有的話）都會被忽略。如果查詢沒有回傳任何資料列，就不會進行任何儲存。（這種情況可以藉由檢查 `spi_exec` 的結果來偵測。）例如：

    ```

    spi_exec "SELECT count(*) AS cnt FROM pg_proc"
    ```

    會將 Tcl 變數 `$cnt` 設為 `pg_proc` 系統目錄中的資料列數量。

    如果有給定可選的 *`loop-body`* 引數，它就是一段 Tcl 指令稿，會針對查詢結果中的每一筆資料列各執行一次。（如果給定的指令不是 `SELECT`，*`loop-body`* 會被忽略。）在每次迭代之前，目前資料列各欄位的值都會被存入 Tcl 變數或陣列元素中。例如：

    ```

    spi_exec -array C "SELECT * FROM pg_class" {
        elog DEBUG "have table $C(relname)"
    }
    ```

    會為 `pg_class` 的每一筆資料列印出一則日誌訊息。這個功能的運作方式與其他 Tcl 迴圈結構類似；特別是 `continue` 與 `break` 在迴圈主體中會以慣常的方式運作。

    如果查詢結果中的某個欄位是 NULL，對應的目標變數會被「unset」，而不是被設值。

`spi_prepare` *`query`* *`typelist`*
:   準備並儲存一份查詢的執行計畫以供之後執行。儲存下來的執行計畫會在目前工作階段的生命週期內一直保留。<a id="id-1.8.9.9.2.1.2.2.1.1"></a>

    查詢中可以使用參數，也就是在執行計畫實際被執行時才提供值的預留位置。在查詢字串中，請以 `$1` ... `$n` 這些符號來指涉參數。如果查詢使用了參數，參數型別的名稱必須以 Tcl list（串列）的形式給定。（如果沒有使用參數，請為 *`typelist`* 寫一個空的 list。）

    `spi_prepare` 的回傳值是一個查詢 ID，可用於後續對 `spi_execp` 的呼叫。範例請參閱 `spi_execp`。

`spi_execp ?-count n? ?-array name? ?-nulls string? queryid ?value-list? ?loop-body?`
:   執行先前以 `spi_prepare` 準備好的查詢。*`queryid`* 是 `spi_prepare` 所回傳的 ID。如果查詢參照了參數，就必須提供 *`value-list`*。這是一個包含參數實際值的 Tcl list。這個 list 的長度必須與先前給定 `spi_prepare` 的參數型別 list 相同。如果查詢沒有參數，請省略 *`value-list`*。

    `-nulls` 的可選值是一個由空格與 `'n'` 字元組成的字串，用來告訴 `spi_execp` 哪些參數是 NULL 值。如果有給定，它的長度必須與 *`value-list`* 完全相同。如果沒有給定，則所有參數值都是非 NULL。

    除了查詢與其參數的指定方式不同之外，`spi_execp` 的運作方式與 `spi_exec` 完全相同。`-count`、`-array` 與 *`loop-body`* 這些選項都相同，結果值也相同。

    以下是一個使用預備好的執行計畫的 PL/Tcl 函式範例：

    ```

    CREATE FUNCTION t1_count(integer, integer) RETURNS integer AS $$
        if {![ info exists GD(plan) ]} {
            # prepare the saved plan on the first call
            set GD(plan) [ spi_prepare \
                    "SELECT count(*) AS cnt FROM t1 WHERE num >= \$1 AND num <= \$2" \
                    [ list int4 int4 ] ]
        }
        spi_execp -count 1 $GD(plan) [ list $1 $2 ]
        return $cnt
    $$ LANGUAGE pltcl;
    ```

    我們需要在給 `spi_prepare` 的查詢字串中加上反斜線，以確保 `$n` 標記會原樣傳遞給 `spi_prepare`，而不會被 Tcl 的變數替換所取代。

`subtransaction` *`command`*
:   *`command`* 中所含的 Tcl 指令稿會在一個 SQL 子交易中執行。如果該指令稿回傳錯誤，整個子交易會在錯誤被回傳到外層 Tcl 程式碼之前被回復。更多細節與範例請參閱[第 42.9 節](pltcl-subtransactions.md)。

`quote` *`string`*
:   將給定字串中所有出現的單引號與反斜線字元都變成兩個。這可以用來安全地為將要插入 `spi_exec` 或 `spi_prepare` 所接收之 SQL 指令中的字串加上引號。例如，想想看像這樣的 SQL 指令字串：

    ```

    "SELECT '$val' AS ret"
    ```

    其中 Tcl 變數 `val` 實際上含有 `doesn't`。這會產生出最終的指令字串：

    ```

    SELECT 'doesn't' AS ret
    ```

    而它會在 `spi_exec` 或 `spi_prepare` 期間造成剖析錯誤。要正確運作，送出的指令應該要包含：

    ```

    SELECT 'doesn''t' AS ret
    ```

    在 PL/Tcl 中可以用下列方式產生：

    ```

    "SELECT '[ quote $val ]' AS ret"
    ```

    `spi_execp` 的一項優點是，你不必像這樣為參數值加上引號，因為那些參數永遠不會被當成 SQL 指令字串的一部分來剖析。

`elog` *`level`* *`msg`* <a id="id-1.8.9.9.2.1.6.1.4"></a>
:   發出日誌或錯誤訊息。可能的層級有 `DEBUG`、`LOG`、`INFO`、`NOTICE`、`WARNING`、`ERROR` 與 `FATAL`。`ERROR` 會引發錯誤狀況；如果外層的 Tcl 程式碼沒有攔截它，該錯誤會向外傳播到呼叫端的查詢，造成目前的交易或子交易被中止。這實際上與 Tcl 的 `error` 指令相同。`FATAL` 會中止交易並使目前的工作階段關閉。（在 PL/Tcl 函式中大概沒有什麼好理由要使用這個錯誤層級，但為了完整性還是提供了它。）其他層級只會產生不同優先層級的訊息。特定優先層級的訊息是否會回報給用戶端、寫入伺服器日誌或兩者皆是，由 [log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 與 [client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 組態變數所控制。更多資訊請參閱[第 19 章](../../server-administration/runtime-config/README.md)與[第 42.8 節](pltcl-error-handling.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-dbaccess.html)（原文版本：18.6；核對日期：2026-09-13）
