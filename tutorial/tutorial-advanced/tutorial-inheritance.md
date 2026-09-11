<a id="TUTORIAL-INHERITANCE"></a>

## 3.6. 繼承 [#](#TUTORIAL-INHERITANCE)

<a id="id-1.4.5.7.2"></a>

繼承（inheritance）是來自物件導向資料庫的概念，為資料庫設計開啟了有趣的新可能性。

我們來建立兩個資料表：資料表 `cities` 與資料表 `capitals`。首府當然也是城市，所以你會希望在列出所有城市時，能以某種方式隱含地一併顯示首府。如果你真的很聰明，可能會想出像這樣的做法：

```

CREATE TABLE capitals (
  name       text,
  population real,
  elevation  int,    -- (in ft)
  state      char(2)
);

CREATE TABLE non_capitals (
  name       text,
  population real,
  elevation  int     -- (in ft)
);

CREATE VIEW cities AS
  SELECT name, population, elevation FROM capitals
    UNION
  SELECT name, population, elevation FROM non_capitals;
```

就查詢而言這樣還算可行，但舉例來說，當你需要更新好幾筆資料列時，就會變得很難看。

更好的解決方式是：

```

CREATE TABLE cities (
  name       text,
  population real,
  elevation  int     -- (in ft)
);

CREATE TABLE capitals (
  state      char(2) UNIQUE NOT NULL
) INHERITS (cities);
```

在這個例子中，`capitals` 的資料列會從它的*父資料表* `cities` *繼承*所有欄位（`name`、`population` 與 `elevation`）。欄位 `name` 的型別是 `text`，這是 PostgreSQL 原生用於可變長度字串的型別。`capitals` 資料表還有一個額外的欄位 `state`，用來表示所屬州的縮寫。在 PostgreSQL 中，一個資料表可以繼承零個或多個其他資料表。

例如，下列查詢會找出所有位於海拔 500 英尺以上的城市名稱，包括州首府在內：

```

SELECT name, elevation
  FROM cities
  WHERE elevation > 500;
```

它會回傳：

```

   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
 Madison   |       845
(3 rows)
```

另一方面，下列查詢會找出所有位於海拔 500 英尺以上、但不是州首府的城市：

```

SELECT name, elevation
    FROM ONLY cities
    WHERE elevation > 500;
```

```

   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
(2 rows)
```

這裡在 `cities` 之前的 `ONLY`，表示查詢只應在 `cities` 資料表上執行，而不包含繼承階層中位於 `cities` 之下的資料表。我們已經討論過的許多指令，例如 `SELECT`、`UPDATE` 與 `DELETE`，都支援這種 `ONLY` 寫法。

### 注意

雖然繼承經常很有用，但它並未與唯一性限制條件或外部索引鍵整合，這限制了它的實用性。詳情請參閱[第 5.11 節](../../the-sql-language/ddl/ddl-inherit.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-inheritance.html)（原文版本：18.6；核對日期：2026-09-11）
