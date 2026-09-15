<a id="INDEXES-INTRO"></a>

## 11.1. 簡介 [#](#INDEXES-INTRO)

假設我們有一個類似這樣的資料表：

```

CREATE TABLE test1 (
    id integer,
    content varchar
);
```

而應用程式會發出許多這種形式的查詢：

```

SELECT content FROM test1 WHERE id = constant;
```

如果沒有事先做任何準備，系統就必須逐筆掃描整個 `test1` 資料表，才能找出所有相符的項目。如果 `test1` 中有很多資料列，而這樣的查詢只會回傳少數幾筆（也許是零筆或一筆），這顯然是沒有效率的方法。但如果已經指示系統在 `id` 欄位上維護一個索引，它就能使用更有效率的方法來找出相符的資料列。例如，它可能只需要往搜尋樹中走幾層即可。

大多數非小說類書籍也採用類似的做法：讀者經常查閱的詞彙與概念，會依字母順序收錄在書末的索引中。有興趣的讀者可以相對快速地瀏覽索引，並翻到對應的頁面，而不必讀完整本書才找到感興趣的內容。正如預先設想讀者可能會查閱哪些項目是作者的工作，預先判斷哪些索引會有用，則是資料庫程式設計人員的工作。

如前所述，可以使用下列命令在 `id` 欄位上建立索引：

```

CREATE INDEX test1_id_index ON test1 (id);
```

名稱 `test1_id_index` 可以自由選擇，但你應該挑一個之後能讓你記起這個索引用途的名稱。

要移除索引，請使用 `DROP INDEX` 命令。索引可以隨時加入資料表或從資料表移除。

索引建立之後，就不需要再做任何處理：系統會在資料表被修改時更新索引，並在它認為使用索引會比循序掃描資料表更有效率時，在查詢中使用索引。不過，你可能需要定期執行 `ANALYZE` 命令來更新統計資訊，讓查詢規劃器能夠做出有根據的決策。關於如何得知索引是否被使用，以及規劃器何時、為何可能選擇*不*使用索引，請參閱[第 14 章](../performance-tips/README.md)。

索引也能讓帶有搜尋條件的 `UPDATE` 與 `DELETE` 命令受益。此外，索引也可以用於聯結搜尋。因此，在屬於聯結條件一部分的欄位上所定義的索引，也可以大幅加快含有聯結的查詢。

一般而言，PostgreSQL 索引可以用來最佳化包含一個或多個下列形式之 `WHERE` 或 `JOIN` 子句的查詢

```

indexed-column indexable-operator comparison-value
```

在這裡，*`indexed-column`* 是索引所定義的任何欄位或運算式。*`indexable-operator`* 是屬於被索引欄位之索引*運算子類別*（operator class）成員的運算子。（更多細節會在下面說明。）而 *`comparison-value`* 可以是任何非易變（volatile）且不參照該索引之資料表的運算式。

在某些情況下，查詢規劃器可以從其他 SQL 結構中擷取出這種形式的可索引子句。一個簡單的例子是，如果原本的子句是

```

comparison-value operator indexed-column
```

那麼只要原本的 *`operator`* 有一個屬於該索引之運算子類別成員的交換運算子（commutator），就可以把它翻轉成可索引的形式。

在大型資料表上建立索引可能需要很長的時間。預設情況下，PostgreSQL 允許在建立索引的同時，對該資料表進行讀取（`SELECT` 陳述式），但寫入（`INSERT`、`UPDATE`、`DELETE`）會被阻擋，直到索引建置完成為止。在正式環境中，這通常是無法接受的。可以讓寫入與索引建立同時進行，但有幾項需要注意的事項——更多資訊請參閱[並行建立索引](../../reference/sql-commands/sql-createindex.md#SQL-CREATEINDEX-CONCURRENTLY)。

索引建立之後，系統必須讓它與資料表保持同步。這會為資料操作帶來額外負擔。索引也可能妨礙[僅存於 heap 的 tuple](../../internals/storage/storage-hot.md)（heap-only tuple，HOT）的建立。因此，在查詢中很少使用或從未使用的索引應該移除。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-intro.html)（原文版本：18.6；核對日期：2026-09-13）
