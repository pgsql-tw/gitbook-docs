<a id="id-1.9.3.59.1"></a>

## CREATE COLLATION

CREATE COLLATION — define a new collation

## Synopsis

```

CREATE COLLATION [ IF NOT EXISTS ] name (
    [ LOCALE = locale, ]
    [ LC_COLLATE = lc_collate, ]
    [ LC_CTYPE = lc_ctype, ]
    [ PROVIDER = provider, ]
    [ DETERMINISTIC = boolean, ]
    [ RULES = rules, ]
    [ VERSION = version ]
)
CREATE COLLATION [ IF NOT EXISTS ] name FROM existing_collation
```

<a id="SQL-CREATECOLLATION-DESCRIPTION"></a>

## Description

`CREATE COLLATION` defines a new collation using
the specified operating system locale settings,
or by copying an existing collation.

To be able to create a collation, you must
have `CREATE` privilege on the destination schema.

<a id="id-1.9.3.59.6"></a>

## Parameters

`IF NOT EXISTS`
:   Do not throw an error if a collation with the same name already exists.
    A notice is issued in this case. Note that there is no guarantee that
    the existing collation is anything like the one that would have been created.

*`name`*
:   The name of the collation. The collation name can be
    schema-qualified. If it is not, the collation is defined in the
    current schema. The collation name must be unique within that
    schema. (The system catalogs can contain collations with the
    same name for other encodings, but these are ignored if the
    database encoding does not match.)

*`locale`*
:   The locale name for this collation. See [Section 23.2.2.3.1](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-LIBC) and [Section 23.2.2.3.2](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-ICU) for details.

    If *`provider`* is `libc`, this
    is a shortcut for setting `LC_COLLATE` and
    `LC_CTYPE` at once. If you specify
    *`locale`*, you cannot specify either of those
    parameters.

    If *`provider`* is `builtin`,
    then *`locale`* must be specified and set to
    either `C`, `C.UTF-8` or
    `PG_UNICODE_FAST`.

*`lc_collate`*
:   If *`provider`* is `libc`, use
    the specified operating system locale for the
    `LC_COLLATE` locale category.

*`lc_ctype`*
:   If *`provider`* is `libc`, use
    the specified operating system locale for the `LC_CTYPE`
    locale category.

*`provider`*
:   Specifies the provider to use for locale services associated with this
    collation. Possible values are `builtin`,
    `icu`<a id="id-1.9.3.59.6.2.6.2.1.3"></a> (if
    the server was built with ICU support) or `libc`.
    `libc` is the default. See [Section 23.1.4](../../server-administration/charset/locale.md#LOCALE-PROVIDERS) for details.

`DETERMINISTIC`
:   Specifies whether the collation should use deterministic comparisons.
    The default is true. A deterministic comparison considers strings that
    are not byte-wise equal to be unequal even if they are considered
    logically equal by the comparison. PostgreSQL breaks ties using a
    byte-wise comparison. Comparison that is not deterministic can make the
    collation be, say, case- or accent-insensitive. For that, you need to
    choose an appropriate `LOCALE` setting
    *and* set the collation to not deterministic here.

    Nondeterministic collations are only supported with the ICU provider.

*`rules`*
:   Specifies additional collation rules to customize the behavior of the
    collation. This is supported for ICU only. See [Section 23.2.3.4](../../server-administration/charset/collation.md#ICU-TAILORING-RULES) for details.

*`version`*
:   Specifies the version string to store with the collation. Normally,
    this should be omitted, which will cause the version to be computed
    from the actual version of the collation as provided by the operating
    system. This option is intended to be used
    by `pg_upgrade` for copying the version from an
    existing installation.

    See also [ALTER COLLATION](sql-altercollation.md) for how to handle
    collation version mismatches.

*`existing_collation`*
:   The name of an existing collation to copy. The new collation
    will have the same properties as the existing one, but it
    will be an independent object.

<a id="SQL-CREATECOLLATION-NOTES"></a>

## Notes

`CREATE COLLATION` takes a `SHARE ROW
EXCLUSIVE` lock, which is self-conflicting, on the
`pg_collation` system catalog, so only one
`CREATE COLLATION` command can run at a time.

Use `DROP COLLATION` to remove user-defined collations.

See [Section 23.2.2.3](../../server-administration/charset/collation.md#COLLATION-CREATE) for more information on how to create collations.

When using the `libc` collation provider, the locale must
be applicable to the current database encoding.
See [CREATE DATABASE](sql-createdatabase.md) for the precise rules.

<a id="SQL-CREATECOLLATION-EXAMPLES"></a>

## Examples

To create a collation from the operating system locale
`fr_FR.utf8`
(assuming the current database encoding is `UTF8`):

```

CREATE COLLATION french (locale = 'fr_FR.utf8');
```

To create a collation using the ICU provider using German phone book sort order:

```

CREATE COLLATION german_phonebook (provider = icu, locale = 'de-u-co-phonebk');
```

To create a collation using the ICU provider, based on the root ICU locale,
with custom rules:

```

CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

See [Section 23.2.3.4](../../server-administration/charset/collation.md#ICU-TAILORING-RULES) for further details and examples
on the rules syntax.

To create a collation from an existing collation:

```

CREATE COLLATION german FROM "de_DE";
```

This can be convenient to be able to use operating-system-independent
collation names in applications.

<a id="SQL-CREATECOLLATION-COMPAT"></a>

## Compatibility

There is a `CREATE COLLATION` statement in the SQL
standard, but it is limited to copying an existing collation. The
syntax to create a new collation is
a PostgreSQL extension.

<a id="SQL-CREATECOLLATION-SEEALSO"></a>

## See Also

[ALTER COLLATION](sql-altercollation.md), [DROP COLLATION](sql-dropcollation.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createcollation.html)（英文原文，待翻譯）
