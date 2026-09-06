# Part II. The SQL Language

<a id="id-1.5.2"></a>

This part describes the use of the SQL language
in PostgreSQL. We start with
describing the general syntax of SQL, then
how to create tables, how to populate the database, and how to
query it. The middle part lists the available data types and
functions for use in SQL commands. Lastly,
we address several aspects of importance for tuning a database.

The information is arranged so that a novice user can
follow it from start to end and gain a full understanding of the topics
without having to refer forward too many times. The chapters are
intended to be self-contained, so that advanced users can read the
chapters individually as they choose. The information is presented
in narrative form with topical units. Readers looking for a complete
description of a particular command are encouraged to review
the [Part VI](../reference/README.md).

Readers should know how to connect to a
PostgreSQL database and issue
SQL commands. Readers that are unfamiliar with
these issues are encouraged to read [Part I](../tutorial/README.md)
first. SQL commands are typically entered
using the PostgreSQL interactive terminal
psql, but other programs that have
similar functionality can be used as well.

**Table of Contents**

[4. SQL Syntax](sql-syntax/README.md)
:   [4.1. Lexical Structure](sql-syntax/sql-syntax-lexical.md)

    [4.2. Value Expressions](sql-syntax/sql-expressions.md)

    [4.3. Calling Functions](sql-syntax/sql-syntax-calling-funcs.md)

[5. Data Definition](ddl/README.md)
:   [5.1. Table Basics](ddl/ddl-basics.md)

    [5.2. Default Values](ddl/ddl-default.md)

    [5.3. Identity Columns](ddl/ddl-identity-columns.md)

    [5.4. Generated Columns](ddl/ddl-generated-columns.md)

    [5.5. Constraints](ddl/ddl-constraints.md)

    [5.6. System Columns](ddl/ddl-system-columns.md)

    [5.7. Modifying Tables](ddl/ddl-alter.md)

    [5.8. Privileges](ddl/ddl-priv.md)

    [5.9. Row Security Policies](ddl/ddl-rowsecurity.md)

    [5.10. Schemas](ddl/ddl-schemas.md)

    [5.11. Inheritance](ddl/ddl-inherit.md)

    [5.12. Table Partitioning](ddl/ddl-partitioning.md)

    [5.13. Foreign Data](ddl/ddl-foreign-data.md)

    [5.14. Other Database Objects](ddl/ddl-others.md)

    [5.15. Dependency Tracking](ddl/ddl-depend.md)

[6. Data Manipulation](dml/README.md)
:   [6.1. Inserting Data](dml/dml-insert.md)

    [6.2. Updating Data](dml/dml-update.md)

    [6.3. Deleting Data](dml/dml-delete.md)

    [6.4. Returning Data from Modified Rows](dml/dml-returning.md)

[7. Queries](queries/README.md)
:   [7.1. Overview](queries/queries-overview.md)

    [7.2. Table Expressions](queries/queries-table-expressions.md)

    [7.3. Select Lists](queries/queries-select-lists.md)

    [7.4. Combining Queries (`UNION`, `INTERSECT`, `EXCEPT`)](queries/queries-union.md)

    [7.5. Sorting Rows (`ORDER BY`)](queries/queries-order.md)

    [7.6. `LIMIT` and `OFFSET`](queries/queries-limit.md)

    [7.7. `VALUES` Lists](queries/queries-values.md)

    [7.8. `WITH` Queries (Common Table Expressions)](queries/queries-with.md)

[8. Data Types](datatype/README.md)
:   [8.1. Numeric Types](datatype/datatype-numeric.md)

    [8.2. Monetary Types](datatype/datatype-money.md)

    [8.3. Character Types](datatype/datatype-character.md)

    [8.4. Binary Data Types](datatype/datatype-binary.md)

    [8.5. Date/Time Types](datatype/datatype-datetime.md)

    [8.6. Boolean Type](datatype/datatype-boolean.md)

    [8.7. Enumerated Types](datatype/datatype-enum.md)

    [8.8. Geometric Types](datatype/datatype-geometric.md)

    [8.9. Network Address Types](datatype/datatype-net-types.md)

    [8.10. Bit String Types](datatype/datatype-bit.md)

    [8.11. Text Search Types](datatype/datatype-textsearch.md)

    [8.12. UUID Type](datatype/datatype-uuid.md)

    [8.13. XML Type](datatype/datatype-xml.md)

    [8.14. JSON Types](datatype/datatype-json.md)

    [8.15. Arrays](datatype/arrays.md)

    [8.16. Composite Types](datatype/rowtypes.md)

    [8.17. Range Types](datatype/rangetypes.md)

    [8.18. Domain Types](datatype/domains.md)

    [8.19. Object Identifier Types](datatype/datatype-oid.md)

    [8.20. `pg_lsn` Type](datatype/datatype-pg-lsn.md)

    [8.21. Pseudo-Types](datatype/datatype-pseudo.md)

[9. Functions and Operators](functions/README.md)
:   [9.1. Logical Operators](functions/functions-logical.md)

    [9.2. Comparison Functions and Operators](functions/functions-comparison.md)

    [9.3. Mathematical Functions and Operators](functions/functions-math.md)

    [9.4. String Functions and Operators](functions/functions-string.md)

    [9.5. Binary String Functions and Operators](functions/functions-binarystring.md)

    [9.6. Bit String Functions and Operators](functions/functions-bitstring.md)

    [9.7. Pattern Matching](functions/functions-matching.md)

    [9.8. Data Type Formatting Functions](functions/functions-formatting.md)

    [9.9. Date/Time Functions and Operators](functions/functions-datetime.md)

    [9.10. Enum Support Functions](functions/functions-enum.md)

    [9.11. Geometric Functions and Operators](functions/functions-geometry.md)

    [9.12. Network Address Functions and Operators](functions/functions-net.md)

    [9.13. Text Search Functions and Operators](functions/functions-textsearch.md)

    [9.14. UUID Functions](functions/functions-uuid.md)

    [9.15. XML Functions](functions/functions-xml.md)

    [9.16. JSON Functions and Operators](functions/functions-json.md)

    [9.17. Sequence Manipulation Functions](functions/functions-sequence.md)

    [9.18. Conditional Expressions](functions/functions-conditional.md)

    [9.19. Array Functions and Operators](functions/functions-array.md)

    [9.20. Range/Multirange Functions and Operators](functions/functions-range.md)

    [9.21. Aggregate Functions](functions/functions-aggregate.md)

    [9.22. Window Functions](functions/functions-window.md)

    [9.23. Merge Support Functions](functions/functions-merge-support.md)

    [9.24. Subquery Expressions](functions/functions-subquery.md)

    [9.25. Row and Array Comparisons](functions/functions-comparisons.md)

    [9.26. Set Returning Functions](functions/functions-srf.md)

    [9.27. System Information Functions and Operators](functions/functions-info.md)

    [9.28. System Administration Functions](functions/functions-admin.md)

    [9.29. Trigger Functions](functions/functions-trigger.md)

    [9.30. Event Trigger Functions](functions/functions-event-triggers.md)

    [9.31. Statistics Information Functions](functions/functions-statistics.md)

[10. Type Conversion](typeconv/README.md)
:   [10.1. Overview](typeconv/typeconv-overview.md)

    [10.2. Operators](typeconv/typeconv-oper.md)

    [10.3. Functions](typeconv/typeconv-func.md)

    [10.4. Value Storage](typeconv/typeconv-query.md)

    [10.5. `UNION`, `CASE`, and Related Constructs](typeconv/typeconv-union-case.md)

    [10.6. `SELECT` Output Columns](typeconv/typeconv-select.md)

[11. Indexes](indexes/README.md)
:   [11.1. Introduction](indexes/indexes-intro.md)

    [11.2. Index Types](indexes/indexes-types.md)

    [11.3. Multicolumn Indexes](indexes/indexes-multicolumn.md)

    [11.4. Indexes and `ORDER BY`](indexes/indexes-ordering.md)

    [11.5. Combining Multiple Indexes](indexes/indexes-bitmap-scans.md)

    [11.6. Unique Indexes](indexes/indexes-unique.md)

    [11.7. Indexes on Expressions](indexes/indexes-expressional.md)

    [11.8. Partial Indexes](indexes/indexes-partial.md)

    [11.9. Index-Only Scans and Covering Indexes](indexes/indexes-index-only-scans.md)

    [11.10. Operator Classes and Operator Families](indexes/indexes-opclass.md)

    [11.11. Indexes and Collations](indexes/indexes-collations.md)

    [11.12. Examining Index Usage](indexes/indexes-examine.md)

[12. Full Text Search](textsearch/README.md)
:   [12.1. Introduction](textsearch/textsearch-intro.md)

    [12.2. Tables and Indexes](textsearch/textsearch-tables.md)

    [12.3. Controlling Text Search](textsearch/textsearch-controls.md)

    [12.4. Additional Features](textsearch/textsearch-features.md)

    [12.5. Parsers](textsearch/textsearch-parsers.md)

    [12.6. Dictionaries](textsearch/textsearch-dictionaries.md)

    [12.7. Configuration Example](textsearch/textsearch-configuration.md)

    [12.8. Testing and Debugging Text Search](textsearch/textsearch-debugging.md)

    [12.9. Preferred Index Types for Text Search](textsearch/textsearch-indexes.md)

    [12.10. psql Support](textsearch/textsearch-psql.md)

    [12.11. Limitations](textsearch/textsearch-limitations.md)

[13. Concurrency Control](mvcc/README.md)
:   [13.1. Introduction](mvcc/mvcc-intro.md)

    [13.2. Transaction Isolation](mvcc/transaction-iso.md)

    [13.3. Explicit Locking](mvcc/explicit-locking.md)

    [13.4. Data Consistency Checks at the Application Level](mvcc/applevel-consistency.md)

    [13.5. Serialization Failure Handling](mvcc/mvcc-serialization-failure-handling.md)

    [13.6. Caveats](mvcc/mvcc-caveats.md)

    [13.7. Locking and Indexes](mvcc/locking-indexes.md)

[14. Performance Tips](performance-tips/README.md)
:   [14.1. Using `EXPLAIN`](performance-tips/using-explain.md)

    [14.2. Statistics Used by the Planner](performance-tips/planner-stats.md)

    [14.3. Controlling the Planner with Explicit `JOIN` Clauses](performance-tips/explicit-joins.md)

    [14.4. Populating a Database](performance-tips/populate.md)

    [14.5. Non-Durable Settings](performance-tips/non-durability.md)

[15. Parallel Query](parallel-query/README.md)
:   [15.1. How Parallel Query Works](parallel-query/how-parallel-query-works.md)

    [15.2. When Can Parallel Query Be Used?](parallel-query/when-can-parallel-query-be-used.md)

    [15.3. Parallel Plans](parallel-query/parallel-plans.md)

    [15.4. Parallel Safety](parallel-query/parallel-safety.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql.html)（英文原文，待翻譯）
