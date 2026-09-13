## 第 39 章 規則系統

**目錄**

[39.1. 查詢樹](querytree.md)

[39.2. 檢視表與規則系統](rules-views.md)
:   [39.2.1. `SELECT` 規則如何運作](rules-views.md#RULES-SELECT)

    [39.2.2. 非 `SELECT` 陳述式中的檢視表規則](rules-views.md#RULES-VIEWS-NON-SELECT)

    [39.2.3. PostgreSQL 中檢視表的威力](rules-views.md#RULES-VIEWS-POWER)

    [39.2.4. 更新檢視表](rules-views.md#RULES-VIEWS-UPDATE)

[39.3. 具體化檢視表](rules-materializedviews.md)

[39.4. `INSERT`、`UPDATE` 與 `DELETE` 上的規則](rules-update.md)
:   [39.4.1. 更新規則如何運作](rules-update.md#RULES-UPDATE-HOW)

    [39.4.2. 與檢視表的搭配](rules-update.md#RULES-UPDATE-VIEWS)

[39.5. 規則與權限](rules-privileges.md)

[39.6. 規則與指令狀態](rules-status.md)

[39.7. 規則與觸發程序的比較](rules-triggers.md)

<a id="id-1.8.6.2"></a>

本章討論 PostgreSQL 中的規則系統。產生式規則系統（production rule system）在概念上很簡單，但實際使用時會牽涉到許多微妙之處。

某些其他資料庫系統定義了主動式資料庫規則，那些通常是預存程序與觸發程序。在 PostgreSQL 中，這些同樣可以用函式與觸發程序來實作。

規則系統（更精確地說，是查詢重寫規則系統）與預存程序及觸發程序完全不同。它會修改查詢以將規則納入考量，然後把修改後的查詢交給查詢規劃器進行規劃與執行。它非常強大，可以用在許多地方，例如查詢語言程序、檢視表與版本。這套規則系統的理論基礎與威力，在 [[ston90b]](../../bibliography.md#STON90B) 與 [[ong90]](../../bibliography.md#ONG90) 中也有討論。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules.html)（原文版本：18.6；核對日期：2026-09-13）
