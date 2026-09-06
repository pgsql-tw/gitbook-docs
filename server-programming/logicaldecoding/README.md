## Chapter 47. Logical Decoding

**Table of Contents**

[47.1. Logical Decoding Examples](logicaldecoding-example.md)

[47.2. Logical Decoding Concepts](logicaldecoding-explanation.md)
:   [47.2.1. Logical Decoding](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)

    [47.2.2. Replication Slots](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)

    [47.2.3. Replication Slot Synchronization](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

    [47.2.4. Output Plugins](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

    [47.2.5. Exported Snapshots](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

[47.3. Streaming Replication Protocol Interface](logicaldecoding-walsender.md)

[47.4. Logical Decoding SQL Interface](logicaldecoding-sql.md)

[47.5. System Catalogs Related to Logical Decoding](logicaldecoding-catalogs.md)

[47.6. Logical Decoding Output Plugins](logicaldecoding-output-plugin.md)
:   [47.6.1. Initialization Function](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-INIT)

    [47.6.2. Capabilities](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)

    [47.6.3. Output Modes](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)

    [47.6.4. Output Plugin Callbacks](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)

    [47.6.5. Functions for Producing Output](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

[47.7. Logical Decoding Output Writers](logicaldecoding-writer.md)

[47.8. Synchronous Replication Support for Logical Decoding](logicaldecoding-synchronous.md)
:   [47.8.1. Overview](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

    [47.8.2. Caveats](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

[47.9. Streaming of Large Transactions for Logical Decoding](logicaldecoding-streaming.md)

[47.10. Two-phase Commit Support for Logical Decoding](logicaldecoding-two-phase-commits.md)

<a id="id-1.8.14.2"></a>

PostgreSQL provides infrastructure to stream the modifications performed
via SQL to external consumers. This functionality can be used for a
variety of purposes, including replication solutions and auditing.

Changes are sent out in streams identified by logical replication slots.

The format in which those changes are streamed is determined by the output
plugin used. An example plugin is provided in the PostgreSQL distribution.
Additional plugins can be
written to extend the choice of available formats without modifying any
core code.
Every output plugin has access to each individual new row produced
by `INSERT` and the new row version created
by `UPDATE`. Availability of old row versions for
`UPDATE` and `DELETE` depends on
the configured replica identity (see [`REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)).

Changes can be consumed either using the streaming replication protocol
(see [Section 54.4](../../internals/protocol/protocol-replication.md) and
[Section 47.3](logicaldecoding-walsender.md)), or by calling functions
via SQL (see [Section 47.4](logicaldecoding-sql.md)). It is also possible
to write additional methods of consuming the output of a replication slot
without modifying core code
(see [Section 47.7](logicaldecoding-writer.md)).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding.html)（英文原文，待翻譯）
