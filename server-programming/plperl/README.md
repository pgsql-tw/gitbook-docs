## Chapter 43. PL/Perl — Perl Procedural Language

**Table of Contents**

[43.1. PL/Perl Functions and Arguments](plperl-funcs.md)

[43.2. Data Values in PL/Perl](plperl-data.md)

[43.3. Built-in Functions](plperl-builtins.md)
:   [43.3.1. Database Access from PL/Perl](plperl-builtins.md#PLPERL-DATABASE)

    [43.3.2. Utility Functions in PL/Perl](plperl-builtins.md#PLPERL-UTILITY-FUNCTIONS)

[43.4. Global Values in PL/Perl](plperl-global.md)

[43.5. Trusted and Untrusted PL/Perl](plperl-trusted.md)

[43.6. PL/Perl Triggers](plperl-triggers.md)

[43.7. PL/Perl Event Triggers](plperl-event-triggers.md)

[43.8. PL/Perl Under the Hood](plperl-under-the-hood.md)
:   [43.8.1. Configuration](plperl-under-the-hood.md#PLPERL-CONFIG)

    [43.8.2. Limitations and Missing Features](plperl-under-the-hood.md#PLPERL-MISSING)

<a id="id-1.8.10.2"></a><a id="id-1.8.10.3"></a>

PL/Perl is a loadable procedural language that enables you to write
PostgreSQL functions and procedures in the
[Perl programming language](https://www.perl.org).

The main advantage to using PL/Perl is that this allows use,
within stored functions and procedures, of the manyfold “string
munging” operators and functions available for Perl. Parsing
complex strings might be easier using Perl than it is with the
string functions and control structures provided in PL/pgSQL.

To install PL/Perl in a particular database, use
`CREATE EXTENSION plperl`.

### Tip

If a language is installed into `template1`, all subsequently
created databases will have the language installed automatically.

### Note

Users of source packages must specially enable the build of
PL/Perl during the installation process. (Refer to [Chapter 17](../../server-administration/installation/README.md) for more information.) Users of
binary packages might find PL/Perl in a separate subpackage.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl.html)（英文原文，待翻譯）
