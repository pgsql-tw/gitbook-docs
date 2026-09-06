## 47.4. Logical Decoding SQL Interface [#](#LOGICALDECODING-SQL)

See [Section 9.28.6](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-REPLICATION) for detailed documentation on
the SQL-level API for interacting with logical decoding.

Synchronous replication (see [Section 26.2.8](../../server-administration/high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION)) is
only supported on replication slots used over the streaming replication interface. The
function interface and additional, non-core interfaces do not support
synchronous replication.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-sql.html)（英文原文，待翻譯）
