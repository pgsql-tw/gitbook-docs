# 51.51. pg\_statistic\_ext

The catalog `pg_statistic_ext` holds extended planner statistics. Each row in this catalog corresponds to a _statistics object_ created with [CREATE STATISTICS](https://www.postgresql.org/docs/10/static/sql-createstatistics.html).

**Table 51.51. `pg_statistic_ext` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `stxrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | Table containing the columns described by this object |
| `stxname` | `name` |   | Name of the statistics object |
| `stxnamespace` | `oid` | [`pg_namespace`](https://www.postgresql.org/docs/10/static/catalog-pg-namespace.html).oid | The OID of the namespace that contains this statistics object |
| `stxowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the statistics object |
| `stxkeys` | `int2vector` | [`pg_attribute`](https://www.postgresql.org/docs/10/static/catalog-pg-attribute.html).attnum | An array of attribute numbers, indicating which table columns are covered by this statistics object; for example a value of `1 3` would mean that the first and the third table columns are covered |
| `stxkind` | `char[]` |   | An array containing codes for the enabled statistic kinds; valid values are: `d` for n-distinct statistics, `f` for functional dependency statistics |
| `stxndistinct` | `pg_ndistinct` |   | N-distinct counts, serialized as `pg_ndistinct` type |
| `stxdependencies` | `pg_dependencies` |   | Functional dependency statistics, serialized as `pg_dependencies` type |

The `stxkind` field is filled at creation of the statistics object, indicating which statistic type\(s\) are desired. The fields after it are initially NULL and are filled only when the corresponding statistic has been computed by`ANALYZE`.

