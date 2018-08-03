---
description: 版本：10
---

# 51.32. pg\_namespace

目錄 pg\_namespace 儲存命名空間。命名空間是 SQL 綱要的基礎結構：每個命名空間可以有一個獨立的關連，型別等集合，而不會有名稱衝突。

**Table 51.32. `pg_namespace` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |   | 資料列指標（隱藏屬性；必須明確選擇） |
| `nspname` | `name` |   | 命名空間的名稱 |
| `nspowner` | `oid` | [`pg_authid`](pg_authid.md).oid | 命名空間的所有者 |
| `nspacl` | `aclitem[]` |   | 存取權限；有關詳細信息，請參閱 [GRANT](../../reference/sql-commands/grant.md) 和 [REVOKE](../../reference/sql-commands/revoke.md) |

