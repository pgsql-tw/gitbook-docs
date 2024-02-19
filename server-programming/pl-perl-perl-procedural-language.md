# 45. PL/Perl — Perl Procedural Language

PL/Perl is a loadable procedural language that enables you to write PostgreSQL functions in the [Perl programming language](https://www.perl.org).

The main advantage to using PL/Perl is that this allows use, within stored functions, of the manyfold “string munging” operators and functions available for Perl. Parsing complex strings might be easier using Perl than it is with the string functions and control structures provided in PL/pgSQL.

To install PL/Perl in a particular database, use `CREATE EXTENSION plperl`.

#### Tip

If a language is installed into `template1`, all subsequently created databases will have the language installed automatically.

#### Note

Users of source packages must specially enable the build of PL/Perl during the installation process. (Refer to [Chapter 16](https://www.postgresql.org/docs/13/installation.html) for more information.) Users of binary packages might find PL/Perl in a separate subpackage.
