---
description: 版本：11
---

# ALTER RULE

ALTER RULE — 變更規則的宣告

### 語法

```
ALTER RULE name ON table_name RENAME TO new_name
```

### 說明

ALTER RULE 變更現有規則的屬性。目前，唯一可用的操作是變更規則的名稱。

要使用 ALTER RULE，您必須擁有該規則適用的資料表或檢視表。

### 參數

_`name`_

要變更的現有規則名稱。

_`table_name`_

規則適用的資料表或檢視表名稱（可加入綱要限定）。

_`new_name`_

規則的新名稱。

### 範例

要重新命名現有規則：

```
ALTER RULE notify_all ON emp RENAME TO notify_me;
```

### 相容性

ALTER RULE 是一個 PostgreSQL 語言延伸功能，整個查詢覆寫系統也都是延伸功能。

### 參閱

[CREATE RULE](create-rule.md), [DROP RULE](drop-rule.md)
