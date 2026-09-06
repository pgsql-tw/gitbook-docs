## 29.1. Publication [#](#LOGICAL-REPLICATION-PUBLICATION)

[29.1.1. Replica Identity](logical-replication-publication.md#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

A *publication* can be defined on any physical
replication primary. The node where a publication is defined is referred to
as *publisher*. A publication is a set of changes
generated from a table or a group of tables, and might also be described as
a change set or replication set. Each publication exists in only one database.

Publications are different from schemas and do not affect how the table is
accessed. Each table can be added to multiple publications if needed.
Publications may currently only contain tables and all tables in schema.
Objects must be added explicitly, except when a publication is created for
`ALL TABLES`.

Publications can choose to limit the changes they produce to
any combination of `INSERT`, `UPDATE`,
`DELETE`, and `TRUNCATE`, similar to how triggers are fired by
particular event types. By default, all operation types are replicated.
These publication specifications apply only for DML operations; they do not affect the initial
data synchronization copy. (Row filters have no effect for
`TRUNCATE`. See [Section 29.4](logical-replication-row-filter.md)).

Every publication can have multiple subscribers.

A publication is created using the [`CREATE PUBLICATION`](../../reference/sql-commands/sql-createpublication.md)
command and may later be altered or dropped using corresponding commands.

The individual tables can be added and removed dynamically using
[`ALTER PUBLICATION`](../../reference/sql-commands/sql-alterpublication.md). Both the `ADD
TABLE` and `DROP TABLE` operations are
transactional, so the table will start or stop replicating at the correct
snapshot once the transaction has committed.

<a id="LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY"></a>

### 29.1.1. Replica Identity [#](#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

A published table must have a *replica identity*
configured in order to be able to replicate `UPDATE`
and `DELETE` operations, so that appropriate rows to
update or delete can be identified on the subscriber side.

By default, this is the primary key, if there is one. Another unique index
(with certain additional requirements) can also be set to be the replica
identity. If the table does not have any suitable key, then it can be set
to replica identity `FULL`, which means the entire row
becomes the key. When replica identity `FULL` is
specified, indexes can be used on the subscriber side for searching the
rows. Candidate indexes must be btree or hash, non-partial, and the
leftmost index field must be a column (not an expression) that references
the published table column. These restrictions on the non-unique index
properties adhere to some of the restrictions that are enforced for
primary keys. If there are no such suitable indexes, the search on the
subscriber side can be very inefficient, therefore replica identity
`FULL` should only be used as a fallback if no other
solution is possible.

If a replica identity other than `FULL` is set on the
publisher side, a replica identity comprising the same or fewer columns
must also be set on the subscriber side.

Tables with a replica identity defined as `NOTHING`,
`DEFAULT` without a primary key, or `USING
INDEX` with a dropped index, cannot support
`UPDATE` or `DELETE` operations when
included in a publication replicating these actions. Attempting such
operations will result in an error on the publisher.

`INSERT` operations can proceed regardless of any replica identity.

See [`ALTER TABLE...REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)
for details on how to set the replica identity.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-publication.html)（英文原文，待翻譯）
