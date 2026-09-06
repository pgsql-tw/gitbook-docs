## 28.2. Data Checksums [#](#CHECKSUMS)

[28.2.1. Off-line Enabling of Checksums](checksums.md#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

<a id="id-1.6.15.4.2"></a>

By default, data pages are protected by checksums, but this can
optionally be disabled for a cluster. When enabled, each data page includes
a checksum that is updated when the page is written and verified each time
the page is read. Only data pages are protected by checksums; internal data
structures and temporary files are not.

Checksums can be disabled when the cluster is initialized using [initdb](../../reference/reference-server/app-initdb.md#APP-INITDB-DATA-CHECKSUMS).
They can also be enabled or disabled at a later time as an offline
operation. Data checksums are enabled or disabled at the full cluster
level, and cannot be specified individually for databases or tables.

The current state of checksums in the cluster can be verified by viewing the
value of the read-only configuration variable [data_checksums](../runtime-config/runtime-config-preset.md#GUC-DATA-CHECKSUMS) by issuing the command `SHOW
data_checksums`.

When attempting to recover from page corruptions, it may be necessary to
bypass the checksum protection. To do this, temporarily set the
configuration parameter [ignore_checksum_failure](../runtime-config/runtime-config-developer.md#GUC-IGNORE-CHECKSUM-FAILURE).

<a id="CHECKSUMS-OFFLINE-ENABLE-DISABLE"></a>

### 28.2.1. Off-line Enabling of Checksums [#](#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

The [pg_checksums](../../reference/reference-server/app-pgchecksums.md)
application can be used to enable or disable data checksums, as well as
verify checksums, on an offline cluster.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/checksums.html)（英文原文，待翻譯）
