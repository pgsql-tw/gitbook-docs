<a id="id-1.9.3.34.1"></a>

## ALTER SYSTEM

ALTER SYSTEM — change a server configuration parameter

## Synopsis

```

ALTER SYSTEM SET configuration_parameter { TO | = } { value [, ...] | DEFAULT }

ALTER SYSTEM RESET configuration_parameter
ALTER SYSTEM RESET ALL
```

<a id="id-1.9.3.34.5"></a>

## Description

`ALTER SYSTEM` is used for changing server configuration
parameters across the entire database cluster. It can be more convenient
than the traditional method of manually editing
the `postgresql.conf` file.
`ALTER SYSTEM` writes the given parameter setting to
the `postgresql.auto.conf` file, which is read in
addition to `postgresql.conf`.
Setting a parameter to `DEFAULT`, or using the
`RESET` variant, removes that configuration entry from the
`postgresql.auto.conf` file. Use `RESET
ALL` to remove all such configuration entries.

Values set with `ALTER SYSTEM` will be effective after
the next server configuration reload, or after the next server restart
in the case of parameters that can only be changed at server start.
A server configuration reload can be commanded by calling the SQL
function `pg_reload_conf()`, running `pg_ctl reload`,
or sending a SIGHUP signal to the main server process.

Only superusers and users granted `ALTER SYSTEM` privilege
on a parameter can change it using `ALTER SYSTEM`. Also, since
this command acts directly on the file system and cannot be rolled back,
it is not allowed inside a transaction block or function.

<a id="id-1.9.3.34.6"></a>

## Parameters

*`configuration_parameter`*
:   Name of a settable configuration parameter. Available parameters are
    documented in [Chapter 19](../../server-administration/runtime-config/README.md).

*`value`*
:   New value of the parameter. Values can be specified as string
    constants, identifiers, numbers, or comma-separated lists of
    these, as appropriate for the particular parameter.
    Values that are neither numbers nor valid identifiers must be quoted.
    `DEFAULT` can be written to specify removing the
    parameter and its value from `postgresql.auto.conf`.

    For some list-accepting parameters, quoted values will produce
    double-quoted output to preserve whitespace and commas; for others,
    double-quotes must be used inside single-quoted strings to get
    this effect.

<a id="id-1.9.3.34.7"></a>

## Notes

This command can't be used to set [data_directory](../../server-administration/runtime-config/runtime-config-file-locations.md#GUC-DATA-DIRECTORY),
[allow_alter_system](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM),
nor parameters that are not allowed in `postgresql.conf`
(e.g., [preset options](../../server-administration/runtime-config/runtime-config-preset.md)).

See [Section 19.1](../../server-administration/runtime-config/config-setting.md) for other ways to set the parameters.

`ALTER SYSTEM` can be disabled by setting
[allow_alter_system](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM) to `off`, but this
is not a security mechanism (as explained in detail in the documentation for
this parameter).

<a id="id-1.9.3.34.8"></a>

## Examples

Set the `wal_level`:

```

ALTER SYSTEM SET wal_level = replica;
```

Undo that, restoring whatever setting was effective
in `postgresql.conf`:

```

ALTER SYSTEM RESET wal_level;
```

<a id="id-1.9.3.34.9"></a>

## Compatibility

The `ALTER SYSTEM` statement is a
PostgreSQL extension.

<a id="id-1.9.3.34.10"></a>

## See Also

[SET](sql-set.md), [SHOW](sql-show.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altersystem.html)（英文原文，待翻譯）
