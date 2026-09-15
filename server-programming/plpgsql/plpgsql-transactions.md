<a id="PLPGSQL-TRANSACTIONS"></a>

## 41.8. 交易管理 [#](#PLPGSQL-TRANSACTIONS)

在以 `CALL` 指令呼叫的程序中，以及在匿名程式區塊（`DO` 指令）中，可以使用 `COMMIT` 與 `ROLLBACK` 指令來結束交易。以這些指令結束交易之後，會自動開始一個新的交易，因此並沒有獨立的 `START TRANSACTION` 指令。（請注意，`BEGIN` 與 `END` 在 PL/pgSQL 中有不同的意義。）

以下是一個簡單的例子：

```

CREATE PROCEDURE transaction_test1()
LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..9 LOOP
        INSERT INTO test1 (a) VALUES (i);
        IF i % 2 = 0 THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
    END LOOP;
END;
$$;

CALL transaction_test1();
```

<a id="id-1.8.8.10.4"></a><a id="PLPGSQL-TRANSACTION-CHAIN"></a>

新的交易會以預設的交易特性開始，例如交易隔離等級。若交易是在迴圈中提交，你可能會希望新交易自動採用與前一個交易相同的特性。`COMMIT AND CHAIN` 與 `ROLLBACK AND CHAIN` 指令就是用來做到這件事。

只有在從最上層發出的 `CALL` 或 `DO` 呼叫中，或是在中間沒有夾雜其他指令的巢狀 `CALL` 或 `DO` 呼叫中，才能進行交易控制。舉例來說，如果呼叫堆疊是 `CALL proc1()` → `CALL proc2()` → `CALL proc3()`，那麼第二個與第三個程序都可以執行交易控制動作。但如果呼叫堆疊是 `CALL proc1()` → `SELECT func2()` → `CALL proc3()`，那麼最後那個程序就不能做交易控制，因為中間夾了一個 `SELECT`。

PL/pgSQL 不支援交易儲存點（`SAVEPOINT`／`ROLLBACK TO SAVEPOINT`／`RELEASE SAVEPOINT` 指令）。交易儲存點的典型使用模式，可以改用帶有例外處理常式的區塊來取代（參閱[第 41.6.8 節](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)）。在內部，帶有例外處理常式的區塊會形成一個子交易，這也表示不能在這樣的區塊內結束交易。

游標迴圈有一些特別要注意的地方。請看這個例子：

```

CREATE PROCEDURE transaction_test2()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM test2 ORDER BY x LOOP
        INSERT INTO test1 (a) VALUES (r.x);
        COMMIT;
    END LOOP;
END;
$$;

CALL transaction_test2();
```

一般來說，游標會在交易提交時自動關閉。不過，像這樣在迴圈中建立的游標，會在第一次 `COMMIT` 或 `ROLLBACK` 時自動轉換成可保留的游標。這表示該游標會在第一次 `COMMIT` 或 `ROLLBACK` 時就完整計算完畢，而不是逐列計算。這個游標在迴圈結束後仍然會自動移除，所以對使用者來說大致上是看不出差別的。但必須記住，該游標的查詢所取得的任何資料表鎖或資料列鎖，在第一次 `COMMIT` 或 `ROLLBACK` 之後就不再持有了。

在由非唯讀指令（例如 `UPDATE ... RETURNING`）所驅動的游標迴圈中，不允許使用交易指令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-transactions.html)（原文版本：18.6；核對日期：2026-09-13）
