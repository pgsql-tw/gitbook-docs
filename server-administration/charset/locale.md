## 23.1. Locale Support [#](#LOCALE)

[23.1.1. Overview](locale.md#LOCALE-OVERVIEW)

[23.1.2. Behavior](locale.md#LOCALE-BEHAVIOR)

[23.1.3. Selecting Locales](locale.md#LOCALE-SELECTING-LOCALES)

[23.1.4. Locale Providers](locale.md#LOCALE-PROVIDERS)

[23.1.5. ICU Locales](locale.md#ICU-LOCALES)

[23.1.6. Problems](locale.md#LOCALE-PROBLEMS)

<a id="id-1.6.10.3.2"></a>

*Locale* support refers to an application respecting
cultural preferences regarding alphabets, sorting, number
formatting, etc. PostgreSQL uses the standard ISO
C and POSIX locale facilities provided by the server operating
system. For additional information refer to the documentation of your
system.

<a id="LOCALE-OVERVIEW"></a>

### 23.1.1. Overview [#](#LOCALE-OVERVIEW)

Locale support is automatically initialized when a database
cluster is created using `initdb`.
`initdb` will initialize the database cluster
with the locale setting of its execution environment by default,
so if your system is already set to use the locale that you want
in your database cluster then there is nothing else you need to
do. If you want to use a different locale (or you are not sure
which locale your system is set to), you can instruct
`initdb` exactly which locale to use by
specifying the `--locale` option. For example:

```

initdb --locale=sv_SE
```

This example for Unix systems sets the locale to Swedish
(`sv`) as spoken
in Sweden (`SE`). Other possibilities might include
`en_US` (U.S. English) and `fr_CA` (French
Canadian). If more than one character set can be used for a
locale then the specifications can take the form
*`language_territory.codeset`*. For example,
`fr_BE.UTF-8` represents the French language (fr) as
spoken in Belgium (BE), with a UTF-8 character set
encoding.

What locales are available on your
system under what names depends on what was provided by the operating
system vendor and what was installed. On most Unix systems, the command
`locale -a` will provide a list of available locales.
Windows uses more verbose locale names, such as `German_Germany`
or `Swedish_Sweden.1252`, but the principles are the same.

Occasionally it is useful to mix rules from several locales, e.g.,
use English collation rules but Spanish messages. To support that, a
set of locale subcategories exist that control only certain
aspects of the localization rules:

<table border="1" class="informaltable"><colgroup><col class="col1"/><col class="col2"/></colgroup><tbody><tr><td><code class="envar">LC_COLLATE</code></td><td>String sort order</td></tr><tr><td><code class="envar">LC_CTYPE</code></td><td>Character classification (What is a letter? Its upper-case equivalent?)</td></tr><tr><td><code class="envar">LC_MESSAGES</code></td><td>Language of messages</td></tr><tr><td><code class="envar">LC_MONETARY</code></td><td>Formatting of currency amounts</td></tr><tr><td><code class="envar">LC_NUMERIC</code></td><td>Formatting of numbers</td></tr><tr><td><code class="envar">LC_TIME</code></td><td>Formatting of dates and times</td></tr></tbody></table>

The category names translate into names of
`initdb` options to override the locale choice
for a specific category. For instance, to set the locale to
French Canadian, but use U.S. rules for formatting currency, use
`initdb --locale=fr_CA --lc-monetary=en_US`.

If you want the system to behave as if it had no locale support,
use the special locale name `C`, or equivalently
`POSIX`.

Some locale categories must have their values
fixed when the database is created. You can use different settings
for different databases, but once a database is created, you cannot
change them for that database anymore. `LC_COLLATE`
and `LC_CTYPE` are these categories. They affect
the sort order of indexes, so they must be kept fixed, or indexes on
text columns would become corrupt.
(But you can alleviate this restriction using collations, as discussed
in [Section 23.2](collation.md).)
The default values for these
categories are determined when `initdb` is run, and
those values are used when new databases are created, unless
specified otherwise in the `CREATE DATABASE` command.

The other locale categories can be changed whenever desired
by setting the server configuration parameters
that have the same name as the locale categories (see [Section 19.11.2](../runtime-config/runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT) for details). The values
that are chosen by `initdb` are actually only written
into the configuration file `postgresql.conf` to
serve as defaults when the server is started. If you remove these
assignments from `postgresql.conf` then the
server will inherit the settings from its execution environment.

Note that the locale behavior of the server is determined by the
environment variables seen by the server, not by the environment
of any client. Therefore, be careful to configure the correct locale settings
before starting the server. A consequence of this is that if
client and server are set up in different locales, messages might
appear in different languages depending on where they originated.

### Note

When we speak of inheriting the locale from the execution
environment, this means the following on most operating systems:
For a given locale category, say the collation, the following
environment variables are consulted in this order until one is
found to be set: `LC_ALL`, `LC_COLLATE`
(or the variable corresponding to the respective category),
`LANG`. If none of these environment variables are
set then the locale defaults to `C`.

Some message localization libraries also look at the environment
variable `LANGUAGE` which overrides all other locale
settings for the purpose of setting the language of messages. If
in doubt, please refer to the documentation of your operating
system, in particular the documentation about
gettext.

To enable messages to be translated to the user's preferred language,
NLS must have been selected at build time
(`configure --enable-nls`). All other locale support is
built in automatically.

<a id="LOCALE-BEHAVIOR"></a>

### 23.1.2. Behavior [#](#LOCALE-BEHAVIOR)

The locale settings influence the following SQL features:

* Sort order in queries using `ORDER BY` or the standard
  comparison operators on textual data
  <a id="id-1.6.10.3.5.2.1.1.1.2"></a>
* The `upper`, `lower`, and `initcap`
  functions
  <a id="id-1.6.10.3.5.2.1.2.1.4"></a>
  <a id="id-1.6.10.3.5.2.1.2.1.5"></a>
* Pattern matching operators (`LIKE`, `SIMILAR TO`,
  and POSIX-style regular expressions); locales affect both case
  insensitive matching and the classification of characters by
  character-class regular expressions
  <a id="id-1.6.10.3.5.2.1.3.1.3"></a>
  <a id="id-1.6.10.3.5.2.1.3.1.4"></a>
* The `to_char` family of functions
  <a id="id-1.6.10.3.5.2.1.4.1.2"></a>
* The ability to use indexes with `LIKE` clauses

The drawback of using locales other than `C` or
`POSIX` in PostgreSQL is its performance
impact. It slows character handling and prevents ordinary indexes
from being used by `LIKE`. For this reason use locales
only if you actually need them.

As a workaround to allow PostgreSQL to use indexes
with `LIKE` clauses under a non-C locale, several custom
operator classes exist. These allow the creation of an index that
performs a strict character-by-character comparison, ignoring
locale comparison rules. Refer to [Section 11.10](../../the-sql-language/indexes/indexes-opclass.md)
for more information. Another approach is to create indexes using
the `C` collation, as discussed in
[Section 23.2](collation.md).

<a id="LOCALE-SELECTING-LOCALES"></a>

### 23.1.3. Selecting Locales [#](#LOCALE-SELECTING-LOCALES)

Locales can be selected in different scopes depending on requirements.
The above overview showed how locales are specified using
`initdb` to set the defaults for the entire cluster. The
following list shows where locales can be selected. Each item provides
the defaults for the subsequent items, and each lower item allows
overriding the defaults on a finer granularity.

1. As explained above, the environment of the operating system provides the
   defaults for the locales of a newly initialized database cluster. In
   many cases, this is enough: if the operating system is configured for
   the desired language/territory, by default
   PostgreSQL will also behave according
   to that locale.
2. As shown above, command-line options for `initdb`
   specify the locale settings for a newly initialized database cluster.
   Use this if the operating system does not have the locale configuration
   you want for your database system.
3. A locale can be selected separately for each database. The SQL command
   `CREATE DATABASE` and its command-line equivalent
   `createdb` have options for that. Use this for example
   if a database cluster houses databases for multiple tenants with
   different requirements.
4. Locale settings can be made for individual table columns. This uses an
   SQL object called *collation* and is explained in
   [Section 23.2](collation.md). Use this for example to sort data in
   different languages or customize the sort order of a particular table.
5. Finally, locales can be selected for an individual query. Again, this
   uses SQL collation objects. This could be used to change the sort order
   based on run-time choices or for ad-hoc experimentation.

<a id="LOCALE-PROVIDERS"></a>

### 23.1.4. Locale Providers [#](#LOCALE-PROVIDERS)

A locale provider specifies which library defines the locale behavior for
collations and character classifications.

The commands and tools that select the locale settings, as described
above, each have an option to select the locale provider. Here is an
example to initialize a database cluster using the ICU provider:

```

initdb --locale-provider=icu --icu-locale=en
```

See the description of the respective commands and programs for
details. Note that you can mix locale providers at different
granularities, for example use `libc` by default for the
cluster but have one database that uses the `icu`
provider, and then have collation objects using either provider within
those databases.

Regardless of the locale provider, the operating system is still used to
provide some locale-aware behavior, such as messages (see [lc_messages](../runtime-config/runtime-config-client.md#GUC-LC-MESSAGES)).

The available locale providers are listed below:

`builtin`
:   The `builtin` provider uses built-in operations. Only
    the `C`, `C.UTF-8`, and
    `PG_UNICODE_FAST` locales are supported for this
    provider.

    The `C` locale behavior is identical to the
    `C` locale in the libc provider. When using this
    locale, the behavior may depend on the database encoding.

    The `C.UTF-8` locale is available only for when the
    database encoding is `UTF-8`, and the behavior is
    based on Unicode. The collation uses the code point values only. The
    regular expression character classes are based on the "POSIX
    Compatible" semantics, and the case mapping is the "simple" variant.

    The `PG_UNICODE_FAST` locale is available only when
    the database encoding is `UTF-8`, and the behavior is
    based on Unicode. The collation uses the code point values only. The
    regular expression character classes are based on the "Standard"
    semantics, and the case mapping is the "full" variant.

`icu`
:   The `icu` provider uses the external
    ICU<a id="id-1.6.10.3.7.6.2.2.1.2"></a>
    library. PostgreSQL must have been
    configured with support.

    ICU provides collation and character classification behavior that is
    independent of the operating system and database encoding, which is
    preferable if you expect to transition to other platforms without any
    change in results. `LC_COLLATE` and
    `LC_CTYPE` can be set independently of the ICU
    locale.

    ### Note

    For the ICU provider, results may depend on the version of the ICU
    library used, as it is updated to reflect changes in natural language
    over time.

`libc`
:   The `libc` provider uses the operating system's C
    library. The collation and character classification behavior is
    controlled by the settings `LC_COLLATE` and
    `LC_CTYPE`, so they cannot be set independently.

    ### Note

    The same locale name may have different behavior on different
    platforms when using the libc provider.

<a id="ICU-LOCALES"></a>

### 23.1.5. ICU Locales [#](#ICU-LOCALES)

<a id="ICU-LOCALE-NAMES"></a>

#### 23.1.5.1. ICU Locale Names [#](#ICU-LOCALE-NAMES)

The ICU format for the locale name is a [Language Tag](locale.md#ICU-LANGUAGE-TAG).

```

CREATE COLLATION mycollation1 (provider = icu, locale = 'ja-JP');
CREATE COLLATION mycollation2 (provider = icu, locale = 'fr');
```

<a id="ICU-CANONICALIZATION"></a>

#### 23.1.5.2. Locale Canonicalization and Validation [#](#ICU-CANONICALIZATION)

When defining a new ICU collation object or database with ICU as the
provider, the given locale name is transformed ("canonicalized") into a
language tag if not already in that form. For instance,

```

CREATE COLLATION mycollation3 (provider = icu, locale = 'en-US-u-kn-true');
NOTICE:  using standard form "en-US-u-kn" for locale "en-US-u-kn-true"
CREATE COLLATION mycollation4 (provider = icu, locale = 'de_DE.utf8');
NOTICE:  using standard form "de-DE" for locale "de_DE.utf8"
```

If you see this notice, ensure that the `provider` and
`locale` are the expected result. For consistent results
when using the ICU provider, specify the canonical [language tag](locale.md#ICU-LANGUAGE-TAG) instead of relying on the
transformation.

A locale with no language name, or the special language name
`root`, is transformed to have the language
`und` ("undefined").

ICU can transform most libc locale names, as well as some other formats,
into language tags for easier transition to ICU. If a libc locale name is
used in ICU, it may not have precisely the same behavior as in libc.

If there is a problem interpreting the locale name, or if the locale name
represents a language or region that ICU does not recognize, you will see
the following warning:

```

CREATE COLLATION nonsense (provider = icu, locale = 'nonsense');
WARNING:  ICU locale "nonsense" has unknown language "nonsense"
HINT:  To disable ICU locale validation, set parameter icu_validation_level to DISABLED.
CREATE COLLATION
```

[icu_validation_level](../runtime-config/runtime-config-client.md#GUC-ICU-VALIDATION-LEVEL) controls how the message is
reported. Unless set to `ERROR`, the collation will
still be created, but the behavior may not be what the user intended.

<a id="ICU-LANGUAGE-TAG"></a>

#### 23.1.5.3. Language Tag [#](#ICU-LANGUAGE-TAG)

A language tag, defined in BCP 47, is a standardized identifier used to
identify languages, regions, and other information about a locale.

Basic language tags are simply
*`language`*`-`*`region`*;
or even just *`language`*. The
*`language`* is a language code
(e.g. `fr` for French), and
*`region`* is a region code
(e.g. `CA` for Canada). Examples:
`ja-JP`, `de`, or
`fr-CA`.

Collation settings may be included in the language tag to customize
collation behavior. ICU allows extensive customization, such as
sensitivity (or insensitivity) to accents, case, and punctuation;
treatment of digits within text; and many other options to satisfy a
variety of uses.

To include this additional collation information in a language tag,
append `-u`, which indicates there are additional
collation settings, followed by one or more
`-`*`key`*`-`*`value`*
pairs. The *`key`* is the key for a [collation setting](collation.md#ICU-COLLATION-SETTINGS) and
*`value`* is a valid value for that setting. For
boolean settings, the `-`*`key`*
may be specified without a corresponding
`-`*`value`*, which implies a
value of `true`.

For example, the language tag `en-US-u-kn-ks-level2`
means the locale with the English language in the US region, with
collation settings `kn` set to `true`
and `ks` set to `level2`. Those
settings mean the collation will be case-insensitive and treat a sequence
of digits as a single number:

```

CREATE COLLATION mycollation5 (provider = icu, deterministic = false, locale = 'en-US-u-kn-ks-level2');
SELECT 'aB' = 'Ab' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)

SELECT 'N-45' < 'N-123' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)
```

See [Section 23.2.3](collation.md#ICU-CUSTOM-COLLATIONS) for details and additional
examples of using language tags with custom collation information for the
locale.

<a id="LOCALE-PROBLEMS"></a>

### 23.1.6. Problems [#](#LOCALE-PROBLEMS)

If locale support doesn't work according to the explanation above,
check that the locale support in your operating system is
correctly configured. To check what locales are installed on your
system, you can use the command `locale -a` if
your operating system provides it.

Check that PostgreSQL is actually using the locale
that you think it is. The `LC_COLLATE` and `LC_CTYPE`
settings are determined when a database is created, and cannot be
changed except by creating a new database. Other locale
settings including `LC_MESSAGES` and `LC_MONETARY`
are initially determined by the environment the server is started
in, but can be changed on-the-fly. You can check the active locale
settings using the `SHOW` command.

The directory `src/test/locale` in the source
distribution contains a test suite for
PostgreSQL's locale support.

Client applications that handle server-side errors by parsing the
text of the error message will obviously have problems when the
server's messages are in a different language. Authors of such
applications are advised to make use of the error code scheme
instead.

Maintaining catalogs of message translations requires the on-going
efforts of many volunteers that want to see
PostgreSQL speak their preferred language well.
If messages in your language are currently not available or not fully
translated, your assistance would be appreciated. If you want to
help, refer to [Chapter 56](../../internals/nls/README.md) or write to the developers'
mailing list.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/locale.html)（英文原文，待翻譯）
