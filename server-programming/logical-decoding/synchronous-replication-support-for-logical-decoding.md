# 49.8. Synchronous Replication Support for Logical Decoding

Logical decoding can be used to build [synchronous replication](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#SYNCHRONOUS-REPLICATION) solutions with the same user interface as synchronous replication for [streaming replication](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#STREAMING-REPLICATION). To do this, the streaming replication interface (see [Section 48.3](streaming-replication-protocol-interface.md)) must be used to stream out data. Clients have to send `Standby status update (F)` (see [Section 52.4](../../internals/52.-frontend-backend-protocol/streaming-replication-protocol.md)) messages, just like streaming replication clients do.

#### Note

A synchronous replica receiving changes via logical decoding will work in the scope of a single database. Since, in contrast to that, _`synchronous_standby_names`_ currently is server wide, this means this technique will not work properly if more than one database is actively used.
