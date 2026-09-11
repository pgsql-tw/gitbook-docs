<a id="QUERIES-LIMIT"></a>

## 7.6. `LIMIT` 與 `OFFSET` [#](#QUERIES-LIMIT)

<a id="id-1.5.6.10.2"></a><a id="id-1.5.6.10.3"></a>

`LIMIT` 與 `OFFSET` 讓你只取出查詢其餘部分所產生之資料列的一部分：

```

SELECT select_list
    FROM table_expression
    [ ORDER BY ... ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start ]
```

如果給定了限制數量，回傳的資料列就不會超過該數量（但如果查詢本身產生的資料列較少，也可能少於該數量）。`LIMIT ALL` 與省略 `LIMIT` 子句相同，`LIMIT` 的參數為 NULL 時也一樣。

`OFFSET` 表示在開始回傳資料列之前，要先略過該數量的資料列。`OFFSET 0` 與省略 `OFFSET` 子句相同，`OFFSET` 的參數為 NULL 時也一樣。

如果同時出現 `OFFSET` 與 `LIMIT`，會先略過 `OFFSET` 指定數量的資料列，再開始計算要回傳的 `LIMIT` 資料列。

使用 `LIMIT` 時，重要的是要使用 `ORDER BY` 子句，將結果資料列限制在唯一的順序中。否則，你會得到查詢資料列中一個無法預測的子集合。你可能要求的是第十到第二十筆資料列，但這是依什麼順序排出來的第十到第二十筆？除非你指定了 `ORDER BY`，否則順序是未知的。

查詢最佳化器在產生查詢計畫時會考量 `LIMIT`，因此依你給 `LIMIT` 與 `OFFSET` 的值不同，你很可能會得到不同的計畫（產生不同的資料列順序）。因此，除非以 `ORDER BY` 強制可預測的結果順序，否則使用不同的 `LIMIT`/`OFFSET` 值來選取查詢結果的不同子集合，*會產生不一致的結果*。這不是錯誤；這是 SQL 的固有結果：除非使用 `ORDER BY` 限制順序，否則 SQL 不保證以任何特定順序傳回查詢結果。

被 `OFFSET` 子句略過的資料列仍然必須在伺服器內部計算；因此，很大的 `OFFSET` 可能會缺乏效率。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-limit.html)（原文版本：18.6；核對日期：2026-09-11）
