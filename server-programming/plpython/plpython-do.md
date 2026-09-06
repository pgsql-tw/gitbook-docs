## 44.4. 匿名程式碼區塊 [#](#PLPYTHON-DO)

PL/Python 也支援使用 [DO](../../reference/sql-commands/sql-do.md) 陳述式呼叫匿名程式碼區塊：

```

DO $$
    # PL/Python code
$$ LANGUAGE plpython3u;
```

匿名程式碼區塊不接收引數，任何回傳值都會被捨棄。除此之外，其行為與函式相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-do.html)（原文版本：18.6；核對日期：2026-09-07）
