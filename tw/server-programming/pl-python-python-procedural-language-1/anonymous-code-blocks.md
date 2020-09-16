# 45.5. Anonymous Code Blocks

PL/Python 還支援使用 [DO](../../reference/sql-commands/do.md) 語句呼叫的暱名代碼：

```text
DO $$
    # PL/Python code
$$ LANGUAGE plpythonu;
```

暱名代碼不接收任何參數，並且它可能回傳的任何值都將被丟棄。不然它的行為就像一個函數了。

