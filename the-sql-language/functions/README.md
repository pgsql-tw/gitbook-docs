## Chapter 9. Functions and Operators

**Table of Contents**

[9.1. Logical Operators](functions-logical.md)

[9.2. Comparison Functions and Operators](functions-comparison.md)

[9.3. Mathematical Functions and Operators](functions-math.md)

[9.4. String Functions and Operators](functions-string.md)
:   [9.4.1. `format`](functions-string.md#FUNCTIONS-STRING-FORMAT)

[9.5. Binary String Functions and Operators](functions-binarystring.md)

[9.6. Bit String Functions and Operators](functions-bitstring.md)

[9.7. Pattern Matching](functions-matching.md)
:   [9.7.1. `LIKE`](functions-matching.md#FUNCTIONS-LIKE)

    [9.7.2. `SIMILAR TO` Regular Expressions](functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP)

    [9.7.3. POSIX Regular Expressions](functions-matching.md#FUNCTIONS-POSIX-REGEXP)

[9.8. Data Type Formatting Functions](functions-formatting.md)

[9.9. Date/Time Functions and Operators](functions-datetime.md)
:   [9.9.1. `EXTRACT`, `date_part`](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)

    [9.9.2. `date_trunc`](functions-datetime.md#FUNCTIONS-DATETIME-TRUNC)

    [9.9.3. `date_bin`](functions-datetime.md#FUNCTIONS-DATETIME-BIN)

    [9.9.4. `AT TIME ZONE` and `AT LOCAL`](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)

    [9.9.5. Current Date/Time](functions-datetime.md#FUNCTIONS-DATETIME-CURRENT)

    [9.9.6. Delaying Execution](functions-datetime.md#FUNCTIONS-DATETIME-DELAY)

[9.10. Enum Support Functions](functions-enum.md)

[9.11. Geometric Functions and Operators](functions-geometry.md)

[9.12. Network Address Functions and Operators](functions-net.md)

[9.13. Text Search Functions and Operators](functions-textsearch.md)

[9.14. UUID Functions](functions-uuid.md)

[9.15. XML Functions](functions-xml.md)
:   [9.15.1. Producing XML Content](functions-xml.md#FUNCTIONS-PRODUCING-XML)

    [9.15.2. XML Predicates](functions-xml.md#FUNCTIONS-XML-PREDICATES)

    [9.15.3. Processing XML](functions-xml.md#FUNCTIONS-XML-PROCESSING)

    [9.15.4. Mapping Tables to XML](functions-xml.md#FUNCTIONS-XML-MAPPING)

[9.16. JSON Functions and Operators](functions-json.md)
:   [9.16.1. Processing and Creating JSON Data](functions-json.md#FUNCTIONS-JSON-PROCESSING)

    [9.16.2. The SQL/JSON Path Language](functions-json.md#FUNCTIONS-SQLJSON-PATH)

    [9.16.3. SQL/JSON Query Functions](functions-json.md#SQLJSON-QUERY-FUNCTIONS)

    [9.16.4. JSON_TABLE](functions-json.md#FUNCTIONS-SQLJSON-TABLE)

[9.17. Sequence Manipulation Functions](functions-sequence.md)

[9.18. Conditional Expressions](functions-conditional.md)
:   [9.18.1. `CASE`](functions-conditional.md#FUNCTIONS-CASE)

    [9.18.2. `COALESCE`](functions-conditional.md#FUNCTIONS-COALESCE-NVL-IFNULL)

    [9.18.3. `NULLIF`](functions-conditional.md#FUNCTIONS-NULLIF)

    [9.18.4. `GREATEST` and `LEAST`](functions-conditional.md#FUNCTIONS-GREATEST-LEAST)

[9.19. Array Functions and Operators](functions-array.md)

[9.20. Range/Multirange Functions and Operators](functions-range.md)

[9.21. Aggregate Functions](functions-aggregate.md)

[9.22. Window Functions](functions-window.md)

[9.23. Merge Support Functions](functions-merge-support.md)

[9.24. Subquery Expressions](functions-subquery.md)
:   [9.24.1. `EXISTS`](functions-subquery.md#FUNCTIONS-SUBQUERY-EXISTS)

    [9.24.2. `IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-IN)

    [9.24.3. `NOT IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-NOTIN)

    [9.24.4. `ANY`/`SOME`](functions-subquery.md#FUNCTIONS-SUBQUERY-ANY-SOME)

    [9.24.5. `ALL`](functions-subquery.md#FUNCTIONS-SUBQUERY-ALL)

    [9.24.6. Single-Row Comparison](functions-subquery.md#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

[9.25. Row and Array Comparisons](functions-comparisons.md)
:   [9.25.1. `IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR)

    [9.25.2. `NOT IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-NOT-IN)

    [9.25.3. `ANY`/`SOME` (array)](functions-comparisons.md#FUNCTIONS-COMPARISONS-ANY-SOME)

    [9.25.4. `ALL` (array)](functions-comparisons.md#FUNCTIONS-COMPARISONS-ALL)

    [9.25.5. Row Constructor Comparison](functions-comparisons.md#ROW-WISE-COMPARISON)

    [9.25.6. Composite Type Comparison](functions-comparisons.md#COMPOSITE-TYPE-COMPARISON)

[9.26. Set Returning Functions](functions-srf.md)

[9.27. System Information Functions and Operators](functions-info.md)
:   [9.27.1. Session Information Functions](functions-info.md#FUNCTIONS-INFO-SESSION)

    [9.27.2. Access Privilege Inquiry Functions](functions-info.md#FUNCTIONS-INFO-ACCESS)

    [9.27.3. Schema Visibility Inquiry Functions](functions-info.md#FUNCTIONS-INFO-SCHEMA)

    [9.27.4. System Catalog Information Functions](functions-info.md#FUNCTIONS-INFO-CATALOG)

    [9.27.5. Object Information and Addressing Functions](functions-info.md#FUNCTIONS-INFO-OBJECT)

    [9.27.6. Comment Information Functions](functions-info.md#FUNCTIONS-INFO-COMMENT)

    [9.27.7. Data Validity Checking Functions](functions-info.md#FUNCTIONS-INFO-VALIDITY)

    [9.27.8. Transaction ID and Snapshot Information Functions](functions-info.md#FUNCTIONS-INFO-SNAPSHOT)

    [9.27.9. Committed Transaction Information Functions](functions-info.md#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

    [9.27.10. Control Data Functions](functions-info.md#FUNCTIONS-INFO-CONTROLDATA)

    [9.27.11. Version Information Functions](functions-info.md#FUNCTIONS-INFO-VERSION)

    [9.27.12. WAL Summarization Information Functions](functions-info.md#FUNCTIONS-INFO-WAL-SUMMARY)

[9.28. System Administration Functions](functions-admin.md)
:   [9.28.1. Configuration Settings Functions](functions-admin.md#FUNCTIONS-ADMIN-SET)

    [9.28.2. Server Signaling Functions](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)

    [9.28.3. Backup Control Functions](functions-admin.md#FUNCTIONS-ADMIN-BACKUP)

    [9.28.4. Recovery Control Functions](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL)

    [9.28.5. Snapshot Synchronization Functions](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)

    [9.28.6. Replication Management Functions](functions-admin.md#FUNCTIONS-REPLICATION)

    [9.28.7. Database Object Management Functions](functions-admin.md#FUNCTIONS-ADMIN-DBOBJECT)

    [9.28.8. Index Maintenance Functions](functions-admin.md#FUNCTIONS-ADMIN-INDEX)

    [9.28.9. Generic File Access Functions](functions-admin.md#FUNCTIONS-ADMIN-GENFILE)

    [9.28.10. Advisory Lock Functions](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS)

[9.29. Trigger Functions](functions-trigger.md)

[9.30. Event Trigger Functions](functions-event-triggers.md)
:   [9.30.1. Capturing Changes at Command End](functions-event-triggers.md#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

    [9.30.2. Processing Objects Dropped by a DDL Command](functions-event-triggers.md#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

    [9.30.3. Handling a Table Rewrite Event](functions-event-triggers.md#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

[9.31. Statistics Information Functions](functions-statistics.md)
:   [9.31.1. Inspecting MCV Lists](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

<a id="id-1.5.8.2"></a><a id="id-1.5.8.3"></a>

PostgreSQL provides a large number of
functions and operators for the built-in data types. This chapter
describes most of them, although additional special-purpose functions
appear in relevant sections of the manual. Users can also
define their own functions and operators, as described in
[Part V](../../server-programming/README.md). The
psql commands `\df` and
`\do` can be used to list all
available functions and operators, respectively.

The notation used throughout this chapter to describe the argument and
result data types of a function or operator is like this:

```

repeat ( text, integer ) → text
```

which says that the function `repeat` takes one text and
one integer argument and returns a result of type text. The right arrow
is also used to indicate the result of an example, thus:

```

repeat('Pg', 4) → PgPgPgPg
```

If you are concerned about portability then note that most of
the functions and operators described in this chapter, with the
exception of the most trivial arithmetic and comparison operators
and some explicitly marked functions, are not specified by the
SQL standard. Some of this extended functionality
is present in other SQL database management
systems, and in many cases this functionality is compatible and
consistent between the various implementations.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions.html)（英文原文，待翻譯）
