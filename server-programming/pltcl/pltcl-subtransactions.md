<a id="PLTCL-SUBTRANSACTIONS"></a>

## 42.9. PL/Tcl 中的明確子交易 [#](#PLTCL-SUBTRANSACTIONS)

<a id="id-1.8.9.13.2"></a>

依照[第 42.8 節](pltcl-error-handling.md)所述的方式，從資料庫存取所造成的錯誤中復原，可能導致一種不樂見的情況：在其中某個操作失敗之前，已經有一些操作成功了，而在從該錯誤復原之後，資料便處於不一致的狀態。PL/Tcl 以明確子交易的形式，為這個問題提供了解決方案。

考慮一個實作兩個帳戶之間轉帳的函式：

```

CREATE FUNCTION transfer_funds() RETURNS void AS $$
    if [catch {
        spi_exec "UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'"
        spi_exec "UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'"
    } errormsg] {
        set result [format "error transferring funds: %s" $errormsg]
    } else {
        set result "funds transferred successfully"
    }
    spi_exec "INSERT INTO operations (result) VALUES ('[quote $result]')"
$$ LANGUAGE pltcl;
```

如果第二個 `UPDATE` 陳述式導致例外被引發，這個函式會記錄下這次失敗，但第一個 `UPDATE` 的結果仍然會被提交。換句話說，資金會從 Joe 的帳戶中被提走，卻沒有轉到 Mary 的帳戶。之所以會這樣，是因為每個 `spi_exec` 都是一個獨立的子交易，而其中只有一個子交易被回復了。

為了處理這類情況，你可以把多個資料庫操作包在一個明確的子交易中，它會整體地成功或整體地回復。PL/Tcl 提供了 `subtransaction` 指令來管理這件事。我們可以把函式改寫成：

```

CREATE FUNCTION transfer_funds2() RETURNS void AS $$
    if [catch {
        subtransaction {
            spi_exec "UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'"
            spi_exec "UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'"
        }
    } errormsg] {
        set result [format "error transferring funds: %s" $errormsg]
    } else {
        set result "funds transferred successfully"
    }
    spi_exec "INSERT INTO operations (result) VALUES ('[quote $result]')"
$$ LANGUAGE pltcl;
```

請注意，為此仍然需要使用 `catch`。否則錯誤會傳播到函式的最上層，使得我們想要的、對 `operations` 資料表的插入無法完成。`subtransaction` 指令並不會攔截錯誤，它只確保當有錯誤被回報時，在其範圍內執行的所有資料庫操作都會一起被回復。

明確子交易的回復，會在其所包含的 Tcl 程式碼回報任何錯誤時發生，而不只是源自資料庫存取的錯誤。因此，在 `subtransaction` 指令內引發的一般 Tcl 例外也會造成該子交易被回復。不過，從其所包含的 Tcl 程式碼以非錯誤方式離開（例如因為 `return`）並不會造成回復。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-subtransactions.html)（原文版本：18.6；核對日期：2026-09-12）
