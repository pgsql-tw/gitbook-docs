## 第 69 章 規劃器如何使用統計資訊

**目錄**

[69.1. 資料列估計範例](row-estimation-examples.md)

[69.2. 多變量統計資訊範例](multivariate-statistics-examples.md)
:   [69.2.1. Functional Dependencies](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)

    [69.2.2. Multivariate N-Distinct Counts](multivariate-statistics-examples.md#MULTIVARIATE-NDISTINCT-COUNTS)

    [69.2.3. MCV Lists](multivariate-statistics-examples.md#MCV-LISTS)

[69.3. 規劃器統計資訊與安全性](planner-stats-security.md)

本章以[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)與[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)的內容為基礎，進一步說明規劃器如何使用系統統計資訊估計查詢各部分可能傳回的資料列數。這是規劃程序的重要部分，提供成本計算所需的大量原始資料。

本章目的不是詳細記錄程式碼，而是概述其運作方式，讓後續想閱讀程式碼的人更容易上手。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/planner-stats-details.html)（原文版本：18.6；核對日期：2026-09-10）
