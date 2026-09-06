## 66.1. Database File Layout [#](#STORAGE-FILE-LAYOUT)

This section describes the storage format at the level of files and
directories.

Traditionally, the configuration and data files used by a database
cluster are stored together within the cluster's data
directory, commonly referred to as `PGDATA` (after the name of the
environment variable that can be used to define it). A common location for
`PGDATA` is `/var/lib/pgsql/data`. Multiple clusters,
managed by different server instances, can exist on the same machine.

The `PGDATA` directory contains several subdirectories and control
files, as shown in [Table 66.1](storage-file-layout.md#PGDATA-CONTENTS-TABLE). In addition to
these required items, the cluster configuration files
`postgresql.conf`, `pg_hba.conf`, and
`pg_ident.conf` are traditionally stored in
`PGDATA`, although it is possible to place them elsewhere.

<a id="PGDATA-CONTENTS-TABLE"></a>

**Table 66.1. Contents of `PGDATA`**

<table border="1" class="table" summary="Contents of PGDATA"><colgroup><col/><col/></colgroup><thead><tr><th>
Item
</th><th>Description</th></tr></thead><tbody><tr><td><code class="filename">PG_VERSION</code></td><td>A file containing the major version number of <span class="productname">PostgreSQL</span></td></tr><tr><td><code class="filename">base</code></td><td>Subdirectory containing per-database subdirectories</td></tr><tr><td><code class="filename">current_logfiles</code></td><td>File recording the log file(s) currently written to by the logging
  collector</td></tr><tr><td><code class="filename">global</code></td><td>Subdirectory containing cluster-wide tables, such as
 <code class="structname">pg_database</code></td></tr><tr><td><code class="filename">pg_commit_ts</code></td><td>Subdirectory containing transaction commit timestamp data</td></tr><tr><td><code class="filename">pg_dynshmem</code></td><td>Subdirectory containing files used by the dynamic shared memory
  subsystem</td></tr><tr><td><code class="filename">pg_logical</code></td><td>Subdirectory containing status data for logical decoding</td></tr><tr><td><code class="filename">pg_multixact</code></td><td>Subdirectory containing multitransaction status data
  (used for shared row locks)</td></tr><tr><td><code class="filename">pg_notify</code></td><td>Subdirectory containing LISTEN/NOTIFY status data</td></tr><tr><td><code class="filename">pg_replslot</code></td><td>Subdirectory containing replication slot data</td></tr><tr><td><code class="filename">pg_serial</code></td><td>Subdirectory containing information about committed serializable transactions</td></tr><tr><td><code class="filename">pg_snapshots</code></td><td>Subdirectory containing exported snapshots</td></tr><tr><td><code class="filename">pg_stat</code></td><td>Subdirectory containing permanent files for the statistics
  subsystem</td></tr><tr><td><code class="filename">pg_stat_tmp</code></td><td>Subdirectory containing temporary files for the statistics
  subsystem</td></tr><tr><td><code class="filename">pg_subtrans</code></td><td>Subdirectory containing subtransaction status data</td></tr><tr><td><code class="filename">pg_tblspc</code></td><td>Subdirectory containing symbolic links to tablespaces</td></tr><tr><td><code class="filename">pg_twophase</code></td><td>Subdirectory containing state files for prepared transactions</td></tr><tr><td><code class="filename">pg_wal</code></td><td>Subdirectory containing WAL (Write Ahead Log) files</td></tr><tr><td><code class="filename">pg_xact</code></td><td>Subdirectory containing transaction commit status data</td></tr><tr><td><code class="filename">postgresql.auto.conf</code></td><td>A file used for storing configuration parameters that are set by
<code class="command">ALTER SYSTEM</code></td></tr><tr><td><code class="filename">postmaster.opts</code></td><td>A file recording the command-line options the server was
last started with</td></tr><tr><td><code class="filename">postmaster.pid</code></td><td>A lock file recording the current postmaster process ID (PID),
  cluster data directory path,
  postmaster start timestamp,
  port number,
  Unix-domain socket directory path (could be empty),
  first valid listen_address (IP address or <code class="literal">*</code>, or empty if
  not listening on TCP),
  and shared memory segment ID
  (this file is not present after server shutdown)</td></tr></tbody></table>

<br>

For each database in the cluster there is a subdirectory within
`PGDATA``/base`, named after the database's OID in
`pg_database`. This subdirectory is the default location
for the database's files; in particular, its system catalogs are stored
there.

Note that the following sections describe the behavior of the builtin
`heap` [table access method](../tableam/README.md),
and the builtin [index access methods](../indexam/README.md). Due
to the extensible nature of PostgreSQL, other
access methods might work differently.

Each table and index is stored in a separate file. For ordinary relations,
these files are named after the table or index's *filenode* number,
which can be found in `pg_class`.`relfilenode`. But
for temporary relations, the file name is of the form
`tBBB_FFF`, where *`BBB`*
is the process number of the backend which created the file, and *`FFF`*
is the filenode number. In either case, in addition to the main file (a/k/a
main fork), each table and index has a *free space map* (see [Section 66.3](storage-fsm.md)), which stores information about free space available in
the relation. The free space map is stored in a file named with the filenode
number plus the suffix `_fsm`. Tables also have a
*visibility map*, stored in a fork with the suffix `_vm`,
to track which pages are known to have no dead tuples. The visibility map is
described further in [Section 66.4](storage-vm.md). Unlogged tables and indexes
have a third fork, known as the initialization fork, which is stored in a fork
with the suffix `_init` (see [Section 66.5](storage-init.md)).

### Caution

Note that while a table's filenode often matches its OID, this is
*not* necessarily the case; some operations, like
`TRUNCATE`, `REINDEX`, `CLUSTER` and some forms
of `ALTER TABLE`, can change the filenode while preserving the OID.
Avoid assuming that filenode and table OID are the same.
Also, for certain system catalogs including `pg_class` itself,
`pg_class`.`relfilenode` contains zero. The
actual filenode number of these catalogs is stored in a lower-level data
structure, and can be obtained using the `pg_relation_filenode()`
function.

When a table or index exceeds 1 GB, it is divided into gigabyte-sized
*segments*. The first segment's file name is the same as the
filenode; subsequent segments are named filenode.1, filenode.2, etc.
This arrangement avoids problems on platforms that have file size limitations.
(Actually, 1 GB is just the default segment size. The segment size can be
adjusted using the configuration option `--with-segsize`
when building PostgreSQL.)
In principle, free space map and visibility map forks could require multiple
segments as well, though this is unlikely to happen in practice.

A table that has columns with potentially large entries will have an
associated *TOAST* table, which is used for out-of-line storage of
field values that are too large to keep in the table rows proper.
`pg_class`.`reltoastrelid` links from a table to
its TOAST table, if any.
See [Section 66.2](storage-toast.md) for more information.

The contents of tables and indexes are discussed further in
[Section 66.6](storage-page-layout.md).

Tablespaces make the scenario more complicated. Each user-defined tablespace
has a symbolic link inside the `PGDATA``/pg_tblspc`
directory, which points to the physical tablespace directory (i.e., the
location specified in the tablespace's `CREATE TABLESPACE` command).
This symbolic link is named after
the tablespace's OID. Inside the physical tablespace directory there is
a subdirectory with a name that depends on the PostgreSQL
server version, such as `PG_9.0_201008051`. (The reason for using
this subdirectory is so that successive versions of the database can use
the same `CREATE TABLESPACE` location value without conflicts.)
Within the version-specific subdirectory, there is
a subdirectory for each database that has elements in the tablespace, named
after the database's OID. Tables and indexes are stored within that
directory, using the filenode naming scheme.
The `pg_default` tablespace is not accessed through
`pg_tblspc`, but corresponds to
`PGDATA``/base`. Similarly, the `pg_global`
tablespace is not accessed through `pg_tblspc`, but corresponds to
`PGDATA``/global`.

The `pg_relation_filepath()` function shows the entire path
(relative to `PGDATA`) of any relation. It is often useful
as a substitute for remembering many of the above rules. But keep in
mind that this function just gives the name of the first segment of the
main fork of the relation — you may need to append a segment number
and/or `_fsm`, `_vm`, or `_init` to find all
the files associated with the relation.

Temporary files (for operations such as sorting more data than can fit in
memory) are created within `PGDATA``/base/pgsql_tmp`,
or within a `pgsql_tmp` subdirectory of a tablespace directory
if a tablespace other than `pg_default` is specified for them.
The name of a temporary file has the form
`pgsql_tmpPPP.NNN`,
where *`PPP`* is the PID of the owning backend and
*`NNN`* distinguishes different temporary files of that backend.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-file-layout.html)（英文原文，待翻譯）
