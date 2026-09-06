## 5.7. Modifying Tables [#](#DDL-ALTER)

[5.7.1. Adding a Column](ddl-alter.md#DDL-ALTER-ADDING-A-COLUMN)

[5.7.2. Removing a Column](ddl-alter.md#DDL-ALTER-REMOVING-A-COLUMN)

[5.7.3. Adding a Constraint](ddl-alter.md#DDL-ALTER-ADDING-A-CONSTRAINT)

[5.7.4. Removing a Constraint](ddl-alter.md#DDL-ALTER-REMOVING-A-CONSTRAINT)

[5.7.5. Changing a Column's Default Value](ddl-alter.md#DDL-ALTER-COLUMN-DEFAULT)

[5.7.6. Changing a Column's Data Type](ddl-alter.md#DDL-ALTER-COLUMN-TYPE)

[5.7.7. Renaming a Column](ddl-alter.md#DDL-ALTER-RENAMING-COLUMN)

[5.7.8. Renaming a Table](ddl-alter.md#DDL-ALTER-RENAMING-TABLE)

<a id="id-1.5.4.9.2"></a>

When you create a table and you realize that you made a mistake, or
the requirements of the application change, you can drop the
table and create it again. But this is not a convenient option if
the table is already filled with data, or if the table is
referenced by other database objects (for instance a foreign key
constraint). Therefore PostgreSQL
provides a family of commands to make modifications to existing
tables. Note that this is conceptually distinct from altering
the data contained in the table: here we are interested in altering
the definition, or structure, of the table.

You can:

* Add columns
* Remove columns
* Add constraints
* Remove constraints
* Change default values
* Change column data types
* Rename columns
* Rename tables

All these actions are performed using the
[ALTER TABLE](../../reference/sql-commands/sql-altertable.md)
command, whose reference page contains details beyond those given
here.

<a id="DDL-ALTER-ADDING-A-COLUMN"></a>

### 5.7.1. Adding a Column [#](#DDL-ALTER-ADDING-A-COLUMN)

<a id="id-1.5.4.9.5.2"></a>

To add a column, use a command like:

```

ALTER TABLE products ADD COLUMN description text;
```

The new column is initially filled with whatever default
value is given (null if you don't specify a `DEFAULT` clause).

### Tip

Adding a column with a constant default value does not require each row of
the table to be updated when the `ALTER TABLE` statement
is executed. Instead, the default value will be returned the next time
the row is accessed, and applied when the table is rewritten, making
the `ALTER TABLE` very fast even on large tables.

If the default value is volatile (e.g., `clock_timestamp()`)
each row will need to be updated with the value calculated at the time
`ALTER TABLE` is executed. To avoid a potentially
lengthy update operation, particularly if you intend to fill the column
with mostly nondefault values anyway, it may be preferable to add the
column with no default, insert the correct values using
`UPDATE`, and then add any desired default as described
below.

You can also define constraints on the column at the same time,
using the usual syntax:

```

ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

In fact all the options that can be applied to a column description
in `CREATE TABLE` can be used here. Keep in mind however
that the default value must satisfy the given constraints, or the
`ADD` will fail. Alternatively, you can add
constraints later (see below) after you've filled in the new column
correctly.

<a id="DDL-ALTER-REMOVING-A-COLUMN"></a>

### 5.7.2. Removing a Column [#](#DDL-ALTER-REMOVING-A-COLUMN)

<a id="id-1.5.4.9.6.2"></a>

To remove a column, use a command like:

```

ALTER TABLE products DROP COLUMN description;
```

Whatever data was in the column disappears. Table constraints involving
the column are dropped, too. However, if the column is referenced by a
foreign key constraint of another table,
PostgreSQL will not silently drop that
constraint. You can authorize dropping everything that depends on
the column by adding `CASCADE`:

```

ALTER TABLE products DROP COLUMN description CASCADE;
```

See [Section 5.15](ddl-depend.md) for a description of the general
mechanism behind this.

<a id="DDL-ALTER-ADDING-A-CONSTRAINT"></a>

### 5.7.3. Adding a Constraint [#](#DDL-ALTER-ADDING-A-CONSTRAINT)

<a id="id-1.5.4.9.7.2"></a>

To add a constraint, the table constraint syntax is used. For example:

```

ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

To add a not-null constraint, which is normally not written as a table
constraint, this special syntax is available:

```

ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

This command silently does nothing if the column already has a
not-null constraint.

The constraint will be checked immediately, so the table data must
satisfy the constraint before it can be added.

<a id="DDL-ALTER-REMOVING-A-CONSTRAINT"></a>

### 5.7.4. Removing a Constraint [#](#DDL-ALTER-REMOVING-A-CONSTRAINT)

<a id="id-1.5.4.9.8.2"></a>

To remove a constraint you need to know its name. If you gave it
a name then that's easy. Otherwise the system assigned a
generated name, which you need to find out. The
psql command `\d
tablename` can be helpful
here; other interfaces might also provide a way to inspect table
details. Then the command is:

```

ALTER TABLE products DROP CONSTRAINT some_name;
```

As with dropping a column, you need to add `CASCADE` if you
want to drop a constraint that something else depends on. An example
is that a foreign key constraint depends on a unique or primary key
constraint on the referenced column(s).

Simplified syntax is available to drop a not-null constraint:

```

ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

This mirrors the `SET NOT NULL` syntax for adding a
not-null constraint. This command will silently do nothing if the column
does not have a not-null constraint. (Recall that a column can have at
most one not-null constraint, so it is never ambiguous which constraint
this command acts on.)

<a id="DDL-ALTER-COLUMN-DEFAULT"></a>

### 5.7.5. Changing a Column's Default Value [#](#DDL-ALTER-COLUMN-DEFAULT)

<a id="id-1.5.4.9.9.2"></a>

To set a new default for a column, use a command like:

```

ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

Note that this doesn't affect any existing rows in the table, it
just changes the default for future `INSERT` commands.

To remove any default value, use:

```

ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

This is effectively the same as setting the default to null.
As a consequence, it is not an error
to drop a default where one hadn't been defined, because the
default is implicitly the null value.

<a id="DDL-ALTER-COLUMN-TYPE"></a>

### 5.7.6. Changing a Column's Data Type [#](#DDL-ALTER-COLUMN-TYPE)

<a id="id-1.5.4.9.10.2"></a>

To convert a column to a different data type, use a command like:

```

ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

This will succeed only if each existing entry in the column can be
converted to the new type by an implicit cast. If a more complex
conversion is needed, you can add a `USING` clause that
specifies how to compute the new values from the old.

PostgreSQL will attempt to convert the column's
default value (if any) to the new type, as well as any constraints
that involve the column. But these conversions might fail, or might
produce surprising results. It's often best to drop any constraints
on the column before altering its type, and then add back suitably
modified constraints afterwards.

<a id="DDL-ALTER-RENAMING-COLUMN"></a>

### 5.7.7. Renaming a Column [#](#DDL-ALTER-RENAMING-COLUMN)

<a id="id-1.5.4.9.11.2"></a>

To rename a column:

```

ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

<a id="DDL-ALTER-RENAMING-TABLE"></a>

### 5.7.8. Renaming a Table [#](#DDL-ALTER-RENAMING-TABLE)

<a id="id-1.5.4.9.12.2"></a>

To rename a table:

```

ALTER TABLE products RENAME TO items;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-alter.html)（英文原文，待翻譯）
