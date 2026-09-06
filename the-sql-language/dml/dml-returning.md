## 6.4. Returning Data from Modified Rows [#](#DML-RETURNING)

<a id="id-1.5.5.6.2"></a><a id="id-1.5.5.6.3"></a><a id="id-1.5.5.6.4"></a><a id="id-1.5.5.6.5"></a><a id="id-1.5.5.6.6"></a>

Sometimes it is useful to obtain data from modified rows while they are
being manipulated. The `INSERT`, `UPDATE`,
`DELETE`, and `MERGE` commands all have an
optional `RETURNING` clause that supports this. Use
of `RETURNING` avoids performing an extra database query to
collect the data, and is especially valuable when it would otherwise be
difficult to identify the modified rows reliably.

The allowed contents of a `RETURNING` clause are the same as
a `SELECT` command's output list
(see [Section 7.3](../queries/queries-select-lists.md)). It can contain column
names of the command's target table, or value expressions using those
columns. A common shorthand is `RETURNING *`, which selects
all columns of the target table in order.

In an `INSERT`, the default data available to
`RETURNING` is
the row as it was inserted. This is not so useful in trivial inserts,
since it would just repeat the data provided by the client. But it can
be very handy when relying on computed default values. For example,
when using a [`serial`](../datatype/datatype-numeric.md#DATATYPE-SERIAL)
column to provide unique identifiers, `RETURNING` can return
the ID assigned to a new row:

```

CREATE TABLE users (firstname text, lastname text, id serial primary key);

INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;
```

The `RETURNING` clause is also very useful
with `INSERT ... SELECT`.

In an `UPDATE`, the default data available to
`RETURNING` is
the new content of the modified row. For example:

```

UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, price AS new_price;
```

In a `DELETE`, the default data available to
`RETURNING` is
the content of the deleted row. For example:

```

DELETE FROM products
  WHERE obsoletion_date = 'today'
  RETURNING *;
```

In a `MERGE`, the default data available to
`RETURNING` is
the content of the source row plus the content of the inserted, updated, or
deleted target row. Since it is quite common for the source and target to
have many of the same columns, specifying `RETURNING *`
can lead to a lot of duplicated columns, so it is often more useful to
qualify it so as to return just the source or target row. For example:

```

MERGE INTO products p USING new_products n ON p.product_no = n.product_no
  WHEN NOT MATCHED THEN INSERT VALUES (n.product_no, n.name, n.price)
  WHEN MATCHED THEN UPDATE SET name = n.name, price = n.price
  RETURNING p.*;
```

In each of these commands, it is also possible to explicitly return the
old and new content of the modified row. For example:

```

UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, old.price AS old_price, new.price AS new_price,
            new.price - old.price AS price_change;
```

In this example, writing `new.price` is the same as
just writing `price`, but it makes the meaning clearer.

This syntax for returning old and new values is available in
`INSERT`, `UPDATE`,
`DELETE`, and `MERGE` commands, but
typically old values will be `NULL` for an
`INSERT`, and new values will be `NULL`
for a `DELETE`. However, there are situations where it
can still be useful for those commands. For example, in an
`INSERT` with an
[`ON CONFLICT DO UPDATE`](../../reference/sql-commands/sql-insert.md#SQL-ON-CONFLICT)
clause, the old values will be non-`NULL` for conflicting
rows. Similarly, if a `DELETE` is turned into an
`UPDATE` by a [rewrite rule](../../reference/sql-commands/sql-createrule.md),
the new values may be non-`NULL`.

If there are triggers ([Chapter 37](../../server-programming/triggers/README.md)) on the target table,
the data available to `RETURNING` is the row as modified by
the triggers. Thus, inspecting columns computed by triggers is another
common use-case for `RETURNING`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dml-returning.html)（英文原文，待翻譯）
