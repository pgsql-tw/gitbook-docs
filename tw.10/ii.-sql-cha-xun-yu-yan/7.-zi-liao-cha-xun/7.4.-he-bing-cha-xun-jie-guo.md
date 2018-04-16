# 7.4. 合併查詢結果

兩個查詢的結果可以使用集合操作聯、交集和差集來組合。其語法為：

```text
query1 UNION [ALL] query2
query1 INTERSECT [ALL] query2
query1 EXCEPT [ALL]query2
```

query1 和 query2 是到目前為止討論過的任何查詢功能。集合操作也可以巢狀也可以連接，例如：

```text
query1 UNION query2 UNION query3
```

會如下方式執行：

```text
(query1 UNION query2) UNION query3
```

UNION 將 query2 的結果有效率地附加到 query1 的結果中（但不能保證這是實際回傳資料列的次序）。此外，除非使用了UNION ALL，否則它將以與 DISTINCT相同的方式從結果中消除重複的資料列。

INTERSECT 返回 query1 的結果和 query2 的結果中所有共同的資料列。除非使用 INTERSECT ALL，否則會刪除重複的資料列。

EXCEPT 回傳 query1 的結果中但不包含在 query2 的結果中的所有資料列。（這有時被稱為兩個查詢之間的差集。）同樣地，除非使用 EXCEPT ALL，否則重複資料列將被刪除。

為了計算兩個查詢的聯集、交集或差集，兩個查詢必須是「union compatible」，這意味著它們回傳相同數量的欄位，相應的欄位具有相容的資料型別，如 [10.5 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/type-conversion/105-union-case-and-related-constructs.md)所述。

