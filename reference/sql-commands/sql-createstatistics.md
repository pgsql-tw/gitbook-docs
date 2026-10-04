<a id="SQL-CREATESTATISTICS"></a><a id="id-1.9.3.83.1"></a>

## CREATE STATISTICS

CREATE STATISTICS — 定義擴充統計資訊

<a id="id-1.9.3.83.4"></a>

## 語法

```

CREATE STATISTICS [ [ IF NOT EXISTS ] statistics_name ]
    ON ( expression )
    FROM table_name

CREATE STATISTICS [ [ IF NOT EXISTS ] statistics_name ]
    [ ( statistics_kind [, ... ] ) ]
    ON { column_name | ( expression ) }, { column_name | ( expression ) } [, ...]
    FROM table_name
```

<a id="SQL-CREATESTATISTICS-DESCRIPTION"></a>

## 說明

`CREATE STATISTICS` 會建立一個新的擴充統計資訊物件，追蹤指定資料表、外部資料表或具體化檢視表的資料。統計資訊物件會建立在目前的資料庫中，並由發出此命令的使用者擁有。

`CREATE STATISTICS` 命令有兩種基本形式。第一種形式可以收集單一運算式的單變量統計資訊，提供類似運算式索引的好處，卻沒有維護索引的額外負擔。此形式不允許指定統計資訊種類，因為各種統計資訊種類都只適用於多變量統計資訊。此命令的第二種形式可以收集多個欄位和（或）運算式上的多變量統計資訊，並可選擇指定要包含哪些統計資訊種類。此形式也會自動為清單中包含的任何運算式收集單變量統計資訊。

若有指定綱要名稱（例如 `CREATE STATISTICS
myschema.mystat ...`），統計資訊物件就會建立在指定的綱要中；否則會建立在目前的綱要中。若有指定名稱，統計資訊物件的名稱必須與同一綱要中任何其他統計資訊物件的名稱不同。

<a id="id-1.9.3.83.6"></a>

## 參數

`IF NOT EXISTS`
:   若已存在同名的統計資訊物件，不擲出錯誤；此情況會發出 notice。請注意，此處只考慮統計資訊物件的名稱，而不考慮其定義的細節。指定 `IF NOT EXISTS` 時，必須提供統計資訊名稱。

*`statistics_name`*
:   要建立的統計資訊物件名稱（可選擇以綱要限定）。若省略名稱，PostgreSQL 會依據父資料表的名稱以及所定義的欄位名稱和（或）運算式，選擇一個合適的名稱。

*`statistics_kind`*
:   要在此統計資訊物件中計算的多變量統計資訊種類。目前支援的種類有：`ndistinct`，啟用 n-distinct 統計資訊；`dependencies`，啟用函數相依性統計資訊；以及 `mcv`，啟用最常見值（most-common values）清單。若省略此子句，所有支援的統計資訊種類都會包含在統計資訊物件中。若統計資訊定義中包含任何複雜運算式，而不只是單純的欄位參照，就會自動建立單變量運算式統計資訊。更多資訊請參閱[第 14.2.2 節](../../the-sql-language/performance-tips/planner-stats.md#PLANNER-STATS-EXTENDED)與[第 69.2 節](../../internals/planner-stats-details/multivariate-statistics-examples.md)。

*`column_name`*
:   計算出的統計資訊所涵蓋之資料表欄位的名稱。只有在建立多變量統計資訊時才允許使用。必須指定至少兩個欄位名稱或運算式，且其順序並不重要。

*`expression`*
:   計算出的統計資訊所涵蓋的運算式。它可以用來建立單一運算式上的單變量統計資訊，或作為多個欄位名稱和（或）運算式清單的一部分，以建立多變量統計資訊。在後者的情況下，會自動為清單中的每個運算式分別建立單變量統計資訊。

*`table_name`*
:   包含要計算統計資訊之欄位的資料表名稱（可選擇以綱要限定）；關於繼承與分割區的處理方式，請參閱 [ANALYZE](sql-analyze.md) 的說明。

<a id="id-1.9.3.83.7"></a>

## 注意事項

你必須是資料表的擁有者，才能建立讀取該資料表的統計資訊物件。不過，一旦建立之後，統計資訊物件的所有權就與其底層資料表無關。

運算式統計資訊是以每個運算式為單位，類似於在該運算式上建立索引，只是避免了維護索引的額外負擔。系統會為統計資訊物件定義中的每個運算式自動建立運算式統計資訊。

目前規劃器在估算資料表連接的選擇率時，並不會使用擴充統計資訊。這項限制很可能會在 PostgreSQL 的未來版本中移除。

<a id="SQL-CREATESTATISTICS-EXAMPLES"></a>

## 範例

建立具有兩個函數相依欄位的資料表 `t1`，也就是說，知道第一個欄位中的值就足以決定另一個欄位中的值。接著在這些欄位上建立函數相依性統計資訊：

```

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

若沒有函數相依性統計資訊，規劃器會假設兩個 `WHERE` 條件彼此獨立，並將它們的選擇率相乘，得出嚴重偏小的資料列數估計值。有了這類統計資訊，規劃器就會辨識出這些 `WHERE` 條件是重複的，而不會低估資料列數。

建立具有兩個完全相關欄位（包含相同資料）的資料表 `t2`，並在這些欄位上建立 MCV 清單：

```

CREATE TABLE t2 (
    a   int,
    b   int
);

INSERT INTO t2 SELECT mod(i,100), mod(i,100)
                 FROM generate_series(1,1000000) s(i);

CREATE STATISTICS s2 (mcv) ON a, b FROM t2;

ANALYZE t2;

-- valid combination (found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 1);

-- invalid combination (not found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 2);
```

MCV 清單提供規劃器更詳細的資訊，包括資料表中常見的特定值，以及未出現在資料表中之值組合的選擇率上限，讓規劃器在這兩種情況下都能產生較好的估計值。

建立具有單一 timestamp 欄位的資料表 `t3`，並執行在該欄位上使用運算式的查詢。若沒有擴充統計資訊，規劃器就沒有這些運算式之資料分布的資訊，只能使用預設估計值。規劃器也不知道截斷到月份的日期值，完全由截斷到日的日期值所決定。接著在這兩個運算式上建立運算式統計資訊與 ndistinct 統計資訊：

```

CREATE TABLE t3 (
    a   timestamp
);

INSERT INTO t3 SELECT i FROM generate_series('2020-01-01'::timestamp,
                                             '2020-12-31'::timestamp,
                                             '1 minute'::interval) s(i);

ANALYZE t3;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('month', a) = '2020-01-01'::timestamp;

EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('day', a) BETWEEN '2020-01-01'::timestamp
                                 AND '2020-06-30'::timestamp;

EXPLAIN ANALYZE SELECT date_trunc('month', a), date_trunc('day', a)
   FROM t3 GROUP BY 1, 2;

-- build ndistinct statistics on the pair of expressions (per-expression
-- statistics are built automatically)
CREATE STATISTICS s3 (ndistinct) ON date_trunc('month', a), date_trunc('day', a) FROM t3;

ANALYZE t3;

-- now the row count estimates are more accurate:
EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('month', a) = '2020-01-01'::timestamp;

EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('day', a) BETWEEN '2020-01-01'::timestamp
                                 AND '2020-06-30'::timestamp;

EXPLAIN ANALYZE SELECT date_trunc('month', a), date_trunc('day', a)
   FROM t3 GROUP BY 1, 2;
```

若沒有運算式統計資訊與 ndistinct 統計資訊，規劃器就沒有運算式相異值數量的資訊，只能依賴預設估計值。等值條件與範圍條件會被假設具有 0.5% 的選擇率，而運算式中相異值的數量會被假設與該欄位相同（也就是唯一）。這會導致前兩個查詢的資料列數被嚴重低估。此外，規劃器沒有關於運算式之間關係的資訊，因此會假設兩個 `WHERE` 與 `GROUP BY` 條件彼此獨立，並將它們的選擇率相乘，導致彙總查詢中的群組數被嚴重高估。缺乏運算式的準確統計資訊使情況更加惡化，迫使規劃器對運算式使用由欄位的 ndistinct 推導而來的預設 ndistinct 估計值。有了這類統計資訊，規劃器就會辨識出這些條件彼此相關，並得出準確得多的估計值。

<a id="id-1.9.3.83.9"></a>

## 相容性

SQL 標準中沒有 `CREATE STATISTICS` 命令。

<a id="id-1.9.3.83.10"></a>

## 另請參閱

[ALTER STATISTICS](sql-alterstatistics.md), [DROP STATISTICS](sql-dropstatistics.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createstatistics.html)（原文版本：18.6；核對日期：2026-10-04）
