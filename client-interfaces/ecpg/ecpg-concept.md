<a id="ECPG-CONCEPT"></a>

## 34.1. 概念 [#](#ecpg-concept) <a href="#ecpg-concept" id="ecpg-concept"></a>

嵌入式 SQL 程式由以一般程式語言（此處為 C）撰寫的程式碼，與位於特別標記區段中的 SQL 命令混合組成。建置程式時，原始碼（`*.pgc`）會先經過嵌入式 SQL 前置處理器，轉換成一般的 C 程式（`*.c`），之後即可由 C 編譯器處理。（關於編譯與連結的細節，請參閱[第 34.10 節](ecpg-process.md)。）轉換後的 ECPG 應用程式會透過嵌入式 SQL 函式庫（ecpglib）呼叫 libpq 函式庫中的函式，並使用一般的前端／後端協定與 PostgreSQL 伺服器通訊。

相較於從 C 程式碼處理 SQL 命令的其他方法，嵌入式 SQL 有幾項優點。第一，它會替你處理在 C 程式的變數之間傳入與傳出資訊這項繁瑣的工作。第二，程式中的 SQL 程式碼會在建置時檢查語法是否正確。第三，C 語言中的嵌入式 SQL 已在 SQL 標準中規範，並受到許多其他 SQL 資料庫系統支援。PostgreSQL 的實作設計上盡可能符合此標準，通常可以相對輕鬆地把為其他 SQL 資料庫撰寫的嵌入式 SQL 程式移植到 PostgreSQL。

如前所述，為嵌入式 SQL 介面撰寫的程式就是一般的 C 程式，只是插入了執行資料庫相關動作的特殊程式碼。這種特殊程式碼一律採用下列形式：

```

EXEC SQL ...;
```

這些陳述式在語法上占據 C 陳述式的位置。視個別陳述式而定，它們可以出現在全域層級，也可以出現在函式內。

嵌入式 SQL 陳述式遵循一般 SQL 程式碼的大小寫區分規則，而不是 C 的規則。此外，它們依照 SQL 標準允許巢狀的 C 風格註解。然而，程式的 C 部分仍遵循 C 標準，不接受巢狀註解。嵌入式 SQL 陳述式同樣使用 SQL 規則（而不是 C 規則）來剖析加上引號的字串與識別字。（分別請參閱[第 4.1.2.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)與[第 4.1.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)。請注意，ECPG 假設 `standard_conforming_strings` 為 `on`。）當然，程式的 C 部分遵循 C 的引號規則。

以下各節將說明所有的嵌入式 SQL 陳述式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-concept.html)（原文版本：18.6；核對日期：2026-10-22）
