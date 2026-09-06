<a id="SQL-ROLLBACK-TO"></a><a id="id-1.9.3.169.1"></a><a id="id-1.9.3.169.2"></a>

# ROLLBACK TO SAVEPOINT

ROLLBACK TO SAVEPOINT — roll back to a savepoint

## Synopsis

```

ROLLBACK [ WORK | TRANSACTION ] TO [ SAVEPOINT ] savepoint_name
```

<a id="id-1.9.3.169.6"></a>

## Description

Roll back all commands that were executed after the savepoint was established. The savepoint remains valid and can be rolled back to again later, if needed.

`ROLLBACK TO SAVEPOINT` implicitly destroys all savepoints that were established after the named savepoint.

<a id="id-1.9.3.169.7"></a>

## Parameters

<em class="replaceable"><code>savepoint&#95;name</code></em>

The savepoint to roll back to.

<a id="id-1.9.3.169.8"></a>

## Notes

Use [`RELEASE SAVEPOINT`](release-savepoint.md) to destroy a savepoint without discarding the effects of commands executed after it was established.

Specifying a savepoint name that has not been established is an error.

Cursors have somewhat non-transactional behavior with respect to savepoints. Any cursor that is opened inside a savepoint will be closed when the savepoint is rolled back. If a previously opened cursor is affected by a `FETCH` or `MOVE` command inside a savepoint that is later rolled back, the cursor remains at the position that `FETCH` left it pointing to (that is, the cursor motion caused by `FETCH` is not rolled back). Closing a cursor is not undone by rolling back, either. However, other side-effects caused by the cursor's query (such as side-effects of volatile functions called by the query) <em>are</em> rolled back if they occur during a savepoint that is later rolled back. A cursor whose execution causes a transaction to abort is put in a cannot-execute state, so while the transaction can be restored using `ROLLBACK TO SAVEPOINT`, the cursor can no longer be used.

<a id="id-1.9.3.169.9"></a>

## Examples

To undo the effects of the commands executed after `my_savepoint` was established:

```

ROLLBACK TO SAVEPOINT my_savepoint;
```

Cursor positions are not affected by savepoint rollback:

```

BEGIN;

DECLARE foo CURSOR FOR SELECT 1 UNION SELECT 2;

SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        1

ROLLBACK TO SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        2

COMMIT;
```

<a id="id-1.9.3.169.10"></a>

## Compatibility

The SQL standard specifies that the key word `SAVEPOINT` is mandatory, but PostgreSQL and Oracle allow it to be omitted. SQL allows only `WORK`, not `TRANSACTION`, as a noise word after `ROLLBACK`. Also, SQL has an optional clause `AND [ NO ] CHAIN` which is not currently supported by PostgreSQL. Otherwise, this command conforms to the SQL standard.

<a id="id-1.9.3.169.11"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [RELEASE SAVEPOINT](release-savepoint.md), [ROLLBACK](rollback.md), [SAVEPOINT](savepoint.md)

---

原文：[PostgreSQL 15.19 Documentation](rollback-to-savepoint.md)（英文原文，待翻譯）
