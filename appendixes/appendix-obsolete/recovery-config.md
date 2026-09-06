## O.1. `recovery.conf` 檔案已併入 `postgresql.conf` [#](#RECOVERY-CONFIG)

<a id="id-1.11.16.3.2"></a>

PostgreSQL 11 及更早版本使用名為
`recovery.conf` 的設定檔
<a id="id-1.11.16.3.3.2"></a>
管理複本與待命伺服器。PostgreSQL 12 已移除對此檔案的支援。關於此變更的詳細資訊，請參閱
[PostgreSQL 12 的發行說明](../release/release-prior.md)。

在 PostgreSQL 12 及以上版本中，
[歸檔復原、串流複寫與 PITR](../../server-administration/backup/continuous-archiving.md)
使用
[一般伺服器設定參數](../../server-administration/runtime-config/runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)進行設定。
如同其他參數，這些參數可在 `postgresql.conf` 中設定，或透過
[ALTER SYSTEM](../../reference/sql-commands/sql-altersystem.md)設定。

若存在 `recovery.conf`，伺服器將無法啟動。

PostgreSQL 15 及更早版本具有
`promote_trigger_file`, or
`trigger_file` before 12.
請改用 `pg_ctl promote` 或呼叫
`pg_promote()` 來提升待命伺服器。

已移除
`standby_mode`
<a id="id-1.11.16.3.7.2"></a>
設定。現在改用資料目錄中的 `standby.signal` 檔案。詳細資訊請參閱[待命伺服器運作](../../server-administration/high-availability/warm-standby.md#STANDBY-SERVER-OPERATION)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/recovery-config.html)（英文原文，待翻譯）
