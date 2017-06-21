# 7.8. 遞迴查詢[^1]

`WITH`provides a way to write auxiliary statements for use in a larger query. These statements, which are often referred to as Common Table Expressions orCTEs, can be thought of as defining temporary tables that exist just for one query. Each auxiliary statement in a`WITH`clause can be a`SELECT`,`INSERT`,`UPDATE`, or`DELETE`; and the`WITH`clause itself is attached to a primary statement that can also be a`SELECT`,`INSERT`,`UPDATE`, or`DELETE`.

### 7.8.1. `SELECT`in`WITH`

The basic value of`SELECT`in`WITH`is to break down complicated queries into simpler parts. An example is:

```
WITH regional_sales AS (
        SELECT region, SUM(amount) AS total_sales
        FROM orders
        GROUP BY region
     ), top_regions AS (
        SELECT region
        FROM regional_sales
        WHERE total_sales 
>
 (SELECT SUM(total_sales)/10 FROM regional_sales)
     )
SELECT region,
       product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;

```

which displays per-product sales totals in only the top sales regions. The`WITH`clause defines two auxiliary statements named`regional_sales`and`top_regions`, where the output of`regional_sales`is used in`top_regions`and the output of`top_regions`is used in the primary`SELECT`query. This example could have been written without`WITH`, but we'd have needed two levels of nested sub-`SELECT`s. It's a bit easier to follow this way.

The optional`RECURSIVE`modifier changes`WITH`from a mere syntactic convenience into a feature that accomplishes things not otherwise possible in standard SQL. Using`RECURSIVE`, a`WITH`query can refer to its own output. A very simple example is this query to sum the integers from 1 through 100:

```
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n 
<
 100
)
SELECT sum(n) FROM t;

```

The general form of a recursive`WITH`query is always a_non-recursive term_, then`UNION`\(or`UNION ALL`\), then a_recursive term_, where only the recursive term can contain a reference to the query's own output. Such a query is executed as follows:

**Recursive Query Evaluation**

1. Evaluate the non-recursive term. For`UNION`\(but not`UNION ALL`\), discard duplicate rows. Include all remaining rows in the result of the recursive query, and also place them in a temporary_working table_.

2. So long as the working table is not empty, repeat these steps:

   1. Evaluate the recursive term, substituting the current contents of the working table for the recursive self-reference. For`UNION`\(but not`UNION ALL`\), discard duplicate rows and rows that duplicate any previous result row. Include all remaining rows in the result of the recursive query, and also place them in a temporary_intermediate table_.

   2. Replace the contents of the working table with the contents of the intermediate table, then empty the intermediate table.

### Note

Strictly speaking, this process is iteration not recursion, but`RECURSIVE`is the terminology chosen by the SQL standards committee.

In the example above, the working table has just a single row in each step, and it takes on the values from 1 through 100 in successive steps. In the 100th step, there is no output because of the`WHERE`clause, and so the query terminates.

Recursive queries are typically used to deal with hierarchical or tree-structured data. A useful example is this query to find all the direct and indirect sub-parts of a product, given only a table that shows immediate inclusions:

```
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
  )
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part

```

When working with recursive queries it is important to be sure that the recursive part of the query will eventually return no tuples, or else the query will loop indefinitely. Sometimes, using`UNION`instead of`UNION ALL`can accomplish this by discarding rows that duplicate previous output rows. However, often a cycle does not involve output rows that are completely duplicate: it may be necessary to check just one or a few fields to see if the same point has been reached before. The standard method for handling such situations is to compute an array of the already-visited values. For example, consider the following query that searches a table`graph`using a`link`field:

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
        SELECT g.id, g.link, g.data, 1
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1
        FROM graph g, search_graph sg
        WHERE g.id = sg.link
)
SELECT * FROM search_graph;

```

This query will loop if the`link`relationships contain cycles. Because we require a“depth”output, just changing`UNION ALL`to`UNION`would not eliminate the looping. Instead we need to recognize whether we have reached the same row again while following a particular path of links. We add two columns`path`and`cycle`to the loop-prone query:

```
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
        SELECT g.id, g.link, g.data, 1,
          ARRAY[g.id],
          false
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1,
          path || g.id,
          g.id = ANY(path)
        FROM graph g, search_graph sg
        WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;

```

Aside from preventing cycles, the array value is often useful in its own right as representing the“path”taken to reach any particular row.

In the general case where more than one field needs to be checked to recognize a cycle, use an array of rows. For example, if we needed to compare fields`f1`and`f2`:

```
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
        SELECT g.id, g.link, g.data, 1,
          ARRAY[ROW(g.f1, g.f2)],
          false
        FROM graph g
      UNION ALL
        SELECT g.id, g.link, g.data, sg.depth + 1,
          path || ROW(g.f1, g.f2),
          ROW(g.f1, g.f2) = ANY(path)
        FROM graph g, search_graph sg
        WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;

```

### Tip

Omit the`ROW()`syntax in the common case where only one field needs to be checked to recognize a cycle. This allows a simple array rather than a composite-type array to be used, gaining efficiency.

### Tip

The recursive query evaluation algorithm produces its output in breadth-first search order. You can display the results in depth-first search order by making the outer query`ORDER BY`a“path”column constructed in this way.

A helpful trick for testing queries when you are not certain if they might loop is to place a`LIMIT`in the parent query. For example, this query would loop forever without the`LIMIT`:

```
WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;

```

This works becausePostgreSQL's implementation evaluates only as many rows of a`WITH`query as are actually fetched by the parent query. Using this trick in production is not recommended, because other systems might work differently. Also, it usually won't work if you make the outer query sort the recursive query's results or join them to some other table, because in such cases the outer query will usually try to fetch all of the`WITH`query's output anyway.

A useful property of`WITH`queries is that they are evaluated only once per execution of the parent query, even if they are referred to more than once by the parent query or sibling`WITH`queries. Thus, expensive calculations that are needed in multiple places can be placed within a`WITH`query to avoid redundant work. Another possible application is to prevent unwanted multiple evaluations of functions with side-effects. However, the other side of this coin is that the optimizer is less able to push restrictions from the parent query down into a`WITH`query than an ordinary subquery. The`WITH`query will generally be evaluated as written, without suppression of rows that the parent query might discard afterwards. \(But, as mentioned above, evaluation might stop early if the reference\(s\) to the query demand only a limited number of rows.\)

The examples above only show`WITH`being used with`SELECT`, but it can be attached in the same way to`INSERT`,`UPDATE`, or`DELETE`. In each case it effectively provides temporary table\(s\) that can be referred to in the main command.

### 7.8.2. Data-Modifying Statements in`WITH`

You can use data-modifying statements \(`INSERT`,`UPDATE`, or`DELETE`\) in`WITH`. This allows you to perform several different operations in the same query. An example is:

```
WITH moved_rows AS (
    DELETE FROM products
    WHERE
        "date" 
>
= '2010-10-01' AND
        "date" 
<
 '2010-11-01'
    RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;

```

This query effectively moves rows from`products`to`products_log`. The`DELETE`in`WITH`deletes the specified rows from`products`, returning their contents by means of its`RETURNING`clause; and then the primary query reads that output and inserts it into`products_log`.

A fine point of the above example is that the`WITH`clause is attached to the`INSERT`, not the sub-`SELECT`within the`INSERT`. This is necessary because data-modifying statements are only allowed in`WITH`clauses that are attached to the top-level statement. However, normal`WITH`visibility rules apply, so it is possible to refer to the`WITH`statement's output from the sub-`SELECT`.

Data-modifying statements in`WITH`usually have`RETURNING`clauses \(see[Section 6.4](https://www.postgresql.org/docs/10/static/dml-returning.html)\), as shown in the example above. It is the output of the`RETURNING`clause,_not_the target table of the data-modifying statement, that forms the temporary table that can be referred to by the rest of the query. If a data-modifying statement in`WITH`lacks a`RETURNING`clause, then it forms no temporary table and cannot be referred to in the rest of the query. Such a statement will be executed nonetheless. A not-particularly-useful example is:

```
WITH t AS (
    DELETE FROM foo
)
DELETE FROM bar;

```

This example would remove all rows from tables`foo`and`bar`. The number of affected rows reported to the client would only include rows removed from`bar`.

Recursive self-references in data-modifying statements are not allowed. In some cases it is possible to work around this limitation by referring to the output of a recursive`WITH`, for example:

```
WITH RECURSIVE included_parts(sub_part, part) AS (
    SELECT sub_part, part FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
  )
DELETE FROM parts
  WHERE part IN (SELECT part FROM included_parts);

```

This query would remove all direct and indirect subparts of a product.

Data-modifying statements in`WITH`are executed exactly once, and always to completion, independently of whether the primary query reads all \(or indeed any\) of their output. Notice that this is different from the rule for`SELECT`in`WITH`: as stated in the previous section, execution of a`SELECT`is carried only as far as the primary query demands its output.

The sub-statements in`WITH`are executed concurrently with each other and with the main query. Therefore, when using data-modifying statements in`WITH`, the order in which the specified updates actually happen is unpredictable. All the statements are executed with the same_snapshot_\(see[Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html)\), so they cannot“see”one another's effects on the target tables. This alleviates the effects of the unpredictability of the actual order of row updates, and means that`RETURNING`data is the only way to communicate changes between different`WITH`sub-statements and the main query. An example of this is that in

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;

```

the outer`SELECT`would return the original prices before the action of the`UPDATE`, while in

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;

```

the outer`SELECT`would return the updated data.

Trying to update the same row twice in a single statement is not supported. Only one of the modifications takes place, but it is not easy \(and sometimes not possible\) to reliably predict which one. This also applies to deleting a row that was already updated in the same statement: only the update is performed. Therefore you should generally avoid trying to modify a single row twice in a single statement. In particular avoid writing`WITH`sub-statements that could affect the same rows changed by the main statement or a sibling sub-statement. The effects of such a statement will not be predictable.

At present, any table used as the target of a data-modifying statement in`WITH`must not have a conditional rule, nor an`ALSO`rule, nor an`INSTEAD`rule that expands to multiple statements.

---



[^1]: [PostgreSQL: Documentation: 10: 7.8. WITH Queries \(Common Table Expressions\)](https://www.postgresql.org/docs/10/static/queries-with.html)

