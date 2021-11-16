# 38. Triggers

This chapter provides general information about writing trigger functions. Trigger functions can be written in most of the available procedural languages, including PL/pgSQL ([Chapter 42](https://www.postgresql.org/docs/13/plpgsql.html)), PL/Tcl ([Chapter 43](https://www.postgresql.org/docs/13/pltcl.html)), PL/Perl ([Chapter 44](https://www.postgresql.org/docs/13/plperl.html)), and PL/Python ([Chapter 45](https://www.postgresql.org/docs/13/plpython.html)). After reading this chapter, you should consult the chapter for your favorite procedural language to find out the language-specific details of writing a trigger in it.

It is also possible to write a trigger function in C, although most people find it easier to use one of the procedural languages. It is not currently possible to write a trigger function in the plain SQL function language.
