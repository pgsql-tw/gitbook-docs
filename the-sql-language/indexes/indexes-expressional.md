<a id="INDEXES-EXPRESSIONAL"></a>

## 11.7. 運算式索引 [#](#INDEXES-EXPRESSIONAL)

<a id="id-1.5.10.10.2"></a>

索引欄位不一定只能是底層資料表的欄位，也可以是由資料表的一個或多個欄位計算出來的函式或純量運算式。這項功能可用於根據計算結果快速存取資料表。

例如，進行不區分大小寫之比較的一種常見方式，是使用 `lower` 函式：

```

SELECT * FROM test1 WHERE lower(col1) = 'value';
```

如果已經在 `lower(col1)` 函式的結果上定義了索引，這個查詢就可以使用該索引：

```

CREATE INDEX test1_lower_col1_idx ON test1 (lower(col1));
```

如果我們將這個索引宣告為 `UNIQUE`，它就會阻止建立 `col1` 值只有大小寫不同的資料列，以及 `col1` 值實際上完全相同的資料列。因此，運算式索引可以用來強制執行無法以簡單唯一限制條件定義的限制。

再舉一個例子，如果你經常進行像這樣的查詢：

```

SELECT * FROM people WHERE (first_name || ' ' || last_name) = 'John Smith';
```

那麼建立像這樣的索引可能是值得的：

```

CREATE INDEX people_names ON people ((first_name || ' ' || last_name));
```

`CREATE INDEX` 命令的語法通常要求在索引運算式外加上括號，如第二個範例所示。當運算式只是一個函式呼叫時，可以省略括號，如第一個範例所示。

索引運算式的維護成本相對較高，因為每次插入資料列以及每次[非 HOT 更新](../../internals/storage/storage-hot.md)時，都必須計算衍生出來的運算式。不過，在使用索引的搜尋中，索引運算式*不會*重新計算，因為它們已經儲存在索引中了。在上面兩個範例中，系統都會將查詢單純視為 `WHERE indexedcolumn = 'constant'`，因此搜尋的速度與任何其他簡單的索引查詢相當。所以，當擷取速度比插入與更新速度更重要時，運算式索引就很有用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-expressional.html)（原文版本：18.6；核對日期：2026-09-11）
