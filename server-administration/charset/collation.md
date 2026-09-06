## 23.2. Collation Support [#](#COLLATION)

[23.2.1. Concepts](collation.md#COLLATION-CONCEPTS)

[23.2.2. Managing Collations](collation.md#COLLATION-MANAGING)

[23.2.3. ICU Custom Collations](collation.md#ICU-CUSTOM-COLLATIONS)

<a id="id-1.6.10.4.2"></a>

The collation feature allows specifying the sort order and character
classification behavior of data per-column, or even per-operation.
This alleviates the restriction that the
`LC_COLLATE` and `LC_CTYPE` settings
of a database cannot be changed after its creation.

<a id="COLLATION-CONCEPTS"></a>

### 23.2.1. Concepts [#](#COLLATION-CONCEPTS)

Conceptually, every expression of a collatable data type has a
collation. (The built-in collatable data types are
`text`, `varchar`, and `char`.
User-defined base types can also be marked collatable, and of course
a [*[domain](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)*](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN) over a
collatable data type is collatable.) If the
expression is a column reference, the collation of the expression is the
defined collation of the column. If the expression is a constant, the
collation is the default collation of the data type of the
constant. The collation of a more complex expression is derived
from the collations of its inputs, as described below.

The collation of an expression can be the “default”
collation, which means the locale settings defined for the
database. It is also possible for an expression's collation to be
indeterminate. In such cases, ordering operations and other
operations that need to know the collation will fail.

When the database system has to perform an ordering or a character
classification, it uses the collation of the input expression. This
happens, for example, with `ORDER BY` clauses
and function or operator calls such as `<`.
The collation to apply for an `ORDER BY` clause
is simply the collation of the sort key. The collation to apply for a
function or operator call is derived from the arguments, as described
below. In addition to comparison operators, collations are taken into
account by functions that convert between lower and upper case
letters, such as `lower`, `upper`, and
`initcap`; by pattern matching operators; and by
`to_char` and related functions.

For a function or operator call, the collation that is derived by
examining the argument collations is used at run time for performing
the specified operation. If the result of the function or operator
call is of a collatable data type, the collation is also used at parse
time as the defined collation of the function or operator expression,
in case there is a surrounding expression that requires knowledge of
its collation.

The *collation derivation* of an expression can be
implicit or explicit. This distinction affects how collations are
combined when multiple different collations appear in an
expression. An explicit collation derivation occurs when a
`COLLATE` clause is used; all other collation
derivations are implicit. When multiple collations need to be
combined, for example in a function call, the following rules are
used:

1. If any input expression has an explicit collation derivation, then
   all explicitly derived collations among the input expressions must be
   the same, otherwise an error is raised. If any explicitly
   derived collation is present, that is the result of the
   collation combination.
2. Otherwise, all input expressions must have the same implicit
   collation derivation or the default collation. If any non-default
   collation is present, that is the result of the collation combination.
   Otherwise, the result is the default collation.
3. If there are conflicting non-default implicit collations among the
   input expressions, then the combination is deemed to have indeterminate
   collation. This is not an error condition unless the particular
   function being invoked requires knowledge of the collation it should
   apply. If it does, an error will be raised at run-time.

For example, consider this table definition:

```

CREATE TABLE test1 (
    a text COLLATE "de_DE",
    b text COLLATE "es_ES",
    ...
);
```

Then in

```

SELECT a < 'foo' FROM test1;
```

the `<` comparison is performed according to
`de_DE` rules, because the expression combines an
implicitly derived collation with the default collation. But in

```

SELECT a < ('foo' COLLATE "fr_FR") FROM test1;
```

the comparison is performed using `fr_FR` rules,
because the explicit collation derivation overrides the implicit one.
Furthermore, given

```

SELECT a < b FROM test1;
```

the parser cannot determine which collation to apply, since the
`a` and `b` columns have conflicting
implicit collations. Since the `<` operator
does need to know which collation to use, this will result in an
error. The error can be resolved by attaching an explicit collation
specifier to either input expression, thus:

```

SELECT a < b COLLATE "de_DE" FROM test1;
```

or equivalently

```

SELECT a COLLATE "de_DE" < b FROM test1;
```

On the other hand, the structurally similar case

```

SELECT a || b FROM test1;
```

does not result in an error, because the `||` operator
does not care about collations: its result is the same regardless
of the collation.

The collation assigned to a function or operator's combined input
expressions is also considered to apply to the function or operator's
result, if the function or operator delivers a result of a collatable
data type. So, in

```

SELECT * FROM test1 ORDER BY a || 'foo';
```

the ordering will be done according to `de_DE` rules.
But this query:

```

SELECT * FROM test1 ORDER BY a || b;
```

results in an error, because even though the `||` operator
doesn't need to know a collation, the `ORDER BY` clause does.
As before, the conflict can be resolved with an explicit collation
specifier:

```

SELECT * FROM test1 ORDER BY a || b COLLATE "fr_FR";
```

<a id="COLLATION-MANAGING"></a>

### 23.2.2. Managing Collations [#](#COLLATION-MANAGING)

A collation is an SQL schema object that maps an SQL name to locales
provided by libraries installed in the operating system. A collation
definition has a *provider* that specifies which
library supplies the locale data. One standard provider name
is `libc`, which uses the locales provided by the
operating system C library. These are the locales used by most tools
provided by the operating system. Another provider
is `icu`, which uses the external
ICU<a id="id-1.6.10.4.5.2.4"></a> library. ICU locales can only be
used if support for ICU was configured when PostgreSQL was built.

A collation object provided by `libc` maps to a
combination of `LC_COLLATE` and `LC_CTYPE`
settings, as accepted by the `setlocale()` system library call. (As
the name would suggest, the main purpose of a collation is to set
`LC_COLLATE`, which controls the sort order. But
it is rarely necessary in practice to have an
`LC_CTYPE` setting that is different from
`LC_COLLATE`, so it is more convenient to collect
these under one concept than to create another infrastructure for
setting `LC_CTYPE` per expression.) Also,
a `libc` collation
is tied to a character set encoding (see [Section 23.3](multibyte.md)).
The same collation name may exist for different encodings.

A collation object provided by `icu` maps to a named
collator provided by the ICU library. ICU does not support
separate “collate” and “ctype” settings, so
they are always the same. Also, ICU collations are independent of the
encoding, so there is always only one ICU collation of a given name in
a database.

<a id="COLLATION-MANAGING-STANDARD"></a>

#### 23.2.2.1. Standard Collations [#](#COLLATION-MANAGING-STANDARD)

On all platforms, the following collations are supported:

`unicode`
:   This SQL standard collation sorts using the Unicode Collation
    Algorithm with the Default Unicode Collation Element Table. It is
    available in all encodings. ICU support is required to use this
    collation, and behavior may change if PostgreSQL is built with a
    different version of ICU. (This collation has the same behavior as
    the ICU root locale; see [`und-x-icu` (for “undefined”)](collation.md#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU).)

`ucs_basic`
:   This SQL standard collation sorts using the Unicode code point values
    rather than natural language order, and only the ASCII letters
    “`A`” through
    “`Z`” are treated as letters. The
    behavior is efficient and stable across all versions. Only available
    for encoding `UTF8`. (This collation has the same
    behavior as the libc locale specification `C` in
    `UTF8` encoding.)

`pg_unicode_fast`
:   This collation sorts by Unicode code point values rather than natural
    language order. For the functions `lower`,
    `initcap`, and `upper` it uses
    Unicode full case mapping. For pattern matching (including regular
    expressions), it uses the Standard variant of Unicode [Compatibility
    Properties](https://www.unicode.org/reports/tr18/#Compatibility_Properties). Behavior is efficient and stable within a
    Postgres major version. It is only
    available for encoding `UTF8`.

`pg_c_utf8`
:   This collation sorts by Unicode code point values rather than natural
    language order. For the functions `lower`,
    `initcap`, and `upper`, it uses
    Unicode simple case mapping. For pattern matching (including regular
    expressions), it uses the POSIX Compatible variant of Unicode [Compatibility
    Properties](https://www.unicode.org/reports/tr18/#Compatibility_Properties). Behavior is efficient and stable within a
    PostgreSQL major version. This collation is
    only available for encoding `UTF8`.

`C` (equivalent to `POSIX`)
:   The `C` and `POSIX` collations are
    based on “traditional C” behavior. They sort by byte
    values rather than natural language order, and only the ASCII letters
    “`A`” through
    “`Z`” are treated as letters. The
    behavior is efficient and stable across all versions for a given
    database encoding, but behavior may vary between different database
    encodings.

`default`
:   The `default` collation selects the locale specified
    at database creation time.

Additional collations may be available depending on operating system
support. The efficiency and stability of these additional collations
depend on the collation provider, the provider version, and the locale.

<a id="COLLATION-MANAGING-PREDEFINED"></a>

#### 23.2.2.2. Predefined Collations [#](#COLLATION-MANAGING-PREDEFINED)

If the operating system provides support for using multiple locales
within a single program (`newlocale` and related functions),
or if support for ICU is configured,
then when a database cluster is initialized, `initdb`
populates the system catalog `pg_collation` with
collations based on all the locales it finds in the operating
system at the time.

To inspect the currently available locales, use the query `SELECT
* FROM pg_collation`, or the command `\dOS+`
in psql.

<a id="COLLATION-MANAGING-PREDEFINED-LIBC"></a>

##### 23.2.2.2.1. libc Collations [#](#COLLATION-MANAGING-PREDEFINED-LIBC)

For example, the operating system might
provide a locale named `de_DE.utf8`.
`initdb` would then create a collation named
`de_DE.utf8` for encoding `UTF8`
that has both `LC_COLLATE` and
`LC_CTYPE` set to `de_DE.utf8`.
It will also create a collation with the `.utf8`
tag stripped off the name. So you could also use the collation
under the name `de_DE`, which is less cumbersome
to write and makes the name less encoding-dependent. Note that,
nevertheless, the initial set of collation names is
platform-dependent.

The default set of collations provided by `libc` map
directly to the locales installed in the operating system, which can be
listed using the command `locale -a`. In case
a `libc` collation is needed that has different values
for `LC_COLLATE` and `LC_CTYPE`, or if new
locales are installed in the operating system after the database system
was initialized, then a new collation may be created using
the [CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md) command.
New operating system locales can also be imported en masse using
the [`pg_import_system_collations()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-COLLATION) function.

Within any particular database, only collations that use that
database's encoding are of interest. Other entries in
`pg_collation` are ignored. Thus, a stripped collation
name such as `de_DE` can be considered unique
within a given database even though it would not be unique globally.
Use of the stripped collation names is recommended, since it will
make one fewer thing you need to change if you decide to change to
another database encoding. Note however that the `default`,
`C`, and `POSIX` collations can be used regardless of
the database encoding.

PostgreSQL considers distinct collation
objects to be incompatible even when they have identical properties.
Thus for example,

```

SELECT a COLLATE "C" < b COLLATE "POSIX" FROM test1;
```

will draw an error even though the `C` and `POSIX`
collations have identical behaviors. Mixing stripped and non-stripped
collation names is therefore not recommended.

<a id="COLLATION-MANAGING-PREDEFINED-ICU"></a>

##### 23.2.2.2.2. ICU Collations [#](#COLLATION-MANAGING-PREDEFINED-ICU)

With ICU, it is not sensible to enumerate all possible locale names. ICU
uses a particular naming system for locales, but there are many more ways
to name a locale than there are actually distinct locales.
`initdb` uses the ICU APIs to extract a set of distinct
locales to populate the initial set of collations. Collations provided by
ICU are created in the SQL environment with names in BCP 47 language tag
format, with a “private use”
extension `-x-icu` appended, to distinguish them from
libc locales.

Here are some example collations that might be created:

<a id="COLLATION-MANAGING-PREDEFINED-ICU-DE-X-ICU"></a>

`de-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-X-ICU)
:   German collation, default variant
<a id="COLLATION-MANAGING-PREDEFINED-ICU-DE-AT-X-ICU"></a>

`de-AT-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-AT-X-ICU)
:   German collation for Austria, default variant

    (There are also, say, `de-DE-x-icu`
    or `de-CH-x-icu`, but as of this writing, they are
    equivalent to `de-x-icu`.)
<a id="COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU"></a>

`und-x-icu` (for “undefined”) [#](#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU)
:   ICU “root” collation. Use this to get a reasonable
    language-agnostic sort order.

Some (less frequently used) encodings are not supported by ICU. When the
database encoding is one of these, ICU collation entries
in `pg_collation` are ignored. Attempting to use one
will draw an error along the lines of “collation "de-x-icu" for
encoding "WIN874" does not exist”.

<a id="COLLATION-CREATE"></a>

#### 23.2.2.3. Creating New Collation Objects [#](#COLLATION-CREATE)

If the standard and predefined collations are not sufficient, users can
create their own collation objects using the SQL
command [CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md).

The standard and predefined collations are in the
schema `pg_catalog`, like all predefined objects.
User-defined collations should be created in user schemas. This also
ensures that they are saved by `pg_dump`.

<a id="COLLATION-MANAGING-CREATE-LIBC"></a>

##### 23.2.2.3.1. libc Collations [#](#COLLATION-MANAGING-CREATE-LIBC)

New libc collations can be created like this:

```

CREATE COLLATION german (provider = libc, locale = 'de_DE');
```

The exact values that are acceptable for the `locale`
clause in this command depend on the operating system. On Unix-like
systems, the command `locale -a` will show a list.

Since the predefined libc collations already include all collations
defined in the operating system when the database instance is
initialized, it is not often necessary to manually create new ones.
Reasons might be if a different naming system is desired (in which case
see also [Section 23.2.2.3.3](collation.md#COLLATION-COPY)) or if the operating system has
been upgraded to provide new locale definitions (in which case see
also [`pg_import_system_collations()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-COLLATION)).

<a id="COLLATION-MANAGING-CREATE-ICU"></a>

##### 23.2.2.3.2. ICU Collations [#](#COLLATION-MANAGING-CREATE-ICU)

ICU collations can be created like:

```

CREATE COLLATION german (provider = icu, locale = 'de-DE');
```

ICU locales are specified as a BCP 47 [Language Tag](locale.md#ICU-LANGUAGE-TAG), but can also accept most
libc-style locale names. If possible, libc-style locale names are
transformed into language tags.

New ICU collations can customize collation behavior extensively by
including collation attributes in the language tag. See [Section 23.2.3](collation.md#ICU-CUSTOM-COLLATIONS) for details and examples.

<a id="COLLATION-COPY"></a>

##### 23.2.2.3.3. Copying Collations [#](#COLLATION-COPY)

The command [CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md) can also be used to
create a new collation from an existing collation, which can be useful to
be able to use operating-system-independent collation names in
applications, create compatibility names, or use an ICU-provided collation
under a more readable name. For example:

```

CREATE COLLATION german FROM "de_DE";
CREATE COLLATION french FROM "fr-x-icu";
```

<a id="COLLATION-NONDETERMINISTIC"></a>

#### 23.2.2.4. Nondeterministic Collations [#](#COLLATION-NONDETERMINISTIC)

A collation is either *deterministic* or
*nondeterministic*. A deterministic collation uses
deterministic comparisons, which means that it considers strings to be
equal only if they consist of the same byte sequence. Nondeterministic
comparison may determine strings to be equal even if they consist of
different bytes. Typical situations include case-insensitive comparison,
accent-insensitive comparison, as well as comparison of strings in
different Unicode normal forms. It is up to the collation provider to
actually implement such insensitive comparisons; the deterministic flag
only determines whether ties are to be broken using bytewise comparison.
See also [Unicode Technical
Standard 10](https://www.unicode.org/reports/tr10) for more information on the terminology.

To create a nondeterministic collation, specify the property
`deterministic = false` to `CREATE
COLLATION`, for example:

```

CREATE COLLATION ndcoll (provider = icu, locale = 'und', deterministic = false);
```

This example would use the standard Unicode collation in a
nondeterministic way. In particular, this would allow strings in
different normal forms to be compared correctly. More interesting
examples make use of the ICU customization facilities explained above.
For example:

```

CREATE COLLATION case_insensitive (provider = icu, locale = 'und-u-ks-level2', deterministic = false);
CREATE COLLATION ignore_accents (provider = icu, locale = 'und-u-ks-level1-kc-true', deterministic = false);
```

All standard and predefined collations are deterministic, all
user-defined collations are deterministic by default. While
nondeterministic collations give a more “correct” behavior,
especially when considering the full power of Unicode and its many
special cases, they also have some drawbacks. Foremost, their use leads
to a performance penalty. Note, in particular, that B-tree cannot use
deduplication with indexes that use a nondeterministic collation. Also,
certain operations are not possible with nondeterministic collations,
such as some pattern matching operations. Therefore, they should be used
only in cases where they are specifically wanted.

### Tip

To deal with text in different Unicode normalization forms, it is also
an option to use the functions/expressions
`normalize` and `is normalized` to
preprocess or check the strings, instead of using nondeterministic
collations. There are different trade-offs for each approach.

<a id="ICU-CUSTOM-COLLATIONS"></a>

### 23.2.3. ICU Custom Collations [#](#ICU-CUSTOM-COLLATIONS)

ICU allows extensive control over collation behavior by defining new
collations with collation settings as a part of the language tag. These
settings can modify the collation order to suit a variety of needs. For
instance:

```

-- ignore differences in accents and case
CREATE COLLATION ignore_accent_case (provider = icu, deterministic = false, locale = 'und-u-ks-level1');
SELECT 'Å' = 'A' COLLATE ignore_accent_case; -- true
SELECT 'z' = 'Z' COLLATE ignore_accent_case; -- true

-- upper case letters sort before lower case.
CREATE COLLATION upper_first (provider = icu, locale = 'und-u-kf-upper');
SELECT 'B' < 'b' COLLATE upper_first; -- true

-- treat digits numerically and ignore punctuation
CREATE COLLATION num_ignore_punct (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-kn');
SELECT 'id-45' < 'id-123' COLLATE num_ignore_punct; -- true
SELECT 'w;x*y-z' = 'wxyz' COLLATE num_ignore_punct; -- true
```

Many of the available options are described in [Section 23.2.3.2](collation.md#ICU-COLLATION-SETTINGS), or see [Section 23.2.3.5](collation.md#ICU-EXTERNAL-REFERENCES) for more details.

<a id="ICU-COLLATION-COMPARISON-LEVELS"></a>

#### 23.2.3.1. ICU Comparison Levels [#](#ICU-COLLATION-COMPARISON-LEVELS)

Comparison of two strings (collation) in ICU is determined by a
multi-level process, where textual features are grouped into
"levels". Treatment of each level is controlled by the [collation settings](collation.md#ICU-COLLATION-SETTINGS-TABLE). Higher
levels correspond to finer textual features.

[Table 23.1](collation.md#ICU-COLLATION-LEVELS) shows which textual feature
differences are considered significant when determining equality at the
given level. The Unicode character `U+2063` is an
invisible separator, and as seen in the table, is ignored for at all
levels of comparison less than `identic`.

<a id="ICU-COLLATION-LEVELS"></a>

**Table 23.1. ICU Collation Levels**

<table border="1" class="table" summary="ICU Collation Levels"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/><col class="col7"/><col class="col8"/></colgroup><thead><tr><th>Level</th><th>Description</th><th><code class="literal">'f' = 'f'</code></th><th><code class="literal">'ab' = U&amp;'a\2063b'</code></th><th><code class="literal">'x-y' = 'x_y'</code></th><th><code class="literal">'g' = 'G'</code></th><th><code class="literal">'n' = 'ñ'</code></th><th><code class="literal">'y' = 'z'</code></th></tr></thead><tbody><tr><td>level1</td><td>Base Character</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td></tr><tr><td>level2</td><td>Accents</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>level3</td><td>Case/Variants</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>level4</td><td>Punctuation<a class="footnote" href="#ftn.id-1.6.10.4.6.3.4.2.10.4.2.1"><sup class="footnote" id="id-1.6.10.4.6.3.4.2.10.4.2.1">[a]</sup></a></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>identic</td><td>All</td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="8"><div class="footnote" id="ftn.id-1.6.10.4.6.3.4.2.10.4.2.1"><p><a class="para" href="#id-1.6.10.4.6.3.4.2.10.4.2.1"><sup class="para">[a] </sup></a>only with
         <code class="literal">ka-shifted</code>; see <a class="xref" href="collation.md#ICU-COLLATION-SETTINGS-TABLE">Table 23.2</a></p></div></td></tr></tbody></table>

<br>

At every level, even with full normalization off, basic normalization is
performed. For example, `'á'` may be composed of the
code points `U&'\0061\0301'` or the single code
point `U&'\00E1'`, and those sequences will be
considered equal even at the `identic` level. To treat
any difference in code point representation as distinct, use a collation
created with `deterministic` set to
`true`.

<a id="ICU-COLLATION-LEVEL-EXAMPLES"></a>

##### 23.2.3.1.1. Collation Level Examples [#](#ICU-COLLATION-LEVEL-EXAMPLES)

```

CREATE COLLATION level3 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level3');
CREATE COLLATION level4 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level4');
CREATE COLLATION identic (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-identic');

-- invisible separator ignored at all levels except identic
SELECT 'ab' = U&'a\2063b' COLLATE level4; -- true
SELECT 'ab' = U&'a\2063b' COLLATE identic; -- false

-- punctuation ignored at level3 but not at level 4
SELECT 'x-y' = 'x_y' COLLATE level3; -- true
SELECT 'x-y' = 'x_y' COLLATE level4; -- false
```

<a id="ICU-COLLATION-SETTINGS"></a>

#### 23.2.3.2. Collation Settings for an ICU Locale [#](#ICU-COLLATION-SETTINGS)

[Table 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE) shows the available
collation settings, which can be used as part of a language tag to
customize a collation.

<a id="ICU-COLLATION-SETTINGS-TABLE"></a>

**Table 23.2. ICU Collation Settings**

<table border="1" class="table" summary="ICU Collation Settings"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>Key</th><th>Values</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">co</code></td><td><code class="literal">emoji</code>, <code class="literal">phonebk</code>, <code class="literal">standard</code>, <em class="replaceable"><code>...</code></em></td><td><code class="literal">standard</code></td><td>
          Collation type. See <a class="xref" href="collation.md#ICU-EXTERNAL-REFERENCES">Section 23.2.3.5</a> for additional options and details.
         </td></tr><tr><td><code class="literal">ka</code></td><td><code class="literal">noignore</code>, <code class="literal">shifted</code></td><td><code class="literal">noignore</code></td><td>
          If set to <code class="literal">shifted</code>, causes some characters
          (e.g. punctuation or space) to be ignored in comparison. Key
          <code class="literal">ks</code> must be set to <code class="literal">level3</code> or
          lower to take effect. Set key <code class="literal">kv</code> to control which
          character classes are ignored.
         </td></tr><tr><td><code class="literal">kb</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
          Backwards comparison for the level 2 differences. For example,
          locale <code class="literal">und-u-kb</code> sorts <code class="literal">'àe'</code>
          before <code class="literal">'aé'</code>.
         </td></tr><tr><td><code class="literal">kc</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
<p>
           Separates case into a "level 2.5" that falls between accents and
           other level 3 features.
          </p>
<p>
           If set to <code class="literal">true</code> and <code class="literal">ks</code> is set
           to <code class="literal">level1</code>, will ignore accents but take case
           into account.
          </p>
</td></tr><tr><td><code class="literal">kf</code></td><td>
<code class="literal">upper</code>, <code class="literal">lower</code>,
          <code class="literal">false</code>
</td><td><code class="literal">false</code></td><td>
          If set to <code class="literal">upper</code>, upper case sorts before lower
          case. If set to <code class="literal">lower</code>, lower case sorts before
          upper case. If set to <code class="literal">false</code>, the sort depends on
          the rules of the locale.
         </td></tr><tr><td><code class="literal">kn</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
          If set to <code class="literal">true</code>, numbers within a string are
          treated as a single numeric value rather than a sequence of
          digits. For example, <code class="literal">'id-45'</code> sorts before
          <code class="literal">'id-123'</code>.
         </td></tr><tr><td><code class="literal">kk</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
<p>
           Enable full normalization; may affect performance. Basic
           normalization is performed even when set to
           <code class="literal">false</code>. Locales for languages that require full
           normalization typically enable it by default.
          </p>
<p>
           Full normalization is important in some cases, such as when
           multiple accents are applied to a single character. For example,
           the code point sequences <code class="literal">U&amp;'\0065\0323\0302'</code>
           and <code class="literal">U&amp;'\0065\0302\0323'</code> represent
           an <code class="literal">e</code> with circumflex and dot-below accents
           applied in different orders. With full normalization
           on, these code point sequences are treated as equal; otherwise they
           are unequal.
          </p>
</td></tr><tr><td><code class="literal">kr</code></td><td>
<code class="literal">space</code>, <code class="literal">punct</code>,
          <code class="literal">symbol</code>, <code class="literal">currency</code>,
          <code class="literal">digit</code>, <em class="replaceable"><code>script-id</code></em>
</td><td> </td><td>
<p>
           Set to one or more of the valid values, or any BCP 47
           <em class="replaceable"><code>script-id</code></em>, e.g. <code class="literal">latn</code>
           ("Latin") or <code class="literal">grek</code> ("Greek"). Multiple values are
           separated by "<code class="literal">-</code>".
          </p>
<p>
           Redefines the ordering of classes of characters; those characters
           belonging to a class earlier in the list sort before characters
           belonging to a class later in the list. For instance, the value
           <code class="literal">digit-currency-space</code> (as part of a language tag
           like <code class="literal">und-u-kr-digit-currency-space</code>) sorts
           punctuation before digits and spaces.
          </p>
</td></tr><tr><td><code class="literal">ks</code></td><td><code class="literal">level1</code>, <code class="literal">level2</code>, <code class="literal">level3</code>, <code class="literal">level4</code>, <code class="literal">identic</code></td><td><code class="literal">level3</code></td><td>
          Sensitivity (or "strength") when determining equality, with
          <code class="literal">level1</code> the least sensitive to differences and
          <code class="literal">identic</code> the most sensitive to differences. See
          <a class="xref" href="collation.md#ICU-COLLATION-LEVELS">Table 23.1</a> for details.
         </td></tr><tr><td><code class="literal">kv</code></td><td>
<code class="literal">space</code>, <code class="literal">punct</code>,
          <code class="literal">symbol</code>, <code class="literal">currency</code>
</td><td><code class="literal">punct</code></td><td>
          Classes of characters ignored during comparison at level 3. Setting
          to a later value includes earlier values;
          e.g. <code class="literal">symbol</code> also includes
          <code class="literal">punct</code> and <code class="literal">space</code> in the
          characters to be ignored. Key <code class="literal">ka</code> must be set to
          <code class="literal">shifted</code> and key <code class="literal">ks</code> must be set
          to <code class="literal">level3</code> or lower to take effect.
         </td></tr></tbody></table>

<br>

Defaults may depend on locale. The above table is not meant to be
complete. See [Section 23.2.3.5](collation.md#ICU-EXTERNAL-REFERENCES) for additional
options and details.

### Note

For many collation settings, you must create the collation with
`deterministic` set to `false` for the
setting to have the desired effect (see [Section 23.2.2.4](collation.md#COLLATION-NONDETERMINISTIC)). Additionally, some settings
only take effect when the key `ka` is set to
`shifted` (see [Table 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE)).

<a id="ICU-LOCALE-EXAMPLES"></a>

#### 23.2.3.3. Collation Settings Examples [#](#ICU-LOCALE-EXAMPLES)

<a id="COLLATION-MANAGING-CREATE-ICU-DE-U-CO-PHONEBK-X-ICU"></a>

`CREATE COLLATION "de-u-co-phonebk-x-icu" (provider = icu, locale = 'de-u-co-phonebk');` [#](#COLLATION-MANAGING-CREATE-ICU-DE-U-CO-PHONEBK-X-ICU)
:   German collation with phone book collation type
<a id="COLLATION-MANAGING-CREATE-ICU-UND-U-CO-EMOJI-X-ICU"></a>

`CREATE COLLATION "und-u-co-emoji-x-icu" (provider = icu, locale = 'und-u-co-emoji');` [#](#COLLATION-MANAGING-CREATE-ICU-UND-U-CO-EMOJI-X-ICU)
:   Root collation with Emoji collation type, per Unicode Technical Standard #51
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KR-GREK-LATN"></a>

`CREATE COLLATION latinlast (provider = icu, locale = 'en-u-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KR-GREK-LATN)
:   Sort Greek letters before Latin ones. (The default is Latin before Greek.)
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER"></a>

`CREATE COLLATION upperfirst (provider = icu, locale = 'en-u-kf-upper');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER)
:   Sort upper-case letters before lower-case letters. (The default is
    lower-case letters first.)
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER-KR-GREK-LATN"></a>

`CREATE COLLATION special (provider = icu, locale = 'en-u-kf-upper-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER-KR-GREK-LATN)
:   Combines both of the above options.

<a id="ICU-TAILORING-RULES"></a>

#### 23.2.3.4. ICU Tailoring Rules [#](#ICU-TAILORING-RULES)

If the options provided by the collation settings shown above are not
sufficient, the order of collation elements can be changed with tailoring
rules, whose syntax is detailed at <https://unicode-org.github.io/icu/userguide/collation/customization/>.

This small example creates a collation based on the root locale with a
tailoring rule:

```

CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

With this rule, the letter “W” is sorted after
“V”, but is treated as a secondary difference similar to an
accent. Rules like this are contained in the locale definitions of some
languages. (Of course, if a locale definition already contains the
desired rules, then they don't need to be specified again explicitly.)

Here is a more complex example. The following statement sets up a
collation named `ebcdic` with rules to sort US-ASCII
characters in the order of the EBCDIC encoding.

```

CREATE COLLATION ebcdic (provider = icu, locale = 'und',
rules = $$
& ' ' < '.' < '<' < '(' < '+' < \|
< '&' < '!' < '$' < '*' < ')' < ';'
< '-' < '/' < ',' < '%' < '_' < '>' < '?'
< '`' < ':' < '#' < '@' < \' < '=' < '"'
<*a-r < '~' <*s-z < '^' < '[' < ']'
< '{' <*A-I < '}' <*J-R < '\' <*S-Z <*0-9
$$);

SELECT c
FROM (VALUES ('a'), ('b'), ('A'), ('B'), ('1'), ('2'), ('!'), ('^')) AS x(c)
ORDER BY c COLLATE ebcdic;
 c
---
 !
 a
 b
 ^
 A
 B
 1
 2
```

<a id="ICU-EXTERNAL-REFERENCES"></a>

#### 23.2.3.5. External References for ICU [#](#ICU-EXTERNAL-REFERENCES)

This section ([Section 23.2.3](collation.md#ICU-CUSTOM-COLLATIONS)) is only a brief
overview of ICU behavior and language tags. Refer to the following
documents for technical details, additional options, and new behavior:

* [Unicode Technical Standard #35](https://www.unicode.org/reports/tr35/tr35-collation.html)
* [BCP 47](https://www.rfc-editor.org/info/bcp47)
* [CLDR repository](https://github.com/unicode-org/cldr/blob/master/common/bcp47/collation.xml)
* <https://unicode-org.github.io/icu/userguide/locale/>
* <https://unicode-org.github.io/icu/userguide/collation/>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/collation.html)（英文原文，待翻譯）
