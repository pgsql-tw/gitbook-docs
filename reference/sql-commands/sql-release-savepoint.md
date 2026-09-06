<a id="id-1.9.3.164.1"></a><a id="id-1.9.3.164.2"></a>

## RELEASE SAVEPOINT

RELEASE SAVEPOINT — release a previously defined savepoint

## Synopsis

```

RELEASE [ SAVEPOINT ] savepoint_name
```

<a id="id-1.9.3.164.6"></a>

## Description

`RELEASE SAVEPOINT` releases the named savepoint and
all active savepoints that were created after the named savepoint,
and frees their resources. All changes made since the creation of
the savepoint that didn't already get rolled back are merged into
the transaction or savepoint that was active when the named savepoint
was created. Changes made after `RELEASE SAVEPOINT`
will also be part of this active transaction or savepoint.

<a id="id-1.9.3.164.7"></a>

## Parameters

*`savepoint_name`*
:   The name of the savepoint to release.

<a id="id-1.9.3.164.8"></a>

## Notes

Specifying a savepoint name that was not previously defined is an error.

It is not possible to release a savepoint when the transaction is in
an aborted state; to do that, use [ROLLBACK TO SAVEPOINT](sql-rollback-to.md).

If multiple savepoints have the same name, only the most recently defined
unreleased one is released. Repeated commands will release progressively
older savepoints.

<a id="id-1.9.3.164.9"></a>

## Examples

To establish and later release a savepoint:

```

BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

The above transaction will insert both 3 and 4.

A more complex example with multiple nested subtransactions:

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT sp1;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT sp2;
    INSERT INTO table1 VALUES (3);
    RELEASE SAVEPOINT sp2;
    INSERT INTO table1 VALUES (4))); -- generates an error
```

In this example, the application requests the release of the savepoint
`sp2`, which inserted 3. This changes the insert's
transaction context to `sp1`. When the statement
attempting to insert value 4 generates an error, the insertion of 2 and
4 are lost because they are in the same, now-rolled back savepoint,
and value 3 is in the same transaction context. The application can
now only choose one of these two commands, since all other commands
will be ignored:

```

ROLLBACK;
ROLLBACK TO SAVEPOINT sp1;
```

Choosing `ROLLBACK` will abort everything, including
value 1, whereas `ROLLBACK TO SAVEPOINT sp1` will retain
value 1 and allow the transaction to continue.

<a id="id-1.9.3.164.10"></a>

## Compatibility

This command conforms to the SQL standard. The standard
specifies that the key word `SAVEPOINT` is
mandatory, but PostgreSQL allows it to
be omitted.

<a id="id-1.9.3.164.11"></a>

## See Also

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md), [ROLLBACK TO SAVEPOINT](sql-rollback-to.md), [SAVEPOINT](sql-savepoint.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-release-savepoint.html)（英文原文，待翻譯）
