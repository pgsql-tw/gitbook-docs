## 29.3. Logical Replication Failover [#](#LOGICAL-REPLICATION-FAILOVER)

To allow subscriber nodes to continue replicating data from the publisher
node even when the publisher node goes down, there must be a physical standby
corresponding to the publisher node. The logical slots on the primary server
corresponding to the subscriptions can be synchronized to the standby server by
specifying `failover = true` when creating subscriptions. See
[Section 47.2.3](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION) for details.
Enabling the
[`failover`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
parameter ensures a seamless transition of those subscriptions after the
standby is promoted. They can continue subscribing to publications on the
new primary server.

Because the slot synchronization logic copies asynchronously, it is
necessary to confirm that replication slots have been synced to the standby
server before the failover happens. To ensure a successful failover, the
standby server must be ahead of the subscriber. This can be achieved by
configuring
[`synchronized_standby_slots`](../runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS).

To confirm that the standby server is indeed ready for failover for a given subscriber, follow these
steps to verify that all the logical replication slots required by that subscriber have been
synchronized to the standby server:

1. On the subscriber node, use the following SQL to identify which replication
   slots should be synced to the standby that we plan to promote. This query
   will return the relevant replication slots associated with the
   failover-enabled subscriptions.

   ```

   /* sub # */ SELECT
                  array_agg(quote_literal(s.subslotname)) AS slots
              FROM  pg_subscription s
              WHERE s.subfailover AND
                    s.subslotname IS NOT NULL;
    slots
   -------
    {'sub1','sub2','sub3'}
   (1 row)
   ```
2. On the subscriber node, use the following SQL to identify which table
   synchronization slots should be synced to the standby that we plan to promote.
   This query needs to be run on each database that includes the failover-enabled
   subscription(s). Note that the table sync slot should be synced to the standby
   server only if the table copy is finished
   (See [Section 52.55](../../internals/catalogs/catalog-pg-subscription-rel.md)).
   We don't need to ensure that the table sync slots are synced in other scenarios
   as they will either be dropped or re-created on the new primary server in those
   cases.

   ```

   /* sub # */ SELECT
                  array_agg(quote_literal(slot_name)) AS slots
              FROM
              (
                  SELECT CONCAT('pg_', srsubid, '_sync_', srrelid, '_', ctl.system_identifier) AS slot_name
                  FROM pg_control_system() ctl, pg_subscription_rel r, pg_subscription s
                  WHERE r.srsubstate = 'f' AND s.oid = r.srsubid AND s.subfailover
              );
    slots
   -------
    {'pg_16394_sync_16385_7394666715149055164'}
   (1 row)
   ```
3. Check that the logical replication slots identified above exist on
   the standby server and are ready for failover.

   ```

   /* standby # */ SELECT slot_name, (synced AND NOT temporary AND invalidation_reason IS NULL) AS failover_ready
                  FROM pg_replication_slots
                  WHERE slot_name IN
                      ('sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164');
     slot_name                                 | failover_ready
   --------------------------------------------+----------------
     sub1                                      | t
     sub2                                      | t
     sub3                                      | t
     pg_16394_sync_16385_7394666715149055164   | t
   (4 rows)
   ```

If all the slots are present on the standby server and the result
(`failover_ready`) of the above SQL query is true, then
existing subscriptions can continue subscribing to publications on the new
primary server.

The first two steps in the above procedure are meant for a
PostgreSQL subscriber. It is recommended to run
these steps on each subscriber node, that will be served by the designated
standby after failover, to obtain the complete list of replication
slots. This list can then be verified in Step 3 to ensure failover readiness.
Non-PostgreSQL subscribers, on the other hand, may
use their own methods to identify the replication slots used by their
respective subscriptions.

In some cases, such as during a planned failover, it is necessary to confirm
that all subscribers, whether PostgreSQL or
non-PostgreSQL, will be able to continue
replication after failover to a given standby server. In such cases, use the
following SQL, instead of performing the first two steps above, to identify
which replication slots on the primary need to be synced to the standby that
is intended for promotion. This query returns the relevant replication slots
associated with all the failover-enabled subscriptions.

```

/* primary # */ SELECT array_agg(quote_literal(r.slot_name)) AS slots
               FROM pg_replication_slots r
               WHERE r.failover AND NOT r.temporary;
 slots
-------
 {'sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164'}
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-failover.html)（英文原文，待翻譯）
