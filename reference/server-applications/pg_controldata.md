<a id="APP-PGCONTROLDATA"></a><a id="id-1.9.5.6.1"></a>

# pg_controldata

pg_controldata — display control information of a PostgreSQL database cluster

## Synopsis

<a id="id-1.9.5.6.4.1"></a>

`pg_controldata` [<em class="replaceable"><code>option</code></em>] [[ `-D` | `--pgdata` ]<em class="replaceable"><code>datadir</code></em>]

<a id="R1-APP-PGCONTROLDATA-1"></a>

## Description

`pg_controldata` prints information initialized during `initdb`, such as the catalog version. It also shows information about write-ahead logging and checkpoint processing. This information is cluster-wide, and not specific to any one database.

This utility can only be run by the user who initialized the cluster because it requires read access to the data directory. You can specify the data directory on the command line, or use the environment variable `PGDATA`. This utility supports the options `-V` and `--version`, which print the pg_controldata version and exit. It also supports options `-?` and `--help`, which output the supported arguments.

<a id="id-1.9.5.6.6"></a>

## Environment

`PGDATA`

Default data directory location

`PG_COLOR`

Specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

---

原文：[PostgreSQL 15.19 Documentation](pg_controldata.md)（英文原文，待翻譯）
