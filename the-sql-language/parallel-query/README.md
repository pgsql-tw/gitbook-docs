## 第 15 章 平行查詢

**目錄**

[15.1. 平行查詢的運作方式](how-parallel-query-works.md)

[15.2. 何時可以使用平行查詢？](when-can-parallel-query-be-used.md)

[15.3. 平行計畫](parallel-plans.md)
:   [15.3.1. 平行掃描](parallel-plans.md#PARALLEL-SCANS)

    [15.3.2. 平行聯結](parallel-plans.md#PARALLEL-JOINS)

    [15.3.3. 平行彙總](parallel-plans.md#PARALLEL-AGGREGATION)

    [15.3.4. 平行 Append](parallel-plans.md#PARALLEL-APPEND)

    [15.3.5. 平行計畫的提示](parallel-plans.md#PARALLEL-PLAN-TIPS)

[15.4. 平行安全性](parallel-safety.md)
:   [15.4.1. 函式與彙總函式的平行標記](parallel-safety.md#PARALLEL-LABELING)

<a id="id-1.5.14.2"></a>

PostgreSQL 可以設計出能運用多個 CPU 的查詢計畫，以便更快地回答查詢。這項功能稱為平行查詢（parallel query）。許多查詢無法從平行查詢中獲益，原因可能是目前實作的限制，也可能是根本想不出比循序查詢計畫更快的查詢計畫。不過，對於能夠獲益的查詢，平行查詢帶來的加速往往非常顯著。許多查詢在使用平行查詢時可以快上兩倍以上，有些查詢甚至可以快上四倍或更多。存取大量資料、但只回傳少數資料列給使用者的查詢，通常獲益最多。本章說明平行查詢如何運作的一些細節，以及在哪些情況下可以使用它，讓想要運用它的使用者能夠瞭解可以期待什麼。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/parallel-query.html)（原文版本：18.6；核對日期：2026-09-11）
