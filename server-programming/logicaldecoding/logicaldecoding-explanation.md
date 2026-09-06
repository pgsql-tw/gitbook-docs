## 47.2. Logical Decoding Concepts [#](#LOGICALDECODING-EXPLANATION)

[47.2.1. Logical Decoding](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)

[47.2.2. Replication Slots](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)

[47.2.3. Replication Slot Synchronization](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

[47.2.4. Output Plugins](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

[47.2.5. Exported Snapshots](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

<a id="LOGICALDECODING-EXPLANATION-LOG-DEC"></a>

### 47.2.1. Logical Decoding [#](#LOGICALDECODING-EXPLANATION-LOG-DEC)

<a id="id-1.8.14.8.2.2"></a>

Logical decoding is the process of extracting all persistent changes
to a database's tables into a coherent, easy to understand format which
can be interpreted without detailed knowledge of the database's internal
state.

In PostgreSQL, logical decoding is implemented
by decoding the contents of the [write-ahead
log](../../server-administration/wal/README.md), which describe changes on a storage level, into an
application-specific form such as a stream of tuples or SQL statements.

<a id="LOGICALDECODING-REPLICATION-SLOTS"></a>

### 47.2.2. Replication Slots [#](#LOGICALDECODING-REPLICATION-SLOTS)

<a id="id-1.8.14.8.3.2"></a>

In the context of logical replication, a slot represents a stream of
changes that can be replayed to a client in the order they were made on
the origin server. Each slot streams a sequence of changes from a single
database.

### Note

PostgreSQL also has streaming replication slots
(see [Section 26.2.5](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)), but they are used somewhat
differently there.

A replication slot has an identifier that is unique across all databases
in a PostgreSQL cluster. Slots persist
independently of the connection using them and are crash-safe.

A logical slot will emit each change just once in normal operation.
The current position of each slot is persisted only at checkpoint, so in
the case of a crash the slot might return to an earlier LSN, which will
then cause recent changes to be sent again when the server restarts.
Logical decoding clients are responsible for avoiding ill effects from
handling the same message more than once. Clients may wish to record
the last LSN they saw when decoding and skip over any repeated data or
(when using the replication protocol) request that decoding start from
that LSN rather than letting the server determine the start point.
The Replication Progress Tracking feature is designed for this purpose,
refer to [replication origins](../replication-origins/README.md).

Multiple independent slots may exist for a single database. Each slot has
its own state, allowing different consumers to receive changes from
different points in the database change stream. For most applications, a
separate slot will be required for each consumer.

A logical replication slot knows nothing about the state of the
receiver(s). It's even possible to have multiple different receivers using
the same slot at different times; they'll just get the changes following
on from when the last receiver stopped consuming them. Only one receiver
may consume changes from a slot at any given time.

A logical replication slot can also be created on a hot standby. To prevent
`VACUUM` from removing required rows from the system
catalogs, `hot_standby_feedback` should be set on the
standby. In spite of that, if any required rows get removed, the slot gets
invalidated. It's highly recommended to use a physical slot between the
primary and the standby. Otherwise, `hot_standby_feedback`
will work but only while the connection is alive (for example a node
restart would break it). Then, the primary may delete system catalog rows
that could be needed by the logical decoding on the standby (as it does
not know about the `catalog_xmin` on the standby).
Existing logical slots on standby also get invalidated if
`wal_level` on the primary is reduced to less than
`logical`.
This is done as soon as the standby detects such a change in the WAL stream.
It means that, for walsenders that are lagging (if any), some WAL records up
to the `wal_level` parameter change on the primary won't be
decoded.

Creation of a logical slot requires information about all the currently
running transactions. On the primary, this information is available
directly, but on a standby, this information has to be obtained from
primary. Thus, slot creation may need to wait for some activity to happen
on the primary. If the primary is idle, creating a logical slot on
standby may take noticeable time. This can be sped up by calling the
`pg_log_standby_snapshot` function on the primary.

### Caution

Replication slots persist across crashes and know nothing about the state
of their consumer(s). They will prevent removal of required resources
even when there is no connection using them. This consumes storage
because neither required WAL nor required rows from the system catalogs
can be removed by `VACUUM` as long as they are required by a replication
slot. In extreme cases this could cause the database to shut down to prevent
transaction ID wraparound (see [Section 24.1.5](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)).
So if a slot is no longer required it should be dropped.

<a id="LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION"></a>

### 47.2.3. Replication Slot Synchronization [#](#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

The logical replication slots on the primary can be synchronized to
the hot standby by using the `failover` parameter of
[`pg_create_logical_replication_slot`](../../the-sql-language/functions/functions-admin.md#PG-CREATE-LOGICAL-REPLICATION-SLOT), or by
using the [`failover`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) option of
`CREATE SUBSCRIPTION` during slot creation.
Additionally, enabling [`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS) on the standby
is required. By enabling [`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS)
on the standby, the failover slots can be synchronized periodically in
the slotsync worker. For the synchronization to work, it is mandatory to
have a physical replication slot between the primary and the standby (i.e.,
[`primary_slot_name`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)
should be configured on the standby), and
[`hot_standby_feedback`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK)
must be enabled on the standby. It is also necessary to specify a valid
`dbname` in the
[`primary_conninfo`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-CONNINFO).
It's highly recommended that the said physical replication slot is named in
[`synchronized_standby_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS)
list on the primary, to prevent the subscriber from consuming changes
faster than the hot standby. Even when correctly configured, some latency
is expected when sending changes to logical subscribers due to the waiting
on slots named in
[`synchronized_standby_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS).
When `synchronized_standby_slots` is utilized, the
primary server will not completely shut down until the corresponding
standbys, associated with the physical replication slots specified
in `synchronized_standby_slots`, have confirmed
receiving the WAL up to the latest flushed position on the primary server.

### Note

While enabling [`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS) allows for automatic
periodic synchronization of failover slots, they can also be manually
synchronized using the [`pg_sync_replication_slots`](../../the-sql-language/functions/functions-admin.md#PG-SYNC-REPLICATION-SLOTS) function on the standby.
However, this function is primarily intended for testing and debugging and
should be used with caution. Unlike automatic synchronization, it does not
include cyclic retries, making it more prone to synchronization failures,
particularly during initial sync scenarios where the required WAL files
or catalog rows for the slot might have already been removed or are at risk
of being removed on the standby. In contrast, automatic synchronization
via `sync_replication_slots` provides continuous slot
updates, enabling seamless failover and supporting high availability.
Therefore, it is the recommended method for synchronizing slots.

When slot synchronization is configured as recommended,
and the initial synchronization is performed either automatically or
manually via `pg_sync_replication_slots`, the standby
can persist the synchronized slot only if the following condition is met:
The logical replication slot on the primary must retain WALs and system
catalog rows that are still available on the standby. This ensures data
integrity and allows logical replication to continue smoothly after
promotion.
If the required WALs or catalog rows have already been purged from the
standby, the slot will not be persisted to avoid data loss. In such
cases, the following log message may appear:

```

LOG:  could not synchronize replication slot "failover_slot"
DETAIL:  Synchronization could lead to data loss, because the remote slot needs WAL at LSN 0/3003F28 and catalog xmin 754, but the standby has LSN 0/3003F28 and catalog xmin 756.
```

If the logical replication slot is actively used by a consumer, no
manual intervention is needed; the slot will advance automatically,
and synchronization will resume in the next cycle. However, if no
consumer is configured, it is advisable to manually advance the slot
on the primary using [`pg_logical_slot_get_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-GET-CHANGES) or
[`pg_logical_slot_get_binary_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-GET-BINARY-CHANGES),
allowing synchronization to proceed.

The ability to resume logical replication after failover depends upon the
[pg_replication_slots](../../internals/views/view-pg-replication-slots.md).`synced`
value for the synchronized slots on the standby at the time of failover.
Only persistent slots that have attained synced state as true on the standby
before failover can be used for logical replication after failover.
Temporary synced slots cannot be used for logical decoding, therefore
logical replication for those slots cannot be resumed. For example, if the
synchronized slot could not become persistent on the standby due to a
disabled subscription, then the subscription cannot be resumed after
failover even when it is enabled.

To resume logical replication after failover from the synced logical
slots, the subscription's 'conninfo' must be altered to point to the
new primary server. This is done using
[`ALTER SUBSCRIPTION ... CONNECTION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION).
It is recommended that subscriptions are first disabled before promoting
the standby and are re-enabled after altering the connection string.

### Caution

There is a chance that the old primary is up again during the promotion
and if subscriptions are not disabled, the logical subscribers may
continue to receive data from the old primary server even after promotion
until the connection string is altered. This might result in data
inconsistency issues, preventing the logical subscribers from being
able to continue replication from the new primary server.

<a id="LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS"></a>

### 47.2.4. Output Plugins [#](#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

Output plugins transform the data from the write-ahead log's internal
representation into the format the consumer of a replication slot desires.

<a id="LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS"></a>

### 47.2.5. Exported Snapshots [#](#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

When a new replication slot is created using the streaming replication
interface (see [CREATE_REPLICATION_SLOT](../../internals/protocol/protocol-replication.md#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT)), a
snapshot is exported
(see [Section 9.28.5](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)), which will show
exactly the state of the database after which all changes will be
included in the change stream. This can be used to create a new replica by
using [`SET TRANSACTION
SNAPSHOT`](../../reference/sql-commands/sql-set-transaction.md) to read the state of the database at the moment
the slot was created. This transaction can then be used to dump the
database's state at that point in time, which afterwards can be updated
using the slot's contents without losing any changes.

Applications that do not require
snapshot export may suppress it with the `SNAPSHOT 'nothing'`
option.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-explanation.html)（英文原文，待翻譯）
