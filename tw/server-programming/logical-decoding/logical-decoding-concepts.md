# 48.2. Logical Decoding Concepts

## 48.2.1. Logical Decoding

Logical decoding is the process of extracting all persistent changes to a database's tables into a coherent, easy to understand format which can be interpreted without detailed knowledge of the database's internal state.

In PostgreSQL, logical decoding is implemented by decoding the contents of the [write-ahead log](https://www.postgresql.org/docs/13/wal.html), which describe changes on a storage level, into an application-specific form such as a stream of tuples or SQL statements.

## 48.2.2. Replication Slots

In the context of logical replication, a slot represents a stream of changes that can be replayed to a client in the order they were made on the origin server. Each slot streams a sequence of changes from a single database.

#### Note

PostgreSQL also has streaming replication slots (see [Section 26.2.5](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION)), but they are used somewhat differently there.

A replication slot has an identifier that is unique across all databases in a PostgreSQL cluster. Slots persist independently of the connection using them and are crash-safe.

A logical slot will emit each change just once in normal operation. The current position of each slot is persisted only at checkpoint, so in the case of a crash the slot may return to an earlier LSN, which will then cause recent changes to be sent again when the server restarts. Logical decoding clients are responsible for avoiding ill effects from handling the same message more than once. Clients may wish to record the last LSN they saw when decoding and skip over any repeated data or (when using the replication protocol) request that decoding start from that LSN rather than letting the server determine the start point. The Replication Progress Tracking feature is designed for this purpose, refer to [replication origins](https://www.postgresql.org/docs/13/replication-origins.html).

Multiple independent slots may exist for a single database. Each slot has its own state, allowing different consumers to receive changes from different points in the database change stream. For most applications, a separate slot will be required for each consumer.

A logical replication slot knows nothing about the state of the receiver(s). It's even possible to have multiple different receivers using the same slot at different times; they'll just get the changes following on from when the last receiver stopped consuming them. Only one receiver may consume changes from a slot at any given time.

#### Caution

Replication slots persist across crashes and know nothing about the state of their consumer(s). They will prevent removal of required resources even when there is no connection using them. This consumes storage because neither required WAL nor required rows from the system catalogs can be removed by `VACUUM` as long as they are required by a replication slot. In extreme cases this could cause the database to shut down to prevent transaction ID wraparound (see [Section 24.1.5](https://www.postgresql.org/docs/13/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND)). So if a slot is no longer required it should be dropped.

## 48.2.3. Output Plugins

Output plugins transform the data from the write-ahead log's internal representation into the format the consumer of a replication slot desires.

## 48.2.4. Exported Snapshots

When a new replication slot is created using the streaming replication interface (see [CREATE\_REPLICATION\_SLOT](https://www.postgresql.org/docs/13/protocol-replication.html#PROTOCOL-REPLICATION-CREATE-SLOT)), a snapshot is exported (see [Section 9.27.5](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)), which will show exactly the state of the database after which all changes will be included in the change stream. This can be used to create a new replica by using [`SET TRANSACTION SNAPSHOT`](https://www.postgresql.org/docs/13/sql-set-transaction.html) to read the state of the database at the moment the slot was created. This transaction can then be used to dump the database's state at that point in time, which afterwards can be updated using the slot's contents without losing any changes.

Creation of a snapshot is not always possible. In particular, it will fail when connected to a hot standby. Applications that do not require snapshot export may suppress it with the `NOEXPORT_SNAPSHOT` option.\
