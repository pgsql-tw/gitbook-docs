<a id="SQL-CLOSE"></a><a id="id-1.9.3.50.1"></a><a id="id-1.9.3.50.2"></a>

# CLOSE

CLOSE — close a cursor

## Synopsis

```

CLOSE { name | ALL }
```

<a id="id-1.9.3.50.6"></a>

## Description

`CLOSE` frees the resources associated with an open cursor. After the cursor is closed, no subsequent operations are allowed on it. A cursor should be closed when it is no longer needed.

Every non-holdable open cursor is implicitly closed when a transaction is terminated by `COMMIT` or `ROLLBACK`. A holdable cursor is implicitly closed if the transaction that created it aborts via `ROLLBACK`. If the creating transaction successfully commits, the holdable cursor remains open until an explicit `CLOSE` is executed, or the client disconnects.

<a id="id-1.9.3.50.7"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of an open cursor to close.

`ALL`

Close all open cursors.

<a id="id-1.9.3.50.8"></a>

## Notes

PostgreSQL does not have an explicit `OPEN` cursor statement; a cursor is considered open when it is declared. Use the [`DECLARE`](declare.md) statement to declare a cursor.

You can see all available cursors by querying the [`pg_cursors`](../../internals/system-views/pg_cursors.md) system view.

If a cursor is closed after a savepoint which is later rolled back, the `CLOSE` is not rolled back; that is, the cursor remains closed.

<a id="id-1.9.3.50.9"></a>

## Examples

Close the cursor `liahona`:

```

CLOSE liahona;
```

<a id="id-1.9.3.50.10"></a>

## Compatibility

`CLOSE` is fully conforming with the SQL standard. `CLOSE ALL` is a PostgreSQL extension.

<a id="id-1.9.3.50.11"></a>

## See Also

[DECLARE](declare.md), [FETCH](fetch.md), [MOVE](move.md)

---

原文：[PostgreSQL 15.19 Documentation](close.md)（英文原文，待翻譯）
