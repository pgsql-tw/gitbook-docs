<a id="PLPGSQL"></a>

# 43. PL/pgSQL - SQL Procedural Language

<strong>Table of Contents</strong>

[43.1. Overview](overview.md)

[43.1.1. Advantages of Using PL/pgSQL](overview.md#PLPGSQL-ADVANTAGES)

[43.1.2. Supported Argument and Result Data Types](overview.md#PLPGSQL-ARGS-RESULTS)

[43.2. Structure of PL/pgSQL](structure-of-pl-pgsql.md)

[43.3. Declarations](declarations.md)

[43.3.1. Declaring Function Parameters](declarations.md#PLPGSQL-DECLARATION-PARAMETERS)

[43.3.2. `ALIAS`](declarations.md#PLPGSQL-DECLARATION-ALIAS)

[43.3.3. Copying Types](declarations.md#PLPGSQL-DECLARATION-TYPE)

[43.3.4. Row Types](declarations.md#PLPGSQL-DECLARATION-ROWTYPES)

[43.3.5. Record Types](declarations.md#PLPGSQL-DECLARATION-RECORDS)

[43.3.6. Collation of PL/pgSQL Variables](declarations.md#PLPGSQL-DECLARATION-COLLATION)

[43.4. Expressions](expressions.md)

[43.5. Basic Statements](basic-statements.md)

[43.5.1. Assignment](basic-statements.md#PLPGSQL-STATEMENTS-ASSIGNMENT)

[43.5.2. Executing SQL Commands](basic-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)

[43.5.3. Executing a Command with a Single-Row Result](basic-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)

[43.5.4. Executing Dynamic Commands](basic-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)

[43.5.5. Obtaining the Result Status](basic-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)

[43.5.6. Doing Nothing At All](basic-statements.md#PLPGSQL-STATEMENTS-NULL)

[43.6. Control Structures](control-structures.md)

[43.6.1. Returning from a Function](control-structures.md#PLPGSQL-STATEMENTS-RETURNING)

[43.6.2. Returning from a Procedure](control-structures.md#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

[43.6.3. Calling a Procedure](control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

[43.6.4. Conditionals](control-structures.md#PLPGSQL-CONDITIONALS)

[43.6.5. Simple Loops](control-structures.md#PLPGSQL-CONTROL-STRUCTURES-LOOPS)

[43.6.6. Looping through Query Results](control-structures.md#PLPGSQL-RECORDS-ITERATING)

[43.6.7. Looping through Arrays](control-structures.md#PLPGSQL-FOREACH-ARRAY)

[43.6.8. Trapping Errors](control-structures.md#PLPGSQL-ERROR-TRAPPING)

[43.6.9. Obtaining Execution Location Information](control-structures.md#PLPGSQL-CALL-STACK)

[43.7. Cursors](43.7.-cursors.md)

[43.7.1. Declaring Cursor Variables](43.7.-cursors.md#PLPGSQL-CURSOR-DECLARATIONS)

[43.7.2. Opening Cursors](43.7.-cursors.md#PLPGSQL-CURSOR-OPENING)

[43.7.3. Using Cursors](43.7.-cursors.md#PLPGSQL-CURSOR-USING)

[43.7.4. Looping through a Cursor's Result](43.7.-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)

[43.8. Transaction Management](43.8.-transaction-management.md)

[43.9. Errors and Messages](43.9.-errors-and-messages.md)

[43.9.1. Reporting Errors and Messages](43.9.-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)

[43.9.2. Checking Assertions](43.9.-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

[43.10. Trigger Functions](43.10.-trigger-functions.md)

[43.10.1. Triggers on Data Changes](43.10.-trigger-functions.md#PLPGSQL-DML-TRIGGER)

[43.10.2. Triggers on Events](43.10.-trigger-functions.md#PLPGSQL-EVENT-TRIGGER)

[43.11. PL/pgSQL under the Hood](43.11.-pl-pgsql-under-the-hood.md)

[43.11.1. Variable Substitution](43.11.-pl-pgsql-under-the-hood.md#PLPGSQL-VAR-SUBST)

[43.11.2. Plan Caching](43.11.-pl-pgsql-under-the-hood.md#PLPGSQL-PLAN-CACHING)

[43.12. Tips for Developing in PL/pgSQL](43.12.-tips-for-developing-in-pl-pgsql.md)

[43.12.1. Handling of Quotation Marks](43.12.-tips-for-developing-in-pl-pgsql.md#PLPGSQL-QUOTE-TIPS)

[43.12.2. Additional Compile-Time and Run-Time Checks](43.12.-tips-for-developing-in-pl-pgsql.md#PLPGSQL-EXTRA-CHECKS)

[43.13. Porting from Oracle PL/SQL](43.13.-porting-from-oracle-pl-sql.md)

[43.13.1. Porting Examples](43.13.-porting-from-oracle-pl-sql.md#id-1.8.8.15.6)

[43.13.2. Other Things to Watch For](43.13.-porting-from-oracle-pl-sql.md#PLPGSQL-PORTING-OTHER)

[43.13.3. Appendix](43.13.-porting-from-oracle-pl-sql.md#PLPGSQL-PORTING-APPENDIX)

<a id="id-1.8.8.2"></a>

---

原文：[PostgreSQL 15.19 Documentation](README.md)（英文原文，待翻譯）
