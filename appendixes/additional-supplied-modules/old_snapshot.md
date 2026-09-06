<a id="OLDSNAPSHOT"></a>

# F.24. old_snapshot

[F.24.1. Functions](#id-1.11.7.33.4)

<a id="id-1.11.7.33.2"></a>

The `old_snapshot` module allows inspection of the server state that is used to implement [old_snapshot_threshold](https://www.postgresql.org/docs/15/runtime-config-resource.html#GUC-OLD-SNAPSHOT-THRESHOLD).

<a id="id-1.11.7.33.4"></a>

## F.24.1. Functions

`pg_old_snapshot_time_mapping(array_offset OUT int4, end_timestamp OUT timestamptz, newest_xmin OUT xid) returns setof record`

Returns all of the entries in the server's timestamp to XID mapping. Each entry represents the newest xmin of any snapshot taken in the corresponding minute.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/oldsnapshot.html)（英文原文，待翻譯）
