## 41.9. Errors and Messages [#](#PLPGSQL-ERRORS-AND-MESSAGES)

[41.9.1. Reporting Errors and Messages](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)

[41.9.2. Checking Assertions](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

<a id="PLPGSQL-STATEMENTS-RAISE"></a>

### 41.9.1. Reporting Errors and Messages [#](#PLPGSQL-STATEMENTS-RAISE)

<a id="id-1.8.8.11.2.2"></a><a id="id-1.8.8.11.2.3"></a>

Use the `RAISE` statement to report messages and
raise errors.

```

RAISE [ level ] 'format' [, expression [, ... ]] [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] condition_name [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] SQLSTATE 'sqlstate' [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] USING option { = | := } expression [, ... ];
RAISE ;
```

The *`level`* option specifies
the error severity. Allowed levels are `DEBUG`,
`LOG`, `INFO`,
`NOTICE`, `WARNING`,
and `EXCEPTION`, with `EXCEPTION`
being the default.
`EXCEPTION` raises an error (which normally aborts the
current transaction); the other levels only generate messages of different
priority levels.
Whether messages of a particular priority are reported to the client,
written to the server log, or both is controlled by the
[log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) and
[client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) configuration
variables. See [Chapter 19](../../server-administration/runtime-config/README.md) for more
information.

In the first syntax variant,
after the *`level`* if any,
write a *`format`* string
(which must be a simple string literal, not an expression). The
format string specifies the error message text to be reported.
The format string can be followed
by optional argument expressions to be inserted into the message.
Inside the format string, `%` is replaced by the
string representation of the next optional argument's value. Write
`%%` to emit a literal `%`.
The number of arguments must match the number of `%`
placeholders in the format string, or an error is raised during
the compilation of the function.

In this example, the value of `v_job_id` will replace the
`%` in the string:

```

RAISE NOTICE 'Calling cs_create_job(%)', v_job_id;
```

In the second and third syntax variants,
*`condition_name`* and
*`sqlstate`* specify an
error condition name or a five-character SQLSTATE code, respectively.
See [Appendix A](../../appendixes/errcodes-appendix/README.md) for the valid error condition
names and the predefined SQLSTATE codes.

Here are examples
of *`condition_name`*
and *`sqlstate`* usage:

```

RAISE division_by_zero;
RAISE WARNING SQLSTATE '22012';
```

In any of these syntax variants,
you can attach additional information to the error report by writing
`USING` followed by *`option`* = *`expression`* items. Each
*`expression`* can be any
string-valued expression. The allowed *`option`* key words are:

<a id="RAISE-USING-OPTIONS"></a>

<a id="RAISE-USING-OPTION-MESSAGE"></a>

`MESSAGE` [#](#RAISE-USING-OPTION-MESSAGE)
:   Sets the error message text. This option can't be used in the
    first syntax variant, since the message is already supplied.
<a id="RAISE-USING-OPTION-DETAIL"></a>

`DETAIL` [#](#RAISE-USING-OPTION-DETAIL)
:   Supplies an error detail message.
<a id="RAISE-USING-OPTION-HINT"></a>

`HINT` [#](#RAISE-USING-OPTION-HINT)
:   Supplies a hint message.
<a id="RAISE-USING-OPTION-ERRCODE"></a>

`ERRCODE` [#](#RAISE-USING-OPTION-ERRCODE)
:   Specifies the error code (SQLSTATE) to report, either by condition
    name, as shown in [Appendix A](../../appendixes/errcodes-appendix/README.md), or directly as a
    five-character SQLSTATE code. This option can't be used in the
    second or third syntax variant, since the error code is already
    supplied.
<a id="RAISE-USING-OPTION-COLUMN"></a>

`COLUMN`<br>`CONSTRAINT`<br>`DATATYPE`<br>`TABLE`<br>`SCHEMA` [#](#RAISE-USING-OPTION-COLUMN)
:   Supplies the name of a related object.

This example will abort the transaction with the given error message
and hint:

```

RAISE EXCEPTION 'Nonexistent ID --> %', user_id
      USING HINT = 'Please check your user ID';
```

These two examples show equivalent ways of setting the SQLSTATE:

```

RAISE 'Duplicate user ID: %', user_id USING ERRCODE = 'unique_violation';
RAISE 'Duplicate user ID: %', user_id USING ERRCODE = '23505';
```

Another way to produce the same result is:

```

RAISE unique_violation USING MESSAGE = 'Duplicate user ID: ' || user_id;
```

As shown in the fourth syntax variant, it is also possible to
write `RAISE USING` or `RAISE
level USING` and put
everything else into the `USING` list.

The last variant of `RAISE` has no parameters at all.
This form can only be used inside a `BEGIN` block's
`EXCEPTION` clause;
it causes the error currently being handled to be re-thrown.

### Note

Before PostgreSQL 9.1, `RAISE` without
parameters was interpreted as re-throwing the error from the block
containing the active exception handler. Thus an `EXCEPTION`
clause nested within that handler could not catch it, even if the
`RAISE` was within the nested `EXCEPTION` clause's
block. This was deemed surprising as well as being incompatible with
Oracle's PL/SQL.

If no condition name nor SQLSTATE is specified in a
`RAISE EXCEPTION` command, the default is to use
`raise_exception` (`P0001`).
If no message text is specified, the default is to use the condition
name or SQLSTATE as message text.

### Note

When specifying an error code by SQLSTATE code, you are not
limited to the predefined error codes, but can select any
error code consisting of five digits and/or upper-case ASCII
letters, other than `00000`. It is recommended that
you avoid throwing error codes that end in three zeroes, because
these are category codes and can only be trapped by trapping
the whole category.

<a id="PLPGSQL-STATEMENTS-ASSERT"></a>

### 41.9.2. Checking Assertions [#](#PLPGSQL-STATEMENTS-ASSERT)

<a id="id-1.8.8.11.3.2"></a><a id="id-1.8.8.11.3.3"></a><a id="id-1.8.8.11.3.4"></a>

The `ASSERT` statement is a convenient shorthand for
inserting debugging checks into PL/pgSQL
functions.

```

ASSERT condition [ , message ];
```

The *`condition`* is a Boolean
expression that is expected to always evaluate to true; if it does,
the `ASSERT` statement does nothing further. If the
result is false or null, then an `ASSERT_FAILURE` exception
is raised. (If an error occurs while evaluating
the *`condition`*, it is
reported as a normal error.)

If the optional *`message`* is
provided, it is an expression whose result (if not null) replaces the
default error message text “assertion failed”, should
the *`condition`* fail.
The *`message`* expression is
not evaluated in the normal case where the assertion succeeds.

Testing of assertions can be enabled or disabled via the configuration
parameter `plpgsql.check_asserts`, which takes a Boolean
value; the default is `on`. If this parameter
is `off` then `ASSERT` statements do nothing.

Note that `ASSERT` is meant for detecting program
bugs, not for reporting ordinary error conditions. Use
the `RAISE` statement, described above, for that.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-errors-and-messages.html)（英文原文，待翻譯）
