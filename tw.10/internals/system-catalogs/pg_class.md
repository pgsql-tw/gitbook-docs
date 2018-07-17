---
description: 版本：10
---

# 51.11 pg\_class

目錄 pg\_class 對資料表和大多數具有欄位或其他類似於資料表的內容進行彙整。 包括索引（但也參閱 pg\_index）、序列（但請參閱 pg\_sequence）、檢視表、具體化檢視表、複合型別和 TOAST 資料表；另請查看 relkind 欄位。以下，當我們指的是所有這些類型的物件時，我們都會說「關連（relation）」。 並非所有欄位對所有關連類型都有意義。

**Table 51.11. `pg_class` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `oid` | `oid` |   | 資料列指標（隱藏屬性；必須明確選擇） |
| `relname` | `name` |   | 資料表的名稱，索引，檢視表等 |
| `relnamespace` | `oid` | [`pg_namespace`](pg_namespace.md).oid | 包含此關連命名空間的 OID |
| `reltype` | `oid` | [`pg_type`](pg_type.md).oid | 與此資料表的資料列類型對應資料型別的OID（如果有）（索引為零，因為沒有 pg\_type 項目） |
| `reloftype` | `oid` | [`pg_type`](pg_type.md).oid | 對於複合型別資料表，底層複合型別的 OID，對於所有其他關連的值為零 |
| `relowner` | `oid` | [`pg_authid`](pg_authid.md).oid | 關連的所有者 |
| `relam` | `oid` | [`pg_am`](pg_am.md).oid | 如果這是索引，則為使用存取的方法（B-tree，hash 等） |
| `relfilenode` | `oid` |   | 此關連的磁碟檔案的名稱；零表示這是一個「映射」關連，其磁碟檔案名稱由底層狀態決定 |
| `reltablespace` | `oid` | [`pg_tablespace`](51.54.-pg_tablespace.md).oid | 儲存此關連的資料表空間。如果為零，則隱含資料庫的預設資料表空間。（如果關連沒有磁碟檔案，則沒有意義。） |
| `relpages` | `int4` |   | 頁面（大小為 BLCKSZ）的磁碟表示形式的大小。這只是計劃程序使用的估算值。它由 VACUUM，ANALYZE 和一些 DDL 指令（如 CREATE INDEX）更新。 |
| `reltuples` | `float4` |   | 資料表中的資料列數。這只是計劃程序使用的估算值。它由VACUUM，ANALYZE 和一些 DDL 指令（如 CREATE INDEX）更新。 |
| `relallvisible` | `int4` |   | 在資料表的可見性映射中標記為全部可見的頁面數。這只是計劃程序使用的估算值。它由 VACUUM，ANALYZE 和一些 DDL 指令（如 CREATE INDEX）更新。 |
| `reltoastrelid` | `oid` | [`pg_class`](pg_class.md).oid | 與此資料表關連的 TOAST 資料表的OID，如果沒有，則為0。TOAST 資料表在輔助資料表中儲存“out of line”的大型屬性。 |
| `relhasindex` | `bool` |   | 如果這是一個資料表並且它有（或最近有）任何索引，則為 True |
| `relisshared` | `bool` |   | 如果此資料表在叢集中的所有資料庫之間共享，則為 True。只有某些系統目錄共享（例如 pg\_database）。 |
| `relpersistence` | `char` |   | p = 永久資料表，u = 無日誌資料，t = 臨時資料表 |
| `relkind` | `char` |   | r = 普通資料表，i = 索引，S = 序列，t = TOAST 資料表，v = 檢視表，m = 具體化檢視表，c = 複合型別，f = 外部資料表，p = 分割資料表 |
| `relnatts` | `int2` |   | 關連中的用戶欄位數（系統欄位未計算）。pg\_attribute 中必須有這麼多對應的項目。另請參閱 pg\_attribute.attnum。 |
| `relchecks` | `int2` |   | 資料表上的 CHECK 限制條件數目；請參閱 [pg\_constraint](pg_constraint.md) 目錄 |
| `relhasoids` | `bool` |   | 如果我們為關連的每一個資料列産生一個 OID，則為 True |
| `relhaspkey` | `bool` |   | 如果資料表具有（或曾經有）主鍵，則為 True |
| `relhasrules` | `bool` |   | 如果資料表有（或曾經有）rule，則為 true；請參閱 [pg\_rewrite](51.44.-pg_rewrite.md) 目錄 |
| `relhastriggers` | `bool` |   | 如果資料表具有（或曾經有）觸發器，則為 True；請參閱 [pg\_trigger](51.56.-pg_trigger.md) 目錄 |
| `relhassubclass` | `bool` |   | 如果資料表具有（或曾經有）任何繼承子項，則為 True |
| `relrowsecurity` | `bool` |   | 如果資料表啟用了資料列級安全性，則為 True；請參閱 [pg\_policy](pg_policy.md) 目錄 |
| `relforcerowsecurity` | `bool` |   | 如果資料列級別安全性（啟用時）也適用於資料表擁有者，則為 True；請參閱 [pg\_policy ](pg_policy.md)目錄 |
| `relispopulated` | `bool` |   | 如果關連充入了資料，則為 True（除了某些具體化檢視表之外的所有關連都是 True） |
| `relreplident` | `char` |   | 用於為資料列形成“replica identity”的欄位：d = 預設（主鍵，如果有），n = 無，f = 所有列，i = 具有 indisreplident 設定的索引，或預設值 |
| `relispartition` | `bool` |   | True if table is a partition |
| `relfrozenxid` | `xid` |   | 此資料表之前的所有事務 ID 都已替換為此資料表中的永久（“frozen”）事務 ID。這用於追踪資料表是否需要被清理以防止事務 ID 重覆或讓 pg\_xact 縮小。如果關連不是資料表，則為零（InvalidTransactionId）。 |
| `relminmxid` | `xid` |   | 此資料表之前的所有 multixact ID 都已被此資料表中的事務 ID 替換。這用於追踪表是否需要被清理以防止多重 ID 重覆或使 pg\_multixact 縮小。如果關連不是資料表，則為零（InvalidMultiXactId）。 |
| `relacl` | `aclitem[]` |   | 存取權限；有關詳細信息，請參閱 [GRANT](../../reference/sql-commands/grant.md) 和 [REVOKE](../../reference/sql-commands/revoke.md) |
| `reloptions` | `text[]` |   | 存取方法的特定選項，為「keyword = value」字串 |
| `relpartbound` | `pg_node_tree` |   | 如果資料表是一個分割區（請參閱 relispartition），則綁定分割區的內部表示 |

pg\_class 中的幾個布林欄位的維護是鬆散的：如果這是正確的狀態，那它們保證為 true，但是當條件不再為真時，可能不會立即重置為 false。例如，relhasindex 由CREATE INDEX 設定，但它永遠不會被 DROP INDEX 清除。相反地，如果 VACUUM 發現資料表沒有索引，則清除 relhasindex。這種安排避免了競爭條件並改善了一致性。

