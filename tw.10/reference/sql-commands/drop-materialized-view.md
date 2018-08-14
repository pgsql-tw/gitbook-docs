---
description: 版本：10
---

# DROP MATERIALIZED VIEW

DROP MATERIALIZED VIEW — 移除具體化檢視表

### 語法

```text
DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### 說明

DROP MATERIALIZED VIEW 移除現有的具體化檢視表。要執行此指令，您必須是具體化檢視表的擁有者。

### 參數

`IF EXISTS`

如果具體化檢視表不存在，請不要拋出錯誤。在這種情況下發出 NOTICE。

_`name`_

要移除的具體化檢視表名稱（可選用綱要名稱）。

`CASCADE`

自動移除相依於具體化檢視表的物件（例如其他具體化檢視表或一般的檢視表），以及相依於這些物件的所有物件（參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果任何物件相依於它，則拒絕移除具體化檢視表。這是預設值。

### 範例

此指令將移除名為 order\_summary 的具體化檢視表：

```text
DROP MATERIALIZED VIEW order_summary;
```

### 相容性

DROP MATERIALIZED VIEW 是 PostgreSQL 延伸語法。

### 參閱

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [ALTER MATERIALIZED VIEW](alter-materialized-view.md), [REFRESH MATERIALIZED VIEW](refresh-materialized-view.md)

