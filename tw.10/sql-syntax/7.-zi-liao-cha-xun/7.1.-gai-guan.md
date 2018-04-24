# 7.1. 概觀

檢索過程或從資料庫檢索資料的命令稱之為查詢。在 SQL 中，SELECT 命令用於進行條件查詢。 SELECT 指令的一般語法是：

```text
[WITH with_queries] SELECT select_list FROM table_expression [sort_specification]
```

以下各節介紹了資料列表（select list），資料表和排序規則的詳細資訊。由於 WITH 查詢是高級功能，因此最後再介紹。

一種簡單的查詢形式如下：

```text
SELECT * FROM table1;
```

假設有一個名稱為 table1 的資料表，該指令會將取出 table1 中的所有資料表和所有用戶定義的欄位。（檢索的方法取決於用戶端的應用程序，例如，psql 程序將在屏幕上顯示一個 ASCII-art 表格，而用戶端的程式函式庫將提供從查詢結果中提取單一值的功能。選擇資料列表定義「\*」表示由資料表表示式所產生的所有欄位。篩選列表可以是可用欄位的子集或使用欄位進行計算。例如，如果 table1 具有名稱為 a，b 和 c（也許是其他）的欄位，則可以進行以下查詢：

```text
SELECT a, b + c FROM table1;
```

（假設 b 和 c 是數字型別）。更多細節詳見 [7.3 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/queries/73-select-lists.md)。

FROM table1是一種簡單的資料表表示式：它只讀取一個資料表。一般來說，資料表表示式可以是一般的資料表，交叉查詢和子查詢的複雜結構。但是，你也可以完全省略資料表表示式，並使用 SELECT 指令作為計算機：

```text
SELECT 3 * 4;
```

使用資料列表中的表達式產生變動的結果，是更為常用的方式。例如，你可以這樣呼叫一個函數：

```text
SELECT random();
```

