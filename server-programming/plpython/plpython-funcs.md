<a id="PLPYTHON-FUNCS"></a>

## 44.1. PL/Python 函式 [#](#PLPYTHON-FUNCS)

PL/Python 中的函式是透過標準的 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 語法來宣告：

```

CREATE FUNCTION funcname (argument-list)
  RETURNS return-type
AS $$
  # PL/Python function body
$$ LANGUAGE plpython3u;
```

函式的本體就只是一段 Python 指令稿。當函式被呼叫時，它的引數會以 list `args` 的元素形式傳入；具名引數同時也會以一般變數的形式傳給該 Python 指令稿。使用具名引數通常可讀性較佳。結果則以 Python 一般的方式從程式碼中回傳，也就是使用 `return`，或（在回傳結果集的情況下）使用 `yield`。如果你沒有提供回傳值，Python 會回傳預設的 `None`。PL/Python 會把 Python 的 `None` 轉換成 SQL 的 NULL 值。在程序中，Python 程式碼的結果必須是 `None`（通常的做法是讓程序結束時沒有 `return` 陳述式，或使用不帶引數的 `return` 陳述式）；否則就會拋出錯誤。

舉例來說，一個回傳兩個整數中較大者的函式可以這樣定義：

```

CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if a > b:
    return a
  return b
$$ LANGUAGE plpython3u;
```

作為函式定義本體所給定的那段 Python 程式碼，會被轉換成一個 Python 函式。例如，上面的例子會產生：

```

def __plpython_procedure_pymax_23456():
  if a > b:
    return a
  return b
```

這裡假設 23456 是 PostgreSQL 指派給該函式的 OID。

引數會被設定成全域變數。由於 Python 的作用範圍規則，這會導致一個微妙的結果：在函式內部，不能把某個引數變數重新指派為「含有該變數名稱本身」的運算式之值，除非該變數在該區塊中被重新宣告為 global。例如，下面的寫法不會成功：

```

CREATE FUNCTION pystrip(x text)
  RETURNS text
AS $$
  x = x.strip()  # error
  return x
$$ LANGUAGE plpython3u;
```

因為對 `x` 進行指派會使 `x` 在整個區塊中成為區域變數，於是指派式右側的 `x` 指的是尚未指派值的區域變數 `x`，而不是 PL/Python 的函式參數。使用 `global` 陳述式就可以讓它正常運作：

```

CREATE FUNCTION pystrip(x text)
  RETURNS text
AS $$
  global x
  x = x.strip()  # ok now
  return x
$$ LANGUAGE plpython3u;
```

但我們建議不要依賴 PL/Python 的這個實作細節。比較好的做法是把函式參數視為唯讀。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-funcs.html)（原文版本：18.6；核對日期：2026-09-13）
