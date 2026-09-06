<a id="OLDSNAPSHOT"></a>

# F.24. old_snapshot

[F.24.1. 函式](#id-1.11.7.33.4)

<a id="id-1.11.7.33.2"></a>

`old_snapshot` 模組可檢視伺服器用來實作 [old_snapshot_threshold](../../server-administration/server-configuration/resource-consumption.md#GUC-OLD-SNAPSHOT-THRESHOLD) 的狀態。

<a id="id-1.11.7.33.4"></a>

## F.24.1. 函式

`pg_old_snapshot_time_mapping(array_offset OUT int4, end_timestamp OUT timestamptz, newest_xmin OUT xid) returns setof record`

傳回伺服器時間戳記至 XID 對應中的所有項目。每個項目代表相應分鐘內所取得任何快照的最新 xmin。

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/old-snapshot.html)
