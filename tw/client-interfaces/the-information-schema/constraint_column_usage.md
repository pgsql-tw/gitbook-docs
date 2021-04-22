# 36.18. constraint\_column\_usage

The view `constraint_column_usage` identifies all columns in the current database that are used by some constraint. Only those columns are shown that are contained in a table owned by a currently enabled role. For a check constraint, this view identifies the columns that are used in the check expression. For a foreign key constraint, this view identifies the columns that the foreign key references. For a unique or primary key constraint, this view identifies the constrained columns.

## **Table 36.16. `constraint_column_usage` Columns**

| Name | Data Type | Description |
| :--- | :--- | :--- |
| `table_catalog` | `sql_identifier` | Name of the database that contains the table that contains the column that is used by some constraint \(always the current database\) |
| `table_schema` | `sql_identifier` | Name of the schema that contains the table that contains the column that is used by some constraint |
| `table_name` | `sql_identifier` | Name of the table that contains the column that is used by some constraint |
| `column_name` | `sql_identifier` | Name of the column that is used by some constraint |
| `constraint_catalog` | `sql_identifier` | Name of the database that contains the constraint \(always the current database\) |
| `constraint_schema` | `sql_identifier` | Name of the schema that contains the constraint |
| `constraint_name` | `sql_identifier` | Name of the constraint |

