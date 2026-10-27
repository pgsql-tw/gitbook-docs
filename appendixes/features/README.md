<a id="FEATURES"></a>

## 附錄 D. SQL 符合性

**目錄**

- [D.1. 支援的特性](features-sql-standard.md)

- [D.2. 不支援的特性](unsupported-features-sql-standard.md)

- [D.3. XML 限制與 SQL/XML 符合性](xml-limits-conformance.md)
  - [D.3.1. 查詢僅限於 XPath 1.0](xml-limits-conformance.md#functions-xml-limits-xpath1)

  - [D.3.2. 實作上的附帶限制](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)

本節嘗試概述
PostgreSQL 在多大程度上符合現行的 SQL
標準。以下資訊並非完整的符合性聲明，但會以對使用者而言既合理又有用的詳細程度，介紹主要的議題。

SQL 標準的正式名稱是 ISO/IEC 9075「Database
Language SQL」。標準會不時發佈修訂版本；最近一次更新是在 2023 年。
2023 年版稱為 ISO/IEC 9075:2023，或簡稱 SQL:2023。
在此之前的版本有 SQL:2016、SQL:2011、SQL:2008、SQL:2006、SQL:2003、
SQL:1999 與 SQL-92。每個版本都會取代前一個版本，因此宣稱符合較早的版本並沒有正式效力。
PostgreSQL 的開發目標是在不違背傳統特性或常理的前提下，符合最新正式版本的標準。SQL
標準所要求的許多特性都已獲得支援，不過有時語法或功能會略有不同。可以預期隨著時間推移，會朝符合標準的方向進一步邁進。

SQL-92 定義了三個符合性特性集：Entry、Intermediate 與 Full。大多數宣稱符合 SQL 標準的資料庫管理系統，都只符合 Entry 等級，因為 Intermediate 與 Full 等級的完整特性集不是過於龐大，就是與既有行為相衝突。

從 SQL:1999 開始，SQL 標準定義了大量個別的特性，而不再採用 SQL-92 中那三個範圍過廣而成效不彰的等級。這些特性中有一大部分屬於「Core」（核心）特性，每個符合標準的 SQL 實作都必須提供。其餘特性則純屬選用。

標準分為若干部分，每一部分也有一個簡稱：

* ISO/IEC 9075-1 框架（SQL/Framework）

  <a id="id-1.11.5.6.1.1.2"></a>
* ISO/IEC 9075-2 基礎（SQL/Foundation）

  <a id="id-1.11.5.6.1.2.2"></a>
* ISO/IEC 9075-3 呼叫層級介面（SQL/CLI）

  <a id="id-1.11.5.6.1.3.2"></a>
* ISO/IEC 9075-4 永續儲存模組（SQL/PSM）

  <a id="id-1.11.5.6.1.4.2"></a>
* ISO/IEC 9075-9 外部資料管理（SQL/MED）

  <a id="id-1.11.5.6.1.5.2"></a>
* ISO/IEC 9075-10 物件語言繫結（SQL/OLB）

  <a id="id-1.11.5.6.1.6.2"></a>
* ISO/IEC 9075-11 資訊與定義綱要（SQL/Schemata）

  <a id="id-1.11.5.6.1.7.2"></a>
* ISO/IEC 9075-13 使用 Java 語言的常式與型別（SQL/JRT）

  <a id="id-1.11.5.6.1.8.2"></a>
* ISO/IEC 9075-14 XML 相關規範（SQL/XML）

  <a id="id-1.11.5.6.1.9.2"></a>
* ISO/IEC 9075-15 多維陣列（SQL/MDA）

  <a id="id-1.11.5.6.1.10.2"></a>
* ISO/IEC 9075-16 屬性圖查詢（SQL/PGQ）

  <a id="id-1.11.5.6.1.11.2"></a>

請注意，有些部分編號未被使用（或已不再使用）。

PostgreSQL 核心涵蓋第 1、2、9、
11 與 14 部分。第 3 部分由 ODBC 驅動程式涵蓋，第 13 部分則由
PL/Java 外掛涵蓋，但這些元件目前並未驗證其確切的符合程度。目前
PostgreSQL 沒有第 4、10、15 與 16 部分的實作。

PostgreSQL 支援 SQL:2023 的大部分主要特性。在完整符合 Core 所需的
177 項必要特性中，
PostgreSQL 至少符合 170 項。此外，還支援一長串的選用特性。值得一提的是，在撰寫本文時，沒有任何資料庫管理系統的現行版本宣稱完全符合 Core SQL:2023。

在接下來的兩節中，我們會先列出
PostgreSQL 支援的特性，接著列出 SQL:2023 中定義但
PostgreSQL 尚未支援的特性。
這兩份清單都只是近似的：列為支援的特性，可能仍有部分細節不符合標準；而不支援的特性，實際上可能已實作了其中一大部分。
文件的正文部分永遠提供關於哪些功能可用、哪些不可用的最準確資訊。

### 注意

含有連字號的特性代碼是子特性。因此，若某個子特性不受支援，即使其他部分子特性已受支援，其主特性仍會列為不支援。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/features.html)（原文版本：18.6；核對日期：2026-10-22）
