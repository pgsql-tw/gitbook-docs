## 第 4 章 SQL 語法

**目錄**

[4.1. 詞彙結構](sql-syntax-lexical.md)
:   [4.1.1. 識別字與關鍵字](sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)

    [4.1.2. 常數](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS)

    [4.1.3. 運算子](sql-syntax-lexical.md#SQL-SYNTAX-OPERATORS)

    [4.1.4. 特殊字元](sql-syntax-lexical.md#SQL-SYNTAX-SPECIAL-CHARS)

    [4.1.5. 註解](sql-syntax-lexical.md#SQL-SYNTAX-COMMENTS)

    [4.1.6. 運算子優先順序](sql-syntax-lexical.md#SQL-PRECEDENCE)

[4.2. 值運算式](sql-expressions.md)
:   [4.2.1. 欄位參照](sql-expressions.md#SQL-EXPRESSIONS-COLUMN-REFS)

    [4.2.2. 位置參數](sql-expressions.md#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)

    [4.2.3. 下標](sql-expressions.md#SQL-EXPRESSIONS-SUBSCRIPTS)

    [4.2.4. 欄位選取](sql-expressions.md#FIELD-SELECTION)

    [4.2.5. 運算子呼叫](sql-expressions.md#SQL-EXPRESSIONS-OPERATOR-CALLS)

    [4.2.6. 函式呼叫](sql-expressions.md#SQL-EXPRESSIONS-FUNCTION-CALLS)

    [4.2.7. 彙總運算式](sql-expressions.md#SYNTAX-AGGREGATES)

    [4.2.8. Window 函式呼叫](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)

    [4.2.9. 型別轉換](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS)

    [4.2.10. 定序運算式](sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS)

    [4.2.11. 純量子查詢](sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES)

    [4.2.12. 陣列建構子](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)

    [4.2.13. 資料列建構子](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)

    [4.2.14. 運算式求值規則](sql-expressions.md#SYNTAX-EXPRESS-EVAL)

[4.3. 呼叫函式](sql-syntax-calling-funcs.md)
:   [4.3.1. 使用位置表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)

    [4.3.2. 使用具名表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-NAMED)

    [4.3.3. 使用混合表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-MIXED)

<a id="id-1.5.3.2"></a>

本章說明 SQL 的語法。它是理解後續各章的基礎，後續各章會詳細說明如何運用 SQL 指令來定義與修改資料。

我們也建議已經熟悉 SQL 的使用者仔細閱讀本章，因為其中包含一些在各 SQL 資料庫之間實作並不一致，或是 PostgreSQL 特有的規則與概念。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax.html)（原文版本：18.6；核對日期：2026-09-11）
