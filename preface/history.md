<a id="HISTORY"></a>

## 2. PostgreSQL 簡史 [#](#history) <a href="#history" id="history"></a>

[2.1. 柏克萊 POSTGRES 專案](history.md#HISTORY-BERKELEY)

[2.2. Postgres95](history.md#HISTORY-POSTGRES95)

[2.3. PostgreSQL](history.md#HISTORY-POSTGRESQL)

<a id="id-1.3.5.2"></a>

現在稱為 PostgreSQL 的這套物件關聯式資料庫管理系統，源自加州大學柏克萊分校所撰寫的 POSTGRES 套件。歷經數十年的開發，PostgreSQL 如今是世界上最先進的開放原始碼資料庫。

關於這段歷史的另一種觀點，可以參閱 Joe Hellerstein 博士的論文〈Looking Back at Postgres〉[[hell18]](../bibliography.md#HELL18)。

<a id="HISTORY-BERKELEY"></a>

### 2.1. 柏克萊 POSTGRES 專案 [#](#HISTORY-BERKELEY)

<a id="id-1.3.5.5.2"></a>

POSTGRES 專案由 Michael Stonebraker 教授領導，由美國國防高等研究計劃署（DARPA）、陸軍研究辦公室（ARO）、國家科學基金會（NSF）以及 ESL, Inc. 贊助。POSTGRES 的實作始於 1986 年。系統的最初概念發表於 [[ston86]](../bibliography.md#STON86)，最初資料模型的定義則出現在 [[rowe87]](../bibliography.md#ROWE87)。當時規則系統的設計記述於 [[ston87a]](../bibliography.md#STON87A)。儲存管理器的設計理念與架構則詳述於 [[ston87b]](../bibliography.md#STON87B)。

此後，POSTGRES 經歷了數次主要版本的發布。第一個「展示版」（demoware）系統於 1987 年開始運作，並在 1988 年的 ACM-SIGMOD 研討會上展示。第 1 版（記述於 [[ston90a]](../bibliography.md#STON90A)）於 1989 年 6 月釋出給少數外部使用者。為了回應外界對第一代規則系統的批評（[[ston89]](../bibliography.md#STON89)），規則系統經過重新設計（[[ston90b]](../bibliography.md#STON90B)），而第 2 版於 1990 年 6 月隨新的規則系統一同釋出。第 3 版於 1991 年問世，新增了對多個儲存管理器的支援、改良的查詢執行器，以及重寫的規則系統。在 Postgres95 之前（見下文），後續的版本大多著重於可攜性與可靠性。

POSTGRES 曾被用來實作許多不同的研究與正式環境應用，包括：金融資料分析系統、噴射引擎效能監控套件、小行星追蹤資料庫、醫療資訊資料庫，以及數個地理資訊系統。POSTGRES 也曾在數所大學作為教學工具。最後，Illustra Information Technologies（後來併入 [Informix](https://www.ibm.com/analytics/informix)，而 Informix 現在屬於 [IBM](https://www.ibm.com/)）取得了這份程式碼並將其商業化。1992 年底，POSTGRES 成為 [[ston92]](../bibliography.md#STON92) 中所述 Sequoia 2000 科學運算專案的主要資料管理器。

1993 年間，外部使用者社群的規模幾乎倍增。情況變得愈來愈明顯：維護原型程式碼與提供支援，占用了大量原本應該投入資料庫研究的時間。為了減輕這項支援負擔，柏克萊 POSTGRES 專案以第 4.2 版正式畫下句點。

<a id="HISTORY-POSTGRES95"></a>

### 2.2. Postgres95 [#](#HISTORY-POSTGRES95)

<a id="id-1.3.5.6.2"></a>

1994 年，Andrew Yu 與 Jolly Chen 為 POSTGRES 加入了 SQL 語言直譯器。隨後，它以新名稱 Postgres95 發布到網路上，作為原始柏克萊 POSTGRES 程式碼的開放原始碼後裔，在世界上闖出自己的路。

Postgres95 的程式碼完全是 ANSI C，大小也縮減了 25%。許多內部變更改善了效能與可維護性。在 Wisconsin Benchmark 上，Postgres95 1.0.x 版的執行速度比 POSTGRES 第 4.2 版快約 30–50%。除了錯誤修正之外，主要的改進如下：

* 查詢語言 PostQUEL 被 SQL（在伺服器中實作）取代。（介面程式庫 [libpq](../client-interfaces/libpq/README.md) 是以 PostQUEL 命名的。）子查詢直到 PostgreSQL 才獲得支援（見下文），但在 Postgres95 中可以用使用者自訂的 SQL 函式來模擬。彙總函式經過重新實作。此外也新增了對 `GROUP BY` 查詢子句的支援。
* 提供了一個新程式（psql），用於互動式 SQL 查詢，它使用 GNU Readline。這在很大程度上取代了舊的 monitor 程式。
* 新的前端程式庫 `libpgtcl` 支援以 Tcl 為基礎的用戶端。一個範例 shell `pgtclsh` 提供了新的 Tcl 命令，讓 Tcl 程式能與 Postgres95 伺服器介接。
* 大型物件介面經過全面翻修。inversion 大型物件成為儲存大型物件的唯一機制。（inversion 檔案系統已被移除。）
* 移除了實例層級（instance-level）的規則系統。規則仍以重寫規則的形式提供。
* 原始碼隨附了一份簡短的教學，介紹一般的 SQL 功能以及 Postgres95 的功能。
* 建置時使用 GNU make（而非 BSD make）。此外，Postgres95 可以用未經修補的 GCC 編譯（double 的資料對齊問題已修正）。

<a id="HISTORY-POSTGRESQL"></a>

### 2.3. PostgreSQL [#](#HISTORY-POSTGRESQL)

到了 1996 年，顯然「Postgres95」這個名稱經不起時間的考驗。我們選擇了新名稱 PostgreSQL，以反映最初的 POSTGRES 與較新、具備 SQL 能力的版本之間的關係。同時，我們將版本編號設定為從 6.0 開始，讓編號回到柏克萊 POSTGRES 專案最初開始的序列上。

Postgres 仍被視為正式的專案名稱，一方面是基於傳統，另一方面是因為人們覺得 Postgres 比 PostgreSQL 更容易發音。

Postgres95 開發期間的重點，在於找出並理解伺服器程式碼中既有的問題。到了 PostgreSQL，重點已轉向擴增功能與能力，不過各方面的工作仍持續進行。

此後每個 PostgreSQL 版本的變更詳情，可以在 <https://www.postgresql.org/docs/release/> 找到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/history.html)（原文版本：18.6；核對日期：2026-10-09）
