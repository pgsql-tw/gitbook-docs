<a id="PLPYTHON-SUBTRANSACTION"></a>

## 44.7. 明確的子交易 [#](#PLPYTHON-SUBTRANSACTION)

[44.7.1. 子交易情境管理器](plpython-subtransaction.md#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

如同[第 44.6.2 節](plpython-database.md#PLPYTHON-TRAPPING)所述，從資料庫存取所造成的錯誤中復原，可能會導致一種不樂見的情況：某些操作在其中一個操作失敗之前已經成功，而在從該錯誤復原之後，資料就停留在不一致的狀態。PL/Python 以明確子交易的形式為這個問題提供了解決方案。

<a id="PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS"></a>

### 44.7.1. 子交易情境管理器 [#](#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

考慮一個實作兩個帳戶之間轉帳的函式：

```

CREATE FUNCTION transfer_funds() RETURNS void AS $$
try:
    plpy.execute("UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'")
    plpy.execute("UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'")
except plpy.SPIError as e:
    result = "error transferring funds: %s" % e.args
else:
    result = "funds transferred correctly"
plan = plpy.prepare("INSERT INTO operations (result) VALUES ($1)", ["text"])
plpy.execute(plan, [result])
$$ LANGUAGE plpython3u;
```

如果第二個 `UPDATE` 陳述式導致例外被拋出，這個函式會回報該錯誤，但第一個 `UPDATE` 的結果仍然會被提交。換句話說，錢會從 Joe 的帳戶中被提走，卻不會轉入 Mary 的帳戶。

為了避免這類問題，你可以把 `plpy.execute` 呼叫包在一個明確的子交易中。`plpy` 模組提供了一個輔助物件來管理明確子交易，它是以 `plpy.subtransaction()` 函式建立的。由這個函式所建立的物件實作了[情境管理器介面](https://docs.python.org/library/stdtypes.html#context-manager-types)。使用明確子交易，我們可以把函式改寫成：

```

CREATE FUNCTION transfer_funds2() RETURNS void AS $$
try:
    with plpy.subtransaction():
        plpy.execute("UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'")
        plpy.execute("UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'")
except plpy.SPIError as e:
    result = "error transferring funds: %s" % e.args
else:
    result = "funds transferred correctly"
plan = plpy.prepare("INSERT INTO operations (result) VALUES ($1)", ["text"])
plpy.execute(plan, [result])
$$ LANGUAGE plpython3u;
```

請注意，仍然必須使用 `try`/`except`。否則例外會傳播到 Python 堆疊的最上層，導致整個函式以 PostgreSQL 錯誤中止，於是 `operations` 資料表也不會被插入任何資料列。子交易情境管理器並不會攔截錯誤，它只確保在其作用範圍內所執行的所有資料庫操作會以不可分割的方式一起提交或一起回復。子交易區塊的回復會在任何形式的例外離開時發生，不只限於資料庫存取所引發的錯誤。在明確子交易區塊內拋出的一般 Python 例外，同樣也會使該子交易被回復。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-subtransaction.html)（原文版本：18.6；核對日期：2026-09-13）
