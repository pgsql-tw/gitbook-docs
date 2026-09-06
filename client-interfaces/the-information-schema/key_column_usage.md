# 36.32. key\_column\_usage

檢視表 key\_column\_usage 列出目前資料庫中受到某些唯一、主鍵或外部鍵限制的所有欄位。此檢視表中不包括 check constraints。僅顯示目前使用者可以透過成為擁有者或具有某些權限存取的那些欄位。

#### **Table 36.30. `key_column_usage` Columns**

| Name                            | Data Type         | Description                                                                                                                               |
| ------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `constraint_catalog`            | `sql_identifier`  | Name of the database that contains the constraint (always the current database)                                                           |
| `constraint_schema`             | `sql_identifier`  | Name of the schema that contains the constraint                                                                                           |
| `constraint_name`               | `sql_identifier`  | Name of the constraint                                                                                                                    |
| `table_catalog`                 | `sql_identifier`  | Name of the database that contains the table that contains the column that is restricted by this constraint (always the current database) |
| `table_schema`                  | `sql_identifier`  | Name of the schema that contains the table that contains the column that is restricted by this constraint                                 |
| `table_name`                    | `sql_identifier`  | Name of the table that contains the column that is restricted by this constraint                                                          |
| `column_name`                   | `sql_identifier`  | Name of the column that is restricted by this constraint                                                                                  |
| `ordinal_position`              | `cardinal_number` | Ordinal position of the column within the constraint key (count starts at 1)                                                              |
| `position_in_unique_constraint` | `cardinal_number` | For a foreign-key constraint, ordinal position of the referenced column within its unique constraint (count starts at 1); otherwise null  |
