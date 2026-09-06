## Chapter 41. PL/pgSQL — SQL Procedural Language

**Table of Contents**

[41.1. Overview](plpgsql-overview.md)
:   [41.1.1. Advantages of Using PL/pgSQL](plpgsql-overview.md#PLPGSQL-ADVANTAGES)

    [41.1.2. Supported Argument and Result Data Types](plpgsql-overview.md#PLPGSQL-ARGS-RESULTS)

[41.2. Structure of PL/pgSQL](plpgsql-structure.md)

[41.3. Declarations](plpgsql-declarations.md)
:   [41.3.1. Declaring Function Parameters](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)

    [41.3.2. `ALIAS`](plpgsql-declarations.md#PLPGSQL-DECLARATION-ALIAS)

    [41.3.3. Copying Types](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE)

    [41.3.4. Row Types](plpgsql-declarations.md#PLPGSQL-DECLARATION-ROWTYPES)

    [41.3.5. Record Types](plpgsql-declarations.md#PLPGSQL-DECLARATION-RECORDS)

    [41.3.6. Collation of PL/pgSQL Variables](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)

[41.4. Expressions](plpgsql-expressions.md)

[41.5. Basic Statements](plpgsql-statements.md)
:   [41.5.1. Assignment](plpgsql-statements.md#PLPGSQL-STATEMENTS-ASSIGNMENT)

    [41.5.2. Executing SQL Commands](plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)

    [41.5.3. Executing a Command with a Single-Row Result](plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)

    [41.5.4. Executing Dynamic Commands](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)

    [41.5.5. Obtaining the Result Status](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)

    [41.5.6. Doing Nothing At All](plpgsql-statements.md#PLPGSQL-STATEMENTS-NULL)

[41.6. Control Structures](plpgsql-control-structures.md)
:   [41.6.1. Returning from a Function](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING)

    [41.6.2. Returning from a Procedure](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

    [41.6.3. Calling a Procedure](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

    [41.6.4. Conditionals](plpgsql-control-structures.md#PLPGSQL-CONDITIONALS)

    [41.6.5. Simple Loops](plpgsql-control-structures.md#PLPGSQL-CONTROL-STRUCTURES-LOOPS)

    [41.6.6. Looping through Query Results](plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING)

    [41.6.7. Looping through Arrays](plpgsql-control-structures.md#PLPGSQL-FOREACH-ARRAY)

    [41.6.8. Trapping Errors](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)

    [41.6.9. Obtaining Execution Location Information](plpgsql-control-structures.md#PLPGSQL-CALL-STACK)

[41.7. Cursors](plpgsql-cursors.md)
:   [41.7.1. Declaring Cursor Variables](plpgsql-cursors.md#PLPGSQL-CURSOR-DECLARATIONS)

    [41.7.2. Opening Cursors](plpgsql-cursors.md#PLPGSQL-CURSOR-OPENING)

    [41.7.3. Using Cursors](plpgsql-cursors.md#PLPGSQL-CURSOR-USING)

    [41.7.4. Looping through a Cursor's Result](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)

[41.8. Transaction Management](plpgsql-transactions.md)

[41.9. Errors and Messages](plpgsql-errors-and-messages.md)
:   [41.9.1. Reporting Errors and Messages](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)

    [41.9.2. Checking Assertions](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

[41.10. Trigger Functions](plpgsql-trigger.md)
:   [41.10.1. Triggers on Data Changes](plpgsql-trigger.md#PLPGSQL-DML-TRIGGER)

    [41.10.2. Triggers on Events](plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER)

[41.11. PL/pgSQL under the Hood](plpgsql-implementation.md)
:   [41.11.1. Variable Substitution](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)

    [41.11.2. Plan Caching](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)

[41.12. Tips for Developing in PL/pgSQL](plpgsql-development-tips.md)
:   [41.12.1. Handling of Quotation Marks](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)

    [41.12.2. Additional Compile-Time and Run-Time Checks](plpgsql-development-tips.md#PLPGSQL-EXTRA-CHECKS)

[41.13. Porting from Oracle PL/SQL](plpgsql-porting.md)
:   [41.13.1. Porting Examples](plpgsql-porting.md#PLPGSQL-PORTING-EXAMPLES)

    [41.13.2. Other Things to Watch For](plpgsql-porting.md#PLPGSQL-PORTING-OTHER)

    [41.13.3. Appendix](plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX)

<a id="id-1.8.8.2"></a>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql.html)（英文原文，待翻譯）
