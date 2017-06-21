# 5.13. 相依性追蹤[^1]

When you create complex database structures involving many tables with foreign key constraints, views, triggers, functions, etc. you implicitly create a net of dependencies between the objects. For instance, a table with a foreign key constraint depends on the table it references.

To ensure the integrity of the entire database structure,PostgreSQLmakes sure that you cannot drop objects that other objects still depend on. For example, attempting to drop the products table we considered in[Section 5.3.5](https://www.postgresql.org/docs/10/static/ddl-constraints.html#ddl-constraints-fk), with the orders table depending on it, would result in an error message like this:

```
DROP TABLE products;

ERROR:  cannot drop table products because other objects depend on it
DETAIL:  constraint orders_product_no_fkey on table orders depends on table products
HINT:  Use DROP ... CASCADE to drop the dependent objects too.

```

The error message contains a useful hint: if you do not want to bother deleting all the dependent objects individually, you can run:

```
DROP TABLE products CASCADE;

```

and all the dependent objects will be removed, as will any objects that depend on them, recursively. In this case, it doesn't remove the orders table, it only removes the foreign key constraint. It stops there because nothing depends on the foreign key constraint. \(If you want to check what`DROP ... CASCADE`will do, run`DROP`without`CASCADE`and read the`DETAIL`output.\)

Almost all`DROP`commands inPostgreSQLsupport specifying`CASCADE`. Of course, the nature of the possible dependencies varies with the type of the object. You can also write`RESTRICT`instead of`CASCADE`to get the default behavior, which is to prevent dropping objects that any other objects depend on.

### Note

According to the SQL standard, specifying either`RESTRICT`or`CASCADE`is required in a`DROP`command. No database system actually enforces that rule, but whether the default behavior is`RESTRICT`or`CASCADE`varies across systems.

If a`DROP`command lists multiple objects,`CASCADE`is only required when there are dependencies outside the specified group. For example, when saying`DROP TABLE tab1, tab2`the existence of a foreign key referencing`tab1`from`tab2`would not mean that`CASCADE`is needed to succeed.

For user-defined functions,PostgreSQLtracks dependencies associated with a function's externally-visible properties, such as its argument and result types, but_not_dependencies that could only be known by examining the function body. As an example, consider this situation:

```
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow',
                             'green', 'blue', 'purple');

CREATE TABLE my_colors (color rainbow, note text);

CREATE FUNCTION get_color_note (rainbow) RETURNS text AS
  'SELECT note FROM my_colors WHERE color = $1'
  LANGUAGE SQL;

```

\(See[Section 37.4](https://www.postgresql.org/docs/10/static/xfunc-sql.html)for an explanation of SQL-language functions.\)PostgreSQLwill be aware that the`get_color_note`function depends on the`rainbow`type: dropping the type would force dropping the function, because its argument type would no longer be defined. ButPostgreSQLwill not consider`get_color_note`to depend on the`my_colors`table, and so will not drop the function if the table is dropped. While there are disadvantages to this approach, there are also benefits. The function is still valid in some sense if the table is missing, though executing it would cause an error; creating a new table of the same name would allow the function to work again.

  


---



[^1]: [PostgreSQL: Documentation: 10: 5.13. Dependency Tracking](https://www.postgresql.org/docs/10/static/ddl-depend.html)

