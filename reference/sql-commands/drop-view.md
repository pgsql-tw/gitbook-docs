# DROP VIEW

DROP VIEW — 移除檢視表

### 語法

```
DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### 說明

DROP VIEW 移除現有檢視表。要執行此命令，您必須是檢視表的擁有者。

### 參數

`IF EXISTS`

如果檢視表不存在，請不要拋出錯誤。在這種情況下發出 NOTICE。

_`name`_

要移除的檢視表名稱（可選擇性加上綱要名稱）。

`CASCADE`

自動移除相依於檢視表的物件（例如其他檢視表），以及相依於這些物件的所有物件（參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果任何物件相依於它，則拒絕移除檢視表。這是預設行為。

### 範例

此指令將移除名稱為 kinds 的檢視表：

```
DROP VIEW kinds;
```

### 相容性

此命令符合 SQL 標準，但標準僅允許每個指令移除一個檢視表，並且除了 IF EXISTS 選項（PostgreSQL 延伸功能）之外。

### 參閱

[ALTER VIEW](alter-view.md), [CREATE VIEW](create-view.md)
