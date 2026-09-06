<a id="id-1.9.5.13.1"></a>

## pg_upgrade

pg_upgrade — upgrade a PostgreSQL server instance

## Synopsis

<a id="id-1.9.5.13.4.1"></a>

`pg_upgrade` `-b` *`oldbindir`* [`-B` *`newbindir`*] `-d` *`oldconfigdir`* `-D` *`newconfigdir`* [*`option`*...]

<a id="id-1.9.5.13.5"></a>

## Description

pg_upgrade (formerly called pg_migrator) allows data
stored in PostgreSQL data files to be upgraded to a later PostgreSQL
major version without the data dump/restore typically required for
major version upgrades, e.g., from 12.14 to 13.10 or from 14.9 to 15.5.
It is not required for minor version upgrades, e.g., from 12.7 to 12.8
or from 14.1 to 14.5.

Major PostgreSQL releases regularly add new features that often
change the layout of the system tables, but the internal data storage
format rarely changes. pg_upgrade uses this fact
to perform rapid upgrades by creating new system tables and simply
reusing the old user data files. If a future major release ever
changes the data storage format in a way that makes the old data
format unreadable, pg_upgrade will not be usable
for such upgrades. (The community will attempt to avoid such
situations.)

pg_upgrade does its best to
make sure the old and new clusters are binary-compatible, e.g., by
checking for compatible compile-time settings, including 32/64-bit
binaries. It is important that
any external modules are also binary compatible, though this cannot
be checked by pg_upgrade.

pg_upgrade supports upgrades from 9.2.X and later to the current
major release of PostgreSQL, including snapshot and beta releases.

### Warning

Upgrading a cluster causes the destination to execute arbitrary code of the
source superusers' choice. Ensure that the source superusers are trusted
before upgrading.

<a id="id-1.9.5.13.6"></a>

## Options

pg_upgrade accepts the following command-line arguments:

`-b` *`bindir`*<br>`--old-bindir=`*`bindir`*
:   the old PostgreSQL executable directory;
    environment variable `PGBINOLD`

`-B` *`bindir`*<br>`--new-bindir=`*`bindir`*
:   the new PostgreSQL executable directory;
    default is the directory where pg_upgrade resides;
    environment variable `PGBINNEW`

`-c`<br>`--check`
:   check clusters only, don't change any data

`-d` *`configdir`*<br>`--old-datadir=`*`configdir`*
:   the old database cluster configuration directory; environment
    variable `PGDATAOLD`

`-D` *`configdir`*<br>`--new-datadir=`*`configdir`*
:   the new database cluster configuration directory; environment
    variable `PGDATANEW`

`-j njobs`<br>`--jobs=njobs`
:   number of simultaneous connections and processes/threads to use

`-k`<br>`--link`
:   use hard links instead of copying files to the new
    cluster

`-N`<br>`--no-sync`
:   By default, `pg_upgrade` will wait for all files
    of the upgraded cluster to be written safely to disk. This option
    causes `pg_upgrade` to return without waiting, which
    is faster, but means that a subsequent operating system crash can leave
    the data directory corrupt. Generally, this option is
    useful for testing but should not be used on a production
    installation.

`-o` *`options`*<br>`--old-options` *`options`*
:   options to be passed directly to the
    old `postgres` command; multiple
    option invocations are appended

`-O` *`options`*<br>`--new-options` *`options`*
:   options to be passed directly to the
    new `postgres` command; multiple
    option invocations are appended

`-p` *`port`*<br>`--old-port=`*`port`*
:   the old cluster port number; environment
    variable `PGPORTOLD`

`-P` *`port`*<br>`--new-port=`*`port`*
:   the new cluster port number; environment
    variable `PGPORTNEW`

`-r`<br>`--retain`
:   retain SQL and log files even after successful completion

`-s` *`dir`*<br>`--socketdir=`*`dir`*
:   directory to use for postmaster sockets during upgrade;
    default is current working directory; environment
    variable `PGSOCKETDIR`

`-U` *`username`*<br>`--username=`*`username`*
:   cluster's install user name; environment
    variable `PGUSER`

`-v`<br>`--verbose`
:   enable verbose internal logging

`-V`<br>`--version`
:   display version information, then exit

`--clone`
:   Use efficient file cloning (also known as “reflinks” on
    some systems) instead of copying files to the new cluster. This can
    result in near-instantaneous copying of the data files, giving the
    speed advantages of `-k`/`--link` while
    leaving the old cluster untouched.

    File cloning is only supported on some operating systems and file
    systems. If it is selected but not supported, the
    pg_upgrade run will error. At present, it
    is supported on Linux (kernel 4.5 or later) with Btrfs and XFS (on
    file systems created with reflink support), and on macOS with APFS.

`--copy`
:   Copy files to the new cluster. This is the default. (See also
    `--link`, `--clone`,
    `--copy-file-range`, and `--swap`.)

`--copy-file-range`
:   Use the `copy_file_range` system call for efficient
    copying. On some file systems this gives results similar to
    `--clone`, sharing physical disk blocks, while on others
    it may still copy blocks, but do so via an optimized path. At present,
    it is supported on Linux and FreeBSD.

`--no-statistics`
:   Do not restore statistics from the old cluster into the new cluster.

`--set-char-signedness=`*`option`*
:   Manually set the default char signedness of new clusters. Possible values
    are `signed` and `unsigned`.

    In the C language, the default signedness of the `char` type
    (when not explicitly specified) varies across platforms. For example,
    `char` defaults to `signed char` on x86 CPUs but
    to `unsigned char` on ARM CPUs.

    Starting from PostgreSQL 18, database clusters
    maintain their own default char signedness setting, which can be used to
    ensure consistent behavior across platforms with different default char
    signedness. By default, pg_upgrade preserves
    the char signedness setting when upgrading from an existing cluster.
    However, when upgrading from PostgreSQL 17 or
    earlier, pg_upgrade adopts the char signedness
    of the platform on which it was built.

    This option allows you to explicitly set the default char signedness for
    the new cluster, overriding any inherited values. There are two specific
    scenarios where this option is relevant:

    * If you are planning to migrate to a different platform after the upgrade,
      you should not use this option. The default behavior is right in this case.
      Instead, perform the upgrade on the original platform without this flag,
      and then migrate the cluster afterward. This is the recommended and safest
      approach.
    * If you have already migrated the cluster to a platform with different
      char signedness (for example, from an x86-based system to an ARM-based
      system), you should use this option to specify the signedness matching
      the original platform's default char signedness. Additionally, it's
      essential not to modify any data files between migrating data files and
      running `pg_upgrade`. `pg_upgrade`
      should be the first operation that starts the cluster on the new platform.

`--swap`
:   Move the data directories from the old cluster to the new cluster.
    Then, replace the catalog files with those generated for the new
    cluster. This mode can outperform `--link`,
    `--clone`, `--copy`, and
    `--copy-file-range`, especially on clusters with many
    relations.

    However, this mode creates many garbage files in the old cluster, which
    can prolong the file synchronization step if
    `--sync-method=syncfs` is used. Therefore, it is
    recommended to use `--sync-method=fsync` with
    `--swap`.

    Additionally, once the file transfer step begins, the old cluster will
    be destructively modified and therefore will no longer be safe to
    start. See [Step 17](pgupgrade.md#PGUPGRADE-STEP-REVERT) for details.

`--sync-method=`*`method`*
:   When set to `fsync`, which is the default,
    `pg_upgrade` will recursively open and synchronize all
    files in the upgraded cluster's data directory. The search for files
    will follow symbolic links for the WAL directory and each configured
    tablespace.

    On Linux, `syncfs` may be used instead to ask the
    operating system to synchronize the whole file systems that contain the
    upgraded cluster's data directory, its WAL files, and each tablespace.
    See [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD) for information
    about the caveats to be aware of when using `syncfs`.

    This option has no effect when `--no-sync` is used.

`-?`<br>`--help`
:   show help, then exit

<a id="id-1.9.5.13.7"></a>

## Usage

These are the steps to perform an upgrade
with pg_upgrade:

### Note

The steps to upgrade [*[logical replication clusters](../../appendixes/glossary/README.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER)*](../../appendixes/glossary/README.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER)
are not covered here;
refer to [Section 29.13](../../server-administration/logical-replication/logical-replication-upgrade.md) for details.

1. **Optionally move the old cluster**

   If you are using a version-specific installation directory, e.g.,
   `/opt/PostgreSQL/18`, you do not need to move the old cluster. The
   graphical installers all use version-specific installation directories.

   If your installation directory is not version-specific, e.g.,
   `/usr/local/pgsql`, it is necessary to move the current PostgreSQL install
   directory so it does not interfere with the new PostgreSQL installation.
   Once the current PostgreSQL server is shut down, it is safe to rename the
   PostgreSQL installation directory; assuming the old directory is
   `/usr/local/pgsql`, you can do:

   ```

   mv /usr/local/pgsql /usr/local/pgsql.old
   ```

   to rename the directory.
2. **For source installs, build the new version**

   Build the new PostgreSQL source with `configure` flags that are compatible
   with the old cluster. pg_upgrade will check `pg_controldata` to make
   sure all settings are compatible before starting the upgrade.
3. **Install the new PostgreSQL binaries**

   Install the new server's binaries and support
   files. pg_upgrade is included in a default installation.

   For source installs, if you wish to install the new server in a custom
   location, use the `prefix` variable:

   ```

   make prefix=/usr/local/pgsql.new install
   ```
4. **Initialize the new PostgreSQL cluster**

   Initialize the new cluster using `initdb`.
   Again, use compatible `initdb`
   flags that match the old cluster. Many
   prebuilt installers do this step automatically. There is no need to
   start the new cluster.
5. **Install extension shared object files**

   Many extensions and custom modules, whether from
   `contrib` or another source, use shared object
   files (or DLLs), e.g., `pgcrypto.so`. If the old
   cluster used these, shared object files matching the new server binary
   must be installed in the new cluster, usually via operating system
   commands. Do not load the schema definitions, e.g., `CREATE
   EXTENSION pgcrypto`, because these will be duplicated from
   the old cluster. If extension updates are available,
   pg_upgrade will report this and create
   a script that can be run later to update them.
6. **Copy custom full-text search files**

   Copy any custom full text search files (dictionary, synonym,
   thesaurus, stop words) from the old to the new cluster.
7. **Adjust authentication**

   `pg_upgrade` will connect to the old and new servers several
   times, so you might want to set authentication to `peer`
   in `pg_hba.conf` or use a `~/.pgpass` file
   (see [Section 32.16](../../client-interfaces/libpq/libpq-pgpass.md)).
8. **Stop both servers**

   Make sure both database servers are stopped using, on Unix, e.g.:

   ```

   pg_ctl -D /opt/PostgreSQL/12 stop
   pg_ctl -D /opt/PostgreSQL/18 stop
   ```

   or on Windows, using the proper service names:

   ```

   NET STOP postgresql-12
   NET STOP postgresql-18
   ```

   Streaming replication and log-shipping standby servers must be
   running during this shutdown so they receive all changes.
9. **Prepare for standby server upgrades**

   If you are upgrading standby servers using methods outlined in section [Step 11](pgupgrade.md#PGUPGRADE-STEP-REPLICAS), verify that the old standby
   servers are caught up by running pg_controldata
   against the old primary and standby clusters. Verify that the
   “Latest checkpoint location” values match in all clusters.
   Also, make sure `wal_level` is not set to
   `minimal` in the `postgresql.conf` file on the
   new primary cluster.
10. **Run pg_upgrade**

    Always run the pg_upgrade binary of the new server, not the old one.
    pg_upgrade requires the specification of the old and new cluster's
    data and executable (`bin`) directories. You can also specify
    user and port values, and whether you want the data files linked, cloned, or swapped
    instead of the default copy behavior.

    If you use link mode, the upgrade will be much faster (no file
    copying) and use less disk space, but you will not be able to access
    your old cluster
    once you start the new cluster after the upgrade. Link mode also
    requires that the old and new cluster data directories be in the
    same file system. (Tablespaces and `pg_wal` can be on
    different file systems.)
    Clone mode provides the same speed and disk space advantages but
    does not cause the old cluster to be unusable once the new cluster
    is started. Clone mode also requires that the old and new data
    directories be in the same file system. This mode is only available
    on certain operating systems and file systems.
    Swap mode may be the fastest if there are many relations, but you will not
    be able to access your old cluster once the file transfer step begins.
    Swap mode also requires that the old and new cluster data directories be
    in the same file system.

    Setting `--jobs` to 2 or higher allows pg_upgrade to
    process multiple databases and tablespaces in parallel. A good starting
    point is the number of CPU cores on the machine. This option can
    substantially reduce the upgrade time for multi-database and
    multi-tablespace servers.

    For Windows users, you must be logged into an administrative account,
    and then run pg_upgrade with quoted
    directories, e.g.:

    ```

    pg_upgrade.exe
            --old-datadir "C:/Program Files/PostgreSQL/12/data"
            --new-datadir "C:/Program Files/PostgreSQL/18/data"
            --old-bindir "C:/Program Files/PostgreSQL/12/bin"
            --new-bindir "C:/Program Files/PostgreSQL/18/bin"
    ```

    Once started, `pg_upgrade` will verify the two clusters are compatible
    and then do the upgrade. You can use `pg_upgrade --check`
    to perform only the checks, even if the old server is still
    running. `pg_upgrade --check` will also outline any
    manual adjustments you will need to make after the upgrade. If you
    are going to be using link, clone, copy-file-range, or swap mode, you
    should use the option `--link`, `--clone`,
    `--copy-file-range`, or `--swap` with
    `--check` to enable mode-specific checks.
    `pg_upgrade` requires write permission in the current directory.

    Obviously, no one should be accessing the clusters during the
    upgrade. pg_upgrade defaults to running servers
    on port 50432 to avoid unintended client connections.
    You can use the same port number for both clusters when doing an
    upgrade because the old and new clusters will not be running at the
    same time. However, when checking an old running server, the old
    and new port numbers must be different.

    If an error occurs while restoring the database schema, `pg_upgrade` will
    exit and you will have to revert to the old cluster as outlined in [Step 17](pgupgrade.md#PGUPGRADE-STEP-REVERT)
    below. To try `pg_upgrade` again, you will need to modify the old
    cluster so the pg_upgrade schema restore succeeds. If the problem is a
    `contrib` module, you might need to uninstall the `contrib` module from
    the old cluster and install it in the new cluster after the upgrade,
    assuming the module is not being used to store user data.
<a id="PGUPGRADE-STEP-REPLICAS"></a>11. **Upgrade streaming replication and log-shipping standby servers**

    If you used link mode and have Streaming Replication (see [Section 26.2.5](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)) or Log-Shipping (see [Section 26.2](../../server-administration/high-availability/warm-standby.md)) standby servers, you can follow these steps to
    quickly upgrade them. You will not be running pg_upgrade on
    the standby servers, but rather rsync on the primary.
    Do not start any servers yet.

    If you did *not* use link mode, do not have or do not
    want to use rsync, or want an easier solution, skip
    the instructions in this section and simply recreate the standby
    servers once pg_upgrade completes and the new primary
    is running.

    1. **Install the new PostgreSQL binaries on standby servers**

       Make sure the new binaries and support files are installed on all
       standby servers.
    2. **Make sure the new standby data directories do *not* exist**

       Make sure the new standby data directories do *not*
       exist or are empty. If initdb was run, delete
       the standby servers' new data directories.
    3. **Install extension shared object files**

       Install the same extension shared object files on the new standbys
       that you installed in the new primary cluster.
    4. **Stop standby servers**

       If the standby servers are still running, stop them now using the
       above instructions.
    5. **Save configuration files**

       Save any configuration files from the old standbys' configuration
       directories you need to keep, e.g., `postgresql.conf`
       (and any files included by it), `postgresql.auto.conf`,
       `pg_hba.conf`, because these will be overwritten
       or removed in the next step.
    6. **Run rsync**

       When using link mode, standby servers can be quickly upgraded using
       rsync. To accomplish this, from a directory on
       the primary server that is above the old and new database cluster
       directories, run this on the *primary* for each standby
       server:

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive old_cluster new_cluster remote_dir
       ```

       where `old_cluster` and `new_cluster` are relative
       to the current directory on the primary, and `remote_dir`
       is *above* the old and new cluster directories
       on the standby. The directory structure under the specified
       directories on the primary and standbys must match. Consult the
       rsync manual page for details on specifying the
       remote directory, e.g.,

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive /opt/PostgreSQL/12 \
             /opt/PostgreSQL/18 standby.example.com:/opt/PostgreSQL
       ```

       You can verify what the command will do using
       rsync's `--dry-run` option. While
       rsync must be run on the primary for at least one
       standby, it is possible to run rsync on an upgraded
       standby to upgrade other standbys, as long as the upgraded standby
       has not been started.

       What this does is to record the links created by
       pg_upgrade's link mode that connect files in the
       old and new clusters on the primary server. It then finds matching
       files in the standby's old cluster and creates links for them in the
       standby's new cluster. Files that were not linked on the primary
       are copied from the primary to the standby. (They are usually
       small.) This provides rapid standby upgrades. Unfortunately,
       rsync needlessly copies files associated with
       temporary and unlogged tables because these files don't normally
       exist on standby servers.

       If you have tablespaces, you will need to run a similar
       rsync command for each tablespace directory, e.g.:

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive /vol1/pg_tblsp/PG_12_201909212 \
             /vol1/pg_tblsp/PG_18_202307071 standby.example.com:/vol1/pg_tblsp
       ```

       If you have relocated `pg_wal` outside the data
       directories, rsync must be run on those directories
       too.
    7. **Configure streaming replication and log-shipping standby servers**

       Configure the servers for log shipping. (You do not need to run
       `pg_backup_start()` and `pg_backup_stop()`
       or take a file system backup as the standbys are still synchronized
       with the primary.) If the old primary is prior to version 17.0, then no
       slots on the primary are copied to the new standby, so all the slots on
       the old standby must be recreated manually. If the old primary is
       version 17.0 or later, then only logical slots on the primary are copied
       to the new standby, but other slots on the old standby are not copied,
       so must be recreated manually.
12. **Restore `pg_hba.conf`**

    If you modified `pg_hba.conf`, restore its original settings.
    It might also be necessary to adjust other configuration files in the new
    cluster to match the old cluster, e.g., `postgresql.conf`
    (and any files included by it), `postgresql.auto.conf`.
13. **Start the new server**

    The new server can now be safely started, and then any
    rsync'ed standby servers.
14. **Post-upgrade processing**

    If any post-upgrade processing is required, pg_upgrade will issue
    warnings as it completes. It will also generate script files that must
    be run by the administrator. The script files will connect to each
    database that needs post-upgrade processing. Each script should be
    run using:

    ```

    psql --username=postgres --file=script.sql postgres
    ```

    The scripts can be run in any order and can be deleted once they have
    been run.

    ### Caution

    In general it is unsafe to access tables referenced in rebuild scripts
    until the rebuild scripts have run to completion; doing so could yield
    incorrect results or poor performance. Tables not referenced in rebuild
    scripts can be accessed immediately.
15. **Statistics**

    Unless the `--no-statistics` option is specified,
    `pg_upgrade` will transfer most optimizer statistics
    from the old cluster to the new cluster. This does not transfer
    all statistics, such as those created explicitly with
    [CREATE STATISTICS](../sql-commands/sql-createstatistics.md), custom statistics added by
    an extension, or statistics collected by the cumulative statistics system.

    Because not all statistics are transferred by
    `pg_upgrade`, you will be instructed to run commands to
    regenerate that information at the end of the upgrade. You might need to
    set connection parameters to match your new cluster.

    First, use
    `vacuumdb --all --analyze-in-stages --missing-stats-only`
    to quickly generate minimal optimizer statistics for relations without
    any. Then, use `vacuumdb --all --analyze-only` to ensure
    all relations have updated cumulative statistics for triggering vacuum and
    analyze. For both commands, the use of `--jobs` can speed
    it up.
    If `vacuum_cost_delay` is set to a non-zero
    value, this can be overridden to speed up statistics generation
    using `PGOPTIONS`, e.g., `PGOPTIONS='-c
    vacuum_cost_delay=0' vacuumdb ...`.
16. **Delete old cluster**

    Once you are satisfied with the upgrade, you can delete the old
    cluster's data directories by running the script mentioned when
    `pg_upgrade` completes. (Automatic deletion is not
    possible if you have user-defined tablespaces inside the old data
    directory.) You can also delete the old installation directories
    (e.g., `bin`, `share`).
<a id="PGUPGRADE-STEP-REVERT"></a>17. **Reverting to old cluster**

    If, after running `pg_upgrade`, you wish to revert to the old cluster,
    there are several options:

    * If the `--check` option was used, the old cluster
      was unmodified; it can be restarted.
    * If neither `--link` nor `--swap` was
      used, the old cluster was unmodified; it can be restarted.
    * If the `--link` option was used, the data
      files might be shared between the old and new cluster:

      * If `pg_upgrade` aborted before linking started,
        the old cluster was unmodified; it can be restarted.
      * If you did *not* start the new cluster, the old
        cluster was unmodified except that, when linking started, a
        `.old` suffix was appended to
        `$PGDATA/global/pg_control`. To reuse the old
        cluster, remove the `.old` suffix from
        `$PGDATA/global/pg_control`; you can then restart
        the old cluster.
      * If you did start the new cluster, it has written to shared files
        and it is unsafe to use the old cluster. The old cluster will
        need to be restored from backup in this case.
    * If the `--swap` option was used, the old cluster might
      be destructively modified:

      * If `pg_upgrade` aborts before reporting that the
        old cluster is no longer safe to start, the old cluster was
        unmodified; it can be restarted.
      * If `pg_upgrade` has reported that the old cluster
        is no longer safe to start, the old cluster was destructively
        modified. The old cluster will need to be restored from backup in
        this case.

<a id="id-1.9.5.13.8"></a>

## Environment

Some environment variables can be used to provide defaults for command-line options:

`PGBINOLD`
:   The old PostgreSQL executable directory; option
    `-b`/`--old-bindir`.

`PGBINNEW`
:   The new PostgreSQL executable directory; option
    `-B`/`--new-bindir`.

`PGDATAOLD`
:   The old database cluster configuration directory; option
    `-d`/`--old-datadir`.

`PGDATANEW`
:   The new database cluster configuration directory; option
    `-D`/`--new-datadir`.

`PGPORTOLD`
:   The old cluster port number; option
    `-p`/`--old-port`.

`PGPORTNEW`
:   The new cluster port number; option
    `-P`/`--new-port`.

`PGSOCKETDIR`
:   Directory to use for postmaster sockets during upgrade; option
    `-s`/`--socketdir`.

`PGUSER`
:   Cluster's install user name; option
    `-U`/`--username`.

<a id="id-1.9.5.13.9"></a>

## Notes

pg_upgrade creates various working files, such
as schema dumps, stored within `pg_upgrade_output.d` in
the directory of the new cluster. Each run creates a new subdirectory named
with a timestamp formatted as per ISO 8601
(`%Y%m%dT%H%M%S`), where all its generated files are
stored.
`pg_upgrade_output.d` and its contained files will be
removed automatically if pg_upgrade completes
successfully; but in the event of trouble, the files there may provide
useful debugging information.

pg_upgrade launches short-lived postmasters in
the old and new data directories. Temporary Unix socket files for
communication with these postmasters are, by default, made in the current
working directory. In some situations the path name for the current
directory might be too long to be a valid socket name. In that case you
can use the `-s` option to put the socket files in some
directory with a shorter path name. For security, be sure that that
directory is not readable or writable by any other users.
(This is not supported on Windows.)

All failure, rebuild, and reindex cases will be reported by
pg_upgrade if they affect your installation;
post-upgrade scripts to rebuild tables and indexes will be
generated automatically. If you are trying to automate the upgrade
of many clusters, you should find that clusters with identical database
schemas require the same post-upgrade steps for all cluster upgrades;
this is because the post-upgrade steps are based on the database
schemas, and not user data.

For deployment testing, create a schema-only copy of the old cluster,
insert dummy data, and upgrade that.

pg_upgrade does not support upgrading of databases
containing table columns using these `reg*` OID-referencing system data types:

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="type">regcollation</code></td></tr><tr><td><code class="type">regconfig</code></td></tr><tr><td><code class="type">regdictionary</code></td></tr><tr><td><code class="type">regnamespace</code></td></tr><tr><td><code class="type">regoper</code></td></tr><tr><td><code class="type">regoperator</code></td></tr><tr><td><code class="type">regproc</code></td></tr><tr><td><code class="type">regprocedure</code></td></tr></table>

(`regclass`, `regrole`, and `regtype` can be upgraded.)

If you want to use link mode and you do not want your old cluster
to be modified when the new cluster is started, consider using the clone mode.
If that is not available, make a copy of the
old cluster and upgrade that in link mode. To make a valid copy
of the old cluster, use `rsync` to create a dirty
copy of the old cluster while the server is running, then shut down
the old server and run `rsync --checksum` again to update the
copy with any changes to make it consistent. (`--checksum`
is necessary because `rsync` only has file modification-time
granularity of one second.) You might want to exclude some
files, e.g., `postmaster.pid`, as documented in [Section 25.3.4](../../server-administration/backup/continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP). If your file system supports
file system snapshots or copy-on-write file copies, you can use that
to make a backup of the old cluster and tablespaces, though the snapshot
and copies must be created simultaneously or while the database server
is down.

<a id="id-1.9.5.13.10"></a>

## See Also

[initdb](app-initdb.md), [pg_ctl](app-pg-ctl.md), [pg_dump](../reference-client/app-pgdump.md), [postgres](app-postgres.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgupgrade.html)（英文原文，待翻譯）
