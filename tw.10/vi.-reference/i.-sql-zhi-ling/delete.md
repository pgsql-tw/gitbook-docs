# DELETE

DELETE — delete rows of a table

## Synopsis

```text
[ WITH [ RECURSIVE ] 
with_query
 [, ...] ]
DELETE FROM [ ONLY ] 
table_name
 [ * ] [ [ AS ] 
alias
 ]
    [ USING 
using_list
 ]
    [ WHERE 
condition
 | WHERE CURRENT OF 
cursor_name
 ]
    [ RETURNING * | 
output_expression
 [ [ AS ] 
output_name
 ] [, ...] ]
```

## Description

`DELETE`deletes rows that satisfy the`WHERE`clause from the specified table. If the`WHERE`clause is absent, the effect is to delete all rows in the table. The result is a valid, but empty table.

### Tip

[TRUNCATE](https://www.postgresql.org/docs/10/static/sql-truncate.html)provides a faster mechanism to remove all rows from a table.

There are two ways to delete rows in a table using information contained in other tables in the database: using sub-selects, or specifying additional tables in the`USING`clause. Which technique is more appropriate depends on the specific circumstances.

The optional`RETURNING`clause causes`DELETE`to compute and return value\(s\) based on each row actually deleted. Any expression using the table's columns, and/or columns of other tables mentioned in`USING`, can be computed. The syntax of the`RETURNING`list is identical to that of the output list of`SELECT`.

You must have the`DELETE`privilege on the table to delete from it, as well as the`SELECT`privilege for any table in the`USING`clause or whose values are read in the`condition`.

## Parameters

`with_query`

The`WITH`clause allows you to specify one or more subqueries that can be referenced by name in the`DELETE`query. See[Section 7.8](https://www.postgresql.org/docs/10/static/queries-with.html)and[SELECT](https://www.postgresql.org/docs/10/static/sql-select.html)for details.

`table_name`

The name \(optionally schema-qualified\) of the table to delete rows from. If`ONLY`is specified before the table name, matching rows are deleted from the named table only. If`ONLY`is not specified, matching rows are also deleted from any tables inheriting from the named table. Optionally,`*`can be specified after the table name to explicitly indicate that descendant tables are included.

`alias`

A substitute name for the target table. When an alias is provided, it completely hides the actual name of the table. For example, given`DELETE FROM foo AS f`, the remainder of the`DELETE`statement must refer to this table as`f`not`foo`.

`using_list`

A list of table expressions, allowing columns from other tables to appear in the`WHERE`condition. This is similar to the list of tables that can be specified in the[`FROM`Clause](https://www.postgresql.org/docs/10/static/sql-select.html#SQL-FROM)of a`SELECT`statement; for example, an alias for the table name can be specified. Do not repeat the target table in the`using_list`, unless you wish to set up a self-join.

`condition`

An expression that returns a value of type`boolean`. Only rows for which this expression returns`true`will be deleted.

`cursor_name`

The name of the cursor to use in a`WHERE CURRENT OF`condition. The row to be deleted is the one most recently fetched from this cursor. The cursor must be a non-grouping query on the`DELETE`'s target table. Note that`WHERE CURRENT OF`cannot be specified together with a Boolean condition. See[DECLARE](https://www.postgresql.org/docs/10/static/sql-declare.html)for more information about using cursors with`WHERE CURRENT OF`.

`output_expression`

An expression to be computed and returned by the`DELETE`command after each row is deleted. The expression can use any column names of the table named by\_`table_name`\_or table\(s\) listed in`USING`. Write`*`to return all columns.

`output_name`

A name to use for a returned column.

## Outputs

On successful completion, a`DELETE`command returns a command tag of the form

```text
DELETE 
count
```

The`count`_\_is the number of rows deleted. Note that the number may be less than the number of rows that matched the_`condition`_when deletes were suppressed by a_`BEFORE DELETE`_trigger. If_`count`\_is 0, no rows were deleted by the query \(this is not considered an error\).

If the`DELETE`command contains a`RETURNING`clause, the result will be similar to that of a`SELECT`statement containing the columns and values defined in the`RETURNING`list, computed over the row\(s\) deleted by the command.

## Notes

PostgreSQLlets you reference columns of other tables in the`WHERE`condition by specifying the other tables in the`USING`clause. For example, to delete all films produced by a given producer, one can do:

```text
DELETE FROM films USING producers
  WHERE producer_id = producers.id AND producers.name = 'foo';
```

What is essentially happening here is a join between`films`and`producers`, with all successfully joined`films`rows being marked for deletion. This syntax is not standard. A more standard way to do it is:

```text
DELETE FROM films
  WHERE producer_id IN (SELECT id FROM producers WHERE name = 'foo');
```

In some cases the join style is easier to write or faster to execute than the sub-select style.

## Examples

Delete all films but musicals:

```text
DELETE FROM films WHERE kind 
<
>
 'Musical';
```

Clear the table`films`:

```text
DELETE FROM films;
```

Delete completed tasks, returning full details of the deleted rows:

```text
DELETE FROM tasks WHERE status = 'DONE' RETURNING *;
```

Delete the row of`tasks`on which the cursor`c_tasks`is currently positioned:

```text
DELETE FROM tasks WHERE CURRENT OF c_tasks;
```

## Compatibility

This command conforms to theSQLstandard, except that the`USING`and`RETURNING`clauses arePostgreSQLextensions, as is the ability to use`WITH`with`DELETE`.

## See Also

[TRUNCATE](https://www.postgresql.org/docs/10/static/sql-truncate.html)

