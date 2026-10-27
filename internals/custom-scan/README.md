<a id="CUSTOM-SCAN"></a>

## 第 60 章 撰寫自訂掃描提供者

**目錄**

- [60.1. 建立自訂掃描路徑](custom-scan-path.md)
  - [60.1.1. 自訂掃描路徑回呼函式](custom-scan-path.md#custom-scan-path-callbacks)

- [60.2. 建立自訂掃描計畫](custom-scan-plan.md)
  - [60.2.1. 自訂掃描計畫回呼函式](custom-scan-plan.md#custom-scan-plan-callbacks)

- [60.3. 執行自訂掃描](custom-scan-execution.md)
  - [60.3.1. 自訂掃描執行回呼函式](custom-scan-execution.md#custom-scan-execution-callbacks)

<a id="id-1.10.12.2"></a>

PostgreSQL 支援一組實驗性的功能，目的是讓擴充模組能夠在系統中加入新的掃描類型。[外部資料包裝器](../fdwhandler/README.md)只負責知道如何掃描它自己的外部資料表；與之不同，自訂掃描提供者可以提供另一種方法來掃描系統中的任何關聯。撰寫自訂掃描提供者的動機，通常是為了使用核心系統不支援的某些最佳化，例如快取或某種形式的硬體加速。本章概述如何撰寫新的自訂掃描提供者。

實作新類型的自訂掃描分為三個步驟。首先，在規劃期間，必須產生代表以所提議策略進行掃描的存取路徑。其次，如果規劃器選中其中一條存取路徑，作為掃描特定關聯的最佳策略，就必須將該存取路徑轉換為計畫。最後，必須能夠執行該計畫，並產生與以同一關聯為目標的任何其他存取路徑所會產生的相同結果。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/custom-scan.html)（原文版本：18.6；核對日期：2026-10-17）
