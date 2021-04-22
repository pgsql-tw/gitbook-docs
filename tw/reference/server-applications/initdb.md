# initdb

initdb — create a new PostgreSQL database cluster

## Synopsis

`initdb` \[_`option`_...\] \[ `--pgdata` \| `-D` \] _`directory`_

## Description

`initdb` creates a new PostgreSQL database cluster. A database cluster is a collection of databases that are managed by a single server instance.

Creating a database cluster consists of creating the directories in which the database data will live, generating the shared catalog tables \(tables that belong to the whole cluster rather than to any particular database\), and creating the `template1` and `postgres` databases. When you later create a new database, everything in the `template1` database is copied. \(Therefore, anything installed in `template1` is automatically copied into each database created later.\) The `postgres` database is a default database meant for use by users, utilities and third party applications.

Although `initdb` will attempt to create the specified data directory, it might not have permission if the parent directory of the desired data directory is root-owned. To initialize in such a setup, create an empty data directory as root, then use `chown` to assign ownership of that directory to the database user account, then `su` to become the database user to run `initdb`.

`initdb` must be run as the user that will own the server process, because the server needs to have access to the files and directories that `initdb` creates. Since the server cannot be run as root, you must not run `initdb` as root either. \(It will in fact refuse to do so.\)

For security reasons the new cluster created by `initdb` will only be accessible by the cluster owner by default. The `--allow-group-access` option allows any user in the same group as the cluster owner to read files in the cluster. This is useful for performing backups as a non-privileged user.

`initdb` initializes the database cluster's default locale and character set encoding. The character set encoding, collation order \(`LC_COLLATE`\) and character set classes \(`LC_CTYPE`, e.g. upper, lower, digit\) can be set separately for a database when it is created. `initdb` determines those settings for the `template1` database, which will serve as the default for all other databases.

To alter the default collation order or character set classes, use the `--lc-collate` and `--lc-ctype` options. Collation orders other than `C` or `POSIX` also have a performance penalty. For these reasons it is important to choose the right locale when running `initdb`.

The remaining locale categories can be changed later when the server is started. You can also use `--locale` to set the default for all locale categories, including collation order and character set classes. All server locale values \(`lc_*`\) can be displayed via `SHOW ALL`. More details can be found in [Section 23.1](https://www.postgresql.org/docs/current/locale.html).

To alter the default encoding, use the `--encoding`. More details can be found in [Section 23.3](https://www.postgresql.org/docs/current/multibyte.html).

## Options

`-A` _`authmethod`_  
`--auth=`_`authmethod`_

This option specifies the default authentication method for local users used in `pg_hba.conf` \(`host` and `local` lines\). `initdb` will prepopulate `pg_hba.conf` entries using the specified authentication method for non-replication as well as replication connections.

Do not use `trust` unless you trust all local users on your system. `trust` is the default for ease of installation.

`--auth-host=`_`authmethod`_

This option specifies the authentication method for local users via TCP/IP connections used in `pg_hba.conf` \(`host` lines\).

`--auth-local=`_`authmethod`_

This option specifies the authentication method for local users via Unix-domain socket connections used in `pg_hba.conf` \(`local` lines\).

`-D` _`directory`_  
`--pgdata=`_`directory`_

This option specifies the directory where the database cluster should be stored. This is the only information required by `initdb`, but you can avoid writing it by setting the `PGDATA` environment variable, which can be convenient since the database server \(`postgres`\) can find the database directory later by the same variable.

`-E` _`encoding`_  
`--encoding=`_`encoding`_

Selects the encoding of the template database. This will also be the default encoding of any database you create later, unless you override it there. The default is derived from the locale, or `SQL_ASCII` if that does not work. The character sets supported by the PostgreSQL server are described in [Section 23.3.1](https://www.postgresql.org/docs/current/multibyte.html#MULTIBYTE-CHARSET-SUPPORTED).

`-g`  
`--allow-group-access`

Allows users in the same group as the cluster owner to read all cluster files created by `initdb`. This option is ignored on Windows as it does not support POSIX-style group permissions.

`-k`  
`--data-checksums`

Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. Enabling checksums may incur a noticeable performance penalty. If set, checksums are calculated for all objects, in all databases. All checksum failures will be reported in the [pg\_stat\_database](https://www.postgresql.org/docs/current/monitoring-stats.html#PG-STAT-DATABASE-VIEW) view.

`--locale=`_`locale`_

Sets the default locale for the database cluster. If this option is not specified, the locale is inherited from the environment that `initdb` runs in. Locale support is described in [Section 23.1](https://www.postgresql.org/docs/current/locale.html).

`--lc-collate=`_`locale`_  
`--lc-ctype=`_`locale`_  
`--lc-messages=`_`locale`_  
`--lc-monetary=`_`locale`_  
`--lc-numeric=`_`locale`_  
`--lc-time=`_`locale`_

Like `--locale`, but only sets the locale in the specified category.`--no-locale`

Equivalent to `--locale=C`.

`-N`  
`--no-sync`

By default, `initdb` will wait for all files to be written safely to disk. This option causes `initdb` to return without waiting, which is faster, but means that a subsequent operating system crash can leave the data directory corrupt. Generally, this option is useful for testing, but should not be used when creating a production installation.

`--pwfile=`_`filename`_

Makes `initdb` read the database superuser's password from a file. The first line of the file is taken as the password.

`-S`  
`--sync-only`

Safely write all database files to disk and exit. This does not perform any of the normal initdb operations.

`-T` _`config`_  
`--text-search-config=`_`config`_

Sets the default text search configuration. See [default\_text\_search\_config](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-DEFAULT-TEXT-SEARCH-CONFIG) for further information.`-U` _`username`_  
`--username=`_`username`_

Selects the user name of the database superuser. This defaults to the name of the effective user running `initdb`. It is really not important what the superuser's name is, but one might choose to keep the customary name postgres, even if the operating system user's name is different.

`-W`  
`--pwprompt`

Makes `initdb` prompt for a password to give the database superuser. If you don't plan on using password authentication, this is not important. Otherwise you won't be able to use password authentication until you have a password set up.

`-X` _`directory`_  
`--waldir=`_`directory`_

This option specifies the directory where the write-ahead log should be stored.

`--wal-segsize=`_`size`_

Set the _WAL segment size_, in megabytes. This is the size of each individual file in the WAL log. The default size is 16 megabytes. The value must be a power of 2 between 1 and 1024 \(megabytes\). This option can only be set during initialization, and cannot be changed later.

It may be useful to adjust this size to control the granularity of WAL log shipping or archiving. Also, in databases with a high volume of WAL, the sheer number of WAL files per directory can become a performance and management problem. Increasing the WAL file size will reduce the number of WAL files.

Other, less commonly used, options are also available:

`-d`  
`--debug`

Print debugging output from the bootstrap backend and a few other messages of lesser interest for the general public. The bootstrap backend is the program `initdb` uses to create the catalog tables. This option generates a tremendous amount of extremely boring output.

`-L` _`directory`_

Specifies where `initdb` should find its input files to initialize the database cluster. This is normally not necessary. You will be told if you need to specify their location explicitly.

`-n`  
`--no-clean`

By default, when `initdb` determines that an error prevented it from completely creating the database cluster, it removes any files it might have created before discovering that it cannot finish the job. This option inhibits tidying-up and is thus useful for debugging.

Other options:

`-V`  
`--version`

Print the initdb version and exit.

`-?`  
`--help`

Show help about initdb command line arguments, and exit.

## Environment

`PGDATA`

Specifies the directory where the database cluster is to be stored; can be overridden using the `-D` option.`PG_COLOR`

Specifies whether to use color in diagnostics messages. Possible values are `always`, `auto`, `never`.`TZ`

Specifies the default time zone of the created database cluster. The value should be a full time zone name \(see [Section 8.5.3](https://www.postgresql.org/docs/current/datatype-datetime.html#DATATYPE-TIMEZONES)\).

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq \(see [Section 33.14](https://www.postgresql.org/docs/current/libpq-envars.html)\).

## Notes

`initdb` can also be invoked via `pg_ctl initdb`.

## See Also

[pg\_ctl](https://www.postgresql.org/docs/current/app-pg-ctl.html), [postgres](https://www.postgresql.org/docs/current/app-postgres.html)

