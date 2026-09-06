## O.1. `recovery.conf` file merged into `postgresql.conf` [#](#RECOVERY-CONFIG)

<a id="id-1.11.16.3.2"></a>

PostgreSQL 11 and below used a configuration file named
`recovery.conf`
<a id="id-1.11.16.3.3.2"></a>
to manage replicas and standbys. Support for this file was removed in PostgreSQL 12. See
[the release notes for PostgreSQL 12](../release/release-prior.md) for details
on this change.

On PostgreSQL 12 and above,
[archive recovery, streaming replication, and PITR](../../server-administration/backup/continuous-archiving.md)
are configured using
[normal server configuration parameters](../../server-administration/runtime-config/runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY).
These are set in `postgresql.conf` or via
[ALTER SYSTEM](../../reference/sql-commands/sql-altersystem.md)
like any other parameter.

The server will not start if a `recovery.conf` exists.

PostgreSQL 15 and below had a setting
`promote_trigger_file`, or
`trigger_file` before 12.
Use `pg_ctl promote` or call
`pg_promote()` to promote a standby instead.

The
`standby_mode`
<a id="id-1.11.16.3.7.2"></a>
setting has been removed. A `standby.signal` file in the data directory
is used instead. See [Standby Server Operation](../../server-administration/high-availability/warm-standby.md#STANDBY-SERVER-OPERATION) for details.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/recovery-config.html)（英文原文，待翻譯）
