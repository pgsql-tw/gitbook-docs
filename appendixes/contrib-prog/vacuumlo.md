<a id="id-1.11.8.4.4.1"></a>

## vacuumlo

vacuumlo — remove orphaned large objects from a PostgreSQL database

## Synopsis

<a id="id-1.11.8.4.4.4.1"></a>

`vacuumlo` [*`option`*...] *`dbname`*...

<a id="id-1.11.8.4.4.5"></a>

## Description

vacuumlo is a simple utility program that will remove any
“orphaned” large objects from a
PostgreSQL database. An orphaned large object (LO) is
considered to be any LO whose OID does not appear in any `oid` or
`lo` data column of the database.

If you use this, you may also be interested in the `lo_manage`
trigger in the [lo](../contrib/lo.md) module.
`lo_manage` is useful to try
to avoid creating orphaned LOs in the first place.

All databases named on the command line are processed.

<a id="id-1.11.8.4.4.6"></a>

## Options

vacuumlo accepts the following command-line arguments:

`-l limit`<br>`--limit=limit`
:   Remove no more than *`limit`* large objects per
    transaction (default 1000). Since the server acquires a lock per LO
    removed, removing too many LOs in one transaction risks exceeding
    [max_locks_per_transaction](../../server-administration/runtime-config/runtime-config-locks.md#GUC-MAX-LOCKS-PER-TRANSACTION). Set the limit to
    zero if you want all removals done in a single transaction.

`-n`<br>`--dry-run`
:   Don't remove anything, just show what would be done.

`-v`<br>`--verbose`
:   Write a lot of progress messages.

`-V`<br>`--version`
:   Print the vacuumlo version and exit.

`-?`<br>`--help`
:   Show help about vacuumlo command line
    arguments, and exit.

vacuumlo also accepts the following command-line
arguments for connection parameters:

`-h host`<br>`--host=host`
:   Database server's host.

`-p port`<br>`--port=port`
:   Database server's port.

`-U username`<br>`--username=username`
:   User name to connect as.

`-w`<br>`--no-password`
:   Never issue a password prompt. If the server requires password
    authentication and a password is not available by other means
    such as a `.pgpass` file, the connection
    attempt will fail. This option can be useful in batch jobs and
    scripts where no user is present to enter a password.

`-W`<br>`--password`
:   Force vacuumlo to prompt for a
    password before connecting to a database.

    This option is never essential, since
    vacuumlo will automatically prompt
    for a password if the server demands password authentication.
    However, vacuumlo will waste a
    connection attempt finding out that the server wants a password.
    In some cases it is worth typing `-W` to avoid the extra
    connection attempt.

<a id="id-1.11.8.4.4.7"></a>

## Environment

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   Default connection parameters.

This utility, like most other PostgreSQL utilities,
also uses the environment variables supported by libpq
(see [Section 32.15](../../client-interfaces/libpq/libpq-envars.md)).

The environment variable `PG_COLOR` specifies whether to use
color in diagnostic messages. Possible values are
`always`, `auto` and
`never`.

<a id="id-1.11.8.4.4.8"></a>

## Notes

vacuumlo works by the following method:
First, vacuumlo builds a temporary table which contains all
of the OIDs of the large objects in the selected database. It then scans
through all columns in the database that are of type
`oid` or `lo`, and removes matching entries from the temporary
table. (Note: Only types with these names are considered; in particular,
domains over them are not considered.) The remaining entries in the
temporary table identify orphaned LOs. These are removed.

<a id="id-1.11.8.4.4.9"></a>

## Author

Peter Mount `<peter@retep.org.uk>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/vacuumlo.html)（英文原文，待翻譯）
