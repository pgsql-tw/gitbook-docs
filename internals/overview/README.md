## 第 51 章 PostgreSQL 內部機制概觀

**目錄**

[51.1. 查詢的路徑](query-path.md)

[51.2. 如何建立連線](connect-estab.md)

[51.3. 剖析器階段](parser-stage.md)
:   [51.3.1. Parser](parser-stage.md#PARSER-STAGE-PARSER)

    [51.3.2. Transformation Process](parser-stage.md#PARSER-STAGE-TRANSFORMATION-PROCESS)

[51.4. PostgreSQL 規則系統](rule-system.md)

[51.5. 規劃器／最佳化器](planner-optimizer.md)
:   [51.5.1. Generating Possible Plans](planner-optimizer.md#PLANNER-OPTIMIZER-GENERATING-POSSIBLE-PLANS)

[51.6. 執行器](executor.md)

### 作者

本章源自 [[sim98]](../../bibliography.md#SIM98) Stefan Simkovics 在維也納科技大學、由 O.Univ.Prof.Dr. Georg Gottlob 與 Univ.Ass. Mag. Katrin Seyr 指導完成的碩士論文。

本章概述 PostgreSQL 後端的內部結構。閱讀下列各節後，你應能瞭解查詢的處理方式。本章旨在協助讀者理解後端從收到查詢到將結果傳回用戶端期間所發生的一般操作順序。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/overview.html)（原文版本：18.6；核對日期：2026-09-10）
