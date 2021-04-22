# 51.95. pg\_views

檢視表 pg\_views 提供對資料庫中每個檢視表有用的資訊。

## **Table 51.96. `pg_views` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `schemaname` | `name` | [`pg_namespace`](pg_namespace.md).nspname | 檢視表所屬的綱要名稱 |
| `viewname` | `name` | \`\`[`pg_class`](pg_class.md).relname | 檢視表的名稱 |
| `viewowner` | `name` | \`\`[`pg_authid`](pg_authid.md).rolname | 檢視表的擁有者 |
| `definition` | `text` |  | 檢視表的內容定義（重新建構的 SELECT 查詢） |

