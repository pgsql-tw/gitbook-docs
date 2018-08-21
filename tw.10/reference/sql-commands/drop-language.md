# DROP LANGUAGE

DROP LANGUAGE — remove a procedural language

### Synopsis

```text
DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

### Description

`DROP LANGUAGE` removes the definition of a previously registered procedural language. You must be a superuser or the owner of the language to use `DROP LANGUAGE`.

#### Note

As of PostgreSQL 9.1, most procedural languages have been made into “extensions”, and should therefore be removed with [DROP EXTENSION](https://www.postgresql.org/docs/10/static/sql-dropextension.html) not `DROP LANGUAGE`.

### Parameters

`IF EXISTS`

Do not throw an error if the language does not exist. A notice is issued in this case.

_`name`_

The name of an existing procedural language. For backward compatibility, the name can be enclosed by single quotes.

`CASCADE`

Automatically drop objects that depend on the language \(such as functions in the language\), and in turn all objects that depend on those objects \(see [Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the language if any objects depend on it. This is the default.

### Examples

This command removes the procedural language `plsample`:

```text
DROP LANGUAGE plsample;
```

### Compatibility

There is no `DROP LANGUAGE` statement in the SQL standard.

### See Also

[ALTER LANGUAGE](alter-language.md), [CREATE LANGUAGE](create-language.md)

