# ALTER TYPE

ALTER TYPE — change the definition of a type

## Synopsis

```text
ALTER TYPE name action [, ... ]
ALTER TYPE name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER TYPE name RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
ALTER TYPE name RENAME TO new_name
ALTER TYPE name SET SCHEMA new_schema
ALTER TYPE name ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } neighbor_enum_value ]
ALTER TYPE name RENAME VALUE existing_enum_value TO new_enum_value

where action is one of:

    ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
    DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
    ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
```

## Description

`ALTER TYPE` changes the definition of an existing type. There are several subforms:`ADD ATTRIBUTE`

This form adds a new attribute to a composite type, using the same syntax as [CREATE TYPE](https://www.postgresql.org/docs/10/static/sql-createtype.html).`DROP ATTRIBUTE [ IF EXISTS ]`

This form drops an attribute from a composite type. If `IF EXISTS` is specified and the attribute does not exist, no error is thrown. In this case a notice is issued instead.`SET DATA TYPE`

This form changes the type of an attribute of a composite type.`OWNER`

This form changes the owner of the type.`RENAME`

This form changes the name of the type or the name of an individual attribute of a composite type.`SET SCHEMA`

This form moves the type into another schema.`ADD VALUE [ IF NOT EXISTS ] [ BEFORE | AFTER ]`

This form adds a new value to an enum type. The new value's place in the enum's ordering can be specified as being `BEFORE` or `AFTER` one of the existing values. Otherwise, the new item is added at the end of the list of values.

If `IF NOT EXISTS` is specified, it is not an error if the type already contains the new value: a notice is issued but no other action is taken. Otherwise, an error will occur if the new value is already present.`RENAME VALUE`

This form renames a value of an enum type. The value's place in the enum's ordering is not affected. An error will occur if the specified value is not present or the new name is already present.

The `ADD ATTRIBUTE`, `DROP ATTRIBUTE`, and `ALTER ATTRIBUTE` actions can be combined into a list of multiple alterations to apply in parallel. For example, it is possible to add several attributes and/or alter the type of several attributes in a single command.

You must own the type to use `ALTER TYPE`. To change the schema of a type, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the type's schema. \(These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the type. However, a superuser can alter ownership of any type anyway.\) To add an attribute or alter an attribute type, you must also have `USAGE` privilege on the data type.

## Parameters

_`name`_

The name \(possibly schema-qualified\) of an existing type to alter.

_`new_name`_

The new name for the type.

_`new_owner`_

The user name of the new owner of the type.

_`new_schema`_

The new schema for the type.

_`attribute_name`_

The name of the attribute to add, alter, or drop.

_`new_attribute_name`_

The new name of the attribute to be renamed.

_`data_type`_

The data type of the attribute to add, or the new type of the attribute to alter.

_`new_enum_value`_

The new value to be added to an enum type's list of values, or the new name to be given to an existing value. Like all enum literals, it needs to be quoted.

_`neighbor_enum_value`_

The existing enum value that the new value should be added immediately before or after in the enum type's sort ordering. Like all enum literals, it needs to be quoted.

_`existing_enum_value`_

The existing enum value that should be renamed. Like all enum literals, it needs to be quoted.

`CASCADE`

Automatically propagate the operation to typed tables of the type being altered, and their descendants.

`RESTRICT`

Refuse the operation if the type being altered is the type of a typed table. This is the default.

## Notes

`ALTER TYPE ... ADD VALUE` \(the form that adds a new value to an enum type\) cannot be executed inside a transaction block.

Comparisons involving an added enum value will sometimes be slower than comparisons involving only original members of the enum type. This will usually only occur if `BEFORE` or `AFTER` is used to set the new value's sort position somewhere other than at the end of the list. However, sometimes it will happen even though the new value is added at the end \(this occurs if the OID counter “wrapped around” since the original creation of the enum type\). The slowdown is usually insignificant; but if it matters, optimal performance can be regained by dropping and recreating the enum type, or by dumping and reloading the database.

## Examples

To rename a data type:

```text
ALTER TYPE electronic_mail RENAME TO email;
```

To change the owner of the type `email` to `joe`:

```text
ALTER TYPE email OWNER TO joe;
```

To change the schema of the type `email` to `customers`:

```text
ALTER TYPE email SET SCHEMA customers;
```

To add a new attribute to a type:

```text
ALTER TYPE compfoo ADD ATTRIBUTE f3 int;
```

To add a new value to an enum type in a particular sort position:

```text
ALTER TYPE colors ADD VALUE 'orange' AFTER 'red';
```

To rename an enum value:

```text
ALTER TYPE colors RENAME VALUE 'purple' TO 'mauve';
```

## Compatibility

The variants to add and drop attributes are part of the SQL standard; the other variants are PostgreSQL extensions.

## See Also

[CREATE TYPE](https://www.postgresql.org/docs/10/static/sql-createtype.html), [DROP TYPE](https://www.postgresql.org/docs/10/static/sql-droptype.html)

