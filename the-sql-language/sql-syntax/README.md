## 第 4 章 SQL 語法

**目錄**

- [4.1. 詞彙結構](sql-syntax-lexical.md)
  - [4.1.1. 識別字與關鍵字](sql-syntax-lexical.md#sql-syntax-identifiers)

  - [4.1.2. 常數](sql-syntax-lexical.md#sql-syntax-constants)

  - [4.1.3. 運算子](sql-syntax-lexical.md#sql-syntax-operators)

  - [4.1.4. 特殊字元](sql-syntax-lexical.md#sql-syntax-special-chars)

  - [4.1.5. 註解](sql-syntax-lexical.md#sql-syntax-comments)

  - [4.1.6. 運算子優先順序](sql-syntax-lexical.md#sql-precedence)

- [4.2. 值運算式](sql-expressions.md)
  - [4.2.1. 欄位參照](sql-expressions.md#sql-expressions-column-refs)

  - [4.2.2. 位置參數](sql-expressions.md#sql-expressions-parameters-positional)

  - [4.2.3. 下標](sql-expressions.md#sql-expressions-subscripts)

  - [4.2.4. 欄位選取](sql-expressions.md#field-selection)

  - [4.2.5. 運算子呼叫](sql-expressions.md#sql-expressions-operator-calls)

  - [4.2.6. 函式呼叫](sql-expressions.md#sql-expressions-function-calls)

  - [4.2.7. 彙總運算式](sql-expressions.md#syntax-aggregates)

  - [4.2.8. Window 函式呼叫](sql-expressions.md#syntax-window-functions)

  - [4.2.9. 型別轉換](sql-expressions.md#sql-syntax-type-casts)

  - [4.2.10. 定序運算式](sql-expressions.md#sql-syntax-collate-exprs)

  - [4.2.11. 純量子查詢](sql-expressions.md#sql-syntax-scalar-subqueries)

  - [4.2.12. 陣列建構子](sql-expressions.md#sql-syntax-array-constructors)

  - [4.2.13. 資料列建構子](sql-expressions.md#sql-syntax-row-constructors)

  - [4.2.14. 運算式求值規則](sql-expressions.md#syntax-express-eval)

- [4.3. 呼叫函式](sql-syntax-calling-funcs.md)
  - [4.3.1. 使用位置表示法](sql-syntax-calling-funcs.md#sql-syntax-calling-funcs-positional)

  - [4.3.2. 使用具名表示法](sql-syntax-calling-funcs.md#sql-syntax-calling-funcs-named)

  - [4.3.3. 使用混合表示法](sql-syntax-calling-funcs.md#sql-syntax-calling-funcs-mixed)

<a id="id-1.5.3.2"></a>

本章說明 SQL 的語法。它是理解後續各章的基礎，後續各章會詳細說明如何運用 SQL 指令來定義與修改資料。

我們也建議已經熟悉 SQL 的使用者仔細閱讀本章，因為其中包含一些在各 SQL 資料庫之間實作並不一致，或是 PostgreSQL 特有的規則與概念。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax.html)（原文版本：18.6；核對日期：2026-09-11）
