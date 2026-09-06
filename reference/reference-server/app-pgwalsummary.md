<a id="id-1.9.5.15.1"></a>

## pg_walsummary

pg_walsummary — print contents of WAL summary files

## Synopsis

<a id="id-1.9.5.15.4.1"></a>

`pg_walsummary` [*`option`*...] [*`file`*...]

<a id="id-1.9.5.15.5"></a>

## Description

pg_walsummary is used to print the contents of
WAL summary files. These binary files are found in the
`pg_wal/summaries` subdirectory of the data directory,
and can be converted to text using this tool. This is not ordinarily
necessary, since WAL summary files primarily exist to support
[incremental backup](../../server-administration/backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP),
but it may be useful for debugging purposes.

A WAL summary file is indexed by tablespace OID, relation OID, and relation
fork. For each relation fork, it stores the list of blocks that were
modified by WAL within the range summarized in the file. It can also
store a "limit block," which is 0 if the relation fork was created or
truncated within the relevant WAL range, and otherwise the shortest length
to which the relation fork was truncated. If the relation fork was not
created, deleted, or truncated within the relevant WAL range, the limit
block is undefined or infinite and will not be printed by this tool.

<a id="id-1.9.5.15.6"></a>

## Options

`-i`<br>`--individual`
:   By default, `pg_walsummary` prints one line of output
    for each range of one or more consecutive modified blocks. This can
    make the output a lot briefer, since a relation where all blocks from
    0 through 999 were modified will produce only one line of output rather
    than 1000 separate lines. This option requests a separate line of
    output for every modified block.

`-q`<br>`--quiet`
:   Do not print any output, except for errors. This can be useful
    when you want to know whether a WAL summary file can be successfully
    parsed but don't care about the contents.

`-V`<br>`--version`
:   Display version information, then exit.

`-?`<br>`--help`
:   Shows help about pg_walsummary command line
    arguments, and exits.

<a id="id-1.9.5.15.7"></a>

## Environment

The environment variable `PG_COLOR` specifies whether to use
color in diagnostic messages. Possible values are
`always`, `auto` and
`never`.

<a id="id-1.9.5.15.8"></a>

## See Also

[pg_basebackup](../reference-client/app-pgbasebackup.md), [pg_combinebackup](../reference-client/app-pgcombinebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgwalsummary.html)（英文原文，待翻譯）
