# 51.73. pg_indexes

`pg_indexes` View 提供資料庫所有 Index 相關有用資訊
## **Table 51.74. `pg_indexes` Columns**

| Name         | Type   | References                                                                               | Description                                                          |
|:-------------|:-------|:-----------------------------------------------------------------------------------------|:---------------------------------------------------------------------|
| `schemaname` | `name` | [`pg_namespace`](https://www.postgresql.org/docs/12/catalog-pg-namespace.html).nspname   | Index 所在的 schema 名稱                                             |
| `tablename`  | `name` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relname           | Index 所在的資料表名稱                                               |
| `indexname`  | `name` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relname           | Index 名稱                                                           |
| `tablespace` | `name` | [`pg_tablespace`](https://www.postgresql.org/docs/12/catalog-pg-tablespace.html).spcname | Name of tablespace containing index \(null if default for database\) |
| `indexdef`   | `text` |                                                                                          | 建立 Index 定義 \(重建 `CREATE INDEX` sql 命令\)                     |

