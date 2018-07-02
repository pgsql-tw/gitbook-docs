# RESET

RESET — restore the value of a run-time parameter to the default value

### Synopsis

```text
RESET configuration_parameter
RESET ALL
```

### Description

`RESET` restores run-time parameters to their default values. `RESET` is an alternative spelling for

```text
SET configuration_parameter TO DEFAULT
```

Refer to [SET](https://www.postgresql.org/docs/10/static/sql-set.html) for details.

The default value is defined as the value that the parameter would have had, if no `SET` had ever been issued for it in the current session. The actual source of this value might be a compiled-in default, the configuration file, command-line options, or per-database or per-user default settings. This is subtly different from defining it as “the value that the parameter had at session start”, because if the value came from the configuration file, it will be reset to whatever is specified by the configuration file now. See [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html) for details.

The transactional behavior of `RESET` is the same as `SET`: its effects will be undone by transaction rollback.

### Parameters

_`configuration_parameter`_

Name of a settable run-time parameter. Available parameters are documented in [Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html) and on the [SET](https://www.postgresql.org/docs/10/static/sql-set.html) reference page.

`ALL`

Resets all settable run-time parameters to default values.

### Examples

Set the `timezone` configuration variable to its default value:

```text
RESET timezone;
```

### Compatibility

`RESET` is a PostgreSQL extension.

### See Also

[SET](set.md), [SHOW](show.md)

