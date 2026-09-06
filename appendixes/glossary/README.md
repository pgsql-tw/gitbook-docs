## Appendix M. Glossary

This is a list of terms and their meaning in the context of
PostgreSQL and relational database
systems in general.

<a id="GLOSSARY-ACID"></a>

ACID
:   [*[Atomicity](README.md#GLOSSARY-ATOMICITY)*](README.md#GLOSSARY-ATOMICITY),
    [*[Consistency](README.md#GLOSSARY-CONSISTENCY)*](README.md#GLOSSARY-CONSISTENCY),
    [*[Isolation](README.md#GLOSSARY-ISOLATION)*](README.md#GLOSSARY-ISOLATION), and
    [*[Durability](README.md#GLOSSARY-DURABILITY)*](README.md#GLOSSARY-DURABILITY).
    This set of properties of database transactions is intended to
    guarantee validity in concurrent operation and even in event of
    errors, power failures, etc.
<a id="GLOSSARY-AGGREGATE"></a>

Aggregate function (routine)
:   A [*[function](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION) that
    combines (*aggregates*) multiple input values,
    for example by counting, averaging or adding,
    yielding a single output value.

    For more information, see
    [Section 9.21](../../the-sql-language/functions/functions-aggregate.md).

    See Also [Window function (routine)](README.md#GLOSSARY-WINDOW-FUNCTION).
<a id="GLOSSARY-AM"></a>

Access Method
:   Interfaces which PostgreSQL use in order to
    access data in tables and indexes. This abstraction allows for adding
    support for new types of data storage.

    For more information, see [Chapter 62](../../internals/tableam/README.md) and
    [Chapter 63](../../internals/indexam/README.md).

Analytic function
:   See [Window function (routine)](README.md#GLOSSARY-WINDOW-FUNCTION).
<a id="GLOSSARY-ANALYZE"></a>

Analyze (operation)
:   The act of collecting statistics from data in
    [*[tables](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE)
    and other [*[relations](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION)
    to help the [*[query planner](README.md#GLOSSARY-PLANNER)*](README.md#GLOSSARY-PLANNER)
    to make decisions about how to execute
    [*[queries](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY).

    (Don't confuse this term with the `ANALYZE` option
    to the [EXPLAIN](../../reference/sql-commands/sql-explain.md) command.)

    For more information, see
    [ANALYZE](../../reference/sql-commands/sql-analyze.md).
<a id="GLOSSARY-AIO"></a>

Asynchronous I/O (AIO)<a id="id-1.11.14.3.6.3"></a>
:   Asynchronous I/O (AIO) describes
    performing I/O in a non-blocking way (asynchronously),
    in contrast to synchronous I/O, which blocks for the
    entire duration of the I/O.

    With AIO, starting an I/O operation
    is separated from waiting for the result of the operation, allowing
    multiple I/O operations to be initiated concurrently,
    as well as performing CPU heavy operations
    concurrently with I/O. The price for that increased
    concurrency is increased complexity.

    See Also [Input/Output](README.md#GLOSSARY-IO).
<a id="GLOSSARY-ATOMIC"></a>

Atomic
:   In reference to a [*[datum](README.md#GLOSSARY-DATUM)*](README.md#GLOSSARY-DATUM):
    the fact that its value cannot be broken down into smaller
    components.
:   In reference to a
    [*[database transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION):
    see [*[atomicity](README.md#GLOSSARY-ATOMICITY)*](README.md#GLOSSARY-ATOMICITY).
<a id="GLOSSARY-ATOMICITY"></a>

Atomicity
:   The property of a [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION)
    that either all its operations complete as a single unit or none do.
    In addition, if a system failure occurs during the execution of a
    transaction, no partial results are visible after recovery.
    This is one of the ACID properties.
<a id="GLOSSARY-ATTRIBUTE"></a>

Attribute
:   An element with a certain name and data type found within a
    [*[tuple](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE).
<a id="GLOSSARY-AUTOVACUUM"></a>

Autovacuum (process)
:   A set of background processes that routinely perform
    [*[vacuum](README.md#GLOSSARY-VACUUM)*](README.md#GLOSSARY-VACUUM)
    and [*[analyze](README.md#GLOSSARY-ANALYZE)*](README.md#GLOSSARY-ANALYZE) operations.
    The [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that coordinates the work and is always present (unless autovacuum
    is disabled) is known as the *autovacuum launcher*,
    and the processes that carry out the tasks are known as the
    *autovacuum workers*.

    For more information, see
    [Section 24.1.6](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM).
<a id="GLOSSARY-AUXILIARY-PROC"></a>

Auxiliary process
:   A process within an [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE)
    that is in charge of some specific background task for the instance.
    The auxiliary processes consist of
    the [*[autovacuum launcher](README.md#GLOSSARY-AUTOVACUUM)*](README.md#GLOSSARY-AUTOVACUUM)
    (but not the autovacuum workers),
    the [*[background writer](README.md#GLOSSARY-BACKGROUND-WRITER)*](README.md#GLOSSARY-BACKGROUND-WRITER),
    the [*[checkpointer](README.md#GLOSSARY-CHECKPOINTER)*](README.md#GLOSSARY-CHECKPOINTER),
    the [*[logger](README.md#GLOSSARY-LOGGER)*](README.md#GLOSSARY-LOGGER),
    the [*[startup process](README.md#GLOSSARY-STARTUP-PROCESS)*](README.md#GLOSSARY-STARTUP-PROCESS),
    the [*[WAL archiver](README.md#GLOSSARY-WAL-ARCHIVER)*](README.md#GLOSSARY-WAL-ARCHIVER),
    the [*[WAL receiver](README.md#GLOSSARY-WAL-RECEIVER)*](README.md#GLOSSARY-WAL-RECEIVER)
    (but not the [*[WAL senders](README.md#GLOSSARY-WAL-SENDER)*](README.md#GLOSSARY-WAL-SENDER)),
    the [*[WAL summarizer](README.md#GLOSSARY-WAL-SUMMARIZER)*](README.md#GLOSSARY-WAL-SUMMARIZER),
    and the [*[WAL writer](README.md#GLOSSARY-WAL-WRITER)*](README.md#GLOSSARY-WAL-WRITER).
<a id="GLOSSARY-BACKEND"></a>

Backend (process)
:   Process of an [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE)
    which acts on behalf of a [*[client session](README.md#GLOSSARY-SESSION)*](README.md#GLOSSARY-SESSION)
    and handles its requests.

    (Don't confuse this term with the similar terms
    [*[Background Worker](README.md#GLOSSARY-BACKGROUND-WORKER)*](README.md#GLOSSARY-BACKGROUND-WORKER) or
    [*[Background Writer](README.md#GLOSSARY-BACKGROUND-WRITER)*](README.md#GLOSSARY-BACKGROUND-WRITER)).
<a id="GLOSSARY-BACKGROUND-WORKER"></a>

Background worker (process)
:   Process within an [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE),
    which runs system- or user-supplied code.
    Serves as infrastructure for several features in
    PostgreSQL, such as
    [*[logical replication](README.md#GLOSSARY-REPLICATION)*](README.md#GLOSSARY-REPLICATION)
    and [*[parallel queries](README.md#GLOSSARY-PARALLEL-QUERY)*](README.md#GLOSSARY-PARALLEL-QUERY).
    In addition, [*[Extensions](README.md#GLOSSARY-EXTENSION)*](README.md#GLOSSARY-EXTENSION) can add
    custom background worker processes.

    For more information, see
    [Chapter 46](../../server-programming/bgworker/README.md).
<a id="GLOSSARY-BACKGROUND-WRITER"></a>

Background writer (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that writes dirty
    [*[data pages](README.md#GLOSSARY-DATA-PAGE)*](README.md#GLOSSARY-DATA-PAGE) from
    [*[shared memory](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY) to
    the file system. It wakes up periodically, but works only for a short
    period in order to distribute its expensive I/O
    activity over time to avoid generating larger
    I/O peaks which could block other processes.

    For more information, see
    [Section 19.4.4](../../server-administration/runtime-config/runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER).
<a id="GLOSSARY-BASEBACKUP"></a>

Base Backup
:   A binary copy of all
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER)
    files. It is generated by the tool [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md).
    In combination with WAL files it can be used as the starting point
    for recovery, log shipping, or streaming replication.
<a id="GLOSSARY-BLOAT"></a>

Bloat
:   Space in data pages which does not contain current row versions,
    such as unused (free) space or outdated row versions.
<a id="GLOSSARY-BOOTSTRAP-SUPERUSER"></a>

Bootstrap superuser
:   The first [*[user](README.md#GLOSSARY-USER)*](README.md#GLOSSARY-USER) initialized in a
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER).

    This user owns all system catalog tables in each database. It is also the role
    from which all granted permissions originate. Because of these things, this
    role may not be dropped.

    This role also behaves as a normal
    [*[database superuser](README.md#GLOSSARY-DATABASE-SUPERUSER)*](README.md#GLOSSARY-DATABASE-SUPERUSER),
    and its superuser status cannot be removed.
<a id="GLOSSARY-BUFFER-ACCESS-STRATEGY"></a>

Buffer Access Strategy
:   Some operations will access a large number of
    [*[pages](README.md#GLOSSARY-DATA-PAGE)*](README.md#GLOSSARY-DATA-PAGE). A
    *Buffer Access Strategy* helps to prevent these
    operations from evicting too many pages from
    [*[shared buffers](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY).

    A Buffer Access Strategy sets up references to a limited number of
    [*[shared buffers](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY) and
    reuses them circularly. When the operation requires a new page, a victim
    buffer is chosen from the buffers in the strategy ring, which may require
    flushing the page's dirty data and possibly also unflushed
    [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL) to permanent storage.

    Buffer Access Strategies are used for various operations such as
    sequential scans of large tables, `VACUUM`,
    `COPY`, `CREATE TABLE AS SELECT`,
    `ALTER TABLE`, `CREATE DATABASE`,
    `CREATE INDEX`, and `CLUSTER`.
<a id="GLOSSARY-CAST"></a>

Cast
:   A conversion of a [*[datum](README.md#GLOSSARY-DATUM)*](README.md#GLOSSARY-DATUM)
    from its current data type to another data type.

    For more information, see
    [CREATE CAST](../../reference/sql-commands/sql-createcast.md).
<a id="GLOSSARY-CATALOG"></a>

Catalog
:   The SQL standard uses this term to
    indicate what is called a
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) in
    PostgreSQL's terminology.

    (Don't confuse this term with
    [*[system catalog](README.md#GLOSSARY-SYSTEM-CATALOG)*](README.md#GLOSSARY-SYSTEM-CATALOG)).

    For more information, see
    [Section 22.1](../../server-administration/managing-databases/manage-ag-overview.md).
<a id="GLOSSARY-CHECK-CONSTRAINT"></a>

Check constraint
:   A type of [*[constraint](README.md#GLOSSARY-CONSTRAINT)*](README.md#GLOSSARY-CONSTRAINT)
    defined on a [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION)
    which restricts the values allowed in one or more
    [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE). The
    check constraint can make reference to any attribute of the same row in
    the relation, but cannot reference other rows of the same relation or
    other relations.

    For more information, see
    [Section 5.5](../../the-sql-language/ddl/ddl-constraints.md).
<a id="GLOSSARY-CHECKPOINT"></a>

Checkpoint
:   A point in the [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL) sequence
    at which it is guaranteed that the heap and index data files have been
    updated with all information from
    [*[shared memory](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY)
    modified before that checkpoint;
    a *checkpoint record* is written and flushed to WAL
    to mark that point.

    A checkpoint is also the act of carrying out all the actions that
    are necessary to reach a checkpoint as defined above.
    This process is initiated when predefined conditions are met,
    such as a specified amount of time has passed, or a certain volume
    of records has been written; or it can be invoked by the user
    with the command `CHECKPOINT`.

    For more information, see
    [Section 28.5](../../server-administration/wal/wal-configuration.md).
<a id="GLOSSARY-CHECKPOINTER"></a>

Checkpointer (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that is responsible for executing
    [*[checkpoints](README.md#GLOSSARY-CHECKPOINT)*](README.md#GLOSSARY-CHECKPOINT).

Class (archaic)
:   See [Relation](README.md#GLOSSARY-RELATION).
<a id="GLOSSARY-CLIENT"></a>

Client (process)
:   Any process, possibly remote, that establishes a
    [*[session](README.md#GLOSSARY-SESSION)*](README.md#GLOSSARY-SESSION)
    by [*[connecting](README.md#GLOSSARY-CONNECTION)*](README.md#GLOSSARY-CONNECTION) to an
    [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE)
    to interact with a [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE).
<a id="GLOSSARY-CLUSTER-OWNER"></a>

Cluster owner
:   The operating system user that owns the
    [*[data directory](README.md#GLOSSARY-DATA-DIRECTORY)*](README.md#GLOSSARY-DATA-DIRECTORY)
    and under which the `postgres` process is run.
    It is required that this user exist prior to creating a new
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER).

    On operating systems with a `root` user,
    said user is not allowed to be the cluster owner.
<a id="GLOSSARY-COLUMN"></a>

Column
:   An [*[attribute](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE) found in
    a [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) or
    [*[view](README.md#GLOSSARY-VIEW)*](README.md#GLOSSARY-VIEW).
<a id="GLOSSARY-COMMIT"></a>

Commit
:   The act of finalizing a
    [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION) within
    the [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE), which
    makes it visible to other transactions and assures its
    [*[durability](README.md#GLOSSARY-DURABILITY)*](README.md#GLOSSARY-DURABILITY).

    For more information, see
    [COMMIT](../../reference/sql-commands/sql-commit.md).
<a id="GLOSSARY-CONCURRENCY"></a>

Concurrency
:   The concept that multiple independent operations happen within the
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) at the same time.
    In PostgreSQL, concurrency is controlled by
    the [*[multiversion concurrency control](README.md#GLOSSARY-MVCC)*](README.md#GLOSSARY-MVCC)
    mechanism.
<a id="GLOSSARY-CONNECTION"></a>

Connection
:   An established line of communication between a client process and a
    [*[backend](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND) process,
    usually over a network, supporting a
    [*[session](README.md#GLOSSARY-SESSION)*](README.md#GLOSSARY-SESSION). This term is
    sometimes used as a synonym for session.

    For more information, see
    [Section 19.3](../../server-administration/runtime-config/runtime-config-connection.md).
<a id="GLOSSARY-CONSISTENCY"></a>

Consistency
:   The property that the data in the
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE)
    is always in compliance with
    [*[integrity constraints](README.md#GLOSSARY-CONSTRAINT)*](README.md#GLOSSARY-CONSTRAINT).
    Transactions may be allowed to violate some of the constraints
    transiently before it commits, but if such violations are not resolved
    by the time it commits, such a transaction is automatically
    [*[rolled back](README.md#GLOSSARY-ROLLBACK)*](README.md#GLOSSARY-ROLLBACK).
    This is one of the ACID properties.
<a id="GLOSSARY-CONSTRAINT"></a>

Constraint
:   A restriction on the values of data allowed within a
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE),
    or in attributes of a
    [*[domain](README.md#GLOSSARY-DOMAIN)*](README.md#GLOSSARY-DOMAIN).

    For more information, see
    [Section 5.5](../../the-sql-language/ddl/ddl-constraints.md).
<a id="GLOSSARY-CUMULATIVE-STATISTICS"></a>

Cumulative Statistics System
:   A system which, if enabled, accumulates statistical information
    about the [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE)'s
    activities.

    For more information, see
    [Section 27.2](../../server-administration/monitoring/monitoring-stats.md).

Data area
:   See [Data directory](README.md#GLOSSARY-DATA-DIRECTORY).
<a id="GLOSSARY-DATABASE"></a>

Database
:   A named collection of
    [*[local SQL objects](README.md#GLOSSARY-SQL-OBJECT)*](README.md#GLOSSARY-SQL-OBJECT).

    For more information, see
    [Section 22.1](../../server-administration/managing-databases/manage-ag-overview.md).
<a id="GLOSSARY-DB-CLUSTER"></a>

Database cluster
:   A collection of databases and global SQL objects,
    and their common static and dynamic metadata.
    Sometimes referred to as a
    *cluster*.
    A database cluster is created using the
    [initdb](../../reference/reference-server/app-initdb.md) program.

    In PostgreSQL, the term
    *cluster* is also sometimes used to refer to an instance.
    (Don't confuse this term with the SQL command `CLUSTER`.)

    See also [*[cluster owner](README.md#GLOSSARY-CLUSTER-OWNER)*](README.md#GLOSSARY-CLUSTER-OWNER),
    the operating-system owner of a cluster,
    and [*[bootstrap superuser](README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)*](README.md#GLOSSARY-BOOTSTRAP-SUPERUSER),
    the PostgreSQL owner of a cluster.

Database server
:   See [Instance](README.md#GLOSSARY-INSTANCE).
<a id="GLOSSARY-DATABASE-SUPERUSER"></a>

Database superuser
:   A role having *superuser status*
    (see [Section 21.2](../../server-administration/user-manag/role-attributes.md)).

    Frequently referred to as *superuser*.
<a id="GLOSSARY-DATA-DIRECTORY"></a>

Data directory
:   The base directory on the file system of a
    [*[server](README.md#GLOSSARY-SERVER)*](README.md#GLOSSARY-SERVER) that contains all
    data files and subdirectories associated with a
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER)
    (with the exception of
    [*[tablespaces](README.md#GLOSSARY-TABLESPACE)*](README.md#GLOSSARY-TABLESPACE),
    and optionally [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL)).
    The environment variable `PGDATA` is commonly used to
    refer to the data directory.

    A [*[cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER)'s storage
    space comprises the data directory plus any additional tablespaces.

    For more information, see
    [Section 66.1](../../internals/storage/storage-file-layout.md).
<a id="GLOSSARY-DATA-PAGE"></a>

Data page
:   The basic structure used to store relation data.
    All pages are of the same size.
    Data pages are typically stored on disk, each in a specific file,
    and can be read to [*[shared buffers](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY)
    where they can be modified, becoming
    *dirty*. They become clean when written
    to disk. New pages, which initially exist in memory only, are also
    dirty until written.
<a id="GLOSSARY-DATUM"></a>

Datum
:   The internal representation of one value of an SQL
    data type.
<a id="GLOSSARY-DELETE"></a>

Delete
:   An SQL command which removes
    [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) from a given
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE)
    or [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).

    For more information, see
    [DELETE](../../reference/sql-commands/sql-delete.md).
<a id="GLOSSARY-DOMAIN"></a>

Domain
:   A user-defined data type that is based on another underlying data type.
    It acts the same as the underlying type except for possibly restricting
    the set of allowed values.

    For more information, see [Section 8.18](../../the-sql-language/datatype/domains.md).
<a id="GLOSSARY-DURABILITY"></a>

Durability
:   The assurance that once a
    [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION) has
    been [*[committed](README.md#GLOSSARY-COMMIT)*](README.md#GLOSSARY-COMMIT), the
    changes remain even after a system failure or crash.
    This is one of the ACID properties.

Epoch
:   See [Transaction ID](README.md#GLOSSARY-XID).
<a id="GLOSSARY-EXTENSION"></a>

Extension
:   A software add-on package that can be installed on an
    [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE) to
    get extra features.

    For more information, see
    [Section 36.17](../../server-programming/extend/extend-extensions.md).
<a id="GLOSSARY-FILE-SEGMENT"></a>

File segment
:   A physical file which stores data for a given
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).
    File segments are limited in size by a configuration value
    (typically 1 gigabyte),
    so if a relation exceeds that size, it is split into multiple segments.

    For more information, see
    [Section 66.1](../../internals/storage/storage-file-layout.md).

    (Don't confuse this term with the similar term
    [*[WAL segment](README.md#GLOSSARY-WAL-FILE)*](README.md#GLOSSARY-WAL-FILE)).
<a id="GLOSSARY-FOREIGN-DATA-WRAPPER"></a>

Foreign data wrapper
:   A means of representing data that is not contained in the local
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) so that it appears as if were in local
    [*[table(s)](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE). With a foreign data wrapper it is
    possible to define a [*[foreign server](README.md#GLOSSARY-FOREIGN-SERVER)*](README.md#GLOSSARY-FOREIGN-SERVER) and
    [*[foreign tables](README.md#GLOSSARY-FOREIGN-TABLE)*](README.md#GLOSSARY-FOREIGN-TABLE).

    For more information, see
    [CREATE FOREIGN DATA WRAPPER](../../reference/sql-commands/sql-createforeigndatawrapper.md).
<a id="GLOSSARY-FOREIGN-KEY"></a>

Foreign key
:   A type of [*[constraint](README.md#GLOSSARY-CONSTRAINT)*](README.md#GLOSSARY-CONSTRAINT)
    defined on one or more [*[columns](README.md#GLOSSARY-COLUMN)*](README.md#GLOSSARY-COLUMN)
    in a [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) which
    requires the value(s) in those [*[columns](README.md#GLOSSARY-COLUMN)*](README.md#GLOSSARY-COLUMN) to
    identify zero or one [*[row](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    in another (or, infrequently, the same)
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE).
<a id="GLOSSARY-FOREIGN-SERVER"></a>

Foreign server
:   A named collection of
    [*[foreign tables](README.md#GLOSSARY-FOREIGN-TABLE)*](README.md#GLOSSARY-FOREIGN-TABLE) which
    all use the same
    [*[foreign data wrapper](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER)*](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER)
    and have other configuration values in common.

    For more information, see
    [CREATE SERVER](../../reference/sql-commands/sql-createserver.md).
<a id="GLOSSARY-FOREIGN-TABLE"></a>

Foreign table (relation)
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) which appears to have
    [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) and
    [*[columns](README.md#GLOSSARY-COLUMN)*](README.md#GLOSSARY-COLUMN) similar to a
    regular [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE), but will forward
    requests for data through its
    [*[foreign data wrapper](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER)*](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER),
    which will return [*[result sets](README.md#GLOSSARY-RESULT-SET)*](README.md#GLOSSARY-RESULT-SET)
    structured according to the definition of the
    [*[foreign table](README.md#GLOSSARY-FOREIGN-TABLE)*](README.md#GLOSSARY-FOREIGN-TABLE).

    For more information, see
    [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md).
<a id="GLOSSARY-FORK"></a>

Fork
:   Each of the separate segmented file sets in which a relation is stored.
    The *main fork* is where the actual data resides.
    There also exist two secondary forks for metadata:
    the [*[free space map](README.md#GLOSSARY-FSM)*](README.md#GLOSSARY-FSM)
    and the [*[visibility map](README.md#GLOSSARY-VM)*](README.md#GLOSSARY-VM).
    [*[Unlogged relations](README.md#GLOSSARY-UNLOGGED)*](README.md#GLOSSARY-UNLOGGED)
    also have an *init fork*.
<a id="GLOSSARY-FSM"></a>

Free space map (fork)
:   A storage structure that keeps metadata about each data page of a table's
    main fork. The free space map entry for each page stores the
    amount of free space that's available for future tuples, and is structured
    to be efficiently searched for available space for a new tuple of a given
    size.

    For more information, see
    [Section 66.3](../../internals/storage/storage-fsm.md).
<a id="GLOSSARY-FUNCTION"></a>

Function (routine)
:   A type of routine that receives zero or more arguments, returns zero or more
    output values, and is constrained to run within one transaction.
    Functions are invoked as part of a query, for example via
    `SELECT`.
    Certain functions can return
    [*[sets](README.md#GLOSSARY-RESULT-SET)*](README.md#GLOSSARY-RESULT-SET); those are
    called *set-returning functions*.

    Functions can also be used for
    [*[triggers](README.md#GLOSSARY-TRIGGER)*](README.md#GLOSSARY-TRIGGER) to invoke.

    For more information, see
    [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md).

GMT
:   See [UTC](README.md#GLOSSARY-UTC).
<a id="GLOSSARY-GRANT"></a>

Grant
:   An SQL command that is used to allow a
    [*[user](README.md#GLOSSARY-USER)*](README.md#GLOSSARY-USER) or
    [*[role](README.md#GLOSSARY-ROLE)*](README.md#GLOSSARY-ROLE) to access
    specific objects within the [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE).

    For more information, see
    [GRANT](../../reference/sql-commands/sql-grant.md).
<a id="GLOSSARY-HEAP"></a>

Heap
:   Contains the values of [*[row](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    attributes (i.e., the data) for a
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).
    The heap is realized within one or more
    [*[file segments](README.md#GLOSSARY-FILE-SEGMENT)*](README.md#GLOSSARY-FILE-SEGMENT)
    in the relation's [*[main fork](README.md#GLOSSARY-FORK)*](README.md#GLOSSARY-FORK).
<a id="GLOSSARY-HOST"></a>

Host
:   A computer that communicates with other computers over a network.
    This is sometimes used as a synonym for
    [*[server](README.md#GLOSSARY-SERVER)*](README.md#GLOSSARY-SERVER).
    It is also used to refer to a computer where
    [*[client processes](README.md#GLOSSARY-CLIENT)*](README.md#GLOSSARY-CLIENT) run.
<a id="GLOSSARY-INDEX"></a>

Index (relation)
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) that contains
    data derived from a [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE)
    or [*[materialized view](README.md#GLOSSARY-MATERIALIZED-VIEW)*](README.md#GLOSSARY-MATERIALIZED-VIEW).
    Its internal structure supports fast retrieval of and access to the original
    data.

    For more information, see
    [CREATE INDEX](../../reference/sql-commands/sql-createindex.md).
<a id="GLOSSARY-INCREMENTAL-BACKUP"></a>

Incremental backup
:   A special [*[base backup](README.md#GLOSSARY-BASEBACKUP)*](README.md#GLOSSARY-BASEBACKUP)
    that for some files may contain only those pages that were modified since
    a previous backup, as opposed to the full contents of every file. Like
    base backups, it is generated by the tool [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md).

    To restore incremental backups the tool [pg_combinebackup](../../reference/reference-client/app-pgcombinebackup.md)
    is used, which combines incremental backups with a base backup.
    Afterwards, recovery can use
    [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL) to bring the
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER) to
    a consistent state.

    For more information, see [Section 25.3.3](../../server-administration/backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP).
<a id="GLOSSARY-IO"></a>

Input/Output (I/O)
:   Input/Output (I/O) describes the communication between
    a program and peripheral devices. In the context of database systems,
    I/O commonly, but not exclusively, refers to
    interaction with storage devices or the network.

    See Also [Asynchronous I/O](README.md#GLOSSARY-AIO).
<a id="GLOSSARY-INSERT"></a>

Insert
:   An SQL command used to add new data into a
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE).

    For more information, see
    [INSERT](../../reference/sql-commands/sql-insert.md).
<a id="GLOSSARY-INSTANCE"></a>

Instance
:   A group of [*[backend](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND) and
    [*[auxiliary processes](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that communicate using a common shared memory area. One
    [*[postmaster process](README.md#GLOSSARY-POSTMASTER)*](README.md#GLOSSARY-POSTMASTER)
    manages the instance; one instance manages exactly one
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER)
    with all its databases. Many instances can run on the same
    [*[server](README.md#GLOSSARY-SERVER)*](README.md#GLOSSARY-SERVER)
    as long as their TCP ports do not conflict.

    The instance handles all key features of a DBMS:
    read and write access to files and shared memory,
    assurance of the ACID properties,
    [*[connections](README.md#GLOSSARY-CONNECTION)*](README.md#GLOSSARY-CONNECTION) to
    [*[client processes](README.md#GLOSSARY-CLIENT)*](README.md#GLOSSARY-CLIENT),
    privilege verification, crash recovery, replication, etc.
<a id="GLOSSARY-ISOLATION"></a>

Isolation
:   The property that the effects of a transaction are not visible to
    [*[concurrent transactions](README.md#GLOSSARY-CONCURRENCY)*](README.md#GLOSSARY-CONCURRENCY)
    before it commits.
    This is one of the ACID properties.

    For more information, see [Section 13.2](../../the-sql-language/mvcc/transaction-iso.md).
<a id="GLOSSARY-JOIN"></a>

Join
:   An operation and SQL keyword used in
    [*[queries](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY)
    for combining data from multiple
    [*[relations](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).
<a id="GLOSSARY-KEY"></a>

Key
:   A means of identifying a [*[row](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) within a
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) or
    other [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) by
    values contained within one or more
    [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE)
    in that relation.
<a id="GLOSSARY-LOCK"></a>

Lock
:   A mechanism that allows a process to limit or prevent simultaneous
    access to a resource.
<a id="GLOSSARY-LOG-FILE"></a>

Log file
:   Log files contain human-readable text lines about events.
    Examples include login failures, long-running queries, etc.

    For more information, see
    [Section 24.3](../../server-administration/maintenance/logfile-maintenance.md).
<a id="GLOSSARY-LOGGED"></a>

Logged
:   A [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) is considered
    [*[logged](README.md#GLOSSARY-LOGGED)*](README.md#GLOSSARY-LOGGED) if changes to it are sent to the
    [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL). By default, all regular
    tables are logged. A table can be specified as
    [*[unlogged](README.md#GLOSSARY-UNLOGGED)*](README.md#GLOSSARY-UNLOGGED) either at
    creation time or via the `ALTER TABLE` command.
<a id="GLOSSARY-LOGGER"></a>

Logger (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    which, if enabled, writes information about database events into the current
    [*[log file](README.md#GLOSSARY-LOG-FILE)*](README.md#GLOSSARY-LOG-FILE).
    When reaching certain time- or
    volume-dependent criteria, a new log file is created.
    Also called *syslogger*.

    For more information, see
    [Section 19.8](../../server-administration/runtime-config/runtime-config-logging.md).
<a id="GLOSSARY-LOGICAL-REPLICATION-CLUSTER"></a>

Logical replication cluster
:   A set of publisher and subscriber instances with the publisher instance
    replicating changes to the subscriber instance.
<a id="GLOSSARY-LOG-RECORD"></a>

Log record
:   Archaic term for a [*[WAL record](README.md#GLOSSARY-WAL-RECORD)*](README.md#GLOSSARY-WAL-RECORD).
<a id="GLOSSARY-LOG-SEQUENCE-NUMBER"></a>

Log sequence number (LSN)
:   Byte offset into the [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL),
    increasing monotonically with each new [*[WAL record](README.md#GLOSSARY-WAL-RECORD)*](README.md#GLOSSARY-WAL-RECORD).

    For more information, see [`pg_lsn`](../../the-sql-language/datatype/datatype-pg-lsn.md) and [Section 28.6](../../server-administration/wal/wal-internals.md).

LSN
:   See [Log sequence number](README.md#GLOSSARY-LOG-SEQUENCE-NUMBER).

Master (server)
:   See [Primary (server)](README.md#GLOSSARY-PRIMARY-SERVER).
<a id="GLOSSARY-MATERIALIZED"></a>

Materialized
:   The property that some information has been pre-computed and stored
    for later use, rather than computing it on-the-fly.

    This term is used in
    [*[materialized view](README.md#GLOSSARY-MATERIALIZED-VIEW)*](README.md#GLOSSARY-MATERIALIZED-VIEW),
    to mean that the data derived from the view's query is stored on
    disk separately from the sources of that data.

    This term is also used to refer to some multi-step queries to mean that
    the data resulting from executing a given step is stored in memory
    (with the possibility of spilling to disk), so that it can be read multiple
    times by another step.
<a id="GLOSSARY-MATERIALIZED-VIEW"></a>

Materialized view (relation)
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) that is
    defined by a `SELECT` statement
    (just like a [*[view](README.md#GLOSSARY-VIEW)*](README.md#GLOSSARY-VIEW)),
    but stores data in the same way that a
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) does. It cannot be
    modified via `INSERT`, `UPDATE`,
    `DELETE`, or `MERGE` operations.

    For more information, see
    [CREATE MATERIALIZED VIEW](../../reference/sql-commands/sql-creatematerializedview.md).
<a id="GLOSSARY-MERGE"></a>

Merge
:   An SQL command used to conditionally add, modify,
    or remove [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    in a given [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE),
    using data from a source
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).

    For more information, see
    [MERGE](../../reference/sql-commands/sql-merge.md).
<a id="GLOSSARY-MVCC"></a>

Multi-version concurrency control (MVCC)
:   A mechanism designed to allow several
    [*[transactions](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION) to be
    reading and writing the same rows without one process causing other
    processes to stall.
    In PostgreSQL, MVCC is implemented by
    creating copies (*versions*) of
    [*[tuples](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) as they are
    modified; after transactions that can see the old versions terminate,
    those old versions need to be removed.
<a id="GLOSSARY-NULL"></a>

Null
:   A concept of non-existence that is a central tenet of relational
    database theory. It represents the absence of a definite value.

Optimizer
:   See [Query planner](README.md#GLOSSARY-PLANNER).
<a id="GLOSSARY-PARALLEL-QUERY"></a>

Parallel query
:   The ability to handle parts of executing a
    [*[query](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY) to take advantage
    of parallel processes on servers with multiple CPUs.
<a id="GLOSSARY-PARTITION"></a>

Partition
:   One of several disjoint (not overlapping) subsets of a larger set.
:   In reference to a
    [*[partitioned table](README.md#GLOSSARY-PARTITIONED-TABLE)*](README.md#GLOSSARY-PARTITIONED-TABLE):
    One of the tables that each contain part of the data of the partitioned table,
    which is said to be the *parent*.
    The partition is itself a table, so it can also be queried directly;
    at the same time, a partition can sometimes be a partitioned table,
    allowing hierarchies to be created.
:   In reference to a [*[window function](README.md#GLOSSARY-WINDOW-FUNCTION)*](README.md#GLOSSARY-WINDOW-FUNCTION)
    in a [*[query](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY),
    a partition is a user-defined criterion that identifies which neighboring
    [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    of the [*[query's result set](README.md#GLOSSARY-RESULT-SET)*](README.md#GLOSSARY-RESULT-SET)
    can be considered by the function.
<a id="GLOSSARY-PARTITIONED-TABLE"></a>

Partitioned table (relation)
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) that is
    in semantic terms the same as a [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE),
    but whose storage is distributed across several
    [*[partitions](README.md#GLOSSARY-PARTITION)*](README.md#GLOSSARY-PARTITION).
<a id="GLOSSARY-POSTMASTER"></a>

Postmaster (process)
:   The very first process of an [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE).
    It starts and manages the
    [*[auxiliary processes](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    and creates [*[backend processes](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND)
    on demand.

    For more information, see
    [Section 18.3](../../server-administration/runtime/server-start.md).
<a id="GLOSSARY-PRIMARY-KEY"></a>

Primary key
:   A special case of a
    [*[unique constraint](README.md#GLOSSARY-UNIQUE-CONSTRAINT)*](README.md#GLOSSARY-UNIQUE-CONSTRAINT)
    defined on a
    [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) or other
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) that also
    guarantees that all of the
    [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE)
    within the [*[primary key](README.md#GLOSSARY-PRIMARY-KEY)*](README.md#GLOSSARY-PRIMARY-KEY)
    do not have [*[null](README.md#GLOSSARY-NULL)*](README.md#GLOSSARY-NULL) values.
    As the name implies, there can be only one
    primary key per table, though it is possible to have multiple unique
    constraints that also have no null-capable attributes.
<a id="GLOSSARY-PRIMARY-SERVER"></a>

Primary (server)
:   When two or more [*[databases](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE)
    are linked via [*[replication](README.md#GLOSSARY-REPLICATION)*](README.md#GLOSSARY-REPLICATION),
    the [*[server](README.md#GLOSSARY-SERVER)*](README.md#GLOSSARY-SERVER)
    that is considered the authoritative source of information is called
    the *primary*,
    also known as a *master*.
<a id="GLOSSARY-PROCEDURE"></a>

Procedure (routine)
:   A type of routine.
    Their distinctive qualities are that they do not return values,
    and that they are allowed to make transactional statements such
    as `COMMIT` and `ROLLBACK`.
    They are invoked via the `CALL` command.

    For more information, see
    [CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md).
<a id="GLOSSARY-QUERY"></a>

Query
:   A request sent by a client to a [*[backend](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND),
    usually to return results or to modify data on the database.
<a id="GLOSSARY-PLANNER"></a>

Query planner
:   The part of PostgreSQL that is devoted to
    determining (*planning*) the most efficient way to
    execute [*[queries](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY).
    Also known as *query optimizer*,
    *optimizer*, or simply *planner*.

Record
:   See [Tuple](README.md#GLOSSARY-TUPLE).

Recycling
:   See [WAL file](README.md#GLOSSARY-WAL-FILE).
<a id="GLOSSARY-REFERENTIAL-INTEGRITY"></a>

Referential integrity
:   A means of restricting data in one [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION)
    by a [*[foreign key](README.md#GLOSSARY-FOREIGN-KEY)*](README.md#GLOSSARY-FOREIGN-KEY)
    so that it must have matching data in another
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).
<a id="GLOSSARY-RELATION"></a>

Relation
:   The generic term for all objects in a
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE)
    that have a name and a list of
    [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE)
    defined in a specific order.
    [*[Tables](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE),
    [*[sequences](README.md#GLOSSARY-SEQUENCE)*](README.md#GLOSSARY-SEQUENCE),
    [*[views](README.md#GLOSSARY-VIEW)*](README.md#GLOSSARY-VIEW),
    [*[foreign tables](README.md#GLOSSARY-FOREIGN-TABLE)*](README.md#GLOSSARY-FOREIGN-TABLE),
    [*[materialized views](README.md#GLOSSARY-MATERIALIZED-VIEW)*](README.md#GLOSSARY-MATERIALIZED-VIEW),
    composite types, and
    [*[indexes](README.md#GLOSSARY-INDEX)*](README.md#GLOSSARY-INDEX) are all relations.

    More generically, a relation is a set of tuples; for example,
    the result of a query is also a relation.

    In PostgreSQL,
    *Class* is an archaic synonym for
    *relation*.
<a id="GLOSSARY-REPLICA"></a>

Replica (server)
:   A [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) that is paired
    with a [*[primary](README.md#GLOSSARY-PRIMARY-SERVER)*](README.md#GLOSSARY-PRIMARY-SERVER)
    database and is maintaining a copy of some or all of the primary database's
    data. The foremost reasons for doing this are to allow for greater access
    to that data, and to maintain availability of the data in the event that
    the [*[primary](README.md#GLOSSARY-PRIMARY-SERVER)*](README.md#GLOSSARY-PRIMARY-SERVER)
    becomes unavailable.
<a id="GLOSSARY-REPLICATION"></a>

Replication
:   The act of reproducing data on one
    [*[server](README.md#GLOSSARY-SERVER)*](README.md#GLOSSARY-SERVER) onto another
    server called a [*[replica](README.md#GLOSSARY-REPLICA)*](README.md#GLOSSARY-REPLICA).
    This can take the form of *physical replication*,
    where all file changes from one server are copied verbatim,
    or *logical replication* where a defined subset
    of data changes are conveyed using a higher-level representation.
<a id="GLOSSARY-RESTARTPOINT"></a>

Restartpoint
:   A variant of a [*[checkpoint](README.md#GLOSSARY-CHECKPOINT)*](README.md#GLOSSARY-CHECKPOINT) performed on a
    [*[replica](README.md#GLOSSARY-REPLICA)*](README.md#GLOSSARY-REPLICA).

    For more information, see [Section 28.5](../../server-administration/wal/wal-configuration.md).
<a id="GLOSSARY-RESULT-SET"></a>

Result set
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) transmitted
    from a [*[backend process](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND)
    to a [*[client](README.md#GLOSSARY-CLIENT)*](README.md#GLOSSARY-CLIENT) upon the
    completion of an SQL command, usually a
    `SELECT` but it can be an
    `INSERT`, `UPDATE`,
    `DELETE`, or `MERGE` command if the
    `RETURNING` clause is specified.

    The fact that a result set is a relation means that a query can be used
    in the definition of another query, becoming a
    *subquery*.
<a id="GLOSSARY-REVOKE"></a>

Revoke
:   A command to prevent access to a named set of
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) objects for a
    named list of [*[roles](README.md#GLOSSARY-ROLE)*](README.md#GLOSSARY-ROLE).

    For more information, see
    [REVOKE](../../reference/sql-commands/sql-revoke.md).
<a id="GLOSSARY-ROLE"></a>

Role
:   A collection of access privileges to the
    [*[instance](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE).
    Roles are themselves a privilege that can be granted to other roles.
    This is often done for convenience or to ensure completeness
    when multiple [*[users](README.md#GLOSSARY-USER)*](README.md#GLOSSARY-USER) need
    the same privileges.

    For more information, see
    [CREATE ROLE](../../reference/sql-commands/sql-createrole.md).
<a id="GLOSSARY-ROLLBACK"></a>

Rollback
:   A command to undo all of the operations performed since the beginning
    of a [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION).

    For more information, see
    [ROLLBACK](../../reference/sql-commands/sql-rollback.md).
<a id="GLOSSARY-ROUTINE"></a>

Routine
:   A defined set of instructions stored in the database system
    that can be invoked for execution.
    A routine can be written in a variety of programming
    languages. Routines can be
    [*[functions](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION)
    (including set-returning functions and
    [*[trigger functions](README.md#GLOSSARY-TRIGGER)*](README.md#GLOSSARY-TRIGGER)),
    [*[aggregate functions](README.md#GLOSSARY-AGGREGATE)*](README.md#GLOSSARY-AGGREGATE),
    and [*[procedures](README.md#GLOSSARY-PROCEDURE)*](README.md#GLOSSARY-PROCEDURE).

    Many routines are already defined within PostgreSQL
    itself, but user-defined ones can also be added.

Row
:   See [Tuple](README.md#GLOSSARY-TUPLE).
<a id="GLOSSARY-SAVEPOINT"></a>

Savepoint
:   A special mark in the sequence of steps in a
    [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION).
    Data modifications after this point in time may be reverted
    to the time of the savepoint.

    For more information, see
    [SAVEPOINT](../../reference/sql-commands/sql-savepoint.md).
<a id="GLOSSARY-SCHEMA"></a>

Schema
:   A schema is a namespace for
    [*[SQL objects](README.md#GLOSSARY-SQL-OBJECT)*](README.md#GLOSSARY-SQL-OBJECT),
    which all reside in the same
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE).
    Each SQL object must reside in exactly one schema.

    All system-defined SQL objects reside in schema `pg_catalog`.
:   More generically, the term *schema* is used to mean
    all data descriptions ([*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) definitions,
    [*[constraints](README.md#GLOSSARY-CONSTRAINT)*](README.md#GLOSSARY-CONSTRAINT), comments, etc.)
    for a given [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) or
    subset thereof.

    For more information, see
    [Section 5.10](../../the-sql-language/ddl/ddl-schemas.md).

Segment
:   See [File segment](README.md#GLOSSARY-FILE-SEGMENT).
<a id="GLOSSARY-SELECT"></a>

Select
:   The SQL command used to request data from a
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE).
    Normally, `SELECT` commands are not expected to modify the
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) in any way,
    but it is possible that
    [*[functions](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION) invoked within
    the query could have side effects that do modify data.

    For more information, see
    [SELECT](../../reference/sql-commands/sql-select.md).
<a id="GLOSSARY-SEQUENCE"></a>

Sequence (relation)
:   A type of relation that is used to generate values.
    Typically the generated values are sequential non-repeating numbers.
    They are commonly used to generate surrogate
    [*[primary key](README.md#GLOSSARY-PRIMARY-KEY)*](README.md#GLOSSARY-PRIMARY-KEY)
    values.
<a id="GLOSSARY-SERVER"></a>

Server
:   A computer on which PostgreSQL
    [*[instances](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE) run.
    The term *server* denotes real hardware, a
    container, or a *virtual machine*.

    This term is sometimes used to refer to an instance or to a host.
<a id="GLOSSARY-SESSION"></a>

Session
:   A state that allows a client and a backend to interact,
    communicating over a [*[connection](README.md#GLOSSARY-CONNECTION)*](README.md#GLOSSARY-CONNECTION).
<a id="GLOSSARY-SHARED-MEMORY"></a>

Shared memory
:   RAM which is used by the processes common to an
    [*[instance](README.md#GLOSSARY-INSTANCE)*](README.md#GLOSSARY-INSTANCE).
    It mirrors parts of [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE)
    files, provides a transient area for
    [*[WAL records](README.md#GLOSSARY-WAL-RECORD)*](README.md#GLOSSARY-WAL-RECORD),
    and stores additional common information.
    Note that shared memory belongs to the complete instance, not to a single
    database.

    The largest part of shared memory is known as *shared buffers*
    and is used to mirror part of data files, organized into pages.
    When a page is modified, it is called a dirty page until it is
    written back to the file system.

    For more information, see
    [Section 19.4.1](../../server-administration/runtime-config/runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY).
<a id="GLOSSARY-SQL-OBJECT"></a>

SQL object
:   Any object that can be created with a `CREATE`
    command. Most objects are specific to one database, and are commonly
    known as *local objects*.

    Most local objects reside in a specific
    [*[schema](README.md#GLOSSARY-SCHEMA)*](README.md#GLOSSARY-SCHEMA) in their
    containing database, such as
    [*[relations](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) (all types),
    [*[routines](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION) (all types),
    data types, etc.
    The names of such objects of the same type in the same schema
    are enforced to be unique.

    There also exist local objects that do not reside in schemas; some examples are
    [*[extensions](README.md#GLOSSARY-EXTENSION)*](README.md#GLOSSARY-EXTENSION),
    [*[data type casts](README.md#GLOSSARY-CAST)*](README.md#GLOSSARY-CAST), and
    [*[foreign data wrappers](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER)*](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER).
    The names of such objects of the same type are enforced to be unique
    within the database.

    Other object types, such as
    [*[roles](README.md#GLOSSARY-ROLE)*](README.md#GLOSSARY-ROLE),
    [*[tablespaces](README.md#GLOSSARY-TABLESPACE)*](README.md#GLOSSARY-TABLESPACE),
    replication origins, subscriptions for logical replication, and
    databases themselves are not local SQL objects since they exist
    entirely outside of any specific database;
    they are called *global objects*.
    The names of such objects are enforced to be unique within the whole
    database cluster.

    For more information, see
    [Section 22.1](../../server-administration/managing-databases/manage-ag-overview.md).
<a id="GLOSSARY-SQL-STANDARD"></a>

SQL standard
:   A series of documents that define the SQL language.

Standby (server)
:   See [Replica (server)](README.md#GLOSSARY-REPLICA).
<a id="GLOSSARY-STARTUP-PROCESS"></a>

Startup process
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that replays WAL during crash recovery and in a
    [*[physical replica](README.md#GLOSSARY-REPLICATION)*](README.md#GLOSSARY-REPLICATION).

    (The name is historical: the startup process was named before
    replication was implemented; the name refers to its task as it
    relates to the server startup following a crash.)
<a id="GLOSSARY-SUPERUSER"></a>

Superuser
:   As used in this documentation, it is a synonym for
    [*[database superuser](README.md#GLOSSARY-DATABASE-SUPERUSER)*](README.md#GLOSSARY-DATABASE-SUPERUSER).
<a id="GLOSSARY-SYSTEM-CATALOG"></a>

System catalog
:   A collection of [*[tables](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE)
    which describe the structure of all
    [*[SQL objects](README.md#GLOSSARY-SQL-OBJECT)*](README.md#GLOSSARY-SQL-OBJECT)
    of the instance.
    The system catalog resides in the schema `pg_catalog`.
    These tables contain data in internal representation and are
    not typically considered useful for user examination;
    a number of user-friendlier [*[views](README.md#GLOSSARY-VIEW)*](README.md#GLOSSARY-VIEW),
    also in schema `pg_catalog`, offer more convenient access to
    some of that information, while additional tables and views
    exist in schema `information_schema`
    (see [Chapter 35](../../client-interfaces/information-schema/README.md)) that expose some
    of the same and additional information as mandated by the
    [*[SQL standard](README.md#GLOSSARY-SQL-STANDARD)*](README.md#GLOSSARY-SQL-STANDARD).

    For more information, see
    [Section 5.10](../../the-sql-language/ddl/ddl-schemas.md).
<a id="GLOSSARY-TABLE"></a>

Table
:   A collection of [*[tuples](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) having
    a common data structure (the same number of
    [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE), in the same
    order, having the same name and type per position).
    A table is the most common form of
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) in
    PostgreSQL.

    For more information, see
    [CREATE TABLE](../../reference/sql-commands/sql-createtable.md).
<a id="GLOSSARY-TABLESPACE"></a>

Tablespace
:   A named location on the server file system.
    All [*[SQL objects](README.md#GLOSSARY-SQL-OBJECT)*](README.md#GLOSSARY-SQL-OBJECT)
    which require storage beyond their definition in the
    [*[system catalog](README.md#GLOSSARY-SYSTEM-CATALOG)*](README.md#GLOSSARY-SYSTEM-CATALOG)
    must belong to a single tablespace.
    Initially, a database cluster contains a single usable tablespace which is
    used as the default for all SQL objects, called `pg_default`.

    For more information, see
    [Section 22.6](../../server-administration/managing-databases/manage-ag-tablespaces.md).
<a id="GLOSSARY-TEMPORARY-TABLE"></a>

Temporary table
:   [*[Tables](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE) that exist either
    for the lifetime of a
    [*[session](README.md#GLOSSARY-SESSION)*](README.md#GLOSSARY-SESSION) or a
    [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION), as
    specified at the time of creation.
    The data in them is not visible to other sessions, and is not
    [*[logged](README.md#GLOSSARY-LOGGED)*](README.md#GLOSSARY-LOGGED).
    Temporary tables are often used to store intermediate data for a
    multi-step operation.

    For more information, see
    [CREATE TABLE](../../reference/sql-commands/sql-createtable.md).
<a id="GLOSSARY-TOAST"></a>

TOAST
:   A mechanism by which large attributes of table rows are split and
    stored in a secondary table, called the *TOAST table*.
    Each relation with large attributes has its own TOAST table.

    For more information, see
    [Section 66.2](../../internals/storage/storage-toast.md).
<a id="GLOSSARY-TRANSACTION"></a>

Transaction
:   A combination of commands that must act as a single
    [*[atomic](README.md#GLOSSARY-ATOMIC)*](README.md#GLOSSARY-ATOMIC) command: they all
    succeed or all fail as a single unit, and their effects are not visible to
    other [*[sessions](README.md#GLOSSARY-SESSION)*](README.md#GLOSSARY-SESSION) until
    the transaction is complete, and possibly even later, depending on the
    isolation level.

    For more information, see
    [Section 13.2](../../the-sql-language/mvcc/transaction-iso.md).
<a id="GLOSSARY-XID"></a>

Transaction ID
:   The numerical, unique, sequentially-assigned identifier that each
    transaction receives when it first causes a database modification.
    Frequently abbreviated as *xid*.
    When stored on disk, xids are only 32-bits wide, so only
    approximately four billion write transaction IDs can be generated;
    to permit the system to run for longer than that,
    *epochs* are used, also 32 bits wide.
    When the counter reaches the maximum xid value, it starts over at
    `3` (values under that are reserved) and the
    epoch value is incremented by one.
    In some contexts, the epoch and xid values are
    considered together as a single 64-bit value; see [Section 67.1](../../internals/transactions/transaction-id.md) for more details.

    For more information, see
    [Section 8.19](../../the-sql-language/datatype/datatype-oid.md).
<a id="GLOSSARY-TPS"></a>

Transactions per second (TPS)
:   Average number of transactions that are executed per second,
    totaled across all sessions active for a measured run.
    This is used as a measure of the performance characteristics of
    an instance.
<a id="GLOSSARY-TRIGGER"></a>

Trigger
:   A [*[function](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION) which can
    be defined to execute whenever a certain operation (`INSERT`,
    `UPDATE`, `DELETE`,
    `TRUNCATE`) is applied to a
    [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION).
    A trigger executes within the same
    [*[transaction](README.md#GLOSSARY-TRANSACTION)*](README.md#GLOSSARY-TRANSACTION) as the
    statement which invoked it, and if the function fails, then the invoking
    statement also fails.

    For more information, see
    [CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md).
<a id="GLOSSARY-TUPLE"></a>

Tuple
:   A collection of [*[attributes](README.md#GLOSSARY-ATTRIBUTE)*](README.md#GLOSSARY-ATTRIBUTE)
    in a fixed order.
    That order may be defined by the [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE)
    (or other [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION))
    where the tuple is contained, in which case the tuple is often called a
    *row*. It may also be defined by the structure of a
    result set, in which case it is sometimes called a *record*.
<a id="GLOSSARY-UNIQUE-CONSTRAINT"></a>

Unique constraint
:   A type of [*[constraint](README.md#GLOSSARY-CONSTRAINT)*](README.md#GLOSSARY-CONSTRAINT)
    defined on a [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION)
    which restricts the values allowed in one or a combination of columns
    so that each value or combination of values can only appear once in the
    relation — that is, no other row in the relation contains values
    that are equal to those.

    Because [*[null values](README.md#GLOSSARY-NULL)*](README.md#GLOSSARY-NULL) are
    not considered equal to each other, multiple rows with null values are
    allowed to exist without violating the unique constraint.
<a id="GLOSSARY-UNLOGGED"></a>

Unlogged
:   The property of certain [*[relations](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION)
    that the changes to them are not reflected in the
    [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL).
    This disables replication and crash recovery for these relations.

    The primary use of unlogged tables is for storing
    transient work data that must be shared across processes.

    [*[Temporary tables](README.md#GLOSSARY-TEMPORARY-TABLE)*](README.md#GLOSSARY-TEMPORARY-TABLE)
    are always unlogged.
<a id="GLOSSARY-UPDATE"></a>

Update
:   An SQL command used to modify
    [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    that may already exist in a specified [*[table](README.md#GLOSSARY-TABLE)*](README.md#GLOSSARY-TABLE).
    It cannot create or remove rows.

    For more information, see
    [UPDATE](../../reference/sql-commands/sql-update.md).
<a id="GLOSSARY-USER"></a>

User
:   A [*[role](README.md#GLOSSARY-ROLE)*](README.md#GLOSSARY-ROLE) that has the
    *login privilege*
    (see [Section 21.2](../../server-administration/user-manag/role-attributes.md)).
<a id="GLOSSARY-USER-MAPPING"></a>

User mapping
:   The translation of login credentials in the local
    [*[database](README.md#GLOSSARY-DATABASE)*](README.md#GLOSSARY-DATABASE) to credentials
    in a remote data system defined by a
    [*[foreign data wrapper](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER)*](README.md#GLOSSARY-FOREIGN-DATA-WRAPPER).

    For more information, see
    [CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md).
<a id="GLOSSARY-UTC"></a>

UTC
:   Universal Coordinated Time, the primary global time reference,
    approximately the time prevailing at the zero meridian of longitude.
    Often but inaccurately referred to as GMT (Greenwich Mean Time).
<a id="GLOSSARY-VACUUM"></a>

Vacuum
:   The process of removing outdated
    [*[tuple versions](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE)
    from tables or materialized views, and other closely related
    processing required by PostgreSQL's
    implementation of [*[MVCC](README.md#GLOSSARY-MVCC)*](README.md#GLOSSARY-MVCC).
    This can be initiated through the use of
    the `VACUUM` command, but can also be handled automatically
    via [*[autovacuum](README.md#GLOSSARY-AUTOVACUUM)*](README.md#GLOSSARY-AUTOVACUUM) processes.

    For more information, see
    [Section 24.1](../../server-administration/maintenance/routine-vacuuming.md) .
<a id="GLOSSARY-VIEW"></a>

View
:   A [*[relation](README.md#GLOSSARY-RELATION)*](README.md#GLOSSARY-RELATION) that is defined by a
    `SELECT` statement, but has no storage of its own.
    Any time a query references a view, the definition of the view is
    substituted into the query as if the user had typed it as a subquery
    instead of the name of the view.

    For more information, see
    [CREATE VIEW](../../reference/sql-commands/sql-createview.md).
<a id="GLOSSARY-VM"></a>

Visibility map (fork)
:   A storage structure that keeps metadata about each data page
    of a table's main fork. The visibility map entry for
    each page stores two bits: the first one
    (`all-visible`) indicates that all tuples
    in the page are visible to all transactions. The second one
    (`all-frozen`) indicates that all tuples
    in the page are marked frozen.

WAL
:   See [Write-ahead log](README.md#GLOSSARY-WAL).
<a id="GLOSSARY-WAL-ARCHIVER"></a>

WAL archiver (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    which, if enabled, saves copies of
    [*[WAL files](README.md#GLOSSARY-WAL-FILE)*](README.md#GLOSSARY-WAL-FILE)
    for the purpose of creating backups or keeping
    [*[replicas](README.md#GLOSSARY-REPLICA)*](README.md#GLOSSARY-REPLICA) current.

    For more information, see
    [Section 25.3](../../server-administration/backup/continuous-archiving.md).
<a id="GLOSSARY-WAL-FILE"></a>

WAL file
:   Also known as *WAL segment* or
    *WAL segment file*.
    Each of the sequentially-numbered files that provide storage space for
    [*[WAL](README.md#GLOSSARY-WAL)*](README.md#GLOSSARY-WAL).
    The files are all of the same predefined size
    and are written in sequential order, interspersing changes
    as they occur in multiple simultaneous sessions.
    If the system crashes, the files are read in order, and each of the
    changes is replayed to restore the system to the state it was in
    before the crash.

    Each WAL file can be released after a
    [*[checkpoint](README.md#GLOSSARY-CHECKPOINT)*](README.md#GLOSSARY-CHECKPOINT)
    writes all the changes in it to the corresponding data files.
    Releasing the file can be done either by deleting it, or by changing its
    name so that it will be used in the future, which is called
    *recycling*.

    For more information, see
    [Section 28.6](../../server-administration/wal/wal-internals.md).
<a id="GLOSSARY-WAL-RECORD"></a>

WAL record
:   A low-level description of an individual data change.
    It contains sufficient information for the data change to be
    re-executed (*replayed*) in case a system failure
    causes the change to be lost.
    WAL records use a non-printable binary format.

    For more information, see
    [Section 28.6](../../server-administration/wal/wal-internals.md).
<a id="GLOSSARY-WAL-RECEIVER"></a>

WAL receiver (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that runs on a [*[replica](README.md#GLOSSARY-REPLICA)*](README.md#GLOSSARY-REPLICA)
    to receive WAL from the
    [*[primary server](README.md#GLOSSARY-PRIMARY-SERVER)*](README.md#GLOSSARY-PRIMARY-SERVER)
    for replay by the
    [*[startup process](README.md#GLOSSARY-STARTUP-PROCESS)*](README.md#GLOSSARY-STARTUP-PROCESS).

    For more information, see
    [Section 26.2](../../server-administration/high-availability/warm-standby.md).

WAL segment
:   See [WAL file](README.md#GLOSSARY-WAL-FILE).
<a id="GLOSSARY-WAL-SENDER"></a>

WAL sender (process)
:   A special [*[backend process](README.md#GLOSSARY-BACKEND)*](README.md#GLOSSARY-BACKEND)
    that streams WAL over a network. The receiving end can be a
    [*[WAL receiver](README.md#GLOSSARY-WAL-RECEIVER)*](README.md#GLOSSARY-WAL-RECEIVER)
    in a [*[replica](README.md#GLOSSARY-REPLICA)*](README.md#GLOSSARY-REPLICA),
    [pg_receivewal](../../reference/reference-client/app-pgreceivewal.md), or any other client program
    that speaks the replication protocol.
<a id="GLOSSARY-WAL-SUMMARIZER"></a>

WAL summarizer (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that summarizes WAL data for
    [*[incremental backups](README.md#GLOSSARY-INCREMENTAL-BACKUP)*](README.md#GLOSSARY-INCREMENTAL-BACKUP).

    For more information, see [Section 19.5.7](../../server-administration/runtime-config/runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION).
<a id="GLOSSARY-WAL-WRITER"></a>

WAL writer (process)
:   An [*[auxiliary process](README.md#GLOSSARY-AUXILIARY-PROC)*](README.md#GLOSSARY-AUXILIARY-PROC)
    that writes [*[WAL records](README.md#GLOSSARY-WAL-RECORD)*](README.md#GLOSSARY-WAL-RECORD)
    from [*[shared memory](README.md#GLOSSARY-SHARED-MEMORY)*](README.md#GLOSSARY-SHARED-MEMORY) to
    [*[WAL files](README.md#GLOSSARY-WAL-FILE)*](README.md#GLOSSARY-WAL-FILE).

    For more information, see
    [Section 19.5](../../server-administration/runtime-config/runtime-config-wal.md).
<a id="GLOSSARY-WINDOW-FUNCTION"></a>

Window function (routine)
:   A type of [*[function](README.md#GLOSSARY-FUNCTION)*](README.md#GLOSSARY-FUNCTION)
    used in a [*[query](README.md#GLOSSARY-QUERY)*](README.md#GLOSSARY-QUERY)
    that applies to a [*[partition](README.md#GLOSSARY-PARTITION)*](README.md#GLOSSARY-PARTITION)
    of the query's [*[result set](README.md#GLOSSARY-RESULT-SET)*](README.md#GLOSSARY-RESULT-SET);
    the function's result is based on values found in
    [*[rows](README.md#GLOSSARY-TUPLE)*](README.md#GLOSSARY-TUPLE) of the same partition or frame.

    All [*[aggregate functions](README.md#GLOSSARY-AGGREGATE)*](README.md#GLOSSARY-AGGREGATE)
    can be used as window functions, but window functions can also be
    used to, for example, give ranks to each of the rows in the partition.
    Also known as *analytic functions*.

    For more information, see
    [Section 3.5](../../tutorial/tutorial-advanced/tutorial-window.md).
<a id="GLOSSARY-WAL"></a>

Write-ahead log
:   The journal that keeps track of the changes in the
    [*[database cluster](README.md#GLOSSARY-DB-CLUSTER)*](README.md#GLOSSARY-DB-CLUSTER)
    as user- and system-invoked operations take place.
    It comprises many individual
    [*[WAL records](README.md#GLOSSARY-WAL-RECORD)*](README.md#GLOSSARY-WAL-RECORD) written
    sequentially to [*[WAL files](README.md#GLOSSARY-WAL-FILE)*](README.md#GLOSSARY-WAL-FILE).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/glossary.html)（英文原文，待翻譯）
