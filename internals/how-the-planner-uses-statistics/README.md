# 75. 查詢計畫如何使用統計資訊

本章以[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)和[第 14.2 節](../../the-sql-language/performance-tips/statistics-used-by-the-planner.md)介紹的內容為基礎，以顯示有關查詢計畫如何使用系統統計資訊來估計查詢的每個部分可能回傳的資料筆數及其他詳細資訊。這是查詢計劃中的重要過程，它們為計算成本提供了大量原始數據。

本章的目的不是詳細記錄程式語法，而是概述其工作原理。對於以後希望閱讀程式的人來說，這可以降低學習難度。
