<a id="id-1.9.3.165.1"></a>

## RESET

RESET — restore the value of a run-time parameter to the default value

## Synopsis

```

RESET configuration_parameter
RESET ALL
```

<a id="id-1.9.3.165.5"></a>

## Description

`RESET` restores run-time parameters to their
default values. `RESET` is an alternative
spelling for

```

SET configuration_parameter TO DEFAULT
```

Refer to [SET](sql-set.md) for
details.

The default value is defined as the value that the parameter would
have had, if no `SET` had ever been issued for it in the
current session. The actual source of this value might be a
compiled-in default, the configuration file, command-line options,
or per-database or per-user default settings. This is subtly different
from defining it as “the value that the parameter had at session
start”, because if the value came from the configuration file, it
will be reset to whatever is specified by the configuration file now.
See [Chapter 19](../../server-administration/runtime-config/README.md) for details.

The transactional behavior of `RESET` is the same as
`SET`: its effects will be undone by transaction rollback.

<a id="id-1.9.3.165.6"></a>

## Parameters

*`configuration_parameter`*
:   Name of a settable run-time parameter. Available parameters are
    documented in [Chapter 19](../../server-administration/runtime-config/README.md) and on the
    [SET](sql-set.md) reference page.

`ALL`
:   Resets all settable run-time parameters to default values.

<a id="id-1.9.3.165.7"></a>

## Examples

Set the `timezone` configuration variable to its default value:

```

RESET timezone;
```

<a id="id-1.9.3.165.8"></a>

## Compatibility

`RESET` is a PostgreSQL extension.

<a id="id-1.9.3.165.9"></a>

## See Also

[SET](sql-set.md), [SHOW](sql-show.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-reset.html)（英文原文，待翻譯）
