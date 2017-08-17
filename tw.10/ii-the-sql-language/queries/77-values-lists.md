# 7.7. 列舉資料[^1]

`VALUES`provides a way to generate a“constant table”that can be used in a query without having to actually create and populate a table on-disk. The syntax is

```
VALUES ( 
expression
 [, ...] ) [, ...]

```

Each parenthesized list of expressions generates a row in the table. The lists must all have the same number of elements \(i.e., the number of columns in the table\), and corresponding entries in each list must have compatible data types. The actual data type assigned to each column of the result is determined using the same rules as for`UNION`\(see[Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html)\).

As an example:

```
VALUES (1, 'one'), (2, 'two'), (3, 'three');

```

will return a table of two columns and three rows. It's effectively equivalent to:

```
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';

```

By default,PostgreSQLassigns the names`column1`,`column2`, etc. to the columns of a`VALUES`table. The column names are not specified by the SQL standard and different database systems do it differently, so it's usually better to override the default names with a table alias list, like this:

```
=
>
 SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t (num,letter);
 num | letter
-----+--------
   1 | one
   2 | two
   3 | three
(3 rows)

```

Syntactically,`VALUES`followed by expression lists is treated as equivalent to:

```
SELECT 
select_list
 FROM 
table_expression
```

and can appear anywhere a`SELECT`can. For example, you can use it as part of a`UNION`, or attach a_`sort_specification`_\(`ORDER BY`,`LIMIT`, and/or`OFFSET`\) to it.`VALUES`is most commonly used as the data source in an`INSERT`command, and next most commonly as a subquery.

For more information see[VALUES](https://www.postgresql.org/docs/10/static/sql-values.html).

  


---



[^1]: [PostgreSQL: Documentation: 10: 7.7. VALUES Lists](https://www.postgresql.org/docs/10/static/queries-values.html)

