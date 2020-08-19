---
description: 版本：11
---

# CREATE STATISTICS

CREATE STATISTICS — 定義延伸統計資訊

## 語法

```text
CREATE STATISTICS [ IF NOT EXISTS ] statistics_name
    [ ( statistics_kind [, ... ] ) ]
    ON column_name, column_name [, ...]
    FROM table_name
```

## 說明

CREATE STATISTICS 將建立一個新的延伸統計資訊物件，追踪指定資料表、外部資料表或具體化檢視表的相關數據。統計資訊物件將在目前的資料庫中建立，並由發出此命令的使用者擁有。

如果使用了綱要名稱（例如，CREATE STATISTICS myschema.mystat ...），則會在指定的綱要中建立統計資訊物件。 否則，它將在目前的綱要中建立。統計資訊物件的名稱必須與同一綱要中任何其他統計資訊物件的名稱不同。

## 參數

`IF NOT EXISTS`

如果已存在具有相同名稱的統計物件，請不要拋出錯誤。在這種情況下發出 NOTICE。請注意，此處僅考慮統計物件的名稱，而不是其定義的詳細內容。

_`statistics_name`_

要建立的統計資訊物件名稱（可選擇性加上綱要名稱）。

_`statistics_kind`_

要在此統計物件中計算的統計類型。目前支援的種類是 ndistinct，它支援 n 個不同的統計資訊和相依關係，它們支援功能相依性統計。如果省略此子句，則統計物件中將包含所有受支援的統計類型。有關更多訊息，請參閱[第 14.2.2 節](../../the-sql-language/performance-tips/statistics-used-by-the-planner.md#14-2-2-yan-shen)和[第 70.2 節](../../internals/how-the-planner-uses-statistics/multivariate-statistics-examples.md)。

_`column_name`_

計算統計資訊要涵蓋的資料表欄位名稱。必須至少提供兩個欄位名稱。

_`table_name`_

包含計算統計資訊欄位的資料表名稱（可選擇性加上綱要）。

## 注意

您必須是資料表的所有者才能建立讀取它的統計物件。但是，一旦建立，統計物件的所有權就獨立於基礎資料表。

## 範例

建立具有兩個功能性相關連的欄位在資料表 t1，也就是知道第一欄位中的值就足以決定另一欄位中的值。然後在這些欄位上建構功能相依性統計資訊：

```text
CREATE TABLE t1 (
    a   int,
    b   int
);

INSERT INTO t1 SELECT i/100, i/500
                 FROM generate_series(1,1000000) s(i);

ANALYZE t1;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);

CREATE STATISTICS s1 (dependencies) ON a, b FROM t1;

ANALYZE t1;

-- now the row count estimate is more accurate:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);
```

如果沒有功能相依性統計，計劃程序將會假設兩個 WHERE 條件是獨立的，並且將它們的可能性相乘而得到非常小的資料列計數估計。有了這樣的統計數據，規劃程序就會瞭解到 WHERE 條件是多餘的，就不會低估資料列數量。

## 相容性

SQL 標準中沒有 CREATE STATISTICS 指令。

## 參閱

[ALTER STATISTICS](alter-statistics.md), [DROP STATISTICS](drop-statistics.md)

