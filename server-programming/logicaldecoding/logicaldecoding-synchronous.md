## 47.8. Synchronous Replication Support for Logical Decoding [#](#LOGICALDECODING-SYNCHRONOUS)

[47.8.1. Overview](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

[47.8.2. Caveats](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

<a id="LOGICALDECODING-SYNCHRONOUS-OVERVIEW"></a>

### 47.8.1. Overview [#](#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

Logical decoding can be used to build
[synchronous
replication](../../server-administration/high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION) solutions with the same user interface as synchronous
replication for [streaming
replication](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION). To do this, the streaming replication interface
(see [Section 47.3](logicaldecoding-walsender.md)) must be used to stream out
data. Clients have to send `Standby status update (F)`
(see [Section 54.4](../../internals/protocol/protocol-replication.md)) messages, just like streaming
replication clients do.

### Note

A synchronous replica receiving changes via logical decoding will work in
the scope of a single database. Since, in contrast to
that, *`synchronous_standby_names`* currently is
server wide, this means this technique will not work properly if more
than one database is actively used.

<a id="LOGICALDECODING-SYNCHRONOUS-CAVEATS"></a>

### 47.8.2. Caveats [#](#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

In synchronous replication setup, a deadlock can happen, if the transaction
has locked [user] catalog tables exclusively. See
[Section 47.6.2](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES) for information on user
catalog tables. This is because logical decoding of transactions can lock
catalog tables to access them. To avoid this users must refrain from taking
an exclusive lock on [user] catalog tables. This can happen in the following
ways:

* Issuing an explicit `LOCK` on `pg_class`
  in a transaction.
* Perform `CLUSTER` on `pg_class` in
  a transaction.
* `PREPARE TRANSACTION` after `LOCK` command
  on `pg_class` and allow logical decoding of two-phase
  transactions.
* `PREPARE TRANSACTION` after `CLUSTER`
  command on `pg_trigger` and allow logical decoding of
  two-phase transactions. This will lead to deadlock only when published table
  have a trigger.
* Executing `TRUNCATE` on [user] catalog table in a
  transaction.

Note that these commands can cause deadlocks not only for the system
catalog tables listed above but for other catalog tables.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-synchronous.html)（英文原文，待翻譯）
