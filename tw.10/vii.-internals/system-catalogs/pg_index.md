# 51.39 pg\_index

The catalog `pg_index` contains part of the information about indexes. The rest is mostly in `pg_class`.

**Table 51.26. `pg_index` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `indexrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | The OID of the `pg_class` entry for this index |
| `indrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | The OID of the `pg_class` entry for the table this index is for |
| `indnatts` | `int2` |   | The number of columns in the index \(duplicates `pg_class.relnatts`\) |
| `indisunique` | `bool` |   | If true, this is a unique index |
| `indisprimary` | `bool` |   | If true, this index represents the primary key of the table \(`indisunique` should always be true when this is true\) |
| `indisexclusion` | `bool` |   | If true, this index supports an exclusion constraint |
| `indimmediate` | `bool` |   | If true, the uniqueness check is enforced immediately on insertion \(irrelevant if `indisunique` is not true\) |
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

