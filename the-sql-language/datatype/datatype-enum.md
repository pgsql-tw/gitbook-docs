<a id="DATATYPE-ENUM"></a>

## 8.7. 列舉型別 [#](#DATATYPE-ENUM)

[8.7.1. 列舉型別的宣告](datatype-enum.md#DATATYPE-ENUM-DECLARATION)

[8.7.2. 排序](datatype-enum.md#DATATYPE-ENUM-ORDERING)

[8.7.3. 型別安全](datatype-enum.md#DATATYPE-ENUM-TYPE-SAFETY)

[8.7.4. 實作細節](datatype-enum.md#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

<a id="id-1.5.7.15.2"></a><a id="id-1.5.7.15.3"></a>

列舉（enum）型別是由一組靜態、有順序的值所構成的資料型別。它們相當於許多程式語言所支援的 `enum` 型別。列舉型別的例子可能是一週中的各天，或是某項資料的一組狀態值。

<a id="DATATYPE-ENUM-DECLARATION"></a>

### 8.7.1. 列舉型別的宣告 [#](#DATATYPE-ENUM-DECLARATION)

列舉型別是以 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md) 指令建立的，例如：

```

CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

建立之後，這個列舉型別就可以像其他型別一樣，用在資料表與函式的定義中：

```

CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
CREATE TABLE person (
    name text,
    current_mood mood
);
INSERT INTO person VALUES ('Moe', 'happy');
SELECT * FROM person WHERE current_mood = 'happy';
 name | current_mood
------+--------------
 Moe  | happy
(1 row)
```

<a id="DATATYPE-ENUM-ORDERING"></a>

### 8.7.2. 排序 [#](#DATATYPE-ENUM-ORDERING)

列舉型別中各個值的順序，就是建立該型別時列出這些值的順序。所有標準的比較運算子與相關的彙總函式都支援列舉型別。例如：

```

INSERT INTO person VALUES ('Larry', 'sad');
INSERT INTO person VALUES ('Curly', 'ok');
SELECT * FROM person WHERE current_mood > 'sad';
 name  | current_mood
-------+--------------
 Moe   | happy
 Curly | ok
(2 rows)

SELECT * FROM person WHERE current_mood > 'sad' ORDER BY current_mood;
 name  | current_mood
-------+--------------
 Curly | ok
 Moe   | happy
(2 rows)

SELECT name
FROM person
WHERE current_mood = (SELECT MIN(current_mood) FROM person);
 name
-------
 Larry
(1 row)
```

<a id="DATATYPE-ENUM-TYPE-SAFETY"></a>

### 8.7.3. 型別安全 [#](#DATATYPE-ENUM-TYPE-SAFETY)

每一個列舉資料型別都是獨立的，不能與其他列舉型別比較。請看這個例子：

```

CREATE TYPE happiness AS ENUM ('happy', 'very happy', 'ecstatic');
CREATE TABLE holidays (
    num_weeks integer,
    happiness happiness
);
INSERT INTO holidays(num_weeks,happiness) VALUES (4, 'happy');
INSERT INTO holidays(num_weeks,happiness) VALUES (6, 'very happy');
INSERT INTO holidays(num_weeks,happiness) VALUES (8, 'ecstatic');
INSERT INTO holidays(num_weeks,happiness) VALUES (2, 'sad');
ERROR:  invalid input value for enum happiness: "sad"
SELECT person.name, holidays.num_weeks FROM person, holidays
  WHERE person.current_mood = holidays.happiness;
ERROR:  operator does not exist: mood = happiness
```

如果你真的需要做這樣的事情，可以自己撰寫一個自訂的運算子，或是在查詢中加上明確的型別轉換：

```

SELECT person.name, holidays.num_weeks FROM person, holidays
  WHERE person.current_mood::text = holidays.happiness::text;
 name | num_weeks
------+-----------
 Moe  |         4
(1 row)
```

<a id="DATATYPE-ENUM-IMPLEMENTATION-DETAILS"></a>

### 8.7.4. 實作細節 [#](#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

列舉的標籤會區分大小寫，所以 `'happy'` 與 `'HAPPY'` 並不相同。標籤中的空白字元也有意義。

雖然列舉型別主要是設計給靜態的值集合使用，但它仍支援把新的值加入既有的列舉型別，以及重新命名值（請參閱 [ALTER TYPE](../../reference/sql-commands/sql-altertype.md)）。既有的值無法從列舉型別中移除，這些值的排序順序也無法變更，除非把該列舉型別刪除後再重新建立。

一個列舉值在磁碟上佔用四個位元組。列舉值文字標籤的長度，受到編譯進 PostgreSQL 的 `NAMEDATALEN` 設定所限制；在標準的建置中，這表示最多 63 個位元組。

從內部列舉值到文字標籤的對照關係，儲存在系統目錄 [`pg_enum`](../../internals/catalogs/catalog-pg-enum.md) 中。直接查詢這個目錄有時會很有用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-enum.html)（原文版本：18.6；核對日期：2026-09-13）
