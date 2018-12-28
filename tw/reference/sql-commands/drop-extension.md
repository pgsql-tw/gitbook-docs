---
description: 版本：11
---

# DROP EXTENSION

DROP EXTENSION — remove an extension

### Synopsis

```text
DROP EXTENSION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### Description

`DROP EXTENSION` removes extensions from the database. Dropping an extension causes its component objects to be dropped as well.

You must own the extension to use `DROP EXTENSION`.

### Parameters

`IF EXISTS`

Do not throw an error if the extension does not exist. A notice is issued in this case.

_`name`_

The name of an installed extension.

`CASCADE`

Automatically drop objects that depend on the extension, and in turn all objects that depend on those objects \(see [Section 5.13](https://www.postgresql.org/docs/11/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the extension if any objects depend on it \(other than its own member objects and other extensions listed in the same `DROP` command\). This is the default.

### Examples

To remove the extension `hstore` from the current database:

```text
DROP EXTENSION hstore;
```

This command will fail if any of `hstore`'s objects are in use in the database, for example if any tables have columns of the `hstore` type. Add the `CASCADE` option to forcibly remove those dependent objects as well.

### Compatibility

`DROP EXTENSION` is a PostgreSQL extension.

### See Also

[CREATE EXTENSION](create-extension.md), [ALTER EXTENSION](alter-extension.md)

