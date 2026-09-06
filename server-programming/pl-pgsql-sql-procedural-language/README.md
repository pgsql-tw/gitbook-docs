<a id="PLPGSQL"></a>

# 43. PL/pgSQL - SQL Procedural Language

<strong>Table of Contents</strong>

[43.1. Overview](overview.md)

[43.1.1. Advantages of Using PL/pgSQL](https://www.postgresql.org/docs/15/plpgsql-overview.html#PLPGSQL-ADVANTAGES)

[43.1.2. Supported Argument and Result Data Types](https://www.postgresql.org/docs/15/plpgsql-overview.html#PLPGSQL-ARGS-RESULTS)

[43.2. Structure of PL/pgSQL](structure-of-pl-pgsql.md)

[43.3. Declarations](declarations.md)

[43.3.1. Declaring Function Parameters](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-PARAMETERS)

[43.3.2. `ALIAS`](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-ALIAS)

[43.3.3. Copying Types](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-TYPE)

[43.3.4. Row Types](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-ROWTYPES)

[43.3.5. Record Types](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-RECORDS)

[43.3.6. Collation of PL/pgSQL Variables](https://www.postgresql.org/docs/15/plpgsql-declarations.html#PLPGSQL-DECLARATION-COLLATION)

[43.4. Expressions](expressions.md)

[43.5. Basic Statements](basic-statements.md)

[43.5.1. Assignment](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-ASSIGNMENT)

[43.5.2. Executing SQL Commands](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-GENERAL-SQL)

[43.5.3. Executing a Command with a Single-Row Result](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-SQL-ONEROW)

[43.5.4. Executing Dynamic Commands](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN)

[43.5.5. Obtaining the Result Status](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-DIAGNOSTICS)

[43.5.6. Doing Nothing At All](https://www.postgresql.org/docs/15/plpgsql-statements.html#PLPGSQL-STATEMENTS-NULL)

[43.6. Control Structures](control-structures.md)

[43.6.1. Returning from a Function](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING)

[43.6.2. Returning from a Procedure](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

[43.6.3. Calling a Procedure](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

[43.6.4. Conditionals](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-CONDITIONALS)

[43.6.5. Simple Loops](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-CONTROL-STRUCTURES-LOOPS)

[43.6.6. Looping through Query Results](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-RECORDS-ITERATING)

[43.6.7. Looping through Arrays](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-FOREACH-ARRAY)

[43.6.8. Trapping Errors](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-ERROR-TRAPPING)

[43.6.9. Obtaining Execution Location Information](https://www.postgresql.org/docs/15/plpgsql-control-structures.html#PLPGSQL-CALL-STACK)

[43.7. Cursors](43.7.-cursors.md)

[43.7.1. Declaring Cursor Variables](https://www.postgresql.org/docs/15/plpgsql-cursors.html#PLPGSQL-CURSOR-DECLARATIONS)

[43.7.2. Opening Cursors](https://www.postgresql.org/docs/15/plpgsql-cursors.html#PLPGSQL-CURSOR-OPENING)

[43.7.3. Using Cursors](https://www.postgresql.org/docs/15/plpgsql-cursors.html#PLPGSQL-CURSOR-USING)

[43.7.4. Looping through a Cursor's Result](https://www.postgresql.org/docs/15/plpgsql-cursors.html#PLPGSQL-CURSOR-FOR-LOOP)

[43.8. Transaction Management](43.8.-transaction-management.md)

[43.9. Errors and Messages](43.9.-errors-and-messages.md)

[43.9.1. Reporting Errors and Messages](https://www.postgresql.org/docs/15/plpgsql-errors-and-messages.html#PLPGSQL-STATEMENTS-RAISE)

[43.9.2. Checking Assertions](https://www.postgresql.org/docs/15/plpgsql-errors-and-messages.html#PLPGSQL-STATEMENTS-ASSERT)

[43.10. Trigger Functions](43.10.-trigger-functions.md)

[43.10.1. Triggers on Data Changes](https://www.postgresql.org/docs/15/plpgsql-trigger.html#PLPGSQL-DML-TRIGGER)

[43.10.2. Triggers on Events](https://www.postgresql.org/docs/15/plpgsql-trigger.html#PLPGSQL-EVENT-TRIGGER)

[43.11. PL/pgSQL under the Hood](43.11.-pl-pgsql-under-the-hood.md)

[43.11.1. Variable Substitution](https://www.postgresql.org/docs/15/plpgsql-implementation.html#PLPGSQL-VAR-SUBST)

[43.11.2. Plan Caching](https://www.postgresql.org/docs/15/plpgsql-implementation.html#PLPGSQL-PLAN-CACHING)

[43.12. Tips for Developing in PL/pgSQL](43.12.-tips-for-developing-in-pl-pgsql.md)

[43.12.1. Handling of Quotation Marks](https://www.postgresql.org/docs/15/plpgsql-development-tips.html#PLPGSQL-QUOTE-TIPS)

[43.12.2. Additional Compile-Time and Run-Time Checks](https://www.postgresql.org/docs/15/plpgsql-development-tips.html#PLPGSQL-EXTRA-CHECKS)

[43.13. Porting from Oracle PL/SQL](43.13.-porting-from-oracle-pl-sql.md)

[43.13.1. Porting Examples](https://www.postgresql.org/docs/15/plpgsql-porting.html#id-1.8.8.15.6)

[43.13.2. Other Things to Watch For](https://www.postgresql.org/docs/15/plpgsql-porting.html#PLPGSQL-PORTING-OTHER)

[43.13.3. Appendix](https://www.postgresql.org/docs/15/plpgsql-porting.html#PLPGSQL-PORTING-APPENDIX)

<a id="id-1.8.8.2"></a>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/plpgsql.html)（英文原文，待翻譯）
