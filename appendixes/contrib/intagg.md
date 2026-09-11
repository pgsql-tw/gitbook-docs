## F.18. intagg — 整數聚合器與列舉器 [#](#INTAGG)

[F.18.1. 函式](intagg.md#INTAGG-FUNCTIONS)

[F.18.2. 使用範例](intagg.md#INTAGG-SAMPLES)

<a id="id-1.11.7.28.2"></a>

`intagg` 模組提供整數聚合器與列舉器。`intagg` 現已過時，因為內建函式提供了其功能的超集。不過，此模組仍作為內建函式的相容性包裝器提供。

<a id="INTAGG-FUNCTIONS"></a>

### F.18.1. 函式 [#](#INTAGG-FUNCTIONS)

<a id="id-1.11.7.28.4.2"></a><a id="id-1.11.7.28.4.3"></a>

聚合器是聚合函式 `int_array_aggregate(integer)`，會產生恰好包含其輸入整數的整數陣列。它是 `array_agg` 的包裝器；後者可對任何陣列型別執行相同工作。

<a id="id-1.11.7.28.4.5"></a>

列舉器是函式 `int_array_enum(integer[])`，會傳回 `setof integer`。它本質上是聚合器的反向操作：指定一個整數陣列，將其展開為一組資料列。它是 `unnest` 的包裝器；後者可對任何陣列型別執行相同工作。

<a id="INTAGG-SAMPLES"></a>

### F.18.2. 使用範例 [#](#INTAGG-SAMPLES)

許多資料庫系統具有多對多資料表的概念。這類資料表通常位於兩個已建立索引的資料表之間，例如：

```

CREATE TABLE left_table  (id INT PRIMARY KEY, ...);
CREATE TABLE right_table (id INT PRIMARY KEY, ...);
CREATE TABLE many_to_many(id_left  INT REFERENCES left_table,
                          id_right INT REFERENCES right_table);
```

通常會如下使用：

```

SELECT right_table.*
FROM right_table JOIN many_to_many ON (right_table.id = many_to_many.id_right)
WHERE many_to_many.id_left = item;
```

這會傳回左側資料表中某個項目所對應的右側資料表全部項目。這是 SQL 中非常常見的結構。

現在，若 `many_to_many` 資料表的項目數量非常多，此方法可能很繁瑣。這類連接通常會對特定左側項目的資料表中每個右側項目進行索引掃描與擷取。若系統變動非常頻繁，可改善的空間不大。不過，若部分資料相當靜態，可使用聚合器建立摘要資料表。

```

CREATE TABLE summary AS
  SELECT id_left, int_array_aggregate(id_right) AS rights
  FROM many_to_many
  GROUP BY id_left;
```

這會建立一個資料表，每個左側項目各有一個資料列，以及一個右側項目陣列。若沒有使用該陣列的方法，這就沒有太大用處；因此才有陣列列舉器。您可以執行：

```

SELECT id_left, int_array_enum(rights) FROM summary WHERE id_left = item;
```

以上使用 `int_array_enum` 的查詢會產生與下列查詢相同的結果：

```

SELECT id_left, id_right FROM many_to_many WHERE id_left = item;
```

差異在於針對摘要資料表的查詢只需從資料表取得一個資料列，而直接查詢 `many_to_many` 必須為每個項目進行索引掃描並擷取一個資料列。

在某個系統上，`EXPLAIN` 顯示一個成本為 8488 的查詢降至成本 329。原始查詢是涉及 `many_to_many` 資料表的連接，改為下列查詢：

```

SELECT id_right, count(id_right) FROM
  ( SELECT id_left, int_array_enum(rights) AS id_right
    FROM summary
    JOIN (SELECT id FROM left_table
          WHERE id = item) AS lefts
    ON (summary.id_left = lefts.id)
  ) AS list
  GROUP BY id_right
  ORDER BY count DESC;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intagg.html)
