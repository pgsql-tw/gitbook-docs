## 5.4. Generated Columns [#](#DDL-GENERATED-COLUMNS)

<a id="id-1.5.4.6.2"></a>

A generated column is a special column that is always computed from other
columns. Thus, it is for columns what a view is for tables. There are two
kinds of generated columns: stored and virtual. A stored generated column
is computed when it is written (inserted or updated) and occupies storage
as if it were a normal column. A virtual generated column occupies no
storage and is computed when it is read. Thus, a virtual generated column
is similar to a view and a stored generated column is similar to a
materialized view (except that it is always updated automatically).

To create a generated column, use the `GENERATED ALWAYS
AS` clause in `CREATE TABLE`, for example:

```

CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54)
);
```

A generated column is by default of the virtual kind. Use the keywords
`VIRTUAL` or `STORED` to make the choice
explicit. See [CREATE TABLE](../../reference/sql-commands/sql-createtable.md) for more details.

A generated column cannot be written to directly. In
`INSERT` or `UPDATE` commands, a value
cannot be specified for a generated column, but the keyword
`DEFAULT` may be specified.

Consider the differences between a column with a default and a generated
column. The column default is evaluated once when the row is first
inserted if no other value was provided; a generated column is updated
whenever the row changes and cannot be overridden. A column default may
not refer to other columns of the table; a generation expression would
normally do so. A column default can use volatile functions, for example
`random()` or functions referring to the current time;
this is not allowed for generated columns.

Several restrictions apply to the definition of generated columns and
tables involving generated columns:

* The generation expression can only use immutable functions and cannot
  use subqueries or reference anything other than the current row in any
  way.
* A generation expression cannot reference another generated column.
* A generation expression cannot reference a system column, except
  `tableoid`.
* A virtual generated column cannot have a user-defined type, and the
  generation expression of a virtual generated column must not reference
  user-defined functions or types, that is, it can only use built-in
  functions or types. This applies also indirectly, such as for functions
  or types that underlie operators or casts. (This restriction does not
  exist for stored generated columns.)
* A generated column cannot have a column default or an identity definition.
* A generated column cannot be part of a partition key.
* Foreign tables can have generated columns. See [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md) for details.
* For inheritance and partitioning:

  * If a parent column is a generated column, its child column must also
    be a generated column of the same kind (stored or virtual); however,
    the child column can have a different generation expression.

    For stored generated columns, the generation expression that is
    actually applied during insert or update of a row is the one
    associated with the table that the row is physically in. (This is
    unlike the behavior for column defaults: for those, the default value
    associated with the table named in the query applies.) For virtual
    generated columns, the generation expression of the table named in the
    query applies when a table is read.
  * If a parent column is not a generated column, its child column must
    not be generated either.
  * For inherited tables, if you write a child column definition without
    any `GENERATED` clause in `CREATE TABLE
    ... INHERITS`, then its `GENERATED` clause
    will automatically be copied from the parent. `ALTER TABLE
    ... INHERIT` will insist that parent and child columns
    already match as to generation status, but it will not require their
    generation expressions to match.
  * Similarly for partitioned tables, if you write a child column
    definition without any `GENERATED` clause
    in `CREATE TABLE ... PARTITION OF`, then
    its `GENERATED` clause will automatically be copied
    from the parent. `ALTER TABLE ... ATTACH PARTITION`
    will insist that parent and child columns already match as to
    generation status, but it will not require their generation
    expressions to match.
  * In case of multiple inheritance, if one parent column is a generated
    column, then all parent columns must be generated columns. If they
    do not all have the same generation expression, then the desired
    expression for the child must be specified explicitly.

Additional considerations apply to the use of generated columns.

* Generated columns maintain access privileges separately from their
  underlying base columns. So, it is possible to arrange it so that a
  particular role can read from a generated column but not from the
  underlying base columns.

  For virtual generated columns, this is only fully secure if the
  generation expression uses only leakproof functions (see [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)), but this is not enforced by the system.
* Privileges of functions used in generation expressions are checked when
  the expression is actually executed, on write or read respectively, as
  if the generation expression had been called directly from the query
  using the generated column. The user of a generated column must have
  permissions to call all functions used by the generation expression.
  Functions in the generation expression are executed with the privileges
  of the user executing the query or the function owner, depending on
  whether the functions are defined as `SECURITY INVOKER`
  or `SECURITY DEFINER`.
* Generated columns are, conceptually, updated after
  `BEFORE` triggers have run. Therefore, changes made to
  base columns in a `BEFORE` trigger will be reflected in
  generated columns. But conversely, it is not allowed to access
  generated columns in `BEFORE` triggers.
* Generated columns are allowed to be replicated during logical replication
  according to the `CREATE PUBLICATION` parameter
  [`publish_generated_columns`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) or by including them
  in the column list of the `CREATE PUBLICATION` command.
  This is currently only supported for stored generated columns.
  See [Section 29.6](../../server-administration/logical-replication/logical-replication-gencols.md) for details.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-generated-columns.html)（英文原文，待翻譯）
