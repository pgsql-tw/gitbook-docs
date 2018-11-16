---
description: 版本：11
---

# 42. Procedural Languages

PostgreSQL allows user-defined functions to be written in other languages besides SQL and C. These other languages are generically called _procedural languages_ \(PLs\). For a function written in a procedural language, the database server has no built-in knowledge about how to interpret the function's source text. Instead, the task is passed to a special handler that knows the details of the language. The handler could either do all the work of parsing, syntax analysis, execution, etc. itself, or it could serve as “glue” between PostgreSQL and an existing implementation of a programming language. The handler itself is a C language function compiled into a shared object and loaded on demand, just like any other C function.

There are currently four procedural languages available in the standard PostgreSQL distribution: PL/pgSQL \([Chapter 43](https://www.postgresql.org/docs/current/plpgsql.html)\), PL/Tcl \([Chapter 44](https://www.postgresql.org/docs/current/pltcl.html)\), PL/Perl \([Chapter 45](https://www.postgresql.org/docs/current/plperl.html)\), and PL/Python \([Chapter 46](https://www.postgresql.org/docs/current/plpython.html)\). There are additional procedural languages available that are not included in the core distribution. [Appendix H](https://www.postgresql.org/docs/current/external-projects.html) has information about finding them. In addition other languages can be defined by users; the basics of developing a new procedural language are covered in [Chapter 56](https://www.postgresql.org/docs/current/plhandler.html).

