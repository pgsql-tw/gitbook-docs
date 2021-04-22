# DROP DATABASE

DROP DATABASE — remove a database

## Synopsis

```text
DROP DATABASE [ IF EXISTS ] name
```

## Description

`DROP DATABASE` drops a database. It removes the catalog entries for the database and deletes the directory containing the data. It can only be executed by the database owner. Also, it cannot be executed while you or anyone else are connected to the target database. \(Connect to `postgres` or any other database to issue this command.\)

`DROP DATABASE` cannot be undone. Use it with care!

## Parameters

`IF EXISTS`

Do not throw an error if the database does not exist. A notice is issued in this case.

_`name`_

The name of the database to remove.

## Notes

`DROP DATABASE` cannot be executed inside a transaction block.

This command cannot be executed while connected to the target database. Thus, it might be more convenient to use the program [dropdb](https://www.postgresql.org/docs/10/static/app-dropdb.html) instead, which is a wrapper around this command.

## Compatibility

There is no `DROP DATABASE` statement in the SQL standard.

## See Also

[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html)

