## 44.4. Anonymous Code Blocks [#](#PLPYTHON-DO)

PL/Python also supports anonymous code blocks called with the
[DO](../../reference/sql-commands/sql-do.md) statement:

```

DO $$
    # PL/Python code
$$ LANGUAGE plpython3u;
```

An anonymous code block receives no arguments, and whatever value it
might return is discarded. Otherwise it behaves just like a function.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-do.html)（英文原文，待翻譯）
