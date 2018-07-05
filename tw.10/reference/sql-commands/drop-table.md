---
description: 版本：10
---

# DROP TABLE

DROP TABLE — 移除一個資料表

## 語法

```text
DROP TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## 說明

DROP TABLE 從資料庫中移除資料表。只有資料表的擁有者，其綱要的擁有者和超級使用者才能移除該資料表。要在不破壞資料表的情況下清空資料表的資料，請使用 [DELETE](delete.md) 或 [TRUNCATE](truncate.md)。

DROP TABLE 會移除目標資料表所關連的任何索引、規則、觸發器和限制條件。但是，要移除由檢視表引用的資料表或另一個資料表的外部鍵，必須指定 CASCADE。（CASCADE 將完全移除從屬的檢視表，但外部鍵情況，它只會移除外部鍵，而不會移除其他資料表。）

## 參數

`IF EXISTS`

如果資料表不存在，請不要拋出錯誤。 在這種情況下發出 NOTICE。

`name`

要移除的資料表名稱（可選用綱要名稱）。

`CASCADE`

自動刪除相依於資料表的物件（例如檢視表），以及相依於這些物件的所有物件（參閱[第 5.13 節](../../the-sql-language/5.-ding-yi-zi-liao-jie-gou/5.13.-xiang-yi-xing-zhui-zong.md)）。

`RESTRICT`

如果任何物件相依於它，就拒絕移除此資料表。這是預設行為。

## 範例

移除兩個資料表，films 和 distributors：

```text
DROP TABLE films, distributors;
```

## 相容性

此命令符合 SQL 標準，除了標準只允許每個指令移除一個資料表，及 IF EXISTS 選項（PostgreSQL 延伸功能）之外。

## 參閱

[ALTER TABLE](alter-table.md), [CREATE TABLE](create-table.md)

