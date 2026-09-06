<a id="id-1.9.5.3.1"></a>

## initdb

initdb — create a new PostgreSQL database cluster

## Synopsis

<a id="id-1.9.5.3.4.1"></a>

`initdb` [*`option`*...] [ `--pgdata` | `-D` ] *`directory`*

<a id="R1-APP-INITDB-1"></a>

## Description

`initdb` creates a new
PostgreSQL [*[database cluster](../../appendixes/glossary/README.md#GLOSSARY-DB-CLUSTER)*](../../appendixes/glossary/README.md#GLOSSARY-DB-CLUSTER).

Creating a database cluster consists of creating the
[*[directories](../../appendixes/glossary/README.md#GLOSSARY-DATA-DIRECTORY)*](../../appendixes/glossary/README.md#GLOSSARY-DATA-DIRECTORY) in
which the cluster data will live, generating the shared catalog
tables (tables that belong to the whole cluster rather than to any
particular database), and creating the `postgres`,
`template1`, and `template0` databases.
The `postgres` database is a default database meant
for use by users, utilities and third party applications.
`template1` and `template0` are
meant as source databases to be copied by later `CREATE
DATABASE` commands. `template0` should never
be modified, but you can add objects to `template1`,
which by default will be copied into databases created later. See
[Section 22.3](../../server-administration/managing-databases/manage-ag-templatedbs.md) for more details.

Although `initdb` will attempt to create the
specified data directory, it might not have permission if the parent
directory of the desired data directory is root-owned. To initialize
in such a setup, create an empty data directory as root, then use
`chown` to assign ownership of that directory to the
database user account, then `su` to become the
database user to run `initdb`.

`initdb` must be run as the user that will own the
server process, because the server needs to have access to the
files and directories that `initdb` creates.
Since the server cannot be run as root, you must not run
`initdb` as root either. (It will in fact refuse
to do so.)

For security reasons the new cluster created by `initdb`
will only be accessible by the cluster owner by default. The
`--allow-group-access` option allows any user in the same
group as the cluster owner to read files in the cluster. This is useful
for performing backups as a non-privileged user.

`initdb` initializes the database cluster's default locale
and character set encoding. These can also be set separately for each
database when it is created. `initdb` determines those
settings for the template databases, which will serve as the default for
all other databases.

By default, `initdb` uses the locale provider
`libc` (see [Section 23.1.4](../../server-administration/charset/locale.md#LOCALE-PROVIDERS)). The
`libc` locale provider takes the locale settings from the
environment, and determines the encoding from the locale settings.

To choose a different locale for the cluster, use the option
`--locale`. There are also individual options
`--lc-*` and `--icu-locale` (see below) to
set values for the individual locale categories. Note that inconsistent
settings for different locale categories can give nonsensical results, so
this should be used with care.

Alternatively, `initdb` can use the ICU library to provide
locale services by specifying `--locale-provider=icu`. The
server must be built with ICU support. To choose the specific ICU locale ID
to apply, use the option `--icu-locale`. Note that for
implementation reasons and to support legacy code,
`initdb` will still select and initialize libc locale
settings when the ICU locale provider is used.

When `initdb` runs, it will print out the locale settings
it has chosen. If you have complex requirements or specified multiple
options, it is advisable to check that the result matches what was
intended.

More details about locale settings can be found in [Section 23.1](../../server-administration/charset/locale.md).

To alter the default encoding, use the `--encoding`.
More details can be found in [Section 23.3](../../server-administration/charset/multibyte.md).

<a id="id-1.9.5.3.6"></a>

## Options

<a id="APP-INITDB-OPTION-AUTH"></a>

`-A authmethod`<br>`--auth=authmethod` [#](#APP-INITDB-OPTION-AUTH)
:   This option specifies the default authentication method for local
    users used in `pg_hba.conf` (`host`
    and `local` lines). See [Section 20.1](../../server-administration/client-authentication/auth-pg-hba-conf.md)
    for an overview of valid values.

    `initdb` will
    prepopulate `pg_hba.conf` entries using the
    specified authentication method for non-replication as well as
    replication connections.

    Do not use `trust` unless you trust all local users on your
    system. `trust` is the default for ease of installation.
<a id="APP-INITDB-OPTION-AUTH-HOST"></a>

`--auth-host=authmethod` [#](#APP-INITDB-OPTION-AUTH-HOST)
:   This option specifies the authentication method for local users via
    TCP/IP connections used in `pg_hba.conf`
    (`host` lines).
<a id="APP-INITDB-OPTION-AUTH-LOCAL"></a>

`--auth-local=authmethod` [#](#APP-INITDB-OPTION-AUTH-LOCAL)
:   This option specifies the authentication method for local users via
    Unix-domain socket connections used in `pg_hba.conf`
    (`local` lines).
<a id="APP-INITDB-OPTION-PGDATA"></a>

`-D directory`<br>`--pgdata=directory` [#](#APP-INITDB-OPTION-PGDATA)
:   This option specifies the directory where the database cluster
    should be stored. This is the only information required by
    `initdb`, but you can avoid writing it by
    setting the `PGDATA` environment variable, which
    can be convenient since the database server
    (`postgres`) can find the data
    directory later by the same variable.
<a id="APP-INITDB-OPTION-ENCODING"></a>

`-E encoding`<br>`--encoding=encoding` [#](#APP-INITDB-OPTION-ENCODING)
:   Selects the encoding of the template databases. This will also be the
    default encoding of any database you create later, unless you override
    it then. The character sets supported by the
    PostgreSQL server are described in [Section 23.3.1](../../server-administration/charset/multibyte.md#MULTIBYTE-CHARSET-SUPPORTED).

    By default, the template database encoding is derived from the
    locale. If [`--no-locale`](app-initdb.md#APP-INITDB-OPTION-NO-LOCALE) is specified
    (or equivalently, if the locale is `C` or
    `POSIX`), then the default is `UTF8`
    for the ICU provider and `SQL_ASCII` for the
    `libc` provider.
<a id="APP-INITDB-ALLOW-GROUP-ACCESS"></a>

`-g`<br>`--allow-group-access` [#](#APP-INITDB-ALLOW-GROUP-ACCESS)
:   Allows users in the same group as the cluster owner to read all cluster
    files created by `initdb`. This option is ignored
    on Windows as it does not support
    POSIX-style group permissions.
<a id="APP-INITDB-ICU-LOCALE"></a>

`--icu-locale=locale` [#](#APP-INITDB-ICU-LOCALE)
:   Specifies the ICU locale when the ICU provider is used. Locale support
    is described in [Section 23.1](../../server-administration/charset/locale.md).
<a id="APP-INITDB-ICU-RULES"></a>

`--icu-rules=rules` [#](#APP-INITDB-ICU-RULES)
:   Specifies additional collation rules to customize the behavior of the
    default collation. This is supported for ICU only.
<a id="APP-INITDB-DATA-CHECKSUMS"></a>

`-k`<br>`--data-checksums` [#](#APP-INITDB-DATA-CHECKSUMS)
:   Use checksums on data pages to help detect corruption by the I/O
    system that would otherwise be silent. This is enabled by default;
    use [`--no-data-checksums`](app-initdb.md#APP-INITDB-NO-DATA-CHECKSUMS) to disable
    checksums.

    Enabling checksums
    might incur a small performance penalty. If set, checksums
    are calculated for all objects, in all databases. All checksum
    failures will be reported in the
    [`pg_stat_database`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW) view.
    See [Section 28.2](../../server-administration/wal/checksums.md) for details.
<a id="APP-INITDB-OPTION-LOCALE"></a>

`--locale=locale` [#](#APP-INITDB-OPTION-LOCALE)
:   Sets the default locale for the database cluster. If this
    option is not specified, the locale is inherited from the
    environment that `initdb` runs in. Locale
    support is described in [Section 23.1](../../server-administration/charset/locale.md).

    If `--locale-provider` is `builtin`,
    `--locale` or `--builtin-locale` must be
    specified and set to `C`, `C.UTF-8`
    or `PG_UNICODE_FAST`.
<a id="APP-INITDB-OPTION-LC-COLLATE"></a>

`--lc-collate=locale`<br>`--lc-ctype=locale`<br>`--lc-messages=locale`<br>`--lc-monetary=locale`<br>`--lc-numeric=locale`<br>`--lc-time=locale` [#](#APP-INITDB-OPTION-LC-COLLATE)
:   Like `--locale`, but only sets the locale in
    the specified category.
<a id="APP-INITDB-OPTION-NO-LOCALE"></a>

`--no-locale` [#](#APP-INITDB-OPTION-NO-LOCALE)
:   Equivalent to `--locale=C`.
<a id="APP-INITDB-BUILTIN-LOCALE"></a>

`--builtin-locale=locale` [#](#APP-INITDB-BUILTIN-LOCALE)
:   Specifies the locale name when the builtin provider is used. Locale support
    is described in [Section 23.1](../../server-administration/charset/locale.md).
<a id="APP-INITDB-OPTION-LOCALE-PROVIDER"></a>

`--locale-provider={builtin|libc|icu}` [#](#APP-INITDB-OPTION-LOCALE-PROVIDER)
:   This option sets the locale provider for databases created in the new
    cluster. It can be overridden in the `CREATE
    DATABASE` command when new databases are subsequently
    created. The default is `libc` (see [Section 23.1.4](../../server-administration/charset/locale.md#LOCALE-PROVIDERS)).
<a id="APP-INITDB-NO-DATA-CHECKSUMS"></a>

`--no-data-checksums` [#](#APP-INITDB-NO-DATA-CHECKSUMS)
:   Do not enable data checksums.
<a id="APP-INITDB-OPTION-PWFILE"></a>

`--pwfile=filename` [#](#APP-INITDB-OPTION-PWFILE)
:   Makes `initdb` read the bootstrap superuser's password
    from a file. The first line of the file is taken as the password.
<a id="APP-INITDB-OPTION-TEXT-SEARCH-CONFIG"></a>

`-T config`<br>`--text-search-config=config` [#](#APP-INITDB-OPTION-TEXT-SEARCH-CONFIG)
:   Sets the default text search configuration.
    See [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) for further information.
<a id="APP-INITDB-OPTION-USERNAME"></a>

`-U username`<br>`--username=username` [#](#APP-INITDB-OPTION-USERNAME)
:   Sets the user name of the
    [*[bootstrap superuser](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)*](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER).
    This defaults to the name of the operating-system user running
    `initdb`.
<a id="APP-INITDB-OPTION-PWPROMPT"></a>

`-W`<br>`--pwprompt` [#](#APP-INITDB-OPTION-PWPROMPT)
:   Makes `initdb` prompt for a password
    to give the bootstrap superuser. If you don't plan on using password
    authentication, this is not important. Otherwise you won't be
    able to use password authentication until you have a password
    set up.
<a id="APP-INITDB-OPTION-WALDIR"></a>

`-X directory`<br>`--waldir=directory` [#](#APP-INITDB-OPTION-WALDIR)
:   This option specifies the directory where the write-ahead log
    should be stored.
<a id="APP-INITDB-OPTION-WAL-SEGSIZE"></a>

`--wal-segsize=size` [#](#APP-INITDB-OPTION-WAL-SEGSIZE)
:   Set the *WAL segment size*, in megabytes. This
    is the size of each individual file in the WAL log. The default size
    is 16 megabytes. The value must be a power of 2 between 1 and 1024
    (megabytes). This option can only be set during initialization, and
    cannot be changed later.

    It may be useful to adjust this size to control the granularity of
    WAL log shipping or archiving. Also, in databases with a high volume
    of WAL, the sheer number of WAL files per directory can become a
    performance and management problem. Increasing the WAL file size
    will reduce the number of WAL files.

Other, less commonly used, options are also available:

<a id="APP-INITDB-OPTION-SET"></a>

`-c name=value`<br>`--set name=value` [#](#APP-INITDB-OPTION-SET)
:   Forcibly set the server parameter *`name`*
    to *`value`* during `initdb`,
    and also install that setting in the
    generated `postgresql.conf` file,
    so that it will apply during future server runs.
    This option can be given more than once to set several parameters.
    It is primarily useful when the environment is such that the server
    will not start at all using the default parameters.
<a id="APP-INITDB-OPTION-DEBUG"></a>

`-d`<br>`--debug` [#](#APP-INITDB-OPTION-DEBUG)
:   Print debugging output from the bootstrap backend and a few other
    messages of lesser interest for the general public.
    The bootstrap backend is the program `initdb`
    uses to create the catalog tables. This option generates a tremendous
    amount of extremely boring output.
<a id="APP-INITDB-OPTION-DISCARD-CACHES"></a>

`--discard-caches` [#](#APP-INITDB-OPTION-DISCARD-CACHES)
:   Run the bootstrap backend with the
    `debug_discard_caches=1` option.
    This takes a very long time and is only of use for deep debugging.
<a id="APP-INITDB-OPTION-L"></a>

`-L directory` [#](#APP-INITDB-OPTION-L)
:   Specifies where `initdb` should find
    its input files to initialize the database cluster. This is
    normally not necessary. You will be told if you need to
    specify their location explicitly.
<a id="APP-INITDB-OPTION-NO-CLEAN"></a>

`-n`<br>`--no-clean` [#](#APP-INITDB-OPTION-NO-CLEAN)
:   By default, when `initdb`
    determines that an error prevented it from completely creating the database
    cluster, it removes any files it might have created before discovering
    that it cannot finish the job. This option inhibits tidying-up and is
    thus useful for debugging.
<a id="APP-INITDB-OPTION-NO-SYNC"></a>

`-N`<br>`--no-sync` [#](#APP-INITDB-OPTION-NO-SYNC)
:   By default, `initdb` will wait for all files to be
    written safely to disk. This option causes `initdb`
    to return without waiting, which is faster, but means that a
    subsequent operating system crash can leave the data directory
    corrupt. Generally, this option is useful for testing, but should not
    be used when creating a production installation.
<a id="APP-INITDB-OPTION-NO-SYNC-DATA-FILES"></a>

`--no-sync-data-files` [#](#APP-INITDB-OPTION-NO-SYNC-DATA-FILES)
:   By default, `initdb` safely writes all database files
    to disk. This option instructs `initdb` to skip
    synchronizing all files in the individual database directories, the
    database directories themselves, and the tablespace directories, i.e.,
    everything in the `base` subdirectory and any other
    tablespace directories. Other files, such as those in
    `pg_wal` and `pg_xact`, will still be
    synchronized unless the `--no-sync` option is also
    specified.

    Note that if `--no-sync-data-files` is used in
    conjunction with `--sync-method=syncfs`, some or all of
    the aforementioned files and directories will be synchronized because
    `syncfs` processes entire file systems.

    This option is primarily intended for internal use by tools that
    separately ensure the skipped files are synchronized to disk.
<a id="APP-INITDB-OPTION-NO-INSTRUCTIONS"></a>

`--no-instructions` [#](#APP-INITDB-OPTION-NO-INSTRUCTIONS)
:   By default, `initdb` will write instructions for how
    to start the cluster at the end of its output. This option causes
    those instructions to be left out. This is primarily intended for use
    by tools that wrap `initdb` in platform-specific
    behavior, where those instructions are likely to be incorrect.
<a id="APP-INITDB-OPTION-SHOW"></a>

`-s`<br>`--show` [#](#APP-INITDB-OPTION-SHOW)
:   Show internal settings and exit, without doing anything else. This
    can be used to debug the initdb
    installation.
<a id="APP-INITDB-OPTION-SYNC-METHOD"></a>

`--sync-method=method` [#](#APP-INITDB-OPTION-SYNC-METHOD)
:   When set to `fsync`, which is the default,
    `initdb` will recursively open and synchronize all
    files in the data directory. The search for files will follow symbolic
    links for the WAL directory and each configured tablespace.

    On Linux, `syncfs` may be used instead to ask the
    operating system to synchronize the whole file systems that contain the
    data directory, the WAL files, and each tablespace. See
    [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD) for information about
    the caveats to be aware of when using `syncfs`.

    This option has no effect when `--no-sync` is used.
<a id="APP-INITDB-OPTION-SYNC-ONLY"></a>

`-S`<br>`--sync-only` [#](#APP-INITDB-OPTION-SYNC-ONLY)
:   Safely write all database files to disk and exit. This does not
    perform any of the normal initdb operations.
    Generally, this option is useful for ensuring reliable recovery after
    changing [fsync](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FSYNC) from `off` to
    `on`.

Other options:

<a id="APP-INITDB-OPTION-VERSION"></a>

`-V`<br>`--version` [#](#APP-INITDB-OPTION-VERSION)
:   Print the initdb version and exit.
<a id="APP-INITDB-OPTION-HELP"></a>

`-?`<br>`--help` [#](#APP-INITDB-OPTION-HELP)
:   Show help about initdb command line
    arguments, and exit.

<a id="id-1.9.5.3.7"></a>

## Environment

<a id="APP-INITDB-ENVIRONMENT-PGDATA"></a>

`PGDATA` [#](#APP-INITDB-ENVIRONMENT-PGDATA)
:   Specifies the directory where the database cluster is to be
    stored; can be overridden using the `-D` option.
<a id="APP-INITDB-ENVIRONMENT-PG-COLOR"></a>

`PG_COLOR` [#](#APP-INITDB-ENVIRONMENT-PG-COLOR)
:   Specifies whether to use color in diagnostic messages. Possible values
    are `always`, `auto` and
    `never`.
<a id="APP-INITDB-ENVIRONMENT-TZ"></a>

`TZ` [#](#APP-INITDB-ENVIRONMENT-TZ)
:   Specifies the default time zone of the created database cluster. The
    value should be a full time zone name
    (see [Section 8.5.3](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-TIMEZONES)).

<a id="id-1.9.5.3.8"></a>

## Notes

`initdb` can also be invoked via
`pg_ctl initdb`.

<a id="id-1.9.5.3.9"></a>

## See Also

[pg_ctl](app-pg-ctl.md), [postgres](app-postgres.md), [Section 20.1](../../server-administration/client-authentication/auth-pg-hba-conf.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-initdb.html)（英文原文，待翻譯）
