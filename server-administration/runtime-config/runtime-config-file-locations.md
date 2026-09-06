## 19.2. File Locations [#](#RUNTIME-CONFIG-FILE-LOCATIONS)

In addition to the `postgresql.conf` file
already mentioned, PostgreSQL uses
two other manually-edited configuration files, which control
client authentication (their use is discussed in [Chapter 20](../client-authentication/README.md)). By default, all three
configuration files are stored in the database cluster's data
directory. The parameters described in this section allow the
configuration files to be placed elsewhere. (Doing so can ease
administration. In particular it is often easier to ensure that
the configuration files are properly backed-up when they are
kept separate.)

<a id="GUC-DATA-DIRECTORY"></a>

`data_directory` (`string`) <a id="id-1.6.6.5.3.1.1.3"></a> [#](#GUC-DATA-DIRECTORY)
:   Specifies the directory to use for data storage.
    This parameter can only be set at server start.
<a id="GUC-CONFIG-FILE"></a>

`config_file` (`string`) <a id="id-1.6.6.5.3.2.1.3"></a> [#](#GUC-CONFIG-FILE)
:   Specifies the main server configuration file
    (customarily called `postgresql.conf`).
    This parameter can only be set on the `postgres` command line.
<a id="GUC-HBA-FILE"></a>

`hba_file` (`string`) <a id="id-1.6.6.5.3.3.1.3"></a> [#](#GUC-HBA-FILE)
:   Specifies the configuration file for host-based authentication
    (customarily called `pg_hba.conf`).
    This parameter can only be set at server start.
<a id="GUC-IDENT-FILE"></a>

`ident_file` (`string`) <a id="id-1.6.6.5.3.4.1.3"></a> [#](#GUC-IDENT-FILE)
:   Specifies the configuration file for user name mapping
    (customarily called `pg_ident.conf`).
    This parameter can only be set at server start.
    See also [Section 20.2](../client-authentication/auth-username-maps.md).
<a id="GUC-EXTERNAL-PID-FILE"></a>

`external_pid_file` (`string`) <a id="id-1.6.6.5.3.5.1.3"></a> [#](#GUC-EXTERNAL-PID-FILE)
:   Specifies the name of an additional process-ID (PID) file that the
    server should create for use by server administration programs.
    This parameter can only be set at server start.

In a default installation, none of the above parameters are set
explicitly. Instead, the
data directory is specified by the `-D` command-line
option or the `PGDATA` environment variable, and the
configuration files are all found within the data directory.

If you wish to keep the configuration files elsewhere than the
data directory, the `postgres` `-D`
command-line option or `PGDATA` environment variable
must point to the directory containing the configuration files,
and the `data_directory` parameter must be set in
`postgresql.conf` (or on the command line) to show
where the data directory is actually located. Notice that
`data_directory` overrides `-D` and
`PGDATA` for the location
of the data directory, but not for the location of the configuration
files.

If you wish, you can specify the configuration file names and locations
individually using the parameters `config_file`,
`hba_file` and/or `ident_file`.
`config_file` can only be specified on the
`postgres` command line, but the others can be
set within the main configuration file. If all three parameters plus
`data_directory` are explicitly set, then it is not necessary
to specify `-D` or `PGDATA`.

When setting any of these parameters, a relative path will be interpreted
with respect to the directory in which `postgres`
is started.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-file-locations.html)（英文原文，待翻譯）
