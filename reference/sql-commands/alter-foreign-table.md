<a id="SQL-ALTERFOREIGNTABLE"></a><a id="id-1.9.3.13.1"></a>

# ALTER FOREIGN TABLE

ALTER FOREIGN TABLE — change the definition of a foreign table

## Synopsis

```

ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    action [, ... ]
ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    RENAME TO new_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    SET SCHEMA new_schema

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    ALTER [ COLUMN ] column_name OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
    ADD table_constraint [ NOT VALID ]
    VALIDATE CONSTRAINT constraint_name
    DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE REPLICA TRIGGER trigger_name
    ENABLE ALWAYS TRIGGER trigger_name
    SET WITHOUT OIDS
    INHERIT parent_table
    NO INHERIT parent_table
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
    OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
```

<a id="id-1.9.3.13.5"></a>

## Description

`ALTER FOREIGN TABLE` changes the definition of an existing foreign table. There are several subforms:

`ADD [ COLUMN ] [ IF NOT EXISTS ]`

This form adds a new column to the foreign table, using the same syntax as [`CREATE FOREIGN TABLE`](create-foreign-table.md). If `IF NOT EXISTS` is specified and a column already exists with this name, no error is thrown. Unlike the case when adding a column to a regular table, nothing happens to the underlying storage: this action simply declares that some new column is now accessible through the foreign table.

`DROP [ COLUMN ] [ IF EXISTS ]`

This form drops a column from a foreign table. You will need to say `CASCADE` if anything outside the table depends on the column; for example, views. If `IF EXISTS` is specified and the column does not exist, no error is thrown. In this case a notice is issued instead.

`SET DATA TYPE`

This form changes the type of a column of a foreign table. Again, this has no effect on any underlying storage: this action simply changes the type that PostgreSQL believes the column to have.

`SET`/`DROP DEFAULT`

These forms set or remove the default value for a column. Default values only apply in subsequent `INSERT` or `UPDATE` commands; they do not cause rows already in the table to change.

`SET`/`DROP NOT NULL`

Mark a column as allowing, or not allowing, null values.

`SET STATISTICS`

This form sets the per-column statistics-gathering target for subsequent [`ANALYZE`](analyze.md) operations. See the similar form of [`ALTER TABLE`](alter-table.md) for more details.

<code class="literal">SET ( <em class="replaceable"><code>attribute&#95;option</code></em> = <em class="replaceable"><code>value</code></em> &#91;, ... &#93; )</code><br><code class="literal">RESET ( <em class="replaceable"><code>attribute&#95;option</code></em> &#91;, ... &#93; )</code>

This form sets or resets per-attribute options. See the similar form of [`ALTER TABLE`](alter-table.md) for more details.

`SET STORAGE`

This form sets the storage mode for a column. See the similar form of [`ALTER TABLE`](alter-table.md) for more details. Note that the storage mode has no effect unless the table's foreign-data wrapper chooses to pay attention to it.

<code class="literal">ADD <em class="replaceable"><code>table&#95;constraint</code></em> &#91; NOT VALID &#93;</code>

This form adds a new constraint to a foreign table, using the same syntax as [`CREATE FOREIGN TABLE`](create-foreign-table.md). Currently only `CHECK` constraints are supported.

Unlike the case when adding a constraint to a regular table, nothing is done to verify the constraint is correct; rather, this action simply declares that some new condition should be assumed to hold for all rows in the foreign table. (See the discussion in [`CREATE FOREIGN TABLE`](create-foreign-table.md).) If the constraint is marked `NOT VALID`, then it isn't assumed to hold, but is only recorded for possible future use.

`VALIDATE CONSTRAINT`

This form marks as valid a constraint that was previously marked as `NOT VALID`. No action is taken to verify the constraint, but future queries will assume that it holds.

`DROP CONSTRAINT [ IF EXISTS ]`

This form drops the specified constraint on a foreign table. If `IF EXISTS` is specified and the constraint does not exist, no error is thrown. In this case a notice is issued instead.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER`

These forms configure the firing of trigger(s) belonging to the foreign table. See the similar form of [`ALTER TABLE`](alter-table.md) for more details.

`SET WITHOUT OIDS`

Backward compatibility syntax for removing the `oid` system column. As `oid` system columns cannot be added anymore, this never has an effect.

<code class="literal">INHERIT <em class="replaceable"><code>parent&#95;table</code></em></code>

This form adds the target foreign table as a new child of the specified parent table. See the similar form of [`ALTER TABLE`](alter-table.md) for more details.

<code class="literal">NO INHERIT <em class="replaceable"><code>parent&#95;table</code></em></code>

This form removes the target foreign table from the list of children of the specified parent table.

`OWNER`

This form changes the owner of the foreign table to the specified user.

<code class="literal">OPTIONS ( &#91; ADD | SET | DROP &#93; <em class="replaceable"><code>option</code></em> &#91;'<em class="replaceable"><code>value</code></em>'&#93; &#91;, ... &#93; )</code>

Change options for the foreign table or one of its columns. `ADD`, `SET`, and `DROP` specify the action to be performed. `ADD` is assumed if no operation is explicitly specified. Duplicate option names are not allowed (although it's OK for a table option and a column option to have the same name). Option names and values are also validated using the foreign data wrapper library.

`RENAME`

The `RENAME` forms change the name of a foreign table or the name of an individual column in a foreign table.

`SET SCHEMA`

This form moves the foreign table into another schema.

All the actions except `RENAME` and `SET SCHEMA` can be combined into a list of multiple alterations to apply in parallel. For example, it is possible to add several columns and/or alter the type of several columns in a single command.

If the command is written as `ALTER FOREIGN TABLE IF EXISTS ...` and the foreign table does not exist, no error is thrown. A notice is issued in this case.

You must own the table to use `ALTER FOREIGN TABLE`. To change the schema of a foreign table, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the table's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the table. However, a superuser can alter ownership of any table anyway.) To add a column or alter a column type, you must also have `USAGE` privilege on the data type.

<a id="id-1.9.3.13.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (possibly schema-qualified) of an existing foreign table to alter. If `ONLY` is specified before the table name, only that table is altered. If `ONLY` is not specified, the table and all its descendant tables (if any) are altered. Optionally, `*` can be specified after the table name to explicitly indicate that descendant tables are included.

<em class="replaceable"><code>column&#95;name</code></em>

Name of a new or existing column.

<em class="replaceable"><code>new&#95;column&#95;name</code></em>

New name for an existing column.

<em class="replaceable"><code>new&#95;name</code></em>

New name for the table.

<em class="replaceable"><code>data&#95;type</code></em>

Data type of the new column, or new data type for an existing column.

<em class="replaceable"><code>table&#95;constraint</code></em>

New table constraint for the foreign table.

<em class="replaceable"><code>constraint&#95;name</code></em>

Name of an existing constraint to drop.

`CASCADE`

Automatically drop objects that depend on the dropped column or constraint (for example, views referencing the column), and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the column or constraint if there are any dependent objects. This is the default behavior.

<em class="replaceable"><code>trigger&#95;name</code></em>

Name of a single trigger to disable or enable.

`ALL`

Disable or enable all triggers belonging to the foreign table. (This requires superuser privilege if any of the triggers are internally generated triggers. The core system does not add such triggers to foreign tables, but add-on code could do so.)

`USER`

Disable or enable all triggers belonging to the foreign table except for internally generated triggers.

<em class="replaceable"><code>parent&#95;table</code></em>

A parent table to associate or de-associate with this foreign table.

<em class="replaceable"><code>new&#95;owner</code></em>

The user name of the new owner of the table.

<em class="replaceable"><code>new&#95;schema</code></em>

The name of the schema to which the table will be moved.

<a id="id-1.9.3.13.7"></a>

## Notes

The key word `COLUMN` is noise and can be omitted.

Consistency with the foreign server is not checked when a column is added or removed with `ADD COLUMN` or `DROP COLUMN`, a `NOT NULL` or `CHECK` constraint is added, or a column type is changed with `SET DATA TYPE`. It is the user's responsibility to ensure that the table definition matches the remote side.

Refer to [`CREATE FOREIGN TABLE`](create-foreign-table.md) for a further description of valid parameters.

<a id="id-1.9.3.13.8"></a>

## Examples

To mark a column as not-null:

```

ALTER FOREIGN TABLE distributors ALTER COLUMN street SET NOT NULL;
```

To change options of a foreign table:

```

ALTER FOREIGN TABLE myschema.distributors OPTIONS (ADD opt1 'value', SET opt2 'value2', DROP opt3);
```

<a id="id-1.9.3.13.9"></a>

## Compatibility

The forms `ADD`, `DROP`, and `SET DATA TYPE` conform with the SQL standard. The other forms are PostgreSQL extensions of the SQL standard. Also, the ability to specify more than one manipulation in a single `ALTER FOREIGN TABLE` command is an extension.

`ALTER FOREIGN TABLE DROP COLUMN` can be used to drop the only column of a foreign table, leaving a zero-column table. This is an extension of SQL, which disallows zero-column foreign tables.

<a id="id-1.9.3.13.10"></a>

## See Also

[CREATE FOREIGN TABLE](create-foreign-table.md), [DROP FOREIGN TABLE](drop-foreign-table.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-foreign-table.md)（英文原文，待翻譯）
