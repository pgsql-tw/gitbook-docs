<a id="PLPYTHON-UTIL"></a>

## 44.9. 公用函式 [#](#PLPYTHON-UTIL)

`plpy` 模組還提供了下列函式

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">plpy.debug(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.log(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.info(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.notice(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.warning(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.error(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.fatal(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr></table>

<a id="id-1.8.11.17.2.3"></a>
`plpy.error` 與 `plpy.fatal` 實際上會拋出一個 Python 例外，若未被攔截，就會向外傳播到呼叫的查詢，使目前的交易或子交易中止。`raise plpy.Error(msg)` 與 `raise plpy.Fatal(msg)` 分別等同於呼叫 `plpy.error(msg)` 與 `plpy.fatal(msg)`，但 `raise` 的形式不允許傳入關鍵字引數。其餘的函式則只會產生不同優先層級的訊息。特定優先層級的訊息是否回報給用戶端、寫入伺服器日誌或兩者皆是，由 [log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 與 [client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 這兩個組態變數控制。更多資訊請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

*`msg`* 引數是以位置引數的方式給定。為了向後相容，也可以給定多個位置引數。在那種情況下，這組位置引數所構成之 tuple（值組）的字串表示法就會成為回報給用戶端的訊息。

以下這些只能以關鍵字形式給定的引數是被接受的：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">detail</code></td></tr><tr><td><code class="literal">hint</code></td></tr><tr><td><code class="literal">sqlstate</code></td></tr><tr><td><code class="literal">schema_name</code></td></tr><tr><td><code class="literal">table_name</code></td></tr><tr><td><code class="literal">column_name</code></td></tr><tr><td><code class="literal">datatype_name</code></td></tr><tr><td><code class="literal">constraint_name</code></td></tr></table>

以關鍵字引數傳入之物件的字串表示法，會被用來豐富回報給用戶端的訊息。例如：

```

CREATE FUNCTION raise_custom_exception() RETURNS void AS $$
plpy.error("custom exception message",
           detail="some info about exception",
           hint="hint for users")
$$ LANGUAGE plpython3u;

=# SELECT raise_custom_exception();
ERROR:  plpy.Error: custom exception message
DETAIL:  some info about exception
HINT:  hint for users
CONTEXT:  Traceback (most recent call last):
  PL/Python function "raise_custom_exception", line 4, in <module>
    hint="hint for users")
PL/Python function "raise_custom_exception"
```

另一組公用函式是 `plpy.quote_literal(string)`、`plpy.quote_nullable(string)` 與 `plpy.quote_ident(string)`。它們等同於[第 9.4 節](../../the-sql-language/functions/functions-string.md)所描述的內建引號處理函式，在組建臨時查詢時相當有用。[範例 41.1](../plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE) 中的動態 SQL 若改寫成 PL/Python 版本，會是：

```

plpy.execute("UPDATE tbl SET %s = %s WHERE key = %s" % (
    plpy.quote_ident(colname),
    plpy.quote_nullable(newvalue),
    plpy.quote_literal(keyvalue)))
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-util.html)（原文版本：18.6；核對日期：2026-09-13）
