# Part V. Server Programming

<a id="id-1.8.2"></a>

This part is about extending the server functionality with
user-defined functions, data types, triggers, etc. These are
advanced topics which should be approached only after all
the other user documentation about PostgreSQL has
been understood. Later chapters in this part describe the server-side
programming languages available in the
PostgreSQL distribution as well as
general issues concerning server-side programming. It
is essential to read at least the earlier sections of [Chapter 36](extend/README.md) (covering functions) before diving into the
material about server-side programming.

**Table of Contents**

[36. Extending SQL](extend/README.md)
:   [36.1. How Extensibility Works](extend/extend-how.md)

    [36.2. The PostgreSQL Type System](extend/extend-type-system.md)

    [36.3. User-Defined Functions](extend/xfunc.md)

    [36.4. User-Defined Procedures](extend/xproc.md)

    [36.5. Query Language (SQL) Functions](extend/xfunc-sql.md)

    [36.6. Function Overloading](extend/xfunc-overload.md)

    [36.7. Function Volatility Categories](extend/xfunc-volatility.md)

    [36.8. Procedural Language Functions](extend/xfunc-pl.md)

    [36.9. Internal Functions](extend/xfunc-internal.md)

    [36.10. C-Language Functions](extend/xfunc-c.md)

    [36.11. Function Optimization Information](extend/xfunc-optimization.md)

    [36.12. User-Defined Aggregates](extend/xaggr.md)

    [36.13. User-Defined Types](extend/xtypes.md)

    [36.14. User-Defined Operators](extend/xoper.md)

    [36.15. Operator Optimization Information](extend/xoper-optimization.md)

    [36.16. Interfacing Extensions to Indexes](extend/xindex.md)

    [36.17. Packaging Related Objects into an Extension](extend/extend-extensions.md)

    [36.18. Extension Building Infrastructure](extend/extend-pgxs.md)

[37. Triggers](triggers/README.md)
:   [37.1. Overview of Trigger Behavior](triggers/trigger-definition.md)

    [37.2. Visibility of Data Changes](triggers/trigger-datachanges.md)

    [37.3. Writing Trigger Functions in C](triggers/trigger-interface.md)

    [37.4. A Complete Trigger Example](triggers/trigger-example.md)

[38. Event Triggers](event-triggers/README.md)
:   [38.1. Overview of Event Trigger Behavior](event-triggers/event-trigger-definition.md)

    [38.2. Writing Event Trigger Functions in C](event-triggers/event-trigger-interface.md)

    [38.3. A Complete Event Trigger Example](event-triggers/event-trigger-example.md)

    [38.4. A Table Rewrite Event Trigger Example](event-triggers/event-trigger-table-rewrite-example.md)

    [38.5. A Database Login Event Trigger Example](event-triggers/event-trigger-database-login-example.md)

[39. The Rule System](rules/README.md)
:   [39.1. The Query Tree](rules/querytree.md)

    [39.2. Views and the Rule System](rules/rules-views.md)

    [39.3. Materialized Views](rules/rules-materializedviews.md)

    [39.4. Rules on `INSERT`, `UPDATE`, and `DELETE`](rules/rules-update.md)

    [39.5. Rules and Privileges](rules/rules-privileges.md)

    [39.6. Rules and Command Status](rules/rules-status.md)

    [39.7. Rules Versus Triggers](rules/rules-triggers.md)

[40. Procedural Languages](xplang/README.md)
:   [40.1. Installing Procedural Languages](xplang/xplang-install.md)

[41. PL/pgSQL — SQL Procedural Language](plpgsql/README.md)
:   [41.1. Overview](plpgsql/plpgsql-overview.md)

    [41.2. Structure of PL/pgSQL](plpgsql/plpgsql-structure.md)

    [41.3. Declarations](plpgsql/plpgsql-declarations.md)

    [41.4. Expressions](plpgsql/plpgsql-expressions.md)

    [41.5. Basic Statements](plpgsql/plpgsql-statements.md)

    [41.6. Control Structures](plpgsql/plpgsql-control-structures.md)

    [41.7. Cursors](plpgsql/plpgsql-cursors.md)

    [41.8. Transaction Management](plpgsql/plpgsql-transactions.md)

    [41.9. Errors and Messages](plpgsql/plpgsql-errors-and-messages.md)

    [41.10. Trigger Functions](plpgsql/plpgsql-trigger.md)

    [41.11. PL/pgSQL under the Hood](plpgsql/plpgsql-implementation.md)

    [41.12. Tips for Developing in PL/pgSQL](plpgsql/plpgsql-development-tips.md)

    [41.13. Porting from Oracle PL/SQL](plpgsql/plpgsql-porting.md)

[42. PL/Tcl — Tcl Procedural Language](pltcl/README.md)
:   [42.1. Overview](pltcl/pltcl-overview.md)

    [42.2. PL/Tcl Functions and Arguments](pltcl/pltcl-functions.md)

    [42.3. Data Values in PL/Tcl](pltcl/pltcl-data.md)

    [42.4. Global Data in PL/Tcl](pltcl/pltcl-global.md)

    [42.5. Database Access from PL/Tcl](pltcl/pltcl-dbaccess.md)

    [42.6. Trigger Functions in PL/Tcl](pltcl/pltcl-trigger.md)

    [42.7. Event Trigger Functions in PL/Tcl](pltcl/pltcl-event-trigger.md)

    [42.8. Error Handling in PL/Tcl](pltcl/pltcl-error-handling.md)

    [42.9. Explicit Subtransactions in PL/Tcl](pltcl/pltcl-subtransactions.md)

    [42.10. Transaction Management](pltcl/pltcl-transactions.md)

    [42.11. PL/Tcl Configuration](pltcl/pltcl-config.md)

    [42.12. Tcl Procedure Names](pltcl/pltcl-procnames.md)

[43. PL/Perl — Perl Procedural Language](plperl/README.md)
:   [43.1. PL/Perl Functions and Arguments](plperl/plperl-funcs.md)

    [43.2. Data Values in PL/Perl](plperl/plperl-data.md)

    [43.3. Built-in Functions](plperl/plperl-builtins.md)

    [43.4. Global Values in PL/Perl](plperl/plperl-global.md)

    [43.5. Trusted and Untrusted PL/Perl](plperl/plperl-trusted.md)

    [43.6. PL/Perl Triggers](plperl/plperl-triggers.md)

    [43.7. PL/Perl Event Triggers](plperl/plperl-event-triggers.md)

    [43.8. PL/Perl Under the Hood](plperl/plperl-under-the-hood.md)

[44. PL/Python — Python Procedural Language](plpython/README.md)
:   [44.1. PL/Python Functions](plpython/plpython-funcs.md)

    [44.2. Data Values](plpython/plpython-data.md)

    [44.3. Sharing Data](plpython/plpython-sharing.md)

    [44.4. Anonymous Code Blocks](plpython/plpython-do.md)

    [44.5. Trigger Functions](plpython/plpython-trigger.md)

    [44.6. Database Access](plpython/plpython-database.md)

    [44.7. Explicit Subtransactions](plpython/plpython-subtransaction.md)

    [44.8. Transaction Management](plpython/plpython-transactions.md)

    [44.9. Utility Functions](plpython/plpython-util.md)

    [44.10. Python 2 vs. Python 3](plpython/plpython-python23.md)

    [44.11. Environment Variables](plpython/plpython-envar.md)

[45. Server Programming Interface](spi/README.md)
:   [45.1. Interface Functions](spi/spi-interface.md)

    [45.2. Interface Support Functions](spi/spi-interface-support.md)

    [45.3. Memory Management](spi/spi-memory.md)

    [45.4. Transaction Management](spi/spi-transaction.md)

    [45.5. Visibility of Data Changes](spi/spi-visibility.md)

    [45.6. Examples](spi/spi-examples.md)

[46. Background Worker Processes](bgworker/README.md)

[47. Logical Decoding](logicaldecoding/README.md)
:   [47.1. Logical Decoding Examples](logicaldecoding/logicaldecoding-example.md)

    [47.2. Logical Decoding Concepts](logicaldecoding/logicaldecoding-explanation.md)

    [47.3. Streaming Replication Protocol Interface](logicaldecoding/logicaldecoding-walsender.md)

    [47.4. Logical Decoding SQL Interface](logicaldecoding/logicaldecoding-sql.md)

    [47.5. System Catalogs Related to Logical Decoding](logicaldecoding/logicaldecoding-catalogs.md)

    [47.6. Logical Decoding Output Plugins](logicaldecoding/logicaldecoding-output-plugin.md)

    [47.7. Logical Decoding Output Writers](logicaldecoding/logicaldecoding-writer.md)

    [47.8. Synchronous Replication Support for Logical Decoding](logicaldecoding/logicaldecoding-synchronous.md)

    [47.9. Streaming of Large Transactions for Logical Decoding](logicaldecoding/logicaldecoding-streaming.md)

    [47.10. Two-phase Commit Support for Logical Decoding](logicaldecoding/logicaldecoding-two-phase-commits.md)

[48. Replication Progress Tracking](replication-origins/README.md)

[49. Archive Modules](archive-modules/README.md)
:   [49.1. Initialization Functions](archive-modules/archive-module-init.md)

    [49.2. Archive Module Callbacks](archive-modules/archive-module-callbacks.md)

[50. OAuth Validator Modules](oauth-validators/README.md)
:   [50.1. Safely Designing a Validator Module](oauth-validators/oauth-validator-design.md)

    [50.2. Initialization Functions](oauth-validators/oauth-validator-init.md)

    [50.3. OAuth Validator Callbacks](oauth-validators/oauth-validator-callbacks.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/server-programming.html)（英文原文，待翻譯）
