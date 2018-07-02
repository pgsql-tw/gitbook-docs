# 51.11 pg\_class

The catalog `pg_class` catalogs tables and most everything else that has columns or is otherwise similar to a table. This includes indexes \(but see also `pg_index`\), sequences \(but see also`pg_sequence`\), views, materialized views, composite types, and TOAST tables; see `relkind`. Below, when we mean all of these kinds of objects we speak of “relations”. Not all columns are meaningful for all relation types.

**Table 51.11. `pg_class` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `relname` | `name` |   | Name of the table, index, view, etc. |
| `relnamespace` | `oid` | [`pg_namespace`](https://www.postgresql.org/docs/10/static/catalog-pg-namespace.html).oid | The OID of the namespace that contains this relation |
| `reltype` | `oid` | [`pg_type`](https://www.postgresql.org/docs/10/static/catalog-pg-type.html).oid | The OID of the data type that corresponds to this table's row type, if any \(zero for indexes, which have no `pg_type` entry\) |
| `reloftype` | `oid` | [`pg_type`](https://www.postgresql.org/docs/10/static/catalog-pg-type.html).oid | For typed tables, the OID of the underlying composite type, zero for all other relations |
| `relowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the relation |
| `relam` | `oid` | [`pg_am`](https://www.postgresql.org/docs/10/static/catalog-pg-am.html).oid | If this is an index, the access method used \(B-tree, hash, etc.\) |
| `relfilenode` | `oid` |   | Name of the on-disk file of this relation; zero means this is a “mapped” relation whose disk file name is determined by low-level state |
| `reltablespace` | `oid` | [`pg_tablespace`](https://www.postgresql.org/docs/10/static/catalog-pg-tablespace.html).oid | The tablespace in which this relation is stored. If zero, the database's default tablespace is implied. \(Not meaningful if the relation has no on-disk file.\) |
| `relpages` | `int4` |   | Size of the on-disk representation of this table in pages \(of size `BLCKSZ`\). This is only an estimate used by the planner. It is updated by `VACUUM`, `ANALYZE`, and a few DDL commands such as `CREATE INDEX`. |
| `reltuples` | `float4` |   | Number of rows in the table. This is only an estimate used by the planner. It is updated by `VACUUM`, `ANALYZE`, and a few DDL commands such as `CREATE INDEX`. |
| `relallvisible` | `int4` |   | Number of pages that are marked all-visible in the table's visibility map. This is only an estimate used by the planner. It is updated by `VACUUM`, `ANALYZE`, and a few DDL commands such as `CREATE INDEX`. |
| `reltoastrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | OID of the TOAST table associated with this table, 0 if none. The TOAST table stores large attributes “out of line” in a secondary table. |
| `relhasindex` | `bool` |   | True if this is a table and it has \(or recently had\) any indexes |
| `relisshared` | `bool` |   | True if this table is shared across all databases in the cluster. Only certain system catalogs \(such as `pg_database`\) are shared. |
| `relpersistence` | `char` |   | `p` = permanent table, `u` = unlogged table, `t` = temporary table |
| `relkind` | `char` |   | `r` = ordinary table, `i` = index, `S` = sequence, `t` = TOAST table, `v` = view, `m` = materialized view, `c` = composite type, `f` = foreign table, `p` = partitioned table |
| `relnatts` | `int2` |   | Number of user columns in the relation \(system columns not counted\). There must be this many corresponding entries in`pg_attribute`. See also `pg_attribute.attnum`. |
| `relchecks` | `int2` |   | Number of `CHECK` constraints on the table; see [`pg_constraint`](https://www.postgresql.org/docs/10/static/catalog-pg-constraint.html) catalog |
| `relhasoids` | `bool` |   | True if we generate an OID for each row of the relation |
| `relhaspkey` | `bool` |   | True if the table has \(or once had\) a primary key |
| `relhasrules` | `bool` |   | True if table has \(or once had\) rules; see [`pg_rewrite`](https://www.postgresql.org/docs/10/static/catalog-pg-rewrite.html) catalog |
| `relhastriggers` | `bool` |   | True if table has \(or once had\) triggers; see [`pg_trigger`](https://www.postgresql.org/docs/10/static/catalog-pg-trigger.html) catalog |
| `relhassubclass` | `bool` |   | True if table has \(or once had\) any inheritance children |
| `relrowsecurity` | `bool` |   | True if table has row level security enabled; see [`pg_policy`](https://www.postgresql.org/docs/10/static/catalog-pg-policy.html) catalog |
| `relforcerowsecurity` | `bool` |   | True if row level security \(when enabled\) will also apply to table owner; see [`pg_policy`](https://www.postgresql.org/docs/10/static/catalog-pg-policy.html) catalog |
| `relispopulated` | `bool` |   | True if relation is populated \(this is true for all relations other than some materialized views\) |
| `relreplident` | `char` |   | Columns used to form “replica identity” for rows: `d` = default \(primary key, if any\), `n` = nothing, `f` = all columns `i` = index with `indisreplident` set, or default |
| `relispartition` | `bool` |   | True if table is a partition |
| `relfrozenxid` | `xid` |   | All transaction IDs before this one have been replaced with a permanent \(“frozen”\) transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent transaction ID wraparound or to allow `pg_xact` to be shrunk. Zero \(`InvalidTransactionId`\) if the relation is not a table. |
| `relminmxid` | `xid` |   | All multixact IDs before this one have been replaced by a transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent multixact ID wraparound or to allow `pg_multixact` to be shrunk. Zero \(`InvalidMultiXactId`\) if the relation is not a table. |
| `relacl` | `aclitem[]` |   | Access privileges; see [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html) for details |
| `reloptions` | `text[]` |   | Access-method-specific options, as “keyword=value” strings |
| `relpartbound` | `pg_node_tree` |   | If table is a partition \(see `relispartition`\), internal representation of the partition bound |

Several of the Boolean flags in `pg_class` are maintained lazily: they are guaranteed to be true if that's the correct state, but may not be reset to false immediately when the condition is no longer true. For example, `relhasindex` is set by `CREATE INDEX`, but it is never cleared by `DROP INDEX`. Instead, `VACUUM` clears `relhasindex` if it finds the table has no indexes. This arrangement avoids race conditions and improves concurrency.

