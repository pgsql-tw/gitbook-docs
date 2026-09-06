<a id="RECOVERY-CONFIG"></a>

# O.1. recovery.conf 檔案併入 postgresql.conf

<a id="id-1.11.16.3.2"></a>

PostgreSQL 11 及更早版本使用名為 `recovery.conf` 的設定檔 <a id="id-1.11.16.3.3.2"></a> 管理複本與備援伺服器。PostgreSQL 12 已移除對此檔案的支援。關於這項變更的詳細資訊，請參閱 [PostgreSQL 12 發布說明](../release-notes/e.4.-prior-releases.md)。

在 PostgreSQL 12 及更新版本中，[封存復原、串流複寫及 PITR](../../server-administration/backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md) 使用[一般伺服器設定參數](../../server-administration/server-configuration/replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)設定。這些參數與其他參數相同，可在 `postgresql.conf` 中設定，或透過 [ALTER SYSTEM](../../reference/sql-commands/alter-system.md) 設定。

若 `recovery.conf` 存在，伺服器將無法啟動。

`trigger_file` <a id="id-1.11.16.3.6.2"></a> 設定已更名為 [promote_trigger_file](../../server-administration/server-configuration/replication.md#GUC-PROMOTE-TRIGGER-FILE)。

`standby_mode` <a id="id-1.11.16.3.7.2"></a> 設定已移除，改為在資料目錄中使用 `standby.signal` 檔案。詳細資訊請參閱[備援伺服器操作](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#STANDBY-SERVER-OPERATION)。

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/recovery-config.html)
