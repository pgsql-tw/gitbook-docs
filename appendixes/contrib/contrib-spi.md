## F.41. spi — Server Programming Interface features/examples [#](#CONTRIB-SPI)

[F.41.1. refint — Functions for Implementing Referential Integrity](contrib-spi.md#CONTRIB-SPI-REFINT)

[F.41.2. autoinc — Functions for Autoincrementing Fields](contrib-spi.md#CONTRIB-SPI-AUTOINC)

[F.41.3. insert_username — Functions for Tracking Who Changed a Table](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)

[F.41.4. moddatetime — Functions for Tracking Last Modification Time](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

<a id="id-1.11.7.51.2"></a>

The spi module provides several workable examples
of using the [Server Programming Interface](../../server-programming/spi/README.md)
(SPI) and triggers. While these functions are of
some value in
their own right, they are even more useful as examples to modify for
your own purposes. The functions are general enough to be used
with any table, but you have to specify table and field names (as described
below) while creating a trigger.

Each of the groups of functions described below is provided as a
separately-installable extension.

<a id="CONTRIB-SPI-REFINT"></a>

### F.41.1. refint — Functions for Implementing Referential Integrity [#](#CONTRIB-SPI-REFINT)

`check_primary_key()` and
`check_foreign_key()` are used to check foreign key constraints.
(This functionality is long since superseded by the built-in foreign
key mechanism, of course, but the module is still useful as an example.
This module will be removed in PostgreSQL 20.)

### Note

`refint` requires a
[secure schema usage pattern](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS) and
data types where the equality operator is named `=`.

`check_primary_key()` checks the referencing table.
To use, create an `AFTER INSERT OR UPDATE` trigger using this
function on a table referencing another table. Specify as the trigger
arguments: the referencing table's column name(s) which form the foreign
key, the referenced table name, and the column names in the referenced table
which form the primary/unique key. To handle multiple foreign
keys, create a trigger for each reference.

### Note

The *referenced* table name and column name arguments to
`check_primary_key()` are copied as-is into internally
generated SQL statements and therefore must be double-quoted by the user as
necessary in the `CREATE TRIGGER` command. See
[Section 4.1.1](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS) for more information about quoting
SQL identifiers. Conversely, the *referencing* table
column name arguments should not be double quoted. See the following mock
example of proper use of `check_primary_key()`:

```

CREATE TRIGGER mytrigger
AFTER INSERT OR UPDATE ON referencing_table
FOR EACH ROW EXECUTE PROCEDURE
check_primary_key (
    'column A', 'column B',         -- referencing table columns
    'myschema."referenced table"',  -- referenced table
    '"column A"', '"column B"'      -- referenced table columns
);
```

`check_foreign_key()` checks the referenced table.
To use, create an `AFTER DELETE OR UPDATE` trigger using this
function on a table referenced by other table(s). Specify as the trigger
arguments: the number of referencing tables for which the function has to
perform checking, the action if a referencing key is found
(`cascade` — to delete the referencing row,
`restrict` — to abort transaction if referencing keys
exist, `setnull` — to set referencing key fields to null),
the referenced table's column names which form the primary/unique key, then
the referencing table name and column names (repeated for as many
referencing tables as were specified by first argument). Note that the
primary/unique key columns should be marked NOT NULL and should have a
unique index.

### Note

The *referencing* table name and column name arguments
to `check_foreign_key()` are copied as-is into
internally generated SQL statements and therefore must be double-quoted by
the user as necessary in the `CREATE TRIGGER` command.
See [Section 4.1.1](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS) for more information about
quoting SQL identifiers. Conversely, the *referenced*
table column name arguments should not be double quoted. See the following
mock example of proper use of `check_foreign_key()`:

```

CREATE TRIGGER mytrigger
AFTER DELETE OR UPDATE ON referenced_table
FOR EACH ROW EXECUTE PROCEDURE
check_foreign_key (
    1,                              -- number of referencing tables
    'cascade',                      -- action
    'column A', 'column B',         -- referenced table columns
    'myschema."referencing table"', -- referencing table
    '"column A"', '"column B"'      -- referencing table columns
);
```

Note that if these triggers are executed from
another `BEFORE` trigger, they can fail unexpectedly. For
example, if a user inserts row1 and then the `BEFORE`
trigger inserts row2 and calls a trigger with the
`check_foreign_key()`,
the `check_foreign_key()`
function will not see row1 and will fail.

There are examples in `refint.example`.

<a id="CONTRIB-SPI-AUTOINC"></a>

### F.41.2. autoinc — Functions for Autoincrementing Fields [#](#CONTRIB-SPI-AUTOINC)

`autoinc()` is a trigger that stores the next value of
a sequence into an integer field. This has some overlap with the
built-in “serial column” feature, but it is not the same.
The trigger will replace the field's value only if that value is
initially zero or null (after the action of the SQL statement that
inserted or updated the row). Also, if the sequence's next value is
zero, `nextval()` will be called a second time in
order to obtain a non-zero value.

To use, create a `BEFORE INSERT` (or optionally `BEFORE
INSERT OR UPDATE`) trigger using this function. Specify two
trigger arguments: the name of the integer column to be modified,
and the name of the sequence object that will supply values.
(Actually, you can specify any number of pairs of such names, if
you'd like to update more than one autoincrementing column.)

There is an example in `autoinc.example`.

<a id="CONTRIB-SPI-INSERT-USERNAME"></a>

### F.41.3. insert_username — Functions for Tracking Who Changed a Table [#](#CONTRIB-SPI-INSERT-USERNAME)

`insert_username()` is a trigger that stores the current
user's name into a text field. This can be useful for tracking
who last modified a particular row within a table.

To use, create a `BEFORE INSERT` and/or `UPDATE`
trigger using this function. Specify a single trigger
argument: the name of the text column to be modified.

There is an example in `insert_username.example`.

<a id="CONTRIB-SPI-MODDATETIME"></a>

### F.41.4. moddatetime — Functions for Tracking Last Modification Time [#](#CONTRIB-SPI-MODDATETIME)

`moddatetime()` is a trigger that stores the current
time into a `timestamp` field. This can be useful for tracking
the last modification time of a particular row within a table.

To use, create a `BEFORE UPDATE`
trigger using this function. Specify a single trigger
argument: the name of the column to be modified.
The column must be of type `timestamp` or `timestamp with
time zone`.

There is an example in `moddatetime.example`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-spi.html)（英文原文，待翻譯）
