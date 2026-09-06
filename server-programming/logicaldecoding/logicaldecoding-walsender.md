## 47.3. 串流複寫協定介面 [#](#LOGICALDECODING-WALSENDER)

下列命令：

* `CREATE_REPLICATION_SLOT slot_name LOGICAL output_plugin`
* `DROP_REPLICATION_SLOT slot_name` [ `WAIT` ]
* `START_REPLICATION SLOT slot_name LOGICAL ...`

分別用於建立、移除複寫槽，以及從複寫槽串流傳送變更。這些命令只能透過複寫連線使用，無法透過 SQL 使用。詳細資訊請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)。

命令 [pg_recvlogical](../../reference/reference-client/app-pgrecvlogical.md) 可用於透過串流複寫連線控制邏輯解碼。（它會在內部使用這些命令。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-walsender.html)（原文版本：18.6；核對日期：2026-09-06）
