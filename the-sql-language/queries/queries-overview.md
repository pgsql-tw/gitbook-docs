<a id="QUERIES-OVERVIEW"></a>

## 7.1. 概觀 [#](#QUERIES-OVERVIEW)

從資料庫取出資料的過程或指令，稱為*查詢*（query）。在 SQL 中，使用 [`SELECT`](../../reference/sql-commands/sql-select.md) 指令來指定查詢。`SELECT` 指令的一般語法是

```

[WITH with_queries] SELECT select_list FROM table_expression [sort_specification]
```

以下各節會詳細說明選取清單、資料表運算式與排序規格。`WITH` 查詢屬於進階功能，因此放在最後討論。

一種簡單的查詢形式如下：

```

SELECT * FROM table1;
```

假設有一個名為 `table1` 的資料表，這個指令會取出 `table1` 中的所有資料列與所有使用者定義的欄位。（取出的方式取決於用戶端應用程式。例如，psql 程式會在畫面上顯示一個 ASCII 字元畫出的表格，而用戶端函式庫則會提供從查詢結果中取出個別值的函式。）選取清單規格 `*` 表示資料表運算式所提供的所有欄位。選取清單也可以只選取可用欄位中的一部分，或使用這些欄位進行計算。例如，如果 `table1` 有名為 `a`、`b` 與 `c` 的欄位（或許還有其他欄位），就可以進行下列查詢：

```

SELECT a, b + c FROM table1;
```

（假設 `b` 與 `c` 是數值資料型別。）更多細節請參閱[第 7.3 節](queries-select-lists.md)。

`FROM table1` 是一種簡單的資料表運算式：它只讀取一個資料表。一般而言，資料表運算式可以是由基本資料表、聯結與子查詢組成的複雜結構。但你也可以完全省略資料表運算式，把 `SELECT` 指令當作計算機使用：

```

SELECT 3 * 4;
```

如果選取清單中的運算式會回傳變動的結果，這種用法就更有用了。例如，你可以用這種方式呼叫函式：

```

SELECT random();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-overview.html)（原文版本：18.6；核對日期：2026-09-11）
