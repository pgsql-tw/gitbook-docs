# 15. 平行查詢[^1]

[15.1. How Parallel Query Works](https://www.postgresql.org/docs/10/static/how-parallel-query-works.html)

[15.2. When Can Parallel Query Be Used?](https://www.postgresql.org/docs/10/static/when-can-parallel-query-be-used.html)

[15.3. Parallel Plans](https://www.postgresql.org/docs/10/static/parallel-plans.html)

[15.3.1. Parallel Scans](https://www.postgresql.org/docs/10/static/parallel-plans.html#parallel-scans)

[15.3.2. Parallel Joins](https://www.postgresql.org/docs/10/static/parallel-plans.html#parallel-joins)

[15.3.3. Parallel Aggregation](https://www.postgresql.org/docs/10/static/parallel-plans.html#parallel-aggregation)

[15.3.4. Parallel Plan Tips](https://www.postgresql.org/docs/10/static/parallel-plans.html#parallel-plan-tips)

[15.4. Parallel Safety](https://www.postgresql.org/docs/10/static/parallel-safety.html)

[15.4.1. Parallel Labeling for Functions and Aggregates](https://www.postgresql.org/docs/10/static/parallel-safety.html#parallel-labeling)



PostgreSQLcan devise query plans which can leverage multiple CPUs in order to answer queries faster. This feature is known as parallel query. Many queries cannot benefit from parallel query, either due to limitations of the current implementation or because there is no imaginable query plan which is any faster than the serial query plan. However, for queries that can benefit, the speedup from parallel query is often very significant. Many queries can run more than twice as fast when using parallel query, and some queries can run four times faster or even more. Queries that touch a large amount of data but return only a few rows to the user will typically benefit most. This chapter explains some details of how parallel query works and in which situations it can be used so that users who wish to make use of it can understand what to expect.

---



[^1]:  [PostgreSQL: Documentation: 10: Chapter 15. Parallel Query](https://www.postgresql.org/docs/10/static/parallel-query.html)

