# 6.1. 新增資料[^1]

When a table is created, it contains no data. The first thing to do before a database can be of much use is to insert data. Data is conceptually inserted one row at a time. Of course you can also insert more than one row, but there is no way to insert less than one row. Even if you know only some column values, a complete row must be created.

To create a new row, use the[INSERT](https://www.postgresql.org/docs/10/static/sql-insert.html)command. The command requires the table name and column values. For example, consider the products table from[Chapter 5](https://www.postgresql.org/docs/10/static/ddl.html):

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);

```

An example command to insert a row would be:

```
INSERT INTO products VALUES (1, 'Cheese', 9.99);

```

The data values are listed in the order in which the columns appear in the table, separated by commas. Usually, the data values will be literals \(constants\), but scalar expressions are also allowed.

The above syntax has the drawback that you need to know the order of the columns in the table. To avoid this you can also list the columns explicitly. For example, both of the following commands have the same effect as the one above:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
INSERT INTO products (name, price, product_no) VALUES ('Cheese', 9.99, 1);

```

Many users consider it good practice to always list the column names.

If you don't have values for all the columns, you can omit some of them. In that case, the columns will be filled with their default values. For example:

```
INSERT INTO products (product_no, name) VALUES (1, 'Cheese');
INSERT INTO products VALUES (1, 'Cheese');

```

The second form is aPostgreSQLextension. It fills the columns from the left with as many values as are given, and the rest will be defaulted.

For clarity, you can also request default values explicitly, for individual columns or for the entire row:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
INSERT INTO products DEFAULT VALUES;

```

You can insert multiple rows in a single command:

```
INSERT INTO products (product_no, name, price) VALUES
    (1, 'Cheese', 9.99),
    (2, 'Bread', 1.99),
    (3, 'Milk', 2.99);

```

It is also possible to insert the result of a query \(which might be no rows, one row, or many rows\):

```
INSERT INTO products (product_no, name, price)
  SELECT product_no, name, price FROM new_products
    WHERE release_date = 'today';

```

This provides the full power of the SQL query mechanism \([Chapter 7](https://www.postgresql.org/docs/10/static/queries.html)\) for computing the rows to be inserted.

### Tip

When inserting a lot of data at the same time, considering using the[COPY](https://www.postgresql.org/docs/10/static/sql-copy.html)command. It is not as flexible as the[INSERT](https://www.postgresql.org/docs/10/static/sql-insert.html)command, but is more efficient. Refer to[Section 14.4](https://www.postgresql.org/docs/10/static/populate.html)for more information on improving bulk loading performance.

---



[^1]: [PostgreSQL: Documentation: 10: 6.1. Inserting Data](https://www.postgresql.org/docs/10/static/dml-insert.html)

