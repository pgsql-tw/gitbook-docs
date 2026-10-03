<a id="SQL-DELETE"></a><a id="id-1.9.3.100.1"></a>

## DELETE

DELETE — 刪除資料表中的資料列

<a id="id-1.9.3.100.4"></a>

## 語法

```

[ WITH [ RECURSIVE ] with_query [, ...] ]
DELETE FROM [ ONLY ] table_name [ * ] [ [ AS ] alias ]
    [ USING from_item [, ...] ]
    [ WHERE condition | WHERE CURRENT OF cursor_name ]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

<a id="id-1.9.3.100.5"></a>

## 說明

`DELETE` 會從指定的資料表中刪除滿足 `WHERE` 子句的資料列。若沒有 `WHERE` 子句，效果就是刪除資料表中的所有資料列。結果會是一個有效但空的資料表。

### 提示

[`TRUNCATE`](sql-truncate.md) 提供了一種更快速的機制，可以移除資料表中的所有資料列。

要使用資料庫中其他資料表所包含的資訊來刪除資料表中的資料列，有兩種方式：使用子查詢，或在 `USING` 子句中指定額外的資料表。哪一種技巧較為合適，取決於具體情況。

選用的 `RETURNING` 子句會讓 `DELETE` 根據每一筆實際被刪除的資料列，計算並傳回值。可以計算任何使用該資料表欄位，及／或 `USING` 中提及之其他資料表欄位的運算式。`RETURNING` 清單的語法與 `SELECT` 的輸出清單語法相同。

您必須擁有資料表的 `DELETE` 權限才能從中刪除資料列；對於 `USING` 子句中的任何資料表，或其值會在 *`condition`* 中被讀取的任何資料表，也必須擁有 `SELECT` 權限。

<a id="id-1.9.3.100.6"></a>

## 參數

*`with_query`*
:   `WITH` 子句可讓您指定一個或多個子查詢，並在 `DELETE` 查詢中以名稱參照它們。詳情請參閱[第 7.8 節](../../the-sql-language/queries/queries-with.md)與 [SELECT](sql-select.md)。

*`table_name`*
:   要從中刪除資料列之資料表的名稱（可選擇以綱要限定）。若在資料表名稱之前指定 `ONLY`，則只會從指名的資料表中刪除符合的資料列。若未指定 `ONLY`，則也會從繼承自指名資料表的任何資料表中刪除符合的資料列。也可以選擇在資料表名稱之後指定 `*`，以明確表示包含後代資料表。

*`alias`*
:   目標資料表的替代名稱。若提供了別名，就會完全隱藏該資料表的實際名稱。例如，給定 `DELETE FROM foo AS f` 時，`DELETE` 陳述式的其餘部分必須以 `f` 而非 `foo` 來參照此資料表。

*`from_item`*
:   一個資料表運算式，讓其他資料表的欄位得以出現在 `WHERE` 條件中。這使用的語法與 `SELECT` 陳述式的 [`FROM`](sql-select.md#SQL-FROM) 子句相同；例如，可以為資料表名稱指定別名。除非您想建立自我連接（在這種情況下，目標資料表必須以別名出現在 *`from_item`* 中），否則不要將目標資料表重複列為 *`from_item`*。

*`condition`*
:   傳回 `boolean` 型別值的運算式。只有這個運算式傳回 `true` 的資料列才會被刪除。

*`cursor_name`*
:   在 `WHERE CURRENT OF` 條件中使用的游標名稱。要刪除的資料列是最近一次從這個游標擷取出的那一列。這個游標必須是針對 `DELETE` 目標資料表的非分組查詢。請注意，`WHERE CURRENT OF` 不能與布林條件一起指定。關於在 `WHERE CURRENT OF` 中使用游標的更多資訊，請參閱 [DECLARE](sql-declare.md)。

*`output_alias`*
:   `RETURNING` 清單中 `OLD` 或 `NEW` 資料列的選用替代名稱。

    依預設，可以撰寫 `OLD.column_name` 或 `OLD.*` 來傳回目標資料表的舊值，也可以撰寫 `NEW.column_name` 或 `NEW.*` 來傳回新值。若提供了別名，這些名稱就會被隱藏，必須改用該別名來參照舊資料列或新資料列。例如 `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`。

*`output_expression`*
:   每筆資料列刪除後，要由 `DELETE` 命令計算並傳回的運算式。此運算式可以使用 *`table_name`* 所指名之資料表，或 `USING` 中列出之資料表的任何欄位名稱。撰寫 `*` 可傳回所有欄位。

    欄位名稱或 `*` 可以使用 `OLD` 或 `NEW`，或是對應於 `OLD` 或 `NEW` 的 *`output_alias`* 加以限定，以傳回舊值或新值。未加限定的欄位名稱、`*`，或是以目標資料表名稱或別名限定的欄位名稱或 `*`，則會傳回舊值。

    對於單純的 `DELETE`，所有新值都會是 `NULL`。不過，若 `ON DELETE` 規則導致改為執行 `INSERT` 或 `UPDATE`，新值則可能不是 `NULL`。

*`output_name`*
:   用於所傳回欄位的名稱。

<a id="id-1.9.3.100.7"></a>

## 輸出

成功完成後，`DELETE` 命令會傳回下列形式的命令標籤

```

DELETE count
```

*`count`* 是被刪除的資料列數。請注意，當刪除被 `BEFORE DELETE` 觸發程序抑制時，這個數字可能會少於符合 *`condition`* 的資料列數。若 *`count`* 為 0，表示查詢未刪除任何資料列（這不會被視為錯誤）。

若 `DELETE` 命令含有 `RETURNING` 子句，其結果會類似於一個 `SELECT` 陳述式的結果，包含 `RETURNING` 清單中定義的欄位與值，並以該命令所刪除的資料列來計算。

<a id="id-1.9.3.100.8"></a>

## 注意事項

PostgreSQL 允許您在 `USING` 子句中指定其他資料表，藉此在 `WHERE` 條件中參照其他資料表的欄位。例如，若要刪除某位製作人所製作的所有影片，可以這樣做：

```

DELETE FROM films USING producers
  WHERE producer_id = producers.id AND producers.name = 'foo';
```

這裡實際上發生的，是 `films` 與 `producers` 之間的連接，所有成功連接的 `films` 資料列都會被標記為要刪除。這種語法並非標準語法。較符合標準的做法是：

```

DELETE FROM films
  WHERE producer_id IN (SELECT id FROM producers WHERE name = 'foo');
```

在某些情況下，連接的寫法會比子查詢的寫法更容易撰寫，或執行速度更快。

<a id="id-1.9.3.100.9"></a>

## 範例

刪除除了音樂劇以外的所有影片：

```

DELETE FROM films WHERE kind <> 'Musical';
```

清空資料表 `films`：

```

DELETE FROM films;
```

刪除已完成的工作，並傳回被刪除資料列的完整詳細資料：

```

DELETE FROM tasks WHERE status = 'DONE' RETURNING *;
```

刪除游標 `c_tasks` 目前所在位置的那一筆 `tasks` 資料列：

```

DELETE FROM tasks WHERE CURRENT OF c_tasks;
```

雖然 `DELETE` 沒有 `LIMIT` 子句，但可以使用 [`UPDATE` 說明文件](sql-update.md#UPDATE-LIMIT)中所述的相同方法，達到類似的效果：

```

WITH delete_batch AS (
  SELECT l.ctid FROM user_logs AS l
    WHERE l.status = 'archived'
    ORDER BY l.creation_date
    FOR UPDATE
    LIMIT 10000
)
DELETE FROM user_logs AS dl
  USING delete_batch AS del
  WHERE dl.ctid = del.ctid;
```

這種 `ctid` 的用法之所以安全，只是因為該查詢會重複執行，從而避免了 `ctid` 已變更的問題。

<a id="id-1.9.3.100.10"></a>

## 相容性

此命令符合 SQL 標準，但 `USING` 與 `RETURNING` 子句是 PostgreSQL 擴充功能，在 `DELETE` 中使用 `WITH` 的能力也是。

<a id="id-1.9.3.100.11"></a>

## 另請參閱

[TRUNCATE](sql-truncate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-delete.html)（原文版本：18.6；核對日期：2026-10-03）
