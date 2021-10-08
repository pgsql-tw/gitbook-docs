---
description: 版本：11
---

# DROP RULE

DROP RULE — 移除覆寫規則

## 語法

```text
DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

## 說明

DROP RULE 用於移除覆寫規則。

## 參數

`IF EXISTS`

如果規則不存在，請不要拋出錯誤。在這種情況下發出 NOTICE。

_`name`_

要移除的規則名稱。

_`table_name`_

規則適用的資料表或檢視表名稱（可加入綱要限定）。

`CASCADE`

自動移除相依於規則的物件，以及相依於這些物件的所有物件（請參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果任何物件相依於它，則拒絕移除規則。這是預設行為。

## 範例

要移除覆寫規則 newrule：

```text
DROP RULE newrule ON mytable;
```

## 相容性

DROP RULE 是 PostgreSQL 語法的延伸功能，整個查詢覆寫系統也是。

## 參閱

[CREATE RULE](create-rule.md), [ALTER RULE](alter-rule.md)

