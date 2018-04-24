# 11.8. 部份索引

A\_partial index\_is an index built over a subset of a table; the subset is defined by a conditional expression \(called the\_predicate\_of the partial index\). The index contains entries only for those table rows that satisfy the predicate. Partial indexes are a specialized feature, but there are several situations in which they are useful.

One major reason for using a partial index is to avoid indexing common values. Since a query searching for a common value \(one that accounts for more than a few percent of all the table rows\) will not use the index anyway, there is no point in keeping those rows in the index at all. This reduces the size of the index, which will speed up those queries that do use the index. It will also speed up many table update operations because the index does not need to be updated in all cases.[Example 11.1](https://www.postgresql.org/docs/10/static/indexes-partial.html#indexes-partial-ex1)shows a possible application of this idea.

**Example 11.1. Setting up a Partial Index to Exclude Common Values**

Suppose you are storing web server access logs in a database. Most accesses originate from the IP address range of your organization but some are from elsewhere \(say, employees on dial-up connections\). If your searches by IP are primarily for outside accesses, you probably do not need to index the IP range that corresponds to your organization's subnet.

Assume a table like this:

```text
CREATE TABLE access_log (
    url varchar,
    client_ip inet,
    ...
);
```

To create a partial index that suits our example, use a command such as this:

```text
CREATE INDEX access_log_client_ip_ix ON access_log (client_ip)
WHERE NOT (client_ip 
>
 inet '192.168.100.0' AND
           client_ip 
<
 inet '192.168.100.255');
```

A typical query that can use this index would be:

```text
SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '212.78.10.32';
```

A query that cannot use this index is:

```text
SELECT *
FROM access_log
WHERE client_ip = inet '192.168.100.23';
```

Observe that this kind of partial index requires that the common values be predetermined, so such partial indexes are best used for data distributions that do not change. The indexes can be recreated occasionally to adjust for new data distributions, but this adds maintenance effort.

Another possible use for a partial index is to exclude values from the index that the typical query workload is not interested in; this is shown in[Example 11.2](https://www.postgresql.org/docs/10/static/indexes-partial.html#indexes-partial-ex2). This results in the same advantages as listed above, but it prevents the“uninteresting”values from being accessed via that index, even if an index scan might be profitable in that case. Obviously, setting up partial indexes for this kind of scenario will require a lot of care and experimentation.

**Example 11.2. Setting up a Partial Index to Exclude Uninteresting Values**

If you have a table that contains both billed and unbilled orders, where the unbilled orders take up a small fraction of the total table and yet those are the most-accessed rows, you can improve performance by creating an index on just the unbilled rows. The command to create the index would look like this:

```text
CREATE INDEX orders_unbilled_index ON orders (order_nr)
    WHERE billed is not true;
```

A possible query to use this index would be:

```text
SELECT * FROM orders WHERE billed is not true AND order_nr 
<
 10000;
```

However, the index can also be used in queries that do not involve`order_nr`at all, e.g.:

```text
SELECT * FROM orders WHERE billed is not true AND amount 
>
 5000.00;
```

This is not as efficient as a partial index on the`amount`column would be, since the system has to scan the entire index. Yet, if there are relatively few unbilled orders, using this partial index just to find the unbilled orders could be a win.

Note that this query cannot use this index:

```text
SELECT * FROM orders WHERE order_nr = 3501;
```

The order 3501 might be among the billed or unbilled orders.

[Example 11.2](https://www.postgresql.org/docs/10/static/indexes-partial.html#indexes-partial-ex2)also illustrates that the indexed column and the column used in the predicate do not need to match.PostgreSQLsupports partial indexes with arbitrary predicates, so long as only columns of the table being indexed are involved. However, keep in mind that the predicate must match the conditions used in the queries that are supposed to benefit from the index. To be precise, a partial index can be used in a query only if the system can recognize that the`WHERE`condition of the query mathematically implies the predicate of the index.PostgreSQLdoes not have a sophisticated theorem prover that can recognize mathematically equivalent expressions that are written in different forms. \(Not only is such a general theorem prover extremely difficult to create, it would probably be too slow to be of any real use.\) The system can recognize simple inequality implications, for example“x &lt; 1”implies“x &lt; 2”; otherwise the predicate condition must exactly match part of the query's`WHERE`condition or the index will not be recognized as usable. Matching takes place at query planning time, not at run time. As a result, parameterized query clauses do not work with a partial index. For example a prepared query with a parameter might specify“x &lt; ?”which will never imply“x &lt; 2”for all possible values of the parameter.

A third possible use for partial indexes does not require the index to be used in queries at all. The idea here is to create a unique index over a subset of a table, as in[Example 11.3](https://www.postgresql.org/docs/10/static/indexes-partial.html#indexes-partial-ex3). This enforces uniqueness among the rows that satisfy the index predicate, without constraining those that do not.

**Example 11.3. Setting up a Partial Unique Index**

Suppose that we have a table describing test outcomes. We wish to ensure that there is only one“successful”entry for a given subject and target combination, but there might be any number of“unsuccessful”entries. Here is one way to do it:

```text
CREATE TABLE tests (
    subject text,
    target text,
    success boolean,
    ...
);

CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

This is a particularly efficient approach when there are few successful tests and many unsuccessful ones.

Finally, a partial index can also be used to override the system's query plan choices. Also, data sets with peculiar distributions might cause the system to use an index when it really should not. In that case the index can be set up so that it is not available for the offending query. Normally,PostgreSQLmakes reasonable choices about index usage \(e.g., it avoids them when retrieving common values, so the earlier example really only saves index size, it is not required to avoid index usage\), and grossly incorrect plan choices are cause for a bug report.

Keep in mind that setting up a partial index indicates that you know at least as much as the query planner knows, in particular you know when an index might be profitable. Forming this knowledge requires experience and understanding of how indexes inPostgreSQLwork. In most cases, the advantage of a partial index over a regular index will be minimal.

More information about partial indexes can be found in[\[ston89b\]](https://www.postgresql.org/docs/10/static/biblio.html#ston89b),[\[olson93\]](https://www.postgresql.org/docs/10/static/biblio.html#olson93), and[\[seshadri95\]](https://www.postgresql.org/docs/10/static/biblio.html#seshadri95).

