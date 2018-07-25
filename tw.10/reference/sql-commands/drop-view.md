# DROP VIEW

DROP VIEW — remove a view

### Synopsis

```text
DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### Description

`DROP VIEW` drops an existing view. To execute this command you must be the owner of the view.

### Parameters

`IF EXISTS`

Do not throw an error if the view does not exist. A notice is issued in this case.

_`name`_

The name \(optionally schema-qualified\) of the view to remove.

`CASCADE`

Automatically drop objects that depend on the view \(such as other views\), and in turn all objects that depend on those objects \(see [Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the view if any objects depend on it. This is the default.

### Examples

This command will remove the view called `kinds`:

```text
DROP VIEW kinds;
```

### Compatibility

This command conforms to the SQL standard, except that the standard only allows one view to be dropped per command, and apart from the `IF EXISTS` option, which is a PostgreSQLextension.

### See Also

[ALTER VIEW](alter-view.md), [CREATE VIEW](create-view.md)

