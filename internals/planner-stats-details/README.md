## Chapter 69. How the Planner Uses Statistics

**Table of Contents**

[69.1. Row Estimation Examples](row-estimation-examples.md)

[69.2. Multivariate Statistics Examples](multivariate-statistics-examples.md)
:   [69.2.1. Functional Dependencies](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)

    [69.2.2. Multivariate N-Distinct Counts](multivariate-statistics-examples.md#MULTIVARIATE-NDISTINCT-COUNTS)

    [69.2.3. MCV Lists](multivariate-statistics-examples.md#MCV-LISTS)

[69.3. Planner Statistics and Security](planner-stats-security.md)

This chapter builds on the material covered in [Section 14.1](../../the-sql-language/performance-tips/using-explain.md) and [Section 14.2](../../the-sql-language/performance-tips/planner-stats.md) to show some
additional details about how the planner uses the
system statistics to estimate the number of rows each part of a query might
return. This is a significant part of the planning process,
providing much of the raw material for cost calculation.

The intent of this chapter is not to document the code in detail,
but to present an overview of how it works.
This will perhaps ease the learning curve for someone who subsequently
wishes to read the code.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/planner-stats-details.html)（英文原文，待翻譯）
