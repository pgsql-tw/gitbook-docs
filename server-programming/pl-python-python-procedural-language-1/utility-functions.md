# 46.9. Utility Functions

The `plpy` module also provides the functions

| `plpy.debug(`_`msg, **kwargs`_`)`   |
| ----------------------------------- |
| `plpy.log(`_`msg, **kwargs`_`)`     |
| `plpy.info(`_`msg, **kwargs`_`)`    |
| `plpy.notice(`_`msg, **kwargs`_`)`  |
| `plpy.warning(`_`msg, **kwargs`_`)` |
| `plpy.error(`_`msg, **kwargs`_`)`   |
| `plpy.fatal(`_`msg, **kwargs`_`)`   |

`plpy.error` and `plpy.fatal` actually raise a Python exception which, if uncaught, propagates out to the calling query, causing the current transaction or subtransaction to be aborted. `raise plpy.Error(`_`msg`_`)` and `raise plpy.Fatal(`_`msg`_`)` are equivalent to calling `plpy.error(`_`msg`_`)` and `plpy.fatal(`_`msg`_`)`, respectively but the `raise` form does not allow passing keyword arguments. The other functions only generate messages of different priority levels. Whether messages of a particular priority are reported to the client, written to the server log, or both is controlled by the [log\_min\_messages](https://www.postgresql.org/docs/15/runtime-config-logging.html#GUC-LOG-MIN-MESSAGES) and [client\_min\_messages](https://www.postgresql.org/docs/15/runtime-config-client.html#GUC-CLIENT-MIN-MESSAGES) configuration variables. See [Chapter 20](https://www.postgresql.org/docs/15/runtime-config.html) for more information.

The _`msg`_ argument is given as a positional argument. For backward compatibility, more than one positional argument can be given. In that case, the string representation of the tuple of positional arguments becomes the message reported to the client.

The following keyword-only arguments are accepted:

| `detail`          |
| ----------------- |
| `hint`            |
| `sqlstate`        |
| `schema_name`     |
| `table_name`      |
| `column_name`     |
| `datatype_name`   |
| `constraint_name` |

The string representation of the objects passed as keyword-only arguments is used to enrich the messages reported to the client. For example:

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

Another set of utility functions are `plpy.quote_literal(`_`string`_`)`, `plpy.quote_nullable(`_`string`_`)`, and `plpy.quote_ident(`_`string`_`)`. They are equivalent to the built-in quoting functions described in [Section 9.4](https://www.postgresql.org/docs/15/functions-string.html). They are useful when constructing ad-hoc queries. A PL/Python equivalent of dynamic SQL from [Example 43.1](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE) would be:

```
plpy.execute("UPDATE tbl SET %s = %s WHERE key = %s" % (
    plpy.quote_ident(colname),
    plpy.quote_nullable(newvalue),
    plpy.quote_literal(keyvalue)))
```
