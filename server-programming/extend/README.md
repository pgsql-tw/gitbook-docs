## Chapter 36. Extending SQL

**Table of Contents**

[36.1. How Extensibility Works](extend-how.md)

[36.2. The PostgreSQL Type System](extend-type-system.md)
:   [36.2.1. Base Types](extend-type-system.md#EXTEND-TYPE-SYSTEM-BASE)

    [36.2.2. Container Types](extend-type-system.md#EXTEND-TYPE-SYSTEM-CONTAINER)

    [36.2.3. Domains](extend-type-system.md#EXTEND-TYPE-SYSTEM-DOMAINS)

    [36.2.4. Pseudo-Types](extend-type-system.md#EXTEND-TYPE-SYSTEM-PSEUDO)

    [36.2.5. Polymorphic Types](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)

[36.3. User-Defined Functions](xfunc.md)

[36.4. User-Defined Procedures](xproc.md)

[36.5. Query Language (SQL) Functions](xfunc-sql.md)
:   [36.5.1. Arguments for SQL Functions](xfunc-sql.md#XFUNC-SQL-FUNCTION-ARGUMENTS)

    [36.5.2. SQL Functions on Base Types](xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS)

    [36.5.3. SQL Functions on Composite Types](xfunc-sql.md#XFUNC-SQL-COMPOSITE-FUNCTIONS)

    [36.5.4. SQL Functions with Output Parameters](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS)

    [36.5.5. SQL Procedures with Output Parameters](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS-PROC)

    [36.5.6. SQL Functions with Variable Numbers of Arguments](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)

    [36.5.7. SQL Functions with Default Values for Arguments](xfunc-sql.md#XFUNC-SQL-PARAMETER-DEFAULTS)

    [36.5.8. SQL Functions as Table Sources](xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS)

    [36.5.9. SQL Functions Returning Sets](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-SET)

    [36.5.10. SQL Functions Returning `TABLE`](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)

    [36.5.11. Polymorphic SQL Functions](xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)

    [36.5.12. SQL Functions with Collations](xfunc-sql.md#XFUNC-SQL-COLLATIONS)

[36.6. Function Overloading](xfunc-overload.md)

[36.7. Function Volatility Categories](xfunc-volatility.md)

[36.8. Procedural Language Functions](xfunc-pl.md)

[36.9. Internal Functions](xfunc-internal.md)

[36.10. C-Language Functions](xfunc-c.md)
:   [36.10.1. Dynamic Loading](xfunc-c.md#XFUNC-C-DYNLOAD)

    [36.10.2. Base Types in C-Language Functions](xfunc-c.md#XFUNC-C-BASETYPE)

    [36.10.3. Version 1 Calling Conventions](xfunc-c.md#XFUNC-C-V1-CALL-CONV)

    [36.10.4. Writing Code](xfunc-c.md#XFUNC-C-CODE)

    [36.10.5. Compiling and Linking Dynamically-Loaded Functions](xfunc-c.md#DFUNC)

    [36.10.6. Server API and ABI Stability Guidance](xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE)

    [36.10.7. Composite-Type Arguments](xfunc-c.md#XFUNC-C-COMPOSITE-TYPE-ARGS)

    [36.10.8. Returning Rows (Composite Types)](xfunc-c.md#XFUNC-C-RETURNING-ROWS)

    [36.10.9. Returning Sets](xfunc-c.md#XFUNC-C-RETURN-SET)

    [36.10.10. Polymorphic Arguments and Return Types](xfunc-c.md#XFUNC-C-POLYMORPHIC)

    [36.10.11. Shared Memory](xfunc-c.md#XFUNC-SHARED-ADDIN)

    [36.10.12. LWLocks](xfunc-c.md#XFUNC-ADDIN-LWLOCKS)

    [36.10.13. Custom Wait Events](xfunc-c.md#XFUNC-ADDIN-WAIT-EVENTS)

    [36.10.14. Injection Points](xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)

    [36.10.15. Custom Cumulative Statistics](xfunc-c.md#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)

    [36.10.16. Using C++ for Extensibility](xfunc-c.md#EXTEND-CPP)

[36.11. Function Optimization Information](xfunc-optimization.md)

[36.12. User-Defined Aggregates](xaggr.md)
:   [36.12.1. Moving-Aggregate Mode](xaggr.md#XAGGR-MOVING-AGGREGATES)

    [36.12.2. Polymorphic and Variadic Aggregates](xaggr.md#XAGGR-POLYMORPHIC-AGGREGATES)

    [36.12.3. Ordered-Set Aggregates](xaggr.md#XAGGR-ORDERED-SET-AGGREGATES)

    [36.12.4. Partial Aggregation](xaggr.md#XAGGR-PARTIAL-AGGREGATES)

    [36.12.5. Support Functions for Aggregates](xaggr.md#XAGGR-SUPPORT-FUNCTIONS)

[36.13. User-Defined Types](xtypes.md)
:   [36.13.1. TOAST Considerations](xtypes.md#XTYPES-TOAST)

[36.14. User-Defined Operators](xoper.md)

[36.15. Operator Optimization Information](xoper-optimization.md)
:   [36.15.1. `COMMUTATOR`](xoper-optimization.md#XOPER-COMMUTATOR)

    [36.15.2. `NEGATOR`](xoper-optimization.md#XOPER-NEGATOR)

    [36.15.3. `RESTRICT`](xoper-optimization.md#XOPER-RESTRICT)

    [36.15.4. `JOIN`](xoper-optimization.md#XOPER-JOIN)

    [36.15.5. `HASHES`](xoper-optimization.md#XOPER-HASHES)

    [36.15.6. `MERGES`](xoper-optimization.md#XOPER-MERGES)

[36.16. Interfacing Extensions to Indexes](xindex.md)
:   [36.16.1. Index Methods and Operator Classes](xindex.md#XINDEX-OPCLASS)

    [36.16.2. Index Method Strategies](xindex.md#XINDEX-STRATEGIES)

    [36.16.3. Index Method Support Routines](xindex.md#XINDEX-SUPPORT)

    [36.16.4. An Example](xindex.md#XINDEX-EXAMPLE)

    [36.16.5. Operator Classes and Operator Families](xindex.md#XINDEX-OPFAMILY)

    [36.16.6. System Dependencies on Operator Classes](xindex.md#XINDEX-OPCLASS-DEPENDENCIES)

    [36.16.7. Ordering Operators](xindex.md#XINDEX-ORDERING-OPS)

    [36.16.8. Special Features of Operator Classes](xindex.md#XINDEX-OPCLASS-FEATURES)

[36.17. Packaging Related Objects into an Extension](extend-extensions.md)
:   [36.17.1. Extension Files](extend-extensions.md#EXTEND-EXTENSIONS-FILES)

    [36.17.2. Extension Relocatability](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)

    [36.17.3. Extension Configuration Tables](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES)

    [36.17.4. Extension Updates](extend-extensions.md#EXTEND-EXTENSIONS-UPDATES)

    [36.17.5. Installing Extensions Using Update Scripts](extend-extensions.md#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)

    [36.17.6. Security Considerations for Extensions](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY)

    [36.17.7. Extension Example](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)

[36.18. Extension Building Infrastructure](extend-pgxs.md)

<a id="id-1.8.3.2"></a>

In the sections that follow, we will discuss how you
can extend the PostgreSQL
SQL query language by adding:

* functions (starting in [Section 36.3](xfunc.md))
* aggregates (starting in [Section 36.12](xaggr.md))
* data types (starting in [Section 36.13](xtypes.md))
* operators (starting in [Section 36.14](xoper.md))
* operator classes for indexes (starting in [Section 36.16](xindex.md))
* packages of related objects (starting in [Section 36.17](extend-extensions.md))

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend.html)（英文原文，待翻譯）
