# 36.51. table\_constraints

The view `table_constraints` contains all constraints belonging to tables that the current user owns or has some privilege other than `SELECT` on.

#### **Table 36.49. `table_constraints` Columns**

| Name | Data Type | Description |
| :--- | :--- | :--- |
| `constraint_catalog` | `sql_identifier` | Name of the database that contains the constraint \(always the current database\) |
| `constraint_schema` | `sql_identifier` | Name of the schema that contains the constraint |
| `constraint_name` | `sql_identifier` | Name of the constraint |
| `table_catalog` | `sql_identifier` | Name of the database that contains the table \(always the current database\) |
| `table_schema` | `sql_identifier` | Name of the schema that contains the table |
| `table_name` | `sql_identifier` | Name of the table |
| `constraint_type` | `character_data` | Type of the constraint: `CHECK`, `FOREIGN KEY`, `PRIMARY KEY`, or `UNIQUE` |
| `is_deferrable` | `yes_or_no` | `YES` if the constraint is deferrable, `NO` if not |
| `initially_deferred` | `yes_or_no` | `YES` if the constraint is deferrable and initially deferred, `NO` if not |
| `enforced` | `yes_or_no` | Applies to a feature not available in PostgreSQL \(currently always `YES`\) |

