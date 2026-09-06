## Chapter 14. Performance Tips

**Table of Contents**

[14.1. Using `EXPLAIN`](using-explain.md)
:   [14.1.1. `EXPLAIN` Basics](using-explain.md#USING-EXPLAIN-BASICS)

    [14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)

    [14.1.3. Caveats](using-explain.md#USING-EXPLAIN-CAVEATS)

[14.2. Statistics Used by the Planner](planner-stats.md)
:   [14.2.1. Single-Column Statistics](planner-stats.md#PLANNER-STATS-SINGLE-COLUMN)

    [14.2.2. Extended Statistics](planner-stats.md#PLANNER-STATS-EXTENDED)

[14.3. Controlling the Planner with Explicit `JOIN` Clauses](explicit-joins.md)

[14.4. Populating a Database](populate.md)
:   [14.4.1. Disable Autocommit](populate.md#DISABLE-AUTOCOMMIT)

    [14.4.2. Use `COPY`](populate.md#POPULATE-COPY-FROM)

    [14.4.3. Remove Indexes](populate.md#POPULATE-RM-INDEXES)

    [14.4.4. Remove Foreign Key Constraints](populate.md#POPULATE-RM-FKEYS)

    [14.4.5. Increase `maintenance_work_mem`](populate.md#POPULATE-WORK-MEM)

    [14.4.6. Increase `max_wal_size`](populate.md#POPULATE-MAX-WAL-SIZE)

    [14.4.7. Disable WAL Archival and Streaming Replication](populate.md#POPULATE-PITR)

    [14.4.8. Run `ANALYZE` Afterwards](populate.md#POPULATE-ANALYZE)

    [14.4.9. Some Notes about pg_dump](populate.md#POPULATE-PG-DUMP)

[14.5. Non-Durable Settings](non-durability.md)

<a id="id-1.5.13.2"></a>

Query performance can be affected by many things. Some of these can
be controlled by the user, while others are fundamental to the underlying
design of the system. This chapter provides some hints about understanding
and tuning PostgreSQL performance.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/performance-tips.html)（英文原文，待翻譯）
