# 36.42. schemata

此檢視表 schemata 包含目前資料庫中目前使用者有權限存取的所有 schema（透過成為擁有者或具有某些權限）。

#### **Table 36.40. `schemata` Columns**

| Name                            | Data Type        | Description                                      |
| ------------------------------- | ---------------- | ------------------------------------------------ |
| `catalog_name`                  | `sql_identifier` | 查詢當下的資料庫名稱（只會是目前資料庫）                             |
| `schema_name`                   | `sql_identifier` | Name of the schema                               |
| `schema_owner`                  | `sql_identifier` | Name of the owner of the schema                  |
| `default_character_set_catalog` | `sql_identifier` | Applies to a feature not available in PostgreSQL |
| `default_character_set_schema`  | `sql_identifier` | Applies to a feature not available in PostgreSQL |
| `default_character_set_name`    | `sql_identifier` | Applies to a feature not available in PostgreSQL |
| `sql_path`                      | `character_data` | Applies to a feature not available in PostgreSQL |
