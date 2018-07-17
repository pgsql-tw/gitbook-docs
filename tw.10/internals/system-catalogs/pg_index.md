---
description: 版本：10
---

# 51.26 pg\_index

目錄 pg\_index 包含有關索引的部分信息。其餘的大多數是在 pg\_class 中。

**Table 51.26. `pg_index` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `indexrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | 此索引在 pg\_class 中的 OID |
| `indrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | 此索引對應資料表在 pg\_class 中的 OID |
| `indnatts` | `int2` |   | 索引中的欄位數（複製自 pg\_class.relnatts） |
| `indisunique` | `bool` |   | 如果為 true，則這是唯一性索引 |
| `indisprimary` | `bool` |   | 如果為 true，則此索引表示資料表的主鍵（如果為 true，則 indisunique 應始終為true） |
| `indisexclusion` | `bool` |   | 如果為 true，則此索引支援排除限制條件 |
| `indimmediate` | `bool` |   | 如果為 true，則在插入時立即強制執行唯一性檢查（如果 indisunique 不成立則無關緊要） |
| `indisclustered` | `bool` |   | If true, the table was last clustered on this index |
| `indisvalid` | `bool` |   | If true, the index is currently valid for queries. False means the index is possibly incomplete: it must still be modified by `INSERT`/`UPDATE` operations, but it cannot safely be used for queries. If it is unique, the uniqueness property is not guaranteed true either. |
| `indcheckxmin` | `bool` |   | If true, queries must not use the index until the `xmin` of this `pg_index` row is below their `TransactionXmin` event horizon, because the table may contain broken HOT chains with incompatible rows that they can see |
| `indisready` | `bool` |   | If true, the index is currently ready for inserts. False means the index must be ignored by `INSERT`/`UPDATE` operations. |
| `indislive` | `bool` |   | If false, the index is in process of being dropped, and should be ignored for all purposes \(including HOT-safety decisions\) |
| `indisreplident` | `bool` |   | If true this index has been chosen as “replica identity” using `ALTER TABLE ... REPLICA IDENTITY USING INDEX ...` |
| `indkey` | `int2vector` | [`pg_attribute`](https://www.postgresql.org/docs/10/static/catalog-pg-attribute.html).attnum | This is an array of `indnatts` values that indicate which table columns this index indexes. For example a value of `1 3` would mean that the first and the third table columns make up the index key. A zero in this array indicates that the corresponding index attribute is an expression over the table columns, rather than a simple column reference. |
| `indcollation` | `oidvector` | [`pg_collation`](https://www.postgresql.org/docs/10/static/catalog-pg-collation.html).oid | For each column in the index key, this contains the OID of the collation to use for the index, or zero if the column is not of a collatable data type. |
| `indclass` | `oidvector` | [`pg_opclass`](https://www.postgresql.org/docs/10/static/catalog-pg-opclass.html).oid | For each column in the index key, this contains the OID of the operator class to use. See [`pg_opclass`](https://www.postgresql.org/docs/10/static/catalog-pg-opclass.html) for details. |
| `indoption` | `int2vector` |   | This is an array of `indnatts` values that store per-column flag bits. The meaning of the bits is defined by the index's access method. |
| `indexprs` | `pg_node_tree` |   | Expression trees \(in `nodeToString()` representation\) for index attributes that are not simple column references. This is a list with one element for each zero entry in `indkey`. Null if all index attributes are simple references. |
| `indpred` | `pg_node_tree` |   | Expression tree \(in `nodeToString()` representation\) for partial index predicate. Null if not a partial index. |

