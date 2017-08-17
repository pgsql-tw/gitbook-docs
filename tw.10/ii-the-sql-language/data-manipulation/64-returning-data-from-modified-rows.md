# 6.4. 修改並回傳資料[^1]

Sometimes it is useful to obtain data from modified rows while they are being manipulated. The`INSERT`,`UPDATE`, and`DELETE`commands all have an optional`RETURNING`clause that supports this. Use of`RETURNING`avoids performing an extra database query to collect the data, and is especially valuable when it would otherwise be difficult to identify the modified rows reliably.

The allowed contents of a`RETURNING`clause are the same as a`SELECT`command's output list \(see[Section 7.3](https://www.postgresql.org/docs/10/static/queries-select-lists.html)\). It can contain column names of the command's target table, or value expressions using those columns. A common shorthand is`RETURNING *`, which selects all columns of the target table in order.

In an`INSERT`, the data available to`RETURNING`is the row as it was inserted. This is not so useful in trivial inserts, since it would just repeat the data provided by the client. But it can be very handy when relying on computed default values. For example, when using a[`serial`](https://www.postgresql.org/docs/10/static/datatype-numeric.html#datatype-serial)column to provide unique identifiers,`RETURNING`can return the ID assigned to a new row:

```
CREATE TABLE users (firstname text, lastname text, id serial primary key);

INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;

```

The`RETURNING`clause is also very useful with`INSERT ... SELECT`.

In an`UPDATE`, the data available to`RETURNING`is the new content of the modified row. For example:

```
UPDATE products SET price = price * 1.10
  WHERE price 
<
= 99.99
  RETURNING name, price AS new_price;

```

In a`DELETE`, the data available to`RETURNING`is the content of the deleted row. For example:

```
DELETE FROM products
  WHERE obsoletion_date = 'today'
  RETURNING *;

```

If there are triggers \([Chapter 38](https://www.postgresql.org/docs/10/static/triggers.html)\) on the target table, the data available to`RETURNING`is the row as modified by the triggers. Thus, inspecting columns computed by triggers is another common use-case for`RETURNING`.

---

---

[^1]: [PostgreSQL: Documentation: 10: 6.4. Returning Data From Modified Rows](https://www.postgresql.org/docs/10/static/dml-returning.html)

