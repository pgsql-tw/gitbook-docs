## 44.9. Utility Functions [#](#PLPYTHON-UTIL)

The `plpy` module also provides the functions

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">plpy.debug(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.log(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.info(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.notice(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.warning(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.error(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr><tr><td><code class="literal">plpy.fatal(<em class="replaceable"><code>msg, **kwargs</code></em>)</code></td></tr></table>

<a id="id-1.8.11.17.2.3"></a>
`plpy.error` and `plpy.fatal`
actually raise a Python exception which, if uncaught, propagates out to
the calling query, causing the current transaction or subtransaction to
be aborted. `raise plpy.Error(msg)` and
`raise plpy.Fatal(msg)` are
equivalent to calling `plpy.error(msg)` and
`plpy.fatal(msg)`, respectively but
the `raise` form does not allow passing keyword arguments.
The other functions only generate messages of different priority levels.
Whether messages of a particular priority are reported to the client,
written to the server log, or both is controlled by the
[log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) and
[client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) configuration
variables. See [Chapter 19](../../server-administration/runtime-config/README.md) for more information.

The *`msg`* argument is given as a positional argument. For
backward compatibility, more than one positional argument can be given. In
that case, the string representation of the tuple of positional arguments
becomes the message reported to the client.

The following keyword-only arguments are accepted:

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">detail</code></td></tr><tr><td><code class="literal">hint</code></td></tr><tr><td><code class="literal">sqlstate</code></td></tr><tr><td><code class="literal">schema_name</code></td></tr><tr><td><code class="literal">table_name</code></td></tr><tr><td><code class="literal">column_name</code></td></tr><tr><td><code class="literal">datatype_name</code></td></tr><tr><td><code class="literal">constraint_name</code></td></tr></table>

The string representation of the objects passed as keyword-only arguments
is used to enrich the messages reported to the client. For example:

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

Another set of utility functions are
`plpy.quote_literal(string)`,
`plpy.quote_nullable(string)`, and
`plpy.quote_ident(string)`. They
are equivalent to the built-in quoting functions described in [Section 9.4](../../the-sql-language/functions/functions-string.md). They are useful when constructing
ad-hoc queries. A PL/Python equivalent of dynamic SQL from [Example 41.1](../plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE) would be:

```

plpy.execute("UPDATE tbl SET %s = %s WHERE key = %s" % (
    plpy.quote_ident(colname),
    plpy.quote_nullable(newvalue),
    plpy.quote_literal(keyvalue)))
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-util.html)（英文原文，待翻譯）
