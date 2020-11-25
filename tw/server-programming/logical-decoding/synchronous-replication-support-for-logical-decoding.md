# 48.8. Synchronous Replication Support for Logical Decoding

Logical decoding can be used to build [synchronous replication](https://www.postgresql.org/docs/13/warm-standby.html#SYNCHRONOUS-REPLICATION) solutions with the same user interface as synchronous replication for [streaming replication](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION). To do this, the streaming replication interface \(see [Section 48.3](https://www.postgresql.org/docs/13/logicaldecoding-walsender.html)\) must be used to stream out data. Clients have to send `Standby status update (F)` \(see [Section 52.4](https://www.postgresql.org/docs/13/protocol-replication.html)\) messages, just like streaming replication clients do.

#### Note

A synchronous replica receiving changes via logical decoding will work in the scope of a single database. Since, in contrast to that, _`synchronous_standby_names`_ currently is server wide, this means this technique will not work properly if more than one database is actively used.

