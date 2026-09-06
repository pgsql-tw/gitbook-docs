## Chapter 37. Triggers

**Table of Contents**

[37.1. Overview of Trigger Behavior](trigger-definition.md)

[37.2. Visibility of Data Changes](trigger-datachanges.md)

[37.3. Writing Trigger Functions in C](trigger-interface.md)

[37.4. A Complete Trigger Example](trigger-example.md)

<a id="id-1.8.4.2"></a>

This chapter provides general information about writing trigger functions.
Trigger functions can be written in most of the available procedural
languages, including
PL/pgSQL ([Chapter 41](../plpgsql/README.md)),
PL/Tcl ([Chapter 42](../pltcl/README.md)),
PL/Perl ([Chapter 43](../plperl/README.md)), and
PL/Python ([Chapter 44](../plpython/README.md)).
After reading this chapter, you should consult the chapter for
your favorite procedural language to find out the language-specific
details of writing a trigger in it.

It is also possible to write a trigger function in C, although
most people find it easier to use one of the procedural languages.
It is not currently possible to write a trigger function in the
plain SQL function language.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/triggers.html)（英文原文，待翻譯）
