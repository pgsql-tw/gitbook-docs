# 3.6. 繼承[^1]

Inheritance is a concept from object-oriented databases. It opens up interesting new possibilities of database design.

Let's create two tables: A table`cities`and a table`capitals`. Naturally, capitals are also cities, so you want some way to show the capitals implicitly when you list all cities. If you're really clever you might invent some scheme like this:

```
CREATE TABLE capitals (
  name       text,
  population real,
  altitude   int,    -- (in ft)
  state      char(2)
);

CREATE TABLE non_capitals (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE VIEW cities AS
  SELECT name, population, altitude FROM capitals
    UNION
  SELECT name, population, altitude FROM non_capitals;

```

This works OK as far as querying goes, but it gets ugly when you need to update several rows, for one thing.

A better solution is this:

```
CREATE TABLE cities (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE TABLE capitals (
  state      char(2)
) INHERITS (cities);

```

In this case, a row of`capitals`_inherits_all columns \(`name`,`population`, and`altitude`\) from its_parent_,`cities`. The type of the column`name`is`text`, a nativePostgreSQLtype for variable length character strings. State capitals have an extra column,`state`, that shows their state. InPostgreSQL, a table can inherit from zero or more other tables.

For example, the following query finds the names of all cities, including state capitals, that are located at an altitude over 500 feet:

```
SELECT name, altitude
  FROM cities
  WHERE altitude 
>
 500;

```

which returns:

```
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
 Madison   |      845
(3 rows)

```

On the other hand, the following query finds all the cities that are not state capitals and are situated at an altitude over 500 feet:

```
SELECT name, altitude
    FROM ONLY cities
    WHERE altitude 
>
 500;

```

```
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
(2 rows)

```

Here the`ONLY`before`cities`indicates that the query should be run over only the`cities`table, and not tables below`cities`in the inheritance hierarchy. Many of the commands that we have already discussed —`SELECT`,`UPDATE`, and`DELETE`— support this`ONLY`notation.

### Note

Although inheritance is frequently useful, it has not been integrated with unique constraints or foreign keys, which limits its usefulness. See[Section 5.9](https://www.postgresql.org/docs/10/static/ddl-inherit.html)for more detail.

---



[^1]: [PostgreSQL: Documentation: 10: 3.6. Inheritance](https://www.postgresql.org/docs/10/static/tutorial-inheritance.html)

