<a id="SQL-SAVEPOINT"></a><a id="id-1.9.3.170.1"></a><a id="id-1.9.3.170.2"></a>

# SAVEPOINT

SAVEPOINT — define a new savepoint within the current transaction

## Synopsis

```

SAVEPOINT savepoint_name
```

<a id="id-1.9.3.170.6"></a>

## Description

`SAVEPOINT` establishes a new savepoint within the current transaction.

A savepoint is a special mark inside a transaction that allows all commands that are executed after it was established to be rolled back, restoring the transaction state to what it was at the time of the savepoint.

<a id="id-1.9.3.170.7"></a>

## Parameters

<em class="replaceable"><code>savepoint&#95;name</code></em>

The name to give to the new savepoint. If savepoints with the same name already exist, they will be inaccessible until newer identically-named savepoints are released.

<a id="id-1.9.3.170.8"></a>

## Notes

Use [`ROLLBACK TO`](rollback-to-savepoint.md) to rollback to a savepoint. Use [`RELEASE SAVEPOINT`](release-savepoint.md) to destroy a savepoint, keeping the effects of commands executed after it was established.

Savepoints can only be established when inside a transaction block. There can be multiple savepoints defined within a transaction.

<a id="id-1.9.3.170.9"></a>

## Examples

To establish a savepoint and later undo the effects of all commands executed after it was established:

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    ROLLBACK TO SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);
COMMIT;
```

The above transaction will insert the values 1 and 3, but not 2.

To establish and later destroy a savepoint:

```

BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

The above transaction will insert both 3 and 4.

To use a single savepoint name:

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);

    -- rollback to the second savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows rows 1 and 2

    -- release the second savepoint
    RELEASE SAVEPOINT my_savepoint;

    -- rollback to the first savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows only row 1
COMMIT;
```

The above transaction shows row 3 being rolled back first, then row 2.

<a id="id-1.9.3.170.10"></a>

## Compatibility

SQL requires a savepoint to be destroyed automatically when another savepoint with the same name is established. In PostgreSQL, the old savepoint is kept, though only the more recent one will be used when rolling back or releasing. (Releasing the newer savepoint with `RELEASE SAVEPOINT` will cause the older one to again become accessible to `ROLLBACK TO SAVEPOINT` and `RELEASE SAVEPOINT`.) Otherwise, `SAVEPOINT` is fully SQL conforming.

<a id="id-1.9.3.170.11"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [RELEASE SAVEPOINT](release-savepoint.md), [ROLLBACK](rollback.md), [ROLLBACK TO SAVEPOINT](rollback-to-savepoint.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-savepoint.html)（英文原文，待翻譯）
