---
description: 版本：11
---

# 51.51. pg\_statistic\_ext

目錄 pg\_statistic\_ext 包含了延伸的計劃程序統計資訊。此目錄中的每一個資料列相對應於使用 [CREATE STATISTICS](../../reference/sql-commands/create-statistics.md) 所建立的統計資訊物件。

## **Table 52.51. `pg_statistic_ext` Columns**

| 欄位 | 型別 | 參考 | 說明 |
| :--- | :--- | :--- | :--- |
| `stxrelid` | `oid` | \`\`[`pg_class`](pg_class.md).oid | 包含此物件包含欄位的所屬資料表 |
| `stxname` | `name` |  | 統計物件的名稱 |
| `stxnamespace` | `oid` | \`\`[`pg_namespace`](pg_namespace.md).oid | 包含此統計資訊物件在命名空間裡的 OID |
| `stxowner` | `oid` | \`\`[`pg_authid`](pg_authid.md).oid | 統計物件的所有者 |
| `stxkeys` | `int2vector` | \`\`[`pg_attribute`](pg_attribute.md).attnum | 一組陣列表示的屬性數字，指示此統計物件覆蓋哪些資料表欄位；例如，值為 1 3 意味著覆蓋了第一個和第三個資料表欄位 |
| `stxkind` | `char[]` |  | 包含已啟用統計類型的代碼的陣列；有效值為：d 表示 n-distinct 統計資訊，f 表示功能相依統計資訊 |
| `stxndistinct` | `pg_ndistinct` |  | N-distinct 計數，序列化為 pg\_ndistinct 型別 |
| `stxdependencies` | `pg_dependencies` |  | 功能相依統計資訊，序列化為 pg\_dependencies 型別 |

stxkind 欄位會在建立統計物件時填入，指示需要哪種統計類型。在它之後的欄位最初為 NULL，僅在 ANALYZE 計算出相對應的統計量時才填入內容。

