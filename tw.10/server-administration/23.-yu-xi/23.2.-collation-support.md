# 23.2. Collation Support

The collation feature allows specifying the sort order and character classification behavior of data per-column, or even per-operation. This alleviates the restriction that the `LC_COLLATE` and `LC_CTYPE` settings of a database cannot be changed after its creation.

#### 23.2.1. Concepts

Conceptually, every expression of a collatable data type has a collation. \(The built-in collatable data types are `text`, `varchar`, and `char`. User-defined base types can also be marked collatable, and of course a domain over a collatable data type is collatable.\) If the expression is a column reference, the collation of the expression is the defined collation of the column. If the expression is a constant, the collation is the default collation of the data type of the constant. The collation of a more complex expression is derived from the collations of its inputs, as described below.

The collation of an expression can be the “default” collation, which means the locale settings defined for the database. It is also possible for an expression's collation to be indeterminate. In such cases, ordering operations and other operations that need to know the collation will fail.

When the database system has to perform an ordering or a character classification, it uses the collation of the input expression. This happens, for example, with `ORDER BY` clauses and function or operator calls such as `<`. The collation to apply for an `ORDER BY` clause is simply the collation of the sort key. The collation to apply for a function or operator call is derived from the arguments, as described below. In addition to comparison operators, collations are taken into account by functions that convert between lower and upper case letters, such as `lower`, `upper`, and `initcap`; by pattern matching operators; and by `to_char` and related functions.

For a function or operator call, the collation that is derived by examining the argument collations is used at run time for performing the specified operation. If the result of the function or operator call is of a collatable data type, the collation is also used at parse time as the defined collation of the function or operator expression, in case there is a surrounding expression that requires knowledge of its collation.

The _collation derivation_ of an expression can be implicit or explicit. This distinction affects how collations are combined when multiple different collations appear in an expression. An explicit collation derivation occurs when a `COLLATE` clause is used; all other collation derivations are implicit. When multiple collations need to be combined, for example in a function call, the following rules are used:

1. If any input expression has an explicit collation derivation, then all explicitly derived collations among the input expressions must be the same, otherwise an error is raised. If any explicitly derived collation is present, that is the result of the collation combination.
2. Otherwise, all input expressions must have the same implicit collation derivation or the default collation. If any non-default collation is present, that is the result of the collation combination. Otherwise, the result is the default collation.
3. If there are conflicting non-default implicit collations among the input expressions, then the combination is deemed to have indeterminate collation. This is not an error condition unless the particular function being invoked requires knowledge of the collation it should apply. If it does, an error will be raised at run-time.

For example, consider this table definition:

```text
CREATE TABLE test1 (
    a text COLLATE "de_DE",
    b text COLLATE "es_ES",
    ...
);
```

Then in

```text
SELECT a < 'foo' FROM test1;
```

the `<` comparison is performed according to `de_DE` rules, because the expression combines an implicitly derived collation with the default collation. But in

```text
SELECT a < ('foo' COLLATE "fr_FR") FROM test1;
```

the comparison is performed using `fr_FR` rules, because the explicit collation derivation overrides the implicit one. Furthermore, given

```text
SELECT a < b FROM test1;
```

the parser cannot determine which collation to apply, since the `a` and `b` columns have conflicting implicit collations. Since the `<` operator does need to know which collation to use, this will result in an error. The error can be resolved by attaching an explicit collation specifier to either input expression, thus:

```text
SELECT a < b COLLATE "de_DE" FROM test1;
```

or equivalently

```text
SELECT a COLLATE "de_DE" < b FROM test1;
```

On the other hand, the structurally similar case

```text
SELECT a || b FROM test1;
```

does not result in an error, because the `||` operator does not care about collations: its result is the same regardless of the collation.

The collation assigned to a function or operator's combined input expressions is also considered to apply to the function or operator's result, if the function or operator delivers a result of a collatable data type. So, in

```text
SELECT * FROM test1 ORDER BY a || 'foo';
```

the ordering will be done according to `de_DE` rules. But this query:

```text
SELECT * FROM test1 ORDER BY a || b;
```

results in an error, because even though the `||` operator doesn't need to know a collation, the `ORDER BY` clause does. As before, the conflict can be resolved with an explicit collation specifier:

```text
SELECT * FROM test1 ORDER BY a || b COLLATE "fr_FR";
```

#### 23.2.2. Managing Collations

A collation is an SQL schema object that maps an SQL name to locales provided by libraries installed in the operating system. A collation definition has a _provider_ that specifies which library supplies the locale data. One standard provider name is `libc`, which uses the locales provided by the operating system C library. These are the locales that most tools provided by the operating system use. Another provider is `icu`, which uses the external ICU library. ICU locales can only be used if support for ICU was configured when PostgreSQL was built.

A collation object provided by `libc` maps to a combination of `LC_COLLATE` and `LC_CTYPE` settings, as accepted by the `setlocale()` system library call. \(As the name would suggest, the main purpose of a collation is to set `LC_COLLATE`, which controls the sort order. But it is rarely necessary in practice to have an `LC_CTYPE` setting that is different from `LC_COLLATE`, so it is more convenient to collect these under one concept than to create another infrastructure for setting `LC_CTYPE` per expression.\) Also, a `libc` collation is tied to a character set encoding \(see [Section 23.3](https://www.postgresql.org/docs/10/static/multibyte.html)\). The same collation name may exist for different encodings.

A collation object provided by `icu` maps to a named collator provided by the ICU library. ICU does not support separate “collate” and “ctype” settings, so they are always the same. Also, ICU collations are independent of the encoding, so there is always only one ICU collation of a given name in a database.

**23.2.2.1. Standard Collations**

On all platforms, the collations named `default`, `C`, and `POSIX` are available. Additional collations may be available depending on operating system support. The `default` collation selects the `LC_COLLATE` and `LC_CTYPE` values specified at database creation time. The `C` and `POSIX` collations both specify “traditional C” behavior, in which only the ASCII letters “`A`” through “`Z`” are treated as letters, and sorting is done strictly by character code byte values.

Additionally, the SQL standard collation name `ucs_basic` is available for encoding `UTF8`. It is equivalent to `C` and sorts by Unicode code point.

**23.2.2.2. Predefined Collations**

If the operating system provides support for using multiple locales within a single program \(`newlocale` and related functions\), or if support for ICU is configured, then when a database cluster is initialized, `initdb` populates the system catalog `pg_collation` with collations based on all the locales it finds in the operating system at the time.

To inspect the currently available locales, use the query `SELECT * FROM pg_collation`, or the command `\dOS+` in psql.

**23.2.2.2.1. libc collations**

For example, the operating system might provide a locale named `de_DE.utf8`. `initdb` would then create a collation named `de_DE.utf8` for encoding `UTF8` that has both `LC_COLLATE` and `LC_CTYPE` set to `de_DE.utf8`. It will also create a collation with the `.utf8` tag stripped off the name. So you could also use the collation under the name `de_DE`, which is less cumbersome to write and makes the name less encoding-dependent. Note that, nevertheless, the initial set of collation names is platform-dependent.

The default set of collations provided by `libc` map directly to the locales installed in the operating system, which can be listed using the command `locale -a`. In case a `libc` collation is needed that has different values for `LC_COLLATE` and `LC_CTYPE`, or if new locales are installed in the operating system after the database system was initialized, then a new collation may be created using the [CREATE COLLATION](https://www.postgresql.org/docs/10/static/sql-createcollation.html) command. New operating system locales can also be imported en masse using the [`pg_import_system_collations()`](https://www.postgresql.org/docs/10/static/functions-admin.html#FUNCTIONS-ADMIN-COLLATION) function.

Within any particular database, only collations that use that database's encoding are of interest. Other entries in `pg_collation` are ignored. Thus, a stripped collation name such as `de_DE` can be considered unique within a given database even though it would not be unique globally. Use of the stripped collation names is recommended, since it will make one less thing you need to change if you decide to change to another database encoding. Note however that the `default`, `C`, and `POSIX` collations can be used regardless of the database encoding.

PostgreSQL considers distinct collation objects to be incompatible even when they have identical properties. Thus for example,

```text
SELECT a COLLATE "C" < b COLLATE "POSIX" FROM test1;
```

will draw an error even though the `C` and `POSIX` collations have identical behaviors. Mixing stripped and non-stripped collation names is therefore not recommended.

**23.2.2.2.2. ICU collations**

With ICU, it is not sensible to enumerate all possible locale names. ICU uses a particular naming system for locales, but there are many more ways to name a locale than there are actually distinct locales. `initdb` uses the ICU APIs to extract a set of distinct locales to populate the initial set of collations. Collations provided by ICU are created in the SQL environment with names in BCP 47 language tag format, with a “private use” extension `-x-icu` appended, to distinguish them from libc locales.

Here are some example collations that might be created:`de-x-icu`

German collation, default variant`de-AT-x-icu`

German collation for Austria, default variant

\(There are also, say, `de-DE-x-icu` or `de-CH-x-icu`, but as of this writing, they are equivalent to `de-x-icu`.\)`und-x-icu` \(for “undefined”\)

ICU “root” collation. Use this to get a reasonable language-agnostic sort order.

Some \(less frequently used\) encodings are not supported by ICU. When the database encoding is one of these, ICU collation entries in `pg_collation` are ignored. Attempting to use one will draw an error along the lines of “collation "de-x-icu" for encoding "WIN874" does not exist”.

**23.2.2.3. Creating New Collation Objects**

If the standard and predefined collations are not sufficient, users can create their own collation objects using the SQL command [CREATE COLLATION](https://www.postgresql.org/docs/10/static/sql-createcollation.html).

The standard and predefined collations are in the schema `pg_catalog`, like all predefined objects. User-defined collations should be created in user schemas. This also ensures that they are saved by `pg_dump`.

**23.2.2.3.1. libc collations**

New libc collations can be created like this:

```text
CREATE COLLATION german (provider = libc, locale = 'de_DE');
```

The exact values that are acceptable for the `locale` clause in this command depend on the operating system. On Unix-like systems, the command `locale -a` will show a list.

Since the predefined libc collations already include all collations defined in the operating system when the database instance is initialized, it is not often necessary to manually create new ones. Reasons might be if a different naming system is desired \(in which case see also [Section 23.2.2.3.3](https://www.postgresql.org/docs/10/static/collation.html#COLLATION-COPY)\) or if the operating system has been upgraded to provide new locale definitions \(in which case see also [`pg_import_system_collations()`](https://www.postgresql.org/docs/10/static/functions-admin.html#FUNCTIONS-ADMIN-COLLATION)\).

**23.2.2.3.2. ICU collations**

ICU allows collations to be customized beyond the basic language+country set that is preloaded by `initdb`. Users are encouraged to define their own collation objects that make use of these facilities to suit the sorting behavior to their requirements. See [http://userguide.icu-project.org/locale](http://userguide.icu-project.org/locale) and [http://userguide.icu-project.org/collation/api](http://userguide.icu-project.org/collation/api) for information on ICU locale naming. The set of acceptable names and attributes depends on the particular ICU version.

Here are some examples:`CREATE COLLATION "de-u-co-phonebk-x-icu" (provider = icu, locale = 'de-u-co-phonebk');`  
`CREATE COLLATION "de-u-co-phonebk-x-icu" (provider = icu, locale = 'de@collation=phonebook');`

German collation with phone book collation type

The first example selects the ICU locale using a “language tag” per BCP 47. The second example uses the traditional ICU-specific locale syntax. The first style is preferred going forward, but it is not supported by older ICU versions.

Note that you can name the collation objects in the SQL environment anything you want. In this example, we follow the naming style that the predefined collations use, which in turn also follow BCP 47, but that is not required for user-defined collations.`CREATE COLLATION "und-u-co-emoji-x-icu" (provider = icu, locale = 'und-u-co-emoji');`  
`CREATE COLLATION "und-u-co-emoji-x-icu" (provider = icu, locale = '@collation=emoji');`

Root collation with Emoji collation type, per Unicode Technical Standard \#51

Observe how in the traditional ICU locale naming system, the root locale is selected by an empty string.`CREATE COLLATION digitslast (provider = icu, locale = 'en-u-kr-latn-digit');`  
`CREATE COLLATION digitslast (provider = icu, locale = 'en@colReorder=latn-digit');`

Sort digits after Latin letters. \(The default is digits before letters.\)`CREATE COLLATION upperfirst (provider = icu, locale = 'en-u-kf-upper');`  
`CREATE COLLATION upperfirst (provider = icu, locale = 'en@colCaseFirst=upper');`

Sort upper-case letters before lower-case letters. \(The default is lower-case letters first.\)`CREATE COLLATION special (provider = icu, locale = 'en-u-kf-upper-kr-latn-digit');`  
`CREATE COLLATION special (provider = icu, locale = 'en@colCaseFirst=upper;colReorder=latn-digit');`

Combines both of the above options.`CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');`  
`CREATE COLLATION numeric (provider = icu, locale = 'en@colNumeric=yes');`

Numeric ordering, sorts sequences of digits by their numeric value, for example: `A-21` &lt; `A-123` \(also known as natural sort\).

See [Unicode Technical Standard \#35](http://unicode.org/reports/tr35/tr35-collation.html) and [BCP 47](https://tools.ietf.org/html/bcp47) for details. The list of possible collation types \(`co` subtag\) can be found in the [CLDR repository](http://www.unicode.org/repos/cldr/trunk/common/bcp47/collation.xml). The [ICU Locale Explorer](https://ssl.icu-project.org/icu-bin/locexp) can be used to check the details of a particular locale definition. The examples using the `k*` subtags require at least ICU version 54.

Note that while this system allows creating collations that “ignore case” or “ignore accents” or similar \(using the `ks` key\), PostgreSQL does not at the moment allow such collations to act in a truly case- or accent-insensitive manner. Any strings that compare equal according to the collation but are not byte-wise equal will be sorted according to their byte values.

#### Note

By design, ICU will accept almost any string as a locale name and match it to the closest locale it can provide, using the fallback procedure described in its documentation. Thus, there will be no direct feedback if a collation specification is composed using features that the given ICU installation does not actually support. It is therefore recommended to create application-level test cases to check that the collation definitions satisfy one's requirements.

**23.2.2.3.3. Copying Collations**

The command [CREATE COLLATION](https://www.postgresql.org/docs/10/static/sql-createcollation.html) can also be used to create a new collation from an existing collation, which can be useful to be able to use operating-system-independent collation names in applications, create compatibility names, or use an ICU-provided collation under a more readable name. For example:

```text
CREATE COLLATION german FROM "de_DE";
CREATE COLLATION french FROM "fr-x-icu";
```

