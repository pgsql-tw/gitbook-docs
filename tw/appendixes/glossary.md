# M. Glossary

This is a list of terms and their meaning in the context of PostgreSQL and relational database systems in general.

#### ACID

[Atomicity](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATOMICITY), [Consistency](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSISTENCY), [Isolation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ISOLATION), and [Durability](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DURABILITY). This set of properties of database transactions is intended to guarantee validity in concurrent operation and even in event of errors, power failures, etc.

#### Aggregate function \(routine\)

A [function](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) that combines \(_aggregates_\) multiple input values, for example by counting, averaging or adding, yielding a single output value.

For more information, see [Section 9.21](https://www.postgresql.org/docs/13/functions-aggregate.html).

See Also [Window function \(routine\)](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WINDOW-FUNCTION).

#### Analytic function

See [Window function \(routine\)](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WINDOW-FUNCTION).

#### Analyze \(operation\)

The process of collecting statistics from data in [tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) and other [relations](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) to help the [query planner](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PLANNER) to make decisions about how to execute [queries](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY).

\(Don't confuse this term with the `ANALYZE` option to the [EXPLAIN](https://www.postgresql.org/docs/13/sql-explain.html) command.\)

For more information, see [ANALYZE](https://www.postgresql.org/docs/13/sql-analyze.html).

#### Atomic

In reference to a [datum](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATUM): the fact that its value cannot be broken down into smaller components.

In reference to a [database transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION): see [atomicity](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATOMICITY).

#### Atomicity

The property of a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION) that either all its operations complete as a single unit or none do. In addition, if a system failure occurs during the execution of a transaction, no partial results are visible after recovery. This is one of the ACID properties.

#### Attribute

An element with a certain name and data type found within a [tuple](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE).

#### Autovacuum \(process\)

A set of background processes that routinely perform [vacuum](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VACUUM) and [analyze](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ANALYZE) operations.

For more information, see [Section 24.1.6](https://www.postgresql.org/docs/13/routine-vacuuming.html#AUTOVACUUM).

#### Backend \(process\)

Process of an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE) which acts on behalf of a [client session](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SESSION) and handles its requests.

\(Don't confuse this term with the similar terms [Background Worker](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKGROUND-WORKER) or [Background Writer](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKGROUND-WRITER)\).

#### Background worker \(process\)

Process within an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE), which runs system- or user-supplied code. Serves as infrastructure for several features in PostgreSQL, such as [logical replication](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-REPLICATION) and [parallel queries](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PARALLEL-QUERY). In addition, [Extensions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-EXTENSION) can add custom background worker processes.

For more information, see [Chapter 47](https://www.postgresql.org/docs/13/bgworker.html).

#### Background writer \(process\)

A process that writes dirty [data pages](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATA-PAGE) from [shared memory](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SHARED-MEMORY) to the file system. It wakes up periodically, but works only for a short period in order to distribute its expensive I/O activity over time to avoid generating larger I/O peaks which could block other processes.

For more information, see [Section 19.4.5](https://www.postgresql.org/docs/13/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER).

#### Bloat

Space in data pages which does not contain current row versions, such as unused \(free\) space or outdated row versions.Cast

A conversion of a [datum](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATUM) from its current data type to another data type.

For more information, see [CREATE CAST](https://www.postgresql.org/docs/13/sql-createcast.html).

#### Catalog

The SQL standard uses this term to indicate what is called a [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) in PostgreSQL's terminology.

\(Don't confuse this term with [system catalog](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SYSTEM-CATALOG)\).

For more information, see [Section 22.1](https://www.postgresql.org/docs/13/manage-ag-overview.html).

#### Check constraint

A type of [constraint](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSTRAINT) defined on a [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) which restricts the values allowed in one or more [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE). The check constraint can make reference to any attribute of the same row in the relation, but cannot reference other rows of the same relation or other relations.

For more information, see [Section 5.4](https://www.postgresql.org/docs/13/ddl-constraints.html).

#### Checkpoint

A point in the [WAL](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL) sequence at which it is guaranteed that the heap and index data files have been updated with all information from [shared memory](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SHARED-MEMORY) modified before that checkpoint; a _checkpoint record_ is written and flushed to WAL to mark that point.

A checkpoint is also the act of carrying out all the actions that are necessary to reach a checkpoint as defined above. This process is initiated when predefined conditions are met, such as a specified amount of time has passed, or a certain volume of records has been written; or it can be invoked by the user with the command `CHECKPOINT`.

For more information, see [Section 29.4](https://www.postgresql.org/docs/13/wal-configuration.html).

#### Checkpointer \(process\)

A specialized process responsible for executing checkpoints.

#### Class \(archaic\)

See [Relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION).Client \(process\)

Any process, possibly remote, that establishes a [session](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SESSION) by [connecting](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONNECTION) to an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE) to interact with a [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE).

#### Column

An [attribute](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE) found in a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) or [view](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VIEW).Commit

The act of finalizing a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION) within the [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE), which makes it visible to other transactions and assures its [durability](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DURABILITY).

For more information, see [COMMIT](https://www.postgresql.org/docs/13/sql-commit.html).

#### Concurrency

The concept that multiple independent operations happen within the [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) at the same time. In PostgreSQL, concurrency is controlled by the [multiversion concurrency control](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-MVCC) mechanism.

#### Connection

An established line of communication between a client process and a [backend](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKEND) process, usually over a network, supporting a [session](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SESSION). This term is sometimes used as a synonym for session.

For more information, see [Section 19.3](https://www.postgresql.org/docs/13/runtime-config-connection.html).

#### Consistency

The property that the data in the [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) is always in compliance with [integrity constraints](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSTRAINT). Transactions may be allowed to violate some of the constraints transiently before it commits, but if such violations are not resolved by the time it commits, such a transaction is automatically [rolled back](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ROLLBACK). This is one of the ACID properties.

#### Constraint

A restriction on the values of data allowed within a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE), or in attributes of a _domain_.

For more information, see [Section 5.4](https://www.postgresql.org/docs/13/ddl-constraints.html).

#### Data area

See [Data directory](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATA-DIRECTORY).Database

A named collection of [local SQL objects](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SQL-OBJECT).

For more information, see [Section 22.1](https://www.postgresql.org/docs/13/manage-ag-overview.html).Database cluster

A collection of databases and global SQL objects, and their common static and dynamic metadata. Sometimes referred to as a _cluster_.

In PostgreSQL, the term _cluster_ is also sometimes used to refer to an instance. \(Don't confuse this term with the SQL command `CLUSTER`.\)Database server

See [Instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE).Data directory

The base directory on the file system of a [server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SERVER) that contains all data files and subdirectories associated with a [database cluster](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DB-CLUSTER) \(with the exception of [tablespaces](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLESPACE), and optionally [WAL](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL)\). The environment variable `PGDATA` is commonly used to refer to the data directory.

A [cluster](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DB-CLUSTER)'s storage space comprises the data directory plus any additional tablespaces.

For more information, see [Section 68.1](https://www.postgresql.org/docs/13/storage-file-layout.html).Data page

The basic structure used to store relation data. All pages are of the same size. Data pages are typically stored on disk, each in a specific file, and can be read to [shared buffers](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SHARED-MEMORY) where they can be modified, becoming _dirty_. They become clean when written to disk. New pages, which initially exist in memory only, are also dirty until written.Datum

The internal representation of one value of an SQL data type.Delete

An SQL command which removes [rows](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) from a given [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) or [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION).

For more information, see [DELETE](https://www.postgresql.org/docs/13/sql-delete.html).Durability

The assurance that once a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION) has been [committed](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-COMMIT), the changes remain even after a system failure or crash. This is one of the ACID properties.Epoch

See [Transaction ID](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-XID).Extension

A software add-on package that can be installed on an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE) to get extra features.

For more information, see [Section 37.17](https://www.postgresql.org/docs/13/extend-extensions.html).File segment

A physical file which stores data for a given [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION). File segments are limited in size by a configuration value \(typically 1 gigabyte\), so if a relation exceeds that size, it is split into multiple segments.

For more information, see [Section 68.1](https://www.postgresql.org/docs/13/storage-file-layout.html).

\(Don't confuse this term with the similar term [WAL segment](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE)\).Foreign data wrapper

A means of representing data that is not contained in the local [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) so that it appears as if were in local [table\(s\)](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE). With a foreign data wrapper it is possible to define a [foreign server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-SERVER) and [foreign tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-TABLE).

For more information, see [CREATE FOREIGN DATA WRAPPER](https://www.postgresql.org/docs/13/sql-createforeigndatawrapper.html).Foreign key

A type of [constraint](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSTRAINT) defined on one or more [columns](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-COLUMN) in a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) which requires the value\(s\) in those [columns](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-COLUMN) to identify zero or one [row](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) in another \(or, infrequently, the same\) [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE).Foreign server

A named collection of [foreign tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-TABLE) which all use the same [foreign data wrapper](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-DATA-WRAPPER) and have other configuration values in common.

For more information, see [CREATE SERVER](https://www.postgresql.org/docs/13/sql-createserver.html).Foreign table \(relation\)

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) which appears to have [rows](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) and [columns](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-COLUMN) similar to a regular [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE), but will forward requests for data through its [foreign data wrapper](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-DATA-WRAPPER), which will return [result sets](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RESULT-SET) structured according to the definition of the [foreign table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-TABLE).

For more information, see [CREATE FOREIGN TABLE](https://www.postgresql.org/docs/13/sql-createforeigntable.html).Fork

Each of the separate segmented file sets in which a relation is stored. The _main fork_ is where the actual data resides. There also exist two secondary forks for metadata: the [free space map](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FSM) and the [visibility map](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VM). [Unlogged relations](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-UNLOGGED) also have an _init fork_.Free space map \(fork\)

A storage structure that keeps metadata about each data page of a table's main fork. The free space map entry for each page stores the amount of free space that's available for future tuples, and is structured to be efficiently searched for available space for a new tuple of a given size.

For more information, see [Section 68.3](https://www.postgresql.org/docs/13/storage-fsm.html).Function \(routine\)

A type of routine that receives zero or more arguments, returns zero or more output values, and is constrained to run within one transaction. Functions are invoked as part of a query, for example via `SELECT`. Certain functions can return [sets](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RESULT-SET); those are called _set-returning functions_.

Functions can also be used for [triggers](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRIGGER) to invoke.

For more information, see [CREATE FUNCTION](https://www.postgresql.org/docs/13/sql-createfunction.html).Grant

An SQL command that is used to allow a [user](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-USER) or [role](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ROLE) to access specific objects within the [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE).

For more information, see [GRANT](https://www.postgresql.org/docs/13/sql-grant.html).Heap

Contains the values of [row](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) attributes \(i.e., the data\) for a [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION). The heap is realized within one or more [file segments](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FILE-SEGMENT) in the relation's [main fork](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FORK).Host

A computer that communicates with other computers over a network. This is sometimes used as a synonym for [server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SERVER). It is also used to refer to a computer where [client processes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CLIENT) run.Index \(relation\)

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that contains data derived from a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) or [materialized view](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-MATERIALIZED-VIEW). Its internal structure supports fast retrieval of and access to the original data.

For more information, see [CREATE INDEX](https://www.postgresql.org/docs/13/sql-createindex.html).Insert

An SQL command used to add new data into a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE).

For more information, see [INSERT](https://www.postgresql.org/docs/13/sql-insert.html).Instance

A group of backend and auxiliary processes that communicate using a common shared memory area. One [postmaster process](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-POSTMASTER) manages the instance; one instance manages exactly one [database cluster](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DB-CLUSTER) with all its databases. Many instances can run on the same [server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SERVER) as long as their TCP ports do not conflict.

The instance handles all key features of a DBMS: read and write access to files and shared memory, assurance of the ACID properties, [connections](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONNECTION) to [client processes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CLIENT), privilege verification, crash recovery, replication, etc.Isolation

The property that the effects of a transaction are not visible to [concurrent transactions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONCURRENCY) before it commits. This is one of the ACID properties.

For more information, see [Section 13.2](https://www.postgresql.org/docs/13/transaction-iso.html).Join

An operation and SQL keyword used in [queries](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY) for combining data from multiple [relations](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION).Key

A means of identifying a [row](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) within a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) or other [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) by values contained within one or more [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE) in that relation.Lock

A mechanism that allows a process to limit or prevent simultaneous access to a resource.Log file

Log files contain human-readable text lines about events. Examples include login failures, long-running queries, etc.

For more information, see [Section 24.3](https://www.postgresql.org/docs/13/logfile-maintenance.html).Logged

A [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) is considered [logged](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-LOGGED) if changes to it are sent to the [WAL](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL). By default, all regular tables are logged. A table can be specified as [unlogged](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-UNLOGGED) either at creation time or via the `ALTER TABLE` command.Logger \(process\)

If activated, the process writes information about database events into the current [log file](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-LOG-FILE). When reaching certain time- or volume-dependent criteria, a new log file is created. Also called _syslogger_.

For more information, see [Section 19.8](https://www.postgresql.org/docs/13/runtime-config-logging.html).Log record

Archaic term for a [WAL record](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-RECORD).Master \(server\)

See [Primary \(server\)](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PRIMARY-SERVER).Materialized

The property that some information has been pre-computed and stored for later use, rather than computing it on-the-fly.

This term is used in [materialized view](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-MATERIALIZED-VIEW), to mean that the data derived from the view's query is stored on disk separately from the sources of that data.

This term is also used to refer to some multi-step queries to mean that the data resulting from executing a given step is stored in memory \(with the possibility of spilling to disk\), so that it can be read multiple times by another step.Materialized view \(relation\)

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that is defined by a `SELECT` statement \(just like a [view](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VIEW)\), but stores data in the same way that a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) does. It cannot be modified via `INSERT`, `UPDATE`, or `DELETE` operations.

For more information, see [CREATE MATERIALIZED VIEW](https://www.postgresql.org/docs/13/sql-creatematerializedview.html).Multi-version concurrency control \(MVCC\)

A mechanism designed to allow several [transactions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION) to be reading and writing the same rows without one process causing other processes to stall. In PostgreSQL, MVCC is implemented by creating copies \(_versions_\) of [tuples](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) as they are modified; after transactions that can see the old versions terminate, those old versions need to be removed.Null

A concept of non-existence that is a central tenet of relational database theory. It represents the absence of a definite value.Optimizer

See [Query planner](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PLANNER).Parallel query

The ability to handle parts of executing a [query](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY) to take advantage of parallel processes on servers with multiple CPUs.Partition

One of several disjoint \(not overlapping\) subsets of a larger set.

In reference to a [partitioned table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PARTITIONED-TABLE): One of the tables that each contain part of the data of the partitioned table, which is said to be the _parent_. The partition is itself a table, so it can also be queried directly; at the same time, a partition can sometimes be a partitioned table, allowing hierarchies to be created.

In reference to a [window function](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WINDOW-FUNCTION) in a [query](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY), a partition is a user-defined criterion that identifies which neighboring [rows](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) of the [query's result set](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RESULT-SET) can be considered by the function.Partitioned table \(relation\)

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that is in semantic terms the same as a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE), but whose storage is distributed across several [partitions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PARTITION).Postmaster \(process\)

The very first process of an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE). It starts and manages the other auxiliary processes and creates [backend processes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKEND) on demand.

For more information, see [Section 18.3](https://www.postgresql.org/docs/13/server-start.html).Primary key

A special case of a [unique constraint](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-UNIQUE-CONSTRAINT) defined on a [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) or other [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that also guarantees that all of the [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE) within the [primary key](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PRIMARY-KEY) do not have [null](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-NULL) values. As the name implies, there can be only one primary key per table, though it is possible to have multiple unique constraints that also have no null-capable attributes.Primary \(server\)

When two or more [databases](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) are linked via [replication](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-REPLICATION), the [server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SERVER) that is considered the authoritative source of information is called the _primary_, also known as a _master_.Procedure \(routine\)

A type of routine. Their distinctive qualities are that they do not return values, and that they are allowed to make transactional statements such as `COMMIT` and `ROLLBACK`. They are invoked via the `CALL` command.

For more information, see [CREATE PROCEDURE](https://www.postgresql.org/docs/13/sql-createprocedure.html).Query

A request sent by a client to a [backend](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKEND), usually to return results or to modify data on the database.Query planner

The part of PostgreSQL that is devoted to determining \(_planning_\) the most efficient way to execute [queries](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY). Also known as _query optimizer_, _optimizer_, or simply _planner_.Record

See [Tuple](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE).Recycling

See [WAL file](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE).Referential integrity

A means of restricting data in one [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) by a [foreign key](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-KEY) so that it must have matching data in another [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION).Relation

The generic term for all objects in a [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) that have a name and a list of [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE) defined in a specific order. [Tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE), [sequences](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SEQUENCE), [views](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VIEW), [foreign tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-TABLE), [materialized views](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-MATERIALIZED-VIEW), composite types, and [indexes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INDEX) are all relations.

More generically, a relation is a set of tuples; for example, the result of a query is also a relation.

In PostgreSQL, _Class_ is an archaic synonym for _relation_.Replica \(server\)

A [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) that is paired with a [primary](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PRIMARY-SERVER) database and is maintaining a copy of some or all of the primary database's data. The foremost reasons for doing this are to allow for greater access to that data, and to maintain availability of the data in the event that the [primary](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PRIMARY-SERVER) becomes unavailable.Replication

The act of reproducing data on one [server](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SERVER) onto another server called a [replica](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-REPLICA). This can take the form of _physical replication_, where all file changes from one server are copied verbatim, or _logical replication_ where a defined subset of data changes are conveyed using a higher-level representation.Result set

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) transmitted from a [backend process](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-BACKEND) to a [client](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CLIENT) upon the completion of an SQL command, usually a `SELECT` but it can be an `INSERT`, `UPDATE`, or `DELETE` command if the `RETURNING` clause is specified.

The fact that a result set is a relation means that a query can be used in the definition of another query, becoming a _subquery_.Revoke

A command to prevent access to a named set of [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) objects for a named list of [roles](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ROLE).

For more information, see [REVOKE](https://www.postgresql.org/docs/13/sql-revoke.html).Role

A collection of access privileges to the [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE). Roles are themselves a privilege that can be granted to other roles. This is often done for convenience or to ensure completeness when multiple [users](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-USER) need the same privileges.

For more information, see [CREATE ROLE](https://www.postgresql.org/docs/13/sql-createrole.html).Rollback

A command to undo all of the operations performed since the beginning of a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION).

For more information, see [ROLLBACK](https://www.postgresql.org/docs/13/sql-rollback.html).Routine

A defined set of instructions stored in the database system that can be invoked for execution. A routine can be written in a variety of programming languages. Routines can be [functions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) \(including set-returning functions and [trigger functions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRIGGER)\), [aggregate functions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-AGGREGATE), and [procedures](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PROCEDURE).

Many routines are already defined within PostgreSQL itself, but user-defined ones can also be added.Row

See [Tuple](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE).Savepoint

A special mark in the sequence of steps in a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION). Data modifications after this point in time may be reverted to the time of the savepoint.

For more information, see [SAVEPOINT](https://www.postgresql.org/docs/13/sql-savepoint.html).Schema

A schema is a namespace for [SQL objects](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SQL-OBJECT), which all reside in the same [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE). Each SQL object must reside in exactly one schema.

All system-defined SQL objects reside in schema `pg_catalog`.

More generically, the term _schema_ is used to mean all data descriptions \([table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) definitions, [constraints](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSTRAINT), comments, etc\) for a given [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) or subset thereof.

For more information, see [Section 5.9](https://www.postgresql.org/docs/13/ddl-schemas.html).Segment

See [File segment](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FILE-SEGMENT).Select

The SQL command used to request data from a [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE). Normally, `SELECT` commands are not expected to modify the [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) in any way, but it is possible that [functions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) invoked within the query could have side effects that do modify data.

For more information, see [SELECT](https://www.postgresql.org/docs/13/sql-select.html).Sequence \(relation\)

A type of relation that is used to generate values. Typically the generated values are sequential non-repeating numbers. They are commonly used to generate surrogate [primary key](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PRIMARY-KEY) values.Server

A computer on which PostgreSQL [instances](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE) run. The term _server_ denotes real hardware, a container, or a _virtual machine_.

This term is sometimes used to refer to an instance or to a host.Session

A state that allows a client and a backend to interact, communicating over a [connection](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONNECTION).Shared memory

RAM which is used by the processes common to an [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE). It mirrors parts of [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) files, provides a transient area for [WAL records](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-RECORD), and stores additional common information. Note that shared memory belongs to the complete instance, not to a single database.

The largest part of shared memory is known as _shared buffers_ and is used to mirror part of data files, organized into pages. When a page is modified, it is called a dirty page until it is written back to the file system.

For more information, see [Section 19.4.1](https://www.postgresql.org/docs/13/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-MEMORY).SQL object

Any object that can be created with a `CREATE` command. Most objects are specific to one database, and are commonly known as _local objects_.

Most local objects belong to a specific [schema](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SCHEMA) in their containing database, such as [relations](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) \(all types\), [routines](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) \(all types\), data types, etc. The names of such objects of the same type in the same schema are enforced to be unique.

There also exist local objects that do not belong to schemas; some examples are [extensions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-EXTENSION), [data type casts](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CAST), and [foreign data wrappers](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-DATA-WRAPPER). The names of such objects of the same type are enforced to be unique within the database.

Other object types, such as [roles](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ROLE), [tablespaces](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLESPACE), replication origins, subscriptions for logical replication, and databases themselves are not local SQL objects since they exist entirely outside of any specific database; they are called _global objects_. The names of such objects are enforced to be unique within the whole database cluster.

For more information, see [Section 22.1](https://www.postgresql.org/docs/13/manage-ag-overview.html).SQL standard

A series of documents that define the SQL language.Standby \(server\)

See [Replica \(server\)](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-REPLICA).Stats collector \(process\)

This process collects statistical information about the [instance](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-INSTANCE)'s activities.

For more information, see [Section 27.2](https://www.postgresql.org/docs/13/monitoring-stats.html).System catalog

A collection of [tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) which describe the structure of all [SQL objects](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SQL-OBJECT) of the instance. The system catalog resides in the schema `pg_catalog`. These tables contain data in internal representation and are not typically considered useful for user examination; a number of user-friendlier [views](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-VIEW), also in schema `pg_catalog`, offer more convenient access to some of that information, while additional tables and views exist in schema `information_schema` \(see [Chapter 36](https://www.postgresql.org/docs/13/information-schema.html)\) that expose some of the same and additional information as mandated by the [SQL standard](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SQL-STANDARD).

For more information, see [Section 5.9](https://www.postgresql.org/docs/13/ddl-schemas.html).Table

A collection of [tuples](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) having a common data structure \(the same number of [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE), in the same order, having the same name and type per position\). A table is the most common form of [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) in PostgreSQL.

For more information, see [CREATE TABLE](https://www.postgresql.org/docs/13/sql-createtable.html).Tablespace

A named location on the server file system. All [SQL objects](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SQL-OBJECT) which require storage beyond their definition in the [system catalog](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SYSTEM-CATALOG) must belong to a single tablespace. Initially, a database cluster contains a single usable tablespace which is used as the default for all SQL objects, called `pg_default`.

For more information, see [Section 22.6](https://www.postgresql.org/docs/13/manage-ag-tablespaces.html).Temporary table

[Tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) that exist either for the lifetime of a [session](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SESSION) or a [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION), as specified at the time of creation. The data in them is not visible to other sessions, and is not [logged](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-LOGGED). Temporary tables are often used to store intermediate data for a multi-step operation.

For more information, see [CREATE TABLE](https://www.postgresql.org/docs/13/sql-createtable.html).TOAST

A mechanism by which large attributes of table rows are split and stored in a secondary table, called the _TOAST table_. Each relation with large attributes has its own TOAST table.

For more information, see [Section 68.2](https://www.postgresql.org/docs/13/storage-toast.html).Transaction

A combination of commands that must act as a single [atomic](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATOMIC) command: they all succeed or all fail as a single unit, and their effects are not visible to other [sessions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SESSION) until the transaction is complete, and possibly even later, depending on the isolation level.

For more information, see [Section 13.2](https://www.postgresql.org/docs/13/transaction-iso.html).Transaction ID

The numerical, unique, sequentially-assigned identifier that each transaction receives when it first causes a database modification. Frequently abbreviated as _xid_. When stored on disk, xids are only 32-bits wide, so only approximately four billion write transaction IDs can be generated; to permit the system to run for longer than that, _epochs_ are used, also 32 bits wide. When the counter reaches the maximum xid value, it starts over at `3` \(values under that are reserved\) and the epoch value is incremented by one. In some contexts, the epoch and xid values are considered together as a single 64-bit value.

For more information, see [Section 8.19](https://www.postgresql.org/docs/13/datatype-oid.html).Transactions per second \(TPS\)

Average number of transactions that are executed per second, totaled across all sessions active for a measured run. This is used as a measure of the performance characteristics of an instance.Trigger

A [function](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) which can be defined to execute whenever a certain operation \(`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`\) is applied to a [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION). A trigger executes within the same [transaction](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TRANSACTION) as the statement which invoked it, and if the function fails, then the invoking statement also fails.

For more information, see [CREATE TRIGGER](https://www.postgresql.org/docs/13/sql-createtrigger.html).Tuple

A collection of [attributes](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ATTRIBUTE) in a fixed order. That order may be defined by the [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE) \(or other [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION)\) where the tuple is contained, in which case the tuple is often called a _row_. It may also be defined by the structure of a result set, in which case it is sometimes called a _record_.Unique constraint

A type of [constraint](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CONSTRAINT) defined on a [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) which restricts the values allowed in one or a combination of columns so that each value or combination of values can only appear once in the relation — that is, no other row in the relation contains values that are equal to those.

Because [null values](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-NULL) are not considered equal to each other, multiple rows with null values are allowed to exist without violating the unique constraint.Unlogged

The property of certain [relations](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that the changes to them are not reflected in the [WAL](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL). This disables replication and crash recovery for these relations.

The primary use of unlogged tables is for storing transient work data that must be shared across processes.

[Temporary tables](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TEMPORARY-TABLE) are always unlogged.Update

An SQL command used to modify [rows](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) that may already exist in a specified [table](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TABLE). It cannot create or remove rows.

For more information, see [UPDATE](https://www.postgresql.org/docs/13/sql-update.html).User

A [role](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-ROLE) that has the `LOGIN` privilege.User mapping

The translation of login credentials in the local [database](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DATABASE) to credentials in a remote data system defined by a [foreign data wrapper](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FOREIGN-DATA-WRAPPER).

For more information, see [CREATE USER MAPPING](https://www.postgresql.org/docs/13/sql-createusermapping.html).Vacuum

The process of removing outdated [tuple versions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) from tables or materialized views, and other closely related processing required by PostgreSQL's implementation of [MVCC](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-MVCC). This can be initiated through the use of the `VACUUM` command, but can also be handled automatically via [autovacuum](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-AUTOVACUUM) processes.

For more information, see [Section 24.1](https://www.postgresql.org/docs/13/routine-vacuuming.html) .View

A [relation](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RELATION) that is defined by a `SELECT` statement, but has no storage of its own. Any time a query references a view, the definition of the view is substituted into the query as if the user had typed it as a subquery instead of the name of the view.

For more information, see [CREATE VIEW](https://www.postgresql.org/docs/13/sql-createview.html).Visibility map \(fork\)

A storage structure that keeps metadata about each data page of a table's main fork. The visibility map entry for each page stores two bits: the first one \(`all-visible`\) indicates that all tuples in the page are visible to all transactions. The second one \(`all-frozen`\) indicates that all tuples in the page are marked frozen.WAL

See [Write-ahead log](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL).WAL archiver \(process\)

A process that saves copies of [WAL files](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE) for the purpose of creating backups or keeping [replicas](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-REPLICA) current.

For more information, see [Section 25.3](https://www.postgresql.org/docs/13/continuous-archiving.html).WAL file

Also known as _WAL segment_ or _WAL segment file_. Each of the sequentially-numbered files that provide storage space for [WAL](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL). The files are all of the same predefined size and are written in sequential order, interspersing changes as they occur in multiple simultaneous sessions. If the system crashes, the files are read in order, and each of the changes is replayed to restore the system to the state it was in before the crash.

Each WAL file can be released after a [checkpoint](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-CHECKPOINT) writes all the changes in it to the corresponding data files. Releasing the file can be done either by deleting it, or by changing its name so that it will be used in the future, which is called _recycling_.

For more information, see [Section 29.5](https://www.postgresql.org/docs/13/wal-internals.html).WAL record

A low-level description of an individual data change. It contains sufficient information for the data change to be re-executed \(_replayed_\) in case a system failure causes the change to be lost. WAL records use a non-printable binary format.

For more information, see [Section 29.5](https://www.postgresql.org/docs/13/wal-internals.html).WAL segment

See [WAL file](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE).WAL writer \(process\)

A process that writes [WAL records](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-RECORD) from [shared memory](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-SHARED-MEMORY) to [WAL files](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE).

For more information, see [Section 19.5](https://www.postgresql.org/docs/13/runtime-config-wal.html).Window function \(routine\)

A type of [function](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-FUNCTION) used in a [query](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-QUERY) that applies to a [partition](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-PARTITION) of the query's [result set](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-RESULT-SET); the function's result is based on values found in [rows](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-TUPLE) of the same partition or frame.

All [aggregate functions](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-AGGREGATE) can be used as window functions, but window functions can also be used to, for example, give ranks to each of the rows in the partition. Also known as _analytic functions_.

For more information, see [Section 3.5](https://www.postgresql.org/docs/13/tutorial-window.html).Write-ahead log

The journal that keeps track of the changes in the [database cluster](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-DB-CLUSTER) as user- and system-invoked operations take place. It comprises many individual [WAL records](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-RECORD) written sequentially to [WAL files](https://www.postgresql.org/docs/13/glossary.html#GLOSSARY-WAL-FILE).

