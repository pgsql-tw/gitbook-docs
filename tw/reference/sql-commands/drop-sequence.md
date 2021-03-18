# DROP SEQUENCE

DROP SEQUENCE — remove a sequence

### Synopsis

```text
DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### Description

`DROP SEQUENCE` removes sequence number generators. A sequence can only be dropped by its owner or a superuser.

### Parameters

`IF EXISTS`

Do not throw an error if the sequence does not exist. A notice is issued in this case.

_`name`_

The name \(optionally schema-qualified\) of a sequence.

`CASCADE`

Automatically drop objects that depend on the sequence, and in turn all objects that depend on those objects \(see [Section 5.14](https://www.postgresql.org/docs/13/ddl-depend.html)\).`RESTRICT`

Refuse to drop the sequence if any objects depend on it. This is the default.

### Examples

To remove the sequence `serial`:

```text
DROP SEQUENCE serial;
```

### Compatibility

`DROP SEQUENCE` conforms to the SQL standard, except that the standard only allows one sequence to be dropped per command, and apart from the `IF EXISTS` option, which is a PostgreSQL extension.

### See Also

[CREATE SEQUENCE](https://www.postgresql.org/docs/13/sql-createsequence.html), [ALTER SEQUENCE](https://www.postgresql.org/docs/13/sql-altersequence.html)  


