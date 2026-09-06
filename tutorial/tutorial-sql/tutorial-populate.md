## 2.4. Populating a Table With Rows [#](#TUTORIAL-POPULATE)

<a id="id-1.4.4.5.2"></a>

The `INSERT` statement is used to populate a table with
rows:

```

INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```

Note that all data types use rather obvious input formats.
Constants that are not simple numeric values usually must be
surrounded by single quotes (`'`), as in the example.
The
`date` type is actually quite flexible in what it
accepts, but for this tutorial we will stick to the unambiguous
format shown here.

The `point` type requires a coordinate pair as input,
as shown here:

```

INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
```

The syntax used so far requires you to remember the order of the
columns. An alternative syntax allows you to list the columns
explicitly:

```

INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

You can list the columns in a different order if you wish or
even omit some columns, e.g., if the precipitation is unknown:

```

INSERT INTO weather (date, city, temp_hi, temp_lo)
    VALUES ('1994-11-29', 'Hayward', 54, 37);
```

Many developers consider explicitly listing the columns better
style than relying on the order implicitly.

Please enter all the commands shown above so you have some data to
work with in the following sections.

<a id="id-1.4.4.5.7.1"></a>
You could also have used `COPY` to load large
amounts of data from flat-text files. This is usually faster
because the `COPY` command is optimized for this
application while allowing less flexibility than
`INSERT`. An example would be:

```

COPY weather FROM '/home/user/weather.txt';
```

where the file name for the source file must be available on the
machine running the backend process, not the client, since the backend process
reads the file directly. The data inserted above into the weather table
could also be inserted from a file containing (values are separated by a
tab character):

```

San Francisco    46    50    0.25    1994-11-27
San Francisco    43    57    0.0    1994-11-29
Hayward    37    54    \N    1994-11-29
```

You can read more about the `COPY` command in
[COPY](../../reference/sql-commands/sql-copy.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-populate.html)（英文原文，待翻譯）
