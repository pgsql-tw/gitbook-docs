# 48.4. Logical Decoding SQL Interface

See [Section 9.27.6](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-REPLICATION) for detailed documentation on the SQL-level API for interacting with logical decoding.

Synchronous replication \(see [Section 26.2.8](https://www.postgresql.org/docs/13/warm-standby.html#SYNCHRONOUS-REPLICATION)\) is only supported on replication slots used over the streaming replication interface. The function interface and additional, non-core interfaces do not support synchronous replication.

