## 29.7. Conflicts [#](#LOGICAL-REPLICATION-CONFLICTS)

Logical replication behaves similarly to normal DML operations in that
the data will be updated even if it was changed locally on the subscriber
node. If incoming data violates any constraints the replication will
stop. This is referred to as a *conflict*. When
replicating `UPDATE` or `DELETE`
operations, missing data is also considered as a
*conflict*, but does not result in an error and such
operations will simply be skipped.

Additional logging is triggered, and the conflict statistics are collected (displayed in the
[`pg_stat_subscription_stats`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS) view)
in the following *conflict* cases:

<a id="CONFLICT-INSERT-EXISTS"></a>

`insert_exists` [#](#CONFLICT-INSERT-EXISTS)
:   Inserting a row that violates a `NOT DEFERRABLE`
    unique constraint. Note that to log the origin and commit
    timestamp details of the conflicting key,
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    should be enabled on the subscriber. In this case, an error will be
    raised until the conflict is resolved manually.
<a id="CONFLICT-UPDATE-ORIGIN-DIFFERS"></a>

`update_origin_differs` [#](#CONFLICT-UPDATE-ORIGIN-DIFFERS)
:   Updating a row that was previously modified by another origin.
    Note that this conflict can only be detected when
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    is enabled on the subscriber. Currently, the update is always applied
    regardless of the origin of the local row.
<a id="CONFLICT-UPDATE-EXISTS"></a>

`update_exists` [#](#CONFLICT-UPDATE-EXISTS)
:   The updated value of a row violates a `NOT DEFERRABLE`
    unique constraint. Note that to log the origin and commit
    timestamp details of the conflicting key,
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    should be enabled on the subscriber. In this case, an error will be
    raised until the conflict is resolved manually. Note that when updating a
    partitioned table, if the updated row value satisfies another partition
    constraint resulting in the row being inserted into a new partition, the
    `insert_exists` conflict may arise if the new row
    violates a `NOT DEFERRABLE` unique constraint.
<a id="CONFLICT-UPDATE-MISSING"></a>

`update_missing` [#](#CONFLICT-UPDATE-MISSING)
:   The row to be updated was not found. The update will simply be
    skipped in this scenario.
<a id="CONFLICT-DELETE-ORIGIN-DIFFERS"></a>

`delete_origin_differs` [#](#CONFLICT-DELETE-ORIGIN-DIFFERS)
:   Deleting a row that was previously modified by another origin. Note that
    this conflict can only be detected when
    [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    is enabled on the subscriber. Currently, the delete is always applied
    regardless of the origin of the local row.
<a id="CONFLICT-DELETE-MISSING"></a>

`delete_missing` [#](#CONFLICT-DELETE-MISSING)
:   The row to be deleted was not found. The delete will simply be
    skipped in this scenario.
<a id="CONFLICT-MULTIPLE-UNIQUE-CONFLICTS"></a>

`multiple_unique_conflicts` [#](#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS)
:   Inserting or updating a row violates multiple
    `NOT DEFERRABLE` unique constraints. Note that to log
    the origin and commit timestamp details of conflicting keys, ensure
    that [`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
    is enabled on the subscriber. In this case, an error will be raised until
    the conflict is resolved manually.

Note that there are other conflict scenarios, such as exclusion constraint
violations. Currently, we do not provide additional details for them in the
log.

The log format for logical replication conflicts is as follows:

```

LOG:  conflict detected on relation "schemaname.tablename": conflict=conflict_type
DETAIL:  detailed_explanation.
{detail_values [; ... ]}.

where detail_values is one of:

    Key (column_name [, ...])=(column_value [, ...])
    existing local row [(column_name [, ...])=](column_value [, ...])
    remote row [(column_name [, ...])=](column_value [, ...])
    replica identity {(column_name [, ...])=(column_value [, ...]) | full [(column_name [, ...])=](column_value [, ...])}
```

The log provides the following information:

`LOG`
:   * *`schemaname`*.*`tablename`*
      identifies the local relation involved in the conflict.
    * *`conflict_type`* is the type of conflict that occurred
      (e.g., `insert_exists`, `update_exists`).

`DETAIL`
:   * *`detailed_explanation`* includes
      the origin, transaction ID, and commit timestamp of the transaction that
      modified the existing local row, if available.
    * The `Key` section includes the key values of the local
      row that violated a unique constraint for
      `insert_exists`, `update_exists` or
      `multiple_unique_conflicts` conflicts.
    * The `existing local row` section includes the local
      row if its origin differs from the remote row for
      `update_origin_differs` or `delete_origin_differs`
      conflicts, or if the key value conflicts with the remote row for
      `insert_exists`, `update_exists` or
      `multiple_unique_conflicts` conflicts.
    * The `remote row` section includes the new row from
      the remote insert or update operation that caused the conflict. Note that
      for an update operation, the column value of the new row will be null
      if the value is unchanged and toasted.
    * The `replica identity` section includes the replica
      identity key values that were used to search for the existing local
      row to be updated or deleted. This may include the full row value
      if the local relation is marked with
      [`REPLICA IDENTITY FULL`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL).
    * *`column_name`* is the column name.
      For `existing local row`, `remote row`,
      and `replica identity full` cases, column names are
      logged only if the user lacks the privilege to access all columns of
      the table. If column names are present, they appear in the same order
      as the corresponding column values.
    * *`column_value`* is the column value.
      The large column values are truncated to 64 bytes.
    * Note that in case of `multiple_unique_conflicts` conflict,
      multiple *`detailed_explanation`*
      and *`detail_values`* lines
      will be generated, each detailing the conflict information associated
      with distinct unique
      constraints.

Logical replication operations are performed with the privileges of the role
which owns the subscription. Permissions failures on target tables will
cause replication conflicts, as will enabled
[row-level security](../../the-sql-language/ddl/ddl-rowsecurity.md) on target tables
that the subscription owner is subject to, without regard to whether any
policy would ordinarily reject the `INSERT`,
`UPDATE`, `DELETE` or
`TRUNCATE` which is being replicated. This restriction on
row-level security may be lifted in a future version of
PostgreSQL.

A conflict that produces an error will stop the replication; it must be
resolved manually by the user. Details about the conflict can be found in
the subscriber's server log.

The resolution can be done either by changing data or permissions on the subscriber so
that it does not conflict with the incoming change or by skipping the
transaction that conflicts with the existing data. When a conflict produces
an error, the replication won't proceed, and the logical replication worker will
emit the following kind of message to the subscriber's server log:

```

ERROR:  conflict detected on relation "public.test": conflict=insert_exists
DETAIL:  Key already exists in unique index "t_pkey", which was modified locally in transaction 740 at 2024-06-26 10:47:04.727375+08.
Key (c)=(1); existing local row (1, 'local'); remote row (1, 'remote').
CONTEXT:  processing remote data for replication origin "pg_16395" during "INSERT" for replication target relation "public.test" in transaction 725 finished at 0/14C0378
```

The LSN of the transaction that contains the change violating the constraint and
the replication origin name can be found from the server log (LSN 0/14C0378 and
replication origin `pg_16395` in the above case). The
transaction that produced the conflict can be skipped by using
[`ALTER SUBSCRIPTION ... SKIP`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP)
with the finish LSN
(i.e., LSN 0/14C0378). The finish LSN could be an LSN at which the transaction
is committed or prepared on the publisher. Alternatively, the transaction can
also be skipped by calling the [`pg_replication_origin_advance()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE) function.
Before using this function, the subscription needs to be disabled temporarily
either by [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE) or, the
subscription can be used with the
[`disable_on_error`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR)
option. Then, you can use `pg_replication_origin_advance()`
function with the *`node_name`* (i.e., `pg_16395`)
and the next LSN of the finish LSN (i.e., 0/14C0379). The current position of
origins can be seen in the [`pg_replication_origin_status`](../../internals/views/view-pg-replication-origin-status.md) system view.
Please note that skipping the whole transaction includes skipping changes that
might not violate any constraint. This can easily make the subscriber
inconsistent.
The additional details regarding conflicting rows, such as their origin and
commit timestamp can be seen in the `DETAIL` line of the
log. But note that this information is only available when
[`track_commit_timestamp`](../runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)
is enabled on the subscriber. Users can use this information to decide
whether to retain the local change or adopt the remote alteration. For
instance, the `DETAIL` line in the above log indicates that
the existing row was modified locally. Users can manually perform a
remote-change-win.

When the
[`streaming`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING)
mode is `parallel`, the finish LSN of failed transactions
may not be logged. In that case, it may be necessary to change the streaming
mode to `on` or `off` and cause the same
conflicts again so the finish LSN of the failed transaction will be written
to the server log. For the usage of finish LSN, please refer to [`ALTER SUBSCRIPTION ...
SKIP`](../../reference/sql-commands/sql-altersubscription.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-conflicts.html)（英文原文，待翻譯）
