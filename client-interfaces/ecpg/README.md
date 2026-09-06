## Chapter 34. ECPG — Embedded SQL in C

**Table of Contents**

[34.1. The Concept](ecpg-concept.md)

[34.2. Managing Database Connections](ecpg-connect.md)
:   [34.2.1. Connecting to the Database Server](ecpg-connect.md#ECPG-CONNECTING)

    [34.2.2. Choosing a Connection](ecpg-connect.md#ECPG-SET-CONNECTION)

    [34.2.3. Closing a Connection](ecpg-connect.md#ECPG-DISCONNECT)

[34.3. Running SQL Commands](ecpg-commands.md)
:   [34.3.1. Executing SQL Statements](ecpg-commands.md#ECPG-EXECUTING)

    [34.3.2. Using Cursors](ecpg-commands.md#ECPG-CURSORS)

    [34.3.3. Managing Transactions](ecpg-commands.md#ECPG-TRANSACTIONS)

    [34.3.4. Prepared Statements](ecpg-commands.md#ECPG-PREPARED)

[34.4. Using Host Variables](ecpg-variables.md)
:   [34.4.1. Overview](ecpg-variables.md#ECPG-VARIABLES-OVERVIEW)

    [34.4.2. Declare Sections](ecpg-variables.md#ECPG-DECLARE-SECTIONS)

    [34.4.3. Retrieving Query Results](ecpg-variables.md#ECPG-RETRIEVING)

    [34.4.4. Type Mapping](ecpg-variables.md#ECPG-VARIABLES-TYPE-MAPPING)

    [34.4.5. Handling Nonprimitive SQL Data Types](ecpg-variables.md#ECPG-VARIABLES-NONPRIMITIVE-SQL)

    [34.4.6. Indicators](ecpg-variables.md#ECPG-INDICATORS)

[34.5. Dynamic SQL](ecpg-dynamic.md)
:   [34.5.1. Executing Statements without a Result Set](ecpg-dynamic.md#ECPG-DYNAMIC-WITHOUT-RESULT)

    [34.5.2. Executing a Statement with Input Parameters](ecpg-dynamic.md#ECPG-DYNAMIC-INPUT)

    [34.5.3. Executing a Statement with a Result Set](ecpg-dynamic.md#ECPG-DYNAMIC-WITH-RESULT)

[34.6. pgtypes Library](ecpg-pgtypes.md)
:   [34.6.1. Character Strings](ecpg-pgtypes.md#ECPG-PGTYPES-CSTRINGS)

    [34.6.2. The numeric Type](ecpg-pgtypes.md#ECPG-PGTYPES-NUMERIC)

    [34.6.3. The date Type](ecpg-pgtypes.md#ECPG-PGTYPES-DATE)

    [34.6.4. The timestamp Type](ecpg-pgtypes.md#ECPG-PGTYPES-TIMESTAMP)

    [34.6.5. The interval Type](ecpg-pgtypes.md#ECPG-PGTYPES-INTERVAL)

    [34.6.6. The decimal Type](ecpg-pgtypes.md#ECPG-PGTYPES-DECIMAL)

    [34.6.7. errno Values of pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-ERRNO)

    [34.6.8. Special Constants of pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-CONSTANTS)

[34.7. Using Descriptor Areas](ecpg-descriptors.md)
:   [34.7.1. Named SQL Descriptor Areas](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS)

    [34.7.2. SQLDA Descriptor Areas](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS)

[34.8. Error Handling](ecpg-errors.md)
:   [34.8.1. Setting Callbacks](ecpg-errors.md#ECPG-WHENEVER)

    [34.8.2. sqlca](ecpg-errors.md#ECPG-SQLCA)

    [34.8.3. `SQLSTATE` vs. `SQLCODE`](ecpg-errors.md#ECPG-SQLSTATE-SQLCODE)

[34.9. Preprocessor Directives](ecpg-preproc.md)
:   [34.9.1. Including Files](ecpg-preproc.md#ECPG-INCLUDE)

    [34.9.2. The define and undef Directives](ecpg-preproc.md#ECPG-DEFINE)

    [34.9.3. ifdef, ifndef, elif, else, and endif Directives](ecpg-preproc.md#ECPG-IFDEF)

[34.10. Processing Embedded SQL Programs](ecpg-process.md)

[34.11. Library Functions](ecpg-library.md)

[34.12. Large Objects](ecpg-lo.md)

[34.13. C++ Applications](ecpg-cpp.md)
:   [34.13.1. Scope for Host Variables](ecpg-cpp.md#ECPG-CPP-SCOPE)

    [34.13.2. C++ Application Development with External C Module](ecpg-cpp.md#ECPG-CPP-AND-C)

[34.14. Embedded SQL Commands](ecpg-sql-commands.md)
:   [ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md) — allocate an SQL descriptor area

    [CONNECT](ecpg-sql-connect.md) — establish a database connection

    [DEALLOCATE DESCRIPTOR](ecpg-sql-deallocate-descriptor.md) — deallocate an SQL descriptor area

    [DECLARE](ecpg-sql-declare.md) — define a cursor

    [DECLARE STATEMENT](ecpg-sql-declare-statement.md) — declare SQL statement identifier

    [DESCRIBE](ecpg-sql-describe.md) — obtain information about a prepared statement or result set

    [DISCONNECT](ecpg-sql-disconnect.md) — terminate a database connection

    [EXECUTE IMMEDIATE](ecpg-sql-execute-immediate.md) — dynamically prepare and execute a statement

    [GET DESCRIPTOR](ecpg-sql-get-descriptor.md) — get information from an SQL descriptor area

    [OPEN](ecpg-sql-open.md) — open a dynamic cursor

    [PREPARE](ecpg-sql-prepare.md) — prepare a statement for execution

    [SET AUTOCOMMIT](ecpg-sql-set-autocommit.md) — set the autocommit behavior of the current session

    [SET CONNECTION](ecpg-sql-set-connection.md) — select a database connection

    [SET DESCRIPTOR](ecpg-sql-set-descriptor.md) — set information in an SQL descriptor area

    [TYPE](ecpg-sql-type.md) — define a new data type

    [VAR](ecpg-sql-var.md) — define a variable

    [WHENEVER](ecpg-sql-whenever.md) — specify the action to be taken when an SQL statement causes a specific class condition to be raised

[34.15. Informix Compatibility Mode](ecpg-informix-compat.md)
:   [34.15.1. Additional Types](ecpg-informix-compat.md#ECPG-INFORMIX-TYPES)

    [34.15.2. Additional/Missing Embedded SQL Statements](ecpg-informix-compat.md#ECPG-INFORMIX-STATEMENTS)

    [34.15.3. Informix-compatible SQLDA Descriptor Areas](ecpg-informix-compat.md#ECPG-INFORMIX-SQLDA)

    [34.15.4. Additional Functions](ecpg-informix-compat.md#ECPG-INFORMIX-FUNCTIONS)

    [34.15.5. Additional Constants](ecpg-informix-compat.md#ECPG-INFORMIX-CONSTANTS)

[34.16. Oracle Compatibility Mode](ecpg-oracle-compat.md)

[34.17. Internals](ecpg-develop.md)

<a id="id-1.7.5.2"></a><a id="id-1.7.5.3"></a><a id="id-1.7.5.4"></a>

This chapter describes the embedded SQL package
for PostgreSQL. It was written by
Linus Tolke (`<linus@epact.se>`) and Michael Meskes
(`<meskes@postgresql.org>`). Originally it was written to work with
C. It also works with C++, but
it does not recognize all C++ constructs yet.

This documentation is quite incomplete. But since this
interface is standardized, additional information can be found in
many resources about SQL.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg.html)（英文原文，待翻譯）
