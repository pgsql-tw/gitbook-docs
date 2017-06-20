# 3.2. Views[^1]

Refer back to the queries in[Section 2.6](https://www.postgresql.org/docs/10/static/tutorial-join.html). Suppose the combined listing of weather records and city location is of particular interest to your application, but you do not want to type the query each time you need it. You can create a\_view\_over the query, which gives a name to the query that you can refer to like an ordinary table:

```
CREATE VIEW myview AS
    SELECT city, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;

SELECT * FROM myview;
```

Making liberal use of views is a key aspect of good SQL database design. Views allow you to encapsulate the details of the structure of your tables, which might change as your application evolves, behind consistent interfaces.

Views can be used in almost any place a real table can be used. Building views upon other views is not uncommon.

---



[^1]: [PostgreSQL: Documentation: 10: 3.2. Views](https://www.postgresql.org/docs/10/static/tutorial-views.html)

