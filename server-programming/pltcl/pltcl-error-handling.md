<a id="PLTCL-ERROR-HANDLING"></a>

## 42.8. PL/Tcl 中的錯誤處理 [#](#PLTCL-ERROR-HANDLING)

<a id="id-1.8.9.12.2"></a>

PL/Tcl 函式中的、或由其呼叫的 Tcl 程式碼可能引發錯誤，可能是因為執行了某個無效的操作，也可能是使用 Tcl 的 `error` 指令或 PL/Tcl 的 `elog` 指令產生錯誤。這類錯誤可以在 Tcl 中以 Tcl 的 `catch` 指令攔截。如果某個錯誤沒有被攔截，而是被允許向外傳播到 PL/Tcl 函式執行的最上層，它就會在該函式的呼叫端查詢中被回報為 SQL 錯誤。

反過來說，在 PL/Tcl 的 `spi_exec`、`spi_prepare` 與 `spi_execp` 指令中發生的 SQL 錯誤會被回報為 Tcl 錯誤，因此可以用 Tcl 的 `catch` 指令攔截。（這些 PL/Tcl 指令各自都在一個子交易中執行其 SQL 操作，該子交易在發生錯誤時會被回復，如此任何只完成一部分的操作都會自動被清理掉。）同樣地，如果錯誤未被攔截而傳播到最上層，它會再變回 SQL 錯誤。

Tcl 提供了一個 `errorCode` 變數，能以方便 Tcl 程式解讀的形式表達關於錯誤的額外資訊。其內容採用 Tcl list（串列）格式，第一個字詞標示回報該錯誤的子系統或函式庫；在那之後的內容則由各個子系統或函式庫自行決定。對於由 PL/Tcl 指令回報的資料庫錯誤，第一個字詞是 `POSTGRES`，第二個字詞是 PostgreSQL 的版本編號，再後面的字詞則是提供該錯誤詳細資訊的欄位名稱／值配對。`SQLSTATE`、`condition` 與 `message` 這幾個欄位一定會提供（前兩者代表[附錄 A](../../appendixes/errcodes-appendix/README.md) 中所列的錯誤碼與條件名稱）。可能出現的欄位包括 `detail`、`hint`、`context`、`schema`、`table`、`column`、`datatype`、`constraint`、`statement`、`cursor_position`、`filename`、`lineno` 與 `funcname`。

要處理 PL/Tcl 的 `errorCode` 資訊，一個方便的做法是把它載入到一個陣列中，如此欄位名稱就會變成陣列的下標。做這件事的程式碼看起來可能像這樣：

```

if {[catch { spi_exec $sql_command }]} {
    if {[lindex $::errorCode 0] == "POSTGRES"} {
        array set errorArray $::errorCode
        if {$errorArray(condition) == "undefined_table"} {
            # deal with missing table
        } else {
            # deal with some other type of SQL error
        }
    }
}
```

（雙冒號明確指出 `errorCode` 是一個全域變數。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-error-handling.html)（原文版本：18.6；核對日期：2026-09-13）
