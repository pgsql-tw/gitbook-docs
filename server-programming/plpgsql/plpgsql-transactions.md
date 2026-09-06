## 41.8. Transaction Management [#](#PLPGSQL-TRANSACTIONS)

In procedures invoked by the `CALL` command
as well as in anonymous code blocks (`DO` command),
it is possible to end transactions using the
commands `COMMIT` and `ROLLBACK`. A new
transaction is started automatically after a transaction is ended using
these commands, so there is no separate `START
TRANSACTION` command. (Note that `BEGIN` and
`END` have different meanings in PL/pgSQL.)

Here is a simple example:

```

CREATE PROCEDURE transaction_test1()
LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..9 LOOP
        INSERT INTO test1 (a) VALUES (i);
        IF i % 2 = 0 THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
    END LOOP;
END;
$$;

CALL transaction_test1();
```

<a id="id-1.8.8.10.4"></a><a id="PLPGSQL-TRANSACTION-CHAIN"></a>

A new transaction starts out with default transaction characteristics such
as transaction isolation level. In cases where transactions are committed
in a loop, it might be desirable to start new transactions automatically
with the same characteristics as the previous one. The commands
`COMMIT AND CHAIN` and `ROLLBACK AND
CHAIN` accomplish this.

Transaction control is only possible in `CALL` or
`DO` invocations from the top level or nested
`CALL` or `DO` invocations without any
other intervening command. For example, if the call stack is
`CALL proc1()` → `CALL proc2()`
→ `CALL proc3()`, then the second and third
procedures can perform transaction control actions. But if the call stack
is `CALL proc1()` → `SELECT
func2()` → `CALL proc3()`, then the last
procedure cannot do transaction control, because of the
`SELECT` in between.

PL/pgSQL does not support savepoints
(`SAVEPOINT`/`ROLLBACK TO
SAVEPOINT`/`RELEASE SAVEPOINT` commands).
Typical usage patterns for savepoints can be replaced by blocks with
exception handlers (see [Section 41.6.8](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)).
Under the hood, a block with exception handlers forms a
subtransaction, which means that transactions cannot be ended inside
such a block.

Special considerations apply to cursor loops. Consider this example:

```

CREATE PROCEDURE transaction_test2()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM test2 ORDER BY x LOOP
        INSERT INTO test1 (a) VALUES (r.x);
        COMMIT;
    END LOOP;
END;
$$;

CALL transaction_test2();
```

Normally, cursors are automatically closed at transaction commit.
However, a cursor created as part of a loop like this is automatically
converted to a holdable cursor by the first `COMMIT` or
`ROLLBACK`. That means that the cursor is fully
evaluated at the first `COMMIT` or
`ROLLBACK` rather than row by row. The cursor is still
removed automatically after the loop, so this is mostly invisible to the
user. But one must keep in mind that any table or row locks taken by
the cursor's query will no longer be held after the
first `COMMIT` or
`ROLLBACK`.

Transaction commands are not allowed in cursor loops driven by commands
that are not read-only (for example `UPDATE
... RETURNING`).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-transactions.html)（英文原文，待翻譯）
