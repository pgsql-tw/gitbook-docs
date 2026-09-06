## 42.10. 交易管理 [#](#PLTCL-TRANSACTIONS)

從最上層呼叫的程序或匿名程式碼區塊（`DO` 命令）可以控制交易。呼叫 `commit` 命令可提交目前的交易，呼叫 `rollback` 命令可回復目前的交易。（請注意，不能透過 `spi_exec` 或類似方式執行 SQL 命令 `COMMIT` 或 `ROLLBACK`，必須使用這些函式。）交易結束後會自動開始新交易，因此沒有另外提供用來開始交易的命令。

以下是一個範例：

```

CREATE PROCEDURE transaction_test1()
LANGUAGE pltcl
AS $$
for {set i 0} {$i < 10} {incr i} {
    spi_exec "INSERT INTO test1 (a) VALUES ($i)"
    if {$i % 2 == 0} {
        commit
    } else {
        rollback
    }
}
$$;

CALL transaction_test1();
```

當明確建立的子交易仍在進行時，不能結束交易。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-transactions.html)（原文版本：18.6；核對日期：2026-09-07）
