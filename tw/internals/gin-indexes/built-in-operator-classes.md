# 66.2. 內建運算子類

主要的 PostgreSQL 版本包括 [Table 64.1](built-in-operator-classes.md#table-64-1-built-in-gin-operator-classes) 中所示的 GIN 運算子類。（[附錄 F](../../appendixes/additional-supplied-modules/) 中描述的一些選用套件提供了額外的 GIN 運算子類。）

#### **Table 66.1. Built-in GIN Operator Classes**

| Name             | Indexed Data Type | Indexable Operators           |
| ---------------- | ----------------- | ----------------------------- |
| `array_ops`      | `anyarray`        | `&&` `<@` `=` `@>`            |
| `jsonb_ops`      | `jsonb`           | `?` `?&` `?\|` `@>` `@?` `@@` |
| `jsonb_path_ops` | `jsonb`           | `@>` `@?` `@@`                |
| `tsvector_ops`   | `tsvector`        | `@@` `@@@`                    |

在 jsonb 型別的兩個運算子類中，jsonb\_ops 是預設值。jsonb\_path\_ops 支援較少的運算子，但為這些運算子提供了更好的效能。有關詳細訊息，請參閱[第 8.14.4 節](../../the-sql-language/data-types/json-types.md#8-14-4-jsonbindexing)。
