# 3.3. Foreign Keys[^1]

Recall the`weather`and`cities`tables from[Chapter 2](https://www.postgresql.org/docs/10/static/tutorial-sql.html). Consider the following problem: You want to make sure that no one can insert rows in the`weather`table that do not have a matching entry in the`cities`table. This is called maintaining the_referential integrity_of your data. In simplistic database systems this would be implemented \(if at all\) by first looking at the`cities`table to check if a matching record exists, and then inserting or rejecting the new`weather`records. This approach has a number of problems and is very inconvenient, soPostgreSQLcan do this for you.

The new declaration of the tables would look like this:

```
CREATE TABLE cities (
        city     varchar(80) primary key,
        location point
);

CREATE TABLE weather (
        city      varchar(80) references cities(city),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);

```

Now try inserting an invalid record:

```
INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');

```

```
ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".

```

The behavior of foreign keys can be finely tuned to your application. We will not go beyond this simple example in this tutorial, but just refer you to[Chapter 5](https://www.postgresql.org/docs/10/static/ddl.html)for more information. Making correct use of foreign keys will definitely improve the quality of your database applications, so you are strongly encouraged to learn about them.

---



[^1]: [PostgreSQL: Documentation: 10: 3.3. Foreign Keys](/PostgreSQL: Documentation: 10: 3.3. Foreign Keys)

