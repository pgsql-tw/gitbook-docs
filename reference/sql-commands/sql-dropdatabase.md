<a id="id-1.9.3.108.1"></a>

## DROP DATABASE

DROP DATABASE — remove a database

## Synopsis

```

DROP DATABASE [ IF EXISTS ] name [ [ WITH ] ( option [, ...] ) ]

where option can be:

    FORCE
```

<a id="id-1.9.3.108.5"></a>

## Description

`DROP DATABASE` drops a database. It removes the
catalog entries for the database and deletes the directory
containing the data. It can only be executed by the database owner.
It cannot be executed while you are connected to the target database.
(Connect to `postgres` or any other database to issue this
command.)
Also, if anyone else is connected to the target database, this command will
fail unless you use the `FORCE` option described below.

`DROP DATABASE` cannot be undone. Use it with care!

<a id="id-1.9.3.108.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the database does not exist. A notice is issued
    in this case.

*`name`*
:   The name of the database to remove.

`FORCE`
:   Attempt to terminate all existing connections to the target database.
    It doesn't terminate if prepared transactions, active logical replication
    slots or subscriptions are present in the target database.

    This terminates background worker connections and connections that the
    current user has permission to terminate
    with `pg_terminate_backend`, described in
    [Section 9.28.2](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL). If connections would remain,
    this command will fail.

<a id="id-1.9.3.108.7"></a>

## Notes

`DROP DATABASE` cannot be executed inside a transaction
block.

This command cannot be executed while connected to the target
database. Thus, it might be more convenient to use the program
[dropdb](../reference-client/app-dropdb.md) instead,
which is a wrapper around this command.

<a id="id-1.9.3.108.8"></a>

## Compatibility

There is no `DROP DATABASE` statement in the SQL standard.

<a id="id-1.9.3.108.9"></a>

## See Also

[CREATE DATABASE](sql-createdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropdatabase.html)（英文原文，待翻譯）
