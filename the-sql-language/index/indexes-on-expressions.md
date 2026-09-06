# 11.7. 表示式索引

索引欄位不必只是基礎資料表的一個欄位，而是可以是從資料表的一個欄位或多個欄位計算的函數或 scalar 表示式。此功能對於根據計算結果來快速存取資料表非常有用。

例如，進行不區分大小寫的比較的常用方法是使用 lower 函數：

```
SELECT * FROM test1 WHERE lower(col1) = 'value';
```

如果已在 lower(col1) 函數的結果上定義了一個索引，則此查詢可以使用索引：

```
CREATE INDEX test1_lower_col1_idx ON test1 (lower(col1));
```

如果我們要宣告這個索引 UNIQUE，它將阻止建立 col1 值僅在大小寫情況下不同的資料，以及 col1 值實際上相同的資料。因此，表示式上的索引可用於強制執行不能作為簡單唯一性定義的限制條件。

另一個例子，如果經常進行如下查詢：

```
SELECT * FROM people WHERE (first_name || ' ' || last_name) = 'John Smith';
```

那麼可能值得建立這樣的索引：

```
CREATE INDEX people_names ON people ((first_name || ' ' || last_name));
```

CREATE INDEX 指令的語法通常需要在索引表示式使用括號，如第二個範例所示。當表示式只是函數呼叫時，可以省略括號，如第一個範例中所示。

索引表示式的維護成本相對較高，因為必須在插入時和每次更新時為每一行計算衍生表示式。但是，索引表示式在索引搜尋期間不會重新計算，因為它們已儲存在索引中。在上面的兩個範例中，系統將查詢視為 WHERE indexedcolumn ='constant'，因此搜尋速度等同於任何其他簡單索引查詢。因此，當檢索速度比插入和更新速度更重要時，表示式上的索引就很有用。
