# 49.4. Logical Decoding SQL Interface

See [Section 9.27.6](../../the-sql-language/functions-and-operators/system-administration.md#FUNCTIONS-REPLICATION) for detailed documentation on the SQL-level API for interacting with logical decoding.

Synchronous replication (see [Section 26.2.8](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#SYNCHRONOUS-REPLICATION)) is only supported on replication slots used over the streaming replication interface. The function interface and additional, non-core interfaces do not support synchronous replication.
