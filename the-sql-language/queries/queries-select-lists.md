<a id="QUERIES-SELECT-LISTS"></a>

## 7.3. 選取清單 [#](#QUERIES-SELECT-LISTS)

[7.3.1. 選取清單項目](queries-select-lists.md#QUERIES-SELECT-LIST-ITEMS)

[7.3.2. 欄位標籤](queries-select-lists.md#QUERIES-COLUMN-LABELS)

[7.3.3. `DISTINCT`](queries-select-lists.md#QUERIES-DISTINCT)

<a id="id-1.5.6.7.2"></a>

如前一節所示，`SELECT` 指令中的資料表運算式會透過組合資料表、檢視表、排除資料列、分組等方式，建構出一個中間的虛擬資料表。這個資料表最後會交給*選取清單*（select list）處理。選取清單決定中間資料表的哪些*欄位*實際上會被輸出。

<a id="QUERIES-SELECT-LIST-ITEMS"></a>

### 7.3.1. 選取清單項目 [#](#QUERIES-SELECT-LIST-ITEMS)

<a id="id-1.5.6.7.4.2"></a>

最簡單的選取清單是 `*`，它會輸出資料表運算式所產生的所有欄位。否則，選取清單是以逗號分隔的值運算式清單（值運算式的定義見[第 4.2 節](../sql-syntax/sql-expressions.md)）。例如，它可以是欄位名稱的清單：

```

SELECT a, b, c FROM ...
```

欄位名稱 `a`、`b` 與 `c`，要嘛是 `FROM` 子句中所參照資料表之欄位的實際名稱，要嘛是依[第 7.2.1.2 節](queries-table-expressions.md#QUERIES-TABLE-ALIASES)所述賦予它們的別名。選取清單中可用的名稱空間與 `WHERE` 子句相同；但如果使用了分組，則與 `HAVING` 子句相同。

如果有多個資料表具有相同名稱的欄位，就必須同時提供資料表名稱，例如：

```

SELECT tbl1.a, tbl2.a, tbl1.b FROM ...
```

處理多個資料表時，要求取得特定資料表的所有欄位也可能很有用：

```

SELECT tbl1.*, tbl2.a FROM ...
```

關於 *`table_name`*`.*` 表示法的更多資訊，請參閱[第 8.16.5 節](../datatype/rowtypes.md#ROWTYPES-USAGE)。

如果在選取清單中使用了任意的值運算式，在概念上它會在回傳的資料表中加入一個新的虛擬欄位。值運算式會對每一筆結果資料列求值一次，其中的欄位參照會以該資料列的值代入。但選取清單中的運算式不一定要參照 `FROM` 子句之資料表運算式中的任何欄位；例如，它們也可以是常數算術運算式。

<a id="QUERIES-COLUMN-LABELS"></a>

### 7.3.2. 欄位標籤 [#](#QUERIES-COLUMN-LABELS)

<a id="id-1.5.6.7.5.2"></a>

可以為選取清單中的項目指定名稱，以供後續處理使用，例如用在 `ORDER BY` 子句中，或供用戶端應用程式顯示。例如：

```

SELECT a AS value, b + c AS sum FROM ...
```

如果沒有使用 `AS` 指定輸出欄位名稱，系統會指派一個預設的欄位名稱。對於簡單的欄位參照，這是所參照欄位的名稱。對於函式呼叫，這是函式的名稱。對於複雜的運算式，系統會產生一個通用的名稱。

`AS` 關鍵字通常是選用的，但在某些情況下，如果想要的欄位名稱與 PostgreSQL 的關鍵字相同，就必須寫 `AS` 或將欄位名稱加上雙引號，以避免歧義。（[附錄 C](../../appendixes/sql-keywords-appendix/README.md) 列出了哪些關鍵字作為欄位標籤時需要使用 `AS`。）例如，`FROM` 就是這樣的關鍵字，因此下列寫法行不通：

```

SELECT a from, b + c AS sum FROM ...
```

但下列任一種寫法都可以：

```

SELECT a AS from, b + c AS sum FROM ...
SELECT a "from", b + c AS sum FROM ...
```

為了盡可能避免未來新增關鍵字時可能產生的問題，建議你一律寫 `AS`，或將輸出欄位名稱加上雙引號。

### 注意

這裡的輸出欄位命名，與在 `FROM` 子句中所做的命名不同（請參閱[第 7.2.1.2 節](queries-table-expressions.md#QUERIES-TABLE-ALIASES)）。同一個欄位可以被重新命名兩次，但傳遞下去的是在選取清單中指派的名稱。

<a id="QUERIES-DISTINCT"></a>

### 7.3.3. `DISTINCT` [#](#QUERIES-DISTINCT)

<a id="id-1.5.6.7.6.2"></a><a id="id-1.5.6.7.6.3"></a><a id="id-1.5.6.7.6.4"></a>

選取清單處理完之後，可以選擇對結果資料表進行重複資料列的排除。要指定這一點，請在 `SELECT` 之後直接寫上 `DISTINCT` 關鍵字：

```

SELECT DISTINCT select_list ...
```

（也可以用關鍵字 `ALL` 取代 `DISTINCT`，以指定保留所有資料列的預設行為。）

<a id="id-1.5.6.7.6.6"></a>

顯然，如果兩筆資料列至少有一個欄位值不同，它們就被視為不同的資料列。在這項比較中，null 值被視為相等。

另外，也可以用任意的運算式來決定哪些資料列要被視為不同：

```

SELECT DISTINCT ON (expression [, expression ...]) select_list ...
```

這裡的 *`expression`* 是對所有資料列求值的任意值運算式。所有運算式都相等的一組資料列會被視為重複，只有該組中的第一筆資料列會保留在輸出中。請注意，除非查詢依足夠多的欄位排序，以確保到達 `DISTINCT` 過濾器的資料列具有唯一的順序，否則一組資料列中的「第一筆資料列」是無法預測的。（`DISTINCT ON` 的處理發生在 `ORDER BY` 排序之後。）

`DISTINCT ON` 子句不是 SQL 標準的一部分，而且由於其結果可能具有不確定性，有時被認為是不好的寫法。只要審慎運用 `GROUP BY` 與 `FROM` 中的子查詢，就可以避免使用這種結構，但它往往是最方便的選擇。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-select-lists.html)（原文版本：18.6；核對日期：2026-09-11）
