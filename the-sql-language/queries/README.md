## Chapter 7. Queries

**Table of Contents**

[7.1. Overview](queries-overview.md)

[7.2. Table Expressions](queries-table-expressions.md)
:   [7.2.1. The `FROM` Clause](queries-table-expressions.md#QUERIES-FROM)

    [7.2.2. The `WHERE` Clause](queries-table-expressions.md#QUERIES-WHERE)

    [7.2.3. The `GROUP BY` and `HAVING` Clauses](queries-table-expressions.md#QUERIES-GROUP)

    [7.2.4. `GROUPING SETS`, `CUBE`, and `ROLLUP`](queries-table-expressions.md#QUERIES-GROUPING-SETS)

    [7.2.5. Window Function Processing](queries-table-expressions.md#QUERIES-WINDOW)

[7.3. Select Lists](queries-select-lists.md)
:   [7.3.1. Select-List Items](queries-select-lists.md#QUERIES-SELECT-LIST-ITEMS)

    [7.3.2. Column Labels](queries-select-lists.md#QUERIES-COLUMN-LABELS)

    [7.3.3. `DISTINCT`](queries-select-lists.md#QUERIES-DISTINCT)

[7.4. Combining Queries (`UNION`, `INTERSECT`, `EXCEPT`)](queries-union.md)

[7.5. Sorting Rows (`ORDER BY`)](queries-order.md)

[7.6. `LIMIT` and `OFFSET`](queries-limit.md)

[7.7. `VALUES` Lists](queries-values.md)

[7.8. `WITH` Queries (Common Table Expressions)](queries-with.md)
:   [7.8.1. `SELECT` in `WITH`](queries-with.md#QUERIES-WITH-SELECT)

    [7.8.2. Recursive Queries](queries-with.md#QUERIES-WITH-RECURSIVE)

    [7.8.3. Common Table Expression Materialization](queries-with.md#QUERIES-WITH-CTE-MATERIALIZATION)

    [7.8.4. Data-Modifying Statements in `WITH`](queries-with.md#QUERIES-WITH-MODIFYING)

<a id="id-1.5.6.2"></a><a id="id-1.5.6.3"></a>

The previous chapters explained how to create tables, how to fill
them with data, and how to manipulate that data. Now we finally
discuss how to retrieve the data from the database.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries.html)（英文原文，待翻譯）
