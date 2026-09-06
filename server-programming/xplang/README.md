## Chapter 40. Procedural Languages

**Table of Contents**

[40.1. Installing Procedural Languages](xplang-install.md)

<a id="id-1.8.7.2"></a>

PostgreSQL allows user-defined functions
to be written in other languages besides SQL and C. These other
languages are generically called *procedural
languages* (PLs). For a function
written in a procedural language, the database server has
no built-in knowledge about how to interpret the function's source
text. Instead, the task is passed to a special handler that knows
the details of the language. The handler could either do all the
work of parsing, syntax analysis, execution, etc. itself, or it
could serve as “glue” between
PostgreSQL and an existing implementation
of a programming language. The handler itself is a
C language function compiled into a shared object and
loaded on demand, just like any other C function.

There are currently four procedural languages available in the
standard PostgreSQL distribution:
PL/pgSQL ([Chapter 41](../plpgsql/README.md)),
PL/Tcl ([Chapter 42](../pltcl/README.md)),
PL/Perl ([Chapter 43](../plperl/README.md)), and
PL/Python ([Chapter 44](../plpython/README.md)).
There are additional procedural languages available that are not
included in the core distribution. [Appendix H](../../appendixes/external-projects/README.md)
has information about finding them. In addition other languages can
be defined by users; the basics of developing a new procedural
language are covered in [Chapter 57](../../internals/plhandler/README.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xplang.html)（英文原文，待翻譯）
