## 51.4. PostgreSQL 規則系統 [#](#RULE-SYSTEM)

PostgreSQL 支援強大的*規則系統*，可用來定義*檢視表*與模稜兩可的*檢視表更新*。
最初 PostgreSQL 規則系統有兩種實作：

* 第一種使用*資料列層級*處理，並深植於*執行器*中。每當存取個別資料列時，規則系統便會被呼叫。這項實作在 1995 年 Berkeley Postgres 專案的最後一個正式版本轉為 Postgres95 時移除。
* 第二種規則系統實作是一種稱為*查詢重寫*的技術。*重寫系統*是一個位於*剖析器階段*與*規劃器／最佳化器*之間的模組，至今仍在實作中。

[第 39 章](../../server-programming/rules/README.md)已詳細討論查詢重寫器，因此此處不再說明。我們僅指出，重寫器的輸入與輸出都是查詢樹；也就是說，樹的表示法與語意細節層級不會改變。重寫可視為一種巨集展開。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rule-system.html)（原文版本：18.6；核對日期：2026-09-10）
