## 44.8. 交易管理 [#](#PLPYTHON-TRANSACTIONS)

從最上層呼叫的程序或匿名程式碼區塊（`DO` 命令）可以控制交易。呼叫 `plpy.commit()` 可提交目前的交易，呼叫 `plpy.rollback()` 可回復目前的交易。（請注意，不能透過 `plpy.execute` 或類似方式執行 SQL 命令 `COMMIT` 或 `ROLLBACK`，必須使用這些函式。）交易結束後會自動開始新交易，因此沒有另外提供用來開始交易的函式。

以下是一個範例：

```

CREATE PROCEDURE transaction_test1()
LANGUAGE plpython3u
AS $$
for i in range(0, 10):
    plpy.execute("INSERT INTO test1 (a) VALUES (%d)" % i)
    if i % 2 == 0:
        plpy.commit()
    else:
        plpy.rollback()
$$;

CALL transaction_test1();
```

當明確建立的子交易仍在進行時，不能結束交易。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-transactions.html)（原文版本：18.6；核對日期：2026-09-07）
