<a id="RECOVERY-CONFIG"></a>

# O.1. recovery.conf file merged into postgresql.conf

<a id="id-1.11.16.3.2"></a>

PostgreSQL 11 and below used a configuration file named `recovery.conf` <a id="id-1.11.16.3.3.2"></a> to manage replicas and standbys. Support for this file was removed in PostgreSQL 12. See [the release notes for PostgreSQL 12](../release-notes/e.4.-prior-releases.md) for details on this change.

On PostgreSQL 12 and above, [archive recovery, streaming replication, and PITR](../../server-administration/backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md) are configured using [normal server configuration parameters](../../server-administration/server-configuration/replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY). These are set in `postgresql.conf` or via [ALTER SYSTEM](../../reference/sql-commands/alter-system.md) like any other parameter.

The server will not start if a `recovery.conf` exists.

The `trigger_file` <a id="id-1.11.16.3.6.2"></a> setting has been renamed to [promote_trigger_file](../../server-administration/server-configuration/replication.md#GUC-PROMOTE-TRIGGER-FILE).

The `standby_mode` <a id="id-1.11.16.3.7.2"></a> setting has been removed. A `standby.signal` file in the data directory is used instead. See [Standby Server Operation](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#STANDBY-SERVER-OPERATION) for details.

---

原文：[PostgreSQL 15.19 Documentation](recovery-config.md)（英文原文，待翻譯）
