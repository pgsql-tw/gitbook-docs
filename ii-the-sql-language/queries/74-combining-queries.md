# 7.4. 合併查詢結果[^1]

The results of two queries can be combined using the set operations union, intersection, and difference. The syntax is

```
query1
 UNION [
ALL
] 
query2
query1
 INTERSECT [
ALL
] 
query2
query1
 EXCEPT [
ALL
] 
query2
```

_`query1`_and_`query2`_are queries that can use any of the features discussed up to this point. Set operations can also be nested and chained, for example

```
query1
 UNION 
query2
 UNION 
query3
```

which is executed as:

```
(
query1
 UNION 
query2
) UNION 
query3
```

`UNION`effectively appends the result of_`query2`_to the result of_`query1`_\(although there is no guarantee that this is the order in which the rows are actually returned\). Furthermore, it eliminates duplicate rows from its result, in the same way as`DISTINCT`, unless`UNION ALL`is used.

`INTERSECT`returns all rows that are both in the result of_`query1`_and in the result of_`query2`_. Duplicate rows are eliminated unless`INTERSECT ALL`is used.

`EXCEPT`returns all rows that are in the result of_`query1`_but not in the result of_`query2`_. \(This is sometimes called the_difference_between two queries.\) Again, duplicates are eliminated unless`EXCEPT ALL`is used.

In order to calculate the union, intersection, or difference of two queries, the two queries must be“union compatible”, which means that they return the same number of columns and the corresponding columns have compatible data types, as described in[Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html).

---



[^1]: [PostgreSQL: Documentation: 10: 7.4. Combining Queries](https://www.postgresql.org/docs/10/static/queries-union.html)

