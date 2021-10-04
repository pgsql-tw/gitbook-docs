# dblink\_send\_query

dblink\_send\_query — 送出非同步的查詢到遠端資料庫

### 語法

```text
dblink_send_query(text connname, text sql) returns int
```

### 說明

dblink\_send\_query 發送查詢以非同步方式執行，意即毋須等待指令結果。 連線上必須沒有其他正在進行的非同步查詢。

成功呼叫非同步查詢後，可以使用 dblink\_is\_busy 檢查完成狀態，並在最後使用 dblink\_get\_result 收集查詢結果。也可以嘗試使用 dblink\_cancel\_query 取消正在進行的非同步查詢。

### 參數

_`connname`_

要使用的連線名稱。

_`sql`_

您希望在遠端資料庫中執行的 SQL 語句，例如，從 `select * from pg_class`。

### 回傳值

如果已成功開始執行查詢，則回傳 1，否則回傳 0。

### 範例

```text
SELECT dblink_send_query('dtest1', 'SELECT * FROM foo WHERE f1 < 3');
```

