<a id="SQL-RELEASE-SAVEPOINT"></a><a id="id-1.9.3.164.1"></a><a id="id-1.9.3.164.2"></a>

# RELEASE SAVEPOINT

RELEASE SAVEPOINT — destroy a previously defined savepoint

## Synopsis

```

RELEASE [ SAVEPOINT ] savepoint_name
```

<a id="id-1.9.3.164.6"></a>

## Description

`RELEASE SAVEPOINT` destroys a savepoint previously defined in the current transaction.

Destroying a savepoint makes it unavailable as a rollback point, but it has no other user visible behavior. It does not undo the effects of commands executed after the savepoint was established. (To do that, see [ROLLBACK TO SAVEPOINT](rollback-to-savepoint.md).) Destroying a savepoint when it is no longer needed allows the system to reclaim some resources earlier than transaction end.

`RELEASE SAVEPOINT` also destroys all savepoints that were established after the named savepoint was established.

<a id="id-1.9.3.164.7"></a>

## Parameters

<em class="replaceable"><code>savepoint&#95;name</code></em>

The name of the savepoint to destroy.

<a id="id-1.9.3.164.8"></a>

## Notes

Specifying a savepoint name that was not previously defined is an error.

It is not possible to release a savepoint when the transaction is in an aborted state.

If multiple savepoints have the same name, only the most recently defined unreleased one is released. Repeated commands will release progressively older savepoints.

<a id="id-1.9.3.164.9"></a>

## Examples

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

<a id="id-1.9.3.164.10"></a>

## Compatibility

This command conforms to the SQL standard. The standard specifies that the key word `SAVEPOINT` is mandatory, but PostgreSQL allows it to be omitted.

<a id="id-1.9.3.164.11"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [ROLLBACK](rollback.md), [ROLLBACK TO SAVEPOINT](rollback-to-savepoint.md), [SAVEPOINT](savepoint.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-release-savepoint.html)（英文原文，待翻譯）
