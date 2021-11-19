# 3.6. 繼承

繼承是一個物件導向資料庫的概念，它開啓了資料庫設計的更多可能性。

讓我們創建兩個資料表：cities 和 capitals。很自然地，首都（capitals）也是城市（cities），所以你希望有個方式，可以在列出所有城市時，同時也包含首都。如果你真的很清楚的話，你可以建立如下的結構：

```text
CREATE TABLE capitals (
  name       text,
  population real,
  altitude   int,    -- (in ft)
  state      char(2)
);

CREATE TABLE non_capitals (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE VIEW cities AS
  SELECT name, population, altitude FROM capitals
    UNION
  SELECT name, population, altitude FROM non_capitals;
```

這樣的查詢結果會是正確的，不過它有點不是很漂亮，當你需要更新一些資料的時候。

有一個更好的方法是這樣：

```text
CREATE TABLE cities (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE TABLE capitals (
  state      char(2)
) INHERITS (cities);
```

在這個例子中，capitals 繼承了 cities 的所有欄位（name, population, altitude）。欄位 name 的資料型別是文字型別（text），是一個 PostgreSQL 內建的資料型別，它允許字串長度是動態的。然後宣告 capitals 另外多一個欄位，state，以呈現它是屬於哪一個州。在 PostgreSQL，一個資料表可以繼承多個其他的資料格。

舉個例子，下面的查詢可以找出所有的城市名稱，包含各州的首都，而其海拔高過於 500 英呎以上：

```text
SELECT name, altitude
  FROM cities
  WHERE altitude > 500;
```

回傳結果：

```text
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
 Madison   |      845
(3 rows)
```

另一方面，下面的查詢可以列出非首都的城市，且其海拔在 500 英呎以上：

```text
SELECT name, altitude
    FROM ONLY cities
    WHERE altitude 
>
 500;
```

```text
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
(2 rows)
```

這裡的「ONLY」（cities之前），指的是這個查詢只要在資料表 cities 上就好，不包含繼承 cities 其他資料表。這裡許多我們都已經討論的指令 — SELECT、UPDATE、DELETE — 都支援 ONLY 這個修飾字。

## 注意

雖然繼承經常被使用，但尚未整合唯一性限制或外部索引鍵的功能，這限制了它的可用性。詳情請參考 [5.9 節](../../the-sql-language/ddl/inheritance.md)的說明。

