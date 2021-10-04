# 48.3. Streaming Replication Protocol Interface

The commands

* `CREATE_REPLICATION_SLOT` _`slot_name`_ LOGICAL _`output_plugin`_
* `DROP_REPLICATION_SLOT` _`slot_name`_ \[ `WAIT` \]
* `START_REPLICATION SLOT` _`slot_name`_ LOGICAL ...

are used to create, drop, and stream changes from a replication slot, respectively. These commands are only available over a replication connection; they cannot be used via SQL. See [Section 52.4](https://www.postgresql.org/docs/13/protocol-replication.html) for details on these commands.

The command [pg\_recvlogical](https://www.postgresql.org/docs/13/app-pgrecvlogical.html) can be used to control logical decoding over a streaming replication connection. \(It uses these commands internally.\)

