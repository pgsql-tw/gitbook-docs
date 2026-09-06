## F.18. intagg — integer aggregator and enumerator [#](#INTAGG)

[F.18.1. Functions](intagg.md#INTAGG-FUNCTIONS)

[F.18.2. Sample Uses](intagg.md#INTAGG-SAMPLES)

<a id="id-1.11.7.28.2"></a>

The `intagg` module provides an integer aggregator and an
enumerator. `intagg` is now obsolete, because there
are built-in functions that provide a superset of its capabilities.
However, the module is still provided as a compatibility wrapper around
the built-in functions.

<a id="INTAGG-FUNCTIONS"></a>

### F.18.1. Functions [#](#INTAGG-FUNCTIONS)

<a id="id-1.11.7.28.4.2"></a><a id="id-1.11.7.28.4.3"></a>

The aggregator is an aggregate function
`int_array_aggregate(integer)`
that produces an integer array
containing exactly the integers it is fed.
This is a wrapper around `array_agg`,
which does the same thing for any array type.

<a id="id-1.11.7.28.4.5"></a>

The enumerator is a function
`int_array_enum(integer[])`
that returns `setof integer`. It is essentially the reverse
operation of the aggregator: given an array of integers, expand it
into a set of rows. This is a wrapper around `unnest`,
which does the same thing for any array type.

<a id="INTAGG-SAMPLES"></a>

### F.18.2. Sample Uses [#](#INTAGG-SAMPLES)

Many database systems have the notion of a many to many table. Such a table
usually sits between two indexed tables, for example:

```

CREATE TABLE left_table  (id INT PRIMARY KEY, ...);
CREATE TABLE right_table (id INT PRIMARY KEY, ...);
CREATE TABLE many_to_many(id_left  INT REFERENCES left_table,
                          id_right INT REFERENCES right_table);
```

It is typically used like this:

```

SELECT right_table.*
FROM right_table JOIN many_to_many ON (right_table.id = many_to_many.id_right)
WHERE many_to_many.id_left = item;
```

This will return all the items in the right hand table for an entry
in the left hand table. This is a very common construct in SQL.

Now, this methodology can be cumbersome with a very large number of
entries in the `many_to_many` table. Often,
a join like this would result in an index scan
and a fetch for each right hand entry in the table for a particular
left hand entry. If you have a very dynamic system, there is not much you
can do. However, if you have some data which is fairly static, you can
create a summary table with the aggregator.

```

CREATE TABLE summary AS
  SELECT id_left, int_array_aggregate(id_right) AS rights
  FROM many_to_many
  GROUP BY id_left;
```

This will create a table with one row per left item, and an array
of right items. Now this is pretty useless without some way of using
the array; that's why there is an array enumerator. You can do

```

SELECT id_left, int_array_enum(rights) FROM summary WHERE id_left = item;
```

The above query using `int_array_enum` produces the same results
as

```

SELECT id_left, id_right FROM many_to_many WHERE id_left = item;
```

The difference is that the query against the summary table has to get
only one row from the table, whereas the direct query against
`many_to_many` must index scan and fetch a row for each entry.

On one system, an `EXPLAIN` showed a query with a cost of 8488 was
reduced to a cost of 329. The original query was a join involving the
`many_to_many` table, which was replaced by:

```

SELECT id_right, count(id_right) FROM
  ( SELECT id_left, int_array_enum(rights) AS id_right
    FROM summary
    JOIN (SELECT id FROM left_table
          WHERE id = item) AS lefts
    ON (summary.id_left = lefts.id)
  ) AS list
  GROUP BY id_right
  ORDER BY count DESC;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intagg.html)（英文原文，待翻譯）
