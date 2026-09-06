<a id="id-1.9.3.179.1"></a>

## SHOW

SHOW — show the value of a run-time parameter

## Synopsis

```

SHOW name
SHOW ALL
```

<a id="id-1.9.3.179.5"></a>

## Description

`SHOW` will display the current setting of
run-time parameters. These variables can be set using the
`SET` statement, by editing the
`postgresql.conf` configuration file, through
the `PGOPTIONS` environmental variable (when using
libpq or a libpq-based
application), or through command-line flags when starting the
`postgres` server. See [Chapter 19](../../server-administration/runtime-config/README.md) for details.

<a id="id-1.9.3.179.6"></a>

## Parameters

*`name`*
:   The name of a run-time parameter. Available parameters are
    documented in [Chapter 19](../../server-administration/runtime-config/README.md) and on the [SET](sql-set.md) reference page. In
    addition, there are a few parameters that can be shown but not
    set:

    `SERVER_VERSION`
    :   Shows the server's version number.

    `SERVER_ENCODING`
    :   Shows the server-side character set encoding. At present,
        this parameter can be shown but not set, because the
        encoding is determined at database creation time.

    `IS_SUPERUSER`
    :   True if the current role has superuser privileges.

`ALL`
:   Show the values of all configuration parameters, with descriptions.

<a id="id-1.9.3.179.7"></a>

## Notes

The function `current_setting` produces
equivalent output; see [Section 9.28.1](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SET).
Also, the
[`pg_settings`](../../internals/views/view-pg-settings.md)
system view produces the same information.

<a id="id-1.9.3.179.8"></a>

## Examples

Show the current setting of the parameter `DateStyle`:

```

SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

Show the current setting of the parameter `geqo`:

```

SHOW geqo;
 geqo
------
 on
(1 row)
```

Show all settings:

```

SHOW ALL;
            name         | setting |                description
-------------------------+---------+-------------------------------------------------
 allow_system_table_mods | off     | Allows modifications of the structure of ...
    .
    .
    .
 xmloption               | content | Sets whether XML data in implicit parsing ...
 zero_damaged_pages      | off     | Continues processing past damaged page headers.
(196 rows)
```

<a id="id-1.9.3.179.9"></a>

## Compatibility

The `SHOW` command is a
PostgreSQL extension.

<a id="id-1.9.3.179.10"></a>

## See Also

[SET](sql-set.md), [RESET](sql-reset.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-show.html)（英文原文，待翻譯）
