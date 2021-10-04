# DROP ACCESS METHOD

DROP ACCESS METHOD — remove an access method

### Synopsis

```text
DROP ACCESS METHOD [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

### Description

`DROP ACCESS METHOD` removes an existing access method. Only superusers can drop access methods.

### Parameters

`IF EXISTS`

Do not throw an error if the access method does not exist. A notice is issued in this case.

_`name`_

The name of an existing access method.

`CASCADE`

Automatically drop objects that depend on the access method \(such as operator classes, operator families, and indexes\), and in turn all objects that depend on those objects \(see [Section 5.14](https://www.postgresql.org/docs/13/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the access method if any objects depend on it. This is the default.

### Examples

Drop the access method `heptree`:

```text
DROP ACCESS METHOD heptree;
```

### Compatibility

`DROP ACCESS METHOD` is a PostgreSQL extension.

### See Also

[CREATE ACCESS METHOD](https://www.postgresql.org/docs/13/sql-create-access-method.html)

