## 43.2. Data Values in PL/Perl [#](#PLPERL-DATA)

The argument values supplied to a PL/Perl function's code are
simply the input arguments converted to text form (just as if they
had been displayed by a `SELECT` statement).
Conversely, the `return` and `return_next`
commands will accept any string that is acceptable input format
for the function's declared return type.

If this behavior is inconvenient for a particular case, it can be
improved by using a transform, as already illustrated
for `bool` values. Several examples of transform modules
are included in the PostgreSQL distribution.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-data.html)（英文原文，待翻譯）
