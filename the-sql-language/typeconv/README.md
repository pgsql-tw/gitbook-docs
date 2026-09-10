## 第 10 章 型別轉換

**目錄**

[10.1. 概觀](typeconv-overview.md)

[10.2. 運算子](typeconv-oper.md)

[10.3. 函式](typeconv-func.md)

[10.4. 值的儲存](typeconv-query.md)

[10.5. `UNION`、`CASE` 與相關結構](typeconv-union-case.md)

[10.6. `SELECT` 輸出欄位](typeconv-select.md)

<a id="id-1.5.9.2"></a>

SQL 陳述式可能有意或無意地要求在同一個運算式中混用不同資料型別。
PostgreSQL 提供廣泛的功能來評估混合型別的運算式。

許多情況下，使用者不需要瞭解型別轉換機制的細節。然而，PostgreSQL 所執行的
隱含型別轉換可能影響查詢結果。必要時，可以使用*明確*型別轉換來調整這些結果。

本章介紹 PostgreSQL 的型別轉換機制與慣例。特定資料型別及允許使用的函式和
運算子，請參閱[第 8 章](../datatype/README.md)與[第 9 章](../functions/README.md)的相關小節。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv.html)（原文版本：18.6；核對日期：2026-09-10）
